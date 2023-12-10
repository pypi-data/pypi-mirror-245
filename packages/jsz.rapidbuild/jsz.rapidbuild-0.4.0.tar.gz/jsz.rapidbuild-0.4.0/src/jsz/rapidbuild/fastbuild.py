import abc
from contextlib import contextmanager
from enum import Enum, auto
from pathlib import Path
from typing import Any
import fs

from .target_graph import (
    TargetImplementation,
)
from .workspace_def import (
    TargetKind,
)
from . import base


class BFFEmitter:
    GENERATED_FILE_HEADER = [
        "/////////////////////////////////////////////////////////////",
        "// This is a generated file, all manual changes will be lost!",
        "/////////////////////////////////////////////////////////////",
    ]
    INDENT_SIZE = 4

    def __init__(self):
        self._lines = []
        self._indent_level = 0

        for line in self.GENERATED_FILE_HEADER:
            self._emit_line(line)

    def _indent(self):
        self._indent_level += 1

    def _dedent(self):
        assert self._indent_level > 0
        self._indent_level -= 1

    def _emit_line(self, content: str):
        if len(content) != 0:
            self._lines.append("{}{}".format(' ' * self._indent_level * self.INDENT_SIZE, content))
        else:
            self._lines.append("")

    def _emit_array(self, name: str, values: list, *, should_split_str=False):
        self._emit_line(".{} = ".format(name))
        self._emit_line("{")
        self._indent()
        for v in values:
            self._emit_line("{},".format(self._format_value(v, should_split_str=should_split_str)))
        self._dedent()
        self._emit_line("}")

    def _emit_struct(self, name: str, dictionary: dict, *, should_split_str=False):
        self._emit_line(".{} = ".format(name))
        self._emit_line("[")
        self._indent()
        for key, value in dictionary.items():
            self.emit_var_assignment(key, value, should_split_str=should_split_str)
        self._dedent()
        self._emit_line("]")

    def _begin_function(self, fn_name: str, args: str):
        self._emit_line("{}('{}')".format(fn_name, args))
        self._emit_line("{")
        self._indent()

    def _end_function(self):
        self._dedent()
        self._emit_line("}")
        self._emit_line("")

    def once(self):
        self._emit_line("#once")

    def include(self, path: str):
        self._emit_line("#include \"{}\"".format(path))

    def line_break(self):
        self._emit_line("")

    def emit_var_assignment(self, name: str, value, *, should_split_str=False):
        if type(value) == list:
            self._emit_array(name, value)
        elif type(value) == dict:
            self._emit_struct(name, value)
        else:
            self._emit_line(".{} = {}".format(name, self._format_value(value, should_split_str=should_split_str)))

    @contextmanager
    def library(self, name: str):
        self._begin_function("Library", name)
        yield
        self._end_function()

    @contextmanager
    def object_list(self, name: str):
        self._begin_function("ObjectList", name)
        yield
        self._end_function()

    @contextmanager
    def dll(self, name: str):
        self._begin_function("DLL", name)
        yield
        self._end_function()

    @contextmanager
    def exe(self, name: str):
        self._begin_function("Executable", name)
        yield
        self._end_function()

    @contextmanager
    def alias(self, name: str):
        self._begin_function("Alias", name)
        yield
        self._end_function()

    @contextmanager
    def copy_dir(self, name: str):
        self._begin_function("CopyDir", name)
        yield
        self._end_function()

    @contextmanager
    def remove_dir(self, name: str):
        self._begin_function("RemoveDir", name)
        yield
        self._end_function()

    @contextmanager
    def compiler(self, name: str):
        self._begin_function("Compiler", name)
        yield
        self._end_function()

    @contextmanager
    def vcxproject(self, name: str):
        self._begin_function("VCXProject", name)
        yield
        self._end_function()

    @contextmanager
    def vssolution(self, name: str):
        self._begin_function("VSSolution", name)
        yield
        self._end_function()

    def build(self):
        return "\n".join(self._lines)

    def _format_value(self, value, *, should_split_str):

        def format_default(v):
            return "{}".format(v)

        def str_smart_split(s: str):
            splits = []
            inside_quoted = False
            delim = " "
            curr = ""
            for c in s:
                if not inside_quoted:
                    if c == "\"":
                        inside_quoted = True
                        curr += c
                    elif c == delim:
                        splits.append(curr)
                        curr = delim
                    else:
                        curr += c
                else:
                    if c == "\"":
                        inside_quoted = False
                        curr += c
                    else:
                        curr += c
            if len(curr) != 0:
                splits.append(curr)
            return splits

        def format_string(s: str):
            if len(s) == 0:
                return "''"

            if not should_split_str:
                return f"'{s}'"

            lines = []
            col_limit = 80

            if len(s) > col_limit:
                lines = str_smart_split(s)
            else:
                lines.append(s)

            result = ""
            result += "'{}'".format(lines[0])
            if len(lines) > 1:
                for line in lines[1:]:
                    result += f"\n{' ' * (self._indent_level + 1) * self.INDENT_SIZE}+ '{line}'"
            return result

        def format_bool(b: bool):
            return "true" if b else "false"

        formatters = {
            str: format_string,
            bool: format_bool,
        }

        f = formatters.get(type(value), format_default)
        return f(value)


def get_target_kind_extension(target_kind):
    if target_kind == TargetKind.STATIC_LIB:
        return "lib"
    elif target_kind == TargetKind.DYNAMIC_LIB:
        return "dll"
    elif target_kind == TargetKind.EXECUTABLE:
        return "exe"
    else:
        raise NotImplementedError("Target kind of this type is not implemented.")


def format_target_filename(target_name, target_kind):
    ext = get_target_kind_extension(target_kind)
    if len(ext) > 0:
        return f"{target_name}.{ext}"
    else:
        return target_name


def format_target_glob_pattern(target_kind):
    return format_target_filename("*", target_kind)


def format_compiler_node_name(toolchain_name: str) -> str:
    return f"compiler-{toolchain_name}"


def format_target_node_name(target_name: str, toolchain_name: str, build_type_name: str) -> str:
    return f"{target_name}-{toolchain_name}-{build_type_name}"


def format_obj_node_name(target_node_name: str):
    return f"obj-{target_node_name}"


def format_make_node_name(target_node_name: str):
    return f"make-{target_node_name}"


def format_deploy_node_name(target_node_name: str):
    return f"deploy-{target_node_name}"


# noinspection PyArgumentList
class CompilerFamily(Enum):
    MSVC = auto()
    CLANG = auto()
    CLANG_CL = auto()
    GCC = auto()


class CouldNotDetermineCompilerFamily(RuntimeError):
    pass


def compiler_family_to_fastbuild_value(f: CompilerFamily):
    return {
        CompilerFamily.MSVC: "msvc",
        CompilerFamily.CLANG: "clang",
        CompilerFamily.CLANG_CL: "clang-cl",
        CompilerFamily.GCC: "gcc"
    }[f]


def guess_compiler_family_from_compiler_path(path: str) -> CompilerFamily:
    filename = Path(path).parts[-1]
    if filename == "cl" or filename == "cl.exe":
        return CompilerFamily.MSVC
    if filename == "clang" or filename == "clang.exe" or filename == "clang++" or filename == "clang++.exe":
        return CompilerFamily.CLANG
    if filename == "clang-cl" or filename == "clang-cl.exe":
        return CompilerFamily.CLANG_CL
    if filename == "gcc":
        return CompilerFamily.GCC
    raise CouldNotDetermineCompilerFamily(f"compiler path: {path}")


class CompilerArgFormatter(abc.ABC):
    @abc.abstractmethod
    def format_beginning_args(self) -> list[str]:
        pass

    @abc.abstractmethod
    def format_object_compilation_args(self) -> list[str]:
        pass

    @abc.abstractmethod
    def format_debug_info_args(self, output_dir_path: str, output_base_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def format_pch_creation_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        pass

    @abc.abstractmethod
    def format_pch_usage_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        pass

    @abc.abstractmethod
    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        pass

    @abc.abstractmethod
    def format_include_dir_arg(self, include_dir: str) -> str:
        pass

    @abc.abstractmethod
    def format_system_include_dir_arg(self, include_dir: str) -> str:
        pass


class CompilerArgFormatterMSVC(CompilerArgFormatter):
    def format_beginning_args(self) -> list[str]:
        return ["/nologo"]

    def format_object_compilation_args(self) -> list[str]:
        return [
            "/c",
            "\"%1\"",
            "/Fo\"%2\"",
        ]

    def format_debug_info_args(self, output_dir_path: str, output_base_name: str) -> list[str]:
        intermediate_pdb_path = fs.path.join(output_dir_path, f"{output_base_name}-lib.pdb")
        return [
            f"/Fd\"{intermediate_pdb_path}\"",
        ]

    def format_pch_creation_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            "/c",
            "\"%1\"",  # PCH input file (.cpp)
            "/Fo\"%3\"",  # PCH output library (.lib)
            f"/Yc\"{fs.path.basename(pch_header_path)}\"",
            "/Fp\"%2\""  # PCH output file (compiled .pch)
        ]

    def format_pch_usage_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            f"/Yu\"{fs.path.basename(pch_header_path)}\"",
            f"/Fp\"{pch_output_path}\"",
        ]

    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        if value is not None:
            return f"/D\"{name}={value}\""
        else:
            return f"/D\"{name}\""

    def format_include_dir_arg(self, include_dir: str) -> str:
        return f"/I\"{include_dir}\""

    def format_system_include_dir_arg(self, include_dir: str) -> str:
        return f"/I\"{include_dir}\""


class CompilerArgFormatterClang(CompilerArgFormatter):
    def format_beginning_args(self) -> list[str]:
        return []

    def format_object_compilation_args(self) -> list[str]:
        return ["-c", "%1", "-o", "%2"]

    def format_debug_info_args(self, output_dir_path: str, output_base_name: str) -> list[str]:
        return []

    def format_pch_creation_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            "-x", "c++-header", f"\"{pch_header_path}\"",
            "-o", "\"%2\""  # PCH output file (compiled .pch)
        ]

    def format_pch_usage_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            "-include-pch", f"\"{pch_output_path}\""
        ]

    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        if value is not None:
            return f"-D\"{name}={value}\""
        else:
            return f"-D\"{name}\""

    def format_include_dir_arg(self, include_dir: str) -> str:
        return f"-I\"{include_dir}\""

    def format_system_include_dir_arg(self, include_dir: str) -> str:
        return f"-isystem\"{include_dir}\""


class CompilerArgFormatterGCC(CompilerArgFormatterClang):
    pass


class CompilerArgFormatterClangCL(CompilerArgFormatterMSVC):
    pass


def create_compiler_arg_formatter(f: CompilerFamily) -> CompilerArgFormatter:
    return {
        CompilerFamily.MSVC: CompilerArgFormatterMSVC(),
        CompilerFamily.CLANG: CompilerArgFormatterClang(),
        CompilerFamily.CLANG_CL: CompilerArgFormatterClangCL(),
        CompilerFamily.GCC: CompilerArgFormatterGCC()
    }[f]


def build_include_dir_compiler_options(
        arg_formatter: CompilerArgFormatter,
        system_include_dirs: list[str],
        target_include_dirs: list[str],
):
    args = []
    args += [arg_formatter.format_system_include_dir_arg(include_dir) for include_dir in system_include_dirs]
    args += [arg_formatter.format_include_dir_arg(include_dir) for include_dir in target_include_dirs]
    return args


def build_definitions_compiler_options(
        arg_formatter: CompilerArgFormatter,
        system_definitions: dict[str, Any],
        target_definitions: dict[str, Any],
):
    args = []
    args += [arg_formatter.format_definition_compiler_arg(name, value) for name, value in system_definitions.items()]
    args += [arg_formatter.format_definition_compiler_arg(name, value) for name, value in target_definitions.items()]
    return args


def build_common_compiler_options(
        arg_formatter: CompilerArgFormatter,
        base_args: list[str],
        system_include_dirs: list[str], system_definitions: dict[str, Any],
        target_include_dirs: list[str], target_definitions: dict[str, Any],
):
    args = []
    args += base_args
    args.extend(build_include_dir_compiler_options(arg_formatter, system_include_dirs, target_include_dirs))
    args.extend(build_definitions_compiler_options(arg_formatter, system_definitions, target_definitions))
    return args


def build_compiler_options(
        arg_formatter: CompilerArgFormatter,
        output_dir_path: str, output_base_name: str,
        pch_header_path: str | None, pch_output_path: str | None,
):
    args = []
    args += arg_formatter.format_beginning_args()
    args += arg_formatter.format_object_compilation_args()
    if pch_header_path is not None and pch_output_path is not None:
        args += arg_formatter.format_pch_usage_args(pch_header_path, pch_output_path)
    args += arg_formatter.format_debug_info_args(output_dir_path, output_base_name)
    return args


def build_pch_options(
        arg_formatter: CompilerArgFormatter,
        output_dir_path: str, output_base_name: str,
        pch_header_path: str, pch_output_path: str,
):
    args = []
    args += arg_formatter.format_beginning_args()
    args += arg_formatter.format_pch_creation_args(pch_header_path, pch_output_path)
    args += arg_formatter.format_debug_info_args(output_dir_path, output_base_name)
    return args


# noinspection PyArgumentList
class LibrarianFamily(Enum):
    MSVC = auto()
    LLVM = auto()
    GCC = auto()


class CouldNotDetermineLibrarianFamily(RuntimeError):
    pass


def guess_librarian_family_from_path(path: str) -> LibrarianFamily:
    filename = Path(path).parts[-1]
    if filename == "lib" or filename == "lib.exe":
        return LibrarianFamily.MSVC
    if filename == "llvm-ar" or filename == "llvm-ar.exe":
        return LibrarianFamily.LLVM
    if filename == "ar" or filename == "ar.exe":
        return LibrarianFamily.GCC
    raise CouldNotDetermineLibrarianFamily(f"librarian path: {path}")


class LibrarianArgFormatter(abc.ABC):
    @abc.abstractmethod
    def format_input_output_args(self) -> list[str]:
        pass


class LibrarianArgFormatterMSVC(LibrarianArgFormatter):
    def format_input_output_args(self) -> list[str]:
        return ["/NOLOGO", "/MACHINE:X64", "/WX", "\"%1\"", "/OUT:\"%2\""]


class LibrarianArgFormatterLLVM(LibrarianArgFormatter):
    def format_input_output_args(self) -> list[str]:
        return ["rc", "%2", "%1"]


class LibrarianArgFormatterGCC(LibrarianArgFormatterLLVM):
    pass


def create_librarian_arg_formatter(f: LibrarianFamily):
    return {
        LibrarianFamily.MSVC: LibrarianArgFormatterMSVC(),
        LibrarianFamily.LLVM: LibrarianArgFormatterLLVM(),
        LibrarianFamily.GCC: LibrarianArgFormatterGCC(),
    }[f]


def build_librarian_options(arg_formatter: LibrarianArgFormatter):
    return arg_formatter.format_input_output_args()


# noinspection PyArgumentList
class LinkerFamily(Enum):
    LINK = auto()
    LLD_LINK = auto()
    LD_LLD = auto()
    LD = auto()


class CouldNotDetermineLinkerFamily(RuntimeError):
    pass


def guess_linker_family_from_path(path: str) -> LinkerFamily:
    filename = Path(path).parts[-1]
    if filename == "link" or filename == "link.exe":
        return LinkerFamily.LINK
    if filename == "lld-link" or filename == "lld-link.exe":
        return LinkerFamily.LLD_LINK
    if filename == "ld.lld" or filename == "ld.lld.exe":
        return LinkerFamily.LD_LLD
    if filename == "ld" or filename == "ld.exe":
        return LinkerFamily.LD
    raise CouldNotDetermineLinkerFamily(f"linker path: {path}")


class LinkerArgFormatter(abc.ABC):
    @abc.abstractmethod
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: TargetKind
    ) -> list[str]:
        pass

    @abc.abstractmethod
    def format_lib_arg(self, lib: str) -> str:
        pass

    @abc.abstractmethod
    def format_lib_dir_arg(self, lib_dir: str) -> str:
        pass


class LinkerArgFormatterLink(LinkerArgFormatter):
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: TargetKind
    ) -> list[str]:
        output_pdb_path = fs.path.join(output_dir_path, f"{output_base_name}-lib.pdb")
        args = ["/nologo", "\"%1\"", "/out:\"%2\"", f"/pdb:\"{output_pdb_path}\""]
        if target_kind == TargetKind.DYNAMIC_LIB:
            args += ["/dll"]
        return args

    def format_lib_arg(self, lib: str) -> str:
        return lib

    def format_lib_dir_arg(self, lib_dir: str) -> str:
        return f"/libpath:\"{lib_dir}\""


class LinkerArgFormatterLLDLink(LinkerArgFormatterLink):
    pass


class LinkerArgFormatterLDLLD(LinkerArgFormatter):
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: TargetKind
    ) -> list[str]:
        args = ["\"%1\"", "-o \"%2\""]
        if target_kind == TargetKind.DYNAMIC_LIB:
            args += ["--shared"]
        return args

    def format_lib_arg(self, lib: str) -> str:
        return f"-l\"{lib}\""

    def format_lib_dir_arg(self, lib_dir: str) -> str:
        return f"-L\"{lib_dir}\""


class LinkerArgFormatterLD(LinkerArgFormatterLDLLD):
    pass


def create_linker_arg_formatter(f: LinkerFamily):
    return {
        LinkerFamily.LINK: LinkerArgFormatterLink(),
        LinkerFamily.LLD_LINK: LinkerArgFormatterLLDLink(),
        LinkerFamily.LD_LLD: LinkerArgFormatterLDLLD(),
        LinkerFamily.LD: LinkerArgFormatterLD()
    }[f]


def build_linker_options(
        arg_formatter: LinkerArgFormatter,
        output_dir_path: str, output_base_name: str, output_target_kind: TargetKind,
        base_args: list[str],
        base_link_libs: list[str], base_lib_dirs: list[str],
        external_link_libs: list[str], external_lib_dirs: list[str]
):
    if output_target_kind != TargetKind.DYNAMIC_LIB and output_target_kind != TargetKind.EXECUTABLE:
        raise RuntimeError()

    args = arg_formatter.format_input_output_declaration(output_dir_path, output_base_name, output_target_kind)
    args += base_args

    args += [arg_formatter.format_lib_arg(lib) for lib in base_link_libs]
    args += [arg_formatter.format_lib_dir_arg(lib_dir) for lib_dir in base_lib_dirs]

    # External libs are added to commandl ine manully, not through "Libraries" variable.
    # If the extension is skipped, fastbuild tries to use "obj"
    args += [arg_formatter.format_lib_arg(f"{lib}.{get_target_kind_extension(TargetKind.STATIC_LIB)}")
             for lib in external_link_libs]
    args += [arg_formatter.format_lib_dir_arg(lib_dir) for lib_dir in external_lib_dirs]

    return args


class BuildScriptEmitterFastbuild(base.BuildScriptEmitter):
    ALL_TARGETS_TARGET_NAME = "rapid_all"
    SLN_TARGET_NAME = "rapid_sln"
    CLEAN_TARGET_NAME = "rapid_clean"
    TARGET_WORKING_DIR_NAME = "data"

    HEADER_EXTENSIONS = ["h", "hh", "hxx", "hpp"]
    SOURCE_EXTENSIONS = ["c", "cc", "cxx", "cpp"]

    def filename(self):
        return "fbuild.bff"

    def contents(self, wks_name, source_dir_abs_path, configure_dir_abs_path, build_dir_abs_path,
                 toolchains_manifest, toolchains_settings, build_types, targets_names, targets_impls) -> str:

        assert (set(toolchains_manifest.keys()).issubset(set(toolchains_settings.keys())))

        intermediate_dir_abs_path = fs.path.join(build_dir_abs_path, "intermediate")
        deploy_dir_abs_path = fs.path.join(build_dir_abs_path, "bin")

        out_bff = BFFEmitter()
        out_bff.once()

        self._emit_compilers(out_bff, toolchains_manifest)
        self._emit_compilation_targets(out_bff, intermediate_dir_abs_path, deploy_dir_abs_path, toolchains_manifest,
                                       toolchains_settings, build_types, targets_names, targets_impls)
        self._emit_vs_solution_targets(out_bff, wks_name, source_dir_abs_path, configure_dir_abs_path, deploy_dir_abs_path,
                                       toolchains_manifest, toolchains_settings, build_types, targets_names, targets_impls)

        with out_bff.remove_dir(self.CLEAN_TARGET_NAME):
            out_bff.emit_var_assignment("RemovePaths", build_dir_abs_path)
            out_bff.emit_var_assignment("RemovePathsRecurse", True)
            
        return out_bff.build()

    @staticmethod
    def _emit_compilers(out_bff, toolchains_manifest):
        
        for toolchain_name, toolchain_def in toolchains_manifest.items():
            with out_bff.compiler(format_compiler_node_name(toolchain_name)):
                compiler_path = toolchain_def["compiler_path"]
                compiler_family = guess_compiler_family_from_compiler_path(compiler_path)

                out_bff.emit_var_assignment("Executable", compiler_path)
                out_bff.emit_var_assignment("CompilerFamily", compiler_family_to_fastbuild_value(compiler_family))
                out_bff.emit_var_assignment("ExtraFiles", toolchain_def["compiler_extra_files"])

    def _search_pch_files_in_dir(self, path: str):
        with fs.open_fs(path) as input_fs:
            pch_header_patterns = [f"*_pch.{ext}" for ext in self.HEADER_EXTENSIONS]
            pch_source_patterns = [f"*_pch.{ext}" for ext in self.SOURCE_EXTENSIONS]

            pch_headers = list(input_fs.filterdir(".", files=pch_header_patterns))
            pch_sources = list(input_fs.filterdir(".", files=pch_source_patterns))

            # For some reason dirs are also found using filterdir()
            pch_headers = [f for f in pch_headers if f.is_file]
            pch_sources = [f for f in pch_sources if f.is_file]

            if len(pch_headers) == 0 and len(pch_sources) == 0:
                return None, None
            elif len(pch_headers) == 1 and len(pch_sources) == 1:
                return pch_headers[0].make_path(path), pch_sources[0].make_path(path)
            else:
                msg = f"Source dir \"{path}\" should contain a single PCH header and a single PCH source.\n"
                
                msg += "When searching for PCH header using patterns: "
                msg += " ".join(pch_header_patterns)
                msg += "\n"
                if len(pch_headers) == 0:
                    msg += f"found 0 files.\n"
                else:
                    msg += f"found {len(pch_headers)} files:\n"
                    for f in pch_headers:
                        msg += f"* {f.name}\n"

                msg += "When searching for PCH source using patterns: "
                msg += " ".join(pch_source_patterns)
                msg += "\n"
                if len(pch_sources) == 0:
                    msg += f"found 0 files.\n"
                else:
                    msg += f"found {len(pch_sources)} files:\n"
                    for f in pch_sources:
                        msg += f"* {f.name}\n"
                    
                raise RuntimeError(msg)

    def _emit_compilation_targets(
            self,
            out_bff: BFFEmitter,
            intermediate_dir_abs_path: str,
            deploy_dir_abs_path: str,
            toolchains_manifest: dict[str, Any],
            toolchains_settings: dict[str, Any],
            build_types: list[str],
            targets_names: list[str],
            targets_impls: dict[str, TargetImplementation]
    ):

        all_nodes: list[str] = []
        per_toolchain_nodes: dict[str, list[str]] = {
            toolchain_name: [] for toolchain_name in toolchains_manifest.keys()
        }
        per_build_type_nodes: dict[str, list[str]] = {
            build_type: [] for build_type in build_types
        }
        config_vector_nodes: dict[str, dict[str, list[str]]] = {
            toolchain_name: {
                build_type: [] for build_type in build_types
            } for toolchain_name in toolchains_manifest.keys()
        }
        external_deploy_nodes = set()

        for toolchain_name, toolchain_def in toolchains_manifest.items():

            toolchain_compiler_family = guess_compiler_family_from_compiler_path(toolchain_def["compiler_path"])
            toolchain_librarian_family = guess_librarian_family_from_path(toolchain_def["librarian_path"])
            toolchain_linker_family = guess_linker_family_from_path(toolchain_def["linker_path"])

            compiler_arg_formatter = create_compiler_arg_formatter(toolchain_compiler_family)
            librarian_arg_formatter = create_librarian_arg_formatter(toolchain_librarian_family)
            linker_arg_formatter = create_linker_arg_formatter(toolchain_linker_family)

            toolchain_include_dirs = toolchain_def["toolchain_include_dirs"]
            toolchain_lib_dirs = toolchain_def["toolchain_lib_dirs"]

            current_toolchain_settings = toolchains_settings[toolchain_name]
            toolchain_definitions = current_toolchain_settings["definitions"]
            toolchain_compiler_args = current_toolchain_settings["compiler_args"]
            toolchain_linker_args = current_toolchain_settings["linker_args"]
            toolchain_link_libs = current_toolchain_settings["link_libs"]

            for build_type in build_types:

                toolchain_build_type_definitions = toolchain_definitions["all"] | toolchain_definitions[build_type]
                toolchain_build_type_compiler_args = toolchain_compiler_args["all"] + toolchain_compiler_args[
                    build_type]
                toolchain_build_type_linker_args = toolchain_linker_args["all"] + toolchain_linker_args[build_type]
                toolchain_build_type_link_libs = toolchain_link_libs["all"] + toolchain_link_libs[build_type]

                build_type_deploy_dir_path = fs.path.join(deploy_dir_abs_path, build_type)

                for target_name in targets_names:

                    target_impl = targets_impls[base.build_target_key(target_name, toolchain_name, build_type)]
                    target_node_name = format_target_node_name(target_name, toolchain_name, build_type)
                    make_node_name = format_make_node_name(target_node_name)
                    deploy_node_name = format_deploy_node_name(target_node_name)

                    target_kind = target_impl.kind

                    common_compiler_options = build_common_compiler_options(
                        compiler_arg_formatter,
                        toolchain_build_type_compiler_args,
                        toolchain_include_dirs, toolchain_build_type_definitions,
                        target_impl.include_dirs, target_impl.definitions
                    )

                    target_output_dir_path = fs.path.join(intermediate_dir_abs_path, target_node_name)

                    compiler_input_path = target_impl.source_dir
                    compiler_input_pattern = [f"*.{ext}" for ext in self.SOURCE_EXTENSIONS]

                    pch_header_path, pch_source_path = self._search_pch_files_in_dir(compiler_input_path)

                    pch_input_path = pch_source_path
                    pch_output_path = fs.path.join(target_output_dir_path, f"{target_node_name}.pch")
                    pch_options = None

                    if pch_header_path is not None and pch_source_path is not None:
                        pch_options = build_pch_options(
                            compiler_arg_formatter,
                            target_output_dir_path, target_node_name,
                            pch_header_path, pch_output_path
                        )
                        pch_options += common_compiler_options

                    compiler_options = build_compiler_options(
                        compiler_arg_formatter,
                        target_output_dir_path, target_node_name,
                        pch_header_path, pch_output_path
                    )
                    compiler_options += common_compiler_options

                    if target_kind == TargetKind.STATIC_LIB:

                        librarian_output_path = fs.path.join(target_output_dir_path,
                                                             format_target_filename(target_node_name, target_kind))

                        with out_bff.library(make_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", target_output_dir_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)
                            out_bff.line_break()

                            if pch_options is not None:
                                out_bff.emit_var_assignment("PCHInputFile", pch_input_path)
                                out_bff.emit_var_assignment("PCHOutputFile", pch_output_path)
                                out_bff.emit_var_assignment("PCHOptions", " ".join(pch_options), should_split_str=True)
                                out_bff.line_break()

                            out_bff.emit_var_assignment("Librarian", toolchain_def["librarian_path"])
                            out_bff.emit_var_assignment("LibrarianOutput", librarian_output_path)
                            out_bff.emit_var_assignment("LibrarianOptions",
                                                        " ".join(build_librarian_options(librarian_arg_formatter)),
                                                        should_split_str=True)

                        # Deploy step does nothing for static libs.
                        with out_bff.alias(deploy_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Targets", make_node_name)

                        with out_bff.alias(target_node_name):
                            out_bff.emit_var_assignment("Targets", deploy_node_name)

                    elif target_kind == TargetKind.DYNAMIC_LIB or target_kind == TargetKind.EXECUTABLE:

                        object_list_node_name = format_obj_node_name(target_node_name)
                        with out_bff.object_list(object_list_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("Compiler", format_compiler_node_name(toolchain_name))
                            out_bff.emit_var_assignment("CompilerInputPath", compiler_input_path)
                            out_bff.emit_var_assignment("CompilerInputPathRecurse", True)
                            out_bff.emit_var_assignment("CompilerInputPattern", compiler_input_pattern)
                            out_bff.emit_var_assignment("CompilerOutputPath", target_output_dir_path)
                            out_bff.emit_var_assignment("CompilerOptions", " ".join(compiler_options),
                                                        should_split_str=True)
                            out_bff.line_break()

                            if pch_options is not None:
                                out_bff.emit_var_assignment("PCHInputFile", pch_input_path)
                                out_bff.emit_var_assignment("PCHOutputFile", pch_output_path)
                                out_bff.emit_var_assignment("PCHOptions", " ".join(pch_options), should_split_str=True)
                                out_bff.line_break()

                        #
                        linker_output_path = fs.path.join(target_output_dir_path,
                                                          format_target_filename(target_node_name, target_kind))

                        libraries = [object_list_node_name]
                        libraries += [format_make_node_name(format_target_node_name(lib, toolchain_name, build_type))
                                      for lib in target_impl.link_libs]

                        linker_options = build_linker_options(
                            linker_arg_formatter, target_output_dir_path, target_node_name, target_kind,
                            toolchain_build_type_linker_args,
                            toolchain_build_type_link_libs, toolchain_lib_dirs,
                            target_impl.link_libs_external, target_impl.link_libs_external_dirs
                        )

                        if target_kind == TargetKind.DYNAMIC_LIB:
                            with out_bff.dll(make_node_name):
                                # out_bff.emit_var_assignment("Hidden", True)  # DLL does not support .Hidden
                                out_bff.emit_var_assignment("Libraries", libraries)
                                out_bff.emit_var_assignment("Linker", toolchain_def["linker_path"])
                                out_bff.emit_var_assignment("LinkerOutput", linker_output_path)
                                out_bff.emit_var_assignment("LinkerOptions", " ".join(linker_options),
                                                            should_split_str=True)

                        elif target_kind == TargetKind.EXECUTABLE:
                            with out_bff.exe(make_node_name):
                                # out_bff.emit_var_assignment("Hidden", True)  # Executable does not support .Hidden
                                out_bff.emit_var_assignment("Libraries", libraries)
                                out_bff.emit_var_assignment("Linker", toolchain_def["linker_path"])
                                out_bff.emit_var_assignment("LinkerOutput", linker_output_path)
                                out_bff.emit_var_assignment("LinkerOptions", " ".join(linker_options),
                                                            should_split_str=True)

                        deploy_deps = [make_node_name]
                        deploy_deps += [
                            format_deploy_node_name(format_target_node_name(lib, toolchain_name, build_type))
                            for lib in target_impl.load_time_libs]

                        for path in target_impl.load_time_libs_external:
                            deploy_external = format_deploy_node_name(path)
                            if path not in external_deploy_nodes:
                                external_deploy_nodes.add(path)

                                with out_bff.copy_dir(deploy_external):
                                    out_bff.emit_var_assignment("Hidden", True)
                                    out_bff.emit_var_assignment("PreBuildDependencies", [])
                                    out_bff.emit_var_assignment("SourcePaths", fs.path.dirname(path))
                                    out_bff.emit_var_assignment("SourcePathsPattern", [(fs.path.basename(path))])
                                    out_bff.emit_var_assignment("Dest", build_type_deploy_dir_path)
                            deploy_deps.append(deploy_external)

                        with out_bff.copy_dir(deploy_node_name):
                            out_bff.emit_var_assignment("Hidden", True)
                            out_bff.emit_var_assignment("PreBuildDependencies", deploy_deps)
                            out_bff.emit_var_assignment("SourcePaths", target_output_dir_path)
                            out_bff.emit_var_assignment("SourcePathsPattern",
                                                        [format_target_glob_pattern(target_kind), "*.pdb"])
                            out_bff.emit_var_assignment("Dest", build_type_deploy_dir_path)

                        with out_bff.alias(target_node_name):
                            out_bff.emit_var_assignment("Targets", deploy_node_name)

                    else:
                        raise NotImplementedError("unsupported target kind")

                    all_nodes.append(target_node_name)
                    per_build_type_nodes[build_type].append(target_node_name)
                    per_toolchain_nodes[toolchain_name].append(target_node_name)
                    config_vector_nodes[toolchain_name][build_type].append(target_node_name)

        for build_type, nodes in per_build_type_nodes.items():
            with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}-{build_type}"):
                out_bff.emit_var_assignment("Targets", nodes)

        for toolchain_name, nodes in per_toolchain_nodes.items():
            with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}-{toolchain_name}"):
                out_bff.emit_var_assignment("Targets", nodes)

        for toolchain_name, per_toolchain_per_build_type_visible_nodes in config_vector_nodes.items():
            for build_type, nodes in per_toolchain_per_build_type_visible_nodes.items():
                with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}-{toolchain_name}-{build_type}"):
                    out_bff.emit_var_assignment("Targets", nodes)

        with out_bff.alias(f"{self.ALL_TARGETS_TARGET_NAME}"):
            out_bff.emit_var_assignment("Targets", all_nodes)

    # noinspection PyUnreachableCode
    def _emit_vs_solution_targets(
            self,
            out_bff: BFFEmitter,
            wks_name: str,
            source_dir_abs_path: str,
            configure_dir_abs_path: str,
            deploy_dir_abs_path: str,
            toolchains_manifest: dict[str, Any],
            toolchains_settings: dict[str, Any],
            build_types: list[str],
            targets_names: list[str],
            targets_impls: dict[str, TargetImplementation]
    ):

        bff_path = fs.path.join(f"{configure_dir_abs_path}", self.filename())
        vs_dir_abs_path = fs.path.join(configure_dir_abs_path, "vs")

        latest_msvc_toolset = None
        latest_vs_version = None
        if base.TOOLCHAIN_VS17_MSVC in toolchains_manifest.keys():
            latest_msvc_toolset = "v143"
            latest_vs_version = "17.0"
        elif base.TOOLCHAIN_VS16_MSVC in toolchains_manifest.keys():
            latest_msvc_toolset = "v142"
            latest_vs_version = "16.0"
        else:
            return

        lang_standard = "c++17"

        # Fastbuild can deduce these automatically based of "Target", manual spec overrides it.
        # Currently, our "Target" is pointing to an alias, which points to a deployment step,
        # and fastbuild is unable to deduce those.
        explicitly_define_intellisense_args = True

        project_nodes = []
        for target_name in targets_names:
            target_source_dir_abs_path = fs.path.join(source_dir_abs_path, target_name)
            project_out_abs_path = fs.path.join(vs_dir_abs_path, f"{target_name}.vcxproj")

            project_node_name = f"vcxproj-{target_name}"
            with out_bff.vcxproject(project_node_name):
                out_bff.emit_var_assignment("ProjectOutput", project_out_abs_path)
                out_bff.emit_var_assignment("ProjectInputPaths", target_source_dir_abs_path)
                out_bff.emit_var_assignment("ProjectBasePath", target_source_dir_abs_path)

                out_bff._emit_line(".ProjectConfigs = {}")

                for toolchain_name, toolchain_def in toolchains_manifest.items():

                    toolchain_include_dirs = toolchain_def["toolchain_include_dirs"]

                    current_toolchain_settings = toolchains_settings[toolchain_name]
                    toolchain_definitions = current_toolchain_settings["definitions"]

                    for build_type in build_types:

                        build_type_deploy_dir_path = fs.path.join(deploy_dir_abs_path, build_type)

                        toolchain_build_type_definitions = toolchain_definitions["all"] | toolchain_definitions[build_type]

                        target_impl = targets_impls[base.build_target_key(target_name, toolchain_name, build_type)]
                        target_node_name = format_target_node_name(target_name, toolchain_name, build_type)

                        out_bff._emit_line(".cfg = [")
                        out_bff._indent()

                        out_bff.emit_var_assignment("Platform", "x64")
                        out_bff.emit_var_assignment("PlatformToolset", latest_msvc_toolset)
                        out_bff.emit_var_assignment("Config", f"{toolchain_name}-{build_type}")
                        # out_bff.emit_var_assignment("Config", "Debug")
                        out_bff.line_break()
                        out_bff.emit_var_assignment("Target", target_node_name)
                        out_bff.emit_var_assignment("ProjectBuildCommand",
                                                    f"fbuild -ide -config \"{bff_path}\" {target_node_name}")
                        out_bff.emit_var_assignment("ProjectRebuildCommand",
                                                    f"fbuild -ide -config \"{bff_path}\" -clean {target_node_name}")
                        # ProjectCleanCommand
                        out_bff.emit_var_assignment("LocalDebuggerCommand",
                                                    fs.path.join(build_type_deploy_dir_path, f"{target_node_name}.exe"))
                        out_bff.emit_var_assignment("LocalDebuggerWorkingDirectory",
                                                    fs.path.join(source_dir_abs_path, target_name, self.TARGET_WORKING_DIR_NAME))

                        out_bff.line_break()

                        if explicitly_define_intellisense_args:
                            include_dirs_intellisense = ""

                            for include_dir in toolchain_include_dirs:
                                include_dirs_intellisense += f"{include_dir};"

                            for include_dir in target_impl.include_dirs:
                                include_dirs_intellisense += f"{include_dir};"

                            out_bff.emit_var_assignment("IncludeSearchPath", include_dirs_intellisense)

                            definitions_intellisense = ""

                            for name, value in toolchain_build_type_definitions.items():
                                if value is not None:
                                    definitions_intellisense += f"{name}={value};"
                                else:
                                    definitions_intellisense += f"{name};"

                            for name, value in target_impl.definitions.items():
                                if value is not None:
                                    definitions_intellisense += f"{name}={value};"
                                else:
                                    definitions_intellisense += f"{name};"

                            out_bff.emit_var_assignment("PreprocessorDefinitions", definitions_intellisense)

                            # TODO: generate AdditionalOptions from compiler options - standard and warning settings
                            out_bff.emit_var_assignment("AdditionalOptions", f"/std:{lang_standard}")

                        out_bff._dedent()
                        out_bff._emit_line("]")

                        out_bff._emit_line(".ProjectConfigs + .cfg")

            project_nodes.append(project_node_name)

        # special 'all' project
        all_targets_project_path = fs.path.join(vs_dir_abs_path, f"{self.ALL_TARGETS_TARGET_NAME}.vcxproj")

        project_node_name = f"vcxproj-{self.ALL_TARGETS_TARGET_NAME}"
        with out_bff.vcxproject(project_node_name):
            out_bff.emit_var_assignment("ProjectOutput", all_targets_project_path)

            out_bff._emit_line(".ProjectConfigs = {}")

            for toolchain_name in toolchains_manifest.keys():
                for build_type in build_types:
                    target_node_name = format_target_node_name(self.ALL_TARGETS_TARGET_NAME, toolchain_name,
                                                               build_type)

                    out_bff._emit_line(".cfg = [")
                    out_bff._indent()

                    out_bff.emit_var_assignment("Platform", "x64")
                    out_bff.emit_var_assignment("PlatformToolset", latest_msvc_toolset)
                    out_bff.emit_var_assignment("Config", f"{toolchain_name}-{build_type}")
                    # out_bff.emit_var_assignment("Config", "Debug")
                    out_bff.line_break()
                    out_bff.emit_var_assignment("Target", target_node_name)
                    out_bff.emit_var_assignment("ProjectBuildCommand",
                                                f"fbuild -ide -config \"{bff_path}\" {target_node_name}")
                    out_bff.emit_var_assignment("ProjectRebuildCommand",
                                                f"fbuild -ide -config \"{bff_path}\" -clean {target_node_name}")
                    # ProjectCleanCommand
                    out_bff.emit_var_assignment("LocalDebuggerCommand", "")

                    out_bff.emit_var_assignment("AdditionalOptions", f"/std:{lang_standard}")

                    out_bff._dedent()
                    out_bff._emit_line("]")
                    out_bff._emit_line(".ProjectConfigs + .cfg")

        project_nodes.append(project_node_name)

        # solution
        sln_path = fs.path.join(vs_dir_abs_path, f"{wks_name}.sln")

        with out_bff.vssolution(self.SLN_TARGET_NAME):
            out_bff.emit_var_assignment("SolutionOutput", sln_path)
            out_bff.emit_var_assignment("SolutionProjects", project_nodes)
            out_bff.line_break()

            if False:
                sln_configs = []

                for toolchain_name in toolchains_manifest.keys():
                    for build_type in build_types:
                        cfg = {
                            "Platform": "x64",
                            "Config": f"{toolchain_name}-{build_type}",
                            "SolutionPlatform": toolchain_name,
                            "SolutionConfig": build_type,
                            "SolutionBuildProject": all_targets_project_path
                        }
                        sln_configs.append(cfg)
                out_bff.emit_var_assignment("SolutionConfigs", sln_configs)
                out_bff.line_break()

                sln_deps = [
                    {
                        "Projects": project_nodes,
                        "Dependencies": [all_targets_project_path]
                    }
                ]

                out_bff.emit_var_assignment("SolutionDependencies", sln_deps, should_split_str=True)

            else:
                out_bff._emit_line(".SolutionConfigs = {}")

                for toolchain_name in toolchains_manifest.keys():
                    for build_type in build_types:
                        out_bff._emit_line(".cfg = [")
                        out_bff._indent()

                        out_bff.emit_var_assignment("Platform", "x64")
                        out_bff.emit_var_assignment("Config", f"{toolchain_name}-{build_type}")
                        out_bff.emit_var_assignment("SolutionPlatform", toolchain_name)
                        out_bff.emit_var_assignment("SolutionConfig", build_type)
                        out_bff.emit_var_assignment("SolutionBuildProject", all_targets_project_path)

                        out_bff._dedent()
                        out_bff._emit_line("]")
                        out_bff._emit_line(".SolutionConfigs + .cfg")
                out_bff.line_break()

                out_bff._emit_line(".SolutionDependencies = {}")

                out_bff._emit_line(".dep = [")
                out_bff._indent()

                out_bff.emit_var_assignment("Projects", project_nodes)
                out_bff.emit_var_assignment("Dependencies", [all_targets_project_path])

                out_bff._dedent()
                out_bff._emit_line("]")
                out_bff._emit_line(".SolutionDependencies + .dep")
            out_bff.line_break()

            out_bff.emit_var_assignment("SolutionVisualStudioVersion", latest_vs_version)
            out_bff.emit_var_assignment("SolutionMinimumVisualStudioVersion", latest_vs_version)
