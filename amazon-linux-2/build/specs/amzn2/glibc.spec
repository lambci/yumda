%define glibcsrcdir glibc-2.26-193-ga0bc5dd3be
%define glibcversion 2.26
%define glibcrelease 35%{?dist}
# Pre-release tarballs are pulled in from git using a command that is
# effectively:
#
# git archive HEAD --format=tar --prefix=$(git describe --match 'glibc-*')/ \
#	> $(git describe --match 'glibc-*').tar
# gzip -9 $(git describe --match 'glibc-*').tar
#
# glibc_release_url is only defined when we have a release tarball.
%{lua: if string.match(rpm.expand("%glibcsrcdir"), "^glibc%-[0-9.]+$") then
  rpm.define("glibc_release_url https://ftp.gnu.org/gnu/glibc/") end}
##############################################################################
# We support hte following options:
# --with/--without,
# * testsuite - Running the testsuite.
# * benchtests - Running and building benchmark subpackage.
# * bootstrap - Bootstrapping the package.
# * werror - Build with -Werror
# * docs - Build with documentation and the required dependencies.
# * valgrind - Run smoke tests with valgrind to verify dynamic loader.
#
# You must always run the testsuite for production builds.
# Default: Always run the testsuite.
%bcond_without testsuite
# Default: Always build the benchtests.
%bcond_without benchtests
# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Enable using -Werror
%bcond_without werror
# Default: Always build documentation.
%bcond_without docs
# Default: Always run valgrind tests
%bcond_without valgrind

# Run a valgrind smoke test to ensure that the release is compatible and
# doesn't any new feature that might cause valgrind to abort.
%if %{with valgrind}
%ifarch s390 ppc64 ppc64p7 %{mips}
# There is no valgrind support for 31-bit s390, nor for MIPS.
# The valgrind test does not work on ppc64, ppc64p7 (bug 1273103).
%undefine with_valgrind
%endif
%endif
%if %{with werror}
%ifarch s390 s390x
# The s390 and s390x builds are not -Werror clean yet.  For s390, the
# latest problem may be due to questionable code in test-string.h
# (upstream bug 19261, rhbz#1283184).
%undefine with_werror
%endif
%endif
%if %{with bootstrap}
# Disable benchtests, -Werror, docs, and valgrind if we're bootstrapping
%undefine with_benchtests
%undefine with_werror
%undefine with_docs
%undefine with_valgrind
%endif
##############################################################################
# Auxiliary arches are those arches that can be built in addition
# to the core supported arches. You either install an auxarch or
# you install the base arch, not both. You would do this in order
# to provide a more optimized version of the package for your arch.
%define auxarches athlon alphaev6
##############################################################################
# Enable lock elision support for these architectures
#
# At the moment lock elision is disabled on x86_64 until there's a CPU that
# would actually benefit from enabling it.  Intel released a microcode update
# to disable HLE and RTM at boot and the Fedora kernel now applies it early
# enough that keeping lock elision enabled should be harmless, but we have
# disabled it anyway as a conservative measure.
#
# We have not yet tested enabling ppc64 or ppc64le lock elision.
#
# We have disabled elision on s390/s390 because of bug 1499260.
#
##############################################################################
# We build a special package for Xen that includes TLS support with
# no negative segment offsets for use with Xen guests. This is
# purely an optimization for increased performance on those arches.
%define xenarches i686 athlon
%ifarch %{xenarches}
%define buildxen 1
%define xenpackage 0
%else
%define buildxen 0
%define xenpackage 0
%endif
##############################################################################
# We support only 64-bit POWER with the following runtimes:
# 64-bit BE:
# - Power 620 / 970 ISA (default runtime, compatile with POWER4 and newer)
#	- Provided for the large number of PowerPC G5 users.
#	- IFUNC support provides optimized core routines for POWER6,
#	  POWER7, and POWER8 transparently (if not using specific runtimes
#	  below)
# - POWER6 (has power6x symlink to power6, enabled via AT_PLATFORM)
#	- Legacy for old systems. Should be deprecated at some point soon.
# - POWER7 (enabled via AT_PLATFORM)
#	- Existing deployments.
# - POWER8 (enabled via AT_PLATFORM)
#	- Latest generation.
# 64-bit LE:
# - POWER8 LE (default)
#	- Latest generation.
#
# No 32-bit POWER support is provided.
#
# There are currently no plans for POWER9 enablement, but as hardware and
# upstream support become available this will be reviewed.
#
%ifarch ppc64
# Build the additional runtimes for 64-bit BE POWER.
%define buildpower6 1
%define buildpower7 1
%define buildpower8 1
%else
# No additional runtimes for ppc64le or ppc64p7, just the default.
%define buildpower6 0
%define buildpower7 0
%define buildpower8 0
%endif

##############################################################################
# Any architecture/kernel combination that supports running 32-bit and 64-bit
# code in userspace is considered a biarch arch.
%define biarcharches %{ix86} x86_64 %{power64} s390 s390x
##############################################################################
# If the debug information is split into two packages, the core debuginfo
# pacakge and the common debuginfo package then the arch should be listed
# here. If the arch is not listed here then a single core debuginfo package
# will be created for the architecture.
%define debuginfocommonarches %{biarcharches} alpha alphaev6
##############################################################################
# Add -s for a less verbose build output.
%define silentrules PARALLELMFLAGS=
##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: glibc
Version: %{glibcversion}
Release: %{glibcrelease}
# GPLv2+ is used in a bunch of programs, LGPLv2+ is used for libraries.
# Things that are linked directly into dynamically linked programs
# and shared libraries (e.g. crt files, lib*_nonshared.a) have an additional
# exception which allows linking it into any kind of programs or shared
# libraries without restrictions.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System Environment/Libraries
URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.gz
Source1: build-locale-archive.c
Source2: glibc_post_upgrade.c
Source4: nscd.conf
Source7: nsswitch.conf
Source8: power6emul.c
Source9: bench.mk
Source10: glibc-bench-compare
# A copt of localedata/SUPPORTED in the Source0 tarball.  The
# SUPPORTED file is used below to generate the list of locale
# packages.  See the language_list macro definition.
Source11: SUPPORTED

##############################################################################
# Start of glibc patches
##############################################################################
# 0000-0999 for patches which are unlikely to ever go upstream or which
# have not been analyzed to see if they ought to go upstream yet.
#
# 1000-2000 for patches that are already upstream.
#
# 2000-3000 for patches that are awaiting upstream approval
#
# Yes, I realize this means some gratutious changes as patches to from
# one bucket to another, but I find this scheme makes it easier to track
# the upstream divergence and patches needing approval.
#
# Note that we can still apply the patches in any order we see fit, so
# the changes from one bucket to another won't necessarily result in needing
# to twiddle the patch because of dependencies on prior patches and the like.


##############################################################################
#
# Patches that are unlikely to go upstream or not yet analyzed.
#
##############################################################################

# Configuration twiddle, not sure there's a good case to get upstream to
# change this.
Patch0001: glibc-fedora-nscd.patch

# Horrible hack, never to be upstreamed.  Can go away once the world
# has been rebuilt to use the new ld.so path.
Patch0006: glibc-arm-hardfloat-3.patch

# All these were from the glibc-fedora.patch mega-patch and need another
# round of reviewing.  Ideally they'll either be submitted upstream or
# dropped.
Patch0012: glibc-fedora-linux-tcsetattr.patch
Patch0014: glibc-fedora-nptl-linklibc.patch
Patch0015: glibc-fedora-localedef.patch
Patch0016: glibc-fedora-i386-tls-direct-seg-refs.patch
Patch0019: glibc-fedora-nis-rh188246.patch
Patch0020: glibc-fedora-manual-dircategory.patch
Patch0024: glibc-fedora-locarchive.patch
Patch0025: glibc-fedora-streams-rh436349.patch
Patch0028: glibc-fedora-localedata-rh61908.patch
Patch0031: glibc-fedora-__libc_multiple_libcs.patch
Patch0033: glibc-fedora-elf-ORIGIN.patch

# Needs to be sent upstream.
# Support mangling and demangling null pointers.
Patch0037: glibc-rh952799.patch

# Allow applications to call pthread_atfork without libpthread.so.
Patch0046: glibc-rh1013801.patch

Patch0047: glibc-nscd-sysconfig.patch

# confstr _CS_PATH should only return /usr/bin on Fedora since /bin is just a
# symlink to it.
Patch0053: glibc-cs-path.patch

# Add C.UTF-8 locale into /usr/lib/locale/
Patch0059: glibc-c-utf8-locale.patch

# Build libcrypt twice, with and without NSS.
Patch0060: glibc-rh1324623.patch

Patch62: glibc-rh1416405.patch
Patch63: glibc-rh1498880-1.patch
Patch64: glibc-rh1498880-2.patch
Patch65: glibc-nscd-reproducible.patch
Patch66: glibc-nss_compat.patch

# Bug 1615608 - Remove abort() warning in manual.
Patch67: glibc-rh1615608.patch

##############################################################################
#
# Patches from upstream
#
##############################################################################

##############################################################################
#
# Patches submitted, but not yet approved upstream.
#
##############################################################################
#
# Each should be associated with a BZ.
# Obviously we're not there right now, but that's the goal
#

# http://sourceware.org/ml/libc-alpha/2012-12/msg00103.html
Patch2007: glibc-rh697421.patch

Patch2013: glibc-rh741105.patch

# Upstream BZ 14247
Patch2023: glibc-rh827510.patch

# Upstream BZ 14185
Patch2027: glibc-rh819430.patch

Patch2031: glibc-rh1070416.patch

# extend_alloca removal, BZ 18023
Patch2036: glibc-rh1315108-glob.patch
Patch2037: glibc-rh1315108.patch

# sln implemented by ldconfig, to conserve disk space.
Patch2112: glibc-rh1315476-2.patch

Patch2115: glibc-rh1484729.patch
Patch2116: glibc-rh1484729-syscall-names.patch

# glibc perfromance patches
Patch3100: 0001-AArch64-Optimized-memcmp.patch
Patch3101: 0002-aarch64-Use-the-L-macro-for-labels-in-memcmp.patch
Patch3102: 0003-aarch64-Optimized-memcmp-for-medium-to-large-sizes.patch
Patch3103: 0004-aarch64-Fix-branch-target-to-loop16.patch
Patch3104: 0005-aarch64-Improve-strcmp-unaligned-performance.patch
Patch3105: 0006-aarch64-strcmp-fix-misaligned-loop-jump-target.patch
Patch3106: 0007-Improve-strstr-performance.patch
Patch3107: 0008-Simplify-and-speedup-strstr-strcasestr-first-match.patch
Patch3108: 0009-Speedup-first-memmem-match.patch
Patch3109: 0010-Fix-strstr-bug-with-huge-needles-bug-23637.patch
Patch3110: 0011-Add-ifunc-support-for-Ares.patch
Patch3111: 0012-Improve-performance-of-strstr.patch
Patch3112: 0013-Improve-performance-of-memmem.patch
Patch3113: 0014-Mark-lazy-tlsdesc-helper-functions-unused-to-avoid-w.patch
Patch3114: 0015-aarch64-Disable-lazy-symbol-binding-of-TLSDESC.patch
Patch3115: 0016-aarch64-Remove-barriers-from-TLS-descriptor-function.patch
Patch3116: 0017-arm-remove-prelinker-support-for-R_ARM_TLS_DESC.patch
Patch3117: 0018-arm-Disable-lazy-initialization-of-tlsdesc-entries.patch
Patch3118: 0019-arm-Remove-lazy-tlsdesc-initialization-related-code.patch
Patch3119: 0020-aarch64-optimize-_dl_tlsdesc_dynamic-fast-path.patch
Patch3120: 0021-aarch64-Use-PTR_REG-macro-to-fix-ILP32-bug-and-make-.patch
Patch3121: 0022-AArch64-update-libm-test-ulps.patch
Patch3122: 0023-Remove-slow-paths-from-pow.patch
Patch3123: 0024-Remove-slow-paths-from-exp.patch
Patch3124: 0025-Remove-slow-paths-from-log.patch
Patch3125: 0026-aarch64-Improve-strncmp-for-mutually-misaligned-inpu.patch
Patch3126: 0027-aarch64-strncmp-Unbreak-builds-with-old-binutils.patch
Patch3127: 0028-aarch64-strncmp-Use-lsr-instead-of-mov-lsr.patch

# CVE-2016-10739
Patch10001: CVE-2016-10739a.patch
Patch10002: CVE-2016-10739b.patch
Patch10003: CVE-2016-10739c.patch
Patch10004: CVE-2016-10739d.patch
Patch10005: CVE-2016-10739e.patch
Patch10006: CVE-2016-10739f.patch
Patch10007: CVE-2016-10739g.patch
##############################################################################
# End of glibc patches.
##############################################################################

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: glibc-profile < 2.4
Provides: ldconfig

# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# Various components (regex, glob) have been imported from gnulib.
Provides: bundled(gnulib)

# The IDNA implementation is based on libidn.
Provides: bundled(libidn)

# This is a short term need until everything is rebuilt in the ARM world
# to use the new dynamic linker path
%ifarch armv7hl armv7hnl
Provides: ld-linux.so.3
Provides: ld-linux.so.3(GLIBC_2.4)
%endif

Requires: glibc-common = %{version}-%{release}

%if %{without bootstrap}
# Use the NSS-based cryptographic libraries by default.
#Suggests: libcrypt-nss%{_isa}
%endif

Requires(pre): basesystem

# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
BuildRequires: gd-devel libpng-devel zlib-devel
%if %{with docs}
# Removing texinfo will cause check-safety.sh test to fail because it seems to
# trigger documentation generation based on dependencies.  We need to fix this
# upstream in some way that doesn't depend on generating docs to validate the
# texinfo.  I expect it's simply the wrong dependency for that target.
BuildRequires: texinfo >= 5.0
%endif
%if %{without bootstrap}
BuildRequires: libselinux-devel >= 1.33.4-3
BuildRequires: nss-devel
%endif
BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
# We need procps-ng (/bin/ps), util-linux (/bin/kill), and gawk (/bin/awk),
# but it is more flexible to require the actual programs and let rpm infer
# the packages. However, until bug 1259054 is widely fixed we avoid the
# following:
# BuildRequires: /bin/ps, /bin/kill, /bin/awk
# And use instead (which should be reverted some time in the future):
BuildRequires: procps-ng, util-linux, gawk
BuildRequires: systemtap-sdt-devel

%if %{with valgrind}
# Require valgrind for smoke testing the dynamic loader to make sure we
# have not broken valgrind.
BuildRequires: valgrind
%endif

# We use systemd rpm macros for nscd
BuildRequires: systemd

# We use python for the microbenchmarks and locale data regeneration from
# unicode sources (carried out manually). We choose python3 explicitly
# because it supports both use cases.
BuildRequires: python

# Required by rpcgen.
BuildRequires: cpp

# This is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: gcc >= 7.3.1-8
%define enablekernel 3.2
Conflicts: kernel < %{enablekernel}
%define target %{_target_cpu}-redhat-linux
%ifarch %{arm}
%define target %{_target_cpu}-redhat-linuxeabi
%endif
%ifarch %{power64}
%ifarch ppc64le
%define target ppc64le-redhat-linux
%else
%define target ppc64-redhat-linux
%endif
%endif

BuildRequires: binutils >= 2.25
# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2

%if 0%{?_enable_debug_packages}
BuildRequires: elfutils >= 0.72
BuildRequires: rpm >= 4.2-0.56
%endif

%if %{without boostrap}
%if %{with testsuite}
# The testsuite builds static C++ binaries that require a C++ compiler,
# static C++ runtime from libstdc++-static, and lastly static glibc.
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
# A configure check tests for the ability to create static C++ binaries
# before glibc is built and therefore we need a glibc-static for that
# check to pass even if we aren't going to use any of those objects to
# build the tests.
BuildRequires: glibc-static
%endif
%endif

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1

# For language packs we have glibc require a virtual dependency
# "glibc-langpack" wich gives us at least one installed langpack.
# If no langpack providing 'glibc-langpack' was installed you'd
# get all of them, and that would make the transition from a
# system without langpacks smoother (you'd get all the locales
# installed). You would then trim that list, and the trimmed list
# is preserved. One problem is you can't have "no" locales installed,
# in that case we offer a "glibc-minimal-langpack" sub-pakcage for
# this purpose.
%if 0%{?amzn}
Requires: glibc-minimal-langpack
%else
Requires: glibc-langpack = %{version}-%{release}
#Suggests: glibc-all-langpacks = %{version}-%{release}
%endif

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

##############################################################################
# glibc "xen" sub-package
##############################################################################
%if %{xenpackage}
%package xen
Summary: The GNU libc libraries (optimized for running under Xen)
Group: System Environment/Libraries
Requires: glibc = %{version}-%{release}, glibc-utils = %{version}-%{release}

%description xen
The standard glibc package is optimized for native kernels and does not
perform as well under the Xen hypervisor.  This package provides alternative
library binaries that will be selected instead when running under Xen.

Install glibc-xen if you might run your system under the Xen hypervisor.
%endif

######################################################################
# crypt subpackages
######################################################################

%package -n libcrypt
Summary: Password hashing library (non-NSS version)
Group: System Environment/Libraries
Requires: %{name}%{_isa} = %{version}-%{release}
Provides: libcrypt%{_isa}
Conflicts: libcrypt-nss

%description -n libcrypt
This package provides the crypt function, which implements password
hashing.  The glibc implementation of the cryptographic algorithms is
used by this package.

%post -n libcrypt
/sbin/ldconfig

%postun -n libcrypt
/sbin/ldconfig

%if %{without bootstrap}
%package -n libcrypt-nss
Summary: Password hashing library (NSS version)
Group: System Environment/Libraries
Requires: %{name}%{_isa} = %{version}-%{release}
Provides: libcrypt%{_isa}
Conflicts: libcrypt

%description -n libcrypt-nss
This package provides the crypt function, which implements password
hashing.  The cryptographic algorithm implementations are provided by
the low-level NSS libraries.

%post -n libcrypt-nss
/sbin/ldconfig

%postun -n libcrypt-nss
/sbin/ldconfig
%endif

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Group: Development/Libraries
Requires(pre): /sbin/install-info
Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: libgcc%{_isa}
Requires: libcrypt%{_isa}

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "static" sub-package
##############################################################################
%package static
Summary: C library static libraries for -static linking.
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

##############################################################################
# glibc "headers" sub-package
# - The headers package includes all common headers that are shared amongst
#   the multilib builds. It was created to reduce the download size, and
#   thus avoid downloading one header package per multilib. The package is
#   identical both in content and file list, any difference is an error.
#   Files like gnu/stubs.h which have gnu/stubs-32.h (i686) and gnu/stubs-64.h
#   are included in glibc-headers, but the -32 and -64 files are in their
#   respective i686 and x86_64 devel packages.
##############################################################################
%package headers
Summary: Header files for development using standard C libraries.
Group: Development/Libraries
Provides: %{name}-headers(%{_target_cpu})
%ifarch x86_64
# If both -m32 and -m64 is to be supported on AMD64, x86_64 glibc-headers
# have to be installed, not i586 ones.
Obsoletes: %{name}-headers(i586)
Obsoletes: %{name}-headers(i686)
%endif
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
BuildRequires: kernel-headers >= 3.2

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "common" sub-package
##############################################################################
%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a
Group: System Environment/Base

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

%package locale-source
Summary: The sources for the locales
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Group: System Environment/Base

%description locale-source
The sources for all locales provided in the language packs.
If you are building custom locales you will most likely use
these sources as the basis for your new locale.

%define lang_package()\
%package langpack-%{1}\
Summary: Locale data for %{1}\
Provides: glibc-langpack = %{version}-%{release}\
Requires: %{name} = %{version}-%{release}\
Requires: %{name}-common = %{version}-%{release}\
%define supplements_list %(cat %{SOURCE11} | grep ^%{1}_ | cut -d / -f 1 | cut -d @ -f 1 | cut -d . -f 1 | sort -u | tr "\\\\n" " " | sed 's/ $//' | sed 's/ / or langpacks-/g' | sed 's/^/ or langpacks-/')\
Group: System Environment/Base\
%description langpack-%{1}\
The glibc-langpack-%{1} package includes the basic information required\
to support the %{1} language in your applications.\
%ifnarch %{auxarches}\
%files -f langpack-%{1}.filelist langpack-%{1}\
%defattr(-,root,root)\
%endif\
%{nil}

# language_list will contain a list of all supported language
# names in iso-639 format, i.e. something like "aa af ... yue zh zu"
# We add "eo" (Esperanto) manually because currently glibc has no
# Esperanto locale in SUPPORTED but translations for Esperanto exist.
# Therefore, we want a glibc-langpack-eo sub-package containing these
# translations.
%define language_list eo %(cat %{SOURCE11} | grep -E  '^[a-z]+_' | cut -d _ -f 1 | sort -u | tr "\\\\n" " " | sed 's/ $//')

%{lua:
local languages = rpm.expand("%language_list")
string.gsub(languages, "(%a+)",
            function(i) print(rpm.expand("%lang_package "..i.."")) end)
}

# The glibc-all-langpacks provides the virtual glibc-langpack,
# and thus satisfies glibc's requirement for installed locales.
# Users can add one more other langauge packs and then eventually
# uninstall all-langpacks to save space.
%package all-langpacks
Summary: All language packs for %{name}.
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-langpack = %{version}-%{release}
%description all-langpacks

# No %%files, this is an empty pacakge. The C/POSIX and
# C.UTF-8 files are already installed by glibc. We create
# minimal-langpack because the virtual provide of
# glibc-langpack needs at least one package installed
# to satisfy it. Given that no-locales installed is a valid
# use case we support it here with this package.
%package minimal-langpack
Summary: Minimal language packs for %{name}.
Group: System Environment/Base
Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description minimal-langpack
This is a Meta package that is used to install minimal language packs.
This package ensures you can use C, POSIX, or C.UTF-8 locales, but
nothing else. It is designed for assembling a minimal system.
%ifnarch %{auxarches}
%files minimal-langpack
%endif

##############################################################################
# glibc "nscd" sub-package
##############################################################################
%package -n nscd
Summary: A Name Service Caching Daemon (nscd).
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%if %{without bootstrap}
Requires: libselinux >= 1.17.10-1
%endif
Requires: audit-libs >= 1.1.3
Requires(pre): /usr/sbin/useradd, coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd, /usr/sbin/userdel

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.

##############################################################################
# Subpackages for NSS modules except nss_files, nss_dns
##############################################################################

%package -n nss_db
Summary: Name Service Switch (NSS) module using hash-indexed files
Group: System Environment/Base
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n nss_db
The nss_db Name Service Switch module uses hash-indexed files in /var/db
to speed up user, group, service, host name, and other NSS-based lookups.

%package -n nss_nis
Summary: Name Service Switch (NSS) module using NIS
Group: System Environment/Base
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n nss_nis
The nss_nis and nss_nisplus Name Service Switch modules uses the
Network Information System (NIS) to obtain user, group, host name, and
other data.

%package -n nss_hesiod
Summary: Name Service Switch (NSS) module using Hesiod
Group: System Environment/Base
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n nss_hesiod
The nss_hesiod Name Service Switch module uses the Domain Name System
(DNS) as a source for user, group, and service information, following
the Hesiod convention of Project Athena.

%package nss-devel
Summary: Development files for directly linking NSS service modules
Group: Development/Libraries
Requires: nss_db%{_isa} = %{version}-%{release}
Requires: nss_nis%{_isa} = %{version}-%{release}
Requires: nss_hesiod%{_isa} = %{version}-%{release}

%description nss-devel
The glibc-nss-devel package contains the object files necessary to
compile applications and libraries which directly link against NSS
modules supplied by glibc.

This is a rare and special use case; regular development has to use
the glibc-devel package instead.

##############################################################################
# glibc "utils" sub-package
##############################################################################
%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

##############################################################################
# glibc core "debuginfo" sub-package
##############################################################################
%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%global __debug_package 1
# Disable thew new features that glibc packages don't use.
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%undefine _unique_debug_names
%undefine _unique_debug_srcs

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no
%ifarch %{debuginfocommonarches}
Requires: glibc-debuginfo-common = %{version}-%{release}
%else
%ifarch %{ix86} %{sparc}
Obsoletes: glibc-debuginfo-common
%endif
%endif

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

This package also contains static standard C libraries with
debugging information.  You need this only if you want to step into
C library routines during debugging programs statically linked against
one or more of the standard C libraries.
To use this debugging information, you need to link binaries
with -static -L%{_prefix}/lib/debug%{_libdir} compiler options.

##############################################################################
# glibc common "debuginfo-common" sub-package
##############################################################################
%ifarch %{debuginfocommonarches}

%package debuginfo-common
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no

%description debuginfo-common
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%endif # %%{debuginfocommonarches}
%endif # 0%%{?_enable_debug_packages}

%if %{with benchtests}
%package benchtests
Summary: Benchmarking binaries and scripts for %{name}
Group: Development/Debug
%description benchtests
This package provides built benchmark binaries and scripts to run
microbenchmark tests on the system.
%endif

##############################################################################
# Prepare for the build.
##############################################################################
%prep
%setup -q -n %{glibcsrcdir}

# Patch order matters.
%patch0001 -p1
%patch0006 -p1
%patch2007 -p1
%patch0012 -p1
%patch2013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0019 -p1
%patch0020 -p1
%patch2023 -p1
%patch0024 -p1
%patch0025 -p1
%patch2027 -p1
%patch0028 -p1
%patch0031 -p1
%patch0033 -p1
%patch0037 -p1
%patch0046 -p1
%patch2031 -p1
%patch0047 -p1
%patch0053 -p1
%patch0059 -p1
%patch0060 -p1
%patch2036 -p1
%patch2037 -p1
%patch2112 -p1
%patch2115 -p1
%patch2116 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch3100 -p1
%patch3101 -p1
%patch3102 -p1
%patch3103 -p1
%patch3104 -p1
%patch3105 -p1
%patch3106 -p1
%patch3107 -p1
%patch3108 -p1
%patch3109 -p1
%patch3110 -p1
%patch3111 -p1
%patch3112 -p1
%patch3113 -p1
%patch3114 -p1
%patch3115 -p1
%patch3116 -p1
%patch3117 -p1
%patch3118 -p1
%patch3119 -p1
%patch3120 -p1
%patch3121 -p1
%patch3122 -p1
%patch3123 -p1
%patch3124 -p1
%patch3125 -p1
%patch3126 -p1
%patch3127 -p1
#patch10001 -p1
#patch10002 -p1
#patch10003 -p1
#patch10004 -p1
#patch10005 -p1
#patch10006 -p1
#patch10007 -p1
##############################################################################
# %%prep - Additional prep required...
##############################################################################
# Make benchmark scripts executable
chmod +x benchtests/scripts/*.py scripts/pylint

# Remove all files generated from patching.
find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
touch locale/programs/*-kw.h

%if ! 0%{?amzn}
# Verify that our copy of localedata/SUPPORTED matches the glibc
# version.
#
# The separate file copy is used by the language_list macro above.
# Patches or new upstream versions may change the list of locales,
# which changes the set of langpacks we need to build.  Verify the
# differences then update the copy of SUPPORTED.  This approach has
# two purposes: (a) avoid spurious changes to the set of langpacks,
# and (b) the language_list macro can use a fully patched-up version
# of the localedata/SUPPORTED file.
diff -u %{SOURCE11} localedata/SUPPORTED
%endif

##############################################################################
# Build glibc...
##############################################################################
%build
# Log system information
uname -a
LD_SHOW_AUXV=1 /bin/true
cat /proc/cpuinfo
cat /proc/meminfo
df

# We build using the native system compilers.
GCC=gcc
GXX=g++

# Propagates the listed flags to BuildFlags if supplied by redhat-rpm-config.
BuildFlags="-O2 -g"
%if %{_target_cpu}=="aarch64"
BuildFlags="$BuildFlags -moutline-atomics"
%endif
rpm_inherit_flags ()
{
	local reference=" $* "
	local flag
	for flag in $RPM_OPT_FLAGS $RPM_LD_FLAGS ; do
		if echo "$reference" | grep -q -F " $flag " ; then
			BuildFlags="$BuildFlags $flag"
		fi
	done
}

# Propgate select compiler flags from redhat-rpm-config.  These flags
# are target-dependent, so we use only those which are specified in
# redhat-rpm-config.  We do not replicate the -march=/-mtune=
# selection here because these match the defaults compiled into GCC.
# We keep the -m32/-m32/-m64 flags to support multilib builds.

rpm_inherit_flags \
	"-fasynchronous-unwind-tables" \
	"-fstack-clash-protection" \
	"-funwind-tables" \
	"-m31" \
	"-m32" \
	"-m64" \

##############################################################################
# %%build - Generic options.
##############################################################################
EnableKernel="--enable-kernel=%{enablekernel}"
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc
AddOns=`echo */configure | sed -e 's!/configure!!g;s!\(nptl\|powerpc-cpu\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`

##############################################################################
# build()
#	Build glibc in `build-%%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, add-ons, kernel
#	version, system tap support, etc.
##############################################################################
build()
{
	local builddir=build-%{target}${1:+-$1}
	${1+shift}
	rm -rf $builddir
	mkdir $builddir
	pushd $builddir
	../configure CC="$GCC" CXX="$GXX" CFLAGS="$BuildFlags $*" \
		--prefix=%{_prefix} \
		--enable-add-ons=$AddOns \
		--with-headers=%{_prefix}/include $EnableKernel \
		--enable-bind-now \
		--build=%{target} \
		--enable-stack-protector=strong \
		--enable-tunables \
		--enable-obsolete-rpc \
		--enable-obsolete-nsl \
		--enable-systemtap \
		${core_with_options} \
%ifarch %{ix86}
		--disable-multi-arch \
%endif
		--disable-lock-elision \
%if %{without werror}
		--disable-werror \
%endif
		--disable-profile \
%if %{with bootstrap}
		--without-selinux \
		--disable-nss-crypt ||
%else
		--enable-nss-crypt ||
%endif
		{ cat config.log; false; }
%if 0%{?amzn}
	make %{?_smp_mflags} -r
%else
	make %{?_smp_mflags} -O -r
%endif
	popd
}

##############################################################################
# Build glibc for the default set of options.
##############################################################################
build

##############################################################################
# Build glibc for xen:
# If we support xen build glibc again for xen support.
##############################################################################
%if %{buildxen}
build nosegneg -mno-tls-direct-seg-refs
%endif

##############################################################################
# Build glibc for power6:
# If we support building a power6 alternate runtime then built glibc again for
# power6.
# XXX: We build in a sub-shell for no apparent reason.
##############################################################################
%if %{buildpower6}
(
	platform=`LD_SHOW_AUXV=1 /bin/true | sed -n 's/^AT_PLATFORM:[[:blank:]]*//p'`
	if [ "$platform" != power6 ]; then
		mkdir -p power6emul/{lib,lib64}
		$GCC -shared -O2 -fpic -o power6emul/%{_lib}/power6emul.so %{SOURCE8} -Wl,-z,initfirst
%ifarch ppc64
		gcc -shared -nostdlib -O2 -fpic -m32 -o power6emul/lib/power6emul.so -xc - < /dev/null
%endif
		export LD_PRELOAD=`pwd`/power6emul/\$LIB/power6emul.so
	fi
	GCC="$GCC -mcpu=power6"
	GXX="$GXX -mcpu=power6"
	core_with_options="--with-cpu=power6"
	build power6
)
%endif # %%{buildpower6}

%if %{buildpower7}
(
  GCC="$GCC -mcpu=power7 -mtune=power7"
  GXX="$GXX -mcpu=power7 -mtune=power7"
  core_with_options="--with-cpu=power7"
  build power7
)
%endif

%if %{buildpower8}
(
  GCC="$GCC -mcpu=power8 -mtune=power8"
  GXX="$GXX -mcpu=power8 -mtune=power8"
  core_with_options="--with-cpu=power8"
  build power8
)
%endif

# Build libcrypt with glibc cryptographic implementations.
%if %{without bootstrap}
make %{?_smpflags} -C build-%{target} subdirs=crypt-glibc \
    CFLAGS="$build_CFLAGS" %{silentrules}
%endif

##############################################################################
# Build the glibc post-upgrade program:
# We only build one of these with the default set of options. This program
# must be able to run on all hardware for the lowest common denomintor since
# we only build it once.
##############################################################################
pushd build-%{target}
$GCC -static -L. -Os -g %{SOURCE2} \
	-o glibc_post_upgrade.%{_target_cpu} \
	'-DLIBTLS="/%{_lib}/tls/"' \
	'-DGCONV_MODULES_DIR="%{_libdir}/gconv"' \
	'-DLD_SO_CONF="/etc/ld.so.conf"' \
	'-DICONVCONFIG="%{_sbindir}/iconvconfig.%{_target_cpu}"'
popd

##############################################################################
# Install glibc...
##############################################################################
%install

# Ensure the permissions of errlist.c do not change.  When the file is
# regenerated the Makefile sets the permissions to 444. We set it to 644
# to match what comes out of git. The tarball of the git archive won't have
# correct permissions because git doesn't track all of the permissions
# accurately (see git-cache-meta if you need that). We also set it to 644 to
# match pre-existing rpms. We do this *after* the build because the build
# might regenerate the file and set the permissions to 444.
chmod 644 sysdeps/gnu/errlist.c

# Reload compiler and build options that were used during %%build.
GCC=`cat Gcc`

# Cleanup any previous installs...
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make -j1 install_root=$RPM_BUILD_ROOT \
	install -C build-%{target} %{silentrules}
# If we are not building an auxiliary arch then install all of the supported
# locales.
%ifnarch %{auxarches}
pushd build-%{target}
# Do not use a parallel make here because the hardlink optimization in
# localedef is not fully reproducible when running concurrently.
make install_root=$RPM_BUILD_ROOT \
	install-locales -C ../localedata objdir=`pwd`
popd
%endif

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}-*.so)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
		dlib=$libdestdir/$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}.so.*)
		ln -sf $libbaseso $dlib
	done
}

#############################################################################
# Install libcrypt
#############################################################################

%if %{without bootstrap}
# Move the NSS-based implementation out of the way.
libcrypt_found=false
for libcrypt in ${RPM_BUILD_ROOT}/%{_lib}/libcrypt-*.so ; do
  if $libcrypt_found; then
    # Multiple libcrypt files
    ls -l ${RPM_BUILD_ROOT}/%{_lib}/libcrypt-*.so
    exit 1
  fi
  mv "$libcrypt" "$(echo "$libcrypt" | sed s/libcrypt-/libcrypt-nss-/)"
done

# Install the non-NSS implementation in the original path.
install -m 755 build-%{target}/crypt-glibc/libcrypt.so "$libcrypt"

unset libcrypt libcrypt_found
%endif

# This symbolic link will be generated by ldconfig.
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libcrypt.so.1

##############################################################################
# Install the xen build files.
##############################################################################
%if %{buildxen}
%define nosegneg_subdir_base i686
%define nosegneg_subdir i686/nosegneg
%define nosegneg_subdir_up ../..
pushd build-%{target}-nosegneg
destdir=$RPM_BUILD_ROOT/%{_lib}
install_different "$destdir" "%{nosegneg_subdir}" "%{nosegneg_subdir_up}"
popd
%endif # %%{buildxen}

##############################################################################
# Install the power6 build files.
##############################################################################
%if %{buildpower6}
%define power6_subdir power6
%define power6_subdir_up ..
%define power6_legacy power6x
%define power6_legacy_up ..
pushd build-%{target}-power6
destdir=$RPM_BUILD_ROOT/%{_lib}
install_different "$destdir" "%{power6_subdir}" "%{power6_subdir_up}"
# Make a legacy /usr/lib[64]/power6x directory that is a symlink to the
# power6 runtime.
# XXX: When can we remove this? What is the history behind this?
mkdir -p ${destdir}/%{power6_legacy}
pushd ${destdir}/%{power6_legacy}
ln -sf %{power6_legacy_up}/%{power6_subdir}/*.so .
cp -a %{power6_legacy_up}/%{power6_subdir}/*.so.* .
popd
popd
%endif # %%{buildpower6}

%if %{buildpower7}
%define power7_subdir power7
%define power7_subdir_up ..
pushd build-%{target}-power7
destdir=$RPM_BUILD_ROOT/%{_lib}
install_different "$destdir" "%{power7_subdir}" "%{power7_subdir_up}"
popd
%endif

%if %{buildpower8}
%define power8_subdir power8
%define power8_subdir_up ..
pushd build-%{target}-power8
destdir=$RPM_BUILD_ROOT/%{_lib}
install_different "$destdir" "%{power8_subdir}" "%{power8_subdir_up}"
popd
%endif

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f $RPM_BUILD_ROOT%{_libdir}/libNoVersion*
rm -f $RPM_BUILD_ROOT/%{_lib}/libNoVersion*

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# Remove the old nss modules.
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1

##############################################################################
# Install info files
##############################################################################

%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_infodir}
  mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

%else
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_infodir}/libc.info*
%endif

##############################################################################
# Create locale sub-package file lists
##############################################################################

%ifnarch %{auxarches}
olddir=`pwd`
pushd ${RPM_BUILD_ROOT}%{_prefix}/lib/locale
rm -f locale-archive
# Intentionally we do not pass --alias-file=, aliases will be added
# by build-locale-archive.
$olddir/build-%{target}/elf/ld.so \
        --library-path $olddir/build-%{target}/ \
        $olddir/build-%{target}/locale/localedef \
        --prefix ${RPM_BUILD_ROOT} --add-to-archive \
        *_*
# Setup the locale-archive template for use by glibc-all-langpacks.
mv locale-archive{,.tmpl}
# Create the file lists for the language specific sub-packages:
for i in eo *_*
do
    lang=${i%%_*}
    if [ ! -e langpack-${lang}.filelist ]; then
        echo "%dir %{_prefix}/lib/locale" >> langpack-${lang}.filelist
    fi
    echo "%dir  %{_prefix}/lib/locale/$i" >> langpack-${lang}.filelist
    echo "%{_prefix}/lib/locale/$i/*" >> langpack-${lang}.filelist
done
popd
pushd ${RPM_BUILD_ROOT}%{_prefix}/share/locale
for i in */LC_MESSAGES/libc.mo
do
    locale=${i%%%%/*}
    lang=${locale%%%%_*}
    echo "%lang($lang) %{_prefix}/share/locale/${i}" \
         >> ${RPM_BUILD_ROOT}%{_prefix}/lib/locale/langpack-${lang}.filelist
done
popd
mv  ${RPM_BUILD_ROOT}%{_prefix}/lib/locale/*.filelist .
%endif

##############################################################################
# Install configuration files for services
##############################################################################

install -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/nsswitch.conf

%ifnarch %{auxarches}
mkdir -p $RPM_BUILD_ROOT/etc/default
install -p -m 644 nis/nss $RPM_BUILD_ROOT/etc/default/nss

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system
install -m 644 nscd/nscd.service nscd/nscd.socket $RPM_BUILD_ROOT/lib/systemd/system
%endif

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
truncate -s 0 $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
%ifnarch %{auxarches}
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
truncate -s 0 $RPM_BUILD_ROOT/etc/sysconfig/nscd
truncate -s 0 $RPM_BUILD_ROOT/etc/gai.conf
%endif

# Include %%{_libdir}/gconv/gconv-modules.cache
truncate -s 0 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache

##############################################################################
# Misc...
##############################################################################

# Install the upgrade program
install -m 700 build-%{target}/glibc_post_upgrade.%{_target_cpu} \
  $RPM_BUILD_ROOT%{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

# Strip all of the installed object files.
strip -g $RPM_BUILD_ROOT%{_libdir}/*.o

# XXX: Ugly hack for buggy rpm. What bug? BZ? Is this fixed?
ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

##############################################################################
# Install debug copies of unstripped static libraries
# - This step must be last in order to capture any additional static
#   archives we might have added.
##############################################################################

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}
cp -a $RPM_BUILD_ROOT%{_libdir}/*.a \
	$RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/*_p.a
%endif

##############################################################################
# Build the file lists used for describing the package and subpackages.
##############################################################################
# There are several main file lists (and many more for
# the langpack sub-packages (langpack-${lang}.filelist)):
# * rpm.fileslist
#	- Master file list. Eventually, after removing files from this list
#	  we are left with the list of files for the glibc package.
# * common.filelist
#	- Contains the list of flies for the common subpackage.
# * utils.filelist
#	- Contains the list of files for the utils subpackage.
# * nscd.filelist
#	- Contains the list of files for the nscd subpackage.
# * devel.filelist
#	- Contains the list of files for the devel subpackage.
# * headers.filelist
#	- Contains the list of files for the headers subpackage.
# * static.filelist
#	- Contains the list of files for the static subpackage.
# * nosegneg.filelist
#	- Contains the list of files for the xen subpackage.
# * libcrypt.filelist, libcrypt-nss.filelist
#       - Contains the list of files for the crypt-related subpackages
# * nss_db.filelist, nss_nis.filelist, nss_hesiod.filelist
#       - File lists for nss_* NSS module subpackages.
# * nss-devel.filelist
#       - File list with the .so symbolic links for NSS packages.
# * debuginfo.filelist
#	- Contains the list of files for the glibc debuginfo package.
# * debuginfocommon.filelist
#	- Contains the list of files for the glibc common debuginfo package.
#

{
  find $RPM_BUILD_ROOT \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  # Print all directories with a %%dir prefix.  We omit the info directory and
  # all directories in (and including) /usr/share/locale.
  find $RPM_BUILD_ROOT -type d \
       \( -path '*%{_prefix}/share/locale' -prune -o \
       \( -path '*%{_prefix}/share/*' \
%if %{with docs}
	! -path '*%{_infodir}' -o \
%endif
	  -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n" \)
} | {

  # primary filelist

  # Also remove the *.mo entries.  We will add them to the
  # language specific sub-packages.
  # libnss_ files go into subpackages related to NSS modules.
  # and .*/share/i18n/charmaps/.*), they go into the sub-package
  # "locale-source":
  sed -e '\,.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo,d' \
      -e '\,.*/share/i18n/locales/.*,d' \
      -e '\,.*/share/i18n/charmaps/.*,d' \
      -e '\,/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,/%{_lib}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > rpm.filelist

touch common.filelist

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_libdir}

# The xtrace and memusage scripts have hard-coded paths that need to be
# translated to a correct set of paths using the $LIB token which is
# dynamically translated by ld.so as the default lib directory.
for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

%if %{with docs}
# Put the info files into the devel file list.
grep '%{_infodir}' < rpm.filelist | grep -v '%{_infodir}/dir' > devel.filelist
%endif

# The glibc-headers package includes only common files which are identical
# across all multilib packages. We must keep gnu/stubs.h and gnu/lib-names.h
# in the glibc-headers package, but the -32, -64, -64-v1, and -64-v2 versions
# go into the development packages.
grep '%{_prefix}/include/gnu/stubs-.*\.h$' < rpm.filelist >> devel.filelist || :
grep '%{_prefix}/include/gnu/lib-names-.*\.h$' < rpm.filelist >> devel.filelist || :
# Put the include files into headers file list.
grep '%{_prefix}/include' < rpm.filelist \
  | egrep -v '%{_prefix}/include/gnu/stubs-.*\.h$' \
  | egrep -v '%{_prefix}/include/gnu/lib-names-.*\.h$' \
  > headers.filelist

# Remove partial (lib*_p.a) static libraries, include files, and info files from
# the core glibc package.
sed -i -e '\|%{_libdir}/lib.*_p.a|d' \
       -e '\|%{_prefix}/include|d' \
       -e '\|%{_infodir}|d' \
	rpm.filelist

# Put some static files into the devel package.
grep '%{_libdir}/lib.*\.a' < rpm.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  >> devel.filelist

# Put the rest of the static files into the static package.
grep '%{_libdir}/lib.*\.a' < rpm.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  > static.filelist

# Put all of the object files and *.so (not the versioned ones) into the
# devel package.
grep '%{_libdir}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < rpm.filelist >> devel.filelist

# Remove all of the static, object, unversioned DSOs, and nscd from the core
# glibc package.
sed -i -e '\|%{_libdir}/lib.*\.a|d' \
       -e '\|%{_libdir}/.*\.o|d' \
       -e '\|%{_libdir}/lib.*\.so|d' \
       -e '\|nscd|d' rpm.filelist

# All of the bin and certain sbin files go into the common package.
# We explicitly exclude certain sbin files that need to go into
# the core glibc package for use during upgrades.
grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
# All of the files under share go into the common package since
# they should be multilib-independent.
grep '%{_prefix}/share' < rpm.filelist | \
  grep -v -e '%{_prefix}/share/zoneinfo' -e '%%dir %{prefix}/share' \
       >> common.filelist

# Remove the bin, locale, some sbin, and share from the
# core glibc package. We cheat a bit and use the slightly dangerous
# /usr/sbin/[^gi] to match the inverse of the search that put the
# files into common.filelist. It's dangerous in that additional files
# that start with g, or i would get put into common.filelist and
# rpm.filelist.
sed -i -e '\|%{_prefix}/bin|d' \
       -e '\|%{_prefix}/lib/locale|d' \
       -e '\|%{_prefix}/sbin/[^gi]|d' \
       -e '\|%{_prefix}/share|d' rpm.filelist

##############################################################################
# Build the xen package file list (nosegneg.filelist)
##############################################################################
truncate -s 0 nosegneg.filelist
%if %{xenpackage}
grep '/%{_lib}/%{nosegneg_subdir}' < rpm.filelist >> nosegneg.filelist
sed -i -e '\|/%{_lib}/%{nosegneg_subdir}|d' rpm.filelist
# TODO: There are files in the nosegneg list which should be in the devel
#	pacakge, but we leave them instead in the xen subpackage. We may
#	wish to clean that up at some point.
%endif

# Add the binary to build locales to the common subpackage.
echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist

# The nscd binary must go into the nscd subpackage.
echo '%{_prefix}/sbin/nscd' > nscd.filelist

# The memusage and pcprofile libraries are put back into the core
# glibc package even though they are only used by utils package
# scripts..
cat >> rpm.filelist <<EOF
%{_libdir}/libmemusage.so
%{_libdir}/libpcprofile.so
EOF

# Add the utils scripts and programs to the utils subpackage.
cat > utils.filelist <<EOF
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%if %{without bootstrap}
%{_prefix}/bin/mtrace
%endif
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

# Move the NSS-related files to the NSS subpackages.  Be careful not
# to pick up .debug files, and the -devel symbolic links.
for module in db nis nisplus compat hesiod files dns; do
  grep -E "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
    rpm.filelist > nss_$module.filelist
done
# nis includes nisplus
cat nss_nisplus.filelist >> nss_nis.filelist
# Symlinks go into the nss-devel package (instead of the main devel
# package).
grep '/libnss_[a-z]*\.so$' devel.filelist > nss-devel.filelist
# /var/db/Makefile goes into nss_db, remove the other files from
# the main and devel file list.
sed -i -e '\,/libnss_.*\.so[0-9.]*$,d' \
    -e '\,/var/db/Makefile,d' \
    rpm.filelist devel.filelist
# Restore the built-in NSS modules.
cat nss_files.filelist nss_dns.filelist nss_compat.filelist >> rpm.filelist

# Prepare the libcrypt-related file lists.
grep '/libcrypt-[0-9.]*.so$' rpm.filelist > libcrypt.filelist
test $(wc -l < libcrypt.filelist) -eq 1
%if %{without bootstrap}
sed s/libcrypt/libcrypt-nss/ < libcrypt.filelist > libcrypt-nss.filelist
%endif
sed -i -e '\,/libcrypt,d' rpm.filelist

# Remove the zoneinfo files
# XXX: Why isn't this don't earlier when we are removing files?
#      Won't this impact what is shipped?
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# Make sure %%config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent.  The choice of using
# glibc_post_upgrade.c is arbitrary.
touch -r %{SOURCE2} $RPM_BUILD_ROOT/etc/ld.so.conf
touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT/etc/rpc

# We allow undefined symbols in shared libraries because the libraries
# referenced at link time here, particularly ld.so, may be different than
# the one used at runtime.  This is really only needed during the ARM
# transition from ld-linux.so.3 to ld-linux-armhf.so.3.
pushd build-%{target}
$GCC -Os -g -static -o build-locale-archive %{SOURCE1} \
	../build-%{target}/locale/locarchive.o \
	../build-%{target}/locale/md5.o \
	-I. -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
	-L../build-%{target} \
	-Wl,--allow-shlib-undefined \
	-B../build-%{target}/csu/ -lc -lc_nonshared
install -m 700 build-locale-archive $RPM_BUILD_ROOT%{_prefix}/sbin/build-locale-archive
popd

# Lastly copy some additional documentation for the packages.
rm -rf documentation
mkdir documentation
cp crypt/README.ufc-crypt documentation/README.ufc-crypt
cp timezone/README documentation/README.timezone
cp posix/gai.conf documentation/

%ifarch s390x
# Compatibility symlink
mkdir -p $RPM_BUILD_ROOT/lib
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT/lib/ld64.so.1
%endif

# Leave a compatibility symlink for the dynamic loader on armhfp targets,
# at least until the world gets rebuilt
%ifarch armv7hl armv7hnl
ln -sf /lib/ld-linux-armhf.so.3 $RPM_BUILD_ROOT/lib/ld-linux.so.3
%endif

%if %{with benchtests}
# Build benchmark binaries.  Ignore the output of the benchmark runs.
pushd build-%{target}
make BENCH_DURATION=1 bench-build
popd

# Copy over benchmark binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests
cp $(find build-%{target}/benchtests -type f -executable) $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/

find build-%{target}/benchtests -type f -executable | while read b; do
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)"
done >> benchtests.filelist

# ... and the makefile.
for b in %{SOURCE9} %{SOURCE10}; do
	cp $b $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)" >> benchtests.filelist
done

# .. and finally, the comparison scripts.
cp benchtests/scripts/benchout.schema.json $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/compare_bench.py $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/import_bench.py $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/validate_benchout.py $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/

echo "%{_prefix}/libexec/glibc-benchtests/benchout.schema.json" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/compare_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/import_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/validate_benchout.py*" >> benchtests.filelist
%endif

###############################################################################
# Rebuild libpthread.a using --whole-archive to ensure all of libpthread
# is included in a static link. This prevents any problems when linking
# statically, using parts of libpthread, and other necessary parts not
# being included. Upstream has decided that this is the wrong approach to
# this problem and that the full set of dependencies should be resolved
# such that static linking works and produces the most minimally sized
# static application possible.
###############################################################################
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
$GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
popd
###############################################################################

%if 0%{?_enable_debug_packages}

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
pushd locale
ln -s programs/*.gperf .
popd
pushd iconv
ln -s ../locale/programs/charmap-kw.gperf .
popd

# Print some diagnostic information in the builds about the
# getconf binaries.
# XXX: Why do we do this?
ls -l $RPM_BUILD_ROOT%{_prefix}/bin/getconf
ls -l $RPM_BUILD_ROOT%{_prefix}/libexec/getconf
eu-readelf -hS $RPM_BUILD_ROOT%{_prefix}/bin/getconf \
	$RPM_BUILD_ROOT%{_prefix}/libexec/getconf/*

find_debuginfo_args='--strict-build-id -g'
%ifarch %{debuginfocommonarches}
find_debuginfo_args="$find_debuginfo_args \
	-l common.filelist \
	-l utils.filelist \
	-l nscd.filelist \
	-p '.*/(sbin|libexec)/.*' \
	-o debuginfocommon.filelist \
	-l nss_db.filelist -l nss_nis.filelist -l nss_hesiod.filelist \
	-l libcrypt.filelist \
%if %{without bootstrap}
	-l libcrypt-nss.filelist \
%endif
	-l rpm.filelist \
%if %{with benchtests}
	-l nosegneg.filelist -l benchtests.filelist"
%else
	-l nosegneg.filelist"
%endif
%endif
/usr/lib/rpm/find-debuginfo.sh $find_debuginfo_args -o debuginfo.filelist

# List all of the *.a archives in the debug directory.
list_debug_archives()
{
	local dir=%{_prefix}/lib/debug%{_libdir}
	find $RPM_BUILD_ROOT$dir -name "*.a" -printf "$dir/%%P\n"
}

%ifarch %{debuginfocommonarches}

# Remove the source files from the common package debuginfo.
sed -i '\#^%{_prefix}/src/debug/#d' debuginfocommon.filelist

# Create a list of all of the source files we copied to the debug directory.
find $RPM_BUILD_ROOT%{_prefix}/src/debug \
     \( -type d -printf '%%%%dir ' \) , \
     -printf '%{_prefix}/src/debug/%%P\n' > debuginfocommon.sources

%ifarch %{biarcharches}

# Add the source files to the core debuginfo package.
cat debuginfocommon.sources >> debuginfo.filelist

%else

%ifarch %{ix86}
%define basearch i686
%endif
%ifarch sparc sparcv9
%define basearch sparc
%endif

# The auxarches get only these few source files.
auxarches_debugsources=\
'/(generic|linux|%{basearch}|nptl(_db)?)/|/%{glibcsrcdir}/build|/dl-osinfo\.h'

# Place the source files into the core debuginfo pakcage.
egrep "$auxarches_debugsources" debuginfocommon.sources >> debuginfo.filelist

# Remove the source files from the common debuginfo package.
egrep -v "$auxarches_debugsources" \
  debuginfocommon.sources >> debuginfocommon.filelist

%endif # %%{biarcharches}

# Add the list of *.a archives in the debug directory to
# the common debuginfo package.
list_debug_archives >> debuginfocommon.filelist

# It happens that find-debuginfo.sh produces duplicate entries even
# though the inputs are unique. Therefore we sort and unique the
# entries in the debug file lists. This avoids the following warnings:
# ~~~
# Processing files: glibc-debuginfo-common-2.17.90-10.fc20.x86_64
# warning: File listed twice: /usr/lib/debug/usr/sbin/build-locale-archive.debug
# warning: File listed twice: /usr/lib/debug/usr/sbin/nscd.debug
# warning: File listed twice: /usr/lib/debug/usr/sbin/zdump.debug
# warning: File listed twice: /usr/lib/debug/usr/sbin/zic.debug
# ~~~
sort -u debuginfocommon.filelist > debuginfocommon2.filelist
mv debuginfocommon2.filelist debuginfocommon.filelist

%endif # %%{debuginfocommonarches}

# Remove any duplicates output by a buggy find-debuginfo.sh.
sort -u debuginfo.filelist > debuginfo2.filelist
mv debuginfo2.filelist debuginfo.filelist

# Remove some common directories from the common package debuginfo so that we
# don't end up owning them.
exclude_common_dirs()
{
	exclude_dirs="%{_prefix}/src/debug"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug{,/%{_lib},/bin,/sbin})"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug%{_prefix}{,/%{_lib},/libexec,/bin,/sbin})"

	for d in $(echo $exclude_dirs | sed 's/ /\n/g'); do
		sed -i "\|^%%dir $d/\?$|d" $1
	done
}

%ifarch %{debuginfocommonarches}
exclude_common_dirs debuginfocommon.filelist
%endif
exclude_common_dirs debuginfo.filelist

%endif # 0%%{?_enable_debug_packages}

%if %{with docs}
# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%endif

%ifarch %{auxarches}

# Delete files that we do not intended to ship with the auxarch.
echo Cutting down the list of unpackaged files
sed -e '/%%dir/d;/%%config/d;/%%verify/d;s/%%lang([^)]*) //;s#^/*##' \
	common.filelist devel.filelist static.filelist headers.filelist \
	utils.filelist nscd.filelist \
%ifarch %{debuginfocommonarches}
	debuginfocommon.filelist \
%endif
	| (cd $RPM_BUILD_ROOT; xargs --no-run-if-empty rm -f 2> /dev/null || :)

%else

mkdir -p $RPM_BUILD_ROOT/var/{db,run}/nscd
touch $RPM_BUILD_ROOT/var/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT/var/run/nscd/{socket,nscd.pid}

%endif # %%{auxarches}

%ifnarch %{auxarches}
truncate -s 0 $RPM_BUILD_ROOT/%{_prefix}/lib/locale/locale-archive
%endif

mkdir -p $RPM_BUILD_ROOT/var/cache/ldconfig
truncate -s 0 $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

# Clean up languages we don't support on amzn2
for lang in agr_PE bi_VU hif_FJ sm_WS to_TO tpi_PG; do
    rm -rf ${RPM_BUILD_ROOT}/usr/lib/locale/${lang}
done

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

# Run the glibc tests. If any tests fail to build we exit %%check with an error
# of 1, otherwise we print the test failure list and the failed test output
# and exit with 0. In the future we want to compare against a baseline and
# exit with 1 if the results deviate from the baseline.
run_tests () {
	truncate -s 0 check.log
	tail -f check.log &
	tailpid=$!
	# Run the make a sub-shell (to avoid %%check failing if make fails)
	# but capture the status for use later. We use the normal sub-shell
	# trick of printing the status. The actual result of the sub-shell
	# is the successful execution of the echo.
	status=$(set +e
		 make %{?_smp_mflags} check %{silentrules} > check.log 2>&1
		 status=$?
		 echo $status)
	# Wait for the tail to catch up with the output and then kill it.
	sleep 10
	kill $tailpid
	# Print the header, so we can find it, but skip the error printing
	# if there aren't any failrues.
	echo ===================FAILED TESTS=====================
	if [ $status -ne 0 ]; then
		# We are not running with `-k`, therefore a test build failure
		# terminates the test run and that terminates %%check with an
		# error which terminates the build. We want this behaviour to
		# ensure that all tests build, and all tests run.
		# If the test result summary is not present it means one of
		# tests failed to build.
		if ! grep 'Summary of test results:' check.log; then
			echo "FAIL: Some glibc tests failed to build."
			exit 1
		fi

		# Print out information about all of the failed tests.
		grep -e ^FAIL -e ^ERROR tests.sum \
			| awk '{print $2}' \
			| while read testcase;
		do
			echo "$testcase"
			cat $testcase.out
			echo -------------------------
		done
	fi

	# If the crypt-glibc test suite fails, something is completely
	# broken, so fail the build in this case.
	make %{?_smp_mflags} subdirs=crypt-glibc check %{silentrules}

	# Unconditonally dump differences in the system call list.
	echo "* System call consistency checks:"
	cat misc/tst-syscall-list.out
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================
##############################################################################
# - Test the default runtime.
# 	- Power 620 / 970 ISA for 64-bit POWER BE.
#	- POWER8 for 64-bit POWER LE.
#	- ??? for 64-bit x86_64
#	- ??? for 32-bit x86
#	- ??? for 64-bit AArch64
#	- ??? for 32-bit ARM
#	- zEC12 for 64-bit s390x
#	- ??? for 32-bit s390
##############################################################################
pushd build-%{target}
run_tests
popd

%if %{buildxen}
echo ====================TESTING -mno-tls-direct-seg-refs=============
##############################################################################
# - Test the xen runtimes (nosegneg).
##############################################################################
pushd build-%{target}-nosegneg
run_tests
popd
%endif

%if %{buildpower6}
echo ====================TESTING -mcpu=power6=============
##############################################################################
# - Test the 64-bit POWER6 BE runtimes.
##############################################################################
pushd build-%{target}-power6
if [ -d ../power6emul ]; then
    export LD_PRELOAD=`cd ../power6emul; pwd`/\$LIB/power6emul.so
fi
run_tests
popd
%endif

%if %{buildpower7}
echo ====================TESTING -mcpu=power7=============
##############################################################################
# - Test the 64-bit POWER7 BE runtimes.
##############################################################################
pushd build-%{target}-power7
run_tests
popd
%endif

%if %{buildpower8}
echo ====================TESTING -mcpu=power8=============
##############################################################################
# - Test the 64-bit POWER8 BE runtimes.
##############################################################################
pushd build-%{target}-power8
run_tests
popd
%endif

echo ====================TESTING DETAILS=================
for i in `sed -n 's|^.*\*\*\* \[\([^]]*\.out\)\].*$|\1|p' build-*-linux*/check.log`; do
  echo =====$i=====
  cat $i || :
  echo ============
done
echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

# Finally, check if valgrind runs with the new glibc.
# We want to fail building if valgrind is not able to run with this glibc so
# that we can then coordinate with valgrind to get it fixed before we update
# glibc.
pushd build-%{target}

# Show the auxiliary vector as seen by the new library
# (even if we do not perform the valgrind test).
LD_SHOW_AUXV=1 elf/ld.so --library-path .:elf:nptl:dlfcn /bin/true

%if %{with valgrind}
elf/ld.so --library-path .:elf:nptl:dlfcn \
	/usr/bin/valgrind --error-exitcode=1 \
	elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/true
%endif
popd

%endif # %%{run_glibc_tests}

# We don't need to worry about the kernel running on
# the build hosts
##pre -p <lua>
#-- Check that the running kernel is new enough
#required = '%{enablekernel}'
#rel = posix.uname("%r")
#if rpm.vercmp(rel, required) < 0 then
#  error("FATAL: kernel too old", 0)
#end

%post -p %{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

%postun -p /sbin/ldconfig

%posttrans all-langpacks -e -p <lua>
-- If at the end of the transaction we are still installed
-- (have a template of non-zero size), then we rebuild the
-- locale cache (locale-archive) from the pre-populated
-- locale cache (locale-archive.tmpl) i.e. template.
if posix.stat("%{_prefix}/lib/locale/locale-archive.tmpl", "size") > 0 then
  pid = posix.fork()
  if pid == 0 then
    posix.exec("%{_prefix}/sbin/build-locale-archive", "--install-langs", "%%{_install_langs}")
  elseif pid > 0 then
    posix.wait(pid)
  end
end

%postun all-langpacks -p <lua>
-- In the postun we always remove the locale cache.
-- We are being uninstalled and if this is an upgrade
-- then the new packages template will be used to
-- recreate a new copy of the cache.
os.remove("%{_prefix}/lib/locale/locale-archive")

%if %{with docs}
%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
%endif

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%if %{with docs}
%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
fi
%endif

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

%pre -n nscd
getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
getent passwd nscd >/dev/null ||
  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
		    -c "NSCD Daemon" -u 28 -g nscd nscd

%post -n nscd
%systemd_post nscd.service

%preun -n nscd
%systemd_preun nscd.service

%postun -n nscd
if test $1 = 0; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart nscd.service

%if %{xenpackage}
%post xen -p /sbin/ldconfig
%postun xen -p /sbin/ldconfig
%endif

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

%files -f rpm.filelist
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/audit
%if %{buildxen} && !%{xenpackage}
%dir /%{_lib}/%{nosegneg_subdir_base}
%dir /%{_lib}/%{nosegneg_subdir}
%endif
%if %{buildpower6}
%dir /%{_lib}/power6
%dir /%{_lib}/power6x
%endif
%if %{buildpower7}
%dir /%{_lib}/power7
%endif
%if %{buildpower8}
%dir /%{_lib}/power8
%endif
%ifarch s390x
/lib/ld64.so.1
%endif
%ifarch armv7hl armv7hnl
/lib/ld-linux.so.3
%endif
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_libdir}/gconv
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/gai.conf
%doc README NEWS INSTALL BUGS CONFORMANCE elf/rtld-debugger-interface.txt
# If rpm doesn't support %%license, then use %%doc instead.
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB LICENSES

%if %{xenpackage}
%files -f nosegneg.filelist xen
%defattr(-,root,root)
%dir /%{_lib}/%{nosegneg_subdir_base}
%dir /%{_lib}/%{nosegneg_subdir}
%endif

%ifnarch %{auxarches}
%files -f common.filelist common
%defattr(-,root,root)
%dir %{_prefix}/lib/locale
%dir %{_prefix}/lib/locale/C.utf8
%{_prefix}/lib/locale/C.utf8/*
%dir %attr(755,root,root) /etc/default
%verify(not md5 size mtime) %config(noreplace) /etc/default/nss
%doc documentation/README.timezone
%doc documentation/gai.conf

%files all-langpacks
%attr(0644,root,root) %verify(not md5 size mtime) %{_prefix}/lib/locale/locale-archive.tmpl
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/lib/locale/locale-archive

%files locale-source
%defattr(-,root,root)
%dir %{_prefix}/share/i18n/locales
%{_prefix}/share/i18n/locales/*
%dir %{_prefix}/share/i18n/charmaps
%{_prefix}/share/i18n/charmaps/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f static.filelist static
%defattr(-,root,root)

%files -f headers.filelist headers
%defattr(-,root,root)

%files -f utils.filelist utils
%defattr(-,root,root)

%files -f nscd.filelist -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
/lib/systemd/system/nscd.service
/lib/systemd/system/nscd.socket
%{_tmpfilesdir}/nscd.conf
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
%ghost %config(missingok,noreplace) /etc/sysconfig/nscd
%endif

%files -f nss_db.filelist -n nss_db
/var/db/Makefile
%files -f nss_nis.filelist -n nss_nis
%files -f nss_hesiod.filelist -n nss_hesiod
%doc hesiod/README.hesiod
%files -f nss-devel.filelist nss-devel

%files -f libcrypt.filelist -n libcrypt
%doc documentation/README.ufc-crypt
%ghost /%{_lib}/libcrypt.so.1
%if %{without bootstrap}
%files -f libcrypt-nss.filelist -n libcrypt-nss
%ghost /%{_lib}/libcrypt.so.1
%endif

%if 0%{?_enable_debug_packages}
%files debuginfo -f debuginfo.filelist
%defattr(-,root,root)
%ifarch %{debuginfocommonarches}
%ifnarch %{auxarches}
%files debuginfo-common -f debuginfocommon.filelist
%defattr(-,root,root)
%endif
%endif
%endif

%if %{with benchtests}
%files benchtests -f benchtests.filelist
%defattr(-,root,root)
%endif

%changelog
* Tue May 19 2020 Anchal Agarwal <anchalag@amazon.com> - 2.26-35
- Add -moutline-atomic to the aarch64 BuildFlags

* Fri Jan 17 2020 Frederick Lefebvre <fredlef@amazon.com> - 2.26-34
- Rollback fix for CVE-2016-10739

* Mon Oct 28 2019 Frederick Lefebvre <fredlef@amazon.com> - 2.26-33
- CVE-2016-10739: getaddrinfo: Fully parse IPv4 address strings [BZ #20018]
- resolv: Do not send queries for non-host-names in nss_dns [BZ#24112]

* Thu Oct  3 2019 Anchal Agarwal <anchalag@amazon.com> - 2.26-32
- AArch64-Optimized-memcmp.patch
- aarch64-Use-the-L-macro-for-labels-in-memcmp.patch
- aarch64-Optimized-memcmp-for-medium-to-large-sizes.patch
- aarch64-Fix-branch-target-to-loop16.patch
- aarch64-Improve-strcmp-unaligned-performance.patch
- aarch64-strcmp-fix-misaligned-loop-jump-target.patch
- Improve-strstr-performance.patch
- Simplify-and-speedup-strstr-strcasestr-first-match.patch
- Speedup-first-memmem-match.patch
- Fix-strstr-bug-with-huge-needles-bug-23637.patch
- Add-ifunc-support-for-Ares.patch
- Improve-performance-of-strstr.patch
- Improve-performance-of-memmem.patch
- Mark-lazy-tlsdesc-helper-functions-unused-to-avoid-w.patch
- aarch64-Disable-lazy-symbol-binding-of-TLSDESC.patch
- aarch64-Remove-barriers-from-TLS-descriptor-function.patch
- arm-remove-prelinker-support-for-R_ARM_TLS_DESC.patch
- arm-Disable-lazy-initialization-of-tlsdesc-entries.patch
- arm-Remove-lazy-tlsdesc-initialization-related-code.patch
- aarch64-optimize-_dl_tlsdesc_dynamic-fast-path.patch
- aarch64-Use-PTR_REG-macro-to-fix-ILP32-bug-and-make-.patch
- AArch64-update-libm-test-ulps.patch
- Remove-slow-paths-from-pow.patch
- Remove-slow-paths-from-exp.patch
- Remove-slow-paths-from-log.patch
- aarch64-Improve-strncmp-for-mutually-misaligned-inpu.patch
- aarch64-strncmp-Unbreak-builds-with-old-binutils.patch
- aarch64-strncmp-Use-lsr-instead-of-mov-lsr.patch

* Wed Nov 28 2018 Florian Weimer <fweimer@redhat.com> - 2.26-32
- Auto-sync with upstream branch release/2.26/master,
  commit a0bc5dd3bed4b04814047265b3bcead7ab973b87:
- CVE-2018-19591: if_nametoindex: Fix descriptor leak (#1654000)
- libanl: proper cleanup if first helper thread creation failed (#1646381)
- x86: Fix Haswell CPU string flags (#1641980)
- resolv/tst-resolv-network.c: Additional test case (swbz#17630)
- Disable -Wrestrict for two nptl/tst-attr3.c tests
- Fix string/bug-strncat1.c build with GCC 8
- Ignore -Wrestrict for one strncat test
- Disable strncat test array-bounds warnings for GCC 8.
- Fix string/tester.c build with GCC 8.
- Fix nscd readlink argument aliasing (swbz#22446)
- nscd: Increase buffer size due to warning from ToT GCC
- Fix p_secstodate overflow handling (swbz#22463)
- timezone: pacify GCC -Wstringop-truncation
- utmp: Avoid -Wstringop-truncation warning
- Avoid use of strlen in getlogin_r (swbz#22447)
- signal: Use correct type for si_band in siginfo_t (swbz#23562)
- Fix misreported errno on preadv2/pwritev2 (swbz#23579)
- preadv2/pwritev2: Handle offset == -1 (swbz#22753)
- posix_spawn: Fix potential segmentation fault

* Mon Nov 26 2018 Florian Weimer <fweimer@redhat.com> - 2.26-31
- Do not use parallel make for building locales (#1652228)

* Wed Aug 29 2018 Florian Weimer <fweimer@redhat.com> - 2.26-30
- Auto-sync with upstream branch release/2.26/master,
  commit 174709d879a15590e00119c7f91dc2460aaf571c:
- CVE-2018-11237: Buffer overflow in mempcpy for Xeon Phi (#1581275)
- nptl: Fix waiters-after-spinning case in pthread_cond_broadcast (#1622669)
- x86: Correct index_cpu_LZCNT (swbz#23456)
- x86: Populate COMMON_CPUID_INDEX_80000001 for Intel CPUs (swbz#23459)
- stdio-common/tst-printf.c: Remove part under a non-free license (swbz#23363)
- libio: Disable vtable validation in case of interposition (swbz#23313)
- if_nametoindex: Check length of ifname before copying (swbz#22442)
- getifaddrs: Don't return ifa entries with NULL names (swbz#21812)
- time: Use _STRUCT_TIMESPEC as guard in <bits/types/struct_timespec.h>
  (swbz#23349)
- math: Fix parameter type in C++ version of iseqsig (swbz#23171)
- libio: Avoid _allocate_buffer, _free_buffer function pointers (swbz#23236)

* Mon Aug 13 2018 Carlos O'Donell <carlos@redhat.com> - 2.26-29
- Remove abort() warning in manual (#1615608)

* Fri May 18 2018 Florian Weimer <fweimer@redhat.com> - 2.26-28
- Do not run telinit u on upgrades (#1579225)
- Auto-sync with upstream branch release/2.26/master,
  commit af7519f7b35024224c163e32a89fb247b0c446fc:
- CVE-2018-11236: Fix path length overflow in realpath (#1581270, swbz#22786)
- Fix stack overflow with huge PT_NOTE segment (swbz#20419)
- Fix signed integer overflow in random_r (swbz#17343)
- i386: Fix i386 sigaction sa_restorer initialization (swbz#21269)
- nscd: Fix netgroup cache keys (swbz#22342)
- CVE-2017-18269: Fix i386 memmove issue (swbz#22644)
- Fix crash in resolver on memory allocation failure (swbz#23005)
- getlogin_r: return early when linux sentinel value is set (swbz#23024)
- resolv: Fully initialize struct mmsghdr in send_dg (swbz#23037)

* Fri Mar  2 2018 Florian Weimer <fweimer@redhat.com> - 2.26-27
- Restore unwind tables on POWER (#1550914)

* Thu Mar 01 2018 Florian Weimer <fweimer@redhat.com> - 2.26-26
- Auto-sync with upstream branch release/2.26/master,
  commit d300041c533a3d837c9f37a099bcc95466860e98:
- CVE-2018-6485, CVE-2018-6551: Fix integer overflows in internal
  memalign and malloc (#1542102, #1542119)
- powerpc: Fix syscalls during early process initialization (swbz#22685)
- math: Provide a C++ version of iseqsig (swbz#22377)
- aarch: Rewrite elf_machine_load_address using _DYNAMIC symbol
- x86-64: Properly align La_x86_64_retval to VEC_SIZE (swbz#22715)

* Wed Jan 17 2018 Florian Weimer <fweimer@redhat.com> - 2.26-25
- Build depend on python3, not python

* Mon Jan 15 2018 Florian Weimer <fweimer@redhat.com> - 2.26-24
- PTHREAD_STACK_MIN is too small on x86-64 (#1527887)
- Auto-sync with upstream branch release/2.26/master,
  commit 247c1ddd309e3f4135045eab554f3817b7d765be.

* Mon Jan 15 2018 Florian Weimer <fweimer@redhat.com> - 2.26-23
- CVE-2018-1000001: Make getcwd fail if it cannot obtain an absolute path
  (#1533837)
- CVE-2017-16997: Check for empty tokens before dynamic string token
  expansion in the dynamic linker (#1526866)
- Auto-sync with upstream branch release/2.26/master,
  commit fabef2edbc29424a8048bdd60eba1a201f95682b:
- elf: do not substitute dst in $LD_LIBRARY_PATH twice (swbz#22627)

* Mon Jan 15 2018 Florian Weimer <fweimer@redhat.com> - 2.26-22
- Add BuildRequires: cpp (for rpcgen)

* Fri Dec 22 2017 Florian Weimer <fweimer@redhat.com> - 2.26-21
- bash no longer has job control under systemd-nspawn (via mock) (#1468837)
- Auto-sync with upstream branch release/2.26/master,
  commit 069c3dd05abc91fced6e1e119e425c361ad97644:
- CVE-2017-1000409: Count in expanded path in _dl_init_path (#1524867)
- CVE-2017-1000408: Compute correct array size in _dl_init_paths (#1524867)

* Wed Dec 06 2017 Florian Weimer <fweimer@redhat.com> - 2.26-20
- Auto-sync with upstream branch release/2.26/master,
  commit 73a92363619e52c458146e903dfb9b1ba823aa40:
- malloc: Fix -Werror compilation failure with -O3 (swbz#22052)

* Wed Dec 06 2017 Florian Weimer <fweimer@redhat.com> - 2.26-19
- Auto-sync with upstream branch release/2.26/master,
  commit df8c219cb987cfe85c550efa693a1383a11e38aa:
- CVE-2017-17426: malloc: Fix integer overflow in tcache (swbz#22375)
- CVE-2017-15804: glob: Fix overflow in GLOB_TILDE unescaping (swbz#22332)
- malloc: Add single-threaded path to _int_malloc
- powerpc: Update AT_HWCAP2 bits
- malloc: Abort on heap corruption, without a backtrace (swbz#21754)
- Don't use IFUNC resolver for longjmp or system in libpthread (swbz#21041)
- powerpc: Replace lxvd2x/stxvd2x with lvx/stvx in P7's memcpy/memmove

* Sat Nov 18 2017 Florian Weimer <fweimer@redhat.com> - 2.26-18
- Auto-sync with upstream branch release/2.26/master,
  commit 2767ebd8bc34c8b632ea737296200a86f57289ad:
- crypt: Use NSPR header files in addition to NSS header files (#1489339)
- malloc: Use relaxed atomics for have_fastchunks
- malloc: Inline tcache functions
- x86-64: Regenerate libm-test-ulps for AVX512 mathvec tests

* Mon Nov 13 2017 Florian Weimer <fweimer@redhat.com> - 2.26-17
- Auto-sync with upstream branch release/2.26/master,
  commit a81c1156c1a9a6161d49b295a09a4e4cff7a88d0:
- posix: Fix improper assert in Linux posix_spawn (swbz#22273)
- posix: Do not use WNOHANG in waitpid call for Linux posix_spawn
- posix: Fix compat glob code on s390 and alpha
- posix: Consolidate Linux glob implementation
- Fix range check in do_tunable_update_val
- Let signbit use the builtin in C++ mode with gcc < 6.x (swbz#22296)
- x86-64: Don't set GLRO(dl_platform) to NULL (swbz#22299)
- x86-64: Use fxsave/xsave/xsavec in _dl_runtime_resolve (swbz#21265)

* Thu Nov  2 2017 Florian Weimer <fweimer@redhat.com> - 2.26-16
- x86: Add x86_64 to x86-64 HWCAP (#1506802)

* Sat Oct 21 2017 Florian Weimer <fweimer@redhat.com> - 2.26-15
- Auto-sync with upstream branch release/2.26/master,
  commit a76376df7c07e577a9515c3faa5dbd50bda5da07:
- CVE-2017-15670: glob: Fix one-byte overflow (#1504807)
- CVE-2017-15671: glob: Fix memory leak (#1504807)
- sysconf: Fix missing definition of UIO_MAXIOV on Linux (#1504165)
- nss_files: Avoid large buffers with many host addresses (swbz#22078)
- nss_files: Use struct scratch_buffer for gethostbyname (swbz#18023)
- aarch64: Optimized implementation of memcpy, memmove for Qualcomm Falkor

* Fri Oct 13 2017 Carlos O'Donell <carlos@redhat.com> - 2.26-14
- Disable lock elision for IBM z Series (#1499260)
- As a precaution escape all % in spec file comments.

* Mon Oct  9 2017 Florian Weimer <fweimer@redhat.com> - 2.26-13
- Move /var/db/Makefile to nss_db (#1498900)

* Sat Oct  7 2017 Carlos O'Donell <carlos@systemhalted.org> - 2.26-12
- Auto-sync with upstream release/2.26/master,
  commit d5c6dea2d5b4b5c64625c5386f6baec7bf2d89b3.
- malloc: Fix tcache leak after thread destruction (swbz#22111)
- Add C++ versions of iscanonical (swbz#22235)

* Sat Oct  7 2017 Florian Weimer <fweimer@redhat.com> - 2.26-11
- Do not flush stdio streams on abort, assertion failure (#1498880)
- Move nss_compat to the main glibc package (#1400538)

* Sun Oct 01 2017 Florian Weimer <fweimer@redhat.com> - 2.26-10
- Drop glibc-gcc-strict-overflow.patch, different workaround applied upstream.
- Auto-sync with upstream release/2.26/master,
  commit fdf58ebc60ce0eb459fd616241b52872b3571ac1:
- Fix nearbyint arithmetic moved before feholdexcept (swbz#22225)
- Avoid __MATH_TG in C++ mode with -Os for fpclassify (swbz#22146)
- Place $(elf-objpfx)sofini.os last (swbz#22051)
- __libc_dynarray_emplace_enlarge: Add missing else
- dynarray: Set errno on overflow-induced allocation failure
- resolv: __resolv_conf_attach must not free passed conf object (swbz#22096)
- resolv: Fix memory leak with OOM during resolv.conf parsing (swbz#22095)
- nss_dns: Remove dead PTR IPv4-to-IPv6 mapping code

* Sat Sep 30 2017 Florian Weimer <fweimer@redhat.com> - 2.26-9
- Add IBM858 charset (#1416405)

* Fri Sep 15 2017 Florian Weimer <fweimer@redhat.com> - 2.26-8
- Restore ARM EABI dynamic loader support (#1491974)

* Mon Sep 04 2017 Florian Weimer <fweimer@redhat.com> - 2.26-7
- Auto-sync with upstream release/2.26/master,
  commit a71a3374cd8cf53776c33994f69ec184c26f2129:
- Provide a C++ version of issignaling that does not use __MATH_TG
- Provide a C++ version of iszero that does not use __MATH_TG (swbz#21930)
- getaddrinfo: Return EAI_NODATA if gethostbyname2_r with NO_DATA (swzbz#21922)
- getaddrinfo: Fix error handling in gethosts (swbz#21915)

* Mon Aug 28 2017 Florian Weimer <fweimer@redhat.com> - 2.26-6
- Backport upstream patch for the built-in system call list (#1484729)
- Auto-sync with upstream release/2.26/master,
  commit 6043d77a47de297b62084c1c261cdada082bf09c.

* Thu Aug 24 2017 Florian Weimer <fweimer@redhat.com> - 2.26-5
- Use an architecture-independent system call list (#1484729)
- Drop glibc-fedora-include-bits-ldbl.patch (#1482105)

* Mon Aug 21 2017 Florian Weimer <fweimer@redhat.com> - 2.26-4
- Auto-sync with upstream release/2.26/master,
  commit fb9a781e9d62c5d7a1f4196915cdfb7c6db59a0c:
- assert: Support types without operator== (int) (#1483005)

* Mon Aug 21 2017 Florian Weimer <fweimer@redhat.com> - 2.26-3
- Auto-sync with upstream release/2.26/master,
  commit 5e989c36934d0f0cf13b7a53ef2fa440bce39210:
- Do not use generic selection in C++ mode
- Do not use __builtin_types_compatible_p in C++ mode (#1481205)
- powerpc: Restrict xssqrtqp operands to Vector Registers (swbz#21941)

* Wed Aug 16 2017 Florian Weimer <fweimer@redhat.com> - 2.26-2
- Disable SSE2 usage on i686 (#1471427)
- Auto-sync with upstream release/2.26/master,
  commit 2aa1a7a8f8b9b7879bc6eb1c34d1580f992c406d:
- assert: Suppress pedantic warning caused by statement expression (swbz#21242)
- malloc: Avoid optimizer warning with GCC 7 and -O3 (#1470060)
- nss: Call __resolv_context_put before early return in get*_r (swbz#21932)
- x86-64: Use _dl_runtime_resolve_opt only with AVX512F (swbz#21871)
- getaddrinfo: Release resolver context on error in gethosts (swbz#21885)

* Thu Aug 03 2017 Carlos O'Donell <carlos@systemhalted.org> - 2.26-1
- Update to released glibc 2.26.
- Auto-sync with upstream master,
  commit 2aad4b04ad7b17a2e6b0e66d2cb4bc559376617b.
- getaddrinfo: Release resolver context on error in gethosts (swbz#21885)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.90-30.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-30
- Auto-sync with upstream master,
  commit 5920a4a624b1f4db310d1c44997b640e2a4653e5:
- mutex: Fix robust mutex lock acquire (swbz#21778)

* Fri Jul 28 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-29
- Auto-sync with upstream master,
  commit d95fcb2df478efbf4f8537ba898374043ac4561f:
- rwlock: Fix explicit hand-over (swbz#21298)
- tunables: Use direct syscall for access (swbz#21744)
- Avoid accessing corrupted stack from __stack_chk_fail (swbz#21752)
- Remove extra semicolons in struct pthread_mutex (swbz#21804)
- grp: Fix cast-after-dereference (another big-endian group merge issue)
- S390: fix sys/ptrace.h to make it includible again after asm/ptrace.h
- Don't add stack_chk_fail_local.o to libc.a (swbz#21740)
- i386: Test memmove_chk and memset_chk only in libc.so (swbz#21741)
- Add new locales az_IR, mai_NP (swbz#14172)
- Various locale improvements

* Thu Jul 27 2017 Carlos O'Donell <codonell@redhat.com> - 2.25.90-28
- Adjust to new rpm debuginfo generation (#1475009).

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.90-27.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-27
- Auto-sync with upstream master,
  commit 00d7a3777369bac3d8d44152dde2bb7381984ef6:
- aarch64: Fix out of bound array access in _dl_hwcap_string

* Mon Jul 17 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-26
- Drop glibc-rh1467518.patch in favor of upstream patch (#1467518)
- Auto-sync with upstream master,
  commit 91ac3a7d8474480685632cd25f844d3154c69fdf:
- Fix pointer alignment in NSS group merge result construction (#1471985)
- Various locale fixes

* Fri Jul 14 2017 Carlos O'Donell <carlos@systemhalted.org> - 2.25.90-25
- armv7hl: Drop 32-bit ARM build fix, already in upstream master.
- s390x: Apply glibc fix again, removing PTRACE_GETREGS etc. (#1469536).
- Auto-sync with upstream master,
  commit de895ddcd7fc45caeeeb0ae312311b8bd31d82c5:
- Added Fiji Hindi language locale for Fiji (swbz#21694).
- Added yesstr/nostr for nds_DE and nds_NL (swbz#21756).
- Added yesstr and nostr for Tigrinya (swbz#21759).
- Fix LC_MESSAGES and LC_ADDRESS for anp_IN (swbz#21760).
- Added yesstr/nostr and fix yesexpr for pap_AW and pap_CW (swbz#21757).
- Added Tongan language locale for Tonga (swbz#21728).
- [ARM] Fix ld.so crash when built using Binutils 2.29.
- Added yesstr and nostr for aa_ET (swbz#21768).
- New locale for bi_VU (swbz#21767).
- Disable single thread optimization for open_memstream

* Wed Jul 12 2017 Carlos O'Donell <carlos@redhat.com> - 2.25.90-24
- Fix IFUNC crash in early startup for ppc64le static binaries (#1467518).
- Enable building with BIND_NOW on ppc64le (#1467518).
- Fix 32-bit ARM builds in presence of new binutils.

* Wed Jul 12 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-23
- malloc: Tell GCC optimizers about MAX_FAST_SIZE in _int_malloc (#1470060)
- Auto-sync with upstream master,
  commit 30200427a99e5ddac9bad08599418d44d54aa9aa:
- Add per-thread cache to malloc
- Add Samoan language locale for Samoa
- Add Awajún / Aguaruna locale for Peru
- CVE-2010-3192: Avoid backtrace from __stack_chk_fail (swbz#12189)
- Add preadv2, writev2 RWF_NOWAIT flag (swbz#21738)
- Fix abday strings for ar_JO/ar_LB/ar_SY locales (swbz#21749)
- Fix abday strings for ar_SA locale (swbz#21748, swbz#19066)
- Set data_fmt for da_DK locale (swbz#17297)
- Add yesstr and nostr for the zh_HK locale (swbz#21733)
- Fix abday strings for the ksIN@devanagari locale (swbz#21743)
- Do not include _dl_resolv_conflicts in libc.a (swbz#21742)
- Test __memmove_chk, __memset_chk only in libc.so (swbz#21741)
- Add iI and eE to  yesexpr and noexpr respectively for ts_ZA locale
- Add yesstr/nostr for kw_GB locale (swbz#21734)
- Add yesstr and nostr for the ts_ZA locale (swbz#21727)
- Fix LC_NAME for hi_IN locale (swbz#21729)
- Add yesstr and nostr for the xh_ZA locale (swbz#21724)
- Add yesstr and nostr for the zh_CN locale (swbz#21723)
- Fix full weekday names for the ks_IN@devanagari locale (swbz#21721)
- Various fixes to Arabic locales after CLDR import 

* Tue Jul 11 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-22
- Reinstantiate stack_t cleanup (#1468904)
- s390x: Restore PTRACE_GETREGS etc. to get GCC to build (#1469536)

* Sun Jul  9 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-21
- Back out stack_t cleanup (#1468904)

* Thu Jul 06 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-20
- Auto-sync with upstream master,
  commit 031e519c95c069abe4e4c7c59e2b4b67efccdee5:
- x86-64: Align the stack in __tls_get_addr (#1440287)
- Add Tok-Pisin (tpi_PG) locale.
- Add missing yesstr/nostr for Pashto locale (swbz#21711)
- Add missing yesstr/nostr for Breton locale (swbz#21706)
- Single threaded stdio optimization
- sysconf: Use conservative default for _SC_NPROCESSORS_ONLN (swbz#21542)

* Tue Jul 04 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-19
- Auto-sync with upstream master,
  commit 4446a885f3aeb3a33b95c72bae1f115bed77f0cb.

* Tue Jul 04 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-18
- Auto-sync with upstream master,
  commit 89f6307c5d270ed4f11cee373031fa9f2222f2b9.

* Tue Jul  4 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-17
- Disable building with BIND_NOW on ppc64le (#1467518)

* Mon Jul 03 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-16
- Auto-sync with upstream master,
  commit e237357a5a0559dee92261f1914d1fa2cd43a1a8:
- Support an arbitrary number of search domains in the stub resolver (#168253)
- Detect and apply /etc/resolv.conf changes in libresolv (#1374239)
- Increase malloc alignment on i386 to 16 (swbz#21120)
- Make RES_ROTATE start with a random name server (swbz#19570)
- Fix tgmath.h totalorder, totalordermag return type (swbz#21687)
- Miscellaneous sys/ucontext.h namespace fixes (swbz#21457)
- Rename struct ucontext tag (swbz#21457)
- Call exit system call directly in clone (swbz#21512)
- powerpc64le: Enable float128
- getaddrinfo: Merge IPv6 addresses and IPv4 addresses (swbz#21295)
- Avoid .symver on common symbols (swbz#21666)
- inet_pton: Reject IPv6 addresses with many leading zeros (swbz#16637)

* Fri Jun 23 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-15
- Auto-sync with upstream master,
  commit 3ec7c02cc3e922b9364dc8cfd1d4546671b91003, fixing:
- memcmp-avx2-movbe.S incorrect results for lengths 2/3 (#1464403)

* Fri Jun 23 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-14
- Auto-sync with upstream master,
  commit 12f50337ae80672c393c2317d471d097ad92c492, changing:
- localedata: fur_IT: Fix spelling of Wednesday (Miercus)
- Update to Unicode 10.0.0
- inet: __inet6_scopeid_pton should accept node-local addresses (swbz#21657)

* Fri Jun 23 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-13
- Reenable valgrind on aarch64

* Thu Jun 22 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-12
- Log auxiliary vector during build

* Thu Jun 22 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-11
- Auto-sync with upstream master,
  commit 0a47d031e44f15236bcef8aeba80e737bd013c6f.

* Thu Jun 22 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-10
- Disable valgrind on aarch64

* Wed Jun 21 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-9
- Drop historic aarch64 TLS patches
- Drop workaround for GCC PR69537
- Auto-sync with upstream master,
  commit 9649350d2ee47fae00794d57e2526aa5d67d900e.

* Wed Jun 21 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-8
- Adjust build requirements for gcc, binutils, kernel-headers.
- Auto-sync with upstream master,
  commit 43e0ac24c836eed627a75ca932eb7e64698407c6, changing:
- Remove <xlocale.h>

* Mon Jun 19 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-7
- Drop glibc-Disable-buf-NULL-in-login-tst-ptsname.c, applied upstream.
- Auto-sync with upstream master,
  commit 37e9dc814636915afb88d0779e5e897e90e7b8c0, fixing:
- CVE-2017-1000366: Avoid large allocas in the dynamic linker (#1462820)
- wait3 namespace (swbz#21625)
- S390: Sync ptrace.h with kernel (swbz#21539)
- Another x86 sys/ucontext.h namespace issue (swbz#21457)
- siginterrupt namespace (swbz#21597)
- Signal stack namespace (swbz#21584)
- Define struct rusage in sys/wait.h when required (swbz#21575)
- S390: Fix build with gcc configured with --enable-default-pie (swbz#21537)
- Update timezone code from tzcode 2017b
- nptl: Invert the mmap/mprotect logic on allocated stacks (swbz#18988)
- PowerPC64 ELFv2 PPC64_OPT_LOCALENTRY
- Make copy of <bits/std_abs.h> from GCC (swbz#21573)
- localedata: ce_RU: update weekdays from CLDR (swbz#21207)
- localedata: Remove trailing spaces (swbz#20275)
- XPG4 bsd_signal namespace (swbz#21552)
- Correct collation rules for Malayalam (swbz#19922, swbz#19919)
- waitid namespace (swbz#21561)
- Condition signal.h inclusion in sys/wait.h (swbz#21560)
- ld.so: Consolidate 2 strtouls into _dl_strtoul (swbz#21528)
- tst-timezone race (swbz#14096)
- Define SIG_HOLD for XPG4 (swbz#21538)
- struct sigaltstack namespace (swbz#21517)
- sigevent namespace (swbz#21543)
- Add shim header for bits/syscall.h (swbz#21514)
- namespace issues in sys/ucontext.h (swbz#21457)
- posix: Implement preadv2 and pwritev2
- Various float128 and tunables improvements

* Tue Jun 06 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.25.90-6
- Reduce libcrypt-nss dependency to 'Suggests:'

* Wed May 31 2017 Arjun Shankar <arjun.is@lostca.se> - 2.25.90-5
- Auto-sync with upstream master,
  commit cfa9bb61cd09c40def96f042a3123ec0093c4ad0.
- Fix sys/ucontext.h namespace from signal.h etc. inclusion (swbz#21457)
- Fix sigstack namespace (swbz#21511)

* Wed May 31 2017 Arjun Shankar <arjun.is@lostca.se> - 2.25.90-4
- Disable the NULL buffer test in login/tst-ptsname.c. It leads to a build
  failure during 'make check'. A permanent solution is being discussed
  upstream.

* Tue May 23 2017 Arjun Shankar <arjun.is@lostca.se> - 2.25.90-3
- Auto-sync with upstream master,
  commit 231a59ce2c5719d2d77752c21092960e28837b4a.
- Add el_GR@euro support (swbz#20686)
- Set dl_platform and dl_hwcap from CPU features (swbz#21391)
- Use __glibc_reserved convention in mcontext, sigcontext (swbz#21457)
- Fix signal.h bsd_signal namespace (swbz#21445)
- Fix network headers stdint.h namespace (swbz#21455)
- resolv: Use RES_DFLRETRY consistently (swbz#21474)
- Condition some sys/ucontext.h contents on __USE_MISC (swbz#21457)
- Consolidate Linux read syscall (swbz#21428)
- fork: Remove bogus parent PID assertions (swbz#21386)
- Reduce value of LD_HWCAP_MASK for tst-env-setuid test case (swbz#21502)
- libio: Avoid dup already opened file descriptor (swbz#21393)

* Mon May 01 2017 Carlos O'Donell <carlos@systemhalted.org> - 2.25.90-2
- Auto-sync with upstream master,
  commit 25e39b4229fb365a605dc4c8f5d6426a77bc08a6.
- logbl for POWER7 return incorrect results (swbz#21280)
- sys/socket.h uio.h namespace (swbz#21426)
- Support POSIX_SPAWN_SETSID (swbz#21340)
- Document how to provide a malloc replacement (swbz#20424)
- Verify that all internal sockets opened with SOCK_CLOEXEC (swbz#15722)
- Use AVX2 memcpy/memset on Skylake server (swbz#21396)
- unwind-dw2-fde deadlock when using AddressSanitizer (swbz#21357)
- resolv: Reduce advertised EDNS0 buffer size to guard against
  fragmentation attacks (swbz#21361)
- mmap64 silently truncates large offset values (swbz#21270)
- _dl_map_segments does not test for __mprotect failures consistently
  (swbz#20831)

* Thu Mar 02 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-1
- Switch back to upstream master branch.
- Drop Unicode 9 patch, merged upstream.
- Auto-sync with upstream master,
  commit a10e9c4e53fc652b79abf838f7f837589d2c84db, fixing:
- Build all DSOs with BIND_NOW (#1406731)

* Wed Mar  1 2017 Jakub Hrozek <jhrozek@redhat.com> - 2.25-3
- NSS: Prefer sss service for passwd, group databases (#1427646)

* Tue Feb 28 2017 Florian Weimer <fweimer@redhat.com> - 2.25-2
- Auto-sync with upstream release/2.25/master,
  commit 93cf93e06ce123439e41d3d62790601c313134cb, fixing:
- sunrpc: Improvements for UDP client timeout handling (#1346406)
- sunrpc: Avoid use-after-free read access in clntudp_call (swbz#21115)
- Fix getting tunable values on big-endian (swbz#21109)

* Wed Feb 08 2017 Carlos O'Donell <carlos@redhat.com> - 2.25-1
- Update to final released glibc 2.25.
