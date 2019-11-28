%define _buildid .178

# XXX: this has to be compiled with gcc48, choose with:
# sudo update-alternatives --config gcc

%bcond_with systemd
%bcond_with usrmerge

%define glibcsrcdir glibc-2.17-c758a686
%define glibcversion 2.17
%define glibcrelease 292
##############################################################################
# We support the following options:
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
%bcond_with testsuite
# Default: Always build the benchtests.
%bcond_with benchtests
# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Enable using -Werror
%bcond_without werror
# Default: Always build documentation.
%bcond_with docs
# Default: Don't run valgrind tests
%bcond_with valgrind

# Run a valgrind smoke test to ensure that the release is compatible and
# doesn't any new feature that might cause valgrind to abort.
%if %{with valgrind}
%ifarch s390
# There is no valgrind support for 31-bit s390.
%undefine with_valgrind
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
%define xenarches i686 athlon
##############################################################################
# We build a special package for Xen that includes TLS support with
# no negative segment offsets for use with Xen guests. This is
# purely an optimization for increased performance on those arches.
%ifarch %{xenarches}
%define buildxen 1
%define xenpackage 0
%else
%define buildxen 0
%define xenpackage 0
%endif
##############################################################################
# We support 32-bit and 64-bit POWER with the following runtimes:
# 64-bit BE:
# - POWER7 (default)
# DISABLED - POWER8 (enabled via AT_PLATFORM)
#            See: https://projects.engineering.redhat.com/browse/RCMPROJ-5774
#	     The ppc64 builders still have POWER7 hardware.
# 64-bit LE:
# - POWER8 LE (default)
# 32-bit BE:
# - POWER7 (default)
#
# The POWER5 and POWER6 runtimes are now deprecated and no longer provided
# or supported. This means that RHEL7 BE will only run on POWER7 or newer
# hardware, and LE will only run on POWER8 or newer hardware.
#
%ifarch ppc ppc64
# Build the additional runtimes for 32-bit and 64-bit BE POWER.
%define buildpower6 0
# Disabled - %%define buildpower8 1 - See note above.
%define buildpower8 0
%else
# No additional runtimes for ppc64le or ppc64p7, just the default.
%define buildpower6 0
%define buildpower8 0
%endif

##############################################################################
# We build librtkaio for all rtkaioarches. The library is installed into
# a distinct subdirectory in the lib dir. This define enables the rtkaio
# add-on during the build. Upstream does not have rtkaio and it is provided
# strictly as part of our builds.
%define rtkaioarches %{ix86} x86_64 ppc %{power64} s390 s390x
##############################################################################
# Any architecture/kernel combination that supports running 32-bit and 64-bit
# code in userspace is considered a biarch arch.
%define biarcharches %{ix86} x86_64 ppc %{power64} s390 s390x
##############################################################################
# If the debug information is split into two packages, the core debuginfo
# pacakge and the common debuginfo package then the arch should be listed
# here. If the arch is not listed here then a single core debuginfo package
# will be created for the architecture.
%define debuginfocommonarches %{biarcharches} alpha alphaev6
##############################################################################
# If the architecture has multiarch support in glibc then it should be listed
# here to enable support in the build. Multiarch support is a single library
# with implementations of certain functions for multiple architectures. The
# most optimal function is selected at runtime based on the hardware that is
# detected by glibc. The underlying support for function selection and
# execution is provided by STT_GNU_IFUNC.
%define multiarcharches ppc %{power64} %{ix86} x86_64 %{sparc} s390 s390x
##############################################################################
# If the architecture has elision support in glibc then it should be listed
# here to enable elision for default pthread mutexes and rwlocks. The elision
# is not enabled automatically and each process has to opt-in to elision via
# the environment variable RHEL_GLIBC_TUNABLES by setting it to enabled e.g.
# RHEL_GLIBC_TUNABLES="glibc.elision.enable=1".
%define elisionarches %{power64}
##############################################################################
# Add -s for a less verbose build output.
%define silentrules PARALLELMFLAGS=-s
##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: glibc
Version: %{glibcversion}
Release: %{glibcrelease}%{?_buildid}%{?dist}
# GPLv2+ is used in a bunch of programs, LGPLv2+ is used for libraries.
# Things that are linked directly into dynamically linked programs
# and shared libraries (e.g. crt files, lib*_nonshared.a) have an additional
# exception which allows linking it into any kind of programs or shared
# libraries without restrictions.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System Environment/Libraries
ExclusiveArch: i686 x86_64

URL: http://www.gnu.org/software/glibc/
# We do not use usptream source tarballs as the start place for our package.
# We should use upstream source tarballs for official releases though and
# it will look like this:
# Source0: http://ftp.gnu.org/gnu/glibc/%%{glibcsrcdir}.tar.gz
# Source1: %%{glibcsrcdir}-releng.tar.gz
# TODO:
# The Source1 URL will never reference an upstream URL. In fact the plan
# should be to merge the entire release engineering tarball into upstream
# instead of keeping it around as a large dump of files. Distro specific
# changes should then be a very very small patch set.
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.gz
Source1: %{glibcsrcdir}-releng.tar.gz
Source2: verify.md5

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

Patch0002: glibc-fedora-regcomp-sw11561.patch
Patch0003: glibc-fedora-ldd.patch

Patch0004: glibc-fedora-ppc-unwind.patch

# Build info files in the source tree, then move to the build
# tree so that they're identical for multilib builds
Patch0005: glibc-rh825061.patch

# Horrible hack, never to be upstreamed.  Can go away once the world
# has been rebuilt to use the new ld.so path.
Patch0006: glibc-arm-hardfloat-3.patch

# Needs to be sent upstream
Patch0008: glibc-fedora-getrlimit-PLT.patch
Patch0009: glibc-fedora-include-bits-ldbl.patch

# stap, needs to be sent upstream
Patch0010: glibc-stap-libm.patch

# Needs to be sent upstream
Patch0029: glibc-rh841318.patch

# All these were from the glibc-fedora.patch mega-patch and need another
# round of reviewing.  Ideally they'll either be submitted upstream or
# dropped.
Patch0012: glibc-fedora-linux-tcsetattr.patch
Patch0014: glibc-fedora-nptl-linklibc.patch
Patch0015: glibc-fedora-localedef.patch
Patch0016: glibc-fedora-i386-tls-direct-seg-refs.patch
Patch0017: glibc-fedora-gai-canonical.patch
Patch0019: glibc-fedora-nis-rh188246.patch
Patch0020: glibc-fedora-manual-dircategory.patch
Patch0024: glibc-fedora-locarchive.patch
Patch0025: glibc-fedora-streams-rh436349.patch
Patch0028: glibc-fedora-localedata-rh61908.patch
Patch0030: glibc-fedora-uname-getrlimit.patch
Patch0031: glibc-fedora-__libc_multiple_libcs.patch
Patch0032: glibc-fedora-elf-rh737223.patch
Patch0034: glibc-fedora-elf-init-hidden_undef.patch

# Needs to be sent upstream
Patch0035: glibc-rh911307.patch
Patch0036: glibc-rh892777.patch
Patch0037: glibc-rh952799.patch
Patch0038: glibc-rh959034.patch
Patch0039: glibc-rh970791.patch

# GLIBC_PTHREAD_STACKSIZE - Needs to be upstreamed on top of the future
# tunables framework.
Patch0040: glibc-rh990388.patch
Patch0041: glibc-rh990388-2.patch
Patch0042: glibc-rh990388-3.patch
Patch0043: glibc-rh990388-4.patch

# Remove non-ELF support in rtkaio
Patch0044: glibc-rh731833-rtkaio.patch
Patch0045: glibc-rh731833-rtkaio-2.patch

# Add -fstack-protector-strong support.
Patch0048: glibc-rh1070806.patch

Patch0060: glibc-aa64-commonpagesize-64k.patch

Patch0061: glibc-rh1133812-1.patch

Patch0062: glibc-cs-path.patch

# Use __int128_t in link.h to support older compilers.
Patch0063: glibc-rh1120490-int128.patch

# Workaround to extend DTV_SURPLUS. Not to go upstream.
Patch0066: glibc-rh1227699.patch

# CVE-2015-7547
Patch0067: glibc-rh1296031.patch

# releng patch from Fedora
Patch0068: glibc-rh1349982.patch

# These changes were brought forward from RHEL 6 for compatibility
Patch0069: glibc-rh1448107.patch
##############################################################################
#
# Patches from upstream
#
##############################################################################

Patch1000: glibc-rh905877.patch
Patch1001: glibc-rh958652.patch
Patch1002: glibc-rh977870.patch
Patch1003: glibc-rh977872.patch
Patch1004: glibc-rh977874.patch
Patch1005: glibc-rh977875.patch
Patch1006: glibc-rh977887.patch
Patch1007: glibc-rh977887-2.patch
Patch1008: glibc-rh980323.patch
Patch1009: glibc-rh984828.patch
Patch1010: glibc-rh966633.patch

# Additional backports from upstream to fix problems caused by
# -ftree-loop-distribute-patterns
Patch1011: glibc-rh911307-2.patch
Patch1012: glibc-rh911307-3.patch

# PowerPC backports
Patch1013: glibc-rh977110.patch
Patch1014: glibc-rh977110-2.patch

# HWCAPS2 support and POWER8 additions to it
Patch1015: glibc-rh731833-hwcap.patch
Patch1016: glibc-rh731833-hwcap-2.patch
Patch1017: glibc-rh731833-hwcap-3.patch
Patch1018: glibc-rh731833-hwcap-4.patch
Patch1019: glibc-rh731833-hwcap-5.patch

# Miscellaneous fixes for PowerPC
Patch1020: glibc-rh731833-misc.patch
Patch1021: glibc-rh731833-misc-2.patch
Patch1022: glibc-rh731833-misc-3.patch
Patch1023: glibc-rh731833-misc-4.patch
Patch1024: glibc-rh731833-misc-5.patch
Patch1025: glibc-rh731833-misc-6.patch

# Math fixes for PowerPC
Patch1026: glibc-rh731833-libm.patch
Patch1027: glibc-rh731833-libm-2.patch
Patch1028: glibc-rh731833-libm-3.patch
Patch1029: glibc-rh731833-libm-4.patch
Patch1030: glibc-rh731833-libm-5.patch
Patch1031: glibc-rh731833-libm-6.patch
Patch1032: glibc-rh731833-libm-7.patch

Patch1034: glibc-rh996227.patch
Patch1035: glibc-rh1000923.patch
Patch1036: glibc-rh884008.patch
Patch1037: glibc-rh1008298.patch
# Add support for rtlddir distinct from slibdir.
Patch1038: glibc-rh950093.patch
Patch1039: glibc-rh1025612.patch
Patch1040: glibc-rh1032435.patch
Patch1041: glibc-rh1020637.patch
# Power value increase for MINSIGSTKSZ and SIGSTKSZ.
Patch1042: glibc-rh1028652.patch

# Upstream BZ 15601
Patch1043: glibc-rh1039496.patch

Patch1044: glibc-rh1047983.patch

Patch1045: glibc-rh1064945.patch

# Patch to update the manual to say SunRPC AUTH_DES will prevent FIPS 140-2
# compliance.
Patch1046: glibc-rh971589.patch
# Patch to update translation for stale file handle error.
# Only libc.pot part is sent upstream, the only valid part
# since upstream translations are done by the TP.
Patch1047: glibc-rh981332.patch

# Upstream BZ 9954
Patch1048: glibc-rh739743.patch

# Upstream BZ 13028
Patch1049: glibc-rh841787.patch

# Systemtap malloc probes
Patch1050: glibc-rh742038.patch

# Upstream BZ 15006
Patch1051: glibc-rh905184.patch

# Upstream BZ 14256
Patch1052: glibc-rh966259.patch

# Upstream BZ 15362
Patch1053: glibc-rh979363.patch

# Upstream BZ 14547
Patch1054: glibc-rh989862.patch
Patch1055: glibc-rh989862-2.patch
Patch1056: glibc-rh989862-3.patch
Patch1057: glibc-rh989861.patch

# Upstream s390/s390x bug fixes
Patch1058: glibc-rh804768-bugfix.patch

# Upstream BZ 15754
Patch1059: glibc-rh990481-CVE-2013-4788.patch

# Upstream BZ 16366
Patch1060: glibc-rh1039970.patch

# Upstream BZ 16365
Patch1061: glibc-rh1046199.patch

# Upstream BZ 16532
Patch1062: glibc-rh1063681.patch

# Upstream BZ 16680
Patch1063: glibc-rh1074410.patch

# PPC64LE Patch Set:
# abilist-pattern configurability
Patch1064: glibc-ppc64le-01.patch

# PowerPC: powerpc64le abilist for 2.17
Patch1065: glibc-ppc64le-02.patch

# Update miscellaneous scripts from upstream.
Patch1066: glibc-ppc64le-03.patch

# IBM long double mechanical changes to support little-endian
Patch1067: glibc-ppc64le-04.patch

# Fix for [BZ #15680] IBM long double inaccuracy
Patch1068: glibc-ppc64le-05.patch

# PowerPC floating point little-endian [1-15 of 15]
Patch1069: glibc-ppc64le-06.patch
Patch1070: glibc-ppc64le-07.patch
Patch1071: glibc-ppc64le-08.patch
Patch1072: glibc-ppc64le-09.patch
Patch1073: glibc-ppc64le-10.patch
Patch1074: glibc-ppc64le-11.patch
Patch1075: glibc-ppc64le-12.patch
Patch1076: glibc-ppc64le-13.patch
Patch1077: glibc-ppc64le-14.patch
Patch1078: glibc-ppc64le-15.patch
Patch1079: glibc-ppc64le-16.patch
Patch1080: glibc-ppc64le-17.patch
Patch1081: glibc-ppc64le-18.patch
Patch1082: glibc-ppc64le-19.patch
Patch1083: glibc-ppc64le-20.patch

# PowerPC LE setjmp/longjmp
Patch1084: glibc-ppc64le-21.patch

# PowerPC ugly symbol versioning
Patch1085: glibc-ppc64le-22.patch

# PowerPC LE _dl_hwcap access
Patch1086: glibc-ppc64le-23.patch

# PowerPC makecontext
Patch1087: glibc-ppc64le-24.patch

# PowerPC LE strlen
Patch1088: glibc-ppc64le-25.patch

# PowerPC LE strnlen
Patch1089: glibc-ppc64le-26.patch

# PowerPC LE strcmp and strncmp
Patch1090: glibc-ppc64le-27.patch

# PowerPC LE strcpy
Patch1091: glibc-ppc64le-28.patch

# PowerPC LE strchr
Patch1092: glibc-ppc64le-29.patch

# PowerPC LE memcmp
Patch1093: glibc-ppc64le-30.patch

# PowerPC LE memcpy
Patch1094: glibc-ppc64le-31.patch

# PowerPC LE memset
Patch1095: glibc-ppc64le-32.patch

# PowerPC LE memchr and memrchr
Patch1096: glibc-ppc64le-33.patch

# PowerPC LE configury
Patch1097: glibc-ppc64le-34.patch

# PowerPC64: Fix incorrect CFI in *context routines
Patch1098: glibc-ppc64le-35.patch

# PowerPC64: Report overflow on @h and @ha relocations
Patch1099: glibc-ppc64le-36.patch

# PowerPC64: Add __private_ss field to TCB header
Patch1100: glibc-ppc64le-37.patch

# PowerPC64 ELFv2 ABI 1/6: Code refactoring
Patch1101: glibc-ppc64le-38.patch

# PowerPC64 ELFv2 ABI 2/6: Remove function descriptors
Patch1102: glibc-ppc64le-39.patch

# PowerPC64 ELFv2 ABI 3/6: PLT local entry point optimization
Patch1103: glibc-ppc64le-40.patch

# PowerPC64 ELFv2 ABI 4/6: Stack frame layout changes
Patch1104: glibc-ppc64le-41.patch

# PowerPC64 ELFv2 ABI 5/6: LD_AUDIT interface changes
Patch1105: glibc-ppc64le-42.patch

# PowerPC64 ELFv2 ABI 6/6: Bump ld.so soname version number
Patch1106: glibc-ppc64le-43.patch

# Fix s_copysign stack temp for PowerPC64 ELFv2 [BZ #16786]
Patch1107: glibc-ppc64le-44.patch

# PPC64LE only Versions.def change.
Patch1108: glibc-ppc64le-45.patch

# powerpc/fpu/libm-test-ulps tan() round-toward-zero fixup.
Patch1109: glibc-ppc64le-46.patch
# End of PPC64LE patch set.
# Leave room up to 1120 for ppc64le patches.

# Split out ldbl_high into a distinct patch that is applied *before*
# the ppc64le patches and the ppc64 IFUNC patches. We do this because
# we want the IFUNC patches to be LE-safe and some code has to be
# factored out and applied for both to use.
Patch1110: glibc-powerpc-ldbl_high.patch

# RH BZ #1186491: disable inlining in math tests to work around
# a GCC bug.
Patch1112: glibc-rh1186491.patch

# Backport the write buffer size adjustment to match newer kernels.
Patch1122: glibc-fix-test-write-buf-size.patch

Patch1123: glibc-rh1248208.patch
Patch1124: glibc-rh1248208-2.patch

# Upstream BZ #14142
# Required RHEL 7.1 BZ #1067754
Patch1499: glibc-rh1067755.patch

# Acadia BZ #1070458
Patch1500: glibc-rh1070458.patch

# Upstream BZ #15036
# Acadia BZ #1070471
Patch1501: glibc-rh1070471.patch

# Upstream BZ #16169
# Acadia BZ #1078225
Patch1502: glibc-rh1078225.patch

# Upstream BZ #16629 -- plus a bit extra
Patch1503: glibc-aa64-setcontext.patch

Patch1504: glibc-aarch64-add-ptr_mangle-support.patch
Patch1505: glibc-aarch64-fpu-optional-trapping-exceptions.patch
Patch1506: glibc-aarch64-syscall-rewrite.patch
Patch1508: glibc-aarch64-ifunc.patch

Patch1509: glibc-rh1133812-2.patch
Patch1510: glibc-rh1133812-3.patch

Patch1511: glibc-rh1083647.patch
Patch1512: glibc-rh1085290.patch
Patch1513: glibc-rh1083644.patch
Patch1514: glibc-rh1083646.patch

Patch1515: glibc-rh1103856.patch
Patch1516: glibc-rh1080766.patch
Patch1517: glibc-rh1103874.patch
Patch1518: glibc-rh1125306.patch
Patch1519: glibc-rh1098047.patch
Patch1520: glibc-rh1138520.patch
Patch1521: glibc-rh1085313.patch
Patch1522: glibc-rh1140474.patch

# Backport multi-lib support in GLIBC for PowerPC using IFUNC
Patch1530: glibc-rh731837-00.patch
Patch1531: glibc-rh731837-01.patch
Patch1532: glibc-rh731837-02.patch
Patch1533: glibc-rh731837-03.patch
Patch1534: glibc-rh731837-04.patch
Patch1535: glibc-rh731837-05.patch
Patch1536: glibc-rh731837-06.patch
Patch1537: glibc-rh731837-07.patch
Patch1538: glibc-rh731837-08.patch
Patch1539: glibc-rh731837-09.patch
Patch1540: glibc-rh731837-10.patch
Patch1541: glibc-rh731837-11.patch
Patch1542: glibc-rh731837-12.patch
Patch1543: glibc-rh731837-13.patch
Patch1544: glibc-rh731837-14.patch
Patch1545: glibc-rh731837-15.patch
Patch1546: glibc-rh731837-16.patch
Patch1547: glibc-rh731837-17.patch
Patch1548: glibc-rh731837-18.patch
Patch1549: glibc-rh731837-19.patch
Patch1550: glibc-rh731837-20.patch
Patch1551: glibc-rh731837-21.patch
Patch1552: glibc-rh731837-22.patch
Patch1553: glibc-rh731837-23.patch
Patch1554: glibc-rh731837-24.patch
Patch1555: glibc-rh731837-25.patch
Patch1556: glibc-rh731837-26.patch
Patch1557: glibc-rh731837-27.patch
Patch1558: glibc-rh731837-28.patch
Patch1559: glibc-rh731837-29.patch
Patch1560: glibc-rh731837-30.patch
Patch1561: glibc-rh731837-31.patch
Patch1562: glibc-rh731837-32.patch
Patch1563: glibc-rh731837-33.patch
Patch1564: glibc-rh731837-34.patch
Patch1565: glibc-rh731837-35.patch
Patch1566: glibc-rh731837-33A.patch
Patch1567: glibc-rh731837-36.patch

# Intel AVX-512 support.
Patch1570: glibc-rh1140272-avx512.patch
# Intel MPX support.
Patch1571: glibc-rh1132518-mpx.patch
# glibc manual update.
Patch1572: glibc-manual-update.patch

Patch1573: glibc-rh1120490.patch

# Fix ppc64le relocation handling:
Patch1574: glibc-rh1162847-p1.patch
Patch1575: glibc-rh1162847-p2.patch

# CVE-2014-7817
Patch1576: glibc-rh1170118-CVE-2014-7817.patch

# Provide artificial OPDs for ppc64 VDSO functions.
Patch1577: glibc-rh1077389-p1.patch
# BZ#16431
Patch1578: glibc-rh1077389-p2.patch
# BZ#16037 - Allow GNU Make version 4.0 and up to be used.
Patch1579: glibc-gmake.patch

Patch1580: glibc-rh1183545.patch

Patch1581: glibc-rh1064066.patch

# RHBZ #1165212 - [SAP] Recursive dlopen causes SAP HANA installer
#                 to crash
#   including RHBZ #1225959 - Test suite failure: tst-rec-dlopen fails
Patch1582: glibc-rh1165212.patch
# BZ#17411
Patch1583: glibc-rh1144133.patch

# BZ#12100 - QoI regression: strstr() slowed from O(n) to O(n^2)
#            on SSE4 machines
# but mainly RHBZ #1150282 - glibc-2.17-55 crashes sqlplus
Patch1584: glibc-rh1150282.patch
# BZ#13862
Patch1585: glibc-rh1189278.patch
Patch1586: glibc-rh1189278-1.patch
# BZ#17892
Patch1587: glibc-rh1183456.patch
# BZ#14841
Patch1588: glibc-rh1186620.patch

# BZ#16878 - nscd enters busy loop on long netgroup entry via nss_ldap
#            of nslcd
Patch1589: glibc-rh1173537.patch

# BZ#14906: inotify failed when /etc/hosts file change
Patch1590: glibc-rh1193797.patch
# RHBZ #1173238 - `check-abi-librtkaio' not performed during
# make check after building glibc
Patch1591: glibc-rh1173238.patch

Patch1592: glibc-rh1207032.patch

Patch1593: glibc-rh1176906.patch
Patch1594: glibc-rh1159169.patch
Patch1595: glibc-rh1098042.patch
Patch1596: glibc-rh1194143.patch
Patch1597: glibc-rh1219891.patch

# RHBZ #1209107 - CVE-2015-1781 CVE-2015-1473 CVE-2015-1472 glibc:
#                 various flaws [rhel-7.2]
# * RHBZ #1188235 - (CVE-2015-1472) CVE-2015-1472 glibc: heap buffer
#                   overflow in glibc swscanf
#   upstream #16618 - wscanf allocates too little memory
#                     (CVE-2015-1472, CVE-2015-1473)
Patch1598: glibc-rh1188235.patch
#
# * RHBZ #1195762 - glibc: _IO_wstr_overflow integer overflow
#   upstream #16009 - Possible buffer overflow in strxfrm
Patch1599: glibc-rh1195762.patch
#
# * RHBZ #1197730 - glibc: potential denial of service in internal_fnmatch()
#   upstream #17062 - fnmatch: buffer overflow read from pattern
#                     "[[:alpha:]'[:alpha:]"
Patch1600: glibc-rh1197730-1.patch
#   upstream #18032 - buffer overflow (read past end of buffer) in
#                     internal_fnmatch
Patch1601: glibc-rh1197730-2.patch
#   upstream #18036 - buffer overflow (read past end of buffer)
#                     in internal_fnmatch=>end_pattern with "**(!()" pattern
Patch1602: glibc-rh1197730-3.patch
#
# * RHBZ #1199525 - (CVE-2015-1781) CVE-2015-1781 glibc: buffer overflow
#                   in gethostbyname_r() and related functions with
#                   misaligned buffer
#  upstream #18287 - (CVE-2015-1781) - Buffer overflow in getanswer_r,
#                    resolv/nss_dns/dns-host.c (CVE-2015-1781)
Patch1603: glibc-rh1199525.patch
#
# RHBZ #1162895 - Backport upstream ppc64 and ppc64le enhancements
# * upstream #17153 - Shared libraries built with multiple tocs resolve
#                     plt to local function entry
Patch1604: glibc-rh1162895-1.patch
#
# * upstream #16740 - IBM long double frexpl wrong when value slightly
#                     smaller than a power of two
# * upstream #16619 - [ldbl-128ibm] frexpl bad results on some denormal
#                     arguments
Patch1605: glibc-rh1162895-2.patch
#
# * upstream #16739 - IBM long double nextafterl wrong on power of two value
Patch1606: glibc-rh1162895-3.patch
# RHBZ #1214326 - Upstream benchtests/ rebase
# RHBZ #1084395 - Run pythong scripts with $(PYTHON).
Patch1607: glibc-rh1084395.patch

# CVE-2014-8121:
Patch1608: glibc-rh1165192.patch

# BZ #17090, BZ #17620, BZ #17621, BZ #17628
Patch1609: glibc-rh1202952.patch

# BZ #15234:
Patch1610: glibc-rh1234622.patch

# Fix 32-bit POWER assembly to use only 32-bit instructions.
Patch1611: glibc-rh1240796.patch

# Fix for RHBZ #1213267 as a prerequisite for the patches below.
Patch1612: glibc-rh1240351-1.patch

# Backport of POWER8 glibc optimizations for RHEL7.3: math functions
Patch1613: glibc-rh1240351-2.patch
Patch1614: glibc-rh1240351-3.patch

# Backport of POWER8 glibc optimizations for RHEL7.3: string functions
Patch1615: glibc-rh1240351-4.patch
Patch1616: glibc-rh1240351-5.patch
Patch1617: glibc-rh1240351-6.patch
Patch1618: glibc-rh1240351-7.patch
Patch1619: glibc-rh1240351-8.patch
Patch1620: glibc-rh1240351-9.patch
Patch1621: glibc-rh1240351-10.patch
Patch1622: glibc-rh1240351-11.patch
Patch1623: glibc-rh1240351-12.patch

# Backport of upstream IBM z13 patches for RHEL 7.3
Patch1624: glibc-rh1268008-1.patch
Patch1625: glibc-rh1268008-2.patch
Patch1626: glibc-rh1268008-3.patch
Patch1627: glibc-rh1268008-4.patch
Patch1628: glibc-rh1268008-5.patch
Patch1629: glibc-rh1268008-6.patch
Patch1630: glibc-rh1268008-7.patch
Patch1631: glibc-rh1268008-8.patch
Patch1632: glibc-rh1268008-9.patch
Patch1633: glibc-rh1268008-10.patch
Patch1634: glibc-rh1268008-11.patch
Patch1635: glibc-rh1268008-12.patch
Patch1636: glibc-rh1268008-13.patch
Patch1637: glibc-rh1268008-14.patch
Patch1638: glibc-rh1268008-15.patch
Patch1639: glibc-rh1268008-16.patch
Patch1640: glibc-rh1268008-17.patch
Patch1641: glibc-rh1268008-18.patch
Patch1642: glibc-rh1268008-19.patch
Patch1643: glibc-rh1268008-20.patch
Patch1644: glibc-rh1268008-21.patch
Patch1645: glibc-rh1268008-22.patch
Patch1646: glibc-rh1268008-23.patch
Patch1647: glibc-rh1268008-24.patch
Patch1648: glibc-rh1268008-25.patch
Patch1649: glibc-rh1268008-26.patch
Patch1650: glibc-rh1268008-27.patch
Patch1651: glibc-rh1268008-28.patch
Patch1652: glibc-rh1268008-29.patch
Patch1653: glibc-rh1268008-30.patch

Patch1654: glibc-rh1249102.patch

# CVE-2015-5229 and regression test.
Patch1656: glibc-rh1293976.patch
Patch1657: glibc-rh1293976-2.patch

# BZ #16574
Patch1658: glibc-rh1296031-0.patch
# BZ #13928
Patch1660: glibc-rh1296031-2.patch

# Malloc trim fixes: #17195, #18502.
Patch1661: glibc-rh1284959-1.patch
Patch1662: glibc-rh1284959-2.patch
Patch1663: glibc-rh1284959-3.patch

# RHBZ #1293916 - iconv appears to be adding a duplicate "SI"
#                 to the output for certain inputs 
Patch1664: glibc-rh1293916.patch

# Race condition in _int_free involving fastbins: #15073
Patch1665: glibc-rh1027101.patch

# BZ #17370: Memory leak in wide-oriented ftell.
Patch1666: glibc-rh1310530.patch

# BZ #19791: NULL pointer dereference in stub resolver with unconnectable
# name server addresses
Patch1667: glibc-rh1320596.patch

# RHBZ #1298349 - Backport tst-getpw enhancements
Patch1668: glibc-rh1298349.patch

# RHBZ #1293433 - Test suite failure: Fix bug17079
Patch1669: glibc-rh1293433.patch

# RHBZ #1298354 - Backport test-skeleton.c conversions
Patch1670: glibc-rh1298354.patch

# RHBZ #1288613 - gethostbyname_r hangs forever
Patch1671: glibc-rh1288613.patch

# RHBZ #1064063 - Test suite failure: tst-mqueue5
Patch1672: glibc-rh1064063.patch

# RHBZ #140250 - Unexpected results from using posix_fallocate
#                with nfs target 
Patch1675: glibc-rh1140250.patch

# RHBZ #1324427 - RHEL7.3 - S390: fprs/vrs are not saved/restored while
#                 resolving symbols
Patch1676: glibc-rh1324427-1.patch
Patch1677: glibc-rh1324427-2.patch
Patch1678: glibc-rh1324427-3.patch

# RHBZ #1234449 - glibc: backport upstream hardening patches
Patch1679: glibc-rh1234449-1.patch
Patch1680: glibc-rh1234449-2.patch
Patch1681: glibc-rh1234449-3.patch
Patch1682: glibc-rh1234449-4.patch

# RHBZ #1221046 - make bits/stat.h FTM guards consistent on all arches
Patch1683: glibc-rh1221046.patch

# RHBZ #971416 - Locale alias no_NO.ISO-8859-1 not working
Patch1684: glibc-rh971416-1.patch
Patch1685: glibc-rh971416-2.patch
Patch1686: glibc-rh971416-3.patch

# RHBZ 1302086 -  Improve libm performance AArch64
Patch1687: glibc-rh1302086-1.patch
Patch1688: glibc-rh1302086-2.patch
Patch1689: glibc-rh1302086-3.patch
Patch1690: glibc-rh1302086-4.patch
Patch1691: glibc-rh1302086-5.patch
Patch1692: glibc-rh1302086-6.patch
Patch1693: glibc-rh1302086-7.patch
Patch1694: glibc-rh1302086-8.patch
Patch1695: glibc-rh1302086-9.patch
Patch1696: glibc-rh1302086-10.patch
Patch1697: glibc-rh1302086-11.patch

# RHBZ 1346397 debug/tst-longjump_chk2 calls printf from a signal handler
Patch1698: glibc-rh1346397.patch

# RHBZ #1211823 Update BIG5-HKSCS charmap to HKSCS-2008
Patch1699: glibc-rh1211823.patch

# RHBZ #1268050 Backport "Coordinate IPv6 definitions for Linux and glibc"
Patch1700: glibc-rh1331283.patch
Patch1701: glibc-rh1331283-1.patch
Patch1702: glibc-rh1331283-2.patch
Patch1703: glibc-rh1331283-3.patch
Patch1704: glibc-rh1331283-4.patch

# RHBZ #1296297 enable (backport) instLangs in RHEL glibc
Patch1705: glibc-rh1296297.patch
Patch1706: glibc-rh1296297-1.patch

# RHBZ #1027348 sem_post/sem_wait race causing sem_post to return EINVAL
Patch1707: glibc-rh1027348.patch
Patch1708: glibc-rh1027348-1.patch
Patch1709: glibc-rh1027348-2.patch
Patch1710: glibc-rh1027348-3.patch
Patch1711: glibc-rh1027348-4.patch

# RHBZ #1308728 Fix __times() handling of EFAULT when buf is NULL
Patch1712: glibc-rh1308728.patch

# RHBZ #1249114 [s390] setcontext/swapcontext does not restore signal mask
Patch1713: glibc-rh1249114.patch
# RHBZ #1249115 S390: backtrace() returns infinitely deep stack ...
Patch1714: glibc-rh1249115.patch

# RHBZ #1321993: CVE-2016-3075: Stack overflow in nss_dns_getnetbyname_r
Patch1715: glibc-rh1321993.patch

# RHBZ #1256317 - IS_IN backports.
Patch1716: glibc-rh1256317-21.patch
Patch1717: glibc-rh1256317-20.patch
Patch1718: glibc-rh1256317-19.patch
Patch1719: glibc-rh1256317-18.patch
Patch1720: glibc-rh1256317-17.patch
Patch1721: glibc-rh1256317-16.patch
Patch1722: glibc-rh1256317-15.patch
Patch1723: glibc-rh1256317-14.patch
Patch1724: glibc-rh1256317-13.patch
Patch1725: glibc-rh1256317-12.patch
Patch1726: glibc-rh1256317-11.patch
Patch1727: glibc-rh1256317-10.patch
Patch1728: glibc-rh1256317-9.patch
Patch1729: glibc-rh1256317-8.patch
Patch1730: glibc-rh1256317-7.patch
Patch1731: glibc-rh1256317-6.patch
Patch1732: glibc-rh1256317-5.patch
Patch1733: glibc-rh1256317-4.patch
Patch1734: glibc-rh1256317-3.patch
Patch1735: glibc-rh1256317-2.patch
Patch1736: glibc-rh1256317-1.patch
Patch1737: glibc-rh1256317-0.patch

# RHBZ #1335286 [Intel 7.3 Bug] (Purley) Backport 64-bit memset from glibc 2.18
Patch1738: glibc-rh1335286-0.patch
Patch1739: glibc-rh1335286.patch

# RHBZ #1292018 [Intel 7.3 Bug] Improve branch prediction on Knights Landing/Silvermont
Patch1740: glibc-rh1292018-0.patch
Patch1741: glibc-rh1292018-0a.patch
Patch1742: glibc-rh1292018-0b.patch
Patch1743: glibc-rh1292018-1.patch
Patch1744: glibc-rh1292018-2.patch
Patch1745: glibc-rh1292018-3.patch
Patch1746: glibc-rh1292018-4.patch
Patch1747: glibc-rh1292018-5.patch
Patch1748: glibc-rh1292018-6.patch
Patch1749: glibc-rh1292018-7.patch

# RHBZ #1255822 glibc: malloc may fall back to calling mmap prematurely if arenas are contended
Patch1750: glibc-rh1255822.patch

# RHBZ #1298526 [Intel 7.3 FEAT] glibc: AVX-512 optimized memcpy
Patch1751: glibc-rh1298526-0.patch
Patch1752: glibc-rh1298526-1.patch
Patch1753: glibc-rh1298526-2.patch
Patch1754: glibc-rh1298526-3.patch
Patch1755: glibc-rh1298526-4.patch

# RHBZ #1350733 locale-archive.tmpl cannot be processed by build-locale-archive
Patch1756: glibc-rh1350733-1.patch

# Fix tst-cancel17/tst-cancelx17, which sometimes segfaults while exiting.
Patch1757: glibc-rh1337242.patch

# RHBZ #1418978: backport upstream support/ directory
Patch17580: glibc-rh1418978-max_align_t.patch
Patch1758: glibc-rh1418978-0.patch
Patch1759: glibc-rh1418978-1.patch
Patch2752: glibc-rh1418978-1a.patch
Patch1760: glibc-rh1418978-2-1.patch
Patch1761: glibc-rh1418978-2-2.patch
Patch1762: glibc-rh1418978-2-3.patch
Patch1763: glibc-rh1418978-2-4.patch
Patch1764: glibc-rh1418978-2-5.patch
Patch1765: glibc-rh1418978-2-6.patch
Patch1766: glibc-rh1418978-3-1.patch
Patch1767: glibc-rh1418978-3-2.patch

# RHBZ #906468: Fix deadlock between fork, malloc, flush (NULL)
Patch1768: glibc-rh906468-1.patch
Patch1769: glibc-rh906468-2.patch

# RHBZ #988869: stdio buffer auto-tuning should reject large buffer sizes
Patch1770: glibc-rh988869.patch

# RHBZ #1398244 - RHEL7.3 - glibc: Fix TOC stub on powerpc64 clone()
Patch1771: glibc-rh1398244.patch

# RHBZ #1228114: Fix sunrpc UDP client timeout handling
Patch1772: glibc-rh1228114-1.patch
Patch1773: glibc-rh1228114-2.patch

# RHBZ #1298975 - [RFE] Backport the groups merging feature
Patch1774: glibc-rh1298975.patch

# RHBZ #1318877 - Per C11 and C++11, <stdint.h> should not look at
# __STDC_LIMIT_MACROS or __STDC_CONSTANT_MACROS
Patch1775: glibc-rh1318877.patch

# RHBZ #1417205: Add AF_VSOCK/PF_VSOCK, TCP_TIMESTAMP
Patch1776: glibc-rh1417205.patch

# RHBZ #1338672: GCC 6 enablement for struct sockaddr_storage
Patch1777: glibc-rh1338672.patch

# RHBZ #1325138 - glibc: Corrupted aux-cache causes ldconfig to segfault
Patch1778: glibc-rh1325138.patch

# RHBZ #1374652: Unbounded stack allocation in nan* functions
Patch1779: glibc-rh1374652.patch

# RHBZ #1374654: Unbounded stack allocation in nan* functions
Patch1780: glibc-rh1374654.patch

# RHBZ #1322544: Segmentation violation can occur within glibc if fork()
# is used in a multi-threaded application
Patch1781: glibc-rh1322544.patch

# RHBZ #1418997: does not build with binutils 2.27 due to misuse of the cmpli instruction on ppc64
Patch1782: glibc-rh1418997.patch

# RHBZ #1383951: LD_POINTER_GUARD in the environment is not sanitized
Patch1783: glibc-rh1383951.patch

# RHBZ #1385004: [7.4 FEAT] POWER8 IFUNC update from upstream
Patch1784: glibc-rh1385004-1.patch
Patch1785: glibc-rh1385004-2.patch
Patch1786: glibc-rh1385004-3.patch
Patch1787: glibc-rh1385004-4.patch
Patch1788: glibc-rh1385004-5.patch
Patch1789: glibc-rh1385004-6.patch
Patch1790: glibc-rh1385004-7.patch
Patch1791: glibc-rh1385004-8.patch
Patch1792: glibc-rh1385004-9.patch
Patch1793: glibc-rh1385004-10.patch
Patch1794: glibc-rh1385004-11.patch
Patch1795: glibc-rh1385004-12.patch
Patch1796: glibc-rh1385004-13.patch
Patch1797: glibc-rh1385004-14.patch
Patch1798: glibc-rh1385004-15.patch
Patch1799: glibc-rh1385004-16.patch
Patch1800: glibc-rh1385004-17.patch
Patch1801: glibc-rh1385004-18.patch
Patch1802: glibc-rh1385004-19.patch
Patch1803: glibc-rh1385004-20.patch
Patch1804: glibc-rh1385004-21.patch
Patch1805: glibc-rh1385004-22.patch
Patch1806: glibc-rh1385004-23.patch
Patch1807: glibc-rh1385004-24.patch

# RHBZ 1380680 - [7.4 FEAT] z13 exploitation in glibc - stage 2
Patch1808: glibc-rh1380680-1.patch
Patch1809: glibc-rh1380680-2.patch
Patch1810: glibc-rh1380680-3.patch
Patch1811: glibc-rh1380680-4.patch
Patch1812: glibc-rh1380680-5.patch
Patch1813: glibc-rh1380680-6.patch
Patch1814: glibc-rh1380680-7.patch
Patch1815: glibc-rh1380680-8.patch
Patch1816: glibc-rh1380680-9.patch
Patch1817: glibc-rh1380680-10.patch
Patch1818: glibc-rh1380680-11.patch
Patch1819: glibc-rh1380680-12.patch
Patch1820: glibc-rh1380680-13.patch
Patch1821: glibc-rh1380680-14.patch
Patch1822: glibc-rh1380680-15.patch
Patch1823: glibc-rh1380680-16.patch
Patch1824: glibc-rh1380680-17.patch

# RHBZ #1326739: malloc: additional unlink hardening for non-small bins
Patch1825: glibc-rh1326739.patch

# RHBZ #1374657: CVE-2015-8778: Integer overflow in hcreate and hcreate_r
Patch1826: glibc-rh1374657.patch

# RHBZ #1374658 - CVE-2015-8776: Segmentation fault caused by passing
# out-of-range data to strftime()
Patch1827: glibc-rh1374658.patch

# RHBZ #1385003 - SIZE_MAX evaluates to an expression of the wrong type
# on s390
Patch1828: glibc-rh1385003.patch

# RHBZ #1387874 - MSG_FASTOPEN definition missing
Patch1829: glibc-rh1387874.patch

# RHBZ #1409611 - poor performance with exp()
Patch1830: glibc-rh1409611.patch

# RHBZ #1421155 - Update dynamic loader trampoline for Intel SSE, AVX, and AVX512 usage.
Patch1831: glibc-rh1421155.patch

# RHBZ #841653 - [Intel 7.0 FEAT] [RFE] TSX-baed lock elision enabled in glibc.
Patch1832: glibc-rh841653-0.patch
Patch1833: glibc-rh841653-1.patch
Patch1834: glibc-rh841653-2.patch
Patch1835: glibc-rh841653-3.patch
Patch1836: glibc-rh841653-4.patch
Patch1837: glibc-rh841653-5.patch
Patch1838: glibc-rh841653-6.patch
Patch1839: glibc-rh841653-7.patch
Patch1840: glibc-rh841653-8.patch
Patch1841: glibc-rh841653-9.patch
Patch1842: glibc-rh841653-10.patch
Patch1843: glibc-rh841653-11.patch
Patch1844: glibc-rh841653-12.patch
Patch1845: glibc-rh841653-13.patch
Patch1846: glibc-rh841653-14.patch
Patch1847: glibc-rh841653-15.patch
Patch1848: glibc-rh841653-16.patch
Patch1849: glibc-rh841653-17.patch

# RHBZ #731835 - [RFE] [7.4 FEAT] Hardware Transactional Memory in GLIBC
Patch1850: glibc-rh731835-0.patch
Patch1851: glibc-rh731835-1.patch
Patch1852: glibc-rh731835-2.patch

# RHBZ #1413638: Inhibit FMA while compiling sqrt, pow
Patch1853: glibc-rh1413638-1.patch
Patch1854: glibc-rh1413638-2.patch

# RHBZ #1439165: Use a built-in list of known syscalls for <bits/syscall.h>
Patch1855: glibc-rh1439165.patch
Patch1856: glibc-rh1439165-syscall-names.patch

# RHBZ #1457177: Rounding issues on POWER
Patch1857: glibc-rh1457177-1.patch
Patch1858: glibc-rh1457177-2.patch
Patch1859: glibc-rh1457177-3.patch
Patch1860: glibc-rh1457177-4.patch

Patch1861: glibc-rh1348000.patch
Patch1862: glibc-rh1443236.patch
Patch1863: glibc-rh1447556.patch
Patch1864: glibc-rh1463692-1.patch
Patch1865: glibc-rh1463692-2.patch
Patch1866: glibc-rh1347277.patch

# RHBZ #1375235: Add new s390x instruction support
Patch1867: glibc-rh1375235-1.patch
Patch1868: glibc-rh1375235-2.patch
Patch1869: glibc-rh1375235-3.patch
Patch1870: glibc-rh1375235-4.patch
Patch1871: glibc-rh1375235-5.patch
Patch1872: glibc-rh1375235-6.patch
Patch1873: glibc-rh1375235-7.patch
Patch1874: glibc-rh1375235-8.patch
Patch1875: glibc-rh1375235-9.patch
Patch1876: glibc-rh1375235-10.patch

# RHBZ #1435615: nscd cache thread hangs
Patch1877: glibc-rh1435615.patch

# RHBZ #1398413: libio: Implement vtable verification
Patch1878: glibc-rh1398413.patch

# RHBZ #1445781:  elf/tst-audit set of tests fails with "no PLTREL"
Patch1879: glibc-rh1445781-1.patch
Patch1880: glibc-rh1445781-2.patch

Patch1881: glibc-rh1500908.patch
Patch1882: glibc-rh1448822.patch
Patch1883: glibc-rh1468807.patch
Patch1884: glibc-rh1372305.patch
Patch1885: glibc-rh1349962.patch
Patch1886: glibc-rh1349964.patch
Patch1887: glibc-rh1440250.patch
Patch1888: glibc-rh1504809-1.patch
Patch1889: glibc-rh1504809-2.patch
Patch1890: glibc-rh1504969.patch
Patch1891: glibc-rh1498925-1.patch
Patch1892: glibc-rh1498925-2.patch

# RHBZ #1503854: Pegas1.0 - Update HWCAP bits for POWER9 DD2.1
Patch1893: glibc-rh1503854-1.patch
Patch1894: glibc-rh1503854-2.patch
Patch1895: glibc-rh1503854-3.patch

# RHBZ #1527904: PTHREAD_STACK_MIN is too small on x86_64
Patch1896: glibc-rh1527904-1.patch
Patch1897: glibc-rh1527904-2.patch
Patch1898: glibc-rh1527904-3.patch
Patch1899: glibc-rh1527904-4.patch

# RHBZ #1534635: CVE-2018-1000001 glibc: realpath() buffer underflow.
Patch1900: glibc-rh1534635.patch

# RHBZ #1529982: recompile glibc to fix incorrect CFI information on i386.
Patch1901: glibc-rh1529982.patch

Patch1902: glibc-rh1523119-compat-symbols.patch

# RHBZ #1609067: Backfort of upstream [#15804] - fix race condition in pldd
Patch1903: glibc-rh1609067.patch

Patch2500: glibc-rh1505492-nscd_stat.patch
Patch2501: glibc-rh1564638.patch
Patch2502: glibc-rh1566623.patch
Patch2503: glibc-rh1349967.patch
Patch2504: glibc-rh1505492-undef-malloc.patch
Patch2505: glibc-rh1505492-undef-elf-dtv-resize.patch
Patch2506: glibc-rh1505492-undef-elision.patch
Patch2507: glibc-rh1505492-undef-max_align_t.patch
Patch2508: glibc-rh1505492-unused-tst-default-attr.patch
Patch2509: glibc-rh1505492-prototypes-rtkaio.patch
Patch2510: glibc-rh1505492-zerodiv-log.patch
Patch2511: glibc-rh1505492-selinux.patch
Patch2512: glibc-rh1505492-undef-abi.patch
Patch2513: glibc-rh1505492-unused-math.patch
Patch2514: glibc-rh1505492-prototypes-1.patch
Patch2515: glibc-rh1505492-uninit-intl-plural.patch
Patch2516: glibc-rh1505492-undef-1.patch
Patch2517: glibc-rh1505492-undef-2.patch
Patch2518: glibc-rh1505492-bounded-1.patch
Patch2519: glibc-rh1505492-bounded-2.patch
Patch2520: glibc-rh1505492-bounded-3.patch
Patch2521: glibc-rh1505492-bounded-4.patch
Patch2522: glibc-rh1505492-undef-3.patch
Patch2523: glibc-rh1505492-bounded-5.patch
Patch2524: glibc-rh1505492-bounded-6.patch
Patch2525: glibc-rh1505492-bounded-7.patch
Patch2526: glibc-rh1505492-bounded-8.patch
Patch2527: glibc-rh1505492-unused-1.patch
Patch2528: glibc-rh1505492-bounded-9.patch
Patch2529: glibc-rh1505492-bounded-10.patch
Patch2530: glibc-rh1505492-bounded-11.patch
Patch2531: glibc-rh1505492-bounded-12.patch
Patch2532: glibc-rh1505492-bounded-13.patch
Patch2533: glibc-rh1505492-unused-2.patch
Patch2534: glibc-rh1505492-bounded-14.patch
Patch2535: glibc-rh1505492-bounded-15.patch
Patch2536: glibc-rh1505492-bounded-16.patch
Patch2537: glibc-rh1505492-bounded-17.patch
Patch2538: glibc-rh1505492-malloc_size_t.patch
Patch2539: glibc-rh1505492-malloc_ptrdiff_t.patch
Patch2540: glibc-rh1505492-prototypes-2.patch
Patch2541: glibc-rh1505492-prototypes-libc_fatal.patch
Patch2542: glibc-rh1505492-getlogin.patch
Patch2543: glibc-rh1505492-undef-4.patch
Patch2544: glibc-rh1505492-register.patch
Patch2545: glibc-rh1505492-prototypes-3.patch
Patch2546: glibc-rh1505492-unused-3.patch
Patch2547: glibc-rh1505492-ports-move-powerpc.patch
Patch2548: glibc-rh1505492-unused-4.patch
Patch2549: glibc-rh1505492-systemtap.patch
Patch2550: glibc-rh1505492-prototypes-wcschr-1.patch
Patch2551: glibc-rh1505492-prototypes-wcsrchr.patch
Patch2552: glibc-rh1505492-prototypes-powerpc-wcscpy.patch
Patch2553: glibc-rh1505492-prototypes-powerpc-wordcopy.patch
Patch2554: glibc-rh1505492-bsd-flatten.patch
Patch2555: glibc-rh1505492-unused-5.patch
Patch2556: glibc-rh1505492-types-1.patch
Patch2557: glibc-rh1505492-powerpc-sotruss.patch
Patch2558: glibc-rh1505492-s390x-sotruss.patch
Patch2559: glibc-rh1505492-ports-am33.patch
Patch2560: glibc-rh1505492-ports-move-arm.patch
Patch2561: glibc-rh1505492-undef-5.patch
Patch2562: glibc-rh1505492-prototypes-4.patch
Patch2563: glibc-rh1505492-ports-move-tile.patch
Patch2564: glibc-rh1505492-ports-move-m68k.patch
Patch2565: glibc-rh1505492-ports-move-mips.patch
Patch2566: glibc-rh1505492-ports-move-aarch64.patch
Patch2567: glibc-rh1505492-ports-move-alpha.patch
Patch2568: glibc-rh1505492-ports-move-ia64.patch
Patch2569: glibc-rh1505492-undef-6.patch
Patch2570: glibc-rh1505492-undef-7.patch
Patch2571: glibc-rh1505492-undef-intl.patch
Patch2572: glibc-rh1505492-undef-obstack.patch
Patch2573: glibc-rh1505492-undef-error.patch
Patch2574: glibc-rh1505492-undef-string.patch
Patch2575: glibc-rh1505492-undef-tempname.patch
Patch2576: glibc-rh1505492-undef-8.patch
Patch2577: glibc-rh1505492-undef-mktime.patch
Patch2578: glibc-rh1505492-undef-sysconf.patch
Patch2579: glibc-rh1505492-prototypes-Xat.patch
Patch2580: glibc-rh1505492-undef-ipc64.patch
Patch2581: glibc-rh1505492-undef-xfs-chown.patch
Patch2582: glibc-rh1505492-undef-9.patch
Patch2583: glibc-rh1505492-undef-10.patch
Patch2584: glibc-rh1505492-undef-11.patch
Patch2585: glibc-rh1505492-undef-12.patch
Patch2586: glibc-rh1505492-prototypes-5.patch
Patch2587: glibc-rh1505492-undef-13.patch
Patch2588: glibc-rh1505492-undef-14.patch
Patch2589: glibc-rh1505492-undef-15.patch
Patch2590: glibc-rh1505492-ports-move-hppa.patch
Patch2591: glibc-rh1505492-undef-16.patch
Patch2592: glibc-rh1505492-undef-17.patch
Patch2593: glibc-rh1505492-undef-18.patch
Patch2594: glibc-rh1505492-undef-19.patch
Patch2595: glibc-rh1505492-undef-20.patch
Patch2596: glibc-rh1505492-undef-21.patch
Patch2597: glibc-rh1505492-undef-22.patch
Patch2598: glibc-rh1505492-undef-23.patch
Patch2599: glibc-rh1505492-undef-24.patch
Patch2600: glibc-rh1505492-prototypes-rwlock.patch
Patch2601: glibc-rh1505492-undef-25.patch
Patch2602: glibc-rh1505492-undef-26.patch
Patch2603: glibc-rh1505492-undef-27.patch
Patch2604: glibc-rh1505492-undef-28.patch
Patch2605: glibc-rh1505492-undef-29.patch
Patch2606: glibc-rh1505492-undef-30.patch
Patch2607: glibc-rh1505492-undef-31.patch
Patch2608: glibc-rh1505492-undef-32.patch
Patch2609: glibc-rh1505492-undef-33.patch
Patch2610: glibc-rh1505492-prototypes-memchr.patch
Patch2611: glibc-rh1505492-undef-34.patch
Patch2612: glibc-rh1505492-prototypes-powerpc-memmove.patch
Patch2613: glibc-rh1505492-undef-35.patch
Patch2614: glibc-rh1505492-undef-36.patch
Patch2615: glibc-rh1505492-undef-37.patch
Patch2616: glibc-rh1505492-uninit-1.patch
Patch2617: glibc-rh1505492-undef-38.patch
Patch2618: glibc-rh1505492-uninit-2.patch
Patch2619: glibc-rh1505492-undef-39.patch
Patch2620: glibc-rh1505492-undef-40.patch
Patch2621: glibc-rh1505492-undef-41.patch
Patch2622: glibc-rh1505492-undef-42.patch
Patch2623: glibc-rh1505492-undef-43.patch
Patch2624: glibc-rh1505492-undef-44.patch
Patch2625: glibc-rh1505492-undef-45.patch
Patch2626: glibc-rh1505492-undef-46.patch
Patch2627: glibc-rh1505492-undef-47.patch
Patch2628: glibc-rh1505492-prototypes-6.patch
Patch2629: glibc-rh1505492-undef-48.patch
Patch2630: glibc-rh1505492-prototypes-execve.patch
Patch2631: glibc-rh1505492-prototypes-readv-writev.patch
Patch2632: glibc-rh1505492-prototypes-7.patch
Patch2633: glibc-rh1505492-prototypes-powerpc-pread-pwrite.patch
Patch2634: glibc-rh1505492-s390-backtrace.patch
Patch2635: glibc-rh1505492-unused-6.patch
Patch2636: glibc-rh1505492-prototypes-8.patch
Patch2637: glibc-rh1505492-prototypes-ctermid.patch
Patch2638: glibc-rh1505492-unused-7.patch
Patch2639: glibc-rh1505492-uninit-3.patch
Patch2640: glibc-rh1505492-types-2.patch
Patch2641: glibc-rh1505492-unused-8.patch
Patch2642: glibc-rh1505492-unused-9.patch
Patch2643: glibc-rh1505492-types-3.patch
Patch2644: glibc-rh1505492-unused-10.patch
Patch2645: glibc-rh1505492-types-5.patch
Patch2646: glibc-rh1505492-unused-11.patch
Patch2647: glibc-rh1505492-unused-12.patch
Patch2648: glibc-rh1505492-unused-13.patch
Patch2649: glibc-rh1505492-deprecated-1.patch
Patch2650: glibc-rh1505492-unused-14.patch
Patch2651: glibc-rh1505492-types-6.patch
Patch2652: glibc-rh1505492-address.patch
Patch2653: glibc-rh1505492-types-7.patch
Patch2654: glibc-rh1505492-prototypes-9.patch
Patch2655: glibc-rh1505492-diag.patch
Patch2656: glibc-rh1505492-zerodiv-1.patch
Patch2657: glibc-rh1505492-deprecated-2.patch
Patch2658: glibc-rh1505492-unused-15.patch
Patch2659: glibc-rh1505492-prototypes-sigvec.patch
Patch2660: glibc-rh1505492-werror-activate.patch
Patch2661: glibc-rh1505492-types-8.patch
Patch2662: glibc-rh1505492-prototypes-intl.patch
Patch2663: glibc-rh1505492-types-9.patch
Patch2664: glibc-rh1505492-types-10.patch
Patch2665: glibc-rh1505492-prototypes-sem_unlink.patch
Patch2666: glibc-rh1505492-prototypes-s390-pthread_once.patch
Patch2667: glibc-rh1505492-types-11.patch
Patch2668: glibc-rh1505492-types-12.patch
Patch2669: glibc-rh1505492-types-13.patch
Patch2670: glibc-rh1505492-undef-49.patch
Patch2671: glibc-rh1505492-undef-50.patch
Patch2672: glibc-rh1505492-undef-51.patch
Patch2673: glibc-rh1505492-undef-52.patch
Patch2674: glibc-rh1505492-types-14.patch
Patch2675: glibc-rh1505492-prototypes-10.patch
Patch2676: glibc-rh1505492-prototypes-wcschr-2.patch
Patch2677: glibc-rh1505492-prototypes-bzero.patch
Patch2678: glibc-rh1505492-winline.patch
Patch2679: glibc-rh1505492-prototypes-scandir.patch
Patch2680: glibc-rh1505492-prototypes-timespec_get.patch
Patch2681: glibc-rh1505492-prototypes-gettimeofday.patch
Patch2682: glibc-rh1505492-prototypes-no_cancellation.patch
Patch2683: glibc-rh1505492-prototypes-getttynam.patch
Patch2684: glibc-rh1505492-undef-53.patch
Patch2685: glibc-rh1505492-prototypes-stpcpy.patch
Patch2686: glibc-rh1505492-undef-54.patch
Patch2687: glibc-rh1505492-undef-55.patch
Patch2688: glibc-rh1505492-undef-activate.patch
Patch2689: glibc-rh1505492-prototypes-debug.patch
Patch2690: glibc-rh1505492-prototypes-putXent.patch
Patch2691: glibc-rh1505492-prototypes-11.patch
Patch2692: glibc-rh1505492-prototypes-12.patch
Patch2693: glibc-rh1505492-prototypes-13.patch
Patch2694: glibc-rh1505492-prototypes-14.patch
Patch2695: glibc-rh1505492-prototypes-15.patch
Patch2696: glibc-rh1505492-prototypes-16.patch
Patch2697: glibc-rh1505492-prototypes-17.patch
Patch2698: glibc-rh1505492-prototypes-18.patch
Patch2699: glibc-rh1505492-prototypes-activate.patch
Patch2700: glibc-rh1505492-unused-16.patch
Patch2701: glibc-rh1505492-unused-17.patch
Patch2702: glibc-rh1505492-undef-56.patch
Patch2703: glibc-rh1548002.patch
Patch2704: glibc-rh1307241-1.patch
Patch2705: glibc-rh1307241-2.patch

Patch2706: glibc-rh1563747.patch
Patch2707: glibc-rh1476120.patch
Patch2708: glibc-rh1505647.patch

Patch2709: glibc-rh1457479-1.patch
Patch2710: glibc-rh1457479-2.patch
Patch2711: glibc-rh1457479-3.patch
Patch2712: glibc-rh1457479-4.patch
Patch2713: glibc-rh1461231.patch

Patch2714: glibc-rh1577333.patch
Patch2715: glibc-rh1531168-1.patch
Patch2716: glibc-rh1531168-2.patch
Patch2717: glibc-rh1531168-3.patch
Patch2718: glibc-rh1579742.patch
Patch2719: glibc-rh1579727-1.patch
Patch2720: glibc-rh1579727-2.patch
Patch2721: glibc-rh1579809-1.patch
Patch2722: glibc-rh1579809-2.patch
Patch2723: glibc-rh1505451.patch
Patch2724: glibc-rh1505477.patch
Patch2725: glibc-rh1505500.patch
Patch2726: glibc-rh1563046.patch

# RHBZ 1560641 - backport of upstream sem_open patch
Patch2727: glibc-rh1560641.patch

Patch2728: glibc-rh1550080.patch
Patch2729: glibc-rh1526193.patch
Patch2730: glibc-rh1372304-1.patch
Patch2731: glibc-rh1372304-2.patch
Patch2732: glibc-rh1540480-0.patch
Patch2733: glibc-rh1540480-1.patch
Patch2734: glibc-rh1540480-2.patch
Patch2735: glibc-rh1540480-3.patch
Patch2736: glibc-rh1540480-4.patch
Patch2737: glibc-rh1540480-5.patch
Patch2738: glibc-rh1540480-6.patch
Patch2739: glibc-rh1540480-7.patch
Patch2740: glibc-rh1540480-8.patch
Patch2741: glibc-rh1447808-0.patch
Patch2742: glibc-rh1447808-1.patch
Patch2743: glibc-rh1447808-2.patch
Patch2744: glibc-rh1401665-0.patch
Patch2745: glibc-rh1401665-1a.patch
Patch2746: glibc-rh1401665-1b.patch
Patch2747: glibc-rh1401665-1c.patch
Patch2748: glibc-rh1401665-2.patch
Patch2749: glibc-rh1401665-3.patch
Patch2750: glibc-rh1401665-4.patch
Patch2751: glibc-rh1401665-5.patch
Patch2753: glibc-rh1595191-1.patch
Patch2754: glibc-rh1595191-2.patch
Patch2755: glibc-rh1595191-3.patch
Patch2756: glibc-rh1595191-4.patch
Patch2757: glibc-rh1647490-1.patch
Patch2758: glibc-rh1647490-2.patch
Patch2759: glibc-rh1647490-3.patch
Patch2760: glibc-rh1647490-4.patch
Patch2761: glibc-rh1647490-5.patch
Patch2762: glibc-rh1639524.patch
Patch2763: glibc-rh1647490-6.patch
Patch2764: glibc-rh1579730-1.patch
Patch2765: glibc-rh1579730-2.patch
Patch2766: glibc-rh1579730-3.patch
Patch2767: glibc-rh1630440-1.patch
Patch2768: glibc-rh1630440-2.patch
Patch2769: glibc-rh1646373.patch
Patch2770: glibc-rh1591268.patch
Patch2771: glibc-rh1592475-1.patch
Patch2772: glibc-rh1592475-2.patch
Patch2773: glibc-rh1592475-3.patch
Patch2774: glibc-rh1657015-1.patch
Patch2775: glibc-rh1657015-2.patch
Patch2776: glibc-rh1657015-3.patch
Patch2777: glibc-rh1657015-4.patch
Patch2778: glibc-rh1673465-1.patch
Patch2779: glibc-rh1673465-2.patch
Patch2780: glibc-rh1673465-3.patch
Patch2781: glibc-rh1673465-4.patch
Patch2782: glibc-rh1673465-5.patch
Patch2783: glibc-rh1673465-6.patch
Patch2784: glibc-rh1673465-7.patch
Patch2785: glibc-rh1039304-1.patch
Patch2786: glibc-rh1039304-2.patch
Patch2787: glibc-rh1039304-3.patch
Patch2788: glibc-rh1039304-4.patch
Patch2789: glibc-rh1443872.patch
Patch2790: glibc-rh1472832.patch
Patch2791: glibc-rh1673465-8.patch
Patch2792: glibc-rh1443872-2.patch
Patch2793: glibc-rh1579354.patch
Patch2794: glibc-rh1579739.patch
Patch2795: glibc-rh1641981.patch
Patch2796: glibc-rh1579739-2.patch
Patch2797: glibc-rh1684874-1.patch
Patch2798: glibc-rh1684874-2.patch
Patch2799: glibc-rh1488370.patch
Patch2800: glibc-rh1662842.patch
Patch2801: glibc-rh1163509-1.patch
Patch2802: glibc-rh1163509-2.patch
Patch2803: glibc-rh1163509-3.patch
Patch2804: glibc-rh1163509-4.patch
Patch2805: glibc-rh1163509-5.patch
Patch2806: glibc-rh1555189-1.patch
Patch2807: glibc-rh1555189-2.patch
Patch2808: glibc-rh1427734-1.patch
Patch2809: glibc-rh1427734-2.patch

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
# Not upstream as of 2014-02-27
Patch2007: glibc-rh697421.patch

# Not upstream as of 2014-02-27
Patch2011: glibc-rh757881.patch

# Not upstream as of 2014-02-27
Patch2013: glibc-rh741105.patch

# Upstream BZ 14247
# Not upstream as of 2014-02-27.
Patch2023: glibc-rh827510.patch

# Upstream BZ 14185
# Not upstream as of 2014-02-27.
Patch2027: glibc-rh819430.patch

# Fix nscd to use permission names not constants.
# Not upstream as of 2014-02-27.
Patch2048: glibc-rh1025934.patch

# Upstream BZ 16398.
Patch2051: glibc-rh1048036.patch
Patch2052: glibc-rh1048123.patch

# Upstream BZ 16680
Patch2053: glibc-rh1074410-2.patch

# Upstream BZ 15493.
# Upstream as of 2013-03-20
Patch2055: glibc-rh1073667.patch

Patch2060: glibc-aarch64-rh1076760.patch

# Include pthread.h in rtkaio/tst-aiod2.c and rtkaio/tst-aiod3.c.
Patch2062: glibc-rtkaio-inc-pthread.patch

Patch2063: glibc-rh1084089.patch

Patch2064: glibc-rh1161666.patch

Patch2065: glibc-rh1156331.patch

# Upstream BZ 18557: Fix ruserok scalability issues.
Patch2066: glibc-rh1216246.patch

# Backport of fix for malloc arena free list management (upstream bug 19048)
# The preparatory patch removes !PER_THREAD conditional code.
Patch20670: glibc-rh1276753-0.patch
Patch2067: glibc-rh1276753.patch

# Backport to fix ld.so crash when audit modules provide path (upstream bug 18251)
Patch2068: glibc-rh1211100.patch

# aarch64 MINSIGSTKSZ/SIGSTKSZ fix
Patch2069: glibc-rh1335629.patch
Patch2070: glibc-rh1335925-1.patch
Patch2071: glibc-rh1335925-2.patch
Patch2072: glibc-rh1335925-3.patch
Patch2073: glibc-rh1335925-4.patch

# Do not set initgroups in default nsswitch.conf
Patch2074: glibc-rh1366569.patch

# Various nss_db fixes
Patch2075: glibc-rh1318890.patch
Patch2076: glibc-rh1213603.patch
Patch2077: glibc-rh1370630.patch

# Add internal-only support for O_TMPFILE.
Patch2078: glibc-rh1330705-1.patch
Patch2079: glibc-rh1330705-2.patch
Patch2080: glibc-rh1330705-3.patch
Patch2081: glibc-rh1330705-4.patch
Patch2082: glibc-rh1330705-5.patch
# The following patch *removes* the public definition of O_TMPFILE.
Patch2083: glibc-rh1330705-6.patch

# getaddrinfo with nscd fixes
Patch2084: glibc-rh1324568.patch

# RHBZ #1404435 - Remove power8 platform directory
Patch2085: glibc-rh1404435.patch

# RHBZ #1144516 - aarch64 profil fix
Patch2086: glibc-rh1144516.patch

# RHBZ #1392540 - Add "sss" service to the automount database in nsswitch.conf
Patch2087: glibc-rh1392540.patch

# RHBZ #1452721: Avoid large allocas in the dynamic linker
Patch2088: glibc-rh1452721-1.patch
Patch2089: glibc-rh1452721-2.patch
Patch2090: glibc-rh1452721-3.patch
Patch2091: glibc-rh1452721-4.patch

Patch2092: glibc-rh677316-libc-pointer-arith.patch
Patch2093: glibc-rh677316-libc-lock.patch
Patch2094: glibc-rh677316-libc-diag.patch
Patch2095: glibc-rh677316-check_mul_overflow_size_t.patch
Patch2096: glibc-rh677316-res_state.patch
Patch2097: glibc-rh677316-qsort_r.patch
Patch2098: glibc-rh677316-fgets_unlocked.patch
Patch2099: glibc-rh677316-in6addr_any.patch
Patch2100: glibc-rh677316-netdb-reentrant.patch
Patch2101: glibc-rh677316-h_errno.patch
Patch2102: glibc-rh677316-scratch_buffer.patch
Patch2103: glibc-rh677316-mtrace.patch
Patch2104: glibc-rh677316-dynarray.patch
Patch2105: glibc-rh677316-alloc_buffer.patch
Patch2106: glibc-rh677316-RES_USE_INET6.patch
Patch2107: glibc-rh677316-inet_pton.patch
Patch2108: glibc-rh677316-inet_pton-zeros.patch
Patch2109: glibc-rh677316-hesiod.patch
Patch2110: glibc-rh677316-resolv.patch
Patch2111: glibc-rh677316-legacy.patch

Patch2112: glibc-rh1498566.patch
Patch2113: glibc-rh1445644.patch

Patch2114: glibc-rh1471405.patch

##############################################################################
# End of glibc patches.
##############################################################################

# Amazon patches
Patch10000: glibc-amazon-Make-gen-posix-conf-vars-awk-script-work-with-AWK3.patch

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: glibc-profile < 2.4
Provides: ldconfig
# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# This is a short term need until everything is rebuilt in the ARM world
# to use the new dynamic linker path
%ifarch armv7hl armv7hnl
Provides: ld-linux.so.3
Provides: ld-linux.so.3(GLIBC_2.4)
%endif

# This should remain (or become a subpackage) to allow easy
# migration from old systems that previously had the old nss_db package
# installed. Note that this doesn't make the migration that smooth, the
# databases still need rebuilding because the formats were different.
# The nss_db package was deprecated in F16 and onwards:
# https://lists.fedoraproject.org/pipermail/devel/2011-July/153665.html
# The different database format does cause some issues for users:
# https://lists.fedoraproject.org/pipermail/devel/2011-December/160497.html
Obsoletes: nss_db < 2.17
Provides: nss_db = %{version}-%{release}
Provides: nss_db%{_isa} = %{version}-%{release}

Requires: glibc-common >= %{version}

# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
BuildRequires: audit-libs-devel >= 1.1.3
BuildRequires: gd-devel
BuildRequires: gettext
BuildRequires: libcap-devel
BuildRequires: libpng-devel
BuildRequires: libselinux-devel >= 1.33.4-3
BuildRequires: nss-devel
BuildRequires: nss-softokn-devel
BuildRequires: nss-softokn-freebl-devel
BuildRequires: sed >= 3.95
BuildRequires: texinfo
BuildRequires: zlib-devel
BuildRequires: /bin/ps
BuildRequires: /bin/kill
BuildRequires: /bin/awk
BuildRequires: systemtap-sdt-devel

# Require the version of freebl that we were built against.
%global freebl_version %(pkg-config --modversion nss-softokn 2>/dev/null || echo 0)
Requires: nss-softokn-freebl%{?_isa} >= %{freebl_version}

# This is needed to get the _tmpfilesdir macro we use for nscd.
%if %{with systemd}
BuildRequires: systemd
%else
# we need some default timezone file to manage /etc/localtime ourselves
BuildRequires: tzdata >= 2013h
%endif

# This GCC version introduced the -fstack-clash-protection option with
# the required semantics.
BuildRequires: gcc >= 4.8.5-25

# This RPM version introduced --g-libs.
%if 0%{?amzn}
BuildRequires: rpm-build >= 4.11.3-40.76.amzn1
%else
BuildRequires: rpm-build >= 4.11.3-38.el7
%endif

%define enablekernel 2.6.32
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

%ifarch %{multiarcharches}
# Need STT_IFUNC support
%ifarch ppc %{power64}
BuildRequires: binutils >= 2.20.51.0.2
Conflicts: binutils < 2.20.51.0.2
%else
%ifarch s390 s390x
# Needed for STT_GNU_IFUNC support for s390/390x
BuildRequires: binutils >= 2.23.52.0.1-8
Conflicts: binutils < 2.23.52.0.1-8
%else
# Default to this version
BuildRequires: binutils >= 2.19.51.0.10
Conflicts: binutils < 2.19.51.0.10
%endif
%endif
# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2
%else
# Need AS_NEEDED directive
# Need --hash-style=* support
BuildRequires: binutils >= 2.17.50.0.2-5
%endif
%ifarch ppc s390 s390x
BuildRequires: gcc >= 4.1.0-0.17
%endif
%if 0%{?_enable_debug_packages}
BuildRequires: elfutils >= 0.72
BuildRequires: rpm >= 4.2-0.56
%endif

%if %{without boostrap}
%if %{with testsuite}
# The testsuite builds static C++ binaries that require a C++ compiler
# and static C++ runtime from libstdc++-static.
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
BuildRequires: glibc-static
%endif
%endif


# Older audit packages owned /usr/lib{,64}/audit with different permissions.
Conflicts: audit < 2.3.0

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1

Prefix: %{_prefix}

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Group: Development/Libraries
Requires: %{name}-headers >= %{version}
Requires: %{name}%{?_isa} >= %{version}
Prefix: %{_prefix}

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
Requires: kernel-headers >= 2.2.1, %{name}%{?_isa} >= %{version}
BuildRequires: kernel-headers >= 2.6.22
Prefix: %{_prefix}

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
# glibc "nscd" sub-package
##############################################################################
%package -n nscd
Summary: A Name Service Caching Daemon (nscd).
Group: System Environment/Daemons
Requires: %{name} >= %{version}
%if %{without bootstrap}
Requires: libselinux >= 1.17.10-1
%endif
Requires: audit-libs >= 1.1.3

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.

##############################################################################
# glibc "utils" sub-package
##############################################################################
%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: %{name}%{?_isa} >= %{version}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

##############################################################################
# Prepare for the build.
##############################################################################
%prep

%setup -q -n %{glibcsrcdir} -b1

# Patch order is important as some patches depend on other patches and
# therefore the order must not be changed.
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch2007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch2011 -p1
%patch0012 -p1
%patch2013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0019 -p1
%patch0020 -p1
%patch1048 -p1
%patch2023 -p1
%patch0024 -p1
%patch0025 -p1
%patch1049 -p1
%patch2027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0034 -p1
%patch1051 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch1000 -p1
%patch0038 -p1
%patch1052 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1
%patch1053 -p1
%patch1010 -p1
%patch0039 -p1
%patch1054 -p1
%patch1055 -p1
%patch1056 -p1
%patch1057 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch1050 -p1
%patch1011 -p1
%patch1012 -p1
%patch1013 -p1
%patch1014 -p1
%patch1015 -p1
%patch1016 -p1
%patch1017 -p1
%patch1018 -p1
%patch1019 -p1
%patch1020 -p1
%patch1021 -p1
%patch1022 -p1
%patch1023 -p1
%patch1024 -p1
%patch1025 -p1
%patch1026 -p1
%patch1027 -p1
%patch1028 -p1
%patch1029 -p1
%patch1030 -p1
%patch1031 -p1
%patch1032 -p1
%patch0044 -p1
%patch0045 -p1
%patch1047 -p1
%patch1034 -p1
%patch1058 -p1
%patch1035 -p1
%patch1059 -p1
%patch1036 -p1
%patch1046 -p1
%patch1037 -p1
%patch1038 -p1
%patch2048 -p1
%patch1039 -p1
%patch1040 -p1
%patch1041 -p1
%patch1042 -p1
%patch1043 -p1
%patch1060 -p1
%patch1061 -p1
%patch2051 -p1
%patch1044 -p1
%patch1045 -p1
%patch2052 -p1
%patch0048 -p1
%patch0060 -p1
%patch1062 -p1
%patch1063 -p1
%patch2053 -p1
# Apply ldbl_high() patch for both ppc64le and ppc64.
%patch1110 -p1

# PPC64LE Patch set:
# 1064 to 1109.

%patch1064 -p1
%patch1065 -p1
%patch1066 -p1
%patch1067 -p1
%patch1068 -p1
%patch1069 -p1
%patch1070 -p1
%patch1071 -p1
%patch1072 -p1
%patch1073 -p1
%patch1074 -p1
%patch1075 -p1
%patch1076 -p1
%patch1077 -p1
%patch1078 -p1
%patch1079 -p1
%patch1080 -p1
%patch1081 -p1
%patch1082 -p1
%patch1083 -p1
%patch1084 -p1
%patch1085 -p1
%patch1086 -p1
%patch1087 -p1
%patch1088 -p1
%patch1089 -p1
%patch1090 -p1
%patch1091 -p1
%patch1092 -p1
%patch1093 -p1
%patch1094 -p1
%patch1095 -p1
%patch1096 -p1
%patch1097 -p1
%patch1098 -p1
%patch1099 -p1
%patch1100 -p1
%patch1101 -p1
%patch1102 -p1
%patch1103 -p1
%patch1104 -p1
%patch1105 -p1
%patch1106 -p1
%patch1107 -p1
%patch1108 -p1
%patch1109 -p1

%patch1112 -p1
# End of PPC64LE Patch Set.

%patch1122 -p1
%patch2055 -p1
%patch1499 -p1
%patch1500 -p1
%patch1501 -p1
%patch1502 -p1
%patch1503 -p1
%patch1504 -p1
%patch1505 -p1
%patch2060 -p1
%patch1506 -p1
%patch1508 -p1
%patch2062 -p1
%patch0061 -p1
%patch1509 -p1
%patch1510 -p1
%patch1511 -p1
%patch1512 -p1
%patch1513 -p1
%patch1514 -p1
%patch1515 -p1
%patch1516 -p1
%patch1517 -p1
%patch1518 -p1
%patch1519 -p1
%if %{with usrmerge}
%patch0062 -p1
%endif
%patch2063 -p1
%patch1520 -p1
%patch1521 -p1
%patch1522 -p1
# Start of IBM IFUNC patch set.
%patch1530 -p1
%patch1531 -p1
%patch1532 -p1
%patch1533 -p1
%patch1534 -p1
%patch1535 -p1
%patch1536 -p1
%patch1537 -p1
%patch1538 -p1
%patch1539 -p1
%patch1540 -p1
%patch1541 -p1
%patch1542 -p1
%patch1543 -p1
%patch1544 -p1
%patch1545 -p1
%patch1546 -p1
%patch1547 -p1
%patch1548 -p1
%patch1549 -p1
%patch1550 -p1
%patch1551 -p1
%patch1552 -p1
%patch1553 -p1
%patch1554 -p1
%patch1555 -p1
%patch1556 -p1
%patch1557 -p1
%patch1558 -p1
%patch1559 -p1
%patch1560 -p1
%patch1561 -p1
%patch1562 -p1
%patch1563 -p1
%patch1564 -p1
%patch1565 -p1
# Apply fixup patch for -33 in the series to make it LE safe.
%patch1566 -p1
%patch1567 -p1
# End of IBM IFUNC patch set.
%patch1570 -p1
%patch1571 -p1
%patch1572 -p1
%patch1573 -p1
%patch0063 -p1
%patch2064 -p1
%patch1574 -p1
%patch1575 -p1
%patch2065 -p1
%patch1576 -p1
%patch1577 -p1
%patch1578 -p1
%patch1608 -p1
%patch1579 -p1
%patch1580 -p1
%patch1581 -p1
%patch1582 -p1
%patch1583 -p1
%patch1584 -p1
%patch1585 -p1
%patch1586 -p1
%patch1587 -p1
%patch1588 -p1
%patch1589 -p1
%patch1590 -p1
%patch1591 -p1
%patch1592 -p1
%patch1593 -p1
%patch1594 -p1
%patch1595 -p1
%patch1596 -p1
%patch1597 -p1
%patch0066 -p1
%patch1598 -p1
%patch1599 -p1
%patch1600 -p1
%patch1601 -p1
%patch1602 -p1
%patch1603 -p1
%patch1604 -p1
%patch1605 -p1
%patch1606 -p1
%patch2066 -p1
%patch20670 -p1
%patch2067 -p1
%patch2068 -p1
%patch2069 -p1
%patch2070 -p1
%patch2071 -p1
%patch2072 -p1
%patch2073 -p1
%patch2074 -p1
%patch2075 -p1
%patch2076 -p1
%patch2077 -p1
%patch2078 -p1
%patch2079 -p1
%patch2080 -p1
%patch2081 -p1
%patch2082 -p1
%patch2083 -p1
%patch2084 -p1
%patch2085 -p1
%patch2086 -p1
%patch2087 -p1
%patch2088 -p1
%patch2089 -p1
%patch2090 -p1
%patch2091 -p1

# Rebase of microbenchmarks.
%patch1607 -p1
%patch1609 -p1
%patch1610 -p1
%patch1611 -p1

# Backport of POWER8 glibc optimizations for RHEL7.3
%patch1612 -p1
%patch1613 -p1
%patch1614 -p1
%patch1615 -p1
%patch1616 -p1
%patch1617 -p1
%patch1618 -p1
%patch1619 -p1
%patch1620 -p1
%patch1621 -p1
%patch1622 -p1
%patch1623 -p1

# Backport of upstream IBM z13 patches for RHEL 7.3
%patch1624 -p1
%patch1625 -p1
%patch1626 -p1
%patch1627 -p1
%patch1628 -p1
%patch1629 -p1
%patch1630 -p1
%patch1631 -p1
%patch1632 -p1
%patch1633 -p1
%patch1634 -p1
%patch1635 -p1
%patch1636 -p1
%patch1637 -p1
%patch1638 -p1
%patch1639 -p1
%patch1640 -p1
%patch1641 -p1
%patch1642 -p1
%patch1643 -p1
%patch1644 -p1
%patch1645 -p1
%patch1646 -p1
%patch1647 -p1
%patch1648 -p1
%patch1649 -p1
%patch1650 -p1
%patch1651 -p1
%patch1652 -p1
%patch1653 -p1
%patch1654 -p1

%patch1123 -p1
%patch1124 -p1

%patch1656 -p1
%patch1657 -p1
%patch1658 -p1
%patch1660 -p1
%patch0067 -p1
%patch1661 -p1
%patch1662 -p1
%patch1663 -p1

%patch1664 -p1
%patch1665 -p1
%patch1666 -p1
%patch1667 -p1
%patch1668 -p1
%patch1669 -p1
%patch1670 -p1
%patch1671 -p1
%patch1672 -p1

%patch1675 -p1

# RHBZ #1324427, parts 1 through 3
%patch1676 -p1
%patch1677 -p1
%patch1678 -p1

# RHBZ #1234449, parts 1 through 4
%patch1679 -p1
%patch1680 -p1
%patch1681 -p1
%patch1682 -p1

# RHBZ #1221046
%patch1683 -p1

# RHBZ #971416
%patch1684 -p1
%patch1685 -p1
%patch1686 -p1

# RHBZ #1302086
%patch1687 -p1
%patch1688 -p1
%patch1689 -p1
%patch1690 -p1
%patch1691 -p1
%patch1692 -p1
%patch1693 -p1
%patch1694 -p1
%patch1695 -p1
%patch1696 -p1
%patch1697 -p1

# RHBZ #1346397
%patch1698 -p1

# RHBZ #1211823
%patch1699 -p1

# RHBZ #1268050, parts 1 through 5
%patch1700 -p1
%patch1701 -p1
%patch1702 -p1
%patch1703 -p1
%patch1704 -p1

# RHBz #1296297, part 1 and 2.
%patch1705 -p1
%patch1706 -p1

# RHBZ #1027348, part 1 through 5.
%patch1707 -p1
%patch1708 -p1
%patch1709 -p1
%patch1710 -p1
%patch1711 -p1

%patch1712 -p1
%patch1713 -p1
%patch1714 -p1

%patch1715 -p1

# RHBZ #1256317, IS_IN backports, parts 1 through 22.
%patch1716 -p1
%patch1717 -p1
%patch1718 -p1
%patch1719 -p1
%patch1720 -p1
%patch1721 -p1
%patch1722 -p1
%patch1723 -p1
%patch1724 -p1
%patch1725 -p1
%patch1726 -p1
%patch1727 -p1
%patch1728 -p1
%patch1729 -p1
%patch1730 -p1
%patch1731 -p1
%patch1732 -p1
%patch1733 -p1
%patch1734 -p1
%patch1735 -p1
%patch1736 -p1
%patch1737 -p1

%patch1738 -p1
%patch1739 -p1

# RHBZ #1292018, patches 1 through 10.
%patch1740 -p1
%patch1741 -p1
%patch1742 -p1
%patch1743 -p1
%patch1744 -p1
%patch1745 -p1
%patch1746 -p1
%patch1747 -p1
%patch1748 -p1
%patch1749 -p1

%patch1750 -p1

# RHBZ #1298526, patch 1 of 5.
%patch1751 -p1
%patch1752 -p1
%patch1753 -p1
%patch1754 -p1
%patch1755 -p1
%patch1756 -p1
%patch0068 -p1
%patch1757 -p1
%patch17580 -p1
%patch1758 -p1
%patch1759 -p1
%patch2752 -p1
%patch1760 -p1
%patch1761 -p1
%patch1762 -p1
%patch1763 -p1
%patch1764 -p1
%patch1765 -p1
%patch1766 -p1
%patch1767 -p1
%patch1768 -p1
%patch1769 -p1
%patch1770 -p1
%patch1771 -p1
%patch1772 -p1
%patch1773 -p1
%patch1774 -p1
%patch1775 -p1
%patch1776 -p1
%patch1777 -p1
%patch1778 -p1
%patch1779 -p1
%patch1780 -p1
%patch1781 -p1
%patch1782 -p1
%patch1783 -p1
%patch1784 -p1
%patch1785 -p1
%patch1786 -p1
%patch1787 -p1
%patch1788 -p1
%patch1789 -p1
%patch1790 -p1
%patch1791 -p1
%patch1792 -p1
%patch1793 -p1
%patch1794 -p1
%patch1795 -p1
%patch1796 -p1
%patch1797 -p1
%patch1798 -p1
%patch1799 -p1
%patch1800 -p1
%patch1801 -p1
%patch1802 -p1
%patch1803 -p1
%patch1804 -p1
%patch1805 -p1
%patch1806 -p1
%patch1807 -p1
%patch1808 -p1
%patch1809 -p1
%patch1810 -p1
%patch1811 -p1
%patch1812 -p1
%patch1813 -p1
%patch1814 -p1
%patch1815 -p1
%patch1816 -p1
%patch1817 -p1
%patch1818 -p1
%patch1819 -p1
%patch1820 -p1
%patch1821 -p1
%patch1822 -p1
%patch1823 -p1
%patch1824 -p1
%patch1825 -p1
%patch1826 -p1
%patch1827 -p1
%patch1828 -p1
%patch1829 -p1
%patch1830 -p1
%patch1831 -p1
# RHBZ #841653 - Intel lock elision patch set.
%patch1832 -p1
%patch1833 -p1
%patch1834 -p1
%patch1835 -p1
%patch1836 -p1
%patch1837 -p1
%patch1838 -p1
%patch1839 -p1
%patch1840 -p1
%patch1841 -p1
%patch1842 -p1
%patch1843 -p1
%patch1844 -p1
%patch1845 -p1
%patch1846 -p1
%patch1847 -p1
%patch1848 -p1
%patch1849 -p1
# End of Intel lock elision patch set.
# RHBZ #731835 - IBM POWER lock elision patch set.
%patch1850 -p1
%patch1851 -p1
%patch1852 -p1
# End of IBM POWER lock elision patch set.

%patch1853 -p1
%patch1854 -p1

# Built-in list of syscall names.
%patch1855 -p1
%patch1856 -p1

%patch1857 -p1
%patch1858 -p1
%patch1859 -p1
%patch1860 -p1

%patch1861 -p1
%patch1862 -p1
%patch1863 -p1
%patch1864 -p1
%patch1865 -p1
%patch1866 -p1

%patch1867 -p1
%patch1868 -p1
%patch1869 -p1
%patch1870 -p1
%patch1871 -p1
%patch1872 -p1
%patch1873 -p1
%patch1874 -p1
%patch1875 -p1
%patch1876 -p1

%patch1877 -p1
%patch2092 -p1
%patch2093 -p1
%patch2094 -p1
%patch2095 -p1
%patch2096 -p1
%patch2097 -p1
%patch2098 -p1
%patch2099 -p1
%patch2100 -p1
%patch2101 -p1
%patch2102 -p1
%patch2103 -p1
%patch2104 -p1
%patch2105 -p1
%patch2106 -p1
%patch2107 -p1
%patch2108 -p1
%patch2109 -p1
%patch2110 -p1
%patch2111 -p1
%patch2112 -p1
%patch2113 -p1
%patch2114 -p1

%patch1878 -p1
%patch1879 -p1
%patch1880 -p1

%patch1881 -p1
%patch1882 -p1
%patch1883 -p1
%patch1884 -p1
%patch1885 -p1
%patch1886 -p1
%patch1887 -p1
%patch1888 -p1
%patch1889 -p1
%patch1890 -p1
%patch1891 -p1
%patch1892 -p1

%patch1893 -p1
%patch1894 -p1
%patch1895 -p1
%patch1896 -p1
%patch1897 -p1
%patch1898 -p1
%patch1899 -p1
%patch1900 -p1
%patch1901 -p1
%patch1902 -p1
%patch1903 -p1
%patch2500 -p1
%patch2501 -p1
%patch2502 -p1
%patch2503 -p1
%patch2504 -p1
%patch2505 -p1
%patch2506 -p1
%patch2507 -p1
%patch2508 -p1
%patch2509 -p1
%patch2510 -p1
%patch2511 -p1
%patch2512 -p1
%patch2513 -p1
%patch2514 -p1
%patch2515 -p1
%patch2516 -p1
%patch2517 -p1
%patch2518 -p1
%patch2519 -p1
%patch2520 -p1
%patch2521 -p1
%patch2522 -p1
%patch2523 -p1
%patch2524 -p1
%patch2525 -p1
%patch2526 -p1
%patch2527 -p1
%patch2528 -p1
%patch2529 -p1
%patch2530 -p1
%patch2531 -p1
%patch2532 -p1
%patch2533 -p1
%patch2534 -p1
%patch2535 -p1
%patch2536 -p1
%patch2537 -p1
%patch2538 -p1
%patch2539 -p1
%patch2540 -p1
%patch2541 -p1
%patch2542 -p1
%patch2543 -p1
%patch0069 -p1
%patch2544 -p1
%patch2545 -p1
%patch2546 -p1
%patch2547 -p1
%patch2548 -p1
%patch2549 -p1
%patch2550 -p1
%patch2551 -p1
%patch2552 -p1
%patch2553 -p1
%patch2554 -p1
%patch2555 -p1
%patch2556 -p1
%patch2557 -p1
%patch2558 -p1
%patch2559 -p1
%patch2560 -p1
%patch2561 -p1
%patch2562 -p1
%patch2563 -p1
%patch2564 -p1
%patch2565 -p1
%patch2566 -p1
%patch2567 -p1
%patch2568 -p1
%patch2569 -p1
%patch2570 -p1
%patch2571 -p1
%patch2572 -p1
%patch2573 -p1
%patch2574 -p1
%patch2575 -p1
%patch2576 -p1
%patch2577 -p1
%patch2578 -p1
%patch2579 -p1
%patch2580 -p1
%patch2581 -p1
%patch2582 -p1
%patch2583 -p1
%patch2584 -p1
%patch2585 -p1
%patch2586 -p1
%patch2587 -p1
%patch2588 -p1
%patch2589 -p1
%patch2590 -p1
%patch2591 -p1
%patch2592 -p1
%patch2593 -p1
%patch2594 -p1
%patch2595 -p1
%patch2596 -p1
%patch2597 -p1
%patch2598 -p1
%patch2599 -p1
%patch2600 -p1
%patch2601 -p1
%patch2602 -p1
%patch2603 -p1
%patch2604 -p1
%patch2605 -p1
%patch2606 -p1
%patch2607 -p1
%patch2608 -p1
%patch2609 -p1
%patch2610 -p1
%patch2611 -p1
%patch2612 -p1
%patch2613 -p1
%patch2614 -p1
%patch2615 -p1
%patch2616 -p1
%patch2617 -p1
%patch2618 -p1
%patch2619 -p1
%patch2620 -p1
%patch2621 -p1
%patch2622 -p1
%patch2623 -p1
%patch2624 -p1
%patch2625 -p1
%patch2626 -p1
%patch2627 -p1
%patch2628 -p1
%patch2629 -p1
%patch2630 -p1
%patch2631 -p1
%patch2632 -p1
%patch2633 -p1
%patch2634 -p1
%patch2635 -p1
%patch2636 -p1
%patch2637 -p1
%patch2638 -p1
%patch2639 -p1
%patch2640 -p1
%patch2641 -p1
%patch2642 -p1
%patch2643 -p1
%patch2644 -p1
%patch2645 -p1
%patch2646 -p1
%patch2647 -p1
%patch2648 -p1
%patch2649 -p1
%patch2650 -p1
%patch2651 -p1
%patch2652 -p1
%patch2653 -p1
%patch2654 -p1
%patch2655 -p1
%patch2656 -p1
%patch2657 -p1
%patch2658 -p1
%patch2659 -p1
%patch2660 -p1
%patch2661 -p1
%patch2662 -p1
%patch2663 -p1
%patch2664 -p1
%patch2665 -p1
%patch2666 -p1
%patch2667 -p1
%patch2668 -p1
%patch2669 -p1
%patch2670 -p1
%patch2671 -p1
%patch2672 -p1
%patch2673 -p1
%patch2674 -p1
%patch2675 -p1
%patch2676 -p1
%patch2677 -p1
%patch2678 -p1
%patch2679 -p1
%patch2680 -p1
%patch2681 -p1
%patch2682 -p1
%patch2683 -p1
%patch2684 -p1
%patch2685 -p1
%patch2686 -p1
%patch2687 -p1
%patch2688 -p1
%patch2689 -p1
%patch2690 -p1
%patch2691 -p1
%patch2692 -p1
%patch2693 -p1
%patch2694 -p1
%patch2695 -p1
%patch2696 -p1
%patch2697 -p1
%patch2698 -p1
%patch2699 -p1
%patch2700 -p1
%patch2701 -p1
%patch2702 -p1
%patch2703 -p1
%patch2704 -p1
%patch2705 -p1

%patch2706 -p1
%patch2707 -p1
%patch2708 -p1

%patch2709 -p1
%patch2710 -p1
%patch2711 -p1
%patch2712 -p1
%patch2713 -p1

%patch2714 -p1
%patch2715 -p1
%patch2716 -p1
%patch2717 -p1
%patch2718 -p1
%patch2719 -p1
%patch2720 -p1
%patch2721 -p1
%patch2722 -p1
%patch2723 -p1
%patch2724 -p1
%patch2725 -p1
%patch2726 -p1
%patch2727 -p1
%patch2728 -p1
%patch2729 -p1
%patch2730 -p1
%patch2731 -p1
%patch2732 -p1
%patch2733 -p1
%patch2734 -p1
%patch2735 -p1
%patch2736 -p1
%patch2737 -p1
%patch2738 -p1
%patch2739 -p1
%patch2740 -p1
%patch2741 -p1
%patch2742 -p1
%patch2743 -p1
%patch2744 -p1
%patch2745 -p1
%patch2746 -p1
%patch2747 -p1
%patch2748 -p1
%patch2749 -p1
%patch2750 -p1
%patch2751 -p1
%patch2753 -p1
%patch2754 -p1
%patch2755 -p1
%patch2756 -p1
%patch2757 -p1
%patch2758 -p1
%patch2759 -p1
%patch2760 -p1
%patch2761 -p1
%patch2762 -p1
%patch2763 -p1
%patch2764 -p1
%patch2765 -p1
%patch2766 -p1
%patch2767 -p1
%patch2768 -p1
%patch2769 -p1
%patch2770 -p1
%patch2771 -p1
%patch2772 -p1
%patch2773 -p1
%patch2774 -p1
%patch2775 -p1
%patch2776 -p1
%patch2777 -p1
%patch2778 -p1
%patch2779 -p1
%patch2780 -p1
%patch2781 -p1
%patch2782 -p1
%patch2783 -p1
%patch2784 -p1
%patch2785 -p1
%patch2786 -p1
%patch2787 -p1
%patch2788 -p1
%patch2789 -p1
%patch2790 -p1
%patch2791 -p1
%patch2792 -p1
%patch2793 -p1
%patch2794 -p1
%patch2795 -p1
%patch2796 -p1
%patch2797 -p1
%patch2798 -p1
%patch2799 -p1
%patch2800 -p1
%patch2801 -p1
%patch2802 -p1
%patch2803 -p1
%patch2804 -p1
%patch2805 -p1
%patch2806 -p1
%patch2807 -p1
%patch2808 -p1
%patch2809 -p1

# Amazon patches
%patch10000 -p1

##############################################################################
# %%prep - Additional prep required...
##############################################################################

# Verify checksum of certain files in the source tree and exit
# with a failure if they don't match expected values. The most
# important purpose for this verification is patched binary files
# which may get corrupted by editors. Check them here to make sure
# they are OK after patching.
if md5sum -c %{SOURCE2}; then
    continue
else
    echo "md5sum: Verification of md5 sum for binary source files failed."
    exit 1
fi

# Remove all files generated from patching.
find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
touch locale/programs/*-kw.h

# RHBZ #1640764: Ensure plural.c is current to prevent regenerating it (bison)
touch intl/plural.c

##############################################################################
# Build glibc...
##############################################################################
%build

# We build using the native system compilers.
GCC=gcc
GXX=g++

# Log system information.
uname -a
cat /proc/cpuinfo
cat /proc/meminfo
df

BuildFlags="-mtune=generic"

##############################################################################
# %%build - Generic options.
##############################################################################
BuildFlags="$BuildFlags -fasynchronous-unwind-tables"
BuildFlags="$BuildFlags -fstack-clash-protection"
# Add -DNDEBUG unless using a prerelease
case %{version} in
  *.*.9[0-9]*) ;;
  *)
     BuildFlags="$BuildFlags -DNDEBUG"
     ;;
esac
EnableKernel="--enable-kernel=%{enablekernel}"
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc
AddOns=`echo */configure | sed -e 's!/configure!!g;s!\(nptl\|rtkaio\|powerpc-cpu\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`
%ifarch %{rtkaioarches}
AddOns=,rtkaio$AddOns
%endif

##############################################################################
# build()
#	Build glibc in `build-%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, add-ons, kernel
#	version, multiarch support, system tap support, etc.
##############################################################################
build()
{
builddir=build-%{target}${1:+-$1}
${1+shift}
rm -rf $builddir
mkdir $builddir
pushd $builddir
build_CFLAGS="$BuildFlags -g -O3 $*"
# Some configure checks can spuriously fail for some architectures if
# unwind info is present
configure_CFLAGS="$build_CFLAGS -fno-asynchronous-unwind-tables"
../configure CC="$GCC" CXX="$GXX" CFLAGS="$configure_CFLAGS" \
	--prefix=%{_prefix} \
	--enable-add-ons=nptl$AddOns \
	--with-headers=%{_includedir} $EnableKernel --enable-bind-now \
	--build=%{target} \
%ifarch %{multiarcharches}
        --enable-multi-arch \
%else
        --disable-multi-arch \
%endif
%ifarch %{elisionarches}
	--enable-lock-elision=yes \
%endif
	--enable-obsolete-rpc \
	--enable-systemtap \
  --disable-static \
	${core_with_options} \
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

make %{?_smp_mflags} -r CFLAGS="$build_CFLAGS" %{silentrules}
popd
}

##############################################################################
# Build glibc for the default set of options.
##############################################################################
build

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
make -j1 install_root=$RPM_BUILD_ROOT install -C build-%{target} %{silentrules}

# NPTL <bits/stdio-lock.h> is not usable outside of glibc, so include
# the generic one (#162634)
cp -a bits/stdio-lock.h $RPM_BUILD_ROOT%{_includedir}/bits/stdio-lock.h
# And <bits/libc-lock.h> needs sanitizing as well.
cp -a releng/libc-lock.h $RPM_BUILD_ROOT%{_includedir}/bits/libc-lock.h

# XXX: What is this for?
ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_libdir}/libbsd.a

##############################################################################
# Install configuration files for services
##############################################################################

install -p -m 644 releng/nsswitch.conf $RPM_BUILD_ROOT%{_sysconfdir}/nsswitch.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/default
install -p -m 644 nis/nss $RPM_BUILD_ROOT%{_sysconfdir}/default/nss

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_initddir}
install -m 755 nscd/nscd.init $RPM_BUILD_ROOT/%{_initddir}/nscd

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
> $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nscd
> $RPM_BUILD_ROOT%{_sysconfdir}/gai.conf

# Include %{_prefix}/%{_lib}/gconv/gconv-modules.cache
> $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache

strip -g $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.o

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

# Remove the old nss modules.
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1

# Ugly hack for buggy rpm
ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# Make sure %config files have the same timestamp
touch -r releng/glibc.spec.in $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT%{_sysconfdir}/rpc

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/debug

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/{db,run}/nscd
touch $RPM_BUILD_ROOT%{_localstatedir}/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT%{_localstatedir}/run/nscd/{socket,nscd.pid}

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/ldconfig

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

%files devel
%defattr(-,root,root)
%{_includedir}/gnu/stubs-64.h
%{_libdir}/Mcrt1.o
%{_libdir}/Scrt1.o
%{_libdir}/crt1.o
%{_libdir}/crti.o
%{_libdir}/crtn.o
%{_libdir}/gcrt1.o
%{_libdir}/libBrokenLocale.so
%{_libdir}/libanl.so
%{_libdir}/libbsd-compat.a
%{_libdir}/libbsd.a
%{_libdir}/libc.so
%{_libdir}/libc_nonshared.a
%{_libdir}/libcidn.so
%{_libdir}/libcrypt.so
%{_libdir}/libdl.so
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libm.so
%{_libdir}/libmcheck.a
%{_libdir}/libnsl.so
%{_libdir}/libnss_compat.so
%{_libdir}/libnss_db.so
%{_libdir}/libnss_dns.so
%{_libdir}/libnss_files.so
%{_libdir}/libnss_hesiod.so
%{_libdir}/libnss_nis.so
%{_libdir}/libnss_nisplus.so
%{_libdir}/libpthread.so
%{_libdir}/libpthread_nonshared.a
%{_libdir}/libresolv.so
%{_libdir}/librpcsvc.a
%{_libdir}/librt.so
%{_libdir}/libthread_db.so
%{_libdir}/libutil.so

%files headers
%defattr(-,root,root)
%exclude %{_includedir}/gnu/stubs-64.h
%{_includedir}/*

%files utils
%defattr(-,root,root)
%{_bindir}/memusage
%{_bindir}/memusagestat
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/xtrace

%files -n nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%dir %attr(0755,root,root) %{_localstatedir}/run/nscd
%dir %attr(0755,root,root) %{_localstatedir}/db/nscd
%config %{_initddir}/nscd
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/services
%ghost %config(missingok,noreplace) %{_sysconfdir}/sysconfig/nscd
%{_sbindir}/nscd

%exclude %{_datadir}
%exclude %{_bindir}
%exclude %{_sbindir}
%exclude %{_libexecdir}
%exclude %{_localstatedir}
%exclude %{_sysconfdir}
%exclude %{_libdir}
%exclude %{_prefix}/var/db/Makefile

%changelog
* Thu Nov 28 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 21 2019 kaos-source-imports <nobody@amazon.com>
- import source package EL7/glibc-2.17-292.el7
- import source package EL7/glibc-2.17-260.el7_6.6
- import source package EL7/glibc-2.17-260.el7_6.5

* Tue Apr 30 2019 Arjun Shankar <arjun@redhat.com> - 2.17-292
- Avoid iconv hang on invalid multi-byte sequences (#1427734)

* Tue Apr 30 2019 Florian Weimer <fweimer@redhat.com> - 2.17-291
- Use versioned Obsoletes: for nss_db (#1703565)

* Mon Apr 29 2019 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-260.el7_6.4

* Mon Apr  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-290
- Adjust to find-debuginfo.sh changes (#1661508)

* Mon Apr  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-289
- ja_JP: Add new Japanese Era name (#1555189)

* Wed Mar 27 2019 Arjun Shankar <arjun@redhat.com> - 2.17-288
- Unify and improve pthread_once implementation for all architectures (#1163509)

* Tue Mar 26 2019 DJ Delorie <dj@redhat.com> - 2.17.287
- malloc: Always call memcpy in _int_realloc (#1662842)

* Wed Mar 20 2019 Carlos O'Donell <carlos@redhat.com> - 2.17-286
- Update comments in nscd.conf and nsswitch.conf (#1488370)

* Tue Mar 19 2019 Arjun Shankar <arjun@redhat.com> - 2.17-285
- intl: Ensure plural.c is current to prevent regenerating it (#1640764)

* Tue Mar  5 2019 Florian Weimer <fweimer@redhat.com> - 2.17-284
- Update <netinet/in.h> to include IP*_PMTUDISC_OMIT and others (#1684874)

* Fri Mar  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-283
- elf: Adjust the big PT_NOTE test to exercise the bug in more cases (#1579739)

* Fri Mar  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-282
- x86: Fix incorrect selection of string functions (#1641981)

* Fri Mar  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-281
- elf: Avoid stack overflow with large PT_NOTE segments (#1579739)

* Fri Mar  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-280
- resolv: Fully initialize sendmmsg argument data (#1579354)

* Fri Mar  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-279
- Improve formatting of Netlink error messages (#1443872)

* Fri Mar  1 2019 Florian Weimer <fweimer@redhat.com> - 2.17-278
- Run resolv/tst-inet_aton_exact test (#1673465)

* Thu Feb 28 2019 Florian Weimer <fweimer@redhat.com> - 2.17-277
- getifaddrs could return interfaces with ifa_name set to NULL (#1472832)

* Thu Feb 28 2019 Florian Weimer <fweimer@redhat.com> - 2.17-276
- Terminate process on invalid netlink response from kernel (#1443872)

* Thu Feb 28 2019 Florian Weimer <fweimer@redhat.com> - 2.17-275
- resolv: Support host names with trailing dashes (#1039304)

* Thu Feb 28 2019 Florian Weimer <fweimer@redhat.com> - 2.17-274
- CVE-2016-10739: Reject trailing characters in getaddrinfo (#1673465)

* Thu Feb 28 2019 Carlos O'Donell <carlos@redhat.com> - 2.17-273
- Update syscall list for Linux 4.20 (#1657015)

* Wed Feb 20 2019 Arjun Shankar <arjun@redhat.com> - 2.17-272
- glibc-headers: Add ipc STAT_ANY constants (#1592475)

* Tue Feb 19 2019 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-260.el7_6.3

* Wed Feb 13 2019 Arjun Shankar <arjun@redhat.com> - 2.17-271
- localedata: Make IBM273 compatible with ISO-8859-1 (#1591268)

* Mon Jan 28 2019 Patsy Griffin Franklin <pfrankli@redhat.com> - 2.17-270
- Fix pldd race condition that may leave the process stopped after
  detaching. (#1609067)

* Tue Jan 22 2019 DJ Delorie <dj@redhat.com> - 2.17-269
- libanl: properly cleanup if first helper thread creation failed (#1646373)

* Mon Jan 21 2019 DJ Delorie <dj@redhat.com> - 2.17-268
- Add note about missing test case for BZ1457479 (#1635325)

* Thu Dec 20 2018 Florian Weimer <fweimer@redhat.com> - 2.17-267
- elf: Fix data race in _dl_profile_fixup (#1630440)

* Wed Dec 19 2018 Florian Weimer <fweimer@redhat.com> - 2.17-266
- Fix i386 sigaction sa_restorer initialization (#1579730)

* Wed Dec 19 2018 Florian Weimer <fweimer@redhat.com> - 2.17-265
- Fix compilation error in stdlib/tst-strtod-overflow.c (#1647490)

* Thu Dec 13 2018 DJ Delorie <dj@redhat.com> - 2.17-264
- aarch64: Disable lazy symbol binding of TLSDESC (#1639524)

* Tue Nov 27 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-260.el7

* Wed Nov 14 2018 Andrew Egelhofer <egelhofe@amazon.com>
- Patch gen-posix-conf-vars.awk script to work with AWK3
- import source package EL7/glibc-2.17-260.el7

* Fri Nov  9 2018 Florian Weimer <fweimer@redhat.com> - 2.17-263
- Reduce RAM requirements for stdlib/test-bz22786 (#1647490)

* Wed Nov  7 2018 Florian Weimer <fweimer@redhat.com> - 2.17-262
- libio vtable validation improvements (#1595191)

* Wed Nov  7 2018 Florian Weimer <fweimer@redhat.com> - 2.17-261
- Update support/ to the most recent upstream version (#1595191)

* Wed Jun 27 2018 Patsy Franklin <pfrankli@redhat.com> - 2.17-260
- Update glibc-rh1560641.patch to initialize pad outside
  the conditional eliminating an uninitialized byte warning from
  valgrind. (#1560641)

* Fri Jun 15 2018 Arjun Shankar <arjun@redhat.com> - 2.17-259
- Correctly set errno when send() fails on i686 (#1550080)

* Tue Jun 12 2018 Carlos O'Donell <carlos@redhat.com> - 2.17-258
- Fix dynamic string token substitution in DT_RPATH etc. (#1447808, #1540480)
- Additional robust mutex fixes (#1401665)

* Tue Jun 12 2018 Carlos O'Donell <carlos@redhat.com> - 2.17-257
- Improve process-shared robust mutex support (#1401665)

* Tue Jun 12 2018 Carlos O'Donell <carlos@redhat.com> 2.17-256
- CVE-2017-16997: Correctly handle DT_RPATH (#1540480).
- Correctly process "$ORIGIN" element in DT_RPATH or DT_NEEDED (#1447808).

* Tue Jun 12 2018 Carlos O'Donell <codonell@redhat.com> - 2.17-255
- Make transition from legacy nss_db easier (#1408964)

* Mon Jun 11 2018 Arjun Shankar <arjun@redhat.com> - 2.17-254
- nptl: Avoid expected SIGALRM in most tests (#1372304)

* Fri Jun  8 2018 Patsy Franklin <pfrankli@redhat.com> - 2.17-253
- Add support for el_GR@euro locale.  Update el_GR, ur_IN and
  wal_ET locales.  (#1448107)

* Fri Jun  8 2018 Arjun Shankar <arjun@redhat.com> - 2.17-252
- Do not scale NPTL tests with available number of CPUs (#1526193)

* Thu Jun  7 2018 Arjun Shankar <arjun@redhat.com> - 2.17-251
- Correctly set errno when send() fails on s390 and s390x (#1550080)

* Wed Jun  6 2018 Patsy Franklin <pfrankli@redhat.com> - 2.17-250
- Initialize pad field in sem_open. (#1560641)

* Mon Jun  4 2018 Arjun Shankar <arjun@redhat.com> - 2.17-249
- getlogin_r: Return early when process has no associated login UID (#1563046)

* Mon Jun  4 2018 Arjun Shankar <arjun@redhat.com> - 2.17-248
- Return static array, not local array from transliteration function (#1505500)

* Mon Jun  4 2018 Arjun Shankar <arjun@redhat.com> - 2.17-247
- Re-write multi-statement strftime_l macros using better style (#1505477)

* Mon Jun  4 2018 Arjun Shankar <arjun@redhat.com> - 2.17-246
- Fix pthread_barrier_init typo (#1505451)

* Wed May 23 2018 Florian Weimer <fweimer@redhat.com> - 2.17-245
- CVE-2018-11237: AVX-512 mempcpy for KNL buffer overflow (#1579809)

* Wed May 23 2018 Florian Weimer <fweimer@redhat.com> - 2.17-244
- resolv: Fix crash after memory allocation failure (#1579727)

* Wed May 23 2018 Florian Weimer <fweimer@redhat.com> - 2.17-243
- CVE-2018-11236: Path length overflow in realpath (#1579742)

* Tue May 22 2018 DJ Delorie <dj@redhat.com> - 2.17-242
- S390: fix sys/ptrace.h to make it includible again after
  asm/ptrace.h (#1457479)

* Tue May 22 2018 Florian Weimer <fweimer@redhat.com> - 2.17-241
- x86: setcontext, makecontext alignment issues (#1531168)

* Wed May 16 2018 DJ Delorie <dj@redhat.com> - 2.17-240
- Remove abort() warning in manual (#1577333)

* Wed May 16 2018 DJ Delorie <dj@redhat.com> - 2.17-239
- Add Open File Description (OFL) locks. (#1461231)

* Sun May 13 2018 Patsy Franklin <pfrankli@redhat.com> - 2.17-238
- Properly handle more invalid --install-langs arguments. (#1349982)

* Fri May 11 2018 DJ Delorie <dj@redhat.com> - 2.17-237
- Add O_TMPFILE macro (#1471405)
- Update syscall names list to kernel 4.16 (#1563747)
- Include <linux/falloc.h> in bits/fcntl-linux.h. (#1476120)
- Fix netgroup cache keys. (#1505647)
- Update ptrace constants. (#1457479)

* Thu May  3 2018 Arjun Shankar <arjun@redhat.com> - 2.17-236
- Fix strfmon_l so that it groups digits (#1307241)

* Thu May  3 2018 Arjun Shankar <arjun@redhat.com> - 2.17-235
- CVE-2018-6485: Integer overflow in posix_memalign in memalign (#1548002)

* Tue Apr 17 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-222.el7

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-234
- Adjust spec file for compiler warnings cleanup (#1505492)
- Drop ports add-on
- Do not attempt to disable warnings-as-errors on s390x

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-233
- Compiler warnings cleanup, phase 7 (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-232
- Compiler warnings cleanup, phase 6 (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-231
- Compiler warnings cleanup, phase 5 (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-230
- Compiler warnings cleanup, phase 4 (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-229
- Compiler warnings cleanup, phase 3 (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-228
- Compiler warnings cleanup, phase 2 (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-227
- Fix downstream-specific compiler warnings (#1505492)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-226
- rtkaio: Do not define IN_MODULE (#1349967)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-225
- Fix K&R function definitions in libio (#1566623)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-224
- Fix type errors in string tests (#1564638)

* Fri Apr 13 2018 Florian Weimer <fweimer@redhat.com> - 2.17-223
- Make nscd build reproducible for verification (#1505492)

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 2.17-222
- Restore internal GLIBC_PRIVATE symbols for use during upgrades (#1523119)

* Fri Jan 19 2018 Carlos O'Donell <carlos@redhat.com> - 2.17-221
- CVE-2018-1000001: Fix realpath() buffer underflow (#1534635)
- i386: Fix unwinding for 32-bit C++ application (#1529982)
- Reduce thread and dynamic loader stack usage (#1527904)
- x86-64: Use XSAVE/XSAVEC more often during lazy symbol binding (#1528418)

* Tue Dec 5 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-196.el7_4.2

* Fri Nov 17 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-220
- Update HWCAP bits for IBM POWER9 DD2.1 (#1503854)

* Fri Nov 17 2017 Florian Weimer <fweimer@redhat.com> - 2.17-219
- Rebuild with newer gcc for aarch64 stack probing fixes (#1500475)

* Tue Nov  7 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-218
- Improve memcpy performance for POWER9 DD2.1 (#1498925)

* Thu Nov  2 2017 Florian Weimer <fweimer@redhat.com> - 2.17-217
- Update Linux system call list to kernel 4.13 (#1508895)

* Thu Nov  2 2017 Florian Weimer <fweimer@redhat.com> - 2.17-216
- x86-64: Use XSAVE/XSAVEC in the ld.so trampoline (#1504969)

* Thu Nov  2 2017 Florian Weimer <fweimer@redhat.com> - 2.17-215
- CVE-2017-15670: glob: Fix one-byte overflow with GLOB_TILDE (#1504809)
- CVE-2017-15804: glob: Fix buffer overflow in GLOB_TILDE unescaping (#1504809)

* Sat Oct 21 2017 Patsy Franklin <pfrankli@redhat.com> - 2.17-214
- Fix check-localplt test failure. 
- Include ld.so in check-localplt test. (#1440250)

* Thu Oct 19 2017 Florian Weimer <fweimer@redhat.com> - 2.17-213
- Fix build warning in locarchive.c (#1349964)

* Wed Oct 18 2017 Florian Weimer <fweimer@redhat.com> - 2.17-212
- Hide reference to mktemp in libpthread (#1349962)

* Wed Oct 18 2017 Florian Weimer <fweimer@redhat.com> - 2.17-211
- Implement fopencookie hardening (#1372305)

* Wed Oct 18 2017 Florian Weimer <fweimer@redhat.com> - 2.17-210
- x86-64: Support __tls_get_addr with an unaligned stack (#1468807)

* Wed Oct 18 2017 Florian Weimer <fweimer@redhat.com> - 2.17-209
- Define CLOCK_TAI in <time.h> (#1448822)

* Mon Oct 16 2017 Florian Weimer <fweimer@redhat.com> - 2.17-208
- Compile glibc with -fstack-clash-protection (#1500475)

* Thu Oct 12 2017 Florian Weimer <fweimer@redhat.com> - 2.17-207
- aarch64: Avoid invalid relocations in the startup code (#1500908)

* Fri Oct  6 2017 Patsy Franklin <pfrankli@redhat.com> - 2.17-206
- Fix timezone test failures on large parallel builds. (#1234449, #1378329)

* Fri Oct  6 2017 DJ Delorie <dj@redhat.com> - 2.17-205
- Handle DSOs with no PLT (#1445781)

* Fri Oct  6 2017 DJ Delorie <dj@redhat.com> - 2.17-204
- libio: Implement vtable verification (#1398413)

* Thu Oct  5 2017 Arjun Shankar <arjun@redhat.com> - 2.17-203
- Fix socket system call selection on s390x (#1498566).
- Use different construct for protected visibility in IFUNC tests (#1445644)

* Fri Sep 29 2017 Florian Weimer <fweimer@redhat.com> - 2.17-202
- Rebase the DNS stub resolver and getaddrinfo to the glibc 2.26 version
- Support an arbitrary number of search domains in the stub resolver (#677316)
- Detect and apply /etc/resolv.conf changes in libresolv (#1432085)
- CVE-2017-1213: Fragmentation attacks possible when ENDS0 is enabled
  (#1487063)
- CVE-2016-3706: Stack (frame) overflow in getaddrinfo when called
  with AF_INET, AF_INET6 (#1329674)
- CVE-2015-5180: resolv: Fix crash with internal QTYPE (#1497131)
- CVE-2014-9402: denial of service in getnetbyname function (#1497132)
- Fix getaddrinfo to handle certain long lines in /etc/hosts (#1452034)
- Make RES_ROTATE start with a random name server (#1257639)
- Stricter IPv6 address parser (#1484034)
- Remove noip6dotint support from the stub resolver (#1482988)
- Remove partial bitstring label support from the stub resolver
- Remove unsupported resolver hook functions from the API
- Remove outdated RR type classification macros from the API
- hesiod: Always use TLS resolver state
- hesiod: Avoid non-trust-boundary crossing heap overflow in get_txt_records

* Tue Sep 26 2017 DJ Delorie <dj@redhat.com> - 2.17.201
- Fix hang in nscd cache prune thread (#1435615)

* Thu Sep 21 2017 Patsy Franklin <pfrankli@redhat.com> - 2.17-200
- Add binary timezone test data files (#1234449, #1378329)

* Wed Sep 20 2017 DJ Delorie <dj@redhat.com> - 2.17.198
- Add support for new IBM z14 (s390x) instructions (#1375235)

* Wed Aug 30 2017 Heath Petty <hpetty@amazon.com>
- Don't enable elision support for x86_64

* Wed Aug 16 2017 DJ Delorie <dj@redhat.com> - 2.17-197
- Fix compile warnings in malloc (#1347277)
- Fix occasional tst-malloc-usable failures (#1348000)
- Additional chunk hardening in malloc (#1447556)
- Pointer alignment fix in nss group merge (#1463692)
- Fix SIGSEGV when LD_LIBRARY_PATH only has non-existing paths (#1443236)

* Wed Aug 2 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-196.el7

* Tue Jul 25 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-157.el7_3.5

* Tue Jun 20 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-157.el7_3.4

* Fri Jun 16 2017 Florian Weimer <fweimer@redhat.com> - 2.17-196
- CVE-2017-1000366: Avoid large allocas in the dynamic linker (#1452721)

* Thu Jun 15 2017 Frederick Lefebvre <fredlef@amazon.com>
- Add constraints on LD_LIBRARY_PATH, LD_PRELOAD and LD_AUDIT

* Fri Jun  9 2017 Florian Weimer <fweimer@redhat.com> - 2.17-195
- Rounding issues on POWER (#1457177)

* Fri May 26 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-157.el7_3.2

* Wed Apr 26 2017 Florian Weimer <fweimer@redhat.com> - 2.17-194
- Use a built-in list of system call names (#1439165)

* Tue Apr 18 2017 Florian Weimer <fweimer@redhat.com> - 2.17-193
- Inhibit FMA while compiling sqrt, pow (#1413638)

* Wed Mar 29 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-192
- Exclude lock elision support for older Intel hardware with
  Intel TSX that has hardware errata (#841653).

* Tue Mar 28 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-191
- Add transparent lock elision for default POSIX mutexes on
  IBM POWER hardware with support for IBM POWER HTM (#731835).

* Tue Mar 28 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-190
- Add transparent lock elision for default POSIX mutexes on
  Intel hardware with support for Intel TSX (#841653).
- Update dynamic loader trampoline for Intel Skylake server (#1421155).

* Wed Mar 15 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-189
- Update dynamic loader trampoline for Intel SSE, AVX, and AVX512 usage (#1421155)

* Wed Mar 15 2017 Carlos O'Donell <carlos@redhat.com> - 2.17-188
- Improve exp() and pow() performance in libm (#1409611)
- Add optimized strcmp and strncmp for IBM POWER9 hardware (#1320947)

* Tue Mar 14 2017 Patsy Franklin <pfrankl@redhat.com> - 2.17-187
- Define MSG_FASTOPEN. (#1387874)

* Tue Mar 14 2017 Patsy Franklin <pfrankl@redhat.com> - 2.17-186
- Update patch for glibc-rh1288613.patch to include tst-res_hconf_reorder
  in the list of tests to be built and run. (#1367804)

* Tue Mar 14 2017 Florian Weimer <fweimer@redhat.com> - 2.17-185
- math: Regenerate ULPs for POWER (#1385004)

* Thu Mar  9 2017 Martin Sebor <msebor@redhat.com> - 2.17-184
- Correct s390 definition of SIZE_MAX (#1385003)

* Thu Mar  9 2017 Martin Sebor <msebor@redhat.com> - 2.17-183
- Fix CVE-2015-8776 glibc: Segmentation fault caused by passing
  out-of-range data to strftime() (#1374658)

* Thu Mar  9 2017 Martin Sebor <msebor@redhat.com> - 2.17-182
- Fix CVE-2015-8778: Integer overflow in hcreate and hcreate_r (#1374657)

* Wed Mar  8 2017 DJ Delorie <dj@redhat.com> - 2.17-181
- Fix rare case where calloc may not zero memory properly (#1430477)

* Wed Mar  8 2017 Florian Weimer <fweimer@redhat.com> - 2.17-180
- malloc: additional unlink hardening for non-small bins (#1326739)

* Wed Mar  8 2017 Martin Sebor <msebor@redhat.com> - 2.17-179
- Add improvements and optimizations to take advantage of the new
  z13 processor design (#1380680)

* Wed Mar  8 2017 Martin Sebor <msebor@redhat.com> - 2.17-178
- Backport the latest POWER8 performance optimizations (#1385004)

* Tue Mar  7 2017 DJ Delorie <dj@redhat.com> - 2.17-177
- LD_POINTER_GUARD in the environment is not sanitized (#1383951)

* Tue Mar  7 2017 DJ Delorie <dj@redhat.com> - 2.17-176
- Fix cmpli usage in power6 memset. (#1418997)

* Mon Mar  6 2017 Martin Sebor <msebor@redhat.com> - 2.17-175
- Avoid accessing user-controlled stdio locks in forked child (#1322544)

* Mon Mar  6 2017 DJ Delorie <dj@redhat.com> - 2.17-174
- Fix unbounded stack allocation in catopen function (#1374654)

* Mon Mar  6 2017 DJ Delorie <dj@redhat.com> - 2.17-173
- Fix unbounded stack allocation in nan* functions (#1374652)

* Fri Mar  3 2017 Martin Sebor <msebor@redhat.com> - 2.17-172
- Handle /var/cache/ldconfig/aux-cache corruption (#1325138)

* Wed Mar  1 2017 DJ Delorie <dj@redhat.com> - 2.17-171
- Make padding in struct sockaddr_storage explicit (#1338672)

* Wed Mar  1 2017 Florian Weimer <fweimer@redhat.com> - 2.17-170
- Add AF_VSOCK/PF_VSOCK, TCP_TIMESTAMP (#1417205)

* Tue Feb 28 2017 Martin Sebor <msebor@redhat.com> - 2.17-169
- Define <inttypes.h> and <stdint.h> macros unconditionally (#1318877)

* Tue Feb 28 2017 Martin Sebor <msebor@redhat.com> - 2.17-168
- Backport the groups merging feature (#1298975)

* Tue Feb 28 2017 Florian Weimer <fweimer@redhat.com> - 2.17-167
- Fix sunrpc UDP client timeout handling (#1228114)

* Tue Feb 28 2017 Florian Weimer <fweimer@redhat.com> - 2.17-166
- Add "sss" service to the automount database in nsswitch.conf (#1392540)

* Mon Feb 27 2017 Florian Weimer <fweimer@redhat.com> - 2.17-165
- Fix use of uninitialized data in getaddrinfo with nscd (#1324568)
- Remove the "power8" AT_PLATFORM directory (#1404435)
- Fix profil on aarch64 (#1144516)

* Tue Feb 21 2017 Martin Sebor <msebor@redhat.com> - 2.17-164
- Fix TOC stub on powerpc64 clone() (#1398244)

* Wed Feb 15 2017 Florian Weimer <fweimer@redhat.com> - 2.17-163
- stdio buffer auto-tuning should reject large buffer sizes (#988869)

* Tue Feb 14 2017 Florian Weimer <fweimer@redhat.com> - 2.17-162
- Backport support/ subdirectory from upstream (#1418978)
- Fix deadlock between fork, malloc, flush (NULL) (#906468)

* Fri Jan 27 2017 Patsy Franklin <pfrankl@redhat.com> - 2.17-161
- Fix tst-cancel17/tst-cancelx17 was sometimes segfaulting.
  Wait for the read to finish before returning. (#1337242)

* Wed Jan 25 2017 Florian Weimer <fweimer@redhat.com> - 2.17-160
- Add internal-only support for O_TMPFILE (#1330705)

* Wed Dec 7 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-157.el7_3.1

* Thu Nov 3 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-157.el7

* Thu Oct 20 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-158
- Do not set initgroups in default nsswitch.conf (#1366569)
- nss_db: Request larger buffers for long group entries (#1318890)
- nss_db: Fix get*ent crash without preceding set*ent (#1213603)
- nss_db: Fix endless loop in services database processing (#1370630)

* Thu Aug 11 2016 Florian Weimer <fweimer@redhat.com> - 2.17-157
- Rebuild with updated binutils (#1268008)

* Wed Aug 3 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-106.el7_2.8

* Tue Jul 19 2016 Florian Weimer <fweimer@redhat.com> - 2.17-156
- malloc arena free free list management fix (#1276753)

* Wed Jun 29 2016 Florian Weimer <fweimer@redhat.com> - 2.17-155
- Basic validity check for locale-archive.tmpl (#1350733)

* Wed Jun 22 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-153
- Add Intel AVX-512 optimized routines (#1298526).

* Wed Jun 22 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-151
- Improve malloc peformance in low-memory situations (#1255822).

* Wed Jun 22 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-150
- Improve performance on Intel Knights Landing/Silvermont (#1292018).

* Tue Jun 21 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-149
- Improve performance on Intel Purley (#1335286).

* Mon Jun 20 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-148
- Support upstream build infrastrucutre changes (#1256317).

* Sun Jun 19 2016 Florian Weimer <fweimer@redhat.com> - 2.17-147
- CVE-2016-3075: Stack overflow in nss_dns_getnetbyname_r (#1321993)

* Sun Jun 19 2016 Carlos O'Donell <carlso@redhat.com> - 2.17-146
- s390: Restore signal mask on setcontext/swapcontext (#1249114).
- s390: Fix backtrace in the presence of makecontext (#1249115).

* Fri Jun 17 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-145
- Fix times() handling of EFAULT when buf is NULL (#1308728).

* Fri Jun 17 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-144
- Fix sem_post/sem_wait race causing sem_post to return EINVAL (#1027348).

* Fri Jun 17 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-143
- Support installing only those locales specified by the RPM macro
  %%_install_langs (#1296297).

* Fri Jun 17 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-142
- Fix Linux kernel UAPI header synchronization for IPv6 (#1268050).

* Fri Jun 17 2016 Florian Weimer <fweimer@redhat.com> - 2.17-141
- Update BIG5-HKSCS charmap to HKSCS-2008 (#1211823)

* Thu Jun 16 2016 Florian Weimer <fweimer@redhat.com> - 2.17-140
- Remove printf from signal handler in tst-longjump_chk2 (#1346397)

* Thu Jun 16 2016 Florian Weimer <fweimer@redhat.com> - 2.17-139
- Improve libm performance AArch64 (#1302086)

* Wed Jun 15 2016 Florian Weimer <fweimer@redhat.com> - 2.17-138
- Search locale archive again after alias expansion (#971416)

* Wed Jun 15 2016 Florian Weimer <fweimer@redhat.com> - 2.17-137
- Revert IPv6 name server management changes (#1305132)

* Fri Jun 10 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.17-136
- aarch64: Fix bits/stat.h FTM guards (#1221046)

* Fri May 13 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-106.el7_2.6

* Fri May 13 2016 Florian Weimer <fweimer@redhat.com> - 2.17-135
- aarch64: Fix various minor ABI incompatibilities (#1335925)

* Fri May 13 2016 Florian Weimer <fweimer@redhat.com> - 2.17-134
- aarch64: Correct definition of MINSIGSTKSZ/SIGSTKSZ (#1335629)

* Tue May 3 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-133
- Require libselinux for nscd in non-bootstrap configuration (#1255847).

* Thu Apr 28 2016 Martin Sebor <msebor@redhat.com> - 2.17-132
- Fix a number of long-standing issues in the TZ parser (#1234449).

* Mon Apr 25 2016 Florian Weimer <fweimer@redhat.com> - 2.17-131
- Remove PER_THREAD preprocessor macro from malloc
- Use final upstream patch for arena free list fix (#1276753)

* Thu Apr 14 2016 Martin Sebor <msebor@redhat.com> - 2.17-130
- Prevent the compiler from clobbering floating point and vector
  registers in S390 symbol resolution functions (#1324427).
- Improve posix_fallocate behavior with NFS file descriptors (#1140250).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-129
- Remove a race condition from tst-mqueue5.c test to prevent spurious
  failures (#1064063).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-128
- Prevent a deadlock in gethostbyname_r (#1288613).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-127
- Use test-skeleton.c in tests (#1298354).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-126
- Fix inconsistent passwd compensation in nss/bug17079.c (#1293433).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-125
- Backport tst-getpw enhancement to limit the time the test takes up
  (#1298349).

* Mon Apr 04 2016 Florian Weimer <fweimer@redhat.com> - 2.17-124
- Log system information during build (#1307028).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-123
- Avoid appending duplicate shift sequences in iconv (#1293916).

* Mon Apr 04 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-122
- Reorganize POWER7 and POWER8 support (#1213267).
  - Only build POWER7 runtime for ppc64p7.
  - Only build POWER8 runtime for ppc64le.
  - Configure with --with-cpu=power8 for ppc64le.
  - Configure with --with-cpu=power8 for ppc.
  - Configure with --with-cpu=power7 for ppc64 default runtime.

* Mon Apr 04 2016 DJ Delorie <dj@redhat.com> - 2.17-121
- Build require gcc-c++ for the C++ tests.
- Add --with/--without controls for building glibc (#1255847)
  - Support --without testsuite option to disable testing after build.
  - Support --without benchtests option to disable microbenchmarks
    (placeholder for upstream compatibility only)
  - Update --with bootstrap to disable valgrind, documentation,
    selinux, and nss-crypt during bootstrap.
  - Support --without werror to disable building with -Werror.
  - Support --without docs to disable build requirement on texinfo.
  - Support --with valgrind to enable testing with valgrind.

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-120
- Make minor compatibility adjustments in headers (#1268050).

* Mon Apr 04 2016 Florian Weimer <fweimer@redhat.com> - 2.17-119
- Avoid aliasing issue in tst-rec-dlopen (#1292224)

* Mon Apr 04 2016 Florian Weimer <fweimer@redhat.com> - 2.17-118
- Suppress expected backtrace in tst-malloc-backtrace (#1276631).

* Mon Apr 04 2016 Florian Weimer <fweimer@redhat.com> - 2.17-117
- Avoid ld.so crash when audit modules provide path (#1211100)

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-116
- Avoid "monstartup: out of memory" error on powerpc64le (#1249102).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-115
- Configure --with-cpu=power8 on powerpc64 to generate POWER8
  instructions for POWER8 runtime (#1183088, #1213267).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-114
- Add enhanced and optimized support for IBM z13 systems (#1268008).

* Mon Apr 04 2016 Florian Weimer <fweimer@redhat.com> - 2.17-113
- Prevent the malloc arena free list form turning cyclic (#1276753).

* Mon Apr 04 2016 Martin Sebor <msebor@redhat.com> - 2.17-112
- Backported POWER8 optimizations for math and string functions (#1240351).

* Mon Apr 04 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-111
- Fix NULL pointer dereference in stub resolver with unconnectable name
  server addresses (#1320596).

* Thu Mar 31 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-110
- Fix memory leak in ftell for wide-oriented streams (#1310530).

* Wed Feb 17 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-106.el7_2.4

* Fri Feb 12 2016 Florian Weimer <fweimer@redhat.com> - 2.17-109
- Avoid race condition in _int_free involving fastbins (#1305406).

* Fri Feb 5 2016 Jason Green <jasg@amazon.com>
- Fix recvfrom function not always using the buffer size of a newly created buffer.
- Fix memory leak in _nss_dns_gethostbyname4_r with big DNS answer

* Fri Jan 15 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-108
- Fix CVE-2015-7547: getaddrinfo() stack-based buffer overflow (#1296031).
- Fix madvise performance issues (#1284959).
- Avoid "monstartup: out of memory" error on powerpc64le (#1249102).
- Update malloc testing for 32-bit POWER (#1293976).

* Wed Jan 13 2016 Carlos O'Donell <carlos@redhat.com> - 2.17-107
- Fix CVE-2015-5229: calloc() may return non-zero memory (#1293976).

* Mon Dec 7 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-106.el7_2.1

* Fri Nov 20 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-105.el7

* Tue Oct 27 2015 Florian Weimer <fweimer@redhat.com> - 2.17-106
- Add fix for CVE-2015-5277 (#1263134).

* Mon Aug 24 2015 Ian Weller <iweller@amazon.com>
- Make dependencies on multilib packages architecture-dependent

* Fri Aug 21 2015 Rodrigo Novo <rodarvus@amazon.com>
- Added glibc-rh1027101.patch
- Clean-up "CVE-2014-8121 is embargoed" message from spec file

* Fri Aug 14 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-105
- Fix up test case for initial-exec fix (#1248208).

* Wed Aug  5 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-104
- Mark all TLS variables in libc.so as initial-exec (#1248208).

* Tue Jul 28 2015 Rodrigo Novo <rodarvus@amazon.com>
- Fix dist suffix location on spec file to aid build scripts
- Remove patch to fix CVE-2015-5040, as that has been now addressed by RHEL

* Sat Jul 11 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-103
- Apply correct fix for #1195672.

* Fri Jul 10 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-102
- Remove workaround for kernel netlink bug (#1089836).
- Use only 32-bit instructions in optimized 32-bit POWER functions (#1240796).

* Mon Jun 22 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-101
- Correct the AArch64 ABI baseline for libpthread (#1234622).

* Mon Jun 22 2015 Martin Sebor <msebor@redhat.com> - 2.17-100
- Prevent tst-rec-dlopen from intermittently failing in parallel
  builds due to a missing makefile dependency (#1225959).

* Sat Jun 20 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-99
- Increase AArch64 TLS descriptor performance (#1202952).

* Sat Jun 20 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-98
- Move arch-specific header files from glibc-headers to glibc-devel (#1230328).

* Sat Jun 20 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-97
- Rebase high-precision timing support for microbenchmark (#1214326).

* Fri Jun 19 2015 Andrew Jorgensen <ajorgens@amazon.com>
- Fix memory leak in libio/wfileops.c do_ftell_wide

* Fri Jun 19 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-96
- Rebase microbenchmarks from upstream for performance testing (#1214326)
- Fix running microbenchmark script bench.pl from source (#1084395)

* Thu Jun 18 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-95
- Enable systemtap support for all architectures (#1225490).

* Thu Jun 18 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-94
- Fix ruserok API scalability issues (#1216246).

* Tue Jun 16 2015 Martin Sebor <msebor@redhat.com> - 2.17-93
- Backport fixes and enhancements for ppc64 and ppc64le (#1162895).
  - Correct DT_PPC64_NUM in elf/elf.h.
  - Correct IBM long double frexpl.
  - Correct IBM long double nextafterl.

* Fri Jun 12 2015 Martin Sebor <msebor@redhat.com> - 2.17-92
- Backport fixes for various security flaws (#1209107):
  - Prevent heap buffer overflow in swscanf (CVE-2015-1472, CVE-2015-1473,
    #1188235).
  - Prevent integer overflow in _IO_wstr_overflow (#1195762).
  - Prevent potential denial of service in internal_fnmatch (#1197730).
  - Prevent buffer overflow in gethostbyname_r and related functions
    with misaligned buffer (CVE-2015-1781, #1199525).

* Fri Jun  5 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-91
- Allow more shared libraries with static TLS to be loaded (#1227699).

* Fri May 29 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-90
- Work around kernel netlink bug on some specialized hardware setup (#1089836).
- Fix invalid file descriptor reuse when sending DNS query
  (CVE-2013-7423, #1194143).
- Sync netinet/tcp.h with the kernel (#1219891).

* Thu May 28 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-89
- Avoid deadlock in malloc on backtrace (#1207032).
- Actually test iconv modules (#1176906).
- Use calloc to allocate xports (#1159169).
- Return EAI_AGAIN for AF_UNSPEC when herrno is TRY_AGAIN (#1098042).

* Wed May 27 2015 Martin Sebor <msebor@redhat.com> - 2.17-88
- Add librtkaio.abilist generated by make update-abi (#1173238).

* Fri May 15 2015 Martin Sebor <msebor@redhat.com> - 2.18-87
- Enhance nscd inotify support (#1193797).

* Fri May 15 2015 Martin Sebor <msebor@redhat.com> - 2.17-86
- Use NSS_STATUS_TRYAGAIN to indicate insufficient buffer (#1173537).

* Thu May 14 2015 Marek Polacek <polacek@redhat.com> - 2.17-85
- Skip logging for DNSSEC responses (#1186620).
- Also apply the RHEL6.7 Makerules patch (#1189278).

* Tue May  5 2015 Marek Polacek <polacek@redhat.com> - 2.17-84
- Initialize nscd stats data (#1183456).

* Mon Apr 27 2015 Marek Polacek <polacek@redhat.com> - 2.17-83
- Resize DTV if the current DTV isn't big enough (#1189278).

* Sun Apr 26 2015 Martin Sebor <msebor@redhat.com> - 2.17-82
- Backport an alternate implementation of strstr and strcasestr for
  x86 that doesn't use the stack for temporaries requiring 16-byte
  alignment (#1150282).

* Tue Apr 21 2015 Rodrigo Novo <rodarvus@amazon.de>
- Fix buffer overflow in gethostbyname_r with misaligned buffer (CVE-2015-1781)
- Fix invalid file descriptor reuse while sending DNS query (CVE-2013-7423)

* Wed Apr 15 2015 Marek Polacek <polacek@redhat.com> - 2.17-81
- Fix recursive dlopen() (#1165212).
- Correctly size profiling reloc table (#1144133).

* Thu Apr  9 2015 Martin Sebor <msebor@redhat.com> - 2.17-80
- Work around a suspected gcc 4.8 bug (#1064066).

* Tue Mar 17 2015 Rodrigo Novo <rodarvus@amazon.de>
- bcond patch 0062 to usrmerge

* Mon Mar 16 2015 Jason Green <jasg@amazon.com>
- restart crond if glibc is upgraded from 2.12 to 2.17

* Fri Mar 13 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/glibc-2.17-78.el7
- import source package EL7/glibc-2.17-55.el7_0.5
- import source package EL7/glibc-2.17-55.el7_0.3
- import source package EL7/glibc-2.17-55.el7_0.1

* Fri Mar 13 2015 Rodrigo Novo <rodarvus@amazon.de>
- Remove double dist suffix

* Thu Mar 12 2015 Rodrigo Novo <rodarvus@amazon.de>
- import source package CENTOS7/glibc-2.17-78.el7

* Thu Mar 12 2015 Andrew Jorgensen <ajorgens@amazon.com>
- CVE-2014-8121 glibc: Unexpected closing of nss_files databases after lookups causes denial of service

* Tue Feb 24 2015 Rodrigo Novo <rodarvus@amazon.de>
- Drop patch #5001 (adopted by RHEL as #1512)

* Fri Feb 13 2015 Cristian Gafton <gafton@amazon.com>
- import source package CENTOS7/glibc-2.17-55.el7_0.5
- import source package CENTOS7/glibc-2.17-55.el7_0.3
- import source package CENTOS7/glibc-2.17-55.el7_0.1

* Tue Jan 27 2015 Rodrigo Novo <rodarvus@amazon.de>
- Fix parsing of numeric hosts in gethostbyname_r (CVE-2015-0235)

* Mon Jan 26 2015 Martin Sebor <msebor@redhat.com> - 2.17-79
- Restructure spec file to unconditionally apply ppc64le support (#1182355).
- Fix test failure in test-ildoubl on ppc64 (#1186491).

* Fri Jan 23 2015 Rodrigo Novo <rodarvus@amazon.de>
- Re-enable patch #1011 and -O3 optimization level
- Change --enable-kernel to 2.6.35 (earliest kernel shipped on ALAMI)

* Mon Jan 19 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-78
- Fix ppc64le builds (#1077389).

* Mon Jan 19 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-77
- Fix parsing of numeric hosts in gethostbyname_r (CVE-2015-0235, #1183545).

* Thu Jan 15 2015 Carlos O'Donell <carlos@redhat.com> - 2.17-76
- Fix application crashes during calls to gettimeofday on ppc64
  when kernel exports gettimeofday via VDSO (#1077389).
- Prevent NSS-based file backend from entering infinite loop
  when different APIs request the same service (CVE-2014-8121, #1182272).

* Thu Jan 8 2015 Rodrigo Novo <rodarvus@amazon.de>
- CVE-2014-6040: Crashes on invalid input in IBM gconv modules [BZ #17325]

* Wed Jan 7 2015 Rodrigo Novo <rodarvus@amazon.de>
- import source package RHEL7/glibc-2.17-55.el7_0.3
- import source package RHEL7/glibc-2.17-55.el7_0.1

* Mon Dec  8 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-75
- Fix permission of debuginfo source files to allow multiarch
  debuginfo packages to be installed and upgraded (#1170110).

* Fri Dec  5 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-74
- Fix wordexp() to honour WRDE_NOCMD (CVE-2014-7817, #1170487).

* Wed Dec  3 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-73
- ftell: seek to end only when there are unflushed bytes (#1156331).

* Wed Nov 12 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-72
- [s390] Fix up _dl_argv after adjusting arguments in _dl_start_user (#1161666).

* Tue Nov 11 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-71
- Fix incorrect handling of relocations in 64-bit LE mode for Power
  (#1162847).

* Tue Nov 11 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-70
- [s390] Retain stack alignment when skipping over loader argv (#1161666).

* Wed Nov  5 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-69
- Use __int128_t in link.h to support older compiler (#1120490).

* Tue Sep 16 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-68
- Revert to defining __extern_inline only for gcc-4.3+ (#1120490).

* Mon Sep 15 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-67
- Correct a defect in the generated math error table in the manual (#786638).

* Fri Sep 12 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-66
- Include preliminary thread, signal and cancellation safety documentation
  in manual (#786638).

* Thu Sep 11 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-65
- PowerPC 32-bit and 64-bit optimized function support using STT_GNU_IFUNC
  (#731837).
- Support running Intel MPX-enabled applications (#1132518).
- Support running Intel AVX-512-enabled applications (#1140272).

* Thu Sep 11 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-64
- Fix crashes on invalid input in IBM gconv modules (#1140474, CVE-2014-6040).

* Wed Sep 10 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-63
- Build build-locale-archive statically (#1070611).
- Return failure in getnetgrent only when all netgroups have been searched
  (#1085313).

* Tue Sep 9 2014 Ben Cressey <bcressey@amazon.com>
- add upstream patch for CVE-2014-0475

* Mon Sep  8 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-62
- Don't use alloca in addgetnetgrentX (#1138520).
- Adjust pointers to triplets in netgroup query data (#1138520).

* Fri Sep  5 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-61
- Set CS_PATH to just /use/bin (#1124453).
- Add systemtap probe in lll_futex_wake for ppc and s390 (#1084089).

* Fri Sep  5 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-60
- Add mmap usage to malloc_info output (#1103856).
- Fix nscd lookup for innetgr when netgroup has wildcards (#1080766).
- Fix memory order when reading libgcc handle (#1103874).
- Fix typo in nscd/selinux.c (#1125306).
- Do not fail if one of the two responses to AF_UNSPEC fails (#1098047).

* Thu Sep  4 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-59
- Provide correct buffer length to netgroup queries in nscd (#1083647).
- Return NULL for wildcard values in getnetgrent from nscd (#1085290).
- Avoid overlapping addresses to stpcpy calls in nscd (#1083644).
- Initialize all of datahead structure in nscd (#1083646).

* Thu Aug 28 2014 Ben Cressey <bcressey@amazon.com>
- add upstream patch for CVE-2014-5119

* Tue Aug 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-58
- Remove gconv transliteration loadable modules support (CVE-2014-5119,
  #1133812).
- _nl_find_locale: Improve handling of crafted locale names (CVE-2014-0475,

* Tue Aug 19 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-57
- Merge 64-bit ARM (AArch64) support (#1027179).
- Fix build failure for rtkaio/tst-aiod2.c and rtkaio/tst-aiod3.c.

* Sun Aug  3 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-56
- Merge LE 64-bit POWER support (#1125513).

* Fri Jul 25 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-55.4
- Fix tst-cancel4, tst-cancelx4, tst-cancel5, and tst-cancelx5 for all targets.
- Fix tst-ildoubl, and tst-ldouble for POWER.
- Allow LE 64-bit POWER to build with VSX if enabled (#1124048).

* Mon Jun  2 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-55.3
- Fix ppc64le ABI issue with pthread_atfork being present in libpthread.so.0.

* Fri May 30 2014 Ben Cressey <bcressey@amazon.com>
- require the version of freebl used at build time

* Fri May 30 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-55.2
- Add ABI baseline for 64-bit POWER LE.

* Fri May 30 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-55.1
- Add 64-bit POWER LE support.

* Wed May 7 2014 Cristian Gafton <gafton@amazon.com>
- import source package RHEL7/glibc-2.17-55.el7

* Thu Apr 3 2014 Ben Cressey <bcressey@amazon.com>
- remove initgroups from default nsswitch.conf

* Wed Mar 19 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-55
- Fix up test case for previous ftell bug (#1074410).

* Tue Mar 18 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-54
- Fix offset computation for a+ mode on switching from read (#1074410).

* Mon Mar 17 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-53
- Fix offset caching for streams and use it for ftell (#1074410).
- Change offset in fdopen only if setting O_APPEND (#1074410).
- Fix up return codes for tests in tst-ftell-active-handler (#1074410).

* Mon Mar 10 2014 Ben Cressey <bcressey@amazon.com>
- turn build-locale-archive back into a static build
- add conflict with audit < 2.3.0

* Sat Mar 8 2014 Cristian Gafton <gafton@amazon.com>
- enable tests again

* Thu Mar 6 2014 Cristian Gafton <gafton@amazon.com>
- disable lua pre script that does not work with older rpm versions

* Thu Mar  6 2014 Richard Henderson <rth@redhat.com> - 2.17-52.2
- Fix argument clobber (#1073667).

* Thu Mar  6 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-52.1
- Fix nscd failure on AArch64 involving errno access (#1067755).

* Wed Mar 5 2014 Cristian Gafton <gafton@amazon.com>
- disable tests for bootstrap builds
- restore /etc/localtime handling for non-systemd installs
- use less aggressive compiler optimzations for bootstrap builds
- remove unused/obsolete AMI patches
- conditionalize systemd support
- import source package F19/glibc-2.17-20.fc19
- import source package F19/glibc-2.17-19.fc19
- import source package F19/glibc-2.17-18.fc19
- import source package F19/glibc-2.17-14.fc19
- import source package F19/glibc-2.17-13.fc19
- import source package F19/glibc-2.17-11.fc19
- import source package F19/glibc-2.17-4.fc19
- import source package F19/glibc-2.16.90-25.fc19
- import source package F18/glibc-2.16-34.fc18
- import source package F18/glibc-2.16-33.fc18
- import source package F18/glibc-2.16-31.fc18
- import source package F18/glibc-2.16-30.fc18
- import source package F18/glibc-2.16-28.fc18
- import source package F18/glibc-2.16-24.fc18
- import source package F18/glibc-2.16-20.fc18
- import source package F17/glibc-2.15-59.fc17
- import source package F17/glibc-2.15-58.fc17
- import source package F17/glibc-2.15-57.fc17
- import source package F17/glibc-2.15-56.fc17
- import source package F17/glibc-2.15-54.fc17
- import source package F17/glibc-2.15-51.fc17
- import source package F17/glibc-2.15-37.fc17
- import source package F17/glibc-2.15-23.fc17
- import source package F16/glibc-2.14.90-24.fc16.9
- import source package F16/glibc-2.14.90-24.fc16.7
- import source package F16/glibc-2.14.90-24.fc16.6
- import source package F16/glibc-2.14.90-24.fc16.4
- import source package F16/glibc-2.14.90-21
- import source package F16/glibc-2.14.90-19
- import source package F16/glibc-2.14.90-18
- import source package F16/glibc-2.14.90-14
- import source package F15/glibc-2.14.1-6
- import source package F15/glibc-2.14.1-5
- import source package F15/glibc-2.14-5
- import source package F15/glibc-2.14-4
- import source package F15/glibc-2.14-3
- import source package F15/glibc-2.14-2
- import source package F15/glibc-2.13.90-9
- import source package F14/glibc-2.13-2

* Tue Mar  4 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-52
- Fix ftell behavior when the stream handle is not active (#1063681).

* Mon Mar  3 2014 Carlos O'Donell <carlos@redhat.com> - 2.17-51
- Build parts of the library with -fstack-protector-strong (#1070806).

* Fri Feb 28 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-50
- Better support for detecting nscd startup failures (#1048123).

* Wed Feb 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-49
- Fix ftime gettimeofday internal call returning bogus data (#1064945).

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.17-48
- Mass rebuild 2014-01-24

* Mon Jan 13 2014 Patsy Franklin <pfrankli@redhat.com> - 2.17-47
- Rebuild without ppc64p7 package (#1051065).

* Thu Jan  9 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-46
- Enable systemtap probes on S/390 and Power (#1049206).

* Mon Jan  6 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-45
- Revert to flushing buffer for ftell if output buffer does not have sufficient
  space for conversion (#1048036).
- Use first name entry for address in /etc/hosts as the canonical name in
  getaddrinfo (#1047983).

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.17-44
- Mass rebuild 2013-12-27

* Fri Dec 27 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-43
- Fix infinite loop on empty netgroups (#1046199).

* Tue Dec 24 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-42
- Return failure for negative lookups from nscd in netgroup cache (#1039970).

* Fri Dec 20 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-41
- Use POWER7 instructions for 32-bit POWER7 and POWER8 runtimes
  (#1028661).

* Wed Dec 18 2013 Cristian Gafton <gafton@amazon.com>
- Add patch to keep glibc compiling under new binutils and gcc 4.6

* Tue Dec 17 2013 Cristian Gafton <gafton@amazon.com>
- import source package F14/glibc-2.13-1
- import source package F14/glibc-2.12.90-21
- import source package F14/glibc-2.12.90-19
- import source package F14/glibc-2.12.90-18
- import source package F14/glibc-2.12.90-17
- import source package F14/glibc-2.12.90-15
- import source package F14/glibc-2.12.90-14
- import source package F14/glibc-2.12.90-11
- import source package F14/glibc-2.12.90-6
- import source package F13/glibc-2.12.2-1
- import source package F13/glibc-2.12.1-4
- import source package F13/glibc-2.12.1-3
- import source package F13/glibc-2.12.1-2
- import source package F13/glibc-2.12-3
- import source package F13/glibc-2.12-2

* Fri Dec 13 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL7/glibc-2.17-36.el7

* Thu Dec 12 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-40
- Change Oriya to Odia.  Convert iso-639.def to utf-8. (#1039496)

* Thu Dec 12 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-39
- Increase the value of SIGSTKSZ and MINSIGSTKSZ for Power (#1028652).

* Fri Nov 29 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-38
- S/390: Fix TLS GOT pointer setup (#1020637).

* Thu Nov 28 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-37
- Fix stack overflow due to large AF_INET6 requests (CVE-2013-4458, #1025612).
- Fix reads for sizes larger than INT_MAX in AF_INET lookup (#1032435).

* Thu Nov 21 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.132.el6

* Fri Nov  8 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-36
- Enhance NSCD's SELinux support to use dynamic permission names (#1025934).

* Fri Nov  8 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-20
- Depend on systemd instead of systemd-units (#1028430).

* Fri Nov  1 2013 Carlos O'Donell <carlos@readhat.com> - 2.17-35
- Add support for installing the dynmic loader in an alternate location.
  This is required for AArch64 support (#1023790).

* Mon Oct 28 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-19
- Add support for installing the dynmic loader in an alternate location.
  This is required for correct AArch64 support (#950093).

* Wed Oct 16 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-34
- Temporarily generate POWER6 code for the 32-bit POWER7 and POWER8
  runtimes to work around bug 1019549 (#1018072).

* Mon Oct 14 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.107.el6_4.5

* Thu Oct  3 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-33
- Update malloc systemtap probes and documentation (#742038).

* Thu Oct  3 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-32
- The default runtime is now POWER7 with an additional POWER8-tuned
  runtime. No other runtimes are provided by default. (#731833)

* Sun Sep 22 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-18
- Fix CVE-2013-4788: Static applications now support pointer mangling.
  Existing static applications must be recompiled (#985625).

* Sun Sep 22 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-17
- Fix indirect function support to avoid calling optimized routines
  for the wrong hardware (#985342).

* Fri Sep 20 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-31
- Fix integer overflows in memalign, valloc and pvalloc (CVE-2013-4332, #1008298).

* Wed Sep 18 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-16
- Fix conditional requiring specific binutils for s390/s390x.

* Mon Sep 16 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-15
- Fix integer overflows in *valloc and memalign (CVE-2013-4332, #1008299).

* Fri Sep 13 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-30
- Document FIPS compliance issues with SunRPC and AUTH_DES (#971589).

* Mon Sep  2 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-29
- Drop patch for #800224 (#884008).
- Fix tst-cleanup2 failure (#884008).

* Tue Aug 27 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.107.el6_4.4

* Tue Aug 27 2013 Carlos O'Donell <codonell@redhat.com> - 2.17-28
- Enable pointer mangling security feature in static applications
  (#990481, CVE-2013-4788).

* Mon Aug 26 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-27
- Update translation for stale file handle error.

* Mon Aug 26 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-26
- Initialize res_hconf in nscd (#1000923).

* Mon Aug 26 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-14
- Add systemd to BuildRequires (#999924).
- Expand sizes of some types in strcoll (#855399, CVE-2012-4424).
- Remove non-ELF support in rtkaio.
- Avoid inlining of cleanup function for kaio_suspend.
- Fix tst-aiod2 and tst-aiod3 test failures (#970865).

* Sun Aug 25 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-25
- Additional bug fixes related to s30/s390x support. (#804768)

* Mon Aug 19 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-24
- Fix buffer overflow in readdir_r (#996227, CVE-2013-4237).

* Mon Aug 19 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-13
- Fix stack overflow in getaddrinfo with many results (#947892, CVE-2013-1914).

* Mon Aug 19 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-12
- Disable pt_chown (#984829, CVE-2013-2207).
- Fix strcoll flaws (#855399, CVE-2012-4412, CVE-2012-4424).
- Fix buffer overflow in readdir_r (#995841, CVE-2013-4237).

* Fri Aug 16 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-23
- Remove non-ELF support in rtkaio.
- Avoid inlining of cleanup function for kaio_suspend.

* Wed Aug 14 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-22
- Fix conditional requiring specific binutils for s390/s390x.

* Thu Aug  8 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-21
- Remove GB18030 from releng tarball.

* Thu Aug  8 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-20
- Use tmpfilesdir macro instead of hard coding /usr/lib/tmpfiles.d.
- Backport GLIBC sched_getcpu and gettimeofday vDSO functions for ppc
  (#977110).
- Backport additional patches from upstream for
  -ftree-loop-distribute-patterns (#911307).
- Add HW_CAP2 support and add POWER8 enablement code (#731833).
- Remove useless .eh_frame to prevent gold linker bug (#731833).
- Add vDSO support or time function (#731833).
- Add PowerPC platform-specific inlines for shared resource hints (#731833).
- Reserve TCB space for EBB framework (#731833).
- Use _dl_static_init to set GLRO(gl_pagesize) (#731833).
- Rename __kernel_vdso_get_tbfreq to __kernel_get_tbfreq (#731833).
- Consolidate copies of PowerPC mp code (#731833).
- Unify math_ldbl.h implementations (#731833).
- Fix ABI issue for sqrtl and llroundl (#731833).
- Remove branch prediction from rint implementation (#731833).
- Optimize modf for PowerPC (#731833).
- Fix hypot/hypotf check for -INF on PowerPC (#731833).
- Use __ieee754_sqrl in acoshl for lbdl-128ibm (#731833).
- Add benchmark framework (#992727).

* Wed Jul 31 2013 Alexandre Oliva <aoliva@redhat.com> - 2.17-19
- Add systemtap probes for malloc functions (#742038).

* Wed Jul 31 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-18
- New environment variable GLIBC_PTHREAD_STACKSIZE to set thread stack
  size (#990388).

* Tue Jul 30 2013 Patsy Franklin < pfrankli@redhat.com> - 2.17.17
- Enable s390/s390x multiarch support (#804768).

* Tue Jul 30 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-16
- Add __glibc_likely as alias for __builtin_expect.
- Fix strcoll() various flaws (#989861, #989862, CVE-2012-4412, CVE-2012-4424).

* Mon Jul 29 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-15
- Correctly name the 240-bit slow path sytemtap probe slowpow_p10 for slowpow (#742035).
- Fix handling of netgroup cache in nscd (#966633).
- Fix loading of audit libraries when TLS is in use (#970791)

* Thu Jul 25 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-14
- Disable the use of pt_chown(Bugzilla #15755).  Distributions can re-enable
  building and using pt_chown with`--enable-pt_chown'.  (#984828i, CVE-2013-2207).

* Wed Jul 24 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-13
- Add build requirement on static libstdc++ library to fix testsuite failures
  for static C++ tests.

* Thu Jul 11 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.107.el6_4.2

* Tue Jul  2 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-12
- Fix stack overflow in getaddrinfo with many results (#980323, CVE-2013-1914).
- Correct fix to return failure on libio function error (#979363).

* Tue Jun 25 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-11
- Fix libm performance regression due to set/restore rounding mode (#977887).

* Tue Jun 25 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-10
- Preserve errno across _PC_CHOWN_RESTRICTED call on XFS (#977870).
- Remove PIPE_BUF Linux-specific code (#977872).
- Fix FPE in memusagestat when malloc utilization is zero (#977874).
- Accept leading and trailing spaces in getdate input string (#977875).

* Tue Jun 25 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-11
- Fix libm performance regression due to set/restore rounding mode (#977887).

* Tue Jun 25 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-10
- Preserve errno across _PC_CHOWN_RESTRICTED call on XFS (#977870).
- Remove PIPE_BUF Linux-specific code (#977872).
- Fix FPE in memusagestat when malloc utilization is zero (#977874).
- Accept leading and trailing spaces in getdate input string (#977875).

* Thu Jun 20 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.17-9
- Set EAI_SYSTEM only when h_errno is NETDB_INTERNAL (#958652).

* Tue Jun  4 2013 Jeff Law <law@redhat.com> - 2.17-8
- Fix ESTALE error message (#966259)

* Sun May  5 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-7
- Fix _nl_find_msg malloc failure case, and callers. (#959034).

* Tue Apr 30 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-6
- Test init_fct for NULL, not result->__init_fct, after demangling (#952799).

* Tue Apr 23 2013 Patsy Franklin <pfrankli@redhat.com> - 2.17-5
- Increase limits on xdr name and record requests (#892777).
- Consistently MANGLE/DEMANGLE init_fct, end_fct and btow_fct (#952799).

* Sun Mar 17 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-4
- Fix multibyte character processing crash in regexp (#905874, #905877, CVE-2013-0242)

* Wed Feb 27 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-3
- Renamed release engineering directory to `releng' (#903754).
- Fix building with gcc 4.8.0 (#911307).

* Fri Feb 22 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.107.el6

* Thu Feb 7 2013 Carlos O'Donell <carlos@redhat.com> - 2.17-2
- Fix ownership of /usr/lib[64]/audit (#894307).
- Support unmarked ARM objects in ld.so.cache and aux cache (#905184).

* Thu Jan 31 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.80.el6_3.7

* Tue Jan 1 2013 Jeff Law <law@redhat.com> - 2.17-1
- Resync with official glibc-2.17 release

* Fri Dec 21 2012 Jeff Law <law@redhat.com> - 2.16.90-40
- Resync with master

* Wed Dec 19 2012 Jeff Law <law@redhat.com> - 2.16.90-39
- Add rtld-debugger-interface.txt as documentation. (#872242)

* Fri Dec 7 2012 Jeff Law <law@redhat.com> - 2.16.90-38
- Resync with master
- Drop patch for 731228 that is no longer needed.

* Thu Dec 6 2012 Jeff Law <law@redhat.com> - 2.16.90-37
- Resync with master
- Patch for 697421 has been submitted upstream.
- Drop local patch for 691912 that is no longer needed.

* Mon Dec 3 2012 Jeff Law <law@redhat.com> - 2.16.90-36
- Resync with master
- Drop local patch for 657588 that is no longer needed.
- Drop local patch for 740682 that is no longer needed.
- Drop local patch for 770439 that is no longer needed.
- Drop local patch for 789209 that is no longer needed.
- Drop local patch for nss-files-overflow that seems useless.
- Drop localedata-locales-fixes as they were rejected upstream.
- Drop test-debug-gnuc-hack.patch that seems useless now.
- Repack patchlist.

* Fri Nov 30 2012 Jeff Law <law@redhat.com> - 2.16.90-35
- Resync with master (#882137).
- Remove local patch for strict-aliasing warnings that
  is no longer needed.
- Remove local patch for 730856 that is no longer needed.
- Repack patchlist.
- Remove local patch for strict-aliasing warnings that is no longer needed.

* Thu Nov 29 2012 Jeff Law <law@redhat.com> - 2.16.90-34
- Remove local patch which "temporarily" re-added currences
  obsoleted by the Euro.
- Remove hunks from strict-aliasing patch that are no longer
  needed.

* Thu Nov 29 2012 Jeff Law <law@redhat.com> - 2.16.90-33
- Resync with master.
- Drop local patch for 788989.
- Repack patchlist.

* Thu Nov 29 2012 Jeff Law <law@redhat.com> - 2.16.90-34
- Remove local patch which "temporarily" re-added currences obsoleted by the Euro.
- Remove hunks from strict-aliasing patch that are no longer needed.

* Thu Nov 29 2012 Jeff Law <law@redhat.com> - 2.16.90-33
- Resync with master.
- Drop local patch for 788989.
- Repack patchlist.

* Wed Nov 28 2012 Jeff Law <law@redhat.com> - 2.16.90-32
- Resync with master.
- Drop local patch for 878913.
- Drop local patch for 880666.
- Drop local patch for 767693.
- Repack patchlist.

* Tue Nov 27 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-31
- Ensure that hashtable size is greater than 3 (#878913).
- fwrite returns 0 on EOF (#880666).

* Mon Nov 26 2012 Jeff Law <law@redhat.com> - 2.16.90-30
- Resync with upstream sources
- Drop local patch for getconf.
- Repack patchlist.

* Fri Nov 16 2012 Jeff Law <law@redhat.com> - 2.16.90-29
- Rsync with upstream sources
- Drop local patches for 803286, 791161, 790292, 790298

* Wed Nov 7 2012 Jeff Law <law@redhat.com> - 2.16.90-28
- Resync with upstream sources (#873397)

* Mon Nov 5 2012 Jeff Law <law@redhat.com> - 2.16.90-27
- Resync with upstream sources.
- Don't use distinct patches for 770869, 787201 and 688948
  as they all modify stuff under fedora/
- Repack patchlist

* Thu Nov 1 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.80.el6_3.6

* Thu Nov 1 2012 Jeff Law <law@redhat.com> - 2.16.90-26
- Resync with upstream sources (#872336)

* Mon Oct 22 2012 Jeff Law <law@redhat.com> - 2.16.90-25
- Rsync with upstream sources
- Drop 864820 patch as now that it's upstream.
- Add sss to /etc/nsswitch.conf (#867473)

* Thu Oct 11 2012 Jeff Law <law@redhat.com> - 2.16.90-24
- Rsync with upstream sources
- Drop local 552960-2 patch now that it's upstream.
- Drop local 858274 patch now that the root problem is fixed upstream.
- Repack patchlist.

* Wed Oct 10 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-23
- Fix Marathi names for Wednesday, September and October (#rh864820).

* Fri Oct  5 2012 Jeff Law <law@redhat.com> - 2.16.90-22
- Resync with upstream sources
- Drop local 552960 patch now that it's upstream
- Drop local stap patch now obsolete
- Drop local s390 patch which avoided problems with old assemblers
- Drop old fortify source patch to deal with old compilers

* Thu Oct 4 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-21
- Take mutex in cleanup only if it is not already taken.

* Tue Oct 2 2012 Jeff Law <law@redhat.com> - 2.16.90-20
- Resync with upstream sources.
- Repack patchlist.

* Mon Oct 1 2012 Jeff Law <law@redhat.com> - 2.16.90-19
- Resync with upstream sources to pick up fma fixes

* Fri Sep 28 2012 Jeff Law <law@redhat.com> - 2.16.90-18
- Resync with upstream sources.
- Drop fedora-cdefs-gnuc.patch, it's not needed anymore.
- Drop fedora-gai-rfc1918.patch, it's upstream now.
- Drop fedora-localedata-no_NO.patch, it was supposed to be
  temporary -- that was back in 2003.   This should have been
  sorted out long ago.  We'll just have to deal with the
  fallout.
- Drop fedora-vfprintf-sw6530.patch, it's upstream now.
- Drop rh769421.patch; Siddhesh has fixed this properly with 552960.

* Fri Sep 28 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-17
- Release mutex before going back to wait for PI mutexes (#552960).

* Fri Sep 28 2012 Jeff Law <law@redhat.com> - 2.16.90-18
- Resync with upstream sources.
- Drop fedora-cdefs-gnuc.patch, it's not needed anymore.
- Drop fedora-gai-rfc1918.patch, it's upstream now.
- Drop fedora-localedata-no_NO.patch, it was supposed to be
  temporary -- that was back in 2003.   This should have been
  sorted out long ago.  We'll just have to deal with the
  fallout.
- Drop fedora-vfprintf-sw6530.patch, it's upstream now.
- Drop rh769421.patch; Siddhesh has fixed this properly with 552960.

* Fri Sep 28 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-17
- Release mutex before going back to wait for PI mutexes (#552960).

* Tue Sep 25 2012 Jeff Law <law@redhat.com> - 2.16.90-16
- Resync with upstream sources.

* Fri Sep 21 2012 Jeff Law <law@redhat.com> - 2.16.90-15
- Remove most of fedora-nscd patch as we no longer use the
  old init files, but systemd instead.
- Remove path-to-vi patch.  With the usr-move changes that
  patch is totally unnecessary.
- Remove i686-nopl patch.  Gas was changed back in 2011 to
  avoid nopl.
- Move gai-rfc1918 patch to submitted upstream status

* Fri Sep 21 2012 Jeff Law <law@redhat.com> - 2.16.90-14
- Revert patch for 816647, it's blatently broken.

* Fri Sep 21 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-13
- Bring back byteswap-16.h (#859268).

* Fri Sep 21 2012 Jeff Law <law@redhat.com> - 2.16.90-15
- Remove most of fedora-nscd patch as we no longer use the
  old init files, but systemd instead.
- Remove path-to-vi patch.  With the usr-move changes that
  patch is totally unnecessary.
- Remove i686-nopl patch.  Gas was changed back in 2011 to
  avoid nopl.
- Move gai-rfc1918 patch to submitted upstream status

* Fri Sep 21 2012 Jeff Law <law@redhat.com> - 2.16.90-14
- Revert patch for 816647, it's blatently broken.

* Fri Sep 21 2012 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.16.90-13
- Bring back byteswap-16.h (#859268).

* Thu Sep 20 2012 Jeff Law <law@redhat.com> - 2.16.90-12
- Revert recent upstream strstr changes (#858274)
- Demangle function pointers before testing them (#816647)
- Remove handling of /etc/localtime and /var/spool/postfix/etc/localtime
  as systemd will be handling them from now on (#858735).

* Fri Sep 14 2012 Jeff Law <law@redhat.com> - 2.16.90-11
- Resync with upstream sources (#857236).

* Sat Sep  8 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.16.90-10
- Enable ports to fix FTBFS on ARM

* Wed Sep 5 2012 Jeff Law <law@redhat.com> - 2.16.90-9
- Resync with upstream sources.

* Tue Sep 4 2012 Jeff Law <law@redhat.com> - 2.16.90-8
- Incorporate ppc64p7 arch changes (#854250)

* Thu Aug 30 2012 Jeff Law <law@redhat.com> - 2.16.90-7
- Resync with upstream sources.

* Wed Aug 29 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.80.el6_3.5

* Wed Aug 22 2012 Jeff Law <law@redhat.com> - 2.16.90-6
- Resync with upstream sources.

* Tue Aug 21 2012 Jeff Law <law@redhat.com> - 2.16.90-5
- Replace manual systemd scriptlets with macroized scriptlets (#850129)

* Mon Aug 20 2012 Jeff Law <law@redhat.com> - 2.16.90-4
- Move /etc/localtime into glibc-common package since glibc-common
  owns the scriptlets which update it.

* Mon Aug 20 2012 Jeff Law <law@redhat.com> - 2.16.90-3
- Remove obsolete patches from glibc-fedora.patch.  Explode
  remaining patches into distinct patchfiles.  Thanks to
  Dmitry V. Levin for identifying them!
  Drop ia64 specific patches and specfile fragments

* Mon Aug 20 2012 Jeff Law <law@redhat.com> - 2.16.90-4
- Move /etc/localtime into glibc-common package since glibc-common
    owns the scriptlets which update it.

* Mon Aug 20 2012 Jeff Law <law@redhat.com> - 2.16.90-3
- Remove obsolete patches from glibc-fedora.patch.  Explode
  remaining patches into distinct patchfiles.  Thanks to
  Dmitry V. Levin for identifying them!
  Drop ia64 specific patches and specfile fragments

* Wed Aug 15 2012 Jeff Law <law@redhat.com> - 2.16.90-2
- Fix integer overflow leading to buffer overflow in strto* (#847718)

* Mon Aug 13 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.80.el6_3.4

* Mon Aug 13 2012 Jeff Law <law@redhat.com> - 2.16.90-1
- Resync with upstream sources, drop obsolete patches.
- Drop glibc-ports bits as they're part of the master
  sources now.

* Mon Aug 13 2012 Jeff Law <law@redhat.com> - 2.16-9
- Replace patch for 179072 with official version from upstream.

* Mon Aug 13 2012 Jeff Law <law@redhat.com> - 2.16.90-1
- Resync with upstream sources, drop obsolete patches.
- Drop glibc-ports bits as they're part of the master
    sources now.

* Mon Aug 13 2012 Jeff Law <law@redhat.com> - 2.16-9
- Replace patch for 179072 with official version from upstream.

* Fri Aug 10 2012 Jeff Law <law@redhat.com> - 2.16-8
- Replace patch for 789238 with official version from upstream.

* Wed Jul 25 2012 Jeff Law <law@redhat.com> - 2.16-7
- Pack IPv4 servers at the start of nsaddr_list and
  only track the number of IPV4 servers in EXT(statp->nscounti (#808147)
- Mark set*uid, set*gid as __wur (warn unused result) (#845960)

* Wed Jul 25 2012 Jeff Law <law@redhat.com> - 2.16-6
- Revert patch for BZ696143, it made it impossible to use IPV6
  addresses explicitly in getaddrinfo, which in turn broke
  ssh, apache and other code. (#808147)
- Avoid another unbound alloca in vfprintf (#841318)
- Remove /etc/localtime.tzupdate in lua scriptlets
- Revert back to using posix.symlink as posix.link with a 3rd
  argument isn't supported in the lua version embedded in rpm.
- Revert recent changes to res_send (804630, 835090).
- Fix memcpy args in res_send (#841787).

* Wed Jul 25 2012 Jeff Law <law@redhat.com> - 2.16-7
- Pack IPv4 servers at the start of nsaddr_list and
    only track the number of IPV4 servers in EXT(statp->nscounti (#808147)
- Mark set*uid, set*gid as __wur (warn unused result) (#845960)

* Wed Jul 25 2012 Jeff Law <law@redhat.com> - 2.16-6
- Revert patch for BZ696143, it made it impossible to use IPV6
  addresses explicitly in getaddrinfo, which in turn broke
  ssh, apache and other code. (#808147)
- Avoid another unbound alloca in vfprintf (#841318)
- Remove /etc/localtime.tzupdate in lua scriptlets
- Revert back to using posix.symlink as posix.link with a 3rd
  argument isn't supported in the lua version embedded in rpm.
- Revert recent changes to res_send (804630, 835090).
- Fix memcpy args in res_send (#841787).

* Thu Jul 19 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.80.el6_3.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 Jeff Law <law@redhat.com> - 2.16-2
- Use posix.link rather than posix.symlink in scriptlet to
  update /etc/localtime (#837344).

* Mon Jul 2 2012 Jeff Law <law@redhat.com> - 2.16-1
- Resync with upstream glibc-2.16 release.

* Fri Jun 22 2012 Jeff Law <law@redhat.com> - 2.15.90-16
- Resync with upstream sources, drop obsolete patch.

* Thu Jun 21 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.80.el6

* Thu Jun 21 2012 Jeff Law <law@redhat.com> - 2.15.90-15
- Resync with upstream sources (#834447).
- Fix use-after-free in dcigettext.c (#816647).

* Fri Jun 15 2012 Jeff Law <law@redhat.com> - 2.15.90-14
- Resync with master.

* Thu Jun 14 2012 Jeff Law <law@redhat.com> - 2.15.90-13
- Delay setting DECIDED field in locale file structure until
  we have read the file's data (#827510).

* Mon Jun 11 2012 Dennis Gilmore <dennis@ausil.us> - 2.15.90-12
- actually apply the arm linker hack

* Mon Jun 11 2012 Dennis Gilmore <dennis@ausil.us> - 2.15.90-11
- only deal with the arm linker compat hack on armhfp arches
- armsfp arches do not have a linker change
- Backward compat hack for armhf binaries.

* Mon Jun 11 2012 Dennis Gilmore <dennis@ausil.us> - 2.15.90-12
- Apply the arm linker hack.

* Mon Jun 11 2012 Dennis Gilmore <dennis@ausil.us> - 2.15.90-11
- only deal with the arm linker compat hack on armhfp arches
- armsfp arches do not have a linker change
- Backward compat hack for armhf binaries.

* Thu Jun  7 2012 Jeff Law <law@redhat.com> - 2.15.90-10
- Fix parsing of /etc/sysconfig/clock when ZONE has spaces. (#828291)

* Tue Jun  5 2012 Jeff Law <law@redhat.com> - 2.15.90-9
- Resync with upstream sources, drop unnecessary patches.
- Fix DoS in RPC implementation (#767693)
- Remove deprecated alpha support.
- Remove redundant hunk from patch. (#823905)

* Fri Jun  1 2012 Patsy Franklin <patsy@redhat.com> - 2.15.90-8
- Fix iconv() segfault when the invalid multibyte character 0xffff is input
  when converting from IBM930 (#823905)

* Fri Jun 1 2012 Jeff Law <law@redhat.com> - 2.15.90-7
- Resync with upstream sources.  (#827040)

* Fri Jun  1 2012 Patsy Franklin <patsy@redhat.com> - 2.15.90-8
- Fix iconv() segfault when the invalid multibyte character 0xffff is input
  when converting from IBM930 (#823905)

* Fri Jun 1 2012 Jeff Law <law@redhat.com> - 2.15.90-7
- Resync with upstream sources.  (#827040)

* Thu May 31 2012 Patsy Franklin <patsy@redhat.com> - 2.15.90-6
- Fix fnmatch() when '*' wildcard is applied on a file name containing
  multibyte chars. (#819430)

* Wed May 30 2012 Jeff Law <law@redhat.com> - 2.15.90-5
- Resync with upstream sources, drop unnecessary patches.

* Tue May 29 2012 Jeff Law <law@redhat.com> - 2.15.90-4
- Build info files in the source dir, then move to objdir
  to avoid multilib conflicts (#825061)

* Fri May 25 2012 Jeff Law <law@redhat.com> - 2.15.90-3
- Work around RPM dropping the contents of /etc/localtime
  when it turns into a symlink with %post common script (#825159).

* Wed May 23 2012 Jeff Law <law@redhat.com> - 2.15.90-2
- Fix option rotate when one IPV6 server is enabled (#804630)
- Reenable slow/uberslow path taps slowpow/slowexp.

* Wed May 23 2012 Jeff Law <law@redhat.com> - 2.15.90-1
- Resync with upstream sources, drop unnecessary patches.

* Wed May 23 2012 Jeff Law <law@redhat.com> - 2.15.90-2
- Fix option rotate when one IPV6 server is enabled (#804630)
- Reenable slow/uberslow path taps slowpow/slowexp.

* Wed May 23 2012 Jeff Law <law@redhat.com> - 2.15.90-1
- Resync with upstream sources, drop unnecessary patches.

* Tue May 22 2012 Patsy Franklin <pfrankli@redhat.com> - 2.15-41
- Fix tzdata trigger (#822200)
- Make the symlink relative rather than linking into the buildroot (#822200).
- Changed /etc/localtime to a symlink. 8222000 (#822200)

* Tue May 15 2012 Jeff Law <law@redhat.com> - 2.15-40
- Update to upstream patch for 806070 (#806070)

* Mon May 14 2012 Jeff Law <law@redhat.com> - 2.15-39
- Update upstream patch for AVX testing (#801650)

* Fri May 11 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.47.el6_2.12

* Fri May 11 2012 Jeff Law <law@redhat.com> - 2.15-38
- Upstream patch to fix AVX testing (#801650)

* Thu May 10 2012 Jeff Law <law@redhat.com> - 2.15-37
- Try again to fix AVX testing (#801650)

* Mon May 7 2012 Jeff Law <law@redhat.com> - 2.15-36
- Improve fortification disabled warning.
- Change location of dynamic linker for armhf.

* Mon Apr 30 2012 Jeff Law <law@redhat.com> - 2.15-35
- Implement context routines for ARM (#817276)

* Fri Apr 13 2012 Jeff Law <law@redhat.com> - 2.15-34
- Issue a warning if FORTIFY_CHECKING is requested, but disabled.

* Thu Apr 12 2012 Jeff Law <law@redhat.com> - 2.15-33
- Fix another unbound alloca in nscd groups (#788989)

* Tue Apr 3 2012 Jeff Law <law@redhat.com> - 2.15-32
- Fix first day of week for lv_LV (#682500)

* Mon Apr 2 2012 Jeff Law <law@redhat.com> - 2.15-31
- When retrying after main arena failure, always retry in a
  different arena. (#789238)

* Tue Mar 27 2012 Jeff Law <law@redhat.com> - 2.15-30
- Avoid unbound alloca usage in *-crypt routines (#804792)
- Fix data race in nscd (#806070)

* Fri Mar 23 2012 Jeff Law <law@redhat.com> - 2.15-29
- Fix typo in __nss_getent (#806403).

* Thu Mar 22 2012 Cristian Gafton <gafton@amazon.com>
- remove applied patch: 0001-Fix-buffer-allocation-in-files-initgroups-handler.patch

* Fri Mar 16 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.47.el6_2.9

* Thu Mar 15 2012 Cristian Gafton <gafton@amazon.com>
- add patch: Fix-buffer-allocation-in-files-initgroups-handler

* Wed Mar 14 2012 Jeff Law <law@redhat.com> - 2.15-28
- Add doi_IN, sat_IN and mni_IN to SUPPORTED locals (#803286)
- Add stap probes in slowpow and slowexp.

* Fri Mar 09 2012 Jeff Law <law@redhat.com> - 2.15-27
- Fix AVX checks (#801650)

* Wed Feb 29 2012 Jeff Law <law@redhat.com> - 2.15-26
- Set errno properly in vfprintf (#794797)
- Don't kill application when LD_PROFILE is set. (#800224)

* Wed Feb 29 2012 Jeff Law <law@redhat.com> - 2.15-25
- Fix out of bounds memory access in resolver (#798471)
- Always mark vDSO as used (#758888)

* Wed Feb 29 2012 Jeff Law <law@redhat.com> - 2.15-26
- Set errno properly in vfprintf (#794797)
- Don't kill application when LD_PROFILE is set. (#800224)

* Wed Feb 29 2012 Jeff Law <law@redhat.com> - 2.15-25
- Fix out of bounds memory access in resolver (#798471)
- Always mark vDSO as used (#758888)

* Fri Feb 24 2012 Jeff Law <law@redhat.com> - 2.15-24
- Fix bogus underflow (#760935)
- Correctly handle dns request where large numbers of A and AAA records
  are returned (#795498)
- Fix nscd crash when group has many members (#788989)

* Mon Feb 20 2012 Jeff Law <law@redhat.com> - 2.15-23
- Avoid "nargs" integer overflow which could be used to bypass FORTIFY_SOURCE (#794797)

* Mon Feb 20 2012 Jeff Law <law@redhat.com> - 2.15-22
- Fix main arena locking in malloc/calloc retry path (#789238)

* Mon Feb 20 2012 Jeff Law <law@redhat.com> - 2.15-23
- Avoid "nargs" integer overflow which could be used to bypass FORTIFY_SOURCE (#794797)

* Mon Feb 20 2012 Jeff Law <law@redhat.com> - 2.15-22
- Fix main arena locking in malloc/calloc retry path (#789238)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.15-21
- Correctly identify all 127.x.y.z addresses (#739743)
- Don't assign native result if result has no associated interface (#739743)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.15-20
- Ignore link-local IPV6 addresses for AI_ADDRCONFIG (#697149)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.15-19
- Fix reply buffer mismanagement in resolver (#730856)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.15-21
- Correctly identify all 127.x.y.z addresses (#739743)
- Don't assign native result if result has no associated interface (#739743)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.15-20
- Ignore link-local IPV6 addresses for AI_ADDRCONFIG (#697149)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.15-19
- Fix reply buffer mismanagement in resolver (#730856)

* Thu Feb 16 2012 Jeff Law <law@redhat.com> - 2.15-18
- Revert 552960/769421 changes again, still causing problems.
- Add doi_IN (#791161)
- Add sat_IN (#790292)
- Add mni_IN (#790298)

* Thu Feb 9 2012 Jeff Law <law@redhat.com> - 2.15-17
- Fix lost wakeups in pthread_cond_*.  (#552960, #769421)
- Clarify info page for snprintf (#564528)
- Fix first_weekday and first_workday for ru_UA (#624296)

* Tue Feb 7 2012 Jeff Law <law@redhat.com> - 2.15-16
- Fix currency_symbol for uk_UA (#789209)
- Fix weekday names in Kashmiri locale (#770439)

* Tue Feb 7 2012 Jeff Law <law@redhat.com> - 2.15-15
- Remove change for 787662, correct fix is in gcc.

* Tue Feb 7 2012 Jeff Law <law@redhat.com> - 2.15-16
- Fix currency_symbol for uk_UA (#789209)
- Fix weekday names in Kashmiri locale (#770439)

* Tue Feb 7 2012 Jeff Law <law@redhat.com> - 2.15-15
- Remove change for 787662, correct fix is in gcc.

* Mon Feb 6 2012 Jeff Law <law@redhat.com> - 2.15-13
- More accurately detect if we're in a chroot (#688948)

* Fri Feb 3 2012 Jeff Law <law@redhat.com> - 2.15-12
- Add fedfs to /etc/rpc (#691912)
- Run nscd in the foreground w/ syslogging, fix systemd config (#770869)
- Avoid mapping past end of shared object (#741105)
- Turn off -mno-minimal-toc on PPC (#787201)
- Remove hunk from glibc-rh657588.patch that didn't belong

* Wed Feb 1 2012 Jeff Law <law@redhat.com> - 2.15-8
- Prevent erroneous inline optimization of initfini.s on PowerPC64 (#783979)
- Use upstream variant of fix for 740506.
- Fix month abbreviations for zh_CN (#657588)

* Sun Jan 29 2012 Jeff Law <law@redhat.com> - 2.15-7
- Sort objects before relocations (sw#13618)
- Fix bogus sort code that was copied from dl-deps.c.

* Thu Jan 26 2012 Jeff Law <law@redhat.com> - 2.15-6
- First argument to settimeofday can be null (#740682)
- Add aliases for ISO-10646-UCS-2 (#697421)

* Wed Jan 25 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.47.el6_2.5

* Tue Jan 24 2012 Jeff Law <law@redhat.com> - 2.15-4
- Update ports from master.
- Fix first workday/weekday for it_IT (#622499)
- Fix type to uint16_t based on upstream comments (729661)
- Do not cache negative results in nscd if these are transient (#784402)

* Mon Jan 23 2012 Jeff Law <law@redhat.com> - 2.15-3
- Fix cycle detection (#729661)
- Fix first workday/weekday for it_IT (#446078)
- Fix first workday/weekday for ca_ES (#454629)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 1 2012 Jeff Law <law@redhat.com> - 2.15-1.fc17
- Update from master (a316c1f)

* Thu Dec 22 2011 Jeff Law <law@redhat.com> - 2.14.90-26.fc17
- Update from master (16c6f99)
- Fix typo in recent tzfile change (#769476)
- Make MALLOC_ARENA_MAX and MALLOC_ARENA_TEST match documentation (#740506)
- Revert "fix" to pthread_cond_wait (#769421)
- Extract patch for 730856 from fedora-patch into a distinct patchfile

* Mon Dec 19 2011 Jeff Law <law@redhat.com> - 2.14.90-25.fc17
- Update from master (a4647e7).

* Sun Dec 18 2011 Jeff Law <law@redhat.com> - 2.14.90-24.fc16.3
- Check values from TZ file header (#767696)
- Handle EAGAIN from FUTEX_WAIT_REQUEUE_PI (#552960)
- Add {dist}.#
- Correct return value from pthread_create when stack alloction fails.
  (#767746)

* Thu Dec 8 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.47.el6

* Wed Dec 7 2011 Jeff Law <law@redhat.com> - 2.14.90-23
- Fix a wrong constant in powerpc hypot implementation (#750811)
  #13534 in python bug database
  #13472 in glibc bug database
- Truncate time values in Linux futimes when falling back to utime

* Mon Dec 5 2011 Jeff Law <law@redhat.com> - 2.14.90-22
- Mark fortified __FD_ELT as extension (#761021)
- Fix typo in manual (#708455)

* Wed Nov 30 2011 Jeff Law <law@redhat.com> - 2.14.90-21
- Don't fail in makedb if SELinux is disabled (#750858)
- Fix access after end of search string in regex matcher (#757887)

* Mon Nov 28 2011 Jeff Law <law@redhat.com> - 2.14.90-20
- Drop lock before calling malloc_printerr (#757881)

* Fri Nov 18 2011 Jeff Law <law@redhat.com> - 2.14.90-19
- Check malloc arena atomically  (BZ#13071)
- Don't call reused_arena when _int_new_arena failed (#753601)

* Wed Nov 16 2011 Jeff Law <law@redhat.com> - 2.14.90-18
- Fix grouping and reuse other locales in various locales (BZ#13147)

* Tue Nov 15 2011 Jeff Law <law@redhat.com> - 2.14.90-17
- Revert bogus commits/rebasing of Nov 14, Nov 11 and Nov 8.  Sources
  should be equivalent to Fedora 16's initial release.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.90-15
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Jim Meyering <meyering@redhat.com> - 2.14.90-14
- Revert the upstream patch that added the leaf attribute, since it
  caused gcc -O2 to move code past thread primitives and sometimes
  even out of critical sections.  See http://bugzilla.redhat.com/747377

* Wed Oct 19 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-13
- Update from master
  - Fix linkage conflict with feraiseexcept (#746753)
  - More libm optimisations

* Wed Oct 19 2011 Jim Meyering <meyering@redhat.com> - 2.14.90-14
- Revert the upstream patch that added the leaf attribute, since it
  caused gcc -O2 to move code past thread primitives and sometimes
  even out of critical sections.  See http://bugzilla.redhat.com/747377

* Wed Oct 19 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-13
- Update from master
  - Fix linkage conflict with feraiseexcept (#746753)
  - More libm optimisations

* Mon Oct 17 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-12
- Update from master
  - Correctly handle missing initgroups database (#745675)
  - Optimize many libm functions
  - Optimize access to isXYZ and toXYZ tables
  - Optimized memcmp and wmemcmp for x86-64 and x86-32
  - Add parameter annotation to modf (BZ#13268)
  - Support optimized isXXX functions in C++ code
  - Check for zero size in memrchr for x86_64 (#745739)
  - Optimized memchr, memrchr, rawmemchr for x86-32

* Tue Oct 11 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-11
- Update from master
  - Clean up locarchive mmap reservation code
  - Fix netname2host (BZ#13179)
  - Fix remainder (NaN, 0) (BZ#6779, BZ#6783)
  - S/390: Fix longlong.h inline asms for zarch
  - Improve 64 bit memchr, memrchr, rawmemchr with SSE2
  - Update translations
  - Implement caching of netgroups in nscd
  - Handle OOM in NSS
  - Don't call ifunc functions in trace mode
- Convert tzdata-update to lua (#729796)
- Horrible workaround for horribly broken software (#737223)

* Wed Sep 28 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-10
- Update from master
  - Correctly reparse group line after enlarging the buffer (#739360)
  - Fix parse error in bits/mathinline.h with --std=c99 (#740235)
- Update nscd service file (#740284)
- Drop nscd init file (#740196)

* Fri Sep 16 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-9
- Update from master
  - Define IP_MULTICAST_ALL (BZ#13192)
  - Add fmax and fmin inlines for x86-64
  - Avoid race between {,__de}allocate_stack and __reclaim_stacks
    during fork (#737387)
  - Optimized lrint and llrint for x86-64
  - Also relocate in dependency order when doing symbol dependency
    testing (#737459)
  - Optimize logb code for 64-bit machines
  - Fix jn precision (BZ#11589)
  - Fix boundary conditions in scanf (BZ#13138)
  - Don't lock string streams in stream cleanup code (BZ#12847)
  - Define ELFOSABI_GNU
  - Fix lround loss of precision
  - Add range checking for FD_SET, FD_CLR, and FD_ISSET
- Make sure AVC thread has capabilities

* Thu Sep  8 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-8
- Update from master
  - Use O_CLOEXEC when loading objects and cache in ld.so (BZ#13068)
  - Fix memory leak in case of failed dlopen (BZ#13123)
  - Optimizations for POWER
  - Prefer real syscalls instead of vsyscalls on x86-64 outside libc.so
  - Add Atom-optimized strchr and strrchr for x86-64
  - Try shell in posix_spawn* only in compat mode (BZ#13134)
  - Fix glob.h header by removing gcc 1.x support (BZ#13150)
  - Optimized strchr and strrchr with SSE2 on x86-32
  - Add optimized x86 wcscmp
  - Fixes and optimizations for 32-bit sparc fabs
  - Fix nptl semaphore cleanup invocation
  - Sanitize HWCAP_SPARC_* defines/usage, and add new entries

* Thu Sep  1 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-7
- Update from master
  - Relocate objects in dependency order (#733462)
- Avoid assertion failure when first DNS answer was empty (#730856)
- Don't treat tls_offset == 1 as forced dynamic (#731228)

* Wed Aug 24 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-6
- Update from master
  - Correct cycle detection during dependency sorting
  - Use ifuncs for time and gettimeofday on x86-64
  - Fix fopen (non-existing-file, "re") errno
  - Fix CFI info in x86-64 trampolines for non-AVX code
  - Build libresolv with SSP flags
  - Avoid executable stack in makedb (#731063)
  - Align x86 TCB to 64 bytes (cache line size), important for Atom

* Thu Aug 18 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.25.el6_1.3

* Mon Aug 15 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-5
- Update from master
  - Implement LD_DEBUG=scopes
  - Locale-independent parsing in libintl (#726536)
  - Fix stack alignment on x86_64 (#728762)
  - Implement scandirat function

* Tue Aug  9 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-4
- Update from master
  - Properly tokenize nameserver line for servers with IPv6 address
  - Fix encoding name for IDN in getaddrinfo (#725755)
  - Fix inline strncat/strncmp on x86
  - Define SEEK_DATA and SEEK_HOLE
  - Define AF_NFC and PF_NFC
  - Update ptrace constants
  - Add read barriers in cancellation initialization
  - Add read barrier protecting DES initialization
  - Fix overflow bug in optimized strncat for x86-64
  - Check for overflows in expressions (BZ#12852)
  - Fix check for AVX enablement (#720176, BZ#13007)
  - Force La_x86_64_ymm to be 16-byte aligned
  - Add const attr to gnu_dev_{major,minor,makedev}
- Filter out GLIBC_PRIVATE symbols again

* Thu Jul 28 2011 Cristian Gafton <gafton@amazon.com>
- re-enable multiarch builds

* Wed Jul 20 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-3
- Update from master
  - S/390: Don't use r11 in INTERNAL_VSYSCALL_NCS macro
  - Avoid warning in nscd config file parsing code
  - Improve 64 bit strcat functions with SSE2/SSSE3
  - Fix alloca accounting in strxfrm
  - Avoid possible crashes in anormal nscd exits
  - Updated Swedish and Dutch translations

* Thu Jul 14 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-2
- Update from master
  - Generalize framework to register monitoring of files in nscd
  - Handle ext4 in {,f}pathconf
  - Handle Lustre filesystem (BZ#12868)
  - Handle W; without long options in getopt (BZ#12922)
  - Change error code for underflows in strtod (BZ#9696)
  - Fix handling of chained netgroups
  - Optimize long-word additions in SHA implementation
  - Handle nscd negtimeout==0
  - nss_compat: query NIS domain only when needed
  - Fix robust mutex handling after fork
  - Make sure RES_USE_INET6 is always restored
- Add systemd configuration for nscd
- Be more careful running build-locale-archive

* Thu Jun 30 2011 Andreas Schwab <schwab@redhat.com> - 2.14.90-1
- Update from master
  - Fix quoting in some installed shell scripts (BZ#12935)
  - Fix missing .ctors/.dtors lead word in soinit
  - Improved st{r,p}{,n}cpy for SSE2 and SSSE3 on x86
  - Avoid __check_pf calls in getaddrinfo unless really needed
    (BZ#12907)
  - Rate limit expensive _SC_NPROCESSORS_ONLN computation
  - Add initgroups lookup support to getent
  - Reenable nss_db with a completely new implementation
  - Rewrite makedb to avoid using db library
  - Add pldd program
- Obsolete nss_db
- Don't build tzdata-update and build-locale-archive statically

* Tue Jun 28 2011 Andreas Schwab <schwab@redhat.com> - 2.14-4
- Update from 2.14 branch
  - Fix crash in GB18030 encoder (#712901)
- Fix more bugs in GB18030 charmap
- Don't use gethostbyaddr to determine canonical name

* Tue Jun 21 2011 Andreas Schwab <schwab@redhat.com> - 2.14-3
- Update from 2.14 branch
  - Fix typo in recent resolver change which causes segvs (#710279)
  - Fix memory leak in getaddrinfo (#712178)
  - Fix <bits/mqueue2.h> for C++ (BZ#12841)
  - Assume Intel Core i3/i5/i7 processor if AVX is available
- Filter results from gethostbyname4_r according to request flags
  (#711827)
- Repair GB18030 charmap (#712901)
- Revert "Use .machine to prevent AS from complaining about z9-109
  instructions in iconv modules" (#711330)

* Fri Jun  3 2011 Andreas Schwab <schwab@redhat.com> - 2.14-2
- Revert "Handle DNS server failures in case of AF_UNSPEC lookups
  correctly" (#710279)

* Tue May 31 2011 Andreas Schwab <schwab@redhat.com> - 2.14-1
- Update to 2.14 release
  - Handle DNS server failures in case of AF_UNSPEC lookups correctly
    (BZ#12684)
  - Prevent loader from loading itself
  - Restore _res correctly (BZ#12350)
  - Interpret numeric values in shadow file as signed (BZ#11099)
  - Recognize use-vc option in resolv.conf (BZ#11558)
  - Mark malloc hook variables as deprecated
  - Declare malloc hook variables as volatile (BZ#11781)
  - Don't document si_code used for raise (BZ#11799)
  - Fix unnecessary overallocation due to incomplete character (BZ#12811)
  - Handle failure of _nl_explode_name in all cases
  - Add support for time syscall in vDSO (BZ#12813)
  - Add sendmmsg and setns syscalls
  - Use getcpu definition from vDSO on x86-64 (BZ#12813)
- Don't free non-malloced memory and fix memory leak (#709267)

* Fri May 27 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-14
- Update from master
  - Fix conversion to ISO-2022-JP-2 with ISO-8859-7 designation
    (BZ#12814)
  - Undo accidental change in x86-64 user.h
  - Update Japanese translation
  - Define RLIMIT_RTTIME (BZ#12795)
  - Update longlong.h from GCC
  - Add a few more alloca size checks (BZ#12671)
  - Fix flags parameter value passed to pltenter and pltexit
  - Define CLOCK_REALTIME_ALARM and CLOCK_BOOTTIME_ALARM
  - Always fill output buffer in XPG strerror function (BZ#12782)
  - Nicer output for negative error numbers in strerror_r
  - Fix CP1258 conversion (BZ#12777)
  - Fix handling of LC_CTYPE in locale name handling (BZ#12788)
  - Set stream errors in more cases (BZ#12792)
  - Don't unconditionally use alloca in gaih_inet (BZ#11869)
  - Update documentation in regex.h (BZ#11857)
  - Prevent Altivec and VSX insns on PowerPC64 when no FPRs or VRs are
    available
  - Fix typo in x86-64 powl (BZ#12775)
- Avoid overriding CFLAGS (#703880)

* Sat May 21 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.25.el6

* Wed May 18 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-13
- Update from master
  - Update GB18030 to 2005 version (BZ#11837)
  - Update RE_SYNTAX*_AWK constants in regex.h
  - Handle long variable names in putenv (BZ#11892)
  - Fix test for error_one_per_line mode in error (BZ#12766)
  - Cleanup x86-64 sys/user.h (BZ#11820)
  - Several locale data updates (BZ#11987, BZ#9732, BZ#9730, BZ#4357,
    BZ#12582)
  - Avoid potential deadlock in mtrace (BZ#6420)
  - Fix a few problems in fopen and freopen
  - Provide more helpful error message in getopt (BZ#7101)
  - Make stack canary value harder to read through read overflow (BZ#10149)
  - Use mmap for allocation of buffers used for __abort_msg (BZ#11901)
  - Fix handling of static TLS in dlopen'ed objects (BZ#12453)
  - Fix initialization of optimization values for AIO (BZ#12083)
  - Fix handling of conversion problem in CP932 module (BZ#12601)
  - Fix potential problem with out-of-scope buffer (BZ#12626)
  - Handle recursive calls in backtrace better (BZ#12432)
  - Fix handling of incomplete character storage in state
  - Fix file descriptor position after fclose (BZ#12724)
- Reinstall NIS RPC headers

* Fri May 13 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-12
- Update from master
  - Fix resizing table for unique symbols when adding symbol for copy
    relocation (BZ#12511)
  - Fix sched_setscheduler call in spawn implementation (BZ#12052)
  - Report write error in addmnt even for cached streams (BZ#12625)
  - Translate kernel error into what pthread_create should return
    (BZ#386)
  - More configurability for secondary group lookup (BZ#11257)
  - Several locale data updates (BZ#11258, BZ#11487, BZ#11532,
    BZ#11578, BZ#11653, BZ#11668, BZ#11945, BZ#11947, BZ#12158,
    BZ#12200, BZ#12178, BZ#12178, BZ#12346, BZ#12449, BZ#12545,
    BZ#12551, BZ#12611, BZ#12660, BZ#12681, BZ#12541, BZ#12711,
    BZ#12738)
  - Fix Linux getcwd for long paths (BZ#12713)
  - static tls memory leak on TLS_DTV_AT_TP archs
  - Actually undefine ARG_MAX from <linux/limits.h>
  - Backport BIND code to query name as TLD (BZ#12734)
  - Allow $ORIGIN to reference trusted directoreis in SUID binaries
    (BZ #12393)
  - Add missing {__BEGIN,__END}_DECLS to sys/sysmacros.h
  - Report if no record is found by initgroups in nss_files
- Never leave $ORIGIN unexpanded
- Revert "Ignore origin of privileged program"
- Reexport RPC interface

* Thu May  5 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-11
- Update from master
  - Don't use removed rpc headers
- Install rpc/netdb.h again

* Wed May  4 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-10
- Update from master
  - ldconfig: don't crash on empty path in config file (#699784)
  - getaddrinfo(AF_INET6) does not return scope_id info provided by
    NSS modules (BZ#12714)
  - Fix pathconf(_PC_BUF_SIZE) (BZ#12723)
  - Fix getnameinfo flags parameter type (BZ#12717)
  - Add finer grained control for initgroups lookups to NSS
  - Use all possible bytes from fopen mode string (BZ#12685, #698025)
  - Define initgroups callback for nss_files
  - elf.h: Define R_ARM_IRELATIVE reloc type
  - Fix static linking with checking x86/x86-64 memcpy (BZ#12653)
  - Fix POWER4/POWER7 optimized strncmp to not read past differing bytes
  - Fix FPU context handling in getcontext on x86-64 (BZ#12420)
  - Skip extra zeroes when searching auxv on s390
  - Obsolete RPC implementation in libc
  - Fix memory leak in TLS of loaded objects (BZ#12650)
  - Don't leave empty element in rpath when skipping an element
  - Make ppc sync_file_range cancelable
  - Maintain stack alignment in ____longjmp_chk on x86_64

* Mon Apr 11 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.7.el6_0.5

* Thu Apr  7 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-9
- Update from master
  - Fix typo in cache information table for x86-{32,64}
  - Define CLOCK_BOOTTIME, O_PATH, AT_EMPTY_PATH
  - Work around old buggy program which cannot cope with memcpy
    semantics (BZ#12518)
  - Fix visibility of declarations of wcpcpy and wcpncpy (BZ#12631)
  - Add clock_adjtime, name_to_handle_at, open_by_handle_at, syncfs
    syscalls
  - Really implement fallocate{,64} and sync_file_range as
    cancellation points
- Enable systemtap support (#690281)

* Thu Mar 24 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-8
- Update from master
  - Fix infinite loop (#690323)

* Mon Mar 21 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-7
- Update from master
  - Handle page boundaries in x86 SSE4.2 strncmp (BZ#12597)
  - Implement x86 cpuid handling of leaf4 for cache information (BZ#12587)
  - Check size of pattern in wide character representation in fnmatch
    (BZ #12583)
  - Remove __restrict quals from wmemcmp prototype
  - Fix copy relocations handling of unique objects (BZ#12510)
- ldd: never run file directly
- Ignore rpath elements containing non-isolated use of $ORIGIN when
  privileged
- Don't leave empty element in rpath when skipping the first element
- Revert "Don't crash when dependencies are missing" (#688990)

* Tue Mar 15 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.7.el6_0.4

* Mon Mar  7 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-6
- Update from master
  - Fix loading first object along a path when tracing
  - Enable SSE2 memset for AMD'supcoming Orochi processor
  - Don't read past end of buffer in fmemopen
- Revert broken changes (#682307)

* Wed Mar  2 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-5
- Update from master
  - Fix memory leak in dlopen with RTLD_NOLOAD (BZ#12509)
  - Don't crash when dependencies are missing (BZ#12454)
  - Fix allocation when handling positional parameters in printf
    (BZ#12445)
  - Fix two printf handler issues
- Fix false assertion (BZ#12454, #673014)

* Mon Feb 14 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-4
- Update from master
  - Update sysdeps/unix/sysv/linux/sparc/bits/socket.h
  - Synchronize generic bits/sched.h cpu_set_t with Linux implementation
  - Schedule nscd cache pruning more accurately from re-added values
  - Fix passing symbol value to pltexit callbacks when ld.so auditing
  - Fix range error handling in sgetspent
- Revert "Fix ordering of DSO constructors and destructors" (#673014)
- Create debuginfo-common on biarch archs
- Reinstall assembler workaround.
- Replace setuid by file capabilities (#646469)

* Tue Jan 25 2011 Andreas Schwab <schwab@redhat.com> - 2.13.90-1
- Update from master
  - Fix ordering of DSO constructors and destructors (BZ#11724)
- Remove no longer needed assembler workaround

* Tue Jan 18 2011 Andreas Schwab <schwab@redhat.com> - 2.13-1
- Update to 2.13 release
  - Define AT_NO_AUTOMOUNT
  - Define MADV_HUGEPAGE and MADV_NOHUGEPAGE
  - Add definitions for new socket protocols
  - Signal temporary host lookup errors in nscd as such to the
    requester (BZ#6812)
  - Change setgroups to affect all the threads in the process
    (BZ#10563)
  - FIx handling of unterminated [ expression in fnmatch (BZ#12378)
  - Relax requirement on close in child created by posix_spawn
  - Fix handling of missing syscall in Linux mkdirat (BZ#12397)
  - Handle long lines in host lookups in the right place (BZ#10484)
  - Fix assertion when handling DSTs during auditing
  - Fix alignment in x86 destructor calls
  - Fix grouping when rounding increases number of integer digits
    (BZ#12394)
  - Update Japanese translations
  - Fix infloop on persistent failing calloc in regex (BZ#12348)
  - Use prlimit64 for 32-bit [gs]etrlimit64 implementation (BZ#12201)
  - Change XPG-compliant strerror_r function to return error code
    (BZ#12204)
  - Always allow overwriting printf modifiers etc.
  - Make PowerPC64 default to nonexecutable stack

* Sat Jan 15 2011 Cristian Gafton <gafton@amazon.com>
- revert gcc44 build requirement

* Tue Dec 14 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-21
- Revert bogus change

* Mon Dec 13 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-20
- Update from master
  - Declare wcpcpy and wcpncpy only under _GNU_SOURCE
  - Fix use of restrict in wchar.h and string.h
  - Fix race in qsort_r initialization (BZ#11655)
  - Don't ignore zero TTL in DNS answers
  - Allow aux_cache_file open()ing to fail silently even in the chroot
    mode (BZ#11149)
  - Fix multiple nss_compat initgroups() bugs (BZ#10085)
  - Define MAP_HUGETLB and SWAP_FLAG_DISCARD
- Remove .UTF-8 suffix from locale names when it is the only supported
  codeset (#657556)
- Don't ignore $ORIGIN in libraries

* Thu Dec 2 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.7.el6_0.3
- import source package RHEL6/glibc-2.12-1.7.el6

* Fri Nov 12 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-19
- Update from master
  - Fix memory leak in fnmatch
  - Support Intel processor model 6 and model 0x2c
  - Fix comparison in sqrtl for IBM long double
  - Fix one exit path in x86-64 SSE4.2 str{,n}casecmp (BZ#12205, #651638)
  - Fix warnings in __bswap_16 (BZ#12194)
  - Use IFUNC on x86-64 memset
  - Power7-optimized mempcpy
  - Handle uneven cache size in 32bit SSE2 memset (BZ#12191)
  - Verify in ttyname that the symlink is valid (BZ#12167)
  - Update Danish translations
  - Fix concurrency problem between dl_open and dl_iterate_phdr
  - Fix x86-64 strchr propagation of search byte into all bytes of SSE
    register (BZ#12159)
  - Fix perturbing in malloc on free (BZ#12140)
  - PPC/A2 optimized memcpy function
  - Add C99 FP_FAST_FMA{,F,L} macros to <math.h>
- Check that the running kernel is new enough (#649589)

* Fri Oct 22 2010 Cristian Gafton <gafton@amazon.com>
- add patch for CVE-2010-3856
- add DST expansion avoidance patch

* Fri Oct 22 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-18
- Require suid bit on audit objects in privileged programs (CVE-2010-3856)

* Tue Oct 19 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-17
- Update from master
  - Fix some fma issues, implement fmal (BZ#3268, #43358)
  - Expect PLT call to _Unwind_Find_FDE on s390*-linux
- Never expand $ORIGIN in privileged programs (#643306, CVE-2010-3847)

* Mon Oct 18 2010 Cristian Gafton <gafton@amazon.com>
- add patch for CVE-2010-3847

* Thu Oct 14 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-16
- Update from master
  - Implement accurate fma (BZ#3268, #43358)
  - Fix alignment of AVX save area on x86-64 (BZ#12113)
  - Fix regex memory leaks (BZ#12078)
  - Improve output of psiginfo (BZ#12107, BZ#12108)
  - Don't return NULL address in getifaddrs (BZ#12093)
  - Fix strstr and memmem algorithm (BZ#12092, #641124)
- Don't discard result of decoding ACE if AI_CANONIDN (#636642)
- Remove /etc/gai.conf from glibc-common and mark it %%ghost in glibc
- Require exact glibc version in nscd

* Mon Oct  4 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-15
- Update from master
  - Handle large requests in debugging hooks for malloc (BZ#12005)
  - Fix handling of remaining bytes in buffer for strncmp and
    strncasecmp (BZ#12077)
  - Handle cgroup and btrfs filesystems in statvfs
  - S/390: Fix highgprs check in startup code (BZ#12067)
  - Properly convert f_fsid in statvfs (BZ#11611)

* Tue Sep 28 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-14
- Don't try to write to _rtld_global_ro after performing relro
  protection (#638091)

* Mon Sep 27 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-13
- Update from master
  - Add two forgotten licence exceptions
  - getdents64 fallback d_type support
  - Move freeres function from ld.so to libc.so
  - Undo feature selection for ftruncate (BZ#12037)
  - Fix namespace pollution in pthread_cleanup_push
  - Fix limit detection in x86-64 SSE2 strncasecmp (#632560)
  - Add support for fanotify_mark on sparc32 and s390
  - Fix register conflict in s390 ____longjmp_chk (#629970)
  - Don't try to free rpath strings allocated during startup (#629976)
  - Actually make it possible to user the default name server
- Fix memory leak on init/fini dependency list (#632936)
- Fix handling of collating symbols in regexps (BZ#11561)
- Don't parse %%s format argument as multibyte string (BZ#6530)
- Fix overflow in nss files parser
- Fix spurious nop at start of __strspn_ia32

* Wed Sep 15 2010 Dennis Gilmore <dennis@ausil.us> - 2.12.90-12
- dont build sparcv9v and sparc64v anymore

* Mon Sep 13 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-11
- Update from master
  - Fix _FORITY_SOURCE version of longjmp for Linux/x86-64 (BZ#11968)
- Work around shortest-stem feature in make 3.82+

* Mon Sep  6 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-10
- Update from master
  - Remove invalid iconv aliases (BZ#11979)
  - Update x86-64 mpn routines from GMP 5.0.1
  - Fix array overflow in floating point parser (BZ#7066)
  - Support fanotify_mark syscall on powerpc32
  - Unroll x86-64 strlen
  - Unroll 32bit SSE strlen and handle slow bsf
  - Missing server address again leads to localhost being used (BZ#10851)
- Revert last change
- Remove or don't install unpackaged files for auxarches

* Sat Sep 04 2010 Dennis Gilmore <dennis@ausil.us> - 2.12.90-9
- disable unpackaged file check on auxarches

* Mon Aug 23 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-8
- Update from master
  - Fix static strspn on x86 (#624852)
  - Various POWER7 optimized string functions
  - Fix x86 pthread_cond_signal() FUTEX_WAKE_OP fallback
  - Add optimized strncasecmp versions for x86-64
  - PowerPC64 ABI fixes
  - Properly quote output of locale (BZ#11904)
  - f_flags in statfs implementation
  - Add support for fanotify_init and fanotify_mask syscalls
  - Add support for prlimit and prlimit64
  - Fix IPTOS_CLASS definition (BZ#11903)
  - Avoid too much stack use in fnmatch (BZ#11883)
  - x86: Add support for frame pointer less mcount
- Disable asynchronous-unwind-tables during configure run

* Mon Aug  2 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-7
- Update from master
  - Add optimized x86-64 implementation of strnlen and strcaecmp
  - Document M_PERTURB
  - Fix vDSO synthetic hwcap handling so they are not masked out from
    ld.so.cache matching
  - POWER6/7 optimizations for copysign
- Build with ports addon on alpha and armv5tel
- Add conflict with kernel < 2.6.32 (#619538)
- Switch to xz compressed tar files
- build-locale-archive: process only directories matching *_*

* Thu Jul 22 2010 Nathan Blackham <blackham@amazon.com>
- adding exclusive arch line to remove i386

* Wed Jul 21 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-6
- Bump minimum kernel version to 2.6.32

* Tue Jul 20 2010 Matt Wilson <msw@amazon.com>
- add fix for hwcap flag handling in ld.so.cache (bz#615701)

* Sun Jul 18 2010 Matt Wilson <msw@amazon.com>
- back out LD_HWCAP_MASK change, it breaks up the nosegneg hwcap ld.so.cache lookups

* Fri Jul 16 2010 Matt Wilson <msw@amazon.com>
- disable strict build id checking when building debuginfo for now

* Wed Jul 14 2010 Matt Wilson <msw@amazon.com>
- disable avx support by force, our current binutils does not support it. remove debuginfo files if it is disabled

* Wed Jul 14 2010 Nathan Blackham <blackham@amazon.com>
- moving to gcc44, and disabling multiarch

* Mon Jul 12 2010 Nathan Blackham <blackham@amazon.com>
- disable multiarch optimizations as it requires a newer version of binutils

* Mon Jul 12 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-5
- Update from master
  - Don't pass NULL occation to dl_signal_cerror
  - Implement _PC_PIPE_BUF.
- Add glibc-ports tarball

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/glibc-2.12-1.2.el6
- import source package RHEL6/glibc-2.11.1-1.10.el6

* Fri Jul  2 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-4
- Update from master
  - Work around kernel rejecting valid absolute timestamps
  - Improve 64bit memcpy/memmove for Atom, Core 2 and Core i7
  - Fix error handling in Linux getlogin*
- Workaround assembler bug sneaking in nopl (#579838)
- Fix scope handling during dl_close
- Fix setxid race handling exiting threads

* Tue Jun 15 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-3
- Update from master
  - Power7 string compare optimizations
  - Properly resize buffer in NIS initgroups
  - Define F_SETPIPE_SZ and F_GETPIPE_SZ
  - Fix more C++ incompatibility problems in headers
- Properly set __libc_multiple_libcs
- Don't assume AT_PAGESIZE is always available (#597578)
- Don't call uname or getrlimit in libpthread init function (#579086)
- Mark /etc/rpc as %%config (#587050)

* Mon May 31 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-2
- Update from master
  - Small fix to POWER7 32-bit memcpy
  - Correct x86 CPU family and model check (BZ#11640, #596554)
  - Fix iov size in SH register_dump
  - Don't crash on unresolved weak symbol reference
  - Implement recvmmsg also as socketcall
  - sunrpc: Fix spurious fall-through
  - Make <sys/timex.h> compatible with C++ (#593762)
- Fix users and groups creation in nscd %%post script

* Thu May 20 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/glibc-2.5-49
- import source package RHEL5/glibc-2.5-42.el5_4.3
- import source package RHEL5/glibc-2.5-42.el5_4.2
- import source package RHEL5/glibc-2.5-42
- import source package RHEL5/glibc-2.5-34.el5_3.1
- import source package RHEL5/glibc-2.5-34
- import source package RHEL5/glibc-2.5-24.el5_2.2
- import source package RHEL5/glibc-2.5-24
- import source package RHEL5/glibc-2.5-18.el5_1.1
- import source package RHEL5/glibc-2.5-18
- import source package RHEL5/glibc-2.5-12
- added submodule prep for package glibc

* Wed May 19 2010 Andreas Schwab <schwab@redhat.com> - 2.12.90-1
- Update from master
  - POWER7 optimized memset
  - Fix typo in es_CR locale
  - Enable IDN support in getent
  - Fix race in free sanity check
  - Fix lookup of collation sequence value during regexp matching
  - Fix name of tt_RU.UTF-8@iqtelif locale (#589138)
  - Handle too-small buffers in Linux getlogin_r (BZ#11571, #589946)

* Tue May  4 2010 Roland McGrath <roland@redhat.com> - 2.12-1
- Update to 2.12 release.
  - Fix ldconfig chroot handling.
  - Don't deadlock in __dl_iterate_phdr while (un)loading objects.
  - Fix handling of newline in addmntent.
  - Fix AIO when thread creation failed.

* Fri Apr 16 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-20
- Update from master
  - Fix bugs in x86-32 strcmp-sse4.S and strcmp-ssse3.S
  - Add x86-32 FMA support
  - Don't crash in trace mode when dependencies are missing
  - x86-64 SSE4 optimized memcmp
  - Fix makecontext on s390/s390x

* Tue Apr 13 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-19
- Avoid multiarch memcmp in tzdata-update (#581677)

* Mon Apr 12 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-18
- Update from master
  - Implement interfaces to set and get names of threads (BZ#11390)
  - Locale data updates (BZ#10824, BZ#10936, BZ#11470, BZ#11471)
  - Print reload count in nscd statistics (BZ#10915)
  - Fix reading loginuid file in getlogin{,_r}
  - Fix fallocate error return on i386
  - Fix cproj implmentation (BZ#10401)
  - Fix getopt handing (BZ#11039, BZ#11040, BZ#11041)
  - Implement new mode for NIS passwd.adjunct.byname table (BZ#11134)
  - Obey LD_HWCAP_MASK in ld.so.cache lookups

* Tue Apr  6 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-17
- Update from master
  - Locale data updates (BZ#11007, BZ#11258, BZ#11272, BZ#10554)
  - Handle DNS timeouts in old-style lookup code (BZ#11010)
  - Fix aux cache handling in ldconfig with chroot (BZ#11149)
  - Fix printing error messages in getopt (BZ#11043)
  - Declare iruserok and iruserok_af (BZ#11070)
  - Fix option aliasing in argp (BZ#11254)
  - Handle POSIX-compliant errno value of unlink in remove (BZ#11276)
  - Fix definition and testing of S_ISSOCK (BZ#11279)
  - Fix retrieving of kernel header version (BZ#11287)
  - Fix concurrent handling of __cpu_features (BZ#11292)
  - Handle unnecessary padding in getdents64 (BZ#11333)
  - Fix changes to interface list during getifaddrs calls (BZ#11387)
  - Missing memory barrier in DES initialization (BZ#11449)
  - Fix spurious UNAVAIL status is getaddrinfo
  - Add support for new clocks (BZ#11389)
  - Fix Linux getlogin{_r,} implementation
  - Fix missing zero-termination in cuserid (BZ#11397)
  - Fix glob with empty pattern
  - Fix handling of STB_GNU_UNIQUE in LD_TRACE_PRELINKING
  - Unify wint_t handling in wchar.h and wctype.h (BZ#11410)
  - Implement handling of libc ABI in ELF header
  - Don't underestimate length of DST substitution in rpath
  - Power7-optimized 64-bit and 32-bit memcpy
- Assign global scope to RFC 1918 addresses (#577626)

* Thu Mar 18 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-16
- Fix SSSE3 memcmp (#574210)

* Tue Mar  9 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-15
- Update from master
  - sparc64: Fix handling of R_SPARC_TLS_LE_* relocations (#571551)
  - Handle ext4 and logfs in statvfs functions
  - Fix setxid race with thread creation
  - Pass -mtune=i686 to assembler when compiling for i686
  - Fix R_X86_64_PC32 overflow detection
  - Fix msgrcv on sparc64
  - Fix unwind info in x86 strcmp-sse4.S (BZ#11332)
  - sparc: Add multiarch support for memset/bzero/memcpy
- Remove directories owned by filesystem (#569414)
- Add %%ghost /etc/gai.conf to glibc-common (#567748)

* Tue Feb 23 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-14
- Update from master
  - Sparc updates
- Fix SSSE3 memcpy (#556584)

* Mon Feb 22 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-13
- Update from master
  - Use CPUID_OFFSET instead of FEATURE_OFFSET
  - Add 32bit memcmp/strcmp/strncmp optimized for SSSE3/SSS4.2
  - Fix file descriotor leak in nftw with FTW_CHDIR (BZ#11271)
  - Add Sparc STT_GNU_IFUNC support
  - Add power7-optimized classification functions
- Reapply "Optimize 32bit memset/memcpy with SSE2/SSSE3."
- Use unsigned comparison in sse memcpy/memset

* Mon Feb  8 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-12
- Update from master
  - Update constants in <sys/mount.h> for current kernels (#11235)
  - Fix endless loop with invalid /etc/shells file (#11242)
  - Fix sorting of malayalam letter 'na' (#10414)
  - Add kok_IN locale
  - Use common collation data in as_IN locale
  - Avoid alloca in setenv for long strings
- Use shared mapping to reserve memory when creating locale archive (#10855)
- Fix fstat on Linux/sparc64 (#11155)

* Mon Feb  1 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-11
- Update from master
  - Fix error checking in iconv (#558053)
  - Don't map U00DF to U1E9E in toupper table
  - _nl_load_locale() incorrectly handles mmap() failures (BZ#11200)
  - Fix various issues in regex matcher (BZ#11183, BZ#11184, BZ#11185,
    BZ#11186, BZ#11187, BZ#11188, BZ#11189, BZ#11190, BZ#11191,
    BZ#11192, BZ#11193)

* Tue Jan 19 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-10
- Update from master
  - Fix ____longjmp_chk for s390/s390x
  - Remove duplicate definitions of O_DSYNC and O_RSYNC for Linux/sparc
  - Ignore negative dynamic entry types (#546890)
  - Fix pthread_cond_*wait with requeue-PI on i386 (#548989)
  - Fix _XOPEN_SOURCE_EXTENDED handling
- Revert "Optimize 32bit memset/memcpy with SSE2/SSSE3."

* Fri Jan 15 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-9
- Update from master.
  - Define IPTOS_CLASS_* macros according to RFC 2474 (BZ#11027)
  - Always use IPv4 sockets for IPv4 addresses (BZ#11141)
  - regcomp.c: do not ignore memory allocation failure (BZ#11127)
  - Fix malloc_info without prior allocations (BZ#11126)
  - Optimize 32bit memset/memcpy with SSE2/SSSE3
  - Relax feature tests in headers

* Tue Jan 12 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-8
- Update from master.
  - More POSIX conformance fixes.

* Mon Jan 11 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-7
- Fix build failure.

* Mon Jan 11 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-6
- Update from master.
  - POSIX conformance fixes (BZ#11125).

* Mon Jan  4 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-5
- Update from master.
  - Additional setcontext(), etc. conformance tests (BZ#11115).
  - Handle AT_FDCWD in futimens (BZ#10992).
  - Update poll.h header for POSIX 2008 (BZ#11093).
  - Avoid ELF lookup race.

* Mon Dec 14 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-4
- Update from master.
  - Add Requeue-PI support for x86 arch.
  - Redefine O_SYNC and O_DSYNC to match 2.6.33+ kernels.
  - Fix a few error cases in *name4_r lookup handling (BZ#11000).
  - Fix kernel version check in recent ptsname change (BZ#11046).
  - Add more warnings to exec functions (BZ#11056).
  - Add recvmmsg interface.
  - Define SCHED_IDLE and SCHED_RESET_ON_FORK for Linux.

* Mon Nov 30 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-3
- Update from master.
  - Fix infloop in __pthread_disable_asynccancel on x86_64 (#537690).
  - Prevent unintended file desriptor leak in grantpt (#530558).
  - Fix startup to security-relevant statically linked binaries (#528631).
- Re-install CFI in x86/x86_64 clone (#491542).

* Tue Nov 24 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-2
- Update from master.
  - Define week, first_weekday, and first_workday for en_DK locale (#525126).
  - Use struct timespec for timestamps in struct stat also if
    __USE_XOPEN2K8 (#539870).
  - Fix week information for nl_NL locale (#499748).
  - Update ntp_gettime for Linux (#479558).
  - Fix getwc* and putwc* on non-wide streams (BZ#10958).
  - Avoid warnings in CPU_* macros when using const bitsets (BZ#10918).
  - Handle LC_GLOBAL_LOCALE in duplocale (BZ#10969).
  - Fix _NC_LOCALE_NAME definition (BZ#10968).
  - Add missing Linux MADV_* definitions (BZ#10972).
  - Add support for new Linux error ERFKILL (BZ#10939).
- Enable multi-arch support on ppc and ppc64.

* Thu Nov 12 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-1
- Update from master.

* Thu Nov  5 2009 Andreas Schwab <schwab@redhat.com> - 2.11-2
- Fix readahead on powerpc32.
- Fix R_PPC64_{JMP_IREL,IRELATIVE} handling.
- Fix preadv, pwritev and fallocate for -D_FILE_OFFSET_BITS=64 (#533063).

* Mon Nov  2 2009 Andreas Schwab <schwab@redhat.com> - 2.11-1
- Update to 2.11 release.
- Disable multi-arch support on PowerPC again since binutils is too old.
- Fix crash in tzdata-update due to use of multi-arch symbol (#532128).

* Fri Oct 30 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-27
- Update from master.
  - Fix races in setXid implementation (BZ#3270).
  - Implement IFUNC for PPC and enable multi-arch support.
  - Implement mkstemps/mkstemps64 and mkostemps/mkostemps64 (BZ#10349).
  - Fix IA-64 and S390 sigevent definitions (BZ#10446).
  - Fix memory leak in NIS grp database handling (BZ#10713).
  - Print timestamp in nscd debug messages (BZ#10742).
  - Fix mixing IPv4 and IPv6 name server in resolv.conf.
  - Fix range checks in coshl.
  - Implement SSE4.2 optimized strchr and strrchr.
  - Handle IFUNC symbols in dlsym (#529965).
  - Misc fixes (BZ#10312, BZ#10315, BZ#10319, BZ#10391, BZ#10425,
    BZ#10540, BZ#10553, BZ#10564, BZ#10609, BZ#10692, BZ#10780,
    BZ#10717, BZ#10784, BZ#10789, BZ#10847
- No longer build with -fno-var-tracking-assignments.

* Mon Oct 19 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-26
- Update from master.
  - Add ____longjmp_chk for sparc.
- Avoid installing the same libraries twice.

* Mon Oct 12 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-25
- Update from master
  - Fix descriptor leak when calling dlopen with RTLD_NOLOAD (#527409).
  - Fix week-1stday in C locale.
  - Check for integer overflows in formatting functions.
  - Fix locale program error handling (#525363).

* Mon Sep 28 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-24
- Update from master.
  - Fix missing reloc dependency (#517001).

* Mon Sep 21 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-23
- Update from master.

* Mon Sep 14 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-22
- Update from master.
  - Fix endless loop in localedef.
  - Fix __longjmp_chk on s390/s390x.
- Fix exit codes in nscd start script (#521848).
- Build with -fno-var-tracking-assignments for now (#523172).

* Mon Sep  7 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-21
- Update from master.
  - Fix strstr/strcasestr on i386 (#519226).

* Thu Sep  3 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-20
- Update from master.
  - Fix strstr/strcasestr/fma/fmaf on x86_64 (#519226).
  - Fix lookup of group names in hesiod initgroups (#520472).

* Wed Sep  2 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-19
- Update from master.
  - Fix x86_64 bits/mathinline.h for -m32 compilation.

* Tue Sep  1 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-18
- Update from master.
  - fix parse error in <bits/mathinline.h> (#520209).

* Thu Aug 27 2009 Roland McGrath <roland@redhat.com> - 2.10.90-17
- Update from master.

* Wed Aug 26 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-16
- Update from master.
  - handle AVX saving on x86-64 in interrupted symbol lookups (#519081).

* Mon Aug 24 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-15
- Update from master.
  - fix fortify failure with longjmp from alternate stack (#512103).
- Add conflict with prelink (#509655).

* Mon Aug 17 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-14
- Update from master.
  - fix pthread_cond_signal (#516469)

* Mon Aug 10 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-13
- Update from master.
  - fix rehashing of unique symbols (#515677)
- Fix spurious messages with --excludedocs (#515948)

* Mon Aug  3 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-12
- Update from master.
  - fix fortify failure with longjmp from alternate stack (#512103)

* Thu Jul 30 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-11
- Update from master.
- Don't package debuginfo files in glibc-devel.

* Tue Jul 28 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-10
- Update from master.
  * fix memory ordering in pthread_mutex_unlock (BZ#10418)
  * implement RES_USE_DNSSEC option in resolver (#205842)
  * fix hang in ldd -r (#513945)

* Mon Jul 27 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-9
- Update from master.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.90-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jakub Jelinek <jakub@redhat.com> - 2.10.90-7.1
- Fix up pthread_cond_timedwait on x86_64 with old kernels.

* Thu Jul 23 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-7
- Update from master.
- Build with -DNDEBUG unless using a prerelease.

* Thu Jul 23 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-6
- Rebuilt with binutils-2.19.51.0.14-29.fc12 to fix static binaries

* Wed Jul 22 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-5
- Update from master.
- Undefine __i686 on x86 to fix build.

* Mon Jul 20 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-4
- Update from master.
- Don't build separate i686 package.

* Wed Jul  8 2009 Andreas Schwab <schwab@redhat.com> 2.10.90-3
- Reenable setuid on pt_chown.

* Thu Jul  2 2009 Andreas Schwab <aschwab@redhat.com> 2.10.90-2
- Update from master.

* Fri Jun 26 2009 Andreas Schwab <aschwab@redhat.com> 2.10.90-1
- Update from master.
- Enable multi-arch support on x86/x86-64.
- Add requires glibc-headers to glibc-devel (#476295).
- Implement second fallback mode for DNS requests (#505105).
- Don't generate invalid POSIX TZ string for Asia/Dhaka timezone (#506941).
- Allow backtrace through __longjmp_chk on powerpc.

* Fri May 22 2009 Jakub Jelinek <jakub@redhat.com> 2.10.1-2
- fix accept4 on architectures other than i?86/x86_64
- robustify nscd client code during server GC
- fix up nscd segfaults during daemon shutdown
- fix memchr on ia64 (BZ#10162)
- replace the Sun RPC license with the BSD license, with the explicit
  permission of Sun Microsystems
- fix up powerpc long double errno reporting

* Sun May 10 2009 Jakub Jelinek <jakub@redhat.com> 2.10.1-1
- fix up getsgent_r and getsgnam_r exports on i?86 and ppc

* Sat May  9 2009 Jakub Jelinek <jakub@redhat.com> 2.10-2
- update from trunk
  - glibc 2.10 release
  - fix memchr on x86_64 (#499689)

* Mon Apr 27 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-22
- update from trunk
  - further localedef fixes
- fix build-locale-archive

* Fri Apr 24 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-21
- update from trunk
  - fix localedef
  - fix SHIFT_JIS iconv EILSEQ handling (#497267)
  - misc fixes (BZ#10093, BZ#10100)

* Fri Apr 24 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-20
- update from trunk
  - fix p{read,write}v{,64} (#497429, #497434)
  - fix strfmon (#496386)

* Thu Apr 16 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-19
- update from trunk
  - fix dlopen from statically linked binaries (#495830)

* Thu Apr 16 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-18
- update from trunk
  - fix fallocate

* Wed Apr 15 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-17
- update from trunk
  - if threads have very small stack sizes, use much smaller buffer
    in __get_nprocs when called from within malloc (#494631)

* Tue Apr 14 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-16
- update from trunk

* Thu Apr  9 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-15
- rebuilt with fixed gcc to avoid miscompilation of i586 memmove
- reenable experimental malloc again

* Wed Apr  8 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-14
- update from trunk
- temporarily disable experimental malloc

* Tue Apr  7 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-13
- update from trunk
  - fix strverscmp (#494457)
- configure with --enable-nss-crypt

* Wed Apr  1 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-12
- update from trunk
- configure with --enable-experimental-malloc

* Fri Mar 20 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-11
- update from trunk
  - POSIX 2008 prototype adjustments for scandir{,64}, alphasort{,64} and
    versionsort{,64}
  - fix libthread_db (#491197)

* Tue Mar 10 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-10
- update from trunk
  - fix atexit/__cxa_atexit

* Mon Mar  9 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-9
- update from trunk
  - POSIX 2008 support: -D_XOPEN_SOURCE=700 and -D_POSIX_C_SOURCE=200809L
- move libnldbl_nonshared.a on ppc*/s390*/sparc* back to glibc-devel

* Fri Feb 27 2009 Roland McGrath <roland@redhat.com> - 2.9.90-8.1
- fix libthread_db (#487212)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.90-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-7
- update from trunk
- adjust for i586 + i686 from i386 + i686 build
- split static libraries into glibc-static subpackage
- ld -r the whole libpthread.a together to avoid endless issues with
  -static ... -lpthread
- require 2.6.18 and later kernel

* Wed Feb  4 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-3
- update from trunk
  - ISO C++ compliant strchr etc. with GCC 4.4+
  - AT_RANDOM support

* Thu Jan  8 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-2
- update from trunk

* Fri Jan  2 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-1
- update from trunk (#478314)

* Mon Dec  8 2008 Jakub Jelinek <jakub@redhat.com> 2.9-3
- temporarily disable _nss_dns_gethostbyname4_r (#459756)
- NIS hostname lookup fixes (#473073, #474800, BZ#7058)
- fix unsetenv (#472941)

* Thu Nov 13 2008 Jakub Jelinek <jakub@redhat.com> 2.9-2
- glibc 2.9 release
- fix CPU_ALLOC_SIZE on 32-bit arches (BZ#7029)

* Wed Nov 12 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-17
- update from trunk
  - don't abort on broken DNS replies (#469299, BZ#7009)
  - misc fixes (BZ#6966, BZ#7008, BZ#6955, BZ#6843)

* Fri Oct 31 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-16
- update from trunk
  - further resolver fixes
  - another dynamic TLS handling fix (#469263)
  - misc fixes (BZ#6867, BZ#6875, BZ#6919, BZ#6920, BZ#6942, BZ#6947,
                BZ#6968, BZ#6974, BZ#6980, BZ#6995)
- rebuild with newer rpm to avoid stripping
  shared libraries when they shouldn't be (#468129)

* Tue Oct 28 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-15
- update from trunk
  - __libc_res_nquery fixes (#466786)

* Sun Oct 19 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-14
- update from trunk
  - fix dynamic TLS handling (#467309)
  - fix sys/signalfd.h for C++ (#467172)
  - fix sprof (#458861)
  - fix _mcount and socket syscalls on s390x (#464146)
  - try harder to allocate memory in valloc and pvalloc (#461481)
- fix power6 32-bit libs (#467311)

* Fri Oct 10 2008 Dennis Gilmore <dennis@ausil.us> 2.8.90-13
- apply sparcv9v memset patch from jakub and davem

* Fri Aug 29 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-12
- update from trunk
  - revert origin changes (#457849)
  - use MAP_STACK for thread stacks
  - misc fixes (BZ#6845, BZ#6544, BZ#6634, BZ#6589, BZ#6790, BZ#6791,
    BZ#6824)
  - power7 bits (BZ#6817)
  - fix expm1 on i?86/x86_64 (#43354, BZ#5794)

* Sat Aug  2 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-11
- update from trunk
  - fix non-absolute $ORIGIN handling (#457560)
  - exported some further libresolv APIs (#453325)
  - misc fixes

* Tue Jul 29 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-10
- update from trunk
  - resolver fixes
  - misc fixes (BZ#6771, BZ#6763, BZ#6698, BZ#6712)
  - s390{,x} utmp/utmpx bi-arch support (BZ#6724)
  - popen "e" flag
- fr_FR locale changes reenabled

* Wed Jul 16 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-9
- update from trunk
  - fix unbuffered vfprintf if writing to the stream fails (#455360)
  - remove useless "malloc: using debugging hooks" message (#455355)
  - nscd fixes
  - fix resolver alignment issues (#454500)
  - fix setvbuf (BZ#6719)

* Thu Jul  3 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-8
- update from trunk
  - watch even resolv.conf in nscd using inotify
  - some nscd fixes

* Fri Jun 13 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-7
- update from trunk
  - avoid *lround* on ppc* clobbering cr3/cr4 registers (#450790)
  - further nscd fixes (#450704)
  - use inotify in nscd to watch files

* Thu Jun 12 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-6
- update from trunk
  - nscd fixes (#450704)
  - fix getservbyport (#449358)
  - fix regexp.h (#446406)
  - avoid crashing on T_DNAME in DNS responses (#450766)

* Sun May 25 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-5
- update from trunk

* Tue May 20 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-4
- further getaddrinfo and nscd fixes

* Sun May 18 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-3
- getaddrinfo and nscd fixes
- reenable assertion checking in rawhide

* Fri May 16 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-2
- fix getaddrinfo (#446801, #446808)

* Thu May 15 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-1
- update to trunk
  - O(n) memmem/strstr/strcasestr
  - i386/x86_64 TLS descriptors support
  - concurrent IPv4 and IPv6 DNS lookups by getaddrinfo

* Mon May  5 2008 Jakub Jelinek <jakub@redhat.com> 2.8-3
- don't run telinit u in %%post if both /dev/initctl and
  /sbin/initctl exist (#444978)
- workaround GCC ppc64 miscompilation of c{log{,10},acosh,atan}l
  (#444996)

* Wed Apr 30 2008 Jakub Jelinek <jakub@redhat.com> 2.8-2
- fix nscd races during GC (BZ#5381)
- rebuilt with fixed GCC to fix regex miscompilation on power6
- SPARC fixes

* Sat Apr 12 2008 Jakub Jelinek <jakub@redhat.com> 2.8-1
- 2.8 release

* Fri Apr 11 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-16
- update to trunk
  - misc fixes (BZ#4997, BZ#5741)
  - make sure all users of __libc_setlocale_lock know it is
    now a rwlock
  - fix ppc/ppc64 compatibility _sys_errlist and _sys_siglist
    symbols

* Thu Apr 10 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-15
- update to trunk
  - misc fixes (BZ#4314, BZ#4407, BZ#5209, BZ#5436, BZ#5768, BZ#5998,
		BZ#6024)
- restart sshd in %%post when upstart is used - it doesn't have
  /dev/initctl (#441763)
- disable assert checking again

* Tue Apr  8 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-14
- update to trunk
  - misc fixes (BZ#5443, BZ#5475, BZ#5478, BZ#5939, BZ#5979, BZ#5995,
                BZ#6004, BZ#6007, BZ#6020, BZ#6021, BZ#6042)
  - change mtrace to keep perl 5.10 quiet (#441082)
  - don't share conversion state between mbtowc and wctomb (#438687)
  - if st_blksize is too large and malloc fails, retry with smaller
    buffer in opendir (#430768)
  - correct *printf overflow test (#358111)

* Fri Mar 28 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-13
- update to trunk
  - don't define ARG_MAX in <limits.h>, as it is no longer
    constant - use sysconf (_SC_ARG_MAX) to get the current
    argument size limit
  - fix build on sparc64
- only service sshd condrestart if /etc/rc.d/init.d/sshd exists
  (#428859)

* Wed Mar 26 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-12
- update to trunk
  - new CLONE_* flags in <sched.h> (#438542)
  - nis+ errno clobbering fix (#437945)
  - fix adjtime (#437974)

* Fri Mar 14 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-11
- update to trunk
- remove <stropts.h>, define _XOPEN_STREAMS -1 (#436349)

* Wed Mar  5 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-8
- update to trunk
  - {,v}{as,d}printf and obstack_{,v}printf fortification (#435905)
  - fix getnameinfo/gethostbyaddr (#428067, BZ#5790)
  - fix yp_order (#435519, BZ#5854)
  - misc fixes (BZ#5779, BZ#5736, BZ#5627, BZ#5818, BZ#5012)
- merge review cleanup (Tom Callaway, #225806)

* Sat Feb 16 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-7
- update to trunk
  - make NI_MAXHOST and NI_MAXSERV available even in BSDish
    namespaces (BZ#5737)
  - timerfd_* syscalls

* Fri Feb  1 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-6
- fix build

* Thu Jan 31 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-5
- update to trunk
- rebuild with gcc 4.3

* Fri Jan 11 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-4
- update to trunk
  - misc fixes (BZ#5541, BZ#5545, BZ#5553, BZ#5112, BZ#5520)
  - getaddrinfo fixes
  - signalize EOVERFLOW from sem_post instead of overflowing
    the counter
  - fix i?86 makecontext
  - fix iconv for iso-2022-jp//translit (#397021)

* Thu Jan  3 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-3
- update to trunk
  - fix recognition of interface family (#425768)
  - add __THROW to __ctype_{b,tolower,toupper}_loc prototypes

* Thu Dec 27 2007 Jakub Jelinek <jakub@redhat.com> 2.7.90-2
- update to trunk
  - nsswitch fix (#425768)
- temporarily enable assert checking

* Wed Dec 12 2007 Jakub Jelinek <jakub@redhat.com> 2.7.90-1
- update to trunk
  - fix __USE_STRING_INLINES on i?86 (#408731, #371711)
  - fix *scanf (#388751)

* Wed Oct 17 2007 Jakub Jelinek <jakub@redhat.com> 2.7-1
- glibc 2.7 release
- fix tzfile.c for times after last transition (#333561)
- fix sem_post@GLIBC_2.0 on i?86
- appease valgrind in libpthread.so initialization
- misc fixes (BZ#3425, BZ#5184, BZ#5186)

* Mon Oct 15 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-21
- fix getgr{name,gid}{,_r} with nscd

* Sun Oct 14 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-20
- install <bits/error.h> (#330031)
- disable -D_FORTIFY_SOURCE{,=2} support (with a warning) for
  GCC 3.4.x and earlier(#327641)
- pl_PL locale changes (BZ#4098, #242296)
- misc fixes (BZ#1140, BZ#3195, BZ#3242, BZ#4359)

* Thu Oct 11 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-19
- fix <netinet/tcp.h>
- simple preprocessor in localedef, fix de_DE collation with it

* Wed Oct 10 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-18
- add signalfd, eventfd, eventfd_read, eventfd_write
- qsort speedups
- workaround for cpuid bugs (#324081)
- make sure gettext's conversion_lock is initialized even if
  program isn't linked against libpthread.so.0, only dlopens it (#321761)
- misc fixes (BZ#5112, BZ#5113, BZ#5104, BZ#5063, BZ#5010, BZ#4407,
  BZ#3924, BZ#5103, BZ#2633, BZ#181, BZ#73, #321901)

* Wed Oct  3 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-17
- fix {,v}swprintf with -D_FORTIFY_SOURCE=1 -mlong-double-64 on ppc*/s390*/sparc*
- strcoll fixes
- misc fixes (BZ#645, BZ#5071)
- locale fixes (BZ#4941, #299321, #203364, #196711, #236212)

* Sat Sep 29 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-16
- misc fixes (BZ#4963, BZ#4972, BZ#5028, BZ#5043, BZ#5058)
- improve -D_FORTIFY_SOURCE{,=2} diagnostic through warning/error
  attributes
- fix wcscpy, wcpcpy, fgetws, fgetws_unlocked, swprintf and vswprintf
  fortification inlines
- fix a scalability issue with lazy binding in heavily multithreaded
  programs

* Thu Sep 20 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-15
- $5$ (SHA-256) and $6$ (SHA-512) support in crypt
  (#228697, #249477, #173834)

* Tue Sep 18 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-14
- -D_FORTIFY_SOURCE{,=2} support for C++
- fortification of fread{,_unlocked}
- support *scanf m allocation modifier (%%ms, %%mls, %%mc, ...)
- in -std=c99 or -D_XOPEN_SOURCE=600 mode don't recognize
  %%as, %%aS and %%a[ as a GNU extension for *scanf
- fix splice, vmsplice, tee return value, make them cancellation
  points
- mq_open checking
- use inline function rather than function-like macro
  for open{,at}{,64} checking
- IFA_F_OPTIMISTIC handling in getaddrinfo (#259681)
- fix an ABBA deadlock in ld.so (#284171)
- remove sparc{32,64} unwind info from _start and clone

* Mon Aug 27 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-13
- fix personality on x86_64/ppc/ppc64 (#256281)

* Sat Aug 25 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-12
- readd x86_64 gettimeofday stuff, initialize it earlier
- nis_list fix (#254115)
- workaround for bugs in ia64 silly /emul/ia32-linux hack (#253961)
- misc fixes (BZ#3924, BZ#4566, BZ#4582, BZ#4588, BZ#4726, BZ#4946,
  BZ#4905, BZ#4814, BZ#4925, BZ#4936, BZ#4896, BZ#4937, BZ#3842,
  BZ#4554, BZ#4557, BZ#4938)

* Fri Aug 17 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-11
- remove __strtold_internal and __wcstold_internal from ppc*/s390*/sparc*
  *-ldbl.h headers
- temporarily backout x86_64 gettimeofday.S changes (#252453)
- some further sparc, sparc64 and alpha fixes

* Wed Aug 15 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-10
- don't open /etc/ld.so.{cache,preload} with O_NOATIME (#252146)
- s390{,x}, alpha and sparc fixes
- sparcv9 is no longer an aux arch, as we expect
  to not build sparc.rpm glibc any longer, only sparcv9.rpm,
  sparc64.rpm and new two aux arches sparcv9v.rpm and sparc64v.rpm

* Tue Aug 14 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-9
- private futex even for mutexes and condvars
- some further O_CLOEXEC changes
- use vDSO on x86_64 if available
- ia64 build fixes (#251983)

* Fri Aug 10 2007 Roland McGrath <roland@redhat.com> 2.6.90-8
- update to trunk
  - fix missing strtold_l export on ppc64

* Thu Aug  9 2007 Roland McGrath <roland@redhat.com> 2.6.90-6
- update to trunk
  - fix local PLT regressions
- spec file revamp for new find-debuginfo.sh

* Sun Aug  5 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-4
- fix librt.so and librtkaio.so on ppc32, so that it is not using
  bss PLT

* Sat Aug  4 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-3
- fix open{,at}{,64} macro for -pedantic (#250897)
- add transliteration for l with stroke (#250492)
- fix strtod ("-0", NULL)
- update License tag

* Wed Aug  1 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-2
- make aux-cache purely optional performance optimization in ldconfig,
  don't issue any errors if it can't be created (#250430)
- remove override_headers hack, BuildRequire >= 2.6.22 kernel-headers
  and rely on its content

* Tue Jul 31 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-1
- update to trunk
  - private futex optimizations
  - open{,at}{,64} argument checking
- ldconfig speedups

* Sun Jul  8 2007 Jakub Jelinek <jakub@redhat.com> 2.6-4
- filter <built-in> pseudo-files from debuginfo source lists (#245714)
- fix sscanf when errno is EINTR before the call (BZ#4745)
- save/restore errno around reading /etc/default/nss (BZ#4702)
- fix LD_HWCAP_MASK handling
- disable workaround for #210748, instead backport
  ld.so locking fixes from the trunk (#235026)
- new x86_64 memcpy
- don't write uninitialized padding bytes to nscd socket
- fix dl{,v}sym, dl_iterate_phdr and dlopen if some library is
  mapped into ld.so's inter-segment hole on x86_64 (#245035, #244545)
- fix LD_AUDIT=a:b program (#180432)
- don't crash on pseudo-zero long double values passed to
  *printf on i?86/x86_64/ia64 (BZ#4586)
- fix *printf %%La and strtold with some hexadecimal floating point
  constants on ppc/ppc64
- fix nextafterl on ppc/ppc64
- fix sem_timedwait on i?86 and x86_64

* Thu May 24 2007 Jakub Jelinek <jakub@redhat.com> 2.6-3
- don't use %%config(missingok) for locale-archive.tmpl,
  instead of removing it altogether truncate it to zero
  size (#240697)
- add a workaround for #210748

* Mon May 21 2007 Jakub Jelinek <jakub@redhat.com> 2.6-2
- restore malloc_set_state backwards compatibility (#239344)
- fix epoll_pwait (BZ#4525)
- fix printf with unknown format spec or positional arguments
  and large width and/or precision (BZ#4514)
- robust mutexes fix (BZ#4512)

* Tue May 15 2007 Roland McGrath <roland@redhat.com> 2.6-1
- glibc 2.6 release

* Fri May 11 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-24
- utimensat, futimens and lutimes support

* Thu May 10 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-23
- use madvise MADV_DONTNEED in malloc
- fix ia64 feraiseexcept
- fix s390{,x} feholdexcept (BZ#3427)
- ppc fenv fixes
- make fdatasync a cancellation point (BZ#4465)
- fix *printf for huge precisions with wide char code and multi-byte
  strings
- fix dladdr (#232224, BZ#4131)

* Fri May  4 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-22
- add transliteration for <U2044> (BZ#3213)
- fix *scanf with %%f on hexadecimal floats without exponent (BZ#4342)
- fix *printf with very large precisions for %%s (#238406, BZ#4438)
- fix inet_ntop size checking for AF_INET (BZ#4439)
- for *printf %%e avoid 1.000e-00, for exponent 0 always use + sign (#238431)
- fix a regression introduced in #223467 changes
- gethostby*_r alignment fixes (BZ#4381)
- fix ifaddrs error handling

* Mon Apr 16 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-21
- don't include individual locale files in glibc-common,
  rather include prepared locale-archive template and let
  build-locale-archive create locale-archive from the template
  and any user supplied /usr/lib/locale/*_* directories,
  then unlink the locale-archive template - this should save
  > 80MB of glibc-common occupied disk space
- fix _XOPEN_VERSION (BZ#4364)
- fix printf with %%g and values tiny bit smaller than 1.e-4 (#235864,
  BZ#4362)
- fix NIS+ __nisfind_server (#235229)

* Sat Mar 31 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-20
- assorted NIS+ speedups (#223467)
- fix HAVE_LIBCAP configure detection (#178934)
- remove %%{_prefix}/sbin/rpcinfo from glibc-common (#228894)
- nexttoward*/nextafter* fixes (BZ#3306)
- feholdexcept/feupdateenv fixes (BZ#3427)
- speed up fnmatch with two or more * in the pattern

* Sat Mar 17 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-19
- fix power6 libm compat symbols on ppc32 (#232633)
- fix child refcntr in NPTL fork (#230198)
- fix ifaddrs with many net devices on > 4KB page size arches (#230151)
- fix pthread_mutex_timedlock on x86_64 (#228103)
- various fixes (BZ#3919, BZ#4101, BZ#4130, BZ#4181, BZ#4069, BZ#3458)

* Wed Feb 21 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-18
- fix nftw with FTW_CHDIR on / (BZ#4076)
- nscd fixes (BZ#4074)
- fix fmod{,f,l} on i?86 (BZ#3325)
- support localized digits for fp values in *scanf (BZ#2211)
- namespaces fixes (BZ#2633)
- fix euidaccess (BZ#3842)
- glob fixes (BZ#3996)
- assorted locale data fixes (BZ#1430, BZ#672, BZ#58, BZ#3156,
  BZ#2692, BZ#2648, BZ#3363, BZ#3334, BZ#3326, BZ#3322, BZ#3995,
  BZ#3885, BZ#3884, BZ#3851)

* Sun Feb 11 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-17
- RFC2671 support in resolver (#205842)
- fix strptime (BZ#3944)
- fix regcomp with REG_NEWLINE (BZ#3957)
- fix pthread_mutex_timedlock on x86_64 (#228103)

* Fri Feb  2 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-16
- add strerror_l
- fix application crashes when doing NSS lookups through nscd
  mmapped databases and nscd decides to start garbage collection
  during the lookups (#219145, #225315)
- fix %%0lld printing of 0LL on 32-bit architectures (BZ#3902)
- ignore errors from install-info in glibc-devel scriptlets
  (#223691)

* Wed Jan 17 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-15
- fix NIS getservbyname when proto is NULL
- fix nss_compat +group handling (#220658)
- cache services in nscd
- fix double free in fts_close (#222089)
- fix vfork+execvp memory leak (#221187)
- soft-fp fixes (BZ#2749)
- further strtod fixes (BZ#3855)
- make sure pthread_kill doesn't return EINVAL even if
  the target thread exits in between pthread_kill ESRCH check
  and the actual tgkill syscall (#220420)
- fix ABBA deadlock possibility in ld.so scope locking code

* Tue Dec 19 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-14
- fix {j,m}rand48{,_r} on 64-bit arches (BZ#3747)
- handle power6x AT_PLATFORM (#216970)
- fix a race condition in getXXbyYY_r (#219145)
- fix tst-pselect testcase

* Thu Dec 14 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-13
- fix setcontext on ppc32 (#219107)
- fix wide stdio after setvbuf (#217064, BZ#2337)
- handle relatime mount option in statvfs
- revert i?86/x86_64 clone CFI temporarily

* Sun Dec 10 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-12
- fix hasmntopt (#218802)
- fix setusershell and getusershell (#218782)
- strtod fixes (BZ#3664, BZ#3673, BZ#3674)
- fix memusage with realloc (x, 0)

* Tue Dec  5 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-11
- allow suid apps to setenv NIS_PATH and influence through that
  nis_list and nis_lookup (#209155)
- fix ttyname and ttyname_r with invalid file descriptor (#218276)
- cs_CZ LC_TIME fixes (#218438)
- fix build with 2.6.19+ headers (#217723)

* Fri Dec  1 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-10
- fix x86-64 restore_rt unwind info

* Thu Nov 30 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-9
- fix last svc_run change (#217850)
- on ppc64 build __libc_start_main without unwind info,
  as it breaks MD_FROB_UPDATE_CONTEXT (#217729, #217775; in the
  future that could be fixable just by providing .cfi_undefined r2
  in __libc_start_main instead)
- add unwind info for x86-64 restore_rt signal return landing pad
  (#217087)
- add power6x subdir to /%%{_lib}/ and /%%{_lib}/rtkaio/,
  link all libs from ../power6/* into them

* Tue Nov 28 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-8
- fix svc_run (#216834, BZ#3559)
- add -fasynchronous-unwind-tables to CFLAGS (#216518)
- make sure there is consistent timestamp for /etc/ld.so.conf,
  /etc/localtime and /etc/rpc between multilib glibc rpms

* Mon Nov 20 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-7
- handle IPv6 addresses in /etc/hosts that are mappable to
  IPv4 addresses in IPv4 host lookups (#215283)
- fix :include: /etc/alias handling (#215572)
- handle new tzdata format to cope with year > 2037 transitions
  on 64-bit architectures

* Fri Nov 10 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-6
- fix strxfrm fix
- fix i?86 floor and ceil inlines (BZ#3451)

* Thu Nov  9 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-5
- fix sysconf (_SC_LEVEL{2,3}_CACHE_SIZE) on Intel Core Duo
  CPUs
- fix libthread_db.so on TLS_DTV_AT_TP architectures
- fix --inhibit-rpath (#214569)
- fix _r_debug content when prelinked ld.so executes
  a program as its argument
- fix strxfrm
- powerpc-cpu add-on updates

* Fri Nov  3 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-4
- fix atexit backwards compatibility (#213388)
- add mai_IN locale (#213415)
- remove bogus %%{_libdir}/librt.so.1 symlink (#213555)
- fix memusage (#213656)
- change libc.info category (#209493)

* Sun Oct 29 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-3
- fix suid/sgid binaries on i?86/x86_64 (#212723)

* Fri Oct 27 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-2
- fix ia64 build
- don't call _dl_close outside of dl_load_lock critical section
  if dlopen failed (BZ#3426)
- add rtld scope locking (#211133)

* Wed Oct 25 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-1
- fix i?86 6 argument syscalls (e.g. splice)
- fix rtld minimal realloc (BZ#3352)
- fix RFC3484 getaddrinfo sorting according to rules 4 and 7 (BZ#3369)
- fix xdrmem_setpos (#211452)
- bump __GLIBC_MINOR__
- increase PTHREAD_STACK_MIN on ppc{,64} to 128K to allow
  64K pagesize kernels (#209877)
- speed up initgroups on NIS+ (#208203)

* Mon Oct  2 2006 Jakub Jelinek <jakub@redhat.com> 2.5-2
- fix nscd database growing (#207928)
- bypass prelinking when LD_DYNAMIC_WEAK=1 is in the environment

* Fri Sep 29 2006 Jakub Jelinek <jakub@redhat.com> 2.5-1
- glibc 2.5 release

* Wed Sep 27 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-36
- rebuilt with gcc-4.1.1-26 to fix unwind info

* Mon Sep 25 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-35
- fix glob with large number of matches (BZ#3253)
- fix fchownat on kernels that don't support that syscall (BZ#3252)
- fix lrintl on s390{,64}

* Sat Sep 23 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-34
- fix ppc{32,64} longjmp (BZ#3225)
- fix user visible spelling errors (BZ#3137)
- fix l{,l}rint{,f,l} around zero (BZ#2592)
- avoid stack trampoline in s390{,x} makecontext

* Tue Sep 19 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-33
- fix dlclose (#206639)
- don't load platform optimized libraries if kernel doesn't set
  AT_PLATFORM
- fix ppc{32,64} libSegFault.so
- use -mtune=generic even for glibc-devel.i386 (#206437)
- fix /%%{_lib}/librt.so.1 symlink

* Fri Sep 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-32
- on ppc* use just AT_PLATFORM and altivec AT_HWCAP bit for library selection
- fix lrintl and lroundl on ppc{,64}
- use hidden visibility on fstatat{,64} and mknodat in libc_nonshared.a

* Sun Sep 10 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-31
- fix pthread_cond_{,timed}wait cancellation (BZ#3123)
- fix lrint on ppc32 (BZ#3155)
- fix malloc allocating more than half of address space (BZ#2775)
- fix mktime on 32-bit arches a few years after 2038 (BZ#2821)

* Thu Sep  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-30
- add librtkaio, to use it add /%%{lib}/rtkaio to your
  LD_LIBRARY_PATH or /etc/ld.so.conf
- fix or_IN February name (#204730)
- fix pthread_create called from cancellation handlers (BZ#3124)
- fix regex case insensitive searches with characters where upper
  and lower case multibyte representations have different length
  (e.g. I and dotless i, #202991)

* Tue Sep  5 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-29
- randomize resolver query ids before use instead after use (#205113)
- fix resolver symver checking with DT_GNU_HASH (#204909)
- put .hash section in glibc libraries at the end of RO segment
  when .gnu.hash is present

* Thu Aug 31 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-28
- another malloc doubly linked list corruption problem fix (#204653)

* Thu Aug 31 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-27
- allow $LIB and $PLATFORM in dlopen parameters even in suid/sgid (#204399)
- handle $LIB/$PLATFORM in LD_LIBRARY_PATH
- fix splice prototype (#204530)

* Mon Aug 28 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-26
- real fix for the doubly linked list corruption problem
- try harder in realloc to allocate memory (BZ#2684)
- fix getnameinfo error reporting (#204122)
- make localedef more robust on invalid input (#203728)

* Fri Aug 25 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-25
- temporarily back out code to limit number of unsorted block
  sort iterations (#203735, #204027)
- handle PLT symbols in dladdr properly (BZ#2683)
- avoid malloc infinite looping for allocations larger than
  the system can allocate (#203915)

* Tue Aug 22 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-23
- malloc fixes, especially for 32-bit arches (#202309)
- further *_IN locale fixes (#200230)
- fix get{serv,rpc}ent{,_r} if NIS map is empty (#203237)
- fix /usr/bin/iconv (#203400)

* Fri Aug 18 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-22
- rebuilt with latest binutils to pick up 64K -z commonpagesize
  on ppc/ppc64 (#203001)

* Tue Aug 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-21
- if some test gets stuck, kill the tee process after make check
  finishes
- build with -mtune=generic on i686 and x86_64

* Tue Aug 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-20
- PTHREAD_PRIO_PROTECT support
- fix errno if nice() fails (#201826)

* Thu Aug 10 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-19
- adaptive malloc brk/mmap threshold
- fix fchownat to use kernel syscall (if available) on many arches (#201870)
- only define O_DIRECT with -D_GNU_SOURCE on ia64 to match all
  other arches (#201748)

* Mon Aug  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-18
- NIS+ fixes
- fix memusage and xtrace scripts (#200736)
- redirect /sbin/service sshd condrestart std{out,err} to /dev/null
  when executed from glibc_post_upgrade

* Wed Aug  2 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-17
- typo fix for the dladdr patch
- build i?86 glibc with -mno-tls-direct-seg-refs (#200469)

* Wed Aug  2 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-16
- fix dladdr on binaries/libraries with only DT_GNU_HASH and no
  DT_HASH (#200635)
- fix early timeout of initgroups data in nscd (#173019)
- add am/pm display to es_PE and es_NI locales (#167101)
- fix nss_compat failures when nis/nis+ unavailable (#192072)

* Mon Jul 31 2006 Roland McGrath <roland@redhat.com> 2.4.90-15
- fix missing destructor calls in dlclose (#197932)
- enable transliteration support in all locales (#196713)
- disallow RTLD_GLOBAL flag for dlmopen in secondary namespaces (#197462)
- PI mutex support

* Mon Jul 10 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-13
- DT_GNU_HASH support

* Fri Jun 30 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-12
- buildrequire gettext
- enable fstatat64/newfstatat syscalls even on ppc*/s390*/ia64 (#196494)
- fix out of memory behavior in gettext (#194321)
- fix regex on multi-byte non-UTF-8 charsets (#193873)
- minor NIS+ fixes (#190803)
- don't use cancellable calls in posix_spawn* and only set{u,g}id
  current thread if requested (#193631)

* Wed May 31 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-11
- don't exit from nscd -i <database> before the database is
  actually invalidated, add locking to prune_cache (#191464)
- build glibc-devel.i386 static libraries with
  -mno-tls-direct-seg-refs -DNO_TLS_DIRECT_SEG_REFS
- RFC3542 support (advanced API for IPv6; #191001, BZ##2693)

* Wed May 24 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-10
- on i686 make glibc owner of /lib/i686 directory (#192597)
- search parent NIS+ domains (#190803)

* Sun May 21 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-9
- update from CVS
  - big NIS+ changes

* Fri May 19 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-8
- update from CVS
  - fix nss_compat when SETENT_BATCH_READ=TRUE is in /etc/default/nss
  - fix RFC3484 precedence table for site-local and ULA addresses (#188364)
  - fix a sunrpc memory leak

* Thu May 11 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-7
- update from CVS
  - fix tcgetattr (#177965)
  - fix <sys/queue.h> (#191264)

* Fri May  5 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-6
- update from CVS
- rebuilt using fixed rpm

* Fri May  5 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-5
- update from CVS
  - some NIS+ fixes
  - allow overriding rfc3484 address sorting tables for getaddrinfo
    through /etc/gai.conf (sample config file included in %%doc directory)

* Mon May  1 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-4
- update from CVS
  - SETENT_BATCH_READ /etc/default/nss option for speeding up
    some usages of NIS+ (#188246)
  - move debug state change notification (#179208)
  - fix ldd script if one of the dynamic linkers is not installed (#190259)

* Thu Apr 27 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-3
- update from CVS
  - fix a typo in nscd.conf (#190085)
  - fix handling of SIGHUP in nscd when some caches are disabled (#189978)
  - make nscd paranoia mode working with non-root server-user (#189779)

* Wed Apr 26 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-2
- update from CVS
  - fix getaddrinfo (#190002)
  - add auto-propagate nscd.conf options (#177154)
  - fix nscd auditing (#169148)

* Tue Apr 25 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-1
- update from CVS

* Mon Apr 24 2006 Jakub Jelinek <jakub@redhat.com> 2.4-6
- update from CVS
  - NIS+ fixes
  - don't segfault on too large argp key values (#189545)
  - getaddrinfo fixes for RFC3484 (#188364)

* Tue Mar 28 2006 Jakub Jelinek <jakub@redhat.com> 2.4-5
- update from CVS
  - pshared robust mutex support
  - fix btowc and bwtoc in C++ (#186410)
  - fix NIS+ (#186592)
  - don't declare __wcsto*l_internal for non-GCC or if not -O1+ (#185667)
- don't mention nscd failures on 2.0 kernels (#185335)

* Tue Mar  7 2006 Roland McGrath <roland@redhat.com> 2.4-4
- back up %%{ix86} gdb conflicts to < 6.3.0.0-1.111

* Tue Mar  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4-3
- really fix rintl on ppc64

* Tue Mar  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4-2
- accurate unwind info for lowlevellock.h stubs on %%{ix86}
- fix ppc/ppc64 ceill, floorl, rintl, roundl and truncl (BZ#2423)

* Mon Mar  6 2006 Jakub Jelinek <jakub@redhat.com> 2.4-1
- update from CVS
  - glibc 2.4 release

* Mon Mar  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.91-2
- update from CVS
  - fix sYSMALLOc for MALLOC_ALIGNMENT > 2 * SIZE_SZ (#183895)
  - revert ppc32 malloc alignment patch, it breaks malloc_set_state
    and needs some further thoughts and time (#183894)
- provide accurate unwind info for lowlevellock.h stubs on x86_64

* Thu Mar  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.91-1
- update from CVS
  - fixes for various arches
- ensure malloc returns pointers aligned to at least
  MIN (2 * sizeof (size_t), __alignof__ (long double))
  (only on ppc32 this has not been the case lately with addition
   of 128-bit long double, #182742)

* Wed Mar  1 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-39
- update from CVS

* Fri Feb 17 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-38
- update from CVS
  - robust mutexes rewrite

* Mon Feb 13 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-37
- update from CVS
  - *at fixes
  - unshare syscall wrapper

* Sat Feb  4 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-36
- update from CVS
  - fix frequency setting for ITIMER_PROF (#179938, BZ#2268)
  - fix powerpc inline fegetround ()
  - fix nptl_db (#179946)

* Fri Feb  3 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-35
- update from CVS
  - handle futimesat (fd, NULL, tvp) as futimes (fd, tvp)
- fix <stdlib.h> q{e,f,g}cvt{,_r} for -mlong-double-64

* Thu Feb  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-34
- fix <math.h> with C++ and -mlong-double-64 (#179742)
- add nexttowardl redirect for -mlong-double-64

* Thu Feb  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-33
- update from CVS
  - long double support fixes

* Wed Feb  1 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-32
- update from CVS
  - 128-bit long double fixes for ppc{,64}, s390{,x} and sparc{,v9},
    alpha 128-bit long double support
- add inotify syscall numbers to the override <asm/unistd.h> headers
  (#179366)

* Mon Jan 30 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-31
- update from CVS
  - 128-bit long double on ppc, ppc64, s390, s390x and sparc{,v9}
- add some new syscall numbers to the override <asm/unistd.h>
  headers

* Mon Jan  9 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-30
- update from CVS
  - <pthread.h> initializer fixes for -std=c{8,9}9 on 32-bit
    arches
- avoid writable .rodata (#177121)

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-29
- update from CVS
  - make pthread_mutex_t an unnamed union again, as it affects
    libstdc++ ABI mangling

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-28
- update from CVS
  - make aio_suspend interruptible by signals (#171968)

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-27
- only rely on d_type in 32-bit getdents on s390 for 2.6.11+

* Wed Jan  4 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-26
- update from CVS
  - for newly linked lio_listio* callers, send per request
    notifications (#170116)
  - fixup nscd -S option removal changes (#176860)
  - remove nonnull attribute from ctermid (#176753)
  - fix PTHREAD_*_INITIALIZER{,_NP} on 64-bit arches
  - SPARC NPTL support for pre-v9 CPUs
- drop support for 2.4.xx and < 2.6.9 kernels

* Mon Jan  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-25
- update from CVS
  - s390{,x} and sparc{,64} pointer mangling fixes
- install a sanitized LinuxThreads <bits/libc-lock.h>

* Mon Jan  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-24
- update from CVS
  - nscd audit changes (#174422)
  - ppc{32,64} vDSO support and ppc32 hp-timing

* Tue Dec 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-23
- update from CVS
  - robust mutexes
- fix transliteration segfaults (#176573, #176583)
- ignore prelink temporaries in ldconfig (#176570)

* Wed Dec 21 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-22
- update from CVS
  - minor fts fixes
- revert broken _Pragma () workaround
- fix ldconfig on bi-arch architectures (#176316)

* Tue Dec 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-21
- update from CVS
  - fix pointer (de)mangling in gconv_cache.c

* Tue Dec 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-20
- update from CVS
  - time ((void *) 1) should segfault, not return -EFAULT (#174856, BZ#1952)
  - fix errlist generation
- update ulps for GCC 4.1 on IA-64

* Mon Dec 19 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-19
- update from CVS
  - sysdeps/generic reorg
  - setjmp/longjmp jump pointer mangling
- rebuilt with GCC 4.1-RH prerelease, worked around broken _Pragma ()
  handling in it
- remove glibc-profile subpackage
- use non-PLT calls for malloc/free/realloc/memalign invocations in
  mtrace and mcheck hooks (#175261)
- setjmp/longjmp jump pointer mangling on ppc{,64}/ia64/s390{,x}

* Sat Nov 19 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-18
- update from CVS
  - change <sys/stat.h> for broken apps that #define const /**/,
    handle non-GCC compilers
  - fix ppc{32,64} strncmp (BZ#1877, #173643, IT#83510)
  - provide shmatt_t typedef in ia64 <sys/shm.h (#173680)
  - support 2nd arg to futimesat being NULL (#173581)

* Wed Nov 16 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-17
- update from CVS
  - fix <sys/stat.h> in C++
  - {fstat,fchown,rename,unlink}at fixes
  - epoll_wait is now a cancellation point

* Tue Nov 15 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-16
- update from CVS
- make sure waitid syscall is used on ppc*/s390*

* Thu Oct 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-15
- update from CVS
  - be permissive in %%n check because of kernel bug #165351 (#171240)
  - don't misalign stack in pthread_once on x86_64 (#170786, IT#81521)
  - many locale fixes

* Mon Oct 10 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-14
- update from CVS
  - fix malloc bug after fork introduced in the last update
  - fix getent hosts IP for IPv4 IPs (#169831)

* Mon Oct  3 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-13
- update from CVS
  - fix setuid etc. hangs if some thread exits during the call (#167766)
  - fix innetgr memory leak (#169051)
  - support > 2GB nscd log files (#168851)
  - too many other changes to list here
- include errno in nscd message if audit_open failed (#169148)

* Mon Sep 12 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-12
- update from CVS
  - netgrp handling fixes (#167728)
  - fix memory leak in setlocale (BZ#1318)
  - fix hwcaps computation
  - several regex portability improvements (#167019)
  - hypotf fix
  - fix *printf return code if underlying write fails (BZ#1146)
  - PPC64 dl{,v}sym fixes for new ABI .opd symbols
- fix calloc with MALLOC_PERTURB_ in environment on 64-bit architectures
  (#166719)
- source /etc/sysconfig/nscd (if it exists) in /etc/rc.d/init.d/nscd
  (#167083)
- add %%triggerin for tzdata to glibc-common, so that tzdata updates
  update /etc/localtime and /var/spool/postfix/etc/localtime if they
  exist (#167787)

* Mon Aug 29 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-11
- FUTEX_WAKE_OP support to speed up pthread_cond_signal

* Wed Aug 24 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-10
- update from CVS
  - fix growing of nscd persistent database (BZ#1204)
  - fix _FORTIFY_SOURCE mbstowcs and wcstombs if destination size
    is known at compile time, but length argument is not

* Mon Aug 22 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-9
- update from CVS
  - fix resolving over TCP (#161181, #165802)
  - on ia64 don't abort on unhandled math function exception codes
    (#165693)

* Mon Aug  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-8
- update from CVS
  - nscd persistent database verifier (#164001)
  - cleanup _FORTIFY_SOURCE bits/*.h headers (#165000)
  - handle EINTR in sigwait properly
- make sure poor man's stack guard randomization keeps first
  byte 0 even on big-endian 32-bit arches
- fix {elf,nptl}/tst-stackguard1
- obsolete linuxthreads-devel in glibc-devel

* Fri Jul 29 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-7
- update from CVS
- do some poor man's stack guard randomization even without
  the costly --enable-stackguard-randomization
- rebuilt with new GCC to make it use -msecure-plt on PPC32

* Mon Jul 25 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-6
- update from CVS
  - fix execvp if PATH is not in environment and the call is going
    to fail (BZ#1125)
  - another bits/wchar2.h fix (#163990)

* Fri Jul 22 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-5
- update from CVS
  - fix stubs.h generation
- don't use _G_va_list in bits/wchar2.h

* Fri Jul 22 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-4
- update from CVS
  - make sure bits/wchar2.h header is installed
  - fix __getgroups_chk return type

* Thu Jul 21 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-3
- update from CVS
  - make sure nscd cmsg buffers aren't misaligned, handle EINTR from
    poll when contacting nscd more gracefully
  - remove malloc attribute from posix_memalign
  - correctly size nscd buffer for grpcache key (#163538)
  - fix atan2f
  - fix error memory leaks
  - some more _FORTIFY_SOURCE protection

* Fri Jul  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-2
- update from CVS
  - ia64 stack protector support
  - handle DNS referral results as server errors (#162625)
  - ctan{,h}{,f,l} fixes (#160759)
  - pass argc, argv and envp also to executable's *ni_array
    functions (BZ#974)
  - add ellipsis to clone prototype (#161593)
  - fix glibc-profile (#162601)
  - nss_compat fixes
- use sysdeps/generic version of <bits/stdio-lock.h> in installed
  headers instead of NPTL version (#162634)

* Mon Jun 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-1
- update from CVS
  - stack protector support
  - fix xdr_{,u_}{longlong_t,hyper} on 64-bit arches (#161583)
- enable @GLIBC_2.4 symbols
- remove linuxthreads

* Mon Jun 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-11
- update from CVS
  - PPC32 -msecure-plt support
  - support classes keyword in /etc/hesiod.conf (#150350)
  - add RLIMIT_NICE and RLIMIT_RTPRIO to <sys/resources.h> (#157049)
  - decrease number of .plt relocations in libc.so
  - use -laudit in nscd (#159217)
  - handle big amounts of networking interfaces in getifaddrs/if_nameindex
    (#159399)
  - fix pa_IN locale's am_pm (#158715, BZ#622)
  - fix debugging of PIEs

* Mon May 30 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-10
- fix LD_ASSUME_KERNEL (since 2.3.5-8 GLRO(dl_osversion)
  has been always overwritten with the version of currently
  running kernel)
- remove linuxthreads man pages other than those covered in
  3p section, as 3p man pages are far better quality and describe
  POSIX behaviour that NPTL implements (#159084)

* Tue May 24 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-9
- update from CVS
  - increase bindresvport's LOWPORT to 512, apparently some
    broken daemons don't think 0 .. 511 ports are reserved

* Mon May 23 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-8
- update from CVS
  - fix kernel version check in ld.so
- fix sendfile{,64} prototypes (BZ#961)
- try more ports in bindresvport if all 600..1023 are
  used, don't use priviledged ports when talking to portmap
  (#141773)

* Fri May 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-7
- update from CVS
  - make regexec thread safe (BZ#934)
- fix statically linked programs on i?86, x86_64, s390* and
  sparc* (#158027)
- fix IBM939 iconv module (BZ#955)

* Wed May  4 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-6
- update from CVS
  - fix cancellation on i?86
  - add call frame information to i?86 assembly

* Tue May  3 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-5
- update from CVS
  - add some more UTF-8 locales (#156115)
- clean up /lib64/tls instead of /lib/tls on x86-64, s390x and
  ppc64 in glibc_post_upgrade (#156656)
- fix posix_fallocate{,64} (#156289)

* Thu Apr 28 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-4
- update from CVS
  - fix nscd cache pruning (#150748)

* Wed Apr 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-3
- update from CVS
  - fix linuxthreads clocks
- put xen libs into the glibc-2*.i686 package instead of a separate one
- fix librt.so symlink in linuxthreads-devel
- do not include linuxthreads-devel on %%{auxarches},
  just on the base architectures

* Wed Apr 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-2
- update from CVS
  - with MALLOC_CHECK_=N N>0 (#153003)
  - fix recursive dlclose (#154641)
  - handle %%z in strptime (#154804)
  - automatically append /%%{_lib}/obsolete/linuxthreads/
    to standard library search path if LD_ASSUME_KERNEL=N N <= 2.4.19
    or for glibc 2.0 binaries (or broken ones that don't use errno/h_errno
    properly).  Warning: all those will stop working when LinuxThreads
    is finally nuked, which is not very far away
  - remove nonnull attribute from acct prototype (BZ#877)
  - kernel CPU clocks support
  - fix *scanf in locales with multi-byte decimal point

* Wed Apr 27 2005 Roland McGrath <roland@redhat.com>
- glibc-xen subpackage for i686

* Fri Apr 15 2005 Roland McGrath <roland@redhat.com> 2.3.5-1
- update from CVS
  - fix execvp regression (BZ#851)
  - ia64 libm updates
  - sparc updates
  - fix initstate{,_r}/strfry (#154504)
  - grok PT_NOTE in vDSO for kernel version and extra hwcap dirs,
    support "hwcap" keyword in ld.so.conf files

* Tue Apr  5 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-21
- update from CVS
  - fix xdr_rmtcall_args on 64-bit arches (#151686)
- fix <pthread.h> and <bits/libc-lock.h> with -std=c89 -fexceptions (#153774)

* Mon Apr  4 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-20
- move LinuxThreads libraries to /%%{_lib}/obsolete/linuxthreads/
  and NPTL libraries to /%%{_lib}.  To run a program against LinuxThreads,
  LD_ASSUME_KERNEL=2.4.xx LD_LIBRARY_PATH=/%%{_lib}/obsolete/linuxthreads/
  is now needed
- bzip2 ChangeLog* files instead of gzipping them

* Sat Apr  2 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-19
- update from CVS
  - fix nextafterl and several other libm routines on ia64
  - fix initgroups (BZ#661)
- kill nptl-devel subpackage, add linuxthreads-devel,
  compile and link by default against NPTL and only with
  -I/usr/include/linuxthreads -L/usr/%%{_lib}/linuxthreads
  against LinuxThreads
- package /usr/lib/debug/%%{_lib}/tls/i{5,6}86 symlinks in
  i386 glibc-debuginfo
- limit number of ChangeLog* files in glibc-common %%doc
  to last 2.5 years of changes only to save space

* Fri Mar 25 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-18
- fix build on 64-bit arches with new GCC

* Thu Mar 24 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-17
- update from CVS
  - fix LD_AUDIT in LinuxThreads ld.so
  - fix calloc with M_PERTURB
  - fix error handling in pthread_create with PTHREAD_EXPLICIT_SCHED
    on ppc*/ia64/alpha/mips (BZ#801)
  - fix a typo in WINDOWS-31J charmap (#151739)
  - fix NIS ypprot_err (#151469)

* Sun Mar 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-16
- fix pread with -D_FILE_OFFSET_BITS=64 (#151573)

* Sat Mar 19 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-15
- update from CVS
  - better fix for the dlclose bug (#145810, #150414)
  - fix regex crash on case insensitive search in zh_CN locale
    (#151215)
  - fix malloc_trim (BZ#779)
  - with -D_FORTIFY_SOURCE=*, avoid defining read and a bunch of others
    as function-like macros, there are too many broken programs
    out there
- add %%dir %%{_prefix}/%%{_lib}/gconv to glibc's file list (#151372)

* Sun Mar  6 2005 Roland McGrath <roland@redhat.com> 2.3.4-14
- fix bits/socket2.h macro typos

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-12
- fix tst-chk{2,3}
- fix up AS_NEEDED directive in /usr/%%{_lib}/libc.so
- BuildReq binutils >= 2.15.94.0.2-1 for AS_NEEDED, in
  glibc-devel Conflict with binutils < 2.15.94.0.2-1

* Thu Mar  3 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-11
- update from CVS
  - fix execvp (#149290)
  - fix dlclose (#145810)
  - clear padding in gconv-modules.cache (#146614, BZ#776)
- rebuilt with GCC4
- changed __GLIBC_MINOR__ for now back to 3
- back out the newly added GLIBC_2.4 *_chk routines, instead
  do the checking in macros

* Sat Feb 12 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-10
- hopefully fix interaction with prelink (#147655)

* Fri Feb 11 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-9
- update from CVS
  - bi-arch <gnu/stubs.h> (BZ#715)

* Fri Feb 11 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-8
- update from CVS
  - bi-arch <gnu/lib-names.h> (BZ#632)
  - fix libdl on s390 and maybe other platforms
  - fix initstate{,_r} (BZ#710)
  - fix <gnu/stubs.h> generation (BZ#157)
- define CMSPAR in bits/termios.h (#147533)

* Tue Feb  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-7
- update from CVS
  - fix TLS handling in linuxthreads

* Tue Feb  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-6
- update from CVS
  - ld.so auditing
  - fix segfault if chrooted app attempts to dlopen a library
    and no standard library directory exists at all (#147067, #144303)
  - fix initgroups when nscd is running, but has group caching disabled
    (#146588)
  - fix pthread_key_{create,destroy} in LinuxThreads when pthread_create
    has not been called yet (#146710)
  - fix ppc64 swapcontext and setcontext (#146736, BZ#700)
  - service nscd cosmetic fixes (#146776)
  - fix IA-32 and x86-64 stack alignment in DSO constructors (#145689)
  - fix zdump -v segfaults on x86-64 (#146210)
  - avoid calling sigaction (SIGPIPE, ...) inside syslog (#146021, IT#56686)
  - fix errno values for futimes (BZ#633)
  - unconditionally include <features.h> in malloc.h (BZ#650)
  - change regex \B handling to match old GNU regex as well as perl/grep's dfa
    (from empty string inside of word to empty string not at a word boundary,
     BZ#693)
  - slightly optimize i686 TLS accesses, use direct TLS %%gs access in sem_*
    and allow building -mno-tls-direct-seg-refs glibc that is free of direct TLS
    %%gs access with negative offsets
  - fix addseverity
  - fix fmemopen
  - fix rewinddir
  - increase svc{tcp,unix}_create listen backlog

* Thu Jan  6 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-5
- update from CVS
  - add some warn_unused_result marking
  - make ftruncate available even for just -D_POSIX_C_SOURCE=200112L
    (BZ#640)

* Thu Jan  6 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-4
- update from CVS
  - fix IA-32 stack alignment for LinuxThreads thread functions
    and functions passed to clone(2) directly
  - fix ecvt{,_r} on denormals (#143279)
  - fix __tls_get_addr typo
  - fix rounding in IA-64 alarm (#143710)
  - don't reinitialize __environ in __libc_start_main, so that
    effects of setenv/putenv done in DSO initializers are preserved
    (#144037, IT#57403)
  - fix fmemopen
  - fix vDSO l_map_end and l_text_end values
  - IA64 libm update (#142494)
- fix ppc rint/ceil etc. (BZ#602)

* Tue Dec 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.4-3
- rebuilt

* Mon Dec 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.4-2
- work around rpm bug some more, this time by copying
  iconvconfig to iconvconfig.%%{_target_cpu}.

* Mon Dec 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.4-1
- update from CVS
  - glibc 2.3.4 release
  - add -o and --nostdlib options to iconvconfig
- if /sbin/ldconfig doesn't exist when running
  glibc_post_upgrade.%%{_target_cpu}, just don't attempt to run it.
  This can happen during first install of bi-arch glibc and the
  other arch glibc's %%post wil run /sbin/ldconfig (#143326)
- use -o and --nostdlib options to create all needed
  gconv-modules.cache files on bi-arch setups

* Sun Dec 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-99
- rebuilt

* Sat Dec 18 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-98
- add .%%{_target_cpu} to glibc_post_upgrade, only run telinit u
  if /sbin/init is the same ELF class and machine as
  glibc_post_upgrade.%%{_target_cpu} and similarly with
  condrestarting sshd (#143046)

* Fri Dec 17 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-97
- update from CVS
  - fix ppc64 getcontext and swapcontext (BZ#610)
  - sparc/sparc64 fixes

* Wed Dec 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-96
- update from CVS
  - fix i686 __USE_STRING_INLINES strncat
  - make sure ppc/ppc64 maintain correct stack alignment
    across clone

* Wed Dec 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-95
- export nis_domain_of_r from libnsl.so again which was
  unintentionally lost

* Wed Dec 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-93
- update from CVS
  - ppc/ppc64 clone without CLONE_THREAD getpid () adjustement
  - fix MALLOC_CHECK_={1,2,3} for non-contiguous main arena
    (BZ#457)
  - fix sysconf (_POSIX_V6_*) for other ABI environments in
    bi-arch setups
- s390/s390x clone without CLONE_THREAD getpid () adjustement

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-92
- update from CVS
- fix %%{_prefix}/libexec/getconf filenames generation

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-91
- update from CVS
  - double buffer size in getXXbyYY or getXXent on ERANGE
    instead of adding BUFLEN (#142617)
  - avoid busy loop in malloc if another thread is doing fork
    (#142214)
  - some more realloc corruption checks
  - fix getconf _POSIX_V6_WIDTH_RESTRICTED_ENVS output,
    tweak %%{_prefix}/libexec/getconf/ filenames

* Fri Dec 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-90
- update from CVS
  - regex speedups
  - use | cat in ldd if running under bash3+ to allow running
    it on binaries that are not through SELinux allowed to access
    console or tty
- add __NR_waitid defines for alpha and ia64

* Wed Dec  8 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-89
- update from CVS
  - fix clone2 on ia64
  - avoid tst-timer5 failing with linuxthreads implementation
- if __libc_enable_secure, disallow mode != normal
- change ldd script to imply -r when -u is used, properly
  propagate return value and handle suid binaries

* Tue Dec  7 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-88
- update from CVS
  - disregard LD_SHOW_AUXV and LD_DYNAMIC_WEAK if __libc_enable_secure
  - disregard LD_DEBUG if __libc_enable_secure in normal mode
    if /suid-debug doesn't exist
  - fix fseekpos after ungetc
  - avoid reading bytes before start of buffers in regex's
    check_dst_limits_calc_pos_1 (#142060)
  - make getpid () working with clone/clone2 without CLONE_THREAD
    (so far on i386/x86_64/ia64 only)
- move %%{_prefix}/libexec/getconf/* to glibc from glibc-common
- make %%{_prefix}/libexec/getconf directory owned by glibc package

* Fri Dec  3 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-87
- update from CVS
  - build libpthread_nonshared.a objects with -fPIC on s390/s390x
  - fix mktime with < 0 or > 59 tm_sec on entry
  - remove nonnull attribute for realpath
  - add $(make-target-directory) for errlist-compat.c rule
    (hopefully fix #141404)
- add testcase for ungetc bug
- define _POSIX_{,THREAD_}CPUTIME to 0 on all Linux arches

* Tue Nov 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-86
- update from CVS
  - some posix_opt.h fixes
- fix strtold use of unitialized memory (#141000)
- some more bugfixes for bugs detected by valgrind
- rebuilt with GCC >= 3.4.3-5 to avoid packed stack layout
  on s390{,x} (#139678)

* Fri Nov 26 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-85
- update from CVS
  - support -v specification in getconf
  - fix sysconf (_SC_LFS64_CFLAGS) etc.
  - avoid thread stack aliasing issues on EM64T (#140803)
- move %%{_prefix}/include/nptl headers from nptl-devel
  to glibc-headers, so that even NPTL specific programs
  can be built bi-arch without problems

* Wed Nov 24 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-84
- update from CVS
  - fix memory leak in getaddrinfo if using nscd (#139559)
  - handle large lines in /etc/hosts and /etc/networks
    (#140378)
  - add nonnull attributes to selected dirent.h and dlfcn.h
    functions

* Sun Nov 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-83
- update from CVS
  - add deprecated and/or nonnull attribute to some signal.h
    functions
  - speed up tzset () by only using stat instead of open/fstat
    when calling tzset for the second and following time if
    /etc/localtime has not changed
- fix tgamma (BZ #552)

* Sat Nov 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-82
- update from CVS
  - some malloc () checking
  - libpthread.a object dependency cleanups (#115157)
  - <bits/socket.h> fix for -std=c89 -pedantic-errors (#140132)

* Fri Nov 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-81
- don't use chunksize in <= 2 * SIZE_SZ free () checks

* Fri Nov 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-80
- update from CVS
  - with -D_FORTIFY_SOURCE=2, prevent missing %%N$ formats
  - for -D_FORTIFY_SOURCE=2 and %%n in writable format string,
    issue special error message instead of using the buffer overflow
    detected one
  - speedup regex searching with REG_NOSUB, add RE_NO_SUB,
    speedup searching with nested subexps (BZ #544)
  - block SIGCANCEL in NPTL timer_* helper thread
- further free () checking

* Tue Nov 16 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-79
- update from CVS
- fix free () checking
- move /etc/default/nss into glibc-common (hopefully fix #132392)

* Mon Nov 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-78
- update from CVS
  - fix LD_DEBUG=statistics
  - issue error message before aborting in __chk_fail ()
- some more free () checking

* Fri Nov 12 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-77
- update from CVS
  - speedup regex on palindromes (BZ #429)
  - fix NPTL set{,e,re,res}[ug]id, so that even if making process
    less priviledged all threads change their credentials successfully

* Wed Nov 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-76
- update from CVS
  - fix regcomp crash (#138439)
  - fix ftell{,o,o64} (#137885)
  - robustification of nscd to cope with corrupt databases (#137140)
  - fix NPTL with pthread_exit immediately after pthread_create (BZ #530)
  - some regex optimizations

* Tue Nov  2 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-75
- update from CVS
  - mktime cleanups (BZ #487, #473)
  - unique comments in free(3) check error messages
- adjust some x86_64 headers for -m32 (#129712)
- object size checking support even with GCC-3.4.2-RH >= 3.4.2-8

* Wed Oct 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-74
- fix <netinet/udp.h> header
- fix globfree (#137176)
- fix exiting if there are dlmopened libraries in namespaces
  other than main one not closed yet
- export again _res_opcodes and __p_{class,type}_syms from
  libresolv.so that were lost in -69

* Thu Oct 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-73
- remove setaltroot and key{_add,_request,ctl} also from Versions
- back out _sys_errlist changes

* Thu Oct 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-72
- back out setaltroot and key{_add,_request,ctl} addition
- fix severe x86-64 symbol versioning regressions that breaks
  e.g. java binaries

* Wed Oct 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-71
- update from CVS
  - fix minor catchsegv temp file handling vulnerability
    (CAN-2004-0968, #136319)
  - add 4 new errno codes
  - setaltroot, key{_add,_request,ctl} syscalls on some arches
  - export _dl_debug_state@GLIBC_PRIVATE from ld.so again for
    gdb purpose
  - use inet_pton to decide what is address and what is hostname
    in getent (#135422)
  - change dladdr/dladdr1, so that dli_saddr is the same kind
    of value as dlsym/dlvsym return (makes difference on ia64/hppa only)
  - fix catchsegv script so that it works with both 32-bit and 64-bit
    programs on multi-arch platforms

* Tue Oct 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-70
- update from CVS
- require newer selinux-policy (#135978)
- add %%dir for /var/run/nscd and /var/db/nscd and %%ghost
  files in it
- conflict with gcc4 4.0.0-0.6 and earlier (needs __builtin_object_size)

* Mon Oct 18 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-69
- update from CVS
  - object size checking support (-D_FORTIFY_SOURCE={1,2})

* Thu Oct 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-68
- update from CVS
  - support for namespaces in the dynamic linker
  - fix dlclose (BZ #77)
  - libSegFault.so uses now backtrace() to work on IA-64, x86-64
    and s390 (#130254)

* Tue Oct 12 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-67
- update from CVS
  - use non-blocking sockets in resolver (#135234)
  - reset pd->res options on thread exit, so that threads
    reusing cached stacks get resolver state properly initialized
    (BZ #434)

* Wed Oct  6 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-66
- update from CVS
- avoid using perl in the spec file, buildrequire sed >= 3.95
  (#127671)
- export TIMEOUTFACTOR=16
- fix _JMPBUF_CFA_UNWINDS_ADJ on s390{,x}

* Tue Oct  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-65
- update from CVS
  - define _POSIX_THREAD_PROCESS_SHARED and _POSIX_CLOCK_SELECTION
    to -1 in LinuxThreads
  - define _POSIX_CPUTIME and _POSIX_THREAD_CPUTIME to 0
    on i?86/ia64 and make sure sysconf (_SC_{,THREAD_}CPUTIME)
    returns correct value
- if _POSIX_CLOCK_SELECTION == -1 in nscd, still try
  sysconf (_SC_CLOCK_SELECTION) and if it returns true,
  dlopen libpthread.so and dlsym pthread_condattr_setclock
- build nscd with -z relro and -z now

* Mon Oct  4 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-64
- update from CVS
  - stop using __builtin_expect in assert and assert_perror
    (#127606)
  - try to avoid too much VA fragmentation with malloc
    on flexmap layout (#118574)
  - nscd robustification
  - change valloc to use debugging hooks (#134385)
- make glibc_post_upgrade more verbose on errors (Fergal Daly,
  #125700)

* Fri Oct  1 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-63
- update from CVS
  - fix __nscd_getgrouplist
  - fix a typo in x86_64 pthread_mutex_timedwait fix

* Fri Oct  1 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-62
- update from CVS
  - fix NPTL pthread_mutex_timedwait on i386/x86_64 (BZ #417)

* Thu Sep 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-61
- update from CVS
  - some nscd fixes (#134193)
  - cache initgroups in nscd (#132850)
  - reread /etc/localtime in tzset () even if just mtime changed
    (#133481)
  - fix glob (#126460)
  - another get_myaddress fix

* Wed Sep 29 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-60
- update from CVS
  - fix get_myaddress (#133982)
  - remove nonnull attribute from second utime argument (#133866)
  - handle SIGSETXID the same way as SIGCANCEL in
    sigaction/pthread_kill/sigwait/sigwaitinfo etc.
  - add __extension__ to long long types in NPTL <bits/pthreadtypes.h>

* Mon Sep 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-59
- update from CVS
  - fix BZ #151, #362, #381, #407
  - fdim fix for +inf/+inf (BZ #376)

* Sun Sep 26 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-58
- update from CVS
  - vasprintf fix (BZ #346)
  - gettext locking (BZ #322)
- change linuxthreads useldt.h inclusion login again, the last
  one failed all linuxthreads FLOATING_STACKS tests

* Sat Sep 25 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-57
- update from CVS
  - fix setuid in LD_ASSUME_KERNEL=2.2.5 libc (#133558)
  - fix nis locking (#132204)
  - RTLD_DEEPBIND support
  - fix pthread_create bugs (BZ #401, #405)

* Wed Sep 22 2004 Roland McGrath <roland@redhat.com> 2.3.3-56
- migrated CVS to fedora-branch in sources.redhat.com glibc repository
  - source tarballs renamed
  - redhat/ moved to fedora/, some old cruft removed
- update from trunk
  - some __nonnull annotations

* Wed Sep 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-55
- update from CVS
  - set{re,e,res}[ug]id now affect the whole process in NPTL
  - return EAGAIN instead of ENOMEM when not enough memory
    in pthread_create

* Fri Sep 17 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-54
- update from CVS
  - nscd getaddrinfo caching

* Tue Sep 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-53
- restore temporarily old definition of __P()/__PMT()
  for third party apps

* Tue Sep 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-52
- update from CVS
  - nscd bi-arch fix
  - remove all uses of __P()/__PMT() from glibc headers
- update and reenable nscd SELinux patch
- remove libnss1* and libnss*.so.1 compatibility NSS modules
  on IA-32, SPARC and Alpha

* Fri Sep 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-51
- update from CVS
  - disable one of the malloc double free checks for non-contiguous
    arenas where it doesn't have to be true even for non-broken
    apps

* Thu Sep  9 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-50
- update from CVS
  - pwd/grp/host loops with nscd speed up by sharing the
    nscd cache r/o with applications
  - inexpensive double free check in free(3)
  - make NPTL pthread.h initializers usable even from C++
    (BZ #375)
- use atomic instructions even in i386 nscd on i486+ CPUs
  (conditionally)

* Fri Sep  3 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-49
- update from CVS
- fix linuxthreads tst-cancel{[45],-static}

* Fri Sep  3 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-48
- update from CVS
  - fix pthread_cond_destroy (BZ #342)
  - fix fnmatch without FNM_NOESCAPE (BZ #361)
  - fix ppc32 setcontext (BZ #357)
- add NPTL support for i386 glibc (only if run on i486 or higher CPU)
- add __NR_waitid defines for i386, x86_64 and sparc*

* Tue Aug 31 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-47
- update from CVS
  - persistent nscd caching
  - ppc64 32-bit atomicity fix
  - fix x86-64 nptl-devel headers for -m32 compilation
- %%ghost /etc/ld.so.cache (#130597)
- edit /etc/ld.so.conf in glibc_post_upgrade if
  include ld.so.conf.d/*.conf line is missing (#120588)
- ugly hacks for the IA-64 /emul braindamage (#124996, #128267)

* Sat Aug 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-46
- update from CVS

* Thu Aug 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-45
- update from CVS
  - fix nss_compat's initgroups handling (#130363)
  - fix getaddrinfo ai_canonname setting

* Thu Aug 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-44
- update from CVS
  - add ip6-dotint resolv.conf option, make
    no-ip6-dotint the default
- BuildPrereq libselinux-devel (#129946)
- on ppc64, build without dot symbols

* Thu Aug 12 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-43
- update from CVS
  - remove debugging printout (#129747)
  - make <sys/shm.h> usable in C++ (IT#45148)
- update RLIMIT_* constants in <bits/resource.h>, make
  <sys/resource.h> POSIX compliant (#129740)

* Wed Aug 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-42
- fix last tzset () fixes, disable rereading of /etc/localtime
  every time for now
- really enable SELinux support for NSCD

* Wed Aug 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-41
- update from CVS
  - fread_unlocked/fwrite_unlocked macro fixes (BZ #309, #316)
  - tzset () fixes (BZ #154)
- speed up pthread_rwlock_unlock on arches other than i386 and
  x86_64 (#129455)
- fix compilation with -ansi (resp. -std=c89 or -std=c99) and
  -D_XOPEN_SOURCE=[56]00 but no -D_POSIX_SOURCE* or -D_POSIX_C_SOURCE*
  (BZ #284)
- add SELinux support for NSCD

* Fri Aug  6 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-40
- update from CVS
  - change res_init to force all threads to re-initialize
    resolver before they use it next time (#125712)
  - various getaddrinfo and related fixes (BZ #295, #296)
  - fix IBM{932,943} iconv modules (#128674)
  - some nscd fixes (e.g. BZ #292)
  - RFC 3678 support (Multicast Source Filters)
- handle /lib/i686/librtkaio-* in i386 glibc_post_upgrade
  the same as /lib/i686/librt-*

* Fri Jul 23 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-39
- update from CVS
  - conformance related changes in headers
- remove -finline-limit=2000 for GCC 3.4.x+

* Thu Jul 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-38
- update from CVS
  - fix res_init leaks
  - fix newlocale races
  - fix ppc64 setjmp
- fix strtold (BZ #274)

* Fri Jul 16 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-37
- update from CVS
  - allow pthread_cancel in DSO destructors run at exit time
- fix pow{f,,l} on IA-32 and powl on x86-64
- allow PIEs on IA-32 to have main in a shared library they depend on

* Mon Jul  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-36
- s390* .plt slot reduction
- fix pthread_rwlock_timedrdlock on x86_64

* Wed Jun 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-35
- tweak spec file for the libpthread-0.61.so -> libpthread-2.3.3.so
  NPTL changes

* Wed Jun 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-34
- update from CVS
  - if_nameindex using preferably netlink
  - printf_parsemb initialization fix
  - NPTL version is now the same as glibc version

* Mon Jun 28 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-33
- update from CVS
  - reread resolv.conf for nscd --invalidate=hosts
  - fix F_GETLK/F_SETLK/F_SETLKW constants on x86_64 for
    -m32 -D_FILE_OFFSET_BITS=64 compilations
  - avoid calling non-existing fcntl64 syscall on ppc64

* Mon Jun 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-32
- update from CVS
  - FUTEX_CMP_REQUEUE support (fix pthread_cond_* deadlocks)
  - fix backtrace in statically linked programs
- rebuilt with GCC 3.4, adjusted ulps and i386 <bits/string.h>

* Fri May 28 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-31
- update from CVS
- <bits/string2.h> and <bits/mathinline.h> changes for GCC 3.{2,4,5}+
- make c_stubs buildable even with GCC 3.2.x (#123042)

* Fri May 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-30
- fix pthread_cond_wait on architectures other than IA-32 and
  x86_64

* Thu May 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-29
- use lib64 instead of lib on ia64 if %%{_lib} is defined to lib64

* Wed May 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-28
- update from CVS
  - FUTEX_REQUEUE fixes (#115349)
  - SPARC GCC 3.4 build fix
  - fix handling of undefined TLS symbols on IA32 (RELA only),
    SPARC and SH
  - regex translate fix
  - speed up sprintf
  - x86_64 makecontext alignment fix
  - make POSIX sigpause the default sigpause, unless BSD sigpause
    requested

* Tue May 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-27
- remove /lib64/tls/librtkaio-2.3.[23].so in glibc_post_upgrade
  on x86-64, s390x and ppc64 instead of /lib/tls/librtkaio-2.3.[23].so
- build mq_{send,receive} with -fexceptions

* Fri May  7 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-26
- update from CVS
  - fix <tgmath.h>
  - fix memory leaks in nis, getifaddrs, etc. caused by incorrect
    use of realloc
- remove /lib/{tls,i686}/librtkaio-2.3.[23].so in glibc_post_upgrade
  and rerun ldconfig if needed, otherwise after glibc upgrade librt.so.1
  might be a stale symlink

* Wed May  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-25
- update from CVS
- disable FUTEX_REQUEUE (work around #115349)
- mq for sparc/sparc64/ia64

* Tue May  4 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-24
- update from CVS
  - define S_ISSOCK in -D_XOPEN_SOURCE=600 and S_I[FS]SOCK
    plus F_[SG]ETOWN also in -D_XOPEN_SOURCE=500 (both
    included already in XNS5)
  - reorder dlopen checks, so that dlopening ET_REL objects
    complains about != ET_DYN != ET_EXEC, not about phentsize
    (#121606)
  - fix strpbrk macro for GCC 3.4+ (BZ #130)
  - fix <sys/sysctl.h> (BZ #140)
  - sched_[gs]etaffinity documentation fix (BZ #131)
  - fix sparc64 build (BZ #139)
  - change linuxthreads back to use non-cancellable writes
    to manager pipes etc.
  - fix sem_timedwait return value in linuxthreads (BZ #133)
  - ia64 unnecessary PLT relocs removal

* Thu Apr 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-23
- update from CVS
  - fix *scanf
  - fix shm_unlink, sem_unlink and mq_unlink errno values
  - avoid memory leaks in error
  - execstack fixes on s390

* Mon Apr 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-22
- update from CVS
  - mq and timer fixes
- rebuilt with binutils >= 2.15.90.0.3-2 to fix IA-64 statically
  linked binaries
- fix linuxthreads librt.so on s390{,x}, so it is no longer DT_TEXTREL

* Sat Apr 17 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-21
- disable rtkaio
- update from CVS
  - POSIX message passing support
  - fixed SIGEV_THREAD support for POSIX timers
  - fix free on non-malloced memory in syslog
  - fix ffsl on some 64-bit arches
  - fix sched_setaffinity on x86-64, ia64
  - fix ppc64 umount
  - NETID_AUTHORITATIVE, SERVICES_AUTHORITATIVE support
  - various NIS speedups
  - fix fwrite with > 2GB sizes on 64-bit arches
  - fix pthread_getattr_np guardsize reporting in NPTL
- report PLT relocations in ld.so and libc.so during the build

* Thu Mar 25 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-20
- update from CVS
  - change NPTL PTHREAD_MUTEX_ADAPTIVE_NP mutexes to spin on SMP
  - strtol speed optimization
  - don't try to use certainly unimplemented syscalls on ppc64
- kill -debug subpackage, move the libs to glibc-debuginfo{,-common}
  into /usr/lib/debug/usr/%%{_lib}/ directory
- fix c_stubs with gcc 3.4
- move all the up to 3 builds into %%build scriptlet and
  leave only installation in the %%install scriptlet

* Mon Mar 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-19
- update from CVS
  - affinity API changes

* Thu Mar 18 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-18
- update from CVS
  - fix ia64 iopl (#118591)
  - add support for /etc/ld.so.conf.d/*.conf
  - fix x86-64 LD_DEBUG=statistics
- fix hwcap handling when using ld.so.cache (#118518)

* Mon Mar 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-17
- update from CVS
  - implement non-_l function on top of _l functions

* Thu Mar 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-16
- update from CVS
- fix s390{,x} TLS handling

* Wed Mar 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-15
- update from CVS
  - special section for compatibility code
  - make getpid () work even in vfork () child
- configure with --enable-bind-now to avoid lazy binding in ld.so
  and libc.so

* Fri Mar  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-14
- update from CVS
  - fix iconv -c (#117021)
  - fix PIEs on sparc/sparc64
  - fix posix_fadvise on 64-bit architectures
- add locale-archive as %%ghost file (#117014)

* Mon Mar  1 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-13
- update from CVS

* Fri Feb 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-12
- update from CVS

* Fri Feb 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-11
- update from CVS
  - fix ld.so when vDSO is randomized

* Fri Feb 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-10
- update from CVS

* Fri Feb 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-9
- update from CVS

* Tue Feb 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-8
- update from CVS

* Tue Jan 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-7
- update from CVS
  - dl_iterate_phdr extension to signal number of added/removed
    libraries
- fix PT_GNU_RELRO support on ppc* with prelinking

* Fri Jan 23 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-6
- rebuilt with fixed GCC on IA-64

* Thu Jan 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-5
- fix PT_GNU_RELRO support

* Wed Jan 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-4
- update from CVS
  - some further regex speedups
  - fix re.translate handling in regex (#112869)
  - change regfree to match old regex behaviour (what is freed
    and clearing of freed pointers)
  - fix accesses to unitialized memory in regex (#113507, #113425,
    #113421)
  - PT_GNU_RELRO support

* Tue Dec 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.3-3
- update from CVS
  - fix pmap_set fd and memory leak (#112726)
- fix backreference handling in regex
- rebuilt under glibc without the above bug to fix
  libc.so linker script (#112738)

* Mon Dec 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.3-2
- update from CVS
  - faster getpid () in NPTL builds
  - fix to make pthread_setcancelstate (PTHREAD_CANCEL_DISABLE, )
    really disable cancellation (#112512)
  - more regex fixes and speedups
  - fix nextafter*/nexttoward*
  - handle 6th syscall(3) argument on AMD64
  - handle memalign/posix_memalign in mtrace
  - fix linuxthreads memory leak (#112208)
  - remove throw () from cancellation points in linuxthreads (#112602)
  - fix NPTL unregister_atfork
  - fix unwinding through alternate signal stacks

* Mon Dec  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.3-1
- update from CVS
  - 2.3.3 release
  - lots of regex fixes and speedups (#110401)
  - fix atan2
  - fix pshared condvars in NPTL
  - fix pthread_attr_destroy for attributes created with
    pthread_attr_init@GLIBC_2.0
- for the time being, include both nb_NO* and no_NO* as locales
  so that the distribution can catch up with the no_NO->nb_NO
  transition
- add BuildPrereq texinfo (#110252)

* Tue Nov 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-102
- update from CVS
  - fix getifaddrs (CAN-2003-0859)
  - fix ftw fd leak
  - fix linuxthreads sigaction (#108634)
  - fix glibc 2.0 stdio compatibility
  - fix uselocale (LC_GLOBAL_LOCALE)
  - speed up stdio locking in non-threaded programs on IA-32
  - try to maintain correct order of cleanups between those
    registered with __attribute__((cleanup))
    and with LinuxThreads style pthread_cleanup_push/pop (#108631)
  - fix segfault in regex (#109606)
  - fix RE_ICASE multi-byte handling in regex
  - fix pthread_exit in libpthread.a (#109790)
  - FTW_ACTIONRETVAL support
  - lots of regex fixes and speedups
  - fix ceill/floorl on AMD64

* Mon Oct 27 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-101
- update from CVS
  - fix ld.so --verify (and ldd)

* Mon Oct 27 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-100
- update from CVS
  - fix sprof (#103727)
  - avoid infinite loops in {,f}statvfs{,64} with hosed mounts file
  - prevent dlopening of executables
  - fix glob with GLOB_BRACE and without GLOB_NOESCAPE
  - fix locale printing of word values on 64-bit big-endian arches
    (#107846)
  - fix getnameinfo and getaddrinfo with reverse IPv6 lookups
    (#101261)

* Wed Oct 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-99
- update from CVS
  - dl_iterate_phdr in libc.a on arches other than IA-64
  - LD_DEBUG=statistics prints number of relative relocations
  - fix hwcap computation
- NPTL is now part of upstream glibc CVS
- include {st,xh,zu}_ZA{,.UTF-8} locales

* Sat Oct  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-98
- update from CVS
  - fix close, pause and fsync (#105348)
  - fix pthread_once on IA-32
- implement backtrace () on IA-64, handle -fomit-frame-pointer
  in AMD64 backtrace () (#90402)

* Tue Sep 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-97
- update from CVS
  - fix <sys/sysmacros.h> with C++ or -ansi or -pedantic C
  - fix mknod/ustat return value when given bogus device number (#105768)

* Fri Sep 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-96
- rebuilt

* Fri Sep 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-95
- fix IA-64 getcontext

* Thu Sep 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-94
- update from CVS
- fix syslog with non-C non-en_* locales (#61296, #104979)
- filter GLIBC_PRIVATE symbols from glibc provides
- fix NIS+

* Thu Sep 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-93
- update from CVS
- assume 2.4.21 kernel features on RHEL/ppc*, so that
  {make,set,get,swap}context works
- backout execstack support for RHEL
- build rtkaio on amd64 too

* Wed Sep 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-92
- update from CVS
  - execstack/noexecstack support
  - build nscd as PIE
- move __libc_stack_end back to @GLIBC_2.1
- build against elfutils >= 0.86 to fix stripping on s390x

* Mon Sep 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-91
- rebuilt

* Mon Sep 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-90
- update from CVS
  - NPTL locking change (#102682)
- don't jump around lock on amd64

* Thu Sep 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-89
- fix open_memstream/syslog (#104661)

* Thu Sep 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-88
- update from CVS
  - retrieve affinity in pthread_getattr_np
  - fix pthread_attr_[gs]etaffinity_np
  - handle hex and octal in wordexp

* Wed Sep 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-87
- update from CVS
  - truncate instead of round in utimes when utimes syscall is not available
  - don't align stack in every glibc function unnecessarily on IA-32
  - make sure threads have their stack 16 byte aligned on IA-32
  - move sched_[sg]etaffinity to GLIBC_2.3.3 symbol version (#103231)
  - fix pthread_getattr_np for the initial thread (#102683)
  - avoid linuxthreads signal race (#104368)
- ensure all gzip invocations are done with -n option

* Fri Sep 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-86
- update from CVS
- avoid linking in libgcc_eh.a unnecessarily
- change ssize_t back to long int on s390 -m31, unless
  gcc 2.95.x is used

* Wed Sep 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-85
- update from CVS
  - fix IA-64 memccpy (#104114)

* Tue Sep  9 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-84
- update from CVS
  - undo broken amd64 signal context changes

* Tue Sep  9 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-83
- update from CVS
- change *nlink_t, *ssize_t and *intptr_t types on s390 -m31 to
  {unsigned,} int
- change *u_quad_t, *quad_t, *qaddr_t, *dev_t, *ino64_t, *loff_t,
  *off64_t, *rlim64_t, *blkcnt64_t, *fsblkcnt64_t, *fsfilcnt64_t
  on 64-bit arches from {unsigned,} long long int {,*} to
  {unsigned,} long int {,*} to restore binary compatibility
  for C++ functions using these types as arguments

* Sun Sep  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-82
- rebuilt

* Sat Sep  6 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-81
- update from CVS
  - fix tc[gs]etattr/cf[gs]et[io]speed on ppc (#102732)
  - libio fixes

* Thu Sep  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-80
- update from CVS
  - fix IA-64 cancellation when mixing __attribute__((cleanup ()))
    and old-style pthread_cleanup_push cleanups

* Tue Sep  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-79
- updated from CVS
  - lots of cancellation fixes
  - fix posix_fadvise* on ppc32
  - TLS layout fix
  - optimize stdio cleanups (#103354)
  - sparcv9 NPTL
  - include sigset, sighold, sigrelse, sigpause and sigignore prototypes
    in signal.h even if -D_XOPEN_SOURCE_EXTENDED (#103269)
  - fix svc_getreqset on 64-bit big-endian arches
  - return ENOSYS in linuxthreads pthread_barrierattr_setpshared for
    PTHREAD_PROCESS_SHARED
  - add pthread_cond_timedwait stubs to libc.so (#102709)
- split glibc-devel into glibc-devel and glibc-headers to ensure
  amd64 /usr/include always wins on amd64/i386 bi-arch installs
- increase PTHREAD_STACK_MIN on alpha, ia64 and sparc*
- get rid of __syscall_* prototypes and stubs in sysdeps/unix/sysv/linux
- run make check also with linuxthreads (on IA-32 non-FLOATING_STACKS)
  ld.so and NPTL (on IA-32 also FLOATING_STACKS linuxthreads) libraries
  and tests

* Mon Aug 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-78
- include dl-osinfo.h only in glibc-debuginfo-2*.rpm, not
  in glibc-debuginfo-common*

* Mon Aug 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-77
- update from CVS
  - fix glibc 2.0 libio compatibility (#101385)
  - fix ldconfig with /usr/lib/lib*.so symlinks (#102853)
  - fix assert.h (#102916, #103017)
  - make ld.so.cache identical between IA-32 and AMD64 (#102887)
  - fix static linking of large IA-64 binaries (#102586)
- avoid using floating point regs in lazy binding code on ppc64 (#102763)

* Fri Aug 22 2003 Roland McGrath <roland@redhat.com> 2.3.2-76
- add td_thr_tls_get_addr changes missed in initial nptl_db rewrite

* Sun Aug 17 2003 Roland McGrath <roland@redhat.com> 2.3.2-74
- nptl_db rewrite not yet in CVS

* Thu Aug 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-72
- update from CVS
  - fix rtkaio aio_fsync{,64}
  - update rtkaio for !BROKEN_THREAD_SIGNALS
  - fix assert macro when used on pointers

* Wed Aug 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-71
- update from CVS

* Tue Aug 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-70
- update from CVS
- disable CLONE_STOPPED for now until it is resolved
- strip crt files
- fix libio on arches with no < GLIBC_2.2 support (#102102, #102105)
- fix glibc-debuginfo to include all nptl and nptl_db sources

* Thu Aug  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-69
- update from CVS
  - fix pthread_create@GLIBC_2.0 (#101767)
- __ASSUME_CLONE_STOPPED on all arches but s390* in RHEL

* Sun Aug  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-68
- update from CVS
  - only use CLONE_STOPPED if kernel supports it, fix setting of thread
    explicit scheduling (#101457)

* Fri Aug  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-67
- update from CVS
  - fix utimes and futimes if kernel doesn't support utimes syscall
  - fix s390 ssize_t type
  - fix dlerror when called before any dlopen/dlsym
  - update IA-64 bits/sigcontext.h (#101344)
  - various warning fixes
  - fix pthread.h comment typos (#101363)

* Wed Jul 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-66
- update from CVS
- fix dlopen of libraries using TLS IE/LE models

* Tue Jul 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-65
- update from CVS
  - fix timer_create
  - use __extension__ before long long typedefs in <bits/types.h> (#100718)

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-64
- update from CVS
  - fix wcpncpy (#99462)
  - export _res@GLIBC_2.0 even from NPTL libc.so (__res_state ()
    unlike __errno_location () or __h_errno_location () was introduced
    in glibc 2.2)
  - fix zic bug on 64-bit platforms
  - some TLS handling fixes
  - make ldconfig look into alternate ABI dirs by default (#99402)
- move %%{_datadir}/zoneinfo to tzdata package, so that it can be
  errataed separately from glibc
- new add-on - rtkaio
- prereq libgcc, as glibc now relies on libgcc_s.so.1 for pthread_cancel

* Tue Jul 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-63
- fix thread cancellation on ppc64

* Sat Jul 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-62
- update from CVS
  - fix thread cancellation on ppc32, s390 and s390x

* Thu Jul 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-61
- update from CVS
  - build libc_nonshared.a with -fPIC instead of -fpic
- fix ppc64 PIE support
- add cfi directives to NPTL sysdep-cancel.h on ppc/ppc64/s390/s390x

* Tue Jul  8 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-60
- update from CVS

* Thu Jul  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-59
- update from CVS
- on IA-64 use different symbols for cancellation portion of syscall
  handlers to make gdb happier

* Thu Jun 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-58
- update from CVS
  - nss_compat supporting LDAP etc.

* Tue Jun 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-57
- update from CVS

* Thu Jun 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-56
- fix condvars and semaphores in ppc* NPTL
- fix test-skeleton.c reporting of timed-out tests (#91269)
- increase timeouts for tests during make check

* Wed Jun 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-55
- make ldconfig default to both /lib+/usr/lib and /lib64+/usr/lib64
  on bi-ABI architectures (#97557)
- disable FUTEX_REQUEUE on ppc* temporarily

* Wed Jun 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-54
- update from CVS
- fix glibc_post_upgrade on ppc

* Tue Jun 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-53
- update from CVS
- fix localedef (#90659)
- tweak linuxthreads for librt cancellation

* Mon Jun 16 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-52
- update from CVS

* Thu Jun 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-51
- update from CVS
- fix <gnu/stubs.h> (#97169)

* Wed Jun 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-50
- update from CVS

* Tue Jun 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-49
- update from CVS
  - fix pthread_cond_signal on IA-32 (#92080, #92253)
  - fix setegid (#91567)
- don't prelink -R libc.so on any architecture, it prohibits
  address randomization

* Thu Jun  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-48
- update from CVS
  - fix IA-64 NPTL build

* Thu Jun  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-47
- update from CVS
- PT_GNU_STACK segment in binaries/executables and .note.GNU-stack
  section in *.[oa]

* Sun Jun  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-46
- update from CVS
- enable NPTL on AMD64
- avoid using trampolines in localedef

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-45
- enable NPTL on IA-64

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-44
- update from CVS
- enable NPTL on s390 and s390x
- make __init_array_start etc. symbols in elf-init.oS hidden undefined

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-43
- update from CVS

* Fri May 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-42
- update from CVS

* Tue May 20 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-41
- update from CVS
- use NPTL libs if uname -r contains nptl substring or is >= 2.5.69
  or set_tid_address syscall is available instead of checking
  AT_SYSINFO dynamic tag

* Thu May 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-40
- update from CVS

* Wed May 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-39
- update from CVS
  - fix for prelinking of libraries with no dependencies

* Tue May 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-38
- update from CVS
- enable NPTL on ppc and ppc64

* Tue May  6 2003 Matt Wilson <msw@redhat.com> 2.3.2-37
- rebuild

* Sun May  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-36
- update from CVS

* Sat May  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-35
- update from CVS
  - make -jN build fixes

* Fri May  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-34
- update from CVS
- avoid using trampolines in iconvconfig for now

* Sat Apr 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-33
- update from CVS

* Fri Apr 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-32
- update from CVS
- more ppc TLS fixes

* Wed Apr 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-31
- update from CVS
  - nscd fixes
  - fix Bahrain spelling (#56298)
  - fix Ukrainian collation (#83973)
  - accept trailing spaces in /etc/ld.so.conf (#86032)
  - perror fix (#85994)
  - fix localedef (#88978)
  - fix getifaddrs (#89026)
  - fix strxfrm (#88409)
- fix ppc TLS
- fix getaddrinfo (#89448)
- don't print warning about errno, h_errno or _res if
  LD_ASSUME_KERNEL=2.4.1 or earlier

* Tue Apr 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-30
- update from CVS
- fix prelink on ppc32
- add TLS support on ppc32 and ppc64
- make sure on -m64 arches all helper binaries are built with this
  option

* Mon Apr 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-29
- update from CVS
  - fix strxfrm (#88409)
- use -m64 -mno-minimal-toc on ppc64
- conflict with kernels < 2.4.20 on ppc64 and < 2.4.0 on x86_64
- link glibc_post_upgrade against newly built libc.a

* Sun Apr 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-28
- update from CVS
  - fix NPTL pthread_detach and already terminated, but not yet
    joined thread (#88219)
  - fix bug-regex4 testcase (#88118)
  - reenable prelink support broken in 2.3.2-13
  - fix register_printf_function (#88052)
  - fix double free with fopen using ccs= (#88056)
  - fix potential access below $esp in {set,swap}context (#88093)
  - fix buffer underrun in gencat -H (#88099)
  - avoid using unitialized variable in tst-tgmath (#88101)
  - fix gammal (#88104)
  - fix iconv -c
  - fix xdr_string (PR libc/4999)
  - fix /usr/lib/nptl/librt.so symlink
  - avoid running NPTL cleanups twice in some cases
  - unblock __pthread_signal_cancel in linuxthreads, so that
    linuxthreads threaded programs work correctly if spawned
    from NPTL threaded programs
  - fix sysconf _SC_{NPROCESSORS_{CONF,ONLN},{,AV}PHYS_PAGES}
- remove /lib/i686 directory before running ldconfig in glibc post
  during i686 -> i386 glibc "upgrades" (#88456)

* Wed Apr  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-22
- update from CVS
  - add pthread_atfork to libpthread.a

* Tue Apr  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-21
- update from CVS
- make sure linuxthreads pthread_mutex_lock etc. is not a cancellation
  point

* Sat Mar 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-20
- update from CVS
- if kernel >= 2.4.1 doesn't support NPTL, fall back to
  /lib/i686 libs on i686, not stright to /lib

* Fri Mar 28 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-19
- update from CVS
  - timers fixes

* Thu Mar 27 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-18
- update from CVS
- fix NPTL pthread_cond_timedwait
- fix sysconf (_SC_MONOTONIC_CLOCK)
- use /%%{_lib}/tls instead of /lib/tls on x86-64
- add /%%{_lib}/tls/librt*so* and /%%{_lib}/i686/librt*so*
- display content of .out files for all make check failures

* Wed Mar 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-17
- update from CVS
  - kernel POSIX timers support

* Sat Mar 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-16
- update from CVS
  - export __fork from glibc again
- fix glibc-compat build in NPTL
- fix c_stubs
- fix some more atomic.h problems
- don't check abi in glibc-compat libs

* Fri Mar 21 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-15
- update from CVS
- build glibc-compat (for glibc 2.0 compatibility) and c_stubs add-ons
- condrestart sshd in glibc_post_upgrade so that the user can
  log in remotely and handle the rest (#86339)
- fix a typo in glibc_post_upgrade on sparc

* Tue Mar 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-14
- update from CVS
- change i686/athlon libc.so.6 base to 0x00e80000

* Mon Mar 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-13
- update from CVS
  - hopefully last fix for condvar problems

* Fri Mar 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-12
- fix bits/syscall.h creation on x86-64

* Thu Mar 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-11
- update from CVS

* Wed Mar 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-10
- update from CVS

* Tue Mar 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-9
- update from CVS
- fix glibc-debug description (#85111)
- make librt.so a symlink again, not linker script

* Tue Mar  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-8
- update from CVS
- remove the workarounds for broken software accessing GLIBC_PRIVATE
  symbols

* Mon Mar  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-7
- update from CVS

* Sun Mar  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-6
- fix TLS IE/LE model handling in dlopened libraries
  on TCB_AT_TP arches

* Tue Feb 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-5
- update from CVS

* Tue Feb 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4
- update from CVS

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-3
- update from CVS
- only warn about errno, h_errno or _res for binaries, never
  libraries
- rebuilt with gcc-3.2.2-4 to use direct %%gs TLS access insn sequences

* Sun Feb 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-2
- update from CVS

* Sat Feb 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-1
- update from CVS

* Thu Feb 20 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-51
- update from CVS

* Wed Feb 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-50
- update from CVS

* Wed Feb 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-49
- update from CVS
- remove nisplus and nis from the default nsswitch.conf (#67401, #9952)

* Tue Feb 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-48
- update from CVS

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-47
- update from CVS

* Fri Feb 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-46
- update from CVS
  - pthread_cond* NPTL fixes, new NPTL testcases

* Thu Feb 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-45
- update from CVS
- include also linuxthreads FLOATING_STACKS libs on i686 and athlon:
  LD_ASSUME_KERNEL=2.2.5 to LD_ASSUME_KERNEL=2.4.0 is non-FLOATING_STACKS lt,
  LD_ASSUME_KERNEL=2.4.1 to LD_ASSUME_KERNEL=2.4.19 is FLOATING_STACKS lt,
  later is NPTL
- enable TLS on alpha/alphaev6
- add BuildPreReq: /usr/bin/readlink

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-44
- update from CVS
  - pthread_once fix

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-43
- update from CVS
- vfork fix on s390
- rebuilt with binutils 2.13.90.0.18-5 so that accesses to errno
  don't bind locally (#83325)

* Thu Feb 06 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-42
- update from CVS
- fix pthread_create after vfork+exec in linuxthreads

* Wed Feb 05 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-41
- update from CVS

* Thu Jan 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-40
- update from CVS

* Wed Jan 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-39
- update from CVS
- enable TLS on s390{,x} and sparc{,v9}

* Fri Jan 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-38
- update from CVS
- initialize __environ in glibc_post_upgrade to empty array,
  so that it is not NULL
- compat symlink for s390x /lib/ld64.so.1
- enable glibc-profile on x86-64
- only include libNoVersion.so on IA-32, Alpha and Sparc 32-bit

* Thu Jan 16 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-37
- update from CVS
  - nscd fixes, *scanf fix
- fix %%nptlarches noarch build (#81909)
- IA-64 TLS fixes

* Tue Jan 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-36
- update from CVS
- rework -debuginfo subpackage, add -debuginfo-common
  subpackage on IA-32, Alpha and Sparc (ie. auxiliary arches)
- fix vfork in libc.a on PPC32, Alpha, Sparc
- fix libio locks in linuxthreads libc.so if libpthread.so
  is dlopened later (#81374)

* Mon Jan 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-35
- update from CVS
  - dlclose bugfixes
- fix NPTL libpthread.a
- fix glibc_post_upgrade on several arches

* Sat Jan 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-34
- update from CVS
- TLS support on IA-64

* Wed Jan  8 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-33
- fix vfork in linuxthreads (#81377, #81363)

* Tue Jan  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-32
- update from CVS
- don't use TLS libs if kernel doesn't set AT_SYSINFO
  (#80921, #81212)
- add ntp_adjtime on alpha (#79996)
- fix nptl_db (#81116)

* Sun Jan  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-31
- update from CVS
- support all architectures again

* Fri Jan  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-30
- fix condvar compatibility wrappers
- add ugly hack to use non-TLS libs if a binary is seen
  to have errno, h_errno or _res symbols in .dynsym

* Fri Jan  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-29
- update from CVS
  - fixes for new condvar

* Thu Jan  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-28
- new NPTL condvar implementation plus related linuxthreads
  symbol versioning updates

* Thu Jan  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-27
- update from CVS
- fix #include <sys/stat.h> with -D_BSD_SOURCE or without
  feature set macros
- make *sigaction, sigwait and raise the same between
  -lpthread -lc and -lc -lpthread in linuxthreads builds

* Tue Dec 31 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-26
- fix dlclose

* Sun Dec 29 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-25
- enable sysenter by default for now
- fix endless loop in ldconfig

* Sat Dec 28 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-24
- update from CVS

* Fri Dec 27 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-23
- update from CVS
  - fix ptmalloc_init after clearenv (#80370)

* Sun Dec 22 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-22
- update from CVS
- add IA-64 back
- move TLS libraries from /lib/i686 to /lib/tls

* Thu Dec 19 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-21
- system(3) fix for linuxthreads
- don't segfault in pthread_attr_init from libc.so
- add cancellation tests from nptl to linuxthreads

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-20
- fix up lists of exported symbols + their versions
  from the libraries

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-19
- fix --with-tls --enable-kernel=2.2.5 libc on IA-32

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-18
- update from CVS
  - fix NPTL hanging mozilla
  - initialize malloc in mALLOPt (fixes problems with squid, #79957)
  - make linuxthreads work with dl_dynamic_weak 0
  - clear dl_dynamic_weak everywhere

* Tue Dec 17 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-17
- update from CVS
  - NPTL socket fixes, flockfile/ftrylockfile/funlockfile fix
  - kill -debug sub-package, rename -debug-static to -debug
  - clear dl_dynamic_weak for NPTL

* Mon Dec 16 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-16
- fix <bits/mathinline.h> and <bits/nan.h> for C++
- automatically generate NPTL libpthread wrappers

* Mon Dec 16 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-15
- update from CVS
  - all functions which need cancellation should now be cancellable
    both in libpthread.so and libc.so
  - removed @@GLIBC_2.3.2 cancellation wrappers

* Fri Dec 13 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-14
- update from CVS
  - replace __libc_lock_needed@GOTOFF(%%ebx) with
    %%gs:offsetof(tcbhead_t, multiple_threads)
  - start of new NPTL cancellation wrappers

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-13
- update from CVS
- use inline locks in malloc

* Tue Dec 10 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-12
- update from CVS
  - support LD_ASSUME_KERNEL=2.2.5 in statically linked programs

* Mon Dec  9 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-11
- update from CVS
- rebuilt with gcc-3.2.1-2

* Fri Dec  6 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-10
- update from CVS
- non-nptl --with-tls --without-__thread FLOATING_STACKS libpthread
  should work now
- faster libc locking when using nptl
- add OUTPUT_FORMAT to linker scripts
- fix x86_64 sendfile (#79111)

* Wed Dec  4 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-9
- update from CVS
  - RUSCII support (#78906)
- for nptl builds add BuildRequires
- fix byteswap.h for non-gcc (#77689)
- add nptl-devel package

* Tue Dec  3 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-8
- update from CVS
  - make --enable-kernel=2.2.5 --with-tls --without-__thread
    ld.so load nptl and other --with-__thread libs
- disable nptl by default for now

* Wed Nov 27 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-7
- update from CVS
- restructured redhat/Makefile and spec, so that src.rpm contains
  glibc-<date>.tar.bz2, glibc-redhat-<date>.tar.bz2 and glibc-redhat.patch
- added nptl

* Fri Nov  8 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-6
- update from CVS
  - even more regex fixes
- run sed testsuite to check glibc regex

* Thu Oct 24 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-5
- fix LD_DEBUG=statistics and LD_TRACE_PRELINKING in programs
  using libpthread.so.

* Thu Oct 24 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-4
- update from CVS
  - fixed %%a and %%A in *printf (#75821)
  - fix re_comp memory leaking (#76594)

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-3
- update from CVS
  - some more regex fixes
- fix libpthread.a (#76484)
- fix locale-archive enlarging

* Fri Oct 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-2
- update from CVS
  - don't need to use 128K of stacks for DNS lookups
  - regex fixes
  - updated timezone data e.g. for this year's Brasil DST
    changes
  - expand ${LIB} in RPATH/RUNPATH/dlopen filenames

* Fri Oct 11 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-1
- update to 2.3.1 final
  - support really low thread stack sizes (#74073)
- tzdata update

* Wed Oct  9 2002 Jakub Jelinek <jakub@redhat.com> 2.3-2
- update from CVS
  - handle low stack limits
  - move s390x into */lib64

* Thu Oct  3 2002 Jakub Jelinek <jakub@redhat.com> 2.3-1
- update to 2.3 final
  - fix freopen on libstdc++ <= 2.96 stdin/stdout/stderr (#74800)

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-3
- don't prelink -r libc.so on ppc/x86-64/sparc*, it doesn't
  speed things up, because they are neither REL arches, nor
  ELF_MACHINE_REL_RELATIVE
- fix sparc64 build

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-2
- update from CVS

* Sat Sep 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-1
- update from CVS
- prelink on ppc and x86-64 too
- don't remove ppc memset
- instead of listing on which arches to remove glibc-compat
  list where it should stay

* Fri Sep  6 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-5
- fix wcsmbs functions with invalid character sets (or malloc
  failures)
- make sure __ctype_b etc. compat vars are updated even if
  they are copy relocs in the main program

* Thu Sep  5 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-4
- fix /lib/libnss1_dns.so.1 (missing __set_h_errno definition
  leading to unresolved __set_h_errno symbol)

* Wed Sep  4 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-3
- security fix - increase dns-network.c MAXPACKET to at least
  65536 to avoid buffer overrun. Likewise glibc-compat
  dns-{host,network}.c.

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-2
- temporarily add back __ctype_b, __ctype_tolower and __ctype_toupper to
  libc.a and export them as @@GLIBC_2.0 symbols, not @GLIBC_2.0
  from libc.so - we have still lots of .a libraries referencing
  __ctype_{b,tolower,toupper} out there...

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-1
- update from CVS
  - 2.2.93 release
  - use double instead of single indirection in isXXX macros
  - per-locale wcsmbs conversion state

* Sat Aug 31 2002 Jakub Jelinek <jakub@redhat.com> 2.2.92-2
- update from CVS
  - fix newlocale/duplocale/uselocale
- disable profile on x86_64 for now

* Sat Aug 31 2002 Jakub Jelinek <jakub@redhat.com> 2.2.92-1
- update from CVS
  - 2.2.92 release
  - fix gettext after uselocale
  - fix locales in statically linked threaded programs
  - fix NSS

* Thu Aug 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.91-1
- update from CVS
  - 2.2.91 release
  - fix fd leaks in locale-archive reader (#72043)
- handle EROFS in build-locale-archive gracefully (#71665)

* Wed Aug 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-27
- update from CVS
  - fix re_match (#72312)
- support more than 1024 threads

* Fri Aug 23 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-26
- update from CVS
  - fix i386 build

* Thu Aug 22 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-25
- update from CVS
  - fix locale-archive loading hang on some (non-primary) locales
    (#72122, #71878)
  - fix umount problems with locale-archives when /usr is a separate
    partition (#72043)
- add LICENSES file

* Fri Aug 16 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-24
- update from CVS
  - only mmap up to 2MB of locale-archive on 32-bit machines
    initially
  - fix fseek past end + fread segfault with mmaped stdio
- include <sys/debugreg.h> which is mistakenly not included
  in glibc-devel on IA-32

* Fri Aug 16 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-23
- don't return normalized locale name in setlocale when using
  locale-archive

* Thu Aug 15 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-22
- update from CVS
  - optimize for primary system locale
- localedef fixes (#71552, #67705)

* Wed Aug 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-21
- fix path to locale-archive in libc reader
- build locale archive at glibc-common %%post time
- export __strtold_internal and __wcstold_internal on Alpha again
- workaround some localedata problems

* Tue Aug 13 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-20
- update from CVS
- patch out set_thread_area for now

* Fri Aug  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-19
- update from CVS
- GB18030 patch from Yu Shao
- applied Debian patch for getaddrinfo IPv4 vs. IPv6
- fix regcomp (#71039)

* Sun Aug  4 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-18
- update from CVS
- use /usr/sbin/prelink, not prelink (#70376)

* Thu Jul 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-17
- update from CVS

* Thu Jul 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-16
- update from CVS
  - ungetc fix (#69586)
  - fseek errno fix (#69589)
  - change *etrlimit prototypes for C++ (#68588)
- use --without-tls instead of --disable-tls

* Thu Jul 11 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-15
- set nscd user's shell to /sbin/nologin (#68369)
- fix glibc-compat buffer overflows (security)
- buildrequire prelink, don't build glibc's own copy of it (#67567)
- update from CVS
  - regex fix (#67734)
  - fix unused warnings (#67706)
  - fix freopen with mmap stdio (#67552)
  - fix realloc (#68499)

* Tue Jun 25 2002 Bill Nottingham <notting@redhat.com> 2.2.90-14
- update from CVS
  - fix argp on long words
  - update atime in libio

* Sat Jun 22 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-13
- update from CVS
  - a thread race fix
  - fix readdir on invalid dirp

* Wed Jun 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-12
- update from CVS
  - don't use __thread in headers
- fix system(3) in threaded apps
- update prelink, so that it is possible to prelink -u libc.so.6.1
  on Alpha

* Fri Jun  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-11
- update from CVS
  - fix __moddi3 (#65612, #65695)
  - fix ether_line (#64427)
- fix setvbuf with mmap stdio (#65864)
- --disable-tls for now, waiting for kernel
- avoid duplication of __divtf3 etc. on IA-64
- make sure get*ent_r and _IO_wfile_jumps are exported (#62278)

* Tue May 21 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-10
- update from CVS
  - fix Alpha pthread bug with gcc 3.1

* Fri Apr 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-35
- fix nice

* Mon Apr 15 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-34
- add relocation dependencies even for weak symbols (#63422)
- stricter check_fds check for suid/sgid binaries
- run make check at %%install time

* Sat Apr 13 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-33
- handle Dec 31 1969 in mktime for timezones west of GMT (#63369)
- back out do-lookup.h change (#63261, #63305)
- use "memory" clobber instead all the fancy stuff in i386/i686/bits/string.h
  since lots of compilers break on it
- fix sparc build with gcc 3.1
- fix spec file for athlon

* Tue Apr  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-32
- fix debugging of threaded apps (#62804)
- fix DST for Estonia (#61494)
- document that pthread_mutexattr_?etkind_np are deprecated
  and pthread_mutexattr_?ettype should be used instead in man
  pages (#61485)
- fix libSegFault.so undefined externals

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-31
- temporarily disable prelinking ld.so, as some statically linked
  binaries linked against debugging versions of old glibcs die on it
  (#62352)
- fix <semaphore.h> for -std=c99 (#62516)
- fix ether_ntohost segfault (#62397)
- remove in glibc_post_upgrade on i386 all /lib/i686/libc-*.so,
  /lib/i686/libm-*.so and /lib/i686/libpthread-*.so, not just current
  version (#61633)
- prelink -r on alpha too

* Thu Mar 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-30
- update GB18030 iconv module (Yu Shao)

* Tue Mar 26 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-29
- features.h fix

* Tue Mar 26 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-28
- update from CVS
  - fix nscd with huge groups
  - fix nis to not close fds it shouldn't
- rebuilt against newer glibc-kernheaders to use the correct
  PATH_MAX
- handle .athlon.rpm glibc the same way as .i686.rpm
- add a couple of .ISO-8859-15 locales (#61908)
- readd temporarily currencies which were superceeded by Euro
  into the list of accepted currencies by localedef to make
  standard conformance testsuites happy
- temporarily moved __libc_waitpid back to make Sun JDK happy
- use old malloc code
- prelink i686/athlon ld.so and prelink -r i686/athlon libc.so

* Thu Mar 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-27
- update from CVS
  - fix DST handling for southern hemisphere (#60747)
  - fix daylight setting for tzset (#59951)
  - fix ftime (#60350)
  - fix nice return value
  - fix a malloc segfault
- temporarily moved __libc_wait, __libc_fork and __libc_stack_end
  back to what they used to be exported at
- censorship (#60758)

* Thu Feb 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-26
- update from CVS
- use __attribute__((visibility(...))) if supported, use _rtld_local
  for ld.so only objects
- provide libc's own __{,u}{div,mod}di3

* Wed Feb 27 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-25
- switch back to 2.2.5, mmap stdio needs work

* Mon Feb 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-8
- fix two other mmap stdio bugs (#60228)

* Thu Feb 21 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-7
- fix yet another mmap stdio bug (#60145)

* Tue Feb 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-6
- fix mmap stdio bug (seen on ld as File truncated error, #60043)
- apply Andreas Schwab's fix for pthread sigwait
- remove /lib/i686/ libraries in glibc_post_upgrade when
  performing i386 glibc install

* Thu Feb 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-5
- update to CVS
- added glibc-utils subpackage
- disable autoreq in glibc-debug
- readd %%lang() to locale files

* Thu Feb  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-4
- update to CVS
- move glibc private symbols to GLIBC_PRIVATE symbol version

* Wed Jan  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-3
- fix a sqrt bug on alpha which caused SHN_UNDEF $__full_ieee754_sqrt..ng
  symbol in libm

* Tue Jan  8 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-2
- add debug-static package

* Mon Dec 31 2001 Jakub Jelinek <jakub@redhat.com> 2.2.90-1
- update from CVS
- remove -D__USE_STRING_INLINES
- add debug subpackage to trim glibc and glibc-devel size

* Wed Oct  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-19
- fix strsep

* Fri Sep 28 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-18
- fix a ld.so bug with duplicate searchlists in l_scope
- fix erfcl(-inf)
- turn /usr/lib/librt.so into linker script

* Wed Sep 26 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-17
- fix a ld.so lookup bug after lots of dlopen calls
- fix CMSG_DATA for non-gcc non-ISOC99 compilers (#53984)
- prelinking support for Sparc64

* Fri Sep 21 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-16
- update from CVS to fix DT_SYMBOLIC
- prelinking support for Alpha and Sparc

* Tue Sep 18 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-15
- update from CVS
  - linuxthreads now retries if -1/EINTR is returned from
    reading or writing to thread manager pipe (#43742)
- use DT_FILTER in librt.so (#53394)
  - update glibc prelink patch so that it handles filters
- fix timer_* with SIGEV_NONE (#53494)
- make glibc_post_upgrade work on PPC (patch from Franz Sirl)

* Mon Sep 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-14
- fix build on sparc32
- 2.2.4-13 build for some reason missed some locales
  on alpha/ia64

* Mon Sep  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-13
- fix iconvconfig

* Mon Sep  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-12
- add fam to /etc/rpc (#52863)
- fix <inttypes.h> for C++ (#52960)
- fix perror

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-11
- fix strnlen(x, -1)

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-10
- doh, <bits/libc-lock.h> should only define __libc_rwlock_t
  if __USE_UNIX98.

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-9
- fix bits/libc-lock.h so that gcc can compile
- fix s390 build

* Fri Aug 24 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-8
- kill stale library symlinks in ldconfig (#52350)
- fix inttypes.h for G++ < 3.0
- use DT_REL*COUNT

* Wed Aug 22 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-7
- fix strnlen on IA-64 (#50077)

* Thu Aug 16 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-6
- glibc 2.2.4 final
- fix -lpthread -static (#51672)

* Fri Aug 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-5
- doh, include libio/tst-swscanf.c

* Fri Aug 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-4
- don't crash on catclose(-1)
- fix wscanf %%[] handling
- fix return value from swprintf
- handle year + %%U/%%W week + week day in strptime

* Thu Aug  9 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-3
- update from CVS to
  - fix strcoll (#50548)
  - fix seekdir (#51132)
  - fix memusage (#50606)
- don't make gconv-modules.cache %%config file, just don't verify
  its content.

* Mon Aug  6 2001 Jakub Jelinek <jakub@redhat.com>
- fix strtod and *scanf (#50723, #50724)

* Sat Aug  4 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix iconv cache handling
- glibc should not own %%{_infodir}, %%{_mandir} nor %%{_mandir}/man3 (#50673)
- add gconv-modules.cache as emtpy config file (#50699)
- only run iconvconfig if /usr is mounted read-write (#50667)

* Wed Jul 25 2001 Jakub Jelinek <jakub@redhat.com>
- move iconvconfig from glibc-common into glibc subpackage,
  call it from glibc_post_upgrade instead of common's post.

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com>
- turn off debugging printouts in iconvconfig
- update from CVS
  - fix IA-32 makecontext
  - make fflush(0) thread-safe (#46446)

* Mon Jul 23 2001 Jakub Jelinek <jakub@redhat.com>
- adjust prelinking DT_* and SHT_* values in elf.h
- update from CVS
  - iconv cache
  - make iconv work in SUID/SGID programs (#34611)

* Fri Jul 20 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - kill non-pic code in libm.so
  - fix getdate
  - fix some locales (#49402)
- rebuilt with binutils-2.11.90.0.8-5 to place .interp section
  properly in libBrokenLocale.so, libNoVersion.so and libanl.so
- add floating stacks on IA-64, Alpha, Sparc (#49308)

* Mon Jul 16 2001 Jakub Jelinek <jakub@redhat.com>
- make /lib/i686 directory owned by glibc*.i686.rpm

* Mon Jul  9 2001 Jakub Jelinek <jakub@redhat.com>
- remove rquota.[hx] headers which are now provided by quota (#47141)
- add prelinking patch

* Thu Jul  5 2001 Jakub Jelinek <jakub@redhat.com>
- require sh-utils for nscd

* Mon Jun 25 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS (#43681, #43350, #44663, #45685)
- fix ro_RO bug (#44644)

* Wed Jun  6 2001 Jakub Jelinek <jakub@redhat.com>
- fix a bunch of math bugs (#43210, #43345, #43346, #43347, #43348, #43355)
- make rpc headers -ansi compilable (#42390)
- remove alphaev6 optimized memcpy, since there are still far too many
  broken apps which call memcpy where they should call memmove
- update from CVS to (among other things):
  - fix tanhl bug (#43352)

* Tue May 22 2001 Jakub Jelinek <jakub@redhat.com>
- fix #include <signal.h> with -D_XOPEN_SOURCE=500 on ia64 (#35968)
- fix a dlclose reldeps handling bug
- some more profiling fixes
- fix tgmath.h

* Thu May 17 2001 Jakub Jelinek <jakub@redhat.com>
- make ldconfig more quiet
- fix LD_PROFILE on i686 (#41030)

* Wed May 16 2001 Jakub Jelinek <jakub@redhat.com>
- fix the hardlink program, so that it really catches all files with
  identical content
- add a s390x clone fix
- fix rpc for non-threaded apps using svc_fdset and similar variables (#40409)
- fix nss compatibility DSO versions for alphaev6
- add a hardlink program instead of the shell 3x for plus cmp -s/link
  which takes a lot of time during build
- rework BuildPreReq and Conflicts with gcc, so that
  it applies only where it has to

* Fri May 11 2001 Jakub Jelinek <jakub@redhat.com>
- fix locale name of ja_JP in UTF-8 (#39783)
- fix re_search_2 (#40244)
- fix memusage script (#39138, #39823)
- fix dlsym(RTLD_NEXT, ) from main program (#39803)
- fix xtrace script (#39609)
- make glibc conflict with glibc-devel 2.2.2 and below (to make sure
  libc_nonshared.a has atexit)
- fix getconf LFS_CFLAGS on 64bitters
- recompile with gcc-2.96-84 or above to fix binary compatibility problem
  with __frame_state_for function (#37933)

* Fri Apr 27 2001 Jakub Jelinek <jakub@redhat.com>
- glibc 2.2.3 release
  - fix strcoll (#36539)
- add BuildPreReqs (#36378)

* Wed Apr 25 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Fri Apr 20 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix sparc64, ia64
  - fix some locale syntax errors (#35982)

* Wed Apr 18 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Wed Apr 11 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Fri Apr  6 2001 Jakub Jelinek <jakub@redhat.com>
- support even 2.4.0 kernels on ia64, sparc64 and s390x
- include UTF-8 locales
- make gconv-modules %%config(noreplace)

* Fri Mar 23 2001 Jakub Jelinek <jakub@redhat.com>
- back out sunrpc changes

* Wed Mar 21 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix ia64 build
  - fix pthread_getattr_np

* Fri Mar 16 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - run atexit() registered functions at dlclose time if they are in shared
    libraries (#28625)
  - add pthread_getattr_np API to make JVM folks happy

* Wed Mar 14 2001 Jakub Jelinek <jakub@redhat.com>
- require 2.4.1 instead of 2.4.0 on platforms where it required 2.4 kernel
- fix ldd behaviour on unresolved symbols
- remove nonsensical ldconfig warning, update osversion for the most
  recent library with the same soname in the same directory instead (#31703)
- apply selected patches from CVS
- s390x spec file changes from Florian La Roche

* Wed Mar  7 2001 Jakub Jelinek <jakub@redhat.com>
- fix gencat (#30894)
- fix ldconfig changes from yesterday, fix LD_ASSUME_KERNEL handling

* Tue Mar  6 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
- make pthread_attr_setstacksize consistent before and after pthread manager
  is started (#28194)
- pass back struct sigcontext from pthread signal wrapper (on ia32 only so
  far, #28493)
- on i686 ship both --enable-kernel 2.2.5 and 2.4.0 libc/libm/libpthread,
  make ld.so pick the right one

* Sat Feb 17 2001 Preston Brown <pbrown@redhat.com>
- glib-common doesn't require glibc, until we can figure out how to get out of dependency hell.

* Sat Feb 17 2001 Jakub Jelinek <jakub@redhat.com>
- make glibc require particular version of glibc-common
  and glibc-common prerequire glibc.

* Fri Feb 16 2001 Jakub Jelinek <jakub@redhat.com>
- glibc 2.2.2 release
  - fix regex REG_ICASE bug seen in ksymoops

* Sat Feb 10 2001 Jakub Jelinek <jakub@redhat.com>
- fix regexec leaking memory (#26864)

* Fri Feb  9 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix ia64 build with gnupro
  - make regex 64bit clean
  - fix tgmath make check failures on alpha

* Tue Feb  6 2001 Jakub Jelinek <jakub@redhat.com>
- update again for ia64 DF_1_INITFIRST

* Fri Feb  2 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix getaddrinfo (#25437)
  - support DF_1_INITFIRST (#25029)

* Wed Jan 24 2001 Jakub Jelinek <jakub@redhat.com>
- build all auxiliary arches with --enablekernel 2.4.0, those wanting
  to run 2.2 kernels can downgrade to the base architecture glibc.

* Sat Jan 20 2001 Jakub Jelinek <jakub@redhat.com>
- remove %%lang() flags from %%{_prefix}/lib/locale files temporarily

* Sun Jan 14 2001 Jakub Jelinek <jakub@redhat.com>
- update to 2.2.1 final
  - fix a pthread_kill_other_threads_np breakage (#23966)
  - make static binaries using dlopen work on ia64 again
- fix a typo in glibc-common group

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- devel requires glibc = %%{version}
- noreplace /etc/nscd.conf

* Wed Jan 10 2001 Jakub Jelinek <jakub@redhat.com>
- some more security fixes:
  - don't look up LD_PRELOAD libs in cache for SUID apps
    (because that bypasses SUID bit checking on the library)
  - place output files for profiling SUID apps into /var/profile,
    use O_NOFOLLOW for them
  - add checks for $MEMUSAGE_OUTPUT and $SEGFAULT_OUTPUT_NAME
- hardlink identical locale files together
- add %%lang() tags to locale stuff
- remove ko_KR.utf8 for now, it is provided by locale-utf8 package

* Mon Jan  8 2001 Jakub Jelinek <jakub@redhat.com>
- add glibc-common subpackage
- fix alphaev6 memcpy (#22494)
- fix sys/cdefs.h (#22908)
- don't define stdin/stdout/stderr as macros for -traditional (#22913)
- work around a bug in IBM JDK (#22932, #23012)
- fix pmap_unset when network is down (#23176)
- move nscd in rc.d before netfs on shutdown
- fix $RESOLV_HOST_CONF in SUID apps (#23562)

* Fri Dec 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix ftw and nftw

* Wed Dec 13 2000 Jakub Jelinek <jakub@redhat.com>
- fix fcvt (#22184)
- ldd /lib/ld-linux.so.2 is not crashing any longer again (#22197)
- fix gencat

* Mon Dec 11 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha htonl and alphaev6 stpcpy

* Sat Dec  9 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to:
  - fix getnameinfo (#21934)
  - don't stomp on memory in rpath handling (#21544)
  - fix setlocale (#21507)
- fix libNoVersion.so.1 loading code (#21579)
- use auxarches define in spec file for auxiliary
  architectures (#21219)
- remove /usr/share directory from filelist (#21218)

* Sun Nov 19 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix getaddrinfo

* Fri Nov 17 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix freopen
- remove all alpha workarounds, not needed anymore

* Wed Nov 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix dladdr bug on alpha/sparc32/sparc64
- fix Makefiles so that they run static tests properly

* Tue Nov 14 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix ldconfig

* Thu Nov  9 2000 Jakub Jelinek <jakub@redhat.com>
- update to glibc 2.2 release

* Mon Nov  6 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to:
  - export __sysconf@@GLIBC_2.2 (#20417)

* Fri Nov  3 2000 Jakub Jelinek <jakub@redhat.com>
- merge to 2.1.97

* Mon Oct 30 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS, including:
  - fix WORD_BIT/LONG_BIT definition in limits.h (#19088)
  - fix hesiod (#19375)
  - set LC_MESSAGES in zic/zdump for proper error message output (#19495)
  - fix LFS fcntl when used with non-LFS aware kernels (#19730)

* Thu Oct 19 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha semctl (#19199)
- update to CVS, including:
  - fix glibc headers for Compaq non-gcc compilers
  - fix locale alias handling code (#18832)
  - fix rexec on little endian machines (#18886)
- started writing changelog again

* Thu Aug 10 2000 Adrian Havill <havill@redhat.com>
- added ja ujis alias for backwards compatibility
