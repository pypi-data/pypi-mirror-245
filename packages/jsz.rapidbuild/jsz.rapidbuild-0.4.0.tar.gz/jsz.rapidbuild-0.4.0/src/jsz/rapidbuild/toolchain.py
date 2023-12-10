from . import base


class ToolchainSettingsProviderDefault(base.ToolchainSettingsProvider):
    @staticmethod
    def _get_toolchain_settings_win_vs_msvc():
        return {
            "compiler_args": {
                "all": [
                    '/options:strict',
                    # warning level 4, as errors, all
                    '/W4', '/WX', '/Wall', '/Wv:19.33',
                    # Info: function not inlined
                    '/wd4710',
                    # Info: the compiler performed inlining on the given function, although it was not marked
                    # for inlining.
                    '/wd4711',
                    # Compiler will insert Spectre mitigation for memory load if /Qspectre switch specified
                    '/wd5045',
                    # 'struct': '4' bytes padding added after data member 'struct::member'
                    '/wd4820',
                    # do not report warnings from third parties
                    '/experimental:external', '/external:anglebrackets', '/external:W0',
                    # specifies that are sources are C + +
                    '/TP',
                    # set standard
                    '/std:c++17', '/permissive-',
                    # enable string pooling
                    '/GF',
                    # disable RTTI
                    '/GR-',
                    # s: Enables standard C++ stack unwinding. Catches only standard C++ exceptions when you
                    #    use catch(...) syntax.
                    # c: Compiler assumes that functions declared as extern "C" never throw a C++ exception.
                    '/EHsc',
                    # no acquire / release semantics for volatile vars
                    '/volatile:iso',
                    # require to always define the class before declaring a pointer-to-member
                    '/vmb',
                    # disable M$ C extensions
                    # '/Za ' # not recommended for C + + code
                    # Force synchronous PDB writes, since fastbuild uses multiple cl.exe instances.
                    '/FS',
                ],
                base.BUILD_TYPE_DEBUG: [
                    '/MDd',
                    # disable optimization
                    '/Od',
                    # debug format: PDB
                    '/Zi',
                    # faster PDB generation
                    '/Zf',
                    # floats according to standard
                    '/fp:strict',
                    # enable buffer security checks
                    '/GS',
                    '/sdl',
                    # enable control flow guards
                    '/guard:cf',
                    # enable EH continuation metadata(must be also present in linker args)
                    '/guard:ehcont',
                    # enable all runtime checks.RTCc rejects conformant code, so it is not supported by
                    # the C++ Standard Library
                    '/RTCsu',
                ],
                base.BUILD_TYPE_RELEASE: [
                    '/MD',
                    # enable optimization
                    '/O2',
                    # fast floats
                    '/fp:fast',
                    # disable buffer security checks
                    '/GS-',
                    # + '/sdl- ' // it overrides / GS -
                    # disable control flow guards
                    '/guard:cf-',
                    # disable EH continuation metadata
                    '/guard:ehcont-',
                ],
                base.BUILD_TYPE_PROFILING: [
                    '/MD',
                    # enable optimization
                    '/O2',
                    # debug format: PDB
                    '/Zi',
                    # faster PDB generation
                    '/Zf',
                    # fast floats
                    '/fp:fast',
                    # disable buffer security checks
                    '/GS-',
                    # + '/sdl- ' // it overrides / GS -
                    # disable control flow guards
                    '/guard:cf-',
                    # disable EH continuation metadata
                    '/guard:ehcont-',
                ],
            },
            "definitions": {
                "all": {
                    "_MT": None,
                    "_DLL": None,
                },
                base.BUILD_TYPE_DEBUG: {
                    "_DEBUG": None,
                },
                base.BUILD_TYPE_RELEASE: {
                },
                base.BUILD_TYPE_PROFILING: {
                },
            },
            "linker_args": {
                "all": [
                    "/WX",
                    # Cannot use debug info for 'some.lib(some.obj)'
                    "/IGNORE:4099",
                    "/machine:x64",
                ],
                base.BUILD_TYPE_DEBUG: [
                    "/DEBUG",
                    "/GUARD:CF",
                ],
                base.BUILD_TYPE_RELEASE: [
                    "/GUARD:CF",
                ],
                base.BUILD_TYPE_PROFILING: [
                    "/DEBUG",
                    "/GUARD:CF",
                ],
            },
            "link_libs": {
                "all": [
                    'kernel32.lib',
                    'user32.lib',
                    'gdi32.lib',
                    'shell32.lib',
                    'winspool.lib',
                    'ole32.lib',
                    'oleaut32.lib',
                    'uuid.lib',
                    'comdlg32.lib',
                    'advapi32.lib',
                ],
                base.BUILD_TYPE_DEBUG: [
                    # DLL import library for the Debug version of the UCRT (ucrtbased.dll).
                    'ucrtd.lib',
                    # Static library for the Debug version of the native CRT startup for use with DLL UCRT and vcruntime.
                    'msvcrtd.lib',
                    # DLL import library for the Debug vcruntime (vcruntime<version>d.dll).
                    'vcruntimed.lib',
                    # Multithreaded, dynamic link (import library for msvcp<version>d.dll)
                    'msvcprtd.lib',
                ],
                base.BUILD_TYPE_RELEASE: [
                    # DLL import library for the UCRT (ucrtbase.dll).
                    'ucrt.lib',
                    # Static library for the native CRT startup for use with DLL UCRT and vcruntime.
                    'msvcrt.lib',
                    # DLL import library for the vcruntime (vcruntime<version>.dll).
                    'vcruntime.lib',
                    # Multithreaded, dynamic link (import library for msvcp<version>.dll)
                    'msvcprt.lib',
                ],
                base.BUILD_TYPE_PROFILING: [
                    # DLL import library for the UCRT (ucrtbase.dll).
                    'ucrt.lib',
                    # Static library for the native CRT startup for use with DLL UCRT and vcruntime.
                    'msvcrt.lib',
                    # DLL import library for the vcruntime (vcruntime<version>.dll).
                    'vcruntime.lib',
                    # Multithreaded, dynamic link (import library for msvcp<version>.dll)
                    'msvcprt.lib',
                ],
            },
        }

    @staticmethod
    def _get_toolchain_settings_win_vs_llvm():
        return {
            "compiler_args": {
                "all": [
                    # warnings
                    '-Wall', '-Wextra', '-pedantic', '-pedantic-errors', '-Werror',
                    # set standard
                    '-std=c++17',
                    # disable RTTI
                    '-fno-rtti',
                    # disable exceptions
                    '-fno-exceptions',
                    # use a best-case representation method for member pointers
                    '-fcomplete-member-pointers',
                    # enable AVX support; this option is hidden in --help
                    '-mavx',
                ],
                base.BUILD_TYPE_DEBUG: [
                    '-O0',
                    '-g',
                ],
                base.BUILD_TYPE_RELEASE: [
                    '-O3',
                    '-ffast-math',
                ],
                base.BUILD_TYPE_PROFILING: [
                    '-O3',
                    '-ffast-math',
                    '-g',
                ],
            },
            "definitions": {
                "all": {
                    "_MT": None,
                    "_DLL": None,
                },
                base.BUILD_TYPE_DEBUG: {
                    "_DEBUG": None,
                },
                base.BUILD_TYPE_RELEASE: {
                },
                base.BUILD_TYPE_PROFILING: {
                },
            },
            "linker_args": {
                "all": [
                    "/WX",
                    # Cannot use debug info for 'some.lib(some.obj)'
                    "/IGNORE:4099",
                    "/machine:x64",
                ],
                base.BUILD_TYPE_DEBUG: [
                    "/DEBUG",
                    "/GUARD:CF",
                ],
                base.BUILD_TYPE_RELEASE: [
                    "/GUARD:CF",
                ],
                base.BUILD_TYPE_PROFILING: [
                    "/GUARD:CF",
                ],
            },
            "link_libs": {
                "all": [
                    'kernel32.lib',
                    'user32.lib',
                    'gdi32.lib',
                    'shell32.lib',
                    'winspool.lib',
                    'ole32.lib',
                    'oleaut32.lib',
                    'uuid.lib',
                    'comdlg32.lib',
                    'advapi32.lib',
                ],
                base.BUILD_TYPE_DEBUG: [
                    # THE ORDER OF THESE IMPORT LIBS IS IMPORTANT
                    # Switching msvcrtd.lib with vcruntimed.lib results in a duplicate symbol error with lld-link.
                    
                    # DLL import library for the Debug version of the UCRT (ucrtbased.dll).
                    'ucrtd.lib',
                    # Static library for the Debug version of the native CRT startup for use with DLL UCRT and vcruntime.
                    'msvcrtd.lib',
                    # DLL import library for the Debug vcruntime (vcruntime<version>d.dll).
                    'vcruntimed.lib',
                    # Multithreaded, dynamic link (import library for msvcp<version>d.dll)
                    'msvcprtd.lib',
                ],
                base.BUILD_TYPE_RELEASE: [
                    # DLL import library for the UCRT (ucrtbase.dll).
                    'ucrt.lib',
                    # Static library for the native CRT startup for use with DLL UCRT and vcruntime.
                    'msvcrt.lib',
                    # DLL import library for the vcruntime (vcruntime<version>.dll).
                    'vcruntime.lib',
                    # Multithreaded, dynamic link (import library for msvcp<version>.dll)
                    'msvcprt.lib',
                ],
                base.BUILD_TYPE_PROFILING: [
                    # DLL import library for the UCRT (ucrtbase.dll).
                    'ucrt.lib',
                    # Static library for the native CRT startup for use with DLL UCRT and vcruntime.
                    'msvcrt.lib',
                    # DLL import library for the vcruntime (vcruntime<version>.dll).
                    'vcruntime.lib',
                    # Multithreaded, dynamic link (import library for msvcp<version>.dll)
                    'msvcprt.lib',
                ],
            },
        }

    def get_toolchain_settings(self):
        return {
            base.TOOLCHAIN_VS16_MSVC: self._get_toolchain_settings_win_vs_msvc(),
            base.TOOLCHAIN_VS16_LLVM13: self._get_toolchain_settings_win_vs_llvm(),
            base.TOOLCHAIN_VS17_MSVC: self._get_toolchain_settings_win_vs_msvc(),
            base.TOOLCHAIN_VS17_LLVM13: self._get_toolchain_settings_win_vs_llvm(),
        }
