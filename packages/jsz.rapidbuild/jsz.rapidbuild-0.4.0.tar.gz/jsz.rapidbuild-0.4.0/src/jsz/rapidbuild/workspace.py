#!/usr/bin/env
from typing import Any, Union
import yaml
import os.path
import fs.path
from fs.base import FS
from fs.osfs import OSFS
import fs.errors

from . import base
from .base import (
    extend_unique,
    append_unique
)
from .conan import SystemConfigManifestProviderConan
from .fastbuild import BuildScriptEmitterFastbuild
from .target_graph import TargetGraph
from .toolchain import ToolchainSettingsProviderDefault
from .workspace_def import (
    TargetKind,
    WorkspaceDefinition,
    WorkspaceInvalidFormat,
)


def _validate_third_party_manifest(manifest):
    if not isinstance(manifest, dict):
        return False
    return True


def _validate_toolchains_manifest(manifest):
    if not isinstance(manifest, dict):
        return False
    if len(manifest.keys()) == 0:
        return False
    return True


def _validate_toolchains_settings(settings):
    if not isinstance(settings, dict):
        return False
    if len(settings.keys()) == 0:
        return False
    return True


class WorkspaceDependencyError(RuntimeError):
    pass


def _create_targets_interfaces_and_implementations(source_dir_abs_path, toolchains, build_types,
                                                   third_party_manifest, workspace_def: WorkspaceDefinition):
    assert (len(source_dir_abs_path) != 0)
    assert (len(build_types) != 0)
    assert (len(toolchains) != 0)
    assert (_validate_third_party_manifest(third_party_manifest))

    target_graph = TargetGraph(wks_def=workspace_def)
    if not target_graph.is_valid():
        raise WorkspaceDependencyError()

    for toolchain_name in toolchains:
        for build_type in build_types:
            for target_def in workspace_def.targets:
                target_graph.calc_target_iface_impl(target_def.name, source_dir_abs_path, toolchain_name,
                                                    build_type, third_party_manifest)

    return target_graph.targets_interfaces, target_graph.targets_impls


class Workspace:
    def __init__(self, *,
                 name: str,
                 wks_fs: FS,
                 logger: base.Logger,
                 system_config_provider: base.SystemConfigManifestProvider,
                 toolchain_settings_provider: base.ToolchainSettingsProvider,
                 build_script_emitter: base.BuildScriptEmitter
                 ):

        # TODO: sanitize name string: only alphanum + _, no spaces
        self.name = name
        self.fs = wks_fs

        self.configure_dir_name = "configure"
        self.source_dir_name = "src"
        self.build_dir_name = "build"

        self.workspace_def: Union[WorkspaceDefinition, None] = None
        self.third_party_manifest: dict[str, Any] = {}
        self.toolchains_manifest: dict[str, Any] = {}

        self.build_types = [base.BUILD_TYPE_DEBUG, base.BUILD_TYPE_RELEASE, base.BUILD_TYPE_PROFILING]

        self.logger = logger
        self.system_config_provider = system_config_provider
        self.toolchain_settings_provider = toolchain_settings_provider
        self.build_script_emitter = build_script_emitter

    def __del__(self):
        self.fs.close()
        pass

    def _get_source_dir_path(self):
        return self.source_dir_name

    def _get_source_dir_abs_path(self):
        if self.fs.hassyspath(self.source_dir_name):
            return self.fs.getsyspath(self.source_dir_name)
        return f"wks://{self.source_dir_name}"

    def _get_configure_dir_abs_path(self):
        if self.fs.hassyspath(self.configure_dir_name):
            return self.fs.getsyspath(self.configure_dir_name)
        return f"wks://{self.configure_dir_name}"

    def _get_build_dir_abs_path(self):
        if self.fs.hassyspath(self.build_dir_name):
            return self.fs.getsyspath(self.build_dir_name)
        return f"wks://{self.build_dir_name}"

    def configure(self) -> bool:

        #
        # Load workspace target definitions
        #
        targets_file_path = fs.path.join(self.source_dir_name, "rapid_targets.yml")
        self.logger.log_info(f"Reading target definitions '{targets_file_path}'...")

        try:
            with self.fs.open(targets_file_path, 'r') as f:
                if not yaml.__with_libyaml__:
                    self.logger.log_info("Warning: using yaml module without C bindings.")
                targets_defs = yaml.load(f, yaml.SafeLoader)
        except fs.errors.ResourceNotFound:
            self.logger.log_error(f"File '{targets_file_path}' does not exist.")
            return False

        try:
            self.workspace_def = WorkspaceDefinition.from_dict(targets_defs)
        except WorkspaceInvalidFormat:
            self.logger.log_error(f"File '{targets_file_path}' is not a valid targets definition file.")
            return False

        self.logger.log_info("Workspace definition loaded.")

        # print(json.dumps(target_defs, indent=2))

        #
        # Prepare configuration directory, provide manifests
        #
        self.fs.makedir(self.configure_dir_name, recreate=True)

        self.system_config_provider.run(self._get_configure_dir_abs_path(), self.build_types)

        self.third_party_manifest = self.system_config_provider.get_third_party_manifest()

        if not _validate_third_party_manifest(self.third_party_manifest):
            self.logger.log_error("Provided third party manifest is invalid.")
            return False

        self.toolchains_manifest = self.system_config_provider.get_toolchains_manifest()

        if not _validate_toolchains_manifest(self.toolchains_manifest):
            self.logger.log_error("Provided toolchains manifest is invalid.")
            return False

        toolchains_settings = self.toolchain_settings_provider.get_toolchain_settings()

        if not _validate_toolchains_settings(toolchains_settings):
            self.logger.log_error("Provided toolchains settings format is invalid.")
            return False

        manifest_toolchains = set(self.toolchains_manifest.keys())
        settings_toolchains = set(toolchains_settings.keys())
        if not manifest_toolchains.issubset(settings_toolchains):
            self.logger.log_error("Missing settings for toolchains.")
            manifest_toolchains = list(manifest_toolchains)
            manifest_toolchains.sort()
            settings_toolchains = list(settings_toolchains)
            settings_toolchains.sort()
            self.logger.log_error(f"Toolchains in manifest: {manifest_toolchains}")
            self.logger.log_error(f"Toolchains for which settings were provided : {settings_toolchains}")
            return False

        #
        # Build targets implementations
        #
        targets_interfaces, targets_impls = _create_targets_interfaces_and_implementations(
            self._get_source_dir_abs_path(),
            self.toolchains_manifest.keys(),
            self.build_types,
            self.third_party_manifest,
            self.workspace_def
        )

        assert (isinstance(targets_interfaces, dict))
        assert (isinstance(targets_impls, dict) and len(targets_impls.keys()) != 0)

        #
        # Generate build script for targets based on implementations
        #

        build_script_filename = self.build_script_emitter.filename()
        build_script_contents = self.build_script_emitter.contents(
            self.name,
            self._get_source_dir_abs_path(),
            self._get_configure_dir_abs_path(),
            self._get_build_dir_abs_path(),
            self.toolchains_manifest,
            toolchains_settings,
            self.build_types,
            [d.name for d in self.workspace_def.targets],
            targets_impls
        )

        build_script_path = fs.path.join(self.configure_dir_name, build_script_filename)

        self.logger.log_info(f"Writing build script '{build_script_path}'...")
        with self.fs.open(build_script_path, 'w') as f:
            f.write(build_script_contents)

        self.logger.log_info("Configuring done.")
        return True


def open_workspace(wks_dir: str, *, dev_mode=False) -> Workspace:
    wks_fs = OSFS(os.path.abspath(wks_dir))

    logger = base.LoggerDefault()

    system_config_provider = SystemConfigManifestProviderConan(
        logger=logger,
        process_runner=base.ProcessRunnerDefault(),
        conanfile_path=wks_fs.getsyspath("conanfile.py"),
        execute_conan=not dev_mode,
        base_to_conan_build_type={
            base.BUILD_TYPE_DEBUG: "Debug",
            base.BUILD_TYPE_RELEASE: "Release",
            base.BUILD_TYPE_PROFILING: "Release",
        }
    )

    wks = Workspace(
        name=wks_dir,
        wks_fs=wks_fs,
        logger=logger,
        system_config_provider=system_config_provider,
        toolchain_settings_provider=ToolchainSettingsProviderDefault(),
        build_script_emitter=BuildScriptEmitterFastbuild()
    )
    return wks
