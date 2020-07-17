%global DATE 20180712
%global SVNREV 262599
%global gcc_version 7.3.1
%global gcc_major 7
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 9
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
%if 0%{?fedora} > 27
# Until annobin is fixed (#1519165).
%undefine _annotated_build
%endif
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64
%global build_ada 1
%else
%global build_ada 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%global build_objc 1
%global build_fortran 1
%global build_multilib 1

%ifarch %{ix86} x86_64 aarch64
%global build_libsanitizer 1
%else
%global build_libsanitizer 0
%endif

%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifarch %{ix86} x86_64
%global build_libmpx 1
%else
%global build_libmpx 0
%endif
%global build_isl 1
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64 ppc64p7
%global multilib_32_arch ppc
%endif

%ifarch x86_64
%global multilib_32_arch i686
%endif

# Disable %check by default
%bcond_with checks

Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-7-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
%global isl_version 0.16.1
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
BuildRequires: binutils >= 2.24
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
BuildRequires: python-devel
BuildRequires: automake >= 1.11
# Needed for dwarf4 support, otherwise the debuginfo packages are useless
BuildRequires: rpm-build >= 4.8.0-32

%if %{build_go}
BuildRequires: hostname, procps
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}

#%if 0%{?__isa_bits} == 64
#Requires: libisl.so.15()(64bit)
#%else
#Requires: libisl.so.15
#%endif

%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
Requires: binutils >= 2.24
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
%endif
Obsoletes: gcc-java < %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true
Provides: bundled(libiberty)
Provides: gcc(major) = %{gcc_major}

Patch0: gcc7-hack.patch
Patch2: gcc7-i386-libgomp.patch
Patch3: gcc7-sparc-config-detection.patch
Patch4: gcc7-libgomp-omp_h-multilib.patch
Patch5: gcc7-libtool-no-rpath.patch
Patch6: gcc7-isl-dl.patch
Patch7: gcc7-libstdc++-docs.patch
Patch8: gcc7-no-add-needed.patch
Patch9: gcc7-aarch64-async-unw-tables.patch
Patch10: gcc7-foffload-default.patch
Patch11: gcc7-Wno-format-security.patch
Patch12: gcc7-aarch64-sanitizer-fix.patch
Patch13: gcc7-rh1512529-aarch64.patch
Patch14: gcc7-pr84128.patch

# Amazon patches
Patch10000: gcc-7.3.1-Add-vec-reverse.patch
Patch10001: gcc-7.3.1-falign-functions-max-0001.patch
Patch10002: gcc-7.3.1-falign-functions-max-0002.patch
Patch10005: gcc-7.3.1-aarch64-Set-default-values-for-falign.patch
Patch10006: 1000-graviton_support.patch

# Graviton2 patches
Patch20000: 0001-Allow-const0_rtx-operand-for-atomic-compare-exchange.patch
Patch20001: 0002-Add-early-clobber-for-aarch64_store_exclusive.patch
Patch20002: 0003-aarch64-Simplify-LSE-cas-generation.patch
Patch20003: 0004-Emit-tighter-strong-atomic-compare-exchange-loop-whe.patch
Patch20004: 0005-aarch64-Improve-cas-generation.patch
Patch20005: 0006-aarch64-Improve-swp-generation.patch
Patch20006: 0007-aarch64-Improve-atomic-op-lse-generation.patch
Patch20007: 0008-aarch64-Remove-early-clobber-from-ATOMIC_LDOP-scratc.patch
Patch20008: 0009-aarch64-Extend-R-for-integer-registers.patch
Patch20009: 0010-aarch64-Implement-TImode-compare-and-swap.patch
Patch20010: 0011-Fix-shrinkwrapping-interactions-with-atomics-PR92692.patch
Patch20011: 0012-aarch64-Tidy-aarch64_split_compare_and_swap.patch
Patch20012: 0013-aarch64-Add-out-of-line-functions-for-LSE-atomics.patch
Patch20013: 0014-Add-visibility-to-libfunc-constructors.patch
Patch20014: 0015-atomic_cmp_exchange_zero_reg_1.c-Pass-march-armv8-a-.patch
Patch20015: 0016-aarch64-Implement-moutline-atomics.patch
Patch20016: 0017-aarch64-Fix-store-exclusive-in-load-operate-LSE-help.patch
Patch20017: 0018-aarch64-Configure-for-sys-auxv.h-in-libgcc-for-lse-i.patch
Patch20018: 0019-aarch64-Fix-up-aarch64_compare_and_swaphi-pattern-PR.patch
Patch20019: 0020-aarch64-Fix-bootstrap-with-old-binutils-PR93053.patch
Patch20020: 0021-aarch64-Fix-ICE-due-to-aarch64_gen_compare_reg_maybe.patch
Patch20021: 0022-re-PR-target-90724-ICE-with-__sync_bool_compare_and_.patch
Patch20022: 0023-aarch64-Fix-for-PR-target-94814.patch
Patch20023: 0024-aarch64-Force-TImode-values-into-even-registers.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
%endif # arm
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc ppc64p7
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc ppc64p7
%global gcc_target_platform %{_target_platform}
%endif

%if 0%{?fedora} >= 27
%if %{build_go}
# Avoid stripping these libraries and binaries.
%global __os_install_post \
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.11.* \
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
%__os_install_post \
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.11.* \
chmod 755 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 755 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
%{nil}
%endif
%endif

Obsoletes: libmudflap-devel
Obsoletes: libmudflap-static
# Main package now inclues static libraries for which we used to have
# versioned subpackages
Obsoletes: libatomic-static < %{version}-%{release}
%if %{build_libatomic}
Provides: libatomic-static = %{version}-%{release}
%endif
Obsoletes: libitm-static < %{version}-%{release}
Obsoletes: libitm-devel < %{version}-%{release}
%if %{build_libitm}
Provides: libitm-static = %{version}-%{release}
Provides: libitm-devel = %{version}-%{release}
Provides: libitm-devel%{?_isa} = %{version}-%{release}
%endif
Obsoletes: libquadmath-devel < %{version}-%{release}
Obsoletes: libquadmath-static < %{version}-%{release}
%if %{build_libquadmath}
Provides: libquadmath-devel = %{version}-%{release}
Provides: libquadmath-devel%{?_isa} = %{version}-%{release}
Provides: libquadmath-static = %{version}-%{release}
%endif
Obsoletes: libgcj-devel < %{version}-%{release}
Obsoletes: libgcj-src < %{version}-%{release}

Obsoletes: libtsan-static < %{version}-%{release}
%if %{build_libsanitizer}
Provides: libtsan-static = %{version}-%{release}
%endif

%description
The gcc package contains the GNU Compiler Collection version 7.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 7 shared support library
Group: System Environment/Libraries
Obsoletes: libmudflap
Obsoletes: libgcj

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc%{?_isa} = %{version}-%{release}
Requires: libstdc++%{?_isa} = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true
Obsoletes: libstdc++-devel < %{version}-%{release}
Obsoletes: libstdc++-static < %{version}-%{release}
Provides: libstdc++-devel = %{version}-%{release}
Provides: libstdc++-devel%{?_isa} = %{version}-%{release}
Provides: libstdc++-static = %{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%if %{build_objc}
%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%endif # build_objc

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true
Obsoletes: libgfortran-devel < %{version}-%{release}
Obsoletes: libgfortran-static < %{version}-%{release}

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.

%package gdb-plugin
Summary: GCC plugin for GDB
Group: Development/Debuggers
Requires: gcc = %{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Group: System Environment/Libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
Group: Development/Libraries
BuildRequires: %{_bindir}/sphinx-build
Requires: libgccjit = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library which is a GCC support runtime
library for atomic operations not supported by hardware.

%package -n libsanitizer
Summary: Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Obsoletes: libtsan = 4.8.5
Obsoletes: libtsan = 4.8.3

%description -n libsanitizer
This package contains sanitizer libraries which are automatically used when
the appropriate -fsanitize option is used for instrumented programs
   -fsanitize=address           will use the Address Sanitizer (libasan)
   -fsanitize=thread            will use the Thread Sanitizer (libtsan)
   -fsanitize=undefined         will use the Undefined Behaviour Sanitizer (libubsan)
   -fsanitize=leak              will use the Leak Sanitizer library (liblsan)


%package -n libcilkrts
Summary: The Cilk+ runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libcilkrts
This package contains the Cilk+ runtime library.

%package -n libmpx
Summary: The Memory Protection Extensions runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libmpx
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: filesystem >= 3
Provides: /lib/cpp
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true
Obsoletes: libgnat-devel < %{version}-%{release}
Provides: libgnat-devel = %{version}-%{release}
Provides: libgnat-devel%{?_isa} = %{version}-%{release}
Obsoletes: libgnat-static < %{version}-%{release}
Provides: libgnat-static = %{version}-%{release}

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Autoreq: true
Obsoletes: libgo-devel < %{version}-%{release}
Provides: libgo-devel = %{version}-%{release}
Provides: libgo-devel%{?_isa} = %{version}-%{release}
Obsoletes: libgo-static < %{version}-%{release}
Provides: libgo-static = %{version}-%{release}

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%if 0%{?fedora} < 27 || 0%{?amzn}
%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%global __debug_package 1
%global __debug_install_post \
   PATH=%{_builddir}/gcc-%{version}-%{DATE}/dwz-wrapper/:$PATH %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_dwz_opts} %{?_find_debuginfo_opts} "%{_builddir}/gcc-%{version}-%{DATE}"\
    %{_builddir}/gcc-%{version}-%{DATE}/split-debuginfo.sh\
%{nil}

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: gcc-base-debuginfo = %{version}-%{release}

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files debuginfo -f debugfiles.list

%package base-debuginfo
Summary: Debug information for libraries from package %{name}
Group: Development/Debug
AutoReqProv: 0

%description base-debuginfo
This package provides debug information for libgcc_s, libgomp and
libstdc++ libraries from package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files base-debuginfo -f debugfiles-base.list
%endif
%endif

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch2 -p0 -b .i386-libgomp~
%patch3 -p0 -b .sparc-config-detection~
%patch4 -p0 -b .libgomp-omp_h-multilib~
%patch5 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch6 -p0 -b .isl-dl~
%endif
%if %{build_libstdcxx_docs}
%patch7 -p0 -b .libstdc++-docs~
%endif
%patch8 -p0 -b .no-add-needed~
%patch9 -p0 -b .aarch64-async-unw-tables~
%patch10 -p0 -b .foffload-default~
%patch11 -p0 -b .Wno-format-security~
%if 0%{?fedora} > 27
%patch12 -p0 -b .aarch64-sanitizer-fix~
%endif
%patch13 -p0 -b .rh1512529-aarch64~
%patch14 -p0 -b .pr84128~

%patch10000 -p1 -b .vec
%patch10001 -p1 -b .falign1
%patch10002 -p1 -b .falign2
%patch10005 -p1 -b .falign3
%patch10006 -p1 -b .graviton_detection

%patch20000 -p1 -b .graviton2_support_1
%patch20001 -p1 -b .graviton2_support_2
%patch20002 -p1 -b .graviton2_support_3
%patch20003 -p1 -b .graviton2_support_4
%patch20004 -p1 -b .graviton2_support_5
%patch20005 -p1 -b .graviton2_support_6
%patch20006 -p1 -b .graviton2_support_7
%patch20007 -p1 -b .graviton2_support_8
%patch20008 -p1 -b .graviton2_support_9
%patch20009 -p1 -b .graviton2_support_10
%patch20010 -p1 -b .graviton2_support_11
%patch20011 -p1 -b .graviton2_support_12
%patch20012 -p1 -b .graviton2_support_13
%patch20013 -p1 -b .graviton2_support_14
%patch20014 -p1 -b .graviton2_support_15
%patch20015 -p1 -b .graviton2_support_16
%patch20016 -p1 -b .graviton2_support_17
%patch20017 -p1 -b .graviton2_support_18
%patch20018 -p1 -b .graviton2_support_19
%patch20019 -p1 -b .graviton2_support_20
%patch20020 -p1 -b .graviton2_support_21
%patch20021 -p1 -b .graviton2_support_22
%patch20022 -p1 -b .graviton2_support_23
%patch20023 -p1 -b .graviton2_support_24

%if 0%{?fedora} < 27 || 0%{?amzn}
%if 0%{?_enable_debug_packages}
mkdir dwz-wrapper
if [ -f /usr/bin/dwz ]; then
cat > dwz-wrapper/dwz <<\EOF
#!/bin/bash
dwz_opts=
dwzm_opts=
dwz_files=
dwzm_files=
while [ $# -gt 0 ]; do
  case "$1" in
  -l|-L)
    dwz_opts="$dwz_opts $1 $2"; shift;;
  -m|-M)
    dwzm_opts="$dwzm_opts $1 $2"; shift;;
  -*)
    dwz_opts="$dwz_opts $1";;
  *)
    if [[ "$1" =~ (lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm|go\.so)|bin/gofmt.gcc.debug|bin/go.gcc.debug|/cgo.debug) ]]; then
      dwz_files="$dwz_files $1"
    else
      dwzm_files="$dwzm_files $1"
    fi;;
  esac
  shift
done
if [ -f /usr/bin/dwz ]; then
  /usr/bin/dwz $dwz_opts $dwz_files
  /usr/bin/dwz $dwz_opts $dwzm_opts $dwzm_files
fi
EOF
chmod 755 dwz-wrapper/dwz
fi
cat > split-debuginfo.sh <<\EOF
#!/bin/sh
BUILDDIR="%{_builddir}/gcc-%{version}-%{DATE}"
if [ -f "${BUILDDIR}"/debugfiles.list \
     -a -f "${BUILDDIR}"/debuglinks.list ]; then
  > "${BUILDDIR}"/debugsources-base.list
  > "${BUILDDIR}"/debugfiles-base.list
  cd "${RPM_BUILD_ROOT}"
  for f in `find usr/lib/debug -name \*.debug \
	    | egrep 'lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm)'`; do
    echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
    if [ -f "$f" -a ! -L "$f" ]; then
      cp -a "$f" "${BUILDDIR}"/test.debug
      /usr/lib/rpm/debugedit -b "${RPM_BUILD_DIR}" -d /usr/src/debug \
			     -l "${BUILDDIR}"/debugsources-base.list \
			     "${BUILDDIR}"/test.debug
      rm -f "${BUILDDIR}"/test.debug
    fi
  done
  for f in `find usr/lib/debug/.build-id -type l`; do
    ls -l "$f" | egrep -q -- '->.*lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm)' \
      && echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
  done
  cp -a "${BUILDDIR}"/debugfiles-base.list "${BUILDDIR}"/debugfiles-remove.list
%if %{build_go}
  libgoso=`basename .%{_prefix}/%{_lib}/libgo.so.11.*`
  for f in %{_prefix}/bin/go.gcc \
	   %{_prefix}/bin/gofmt.gcc \
	   %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
	   %{_prefix}/%{_lib}/$libgoso ; do
    eu-unstrip .$f usr/lib/debug$f.debug -o .$f.new
    chmod --reference=.$f .$f.new
    mv -f .$f.new .$f
    rm -f usr/lib/debug$f.debug
    echo "/usr/lib/debug$f.debug" >> "${BUILDDIR}"/debugfiles-remove.list
  done
  rm -f usr/lib/debug%{_prefix}/%{_lib}/libgo.so.11.debug
  echo "/usr/lib/debug%{_prefix}/%{_lib}/libgo.so.11.debug" >> "${BUILDDIR}"/debugfiles-remove.list
  for f in `find usr/lib/debug/.build-id -type l`; do
    if ls -l "$f" | egrep -q -- '->.*(/bin/go.gcc|/bin/gofmt.gcc|/cgo|lib[0-9]*/libgo\.so)'; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-remove.list
      rm -f "$f"
    fi
  done
%endif
  grep -v -f "${BUILDDIR}"/debugfiles-remove.list \
    "${BUILDDIR}"/debugfiles.list > "${BUILDDIR}"/debugfiles.list.new
  mv -f "${BUILDDIR}"/debugfiles.list.new "${BUILDDIR}"/debugfiles.list
  for f in `LC_ALL=C sort -z -u "${BUILDDIR}"/debugsources-base.list \
	    | grep -E -v -z '(<internal>|<built-in>)$' \
	    | xargs --no-run-if-empty -n 1 -0 echo \
	    | sed 's,^,usr/src/debug/,'`; do
    if [ -f "$f" ]; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
      echo "%%exclude /$f" >> "${BUILDDIR}"/debugfiles.list
    fi
  done
  mv -f "${BUILDDIR}"/debugfiles-base.list{,.old}
  echo "%%dir /usr/lib/debug" > "${BUILDDIR}"/debugfiles-base.list
  awk 'BEGIN{FS="/"}(NF>4&&$NF){d="%%dir /"$2"/"$3"/"$4;for(i=5;i<NF;i++){d=d"/"$i;if(!v[d]){v[d]=1;print d}}}' \
    "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  cat "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  rm -f "${BUILDDIR}"/debugfiles-base.list.old
fi
EOF
chmod 755 split-debuginfo.sh
%endif
%endif

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
%ifarch aarch64
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fexceptions/-fexceptions -falign-jumps=32:16 -falign-loops=32:16 -falign-functions=32:16/g'`
%endif
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

enablelgo=
enablelada=
enablefortran=
enableobjc=
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_fortran}
enablefortran=,fortran
%endif
%if %{build_objc}
enableobjc=,objc,obj-c++
%endif

CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux \
%endif
%ifarch %{multilib_64_archs}
    --enable-multilib \
%else
	--disable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
%ifnarch %{mips}
	--with-linker-hash-style=gnu \
%endif
	--enable-plugin --enable-initfini-array \
%if %{build_isl}
	--with-isl \
%else
	--without-isl \
%endif
%if %{build_libmpx}
	--enable-libmpx \
%else
	--disable-libmpx \
%endif
%if %{build_libsanitizer}
    --enable-libsanitizer \
%else
    --disable-libsanitizer \
%endif # build_libsanitizer
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%if %{build_libcilkrts}
        --enable-libcilkrts \
%else
        --disable-libcilkrts \
%endif
%if %{build_libatomic}
        --enable-libatomic \
%else
        --disable-libatomic \
%endif
%ifarch ppc64le
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%if %{build_libquadmath}
    --enable-libquadmath \
%else
    --disable-libquadmath \
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%if %{build_libitm}
    --enable-libitm \
%else
    --disable-libitm \
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
	--with-arch=z196 --with-tune=zEC12 --enable-decimal-float \
%else
%if 0%{?fedora} >= 26
	--with-arch=zEC12 --with-tune=z13 --enable-decimal-float \
%else
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif #fedora
%endif #rhel
%endif #s390
%ifarch armv7hl
	--with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
	--with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
	--with-arch=mips64r2 --with-abi=64 \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform} \
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
    --enable-languages=c,c++${enableobjc}${enablefortran}${enablelada}${enablelgo},lto \
	$CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}

for i in {gcc,gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -rf %{buildroot}

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
rm -f %{buildroot}%{_prefix}/lib/cpp
ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc
mkdir -p %{buildroot}%{_fmoddir}

%if %{build_go}
mv %{buildroot}%{_prefix}/bin/go{,.gcc}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_prefix}/bin/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_prefix}/bin/gofmt
%endif

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64 ppc64p7
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

FULLLSUBDIR=
%ifarch sparcv9 ppc
FULLLSUBDIR=lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLSUBDIR=lib64
%endif
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

%if %{build_fortran}
mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%endif # build_fortran
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libsanitizer}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif
%if %{build_libcilkrts}
mv %{buildroot}%{_prefix}/%{_lib}/libcilkrts.spec $FULLPATH/
%endif
%if %{build_libmpx}
mv %{buildroot}%{_prefix}/%{_lib}/libmpx.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64 ppc64p7
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif
%ifarch %{arm} aarch64
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/ \
	       %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
  %{__python} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
done

rm -f $FULLEPATH/libgccjit.so
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_prefix}/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif # build_objc
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
%if %{build_fortran}
ln -sf ../../../libgfortran.so.4.* libgfortran.so
%endif # build_fortran
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.11.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libsanitizer}
ln -sf ../../../libasan.so.4.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
ln -sf ../../../libubsan.so.0.* libubsan.so
%endif # build_libsanitizer
%if %{build_libcilkrts}
ln -sf ../../../libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../libmpx.so.2.* libmpx.so
ln -sf ../../../libmpxwrappers.so.2.* libmpxwrappers.so
%endif
else # "%{_lib}" = "lib"
%if %{build_objc}
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
%endif # build_objc
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
%if %{build_fortran}
ln -sf ../../../../%{_lib}/libgfortran.so.4.* libgfortran.so
%endif # build_fortran
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.11.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libsanitizer}
ln -sf ../../../../%{_lib}/libasan.so.4.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
ln -sf ../../../../%{_lib}/libubsan.so.0.* libubsan.so
%ifarch x86_64 aarch64
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.0.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../../%{_lib}/libtsan_preinit.o libtsan_preinit.o
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
%endif
%endif # build_libsanitizer
%if %{build_libcilkrts}
ln -sf ../../../../%{_lib}/libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../../%{_lib}/libmpx.so.2.* libmpx.so
ln -sf ../../../../%{_lib}/libmpxwrappers.so.2.* libmpxwrappers.so
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
%endif # build_fortran
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
%endif # build_objc
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libsanitizer}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%ifarch x86_64 aarch64
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLLPATH/
%endif
%endif
%if %{build_libcilkrts}
mv -f %{buildroot}%{_prefix}/%{_lib}/libcilkrts.*a $FULLLPATH/
%endif
%if %{build_libmpx}
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpx.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.*a $FULLLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-7.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-7.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-7.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-7.so
fi
popd
fi
%endif # build_ada

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.4.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.11.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.11.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libatomic.so
%endif
%if %{build_libsanitizer}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.4.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.4.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > 64/libubsan.so
%endif # build_libsanitizer
%if %{build_libcilkrts}
rm -f libcilkrts.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > libcilkrts.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > 64/libcilkrts.so
%endif
%if %{build_libmpx}
rm -f libmpx.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpx.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > 64/libmpx.so
rm -f libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > 64/libmpxwrappers.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libsanitizer}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif # build_libsanitizer
%if %{build_libcilkrts}
ln -sf lib32/libcilkrts.a libcilkrts.a
ln -sf ../lib64/libcilkrts.a 64/libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf lib32/libmpx.a libmpx.a
ln -sf ../lib64/libmpx.a 64/libmpx.a
ln -sf lib32/libmpxwrappers.a libmpxwrappers.a
ln -sf ../lib64/libmpxwrappers.a 64/libmpxwrappers.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
ln -sf lib32/libgolibbegin.a libgolibbegin.a
ln -sf ../lib64/libgolibbegin.a 64/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif #sparcv9

%ifarch %{multilib_64_archs}
mkdir -p 32
%if %{build_objc}
ln -sf ../../../../libobjc.so.4 32/libobjc.so
%endif
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
%if %{build_fortran}
ln -sf ../`echo ../../../../lib64/libgfortran.so.4.* | sed s~/../lib64/~/~` 32/libgfortran.so
%endif
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so

%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.11.* | sed 's,^.*libg,libg,'`' )' > libgo.so
%ifarch %{multilib_64_archs}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.11.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%endif

%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
%ifarch %{multilib_64_archs}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%endif

%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
%ifarch %{multilib_64_archs}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%endif

%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
%ifarch %{multilib_64_archs}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libatomic.so
%endif
%endif

%if %{build_libsanitizer}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.4.* | sed 's,^.*liba,liba,'`' )' > libasan.so
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
%ifarch %{multilib_64_archs}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.4.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > 32/libubsan.so
%endif
%endif # build_libsanitizer

%if %{build_libcilkrts}
rm -f libcilkrts.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > libcilkrts.so
%if %{build_multilib}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > 32/libcilkrts.so
%endif
%endif

%if %{build_libmpx}
rm -f libmpx.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpx.so
rm -f libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpxwrappers.so
%if %{build_multilib}
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > 32/libmpx.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > 32/libmpxwrappers.so
%endif
%endif

%if %{build_objc}
%if %{build_multilib}
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%endif

%endif # multilib_64_archs

%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libsanitizer}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
ln -sf ../lib32/libubsan.a 32/libubsan.a
ln -sf lib64/libubsan.a libubsan.a
%endif # build_libsanitizer
%if %{build_libcilkrts}
ln -sf ../lib32/libcilkrts.a 32/libcilkrts.a
ln -sf lib64/libcilkrts.a libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf ../lib32/libmpx.a 32/libmpx.a
ln -sf lib64/libmpx.a libmpx.a
ln -sf ../lib32/libmpxwrappers.a 32/libmpxwrappers.a
ln -sf lib64/libmpxwrappers.a libmpxwrappers.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
ln -sf ../lib32/libgolibbegin.a 32/libgolibbegin.a
ln -sf lib64/libgolibbegin.a libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif

%else # sparc64 ppc64 ppc64p7

%ifarch %{multilib_64_archs}
%if %{build_fortran}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgfortran.a 32/libgfortran.a
%endif
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++fs.a 32/libstdc++fs.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libsupc++.a 32/libsupc++.a

%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libquadmath.a 32/libquadmath.a
%endif

%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libitm.a 32/libitm.a
%endif

%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libatomic.a 32/libatomic.a
%endif

%if %{build_libsanitizer}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libasan.a 32/libasan.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libubsan.a 32/libubsan.a
%endif

%if %{build_libcilkrts}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libcilkrts.a 32/libcilkrts.a
%endif

%if %{build_libmpx}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libmpx.a 32/libmpx.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libmpxwrappers.a 32/libmpxwrappers.a
%endif

%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgobegin.a 32/libgobegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgolibbegin.a 32/libgolibbegin.a
%endif

%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adalib 32/adalib
%endif
%endif # multilib_64_archs
%endif # sparc64 ppc64 ppc64p7

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a -o -name libcilkrts.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libmpx.a -o -name libmpxwrappers.a \
		-o -name libobjc.a \
		-o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libsupc++.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d/
  done
done
%endif

popd

%if %{build_fortran}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.4.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libsanitizer}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.4.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.0.*
%ifarch x86_64 aarch64
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%endif
%if %{build_libcilkrts}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcilkrts.so.5.*
%endif
%if %{build_libmpx}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpx.so.2.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.so.2.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.11.*
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*
%endif
%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec ${name} $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec ${name} $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib
%find_lang libstdc++

# Remove binaries and files we will not be including, so that they don't end
# up in gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a} || :
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/gappletviewer || :
rm -rf $FULLPATH/include-fixed
rm -rf $FULLPATH/include/ssp
rm -rf $FULLPATH/install-tools
rm -rf $FULLEPATH/install-tools

%if %{build_multilib}
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif # build_go
%else # multilib_64_archs
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif # sparcv9 ppc
%endif # multilib_64_archs
%endif # build_multilib

rm -f %{buildroot}%{_mandir}/man3/ffi*
rm -f %{buildroot}%{_mandir}/man7/*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%check
%if %{with checks}
cd obj-%{gcc_target_platform}

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%endif
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
rm -rf testlogs-%{_target_platform}-%{version}-%{release}
%endif # with checks

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
if [ -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%preun -n cpp
if [ $1 = 0 -a -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post gnat
if [ -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%preun gnat
if [ $1 = 0 -a -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%post go
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%if %{build_objc}
%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig
%endif

%if %{build_fortran}
%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig
%endif

%if %{build_ada}
%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig
%endif

%post -n libgomp
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post gdb-plugin -p /sbin/ldconfig

%postun gdb-plugin -p /sbin/ldconfig

%post -n libgccjit -p /sbin/ldconfig

%postun -n libgccjit -p /sbin/ldconfig

%post -n libgccjit-devel
if [ -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%preun -n libgccjit-devel
if [ $1 = 0 -a -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%post -n libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libsanitizer -p /sbin/ldconfig

%postun -n libsanitizer -p /sbin/ldconfig

%post -n libcilkrts -p /sbin/ldconfig

%postun -n libcilkrts -p /sbin/ldconfig

%post -n libmpx -p /sbin/ldconfig

%postun -n libmpx -p /sbin/ldconfig

%post -n libgo -p /sbin/ldconfig

%postun -n libgo -p /sbin/ldconfig

%files -f %{name}.lang
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
%{_prefix}/bin/gcov-dump
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%if ! 0%{build_multilib}
%{_prefix}/bin/%{gcc_target_platform}-gcc-ar
%{_prefix}/bin/%{gcc_target_platform}-gcc-nm
%{_prefix}/bin/%{gcc_target_platform}-gcc-ranlib
%endif # ! build_multilib
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64 ppc64p7
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-dump.1*
%{_mandir}/man1/gcov-tool.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vecintrin.h
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cilk
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.spec
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.spec
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.so
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.so
%endif # build_libsanitizer
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libmpxwrappers.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.so
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.so
%endif # build_libsanitizer
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libmpxwrappers.so
%endif
%endif # multilib_64_archs
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif # build_libsanitizer
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpxwrappers.so
%endif
%else # sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%ifarch x86_64 aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%endif # x86_64 aarch64
%endif # build_libsanitizer
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpxwrappers.so
%endif
%endif # sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

# MERGED SUBPACKAGES
%if %{build_libatomic}
%{_libdir}/libatomic.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif # build_libatomic

%if %{build_libitm}
%{_libdir}/libitm.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%doc rpm.doc/libitm/ChangeLog*
%endif
%if %{build_libquadmath}
%{_libdir}/libquadmath.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%doc rpm.doc/libquadmath/ChangeLog*
%endif
%if %{build_libsanitizer}
%{_libdir}/libasan.so
%ifarch x86_64 aarch64
%{_libdir}/liblsan.so
%{_libdir}/libtsan.so
%endif # x86_64 aarch64
%{_libdir}/libubsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%ifarch x86_64 aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif # build_libsanitizer
%if %{build_libcilkrts}
%{_libdir}/libcilkrts.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.a
%doc rpm.doc/changelogs/libcilkrts/ChangeLog* libcilkrts/README
%endif
%if %{build_libmpx}
%{_libdir}/libmpx.so
%{_libdir}/libmpxwrappers.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpxwrappers.a
%doc rpm.doc/changelogs/libmpx/ChangeLog*
%endif
%{_libdir}/libgomp.so
%{_libdir}/libgcc_s.so

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
%{_prefix}/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libsupc++.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libsupc++.a
%endif
%{_libdir}/libstdc++.so
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++ -f libstdc++.lang
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6.*
%{_prefix}/%{_lib}/libstdc++.so.6
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%if 0%{?_sys_python_major} >= 3
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%endif
%dir %{_prefix}/share/gcc-%{gcc_major}
%dir %{_prefix}/share/gcc-%{gcc_major}/python
%{_prefix}/share/gcc-%{gcc_major}/python/libstdcxx

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_objc}
%files objc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.so
%endif
%{_libdir}/libobjc.so
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.4*
%endif # build_objc

%if %{build_fortran}
%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%if ! 0%{build_multilib}
%{_prefix}/bin/%{_target_platform}-gfortran
%endif # ! build_multilib
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/finclude
%endif
%doc rpm.doc/gfortran/*
%{_libdir}/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.4*
%endif # build_fortran

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adalib
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so
%endif # build_ada

%files -n libgomp
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_libquadmath}
%files -n libquadmath
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*
%endif # build_libquadmath

%if %{build_libitm}
%files -n libitm
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*
%endif # build_libitm

%if %{build_libatomic}
%files -n libatomic
%{_prefix}/%{_lib}/libatomic.so.1*
%endif

%if %{build_libsanitizer}
%files -n libsanitizer
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%{_prefix}/%{_lib}/libasan.so.4*
%{_prefix}/%{_lib}/libubsan.so.0*
%ifarch x86_64 aarch64
%{_prefix}/%{_lib}/libtsan.so.0*
%{_prefix}/%{_lib}/liblsan.so.0*
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif # build_libsanitizer

%if %{build_libcilkrts}
%files -n libcilkrts
%{_prefix}/%{_lib}/libcilkrts.so.5*
%doc rpm.doc/changelogs/libcilkrts/ChangeLog* libcilkrts/README
%endif # build_libcilkrts

%if %{build_libmpx}
%files -n libmpx
%{_prefix}/%{_lib}/libmpx.so.2*
%{_prefix}/%{_lib}/libmpxwrappers.so.2*
%doc rpm.doc/changelogs/libmpx/ChangeLog*
%endif # build_libmpx

%if %{build_go}
%files go
%defattr(-,root,root,-)
%{_prefix}/bin/go
%attr(755,root,root) %{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%{_prefix}/bin/gofmt
%attr(755,root,root) %{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgolibbegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgolibbegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%endif
%doc rpm.doc/go/*
# devel files
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_major}
%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%endif
%{_libdir}/libgo.so

%files -n libgo
%{_prefix}/%{_lib}/libgo.so.11*
%doc rpm.doc/libgo/*
%endif #build_go

%files -n libgccjit
%{_prefix}/%{_lib}/libgccjit.so.*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n libgccjit-devel
%{_prefix}/%{_lib}/libgccjit.so
%{_prefix}/include/libgccjit*.h
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples

%files plugin-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/plugin

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%changelog
* Wed Jun 24 2020 Jakub Jelinek <jakub@redhat.com> 7.3.1-9.amzn2
- use libgcc_s.so linker script also on aarch64 (#1830472)

* Thu May 21 2020 Emmanuel Lepage <emmlep@amazon.com> 7.3.1-8.amzn2
- Add -march=native support for Graviton2

* Fri May 08 2020 Emmanuel Lepage <emmlep@amazon.com> 7.3.1-7.amzn2
- Add Aarch64 LSE -moutline-atomics support
- Backport most aarch64 patches from GCC 7.3.5

* Mon Sep 23 2019 Frederick Lefebvre <fredlef@amazon.com> 7.3.1-6.amzn2.0.4
- Default falign-jumps, falign-loops and falign-functions to "32:16" for aarch64 instances

* Fri Sep 06 2019 Frederick Lefebvre <fredlef@amazon.com> 7.3.1-6.amzn2.0.3
- Backport support for specifying maxskip for each falign_ parameters
  pr84100, middle-end/66240, target/45996, c/84100

* Fri Jul 12 2019 Frederick Lefebvre <fredlef@amazon.com> 7.3.1-6.amzn2.0.1
- Add missing arch specific provides for devel packages we folder into gcc
- Rebuild with aarch64 gcc with "-falign-jumps=32 -falign-loops=32 -falign-functions=32"
- Default falign-jumps, falign-loops and falign-functions to 32

* Thu Jul 12 2018 Jakub Jelinek <jakub@redhat.com> 7.3.1-6
- update from the 7 branch
  - PRs ada/82813, c++/64095, c++/71638, c++/71834, c++/78489, c++/79085,
	c++/80227, c++/80290, c++/80598, c++/82152, c++/82336, c++/84076,
	c++/84222, c++/84355, c++/84463, c++/84662, c++/84665, c++/84684,
	c++/84686, c++/84767, c++/84783, c++/84791, c++/84798, c++/84839,
	c++/84854, c++/84874, c++/84927, c++/84937, c++/84961, c++/85006,
	c++/85060, c++/85068, c++/85076, c++/85113, c++/85118, c++/85140,
	c++/85147, c++/85148, c++/85208, c++/85210, c++/85279, c++/85464,
	c++/85470, c++/85646, c++/85659, c++/85662, c++/85815, c++/85952,
	c++/86025, c++/86060, c++/86210, c++/86291, c++/86378, c/84229,
	c/84310, c/84853, c/84873, c/84953, c/84999, c/85696, debug/84875,
	debug/85252, fortran/38351, fortran/44491, fortran/51434,
	fortran/56667, fortran/63514, fortran/64124, fortran/65453,
	fortran/66694, fortran/68846, fortran/70409, fortran/70864,
	fortran/70870, fortran/71085, fortran/77414, fortran/78278,
	fortran/78741, fortran/78990, fortran/80657, fortran/80965,
	fortran/81773, fortran/82275, fortran/82617, fortran/82814,
	fortran/82923, fortran/82969, fortran/82972, fortran/83076,
	fortran/83088, fortran/83118, fortran/83149, fortran/83319,
	fortran/83606, fortran/83898, fortran/83939, fortran/84546,
	fortran/84734, fortran/84931, fortran/85001, fortran/85084,
	fortran/85138, fortran/85313, fortran/85507, fortran/85520,
	fortran/85521, fortran/85542, fortran/85543, fortran/85641,
	fortran/85687, fortran/85779, fortran/85780, fortran/85851,
	fortran/85895, fortran/85981, fortran/85996, fortran/86045,
	fortran/86051, fortran/86059, fortran/86110, fortran/86242,
	gcov-profile/83879, gcov-profile/84137, hsa/86371, inline-asm/84941,
	inline-asm/85022, inline-asm/85034, inline-asm/85172, ipa/81360,
	ipa/84658, ipa/84963, ipa/85655, jit/85384, libgfortran/85840,
	libgfortran/86070, libstdc++/67554, libstdc++/68397, libstdc++/77691,
	libstdc++/80506, libstdc++/82966, libstdc++/83662, libstdc++/83982,
	libstdc++/84087, libstdc++/84769, libstdc++/84773, libstdc++/85098,
	libstdc++/85222, libstdc++/85442, libstdc++/85632, libstdc++/85671,
	libstdc++/85812, libstdc++/86127, libstdc++/86138, libstdc++/86169,
	libstdc++/86272, libstdc++/pr66689, lto/81004, lto/81440, lto/83954,
	lto/85248, lto/85405, middle-end/82063, middle-end/84607,
	middle-end/84834, middle-end/84955, middle-end/85244,
	middle-end/85496, middle-end/85567, middle-end/85588,
	middle-end/85878, rtl-optimization/82675, rtl-optimization/84878,
	rtl-optimization/85167, rtl-optimization/85300,
	rtl-optimization/85431, sanitizer/78651, sanitizer/84761,
	sanitizer/85018, sanitizer/85081, sanitizer/85389, sanitizer/85835,
	sanitizer/86012, target/63177, target/79747, target/80546,
	target/81143, target/81572, target/81647, target/82411, target/82518,
	target/82989, target/83451, target/83660, target/83789, target/83969,
	target/83984, target/84209, target/84371, target/84574, target/84700,
	target/84748, target/84772, target/84786, target/84826, target/84827,
	target/84860, target/84899, target/84912, target/84990, target/85026,
	target/85056, target/85095, target/85100, target/85193, target/85196,
	target/85203, target/85261, target/85424, target/85430, target/85436,
	target/85698, target/85755, target/85903, target/85904, target/85945,
	target/86314, testsuite/79455, testsuite/80551,
	tree-optimization/84485, tree-optimization/84486,
	tree-optimization/84739, tree-optimization/84841,
	tree-optimization/84956, tree-optimization/85168,
	tree-optimization/85257, tree-optimization/85284,
	tree-optimization/85446, tree-optimization/85529,
	tree-optimization/85597, tree-optimization/85712,
	tree-optimization/85989, tree-optimization/86231, web/85578
  - fix ICE with alias template and default targs (#1598912, PR c++/84785)

* Mon Jun  4 2018 Frederick Lefebvre <fredlef@amazon.com 7.3.1-5.amzn2.0.1
- Add back multilib support

* Sat Mar  3 2018 Jakub Jelinek <jakub@redhat.com> 7.3.1-5
- update from the 7 branch
  - PRs ada/84277, bootstrap/80867, bootstrap/82916, bootstrap/84017,
	c++/71569, c++/71784, c++/81589, c++/81853, c++/81860, c++/82664,
	c++/82764, c++/83227, c++/83659, c++/83817, c++/83824, c++/83835,
	c++/83958, c++/83990, c++/83993, c++/84015, c++/84031, c++/84045,
	c++/84082, c++/84151, c++/84192, c++/84341, c++/84420, c++/84430,
	c++/84441, c++/84444, c++/84445, c++/84448, c++/84449, c++/84489,
	c++/84496, c++/84520, c++/84556, c++/84557, c++/84558, c/82210,
	fortran/30792, fortran/35299, fortran/54223, fortran/68560,
	fortran/78238, fortran/81116, fortran/82007, fortran/82049,
	fortran/82994, fortran/83633, fortran/84116, fortran/84270,
	fortran/84276, fortran/84346, fortran/84418, fortran/84495,
	fortran/84506, fortran/84511, inline-asm/84625, ipa/84425, ipa/84628,
	libgfortran/84412, libgomp/84096, libstdc++/81797, libstdc++/84532,
	libstdc++/84671, middle-end/83945, middle-end/83977, middle-end/84040,
	preprocessor/69869, preprocessor/83722, rtl-optimization/83496,
	rtl-optimization/83986, rtl-optimization/84071,
	rtl-optimization/84123, rtl-optimization/84308, sanitizer/70875,
	sanitizer/83987, sanitizer/84285, target/56010, target/79242,
	target/79975, target/81228, target/82096, target/83370, target/83743,
	target/83758, target/83790, target/83930, target/84039, target/84089,
	target/84113, target/84154, target/84279, target/84388, target/84390,
	target/84530, target/PR84295, tree-optimization/81661,
	tree-optimization/82795, tree-optimization/83605,
	tree-optimization/84117, tree-optimization/84190,
	tree-optimization/84233, tree-optimization/84503
- fix AVX512BW wrong-code bug (PR target/84524)
- fix go provides/requires (#1545071)

* Mon Feb  5 2018 Richard W.M. Jones <rjones@redhat.com> 7.3.1-4
- disable multilib on riscv64

* Thu Feb  1 2018 Jeff Law <law@redhat.com> 7.3.1-3
- fix -fstack-clash-protection codegen issue on 32 bit x86
  (#1540221, PR target/84128)

* Tue Jan 30 2018 Jakub Jelinek <jakub@redhat.com> 7.3.1-2
- update from the 7 branch
  - PRs c++/82461, c++/82878, libstdc++/81076, libstdc++/83658,
	libstdc++/83830, libstdc++/83833, rtl-optimization/83985, target/68467,
	target/81763, target/83399, target/83862, target/83905, target/84033
- fix -fstack-clash-protection ICE with -mtune=i686 (#1538648, PR target/84064)

* Thu Jan 25 2018 Jakub Jelinek <jakub@redhat.com> 7.3.1-1
- update from the 7 branch
  - 7.3 release
  - PRs c++/81843, c++/82331, c++/82760, fortran/80768, fortran/83864,
	fortran/83874, fortran/83900, ipa/82352, ipa/83549, libstdc++/83834,
	middle-end/81782, rtl-optimization/81443, target/80870, target/83687,
	target/83946, tree-optimization/81877, tree-optimization/83552

* Wed Jan 24 2018 Jeff Law <law@redhat.com> 7.2.1-8
- fix -fstack-clash-protection codegen issue on 32 bit x86 (#1536555)

* Wed Jan 17 2018 Jakub Jelinek <jakub@redhat.com> 7.2.1-7
- update from the 7 branch
  - PRs fortran/78814, fortran/82367, fortran/82841, fortran/83093,
	fortran/83679, libgfortran/83811, libstdc++/79283, libstdc++/83279,
	libstdc++/83598, libstdc++/83600, libstdc++/83626, middle-end/83713,
	preprocessor/83492, rtl-optimization/83424, rtl-optimization/83565,
	target/81481, target/81819, target/81821, target/82975, target/83330,
	target/83628, target/83629, target/83677, target/83839,
	testsuite/77734
  - x86 retpoline support
- comment out gcc-debuginfo/gcc-base-debuginfo splitting hacks for f27 and
  later (#1517259)

* Thu Jan  4 2018 Jakub Jelinek <jakub@redhat.com> 7.2.1-6
- update from the 7 branch
  - PRs c++/83556, fortran/83650, libgfortran/83649
- backport fixes for two -fstack-clash-protection bugs from the trunk
  (PRs middle-end/83654, target/83641)
- commit -fstack-clash-protection patches except aarch64 to
  redhat/gcc-7-branch instead of applying them as patches in the spec file

* Mon Jan  1 2018 Jakub Jelinek <jakub@redhat.com> 7.2.1-5
- update from the 7 branch
  - PRs ada/82393, bootstrap/83439, c++/70029, c++/79650, c++/80259,
	c++/80767, c++/80935, c++/81197, c++/81212, c++/81236, c++/81525,
	c++/81671, c++/81675, c++/81702, c++/81888, c++/82030, c++/82085,
	c++/82159, c++/82299, c++/82373, c++/82406, c++/82560, c++/82781,
	c++/83059, c++/83116, c++/83205, c++/83217, c++/83553, c/81875,
	c/82234, c/82340, c/83448, debug/83084, driver/81829, fortran/52832,
	fortran/67543, fortran/69739, fortran/78152, fortran/78512,
	fortran/78619, fortran/78641, fortran/78686, fortran/79072,
	fortran/79795, fortran/80118, fortran/80120, fortran/80554,
	fortran/80850, fortran/81048, fortran/81304, fortran/81735,
	fortran/81758, fortran/81841, fortran/81903, fortran/82121,
	fortran/82312, fortran/82796, fortran/82934, fortran/83021,
	fortran/83191, fortran/83436, fortran/83548, gcov-profile/82457,
	gcov-profile/82633, go/80914, ipa/82801, ipa/82808, ipa/83346,
	libfortran/82233, libgcc/82635, libgfortran/78387, libgfortran/78549,
	libgfortran/81937, libgfortran/81938, libgfortran/83168,
	libgfortran/83191, libgfortran/83225, libgfortran/83613,
	libstdc++/59568, libstdc++/79433, libstdc++/81395, libstdc++/82254,
	libstdc++/82262, libstdc++/82481, libstdc++/82522, libstdc++/82685,
	libstdc++/83134, libstdc++/83226, libstdc++/83395, libstdc++/83427,
	lto/82027, middle-end/60580, middle-end/80295, middle-end/82128,
	middle-end/82253, middle-end/82556, middle-end/82765,
	middle-end/83471, middle-end/83608, middle-end/83609,
	middle-end/83623, rtl-optimization/64682, rtl-optimization/69567,
	rtl-optimization/69737, rtl-optimization/80747,
	rtl-optimization/81553, rtl-optimization/81803,
	rtl-optimization/82044, rtl-optimization/82192,
	rtl-optimization/82602, rtl-optimization/82621,
	rtl-optimization/82683, rtl-optimization/83512, sanitizer/81715,
	sanitizer/82379, sanitizer/82545, sanitizer/82595, sanitizer/82792,
	sanitizer/82869, sanitizer/83014, target/39570, target/66488,
	target/71727, target/71951, target/77480, target/77687, target/78643,
	target/80583, target/80600, target/80819, target/81288, target/81906,
	target/81959, target/81996, target/82274, target/82445, target/82524,
	target/82703, target/82717, target/82772, target/82880, target/82941,
	target/82942, target/82990, target/83111, target/83387, target/83467,
	tree-optimization/80631, tree-optimization/81790,
	tree-optimization/82042, tree-optimization/82060,
	tree-optimization/82084, tree-optimization/82102,
	tree-optimization/82108, tree-optimization/82244,
	tree-optimization/82276, tree-optimization/82285,
	tree-optimization/82291, tree-optimization/82337,
	tree-optimization/82402, tree-optimization/82436,
	tree-optimization/82549, tree-optimization/82603,
	tree-optimization/82697, tree-optimization/82726,
	tree-optimization/82902, tree-optimization/82985,
	tree-optimization/83198, tree-optimization/83269,
	tree-optimization/83521, tree-optimization/83523
  - fix debuginfo for forward declared C structs (#1500862, PR debug/83550)
  - fix sccvn ICE (#1506809, PR tree-optimization/82264)
  - fix ICE in dwarf2out force_type_die (#1516576, #1516577, PR debug/82155)
  - fix power6 ICE in store_data_bypass_p (#1522675, PR target/80101)
- fix replace_placeholders (PR c++/83556)

* Wed Nov 29 2017 Jeff Law <law@redhat.com> 7.2.1-4
- fix problem with large outgoing args and -fstack-clash-protection
  on aarch64 (#1518823)

* Tue Nov 28 2017 Jeff Law <law@redhat.com> 7.2.1-3
- backport -fstack-clash-protection from development trunk (#1512529)

* Fri Sep 15 2017 Jakub Jelinek <jakub@redhat.com> 7.2.1-2
- update from the 7 branch
  - PRs ada/62235, ada/79441, ada/79542, bootstrap/81926, c++/81355,
	c++/81852, c++/82039, c++/82040, c/45784, c/81687, driver/81650,
	fortran/81770, inline-asm/82001, ipa/81128, libstdc++/70483,
	libstdc++/81338, libstdc++/81468, libstdc++/81599, libstdc++/81835,
	libstdc++/81891, libstdc++/81912, middle-end/81052, middle-end/81768,
	other/39851, sanitizer/63361, sanitizer/81923, target/80695,
	target/81504, target/81593, target/81621, target/81833, target/81988,
	target/82181, testsuite/82114, testsuite/82120, tree-opt/81696,
	tree-optimization/81503, tree-optimization/81987
- fix OpenMP implicit firstprivate handling of references (PR c++/81314)
- fix -fcompare-debug failures with PowerPC atomics (PR target/81325)
- fix compile time hog in C++ replace_placeholders (PR sanitizer/81929)
- fix __atomic* and PowerPC vec_ld/vec_st handling of array arguments
  (PR target/82112)

* Tue Aug 29 2017 Jakub Jelinek <jakub@redhat.com> 7.2.1-1
- update from the 7 branch
  - 7.2 release
  - PRs c++/67054, c++/81607, debug/81993, driver/81523, fortran/80164,
	fortran/81296, ipa/77732, libstdc++/53984, libstdc++/79820,
	libstdc++/81751, middle-end/81065, middle-end/81088, middle-end/81766,
	middle-end/81884, sanitizer/80932, target/67712, target/72804,
	target/78460, target/80210, target/81170, target/81295, target/81861,
	target/81894, target/81910, target/81921, testsuite/81056,
	tree-optimization/81181, tree-optimization/81354,
	tree-optimization/81723, tree-optimization/81977

* Wed Aug  2 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-7
- update from the 7 branch
  - 7.2-rc1
  - PRs c++/71570, gcov-profile/81561, libgcc/61152, libquadmath/65757,
	libstdc++/80553, libstdc++/80721, libstdc++/80737, libstdc++/80939,
	libstdc++/81017, lto/81487, middle-end/79499, middle-end/81505,
	rtl-optimization/75964, sanitize/81186, sanitizer/81021,
	sanitizer/81224, sanitizer/81302, sanitizer/81604, target/79041,
	target/80569, target/81069, target/81175, target/81193, target/81407,
	target/81414, target/81471, target/81473, target/81534, target/81622,
	target/81641, tree-optimization/71752, tree-optimization/80769,
	tree-optimization/81162, tree-optimization/81388,
	tree-optimization/81410, tree-optimization/81455,
	tree-optimization/81555, tree-optimization/81556,
	tree-optimization/81588, tree-optimization/81633,
	tree-optimization/81655

* Tue Jul 18 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-6
- update from the 7 branch
  - PRs ada/81446, c++/81258, middle-end/80929, rtl-optimization/81424,
	target/79883, target/81225, tree-optimization/81365,
	tree-optimization/81428
- fix bootstrap on s390{,x} in libgo (PR go/81393)
- rebuilt against hopefully fixed glibc to reenable TLS support on ppc64le
  in libstdc++ (#1470692)

* Tue Jul 11 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-5
- update from the 7 branch
  - PRs libstdc++/80316, target/81375
- fix libsanitizer build against recent glibc (PR sanitizer/81066)

* Sun Jul  9 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-4
- update from the 7 branch
  - PRs c++/54769, c++/61022, c++/72801, c++/79056, c++/81164, c++/81180,
	c++/81187, c++/81188, c++/81204, c++/81215, c++/81257, driver/31468,
	driver/56469, gcov-profile/53915, gcov-profile/81080, ipa/79849,
	ipa/79850, ipa/80663, ipa/81112, libfortran/81195, libgfortran/53029,
	libstdc++/81221, middle-end/80692, middle-end/80902, middle-end/81007,
	middle-end/81207, other/80589, other/80909, sanitizer/80879,
	sanitizer/81209, target/79155, target/79799, target/80618,
	target/80966, target/81294, target/81300, target/81305, target/81348,
	tree-optimization/80612, tree-optimization/81083,
	tree-optimization/81192
- fix ppc* float128 ifunc (#1467526)

* Thu Jun 22 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-3
- update from the 7 branch
  - PRs ada/80921, ada/81070, ada/81105, c++/60063, c++/66297, c++/70844,
	c++/71747, c++/80179, c++/80384, c++/80465, c++/80562, c++/80593,
	c++/80605, c++/80614, c++/80639, c++/80829, c++/80831, c++/80840,
	c++/80856, c++/80972, c++/80973, c++/80984, c++/81011, c++/81045,
	c++/81073, c++/81074, c++/81102, c++/81130, c++/81154, c/80919,
	c/81006, fortran/70601, fortran/80766, fortran/80904, fortran/80918,
	fortran/80975, libgcc/80037, libgomp/80822, libstdc++/80675,
	libstdc++/80940, libstdc++/81002, libstdc++/81092,
	rtl-optimization/80474, rtl-optimization/80903, sanitizer/81111,
	sanitizer/81125, target/59874, target/71607, target/71778,
	target/80718, target/80968, target/80970, target/81015, target/81121,
	target/81151, tree-optimization/80293, tree-optimization/80549,
	tree-optimization/80705, tree-optimization/80842,
	tree-optimization/80906

* Fri May 26 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-2
- update from the 7 branch
  - PRs ada/80626, ada/80784, documentation/50642, fortran/78659,
	fortran/80121, fortran/80333, fortran/80392, fortran/80484,
	fortran/80741, fortran/80752, go/64238, libgfortran/80333,
	libgfortran/80727, libgfortran/80741, libstdc++/78939, libstdc++/80478,
	libstdc++/80761, libstdc++/80796, middle-end/80539, middle-end/80809,
	middle-end/80853, rtl-optimization/80754, sanitizer/80659,
	sanitizer/80875, target/68163, target/79027, target/79202,
	target/79203, target/80090, target/80510, target/80671, target/80706,
	target/80799, tree-optimization/80453, tree-optimization/80492
- fix s390 indirect_jump reloading (#1450353, PR target/80725)

* Wed May  3 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-1
- update from the 7 branch
  - GCC 7.1 release
  - PRs bootstrap/80531, c++/80534, c/80468, target/68491, target/79430,
	target/80530, tree-optimization/80591

* Tue Apr 25 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.16
- update from the 7 branch
  - ABI change on ARM and AArch64 (PR target/77728)
  - PRs middle-end/79931, rtl-optimization/80500, rtl-optimization/80501,
	target/79895, target/80080, target/80464, target/80482,
	tree-optimization/80497

* Fri Apr 21 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.15
- update from the trunk and 7 branch
  - PRs bootstrap/77661, c++/80176, c++/80241, c++/80244, c++/80287,
	c++/80294, c++/80363, c++/80370, c++/80415, c++/80459, c++/80473,
	c/80163, debug/80263, debug/80436, debug/80461, fortran/80046,
	fortran/80361, fortran/80440, gcov-profile/78783, gcov-profile/80413,
	gcov-profile/80435, ipa/65972, libgomp/80394, libstdc++/80446,
	libstdc++/80448, lto/50345, lto/69953, middle-end/79671,
	middle-end/79788, middle-end/80100, middle-end/80364,
	middle-end/80375, middle-end/80422, middle-end/80423,
	rtl-optimization/80343, rtl-optimization/80357,
	rtl-optimization/80385, rtl-optimization/80429, sanitizer/70878,
	sanitizer/80349, sanitizer/80403, sanitizer/80404, sanitizer/80405,
	sanitizer/80414, sanitizer/80444, target/74563, target/79453,
	target/80057, target/80098, target/80099, target/80108, target/80315,
	target/80376, target/80381, target/80382, target/80389, target/80462,
	testsuite/79867, testsuite/80221, testsuite/80416,
	tree-optimization/80153, tree-optimization/80359,
	tree-optimization/80374, tree-optimization/80426,
	tree-optimization/80443
- reenable {gcc,libgomp}-offload-nvptx on ppc64le

* Mon Apr 10 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.14
- update from the trunk
  - PRs ada/80117, ada/80146, c++/60992, c++/69487, c++/79572, c++/80095,
	c++/80267, c++/80296, c++/80297, c++/80309, c++/80356, c/79730,
	debug/79255, debug/80025, debug/80234, documentation/78732,
	fortran/78661, fortran/80254, gcov-profile/80224, go/80226, ipa/77333,
	ipa/79776, ipa/80104, ipa/80205, ipa/80212, libgfortran/78670,
	libgomp/79876, libstdc++/79141, libstdc++/80137, libstdc++/80229,
	libstdc++/80251, middle-end/80162, middle-end/80163, middle-end/80173,
	middle-end/80222, middle-end/80281, middle-end/80341,
	middle-end/80344, middle-end/80362, rtl-optimization/60818,
	rtl-optimization/70478, rtl-optimization/70703,
	rtl-optimization/79405, rtl-optimization/80193,
	rtl-optimization/80233, sanitizer/79993, sanitizer/80067,
	sanitizer/80166, sanitizer/80308, sanitizer/80348, sanitizer/80350,
	target/45053, target/53383, target/78002, target/78543, target/79733,
	target/79889, target/79890, target/79905, target/80102, target/80103,
	target/80107, target/80206, target/80246, target/80250, target/80286,
	target/80298, target/80307, target/80310, target/80322, target/80323,
	target/80324, target/80325, target/80326, target/80358,
	testsuite/43496, translation/80189, tree-optimization/49498,
	tree-optimization/77498, tree-optimization/78644,
	tree-optimization/79390, tree-optimization/80181,
	tree-optimization/80216, tree-optimization/80218,
	tree-optimization/80262, tree-optimization/80275,
	tree-optimization/80304, tree-optimization/80334
- fix dwarf ICE with nested function self-inlining (PR debug/80321)

* Mon Mar 27 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.13
- update from the trunk
  - PRs bootstrap/79771, bootstrap/79952, c++/35878, c++/52477, c++/77339,
	c++/77563, c++/77752, c++/78345, c++/79393, c++/79519, c++/79548,
	c++/79640, c++/79687, c++/79896, c++/79899, c++/79960, c++/79962,
	c++/79967, c++/79984, c++/80029, c++/80043, c++/80059, c++/80073,
	c++/80077, c++/80084, c++/80096, c++/80119, c++/80129, c++/80141,
	c++/80150, c/67338, c/78165, c/79921, c/79936, c/80097, driver/79875,
	fortran/33271, fortran/39239, fortran/69498, fortran/71838,
	fortran/79602, fortran/79676, fortran/79838, fortran/79844,
	fortran/79853, fortran/79859, fortran/79860, fortran/79886,
	fortran/80010, fortran/80011, fortran/80142, fortran/80156,
	gcov-profile/80081, libfortran/79956, libgfortran/78854,
	libgfortran/78881, libstdc++/62045, libstdc++/67440, libstdc++/79162,
	libstdc++/79511, libstdc++/79980, libstdc++/80034, libstdc++/80041,
	libstdc++/80064, libstdc++/80183, middle-end/78339, middle-end/79753,
	middle-end/79831, middle-end/80020, middle-end/80050,
	middle-end/80075, middle-end/80171, other/79991, plugins/80094,
	rtl-optimization/63191, rtl-optimization/78911,
	rtl-optimization/79150, rtl-optimization/79728,
	rtl-optimization/79909, rtl-optimization/79910,
	rtl-optimization/80112, rtl-optimization/80159,
	rtl-optimization/80160, sanitizer/78158, sanitizer/79757,
	sanitizer/80063, sanitizer/80110, sanitizer/80168, target/71294,
	target/71436, target/78857, target/79769, target/79770, target/79892,
	target/79893, target/79906, target/79907, target/79911, target/79912,
	target/79925, target/79941, target/79947, target/79951, target/79963,
	target/80017, target/80019, target/80052, target/80082, target/80083,
	target/80123, target/80125, target/80148, target/80180,
	testsuite/79356, testsuite/80092, translation/79848,
	translation/79923, translation/80001, tree-optimization/71437,
	tree-optimization/77975, tree-optimization/79800,
	tree-optimization/79908, tree-optimization/79981,
	tree-optimization/80030, tree-optimization/80032,
	tree-optimization/80048, tree-optimization/80054,
	tree-optimization/80072, tree-optimization/80079,
	tree-optimization/80109, tree-optimization/80113,
	tree-optimization/80122, tree-optimization/80136,
	tree-optimization/80158, tree-optimization/80167,
	tree-optimization/80170

* Thu Mar  9 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.12
- update from the trunk
  - PRs c++/71966, c++/79672, c++/79797, c++/79900, ipa/79761, ipa/79764,
	ipa/79970, middle-end/79971, rtl-optimization/79949, target/65705,
	target/69804, target/79913, target/79928, tree-optimization/79631,
	tree-optimization/79977
- fix DW_AT_decl_line on DW_TAG_enumeration_type for C enumeration
  definitions following forward declarations (#1423460, PR c/79969)
- fix ICE with -Walloca (PR tree-optimization/79972)

* Wed Mar  8 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.11
- update from the trunk
  - PRs ada/79903, ada/79945, c++/42000, c++/64574, c++/70266, c++/71568,
	c++/79414, c++/79681, c++/79746, c++/79782, c++/79791, c++/79796,
	c++/79821, c++/79822, c++/79825, c/79756, c/79758, c/79834, c/79836,
	c/79837, c/79847, c/79855, c/79940, demangler/67264, demangler/70909,
	fortran/51119, fortran/78379, fortran/79739, fortran/79841,
	fortran/79894, libstdc++/79789, libstdc++/79798, lto/78140, lto/79625,
	lto/79760, middle-end/68270, middle-end/79692, middle-end/79721,
	middle-end/79731, middle-end/79805, middle-end/79809,
	middle-end/79818, rtl-optimization/79571, rtl-optimization/79584,
	rtl-optimization/79780, rtl-optimization/79901, sanitize/79783,
	sanitizer/79897, sanitizer/79904, target/43763, target/68739,
	target/79395, target/79439, target/79514, target/79544, target/79729,
	target/79742, target/79749, target/79752, target/79793, target/79807,
	target/79812, tree-optimization/45397, tree-optimization/66768,
	tree-optimization/77536, tree-optimization/79345,
	tree-optimization/79690, tree-optimization/79691,
	tree-optimization/79699, tree-optimization/79723,
	tree-optimization/79732, tree-optimization/79734,
	tree-optimization/79737, tree-optimization/79740,
	tree-optimization/79777, tree-optimization/79803,
	tree-optimization/79824, tree-optimization/79894,
	tree-optimization/79920, tree-optimization/79943,
	tree-optimization/79955
- fix 64 avx512vl and 6 avx512bw intrinsics that were not available with -O0
  (PR target/79932)
- temporarily disable incorrect folding of Altivec vmul[oe]u[bh] intrinsics
  (#1429961, PR middle-end/79941)
- fix -fsanitize=address with some atomic/sync builtins (PR sanitizer/79944)

* Sat Feb 25 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.10
- update from the trunk
  - PRs c++/17729, c++/41727, c++/50308, c++/69523, c++/78139, c++/78282,
	c++/79361, c++/79380, c++/79400, c++/79470, c++/79500, c++/79503,
	c++/79535, c++/79566, c++/79580, c++/79588, c++/79606, c++/79607,
	c++/79639, c++/79641, c++/79653, c++/79654, c++/79655, c++/79657,
	c++/79664, c++/79679, c/79662, c/79677, c/79684, debug/77589,
	fortran/79229, fortran/79382, fortran/79402, fortran/79434,
	fortran/79447, fortran/79523, fortran/79597, fortran/79599,
	fortran/79601, go/79642, lto/79579, lto/79587, middle-end/79396,
	middle-end/79537, middle-end/79665, rtl-optimization/68749,
	rtl-optimization/79286, sanitizer/79558, sanitizer/79589,
	target/71017, target/78012, target/78056, target/78660, target/79211,
	target/79473, target/79494, target/79568, target/79570, target/79593,
	target/79633, translation/79638, translation/79705,
	tree-optimization/61441, tree-optimization/68644,
	tree-optimization/79389, tree-optimization/79578,
	tree-optimization/79621, tree-optimization/79649,
	tree-optimization/79663, tree-optimization/79666,
	tree-optimization/79673, tree-optimization/79683

* Sun Feb 19 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.9
- update from the trunk
  - PRs bootstrap/79567, c++/77659, c++/77790, c++/78572, c++/78690,
	c++/79050, c++/79296, c++/79301, c++/79363, c++/79420, c++/79461,
	c++/79463, c++/79464, c++/79502, c++/79508, c++/79512, c++/79533,
	c++/79549, c++/79556, c/79471, c/79478, c/79515, fortran/65542,
	ipa/79224, libstdc++/78723, libstdc++/79348, libstdc++/79467,
	libstdc++/79486, libstdc++/79513, middle-end/61225, middle-end/79432,
	middle-end/79448, middle-end/79496, middle-end/79505,
	middle-end/79521, middle-end/79536, middle-end/79576,
	rtl-optimization/78127, rtl-optimization/79286,
	rtl-optimization/79541, rtl-optimization/79574,
	rtl-optimization/79577, sanitizer/79562, target/79261, target/79282,
	target/79404, target/79421, target/79449, target/79462, target/79481,
	target/79487, target/79495, target/79498, target/79559, target/79569,
	tree-optimization/79095, tree-optimization/79347,
	tree-optimization/79529, tree-optimization/79552, tree-ssa/56727

* Sat Feb 11 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.8
- update from the trunk
  - PRs c++/71285, c++/78897, c++/78908, c++/79143, c++/79184, c++/79316,
	c++/79350, c++/79401, c++/79435, c++/79457, ipa/70795,
	middle-end/79454, target/79295, tree-optimization/66612,
	tree-optimization/79411
- fix combiner get_last_value handling (PRs rtl-optimization/79388,
  rtl-optimization/79450)

* Thu Feb  9 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.7
- update from the trunk
  - PRs c++/70448, c++/71193, c++/79360, c++/79372, c++/79377, c++/79379,
	c++/79429, c/79413, c/79428, c/79431, fortran/78958, fortran/79230,
	fortran/79335, fortran/79344, ipa/79375, libstdc++/79323,
	middle-end/79278, middle-end/79399, rtl-optimization/68664,
	rtl-optimization/79386, target/66144, target/68972, target/78604,
	target/78883, target/79299, target/79353, translation/79397,
	tree-optimization/69823, tree-optimization/78348,
	tree-optimization/79284, tree-optimization/79376,
	tree-optimization/79408, tree-optimization/79409, tree-ssa/79347
- fix addition of OFFLOAD_TARGET_DEFAULT env var in gcc driver
- use isl 0.16.1 instead of 0.14
- fix s390x libasan __tls_get_offset interception (PR sanitizer/79341)
- list fixed RHEL{6,7} kernels in CVE-2016-2143 s390x libsanitizer whitelist

* Sat Feb  4 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.6
- update from the trunk
  - PRs ada/79309, c++/12245, c++/69637, c++/78689, c++/79294, cp/14179,
	ipa/79337, libstdc++/60936, libstdc++/78346, lto/66295,
	middle-end/32003, middle-end/78142, middle-end/78468,
	middle-end/79275, sanitizer/78663, target/70012, target/78862,
	target/79158, target/79354, testsuite/76957, testsuite/79272,
	testsuite/79324, tree-optimization/79327, tree-optimization/79338,
	tree-optimization/79339, tree-optimization/79340,
	tree-optimization/79352
- default to -march=zEC12 -mtune=z13 on s390x (#1404991)

* Wed Feb  1 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.5
- update from the trunk
  - PRs c++/67273, c++/79253, c++/79264, c++/79290, c++/79298, c++/79304,
	fortran/79305, ipa/79285, middle-end/79315, preprocessor/79210,
	target/78597, target/79038, tree-optimization/71691,
	tree-optimization/71824, tree-optimization/77318

* Tue Jan 31 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.4
- update from the trunk
  - PRs bootstrap/78985, debug/63238, debug/79289, gcov-profile/79259,
	target/78945, target/79170, target/79240, target/79260, target/79268,
	testsuite/70583, testsuite/79293, tree-optimization/79256,
	tree-optimization/79267, tree-optimization/79276
- fix ICEs with powerpc conversion of float/double to 64-bit unsigned integer
  (PR target/79197)
- fix C++ ICE with comma expression on lhs of assignment (PR c++/79232)
- fix default TLS model for C++ non-inline static data members (PR c++/79288)
- libcp1plugin.so added to gcc-gdb-plugin for C++ support

* Sat Jan 28 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.3
- update from the trunk
  - PRs c++/64382, c++/68727, c++/78771, c++/79176, debug/78835, debug/79129,
	libstdc++/79190, libstdc++/79243, libstdc++/79254,
	rtl-optimization/78559, rtl-optimization/79194, target/65484,
	target/79131, target/79239, tree-optimization/71374,
	tree-optimization/79244, tree-optimization/79245

* Thu Jan 26 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.2
- update from the trunk
  - PRs bootstrap/79132, bootstrap/79198, c++/71290, c++/71406, c++/71710,
	c++/77508, c++/77914, c++/78469, c++/78896, c++/79118, c++/79205,
	c/79199, debug/78363, fortran/79154, ipa/79108, libstdc++/61791,
	libstdc++/70607, libstdc++/79195, libstdc++/79206, middle-end/78703,
	middle-end/79123, middle-end/79212, middle-end/79236,
	rtl-optimization/71724, rtl-optimization/78634,
	rtl-optimization/79125, sanitizer/79168, target/61729, target/66669,
	target/70465, target/77439, target/77850, target/79145, target/79179,
	testsuite/72850, testsuite/78421, testsuite/79169, translation/79208,
	tree-optimization/69264, tree-optimization/70754,
	tree-optimization/78384, tree-optimization/79088,
	tree-optimization/79159, tree-optimization/79186,
	tree-optimization/79188, tree-optimization/79196
- temporarily disable {gcc,libgomp}-offload-nvptx on ppc64le, further
  debugging there is needed
- enable libasan and libubsan on s390x and libtsan and liblsan on
  ppc64{,le}

* Fri Jan 20 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.1
- update from the trunk
  - PRs c++/77829, c++/78495, c++/78656, c++/79495, c/64279, c/79152,
	libstdc++/69240, target/71270

* Fri Jan 20 2017 Jakub Jelinek <jakub@redhat.com> 7.0.0-0.3
- update from the trunk
  - PRs ada/67205, bootstrap/78616, bootstrap/79052, bootstrap/79069,
	c++/24511, c++/61636, c++/68666, c++/70182, c++/70565, c++/71166,
	c++/71497, c++/71537, c++/71737, c++/72813, c++/77489, c++/77812,
	c++/78337, c++/78341, c++/78488, c++/78894, c++/79091, c++/79130,
	c/47931, c/78304, c/78768, c/79074, c/79089, c/79116, debug/71669,
	debug/78839, driver/49726, driver/78877, fortran/50069, fortran/55086,
	fortran/70696, fortran/70697, ipa/71190, ipa/71207, ipa/79043,
	libobjc/78697, libobjc/78698, libstdc++/64903, libstdc++/65411,
	libstdc++/66145, libstdc++/66284, libstdc++/67085, libstdc++/68925,
	libstdc++/69301, libstdc++/69321, libstdc++/69699, libstdc++/72792,
	libstdc++/72793, libstdc++/77528, libstdc++/78134, libstdc++/78273,
	libstdc++/78361, libstdc++/78389, libstdc++/78702, libstdc++/78905,
	libstdc++/78979, libstdc++/79075, libstdc++/79114, libstdc++/79156,
	lto/69188, lto/78407, lto/79042, lto/79061, middle-end/77445,
	middle-end/78411, other/79046, rtl-optimization/78626,
	rtl-optimization/78727, rtl-optimization/78751,
	rtl-optimization/78952, rtl-optimization/79032,
	rtl-optimization/79121, sanitizer/78887, target/72749, target/76731,
	target/77416, target/78176, target/78253, target/78478, target/78516,
	target/78633, target/78875, target/79004, target/79040, target/79044,
	target/79058, target/79066, target/79079, target/79080, target/79098,
	target/79127, target/79140, target/79144, testsuite/52563,
	testsuite/71237, testsuite/77737, testsuite/79051, testsuite/79073,
	testsuite/79115, tree-optimization/33562, tree-optimization/61912,
	tree-optimization/71264, tree-optimization/71433,
	tree-optimization/71854, tree-optimization/72488,
	tree-optimization/77283, tree-optimization/77485,
	tree-optimization/78319, tree-optimization/78608,
	tree-optimization/79090
- add gcc-offload-nvptx and libgomp-offload-nvptx packages for offloading
  to NVPTX on x86_64 or ppc64le

* Thu Jan 12 2017 Jakub Jelinek <jakub@redhat.com> 7.0.0-0.2
- new package
