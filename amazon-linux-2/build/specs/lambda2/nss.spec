%global nspr_version 4.21.0
%global nss_util_version 3.44.0
%global nss_util_build -3
# adjust to the version that gets submitted for FIPS validation
%global nss_softokn_fips_version 3.44.0
%global nss_softokn_version 3.44.0
# Attention: Separate softokn versions for build and runtime.
%global runtime_required_softokn_build_version -1
# Building NSS doesn't require the same version of softokn built for runtime.
%global build_required_softokn_build_version -1
%global nss_version 3.44.0

%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global allTools "certutil cmsutil crlutil derdump modutil nss-policy-check pk12util pp signtool signver ssltap vfychain vfyserv"

# The timestamp of our downstream manual pages, e.g., nss-config.1
%global manual_date "Nov 13 2013"

# The upstream omits the trailing ".0", while we need it for
# consistency with the pkg-config version:
# https://bugzilla.redhat.com/show_bug.cgi?id=1578106
%{lua:
rpm.define(string.format("nss_archive_version %s",
           string.gsub(rpm.expand("%nss_version"), "(.*)%.0$", "%1")))
}

# solution taken from icedtea-web.spec
%define multilib_arches ppc64 s390x sparc64 x86_64
%ifarch %{multilib_arches}
%define alt_ckbi  libnssckbi.so.%{_arch}
%else
%define alt_ckbi  libnssckbi.so
%endif

# Define if using a source archive like "nss-version.with.ckbi.version".
# To "disable", add "#" to start of line, AND a space after "%".
#% define nss_ckbi_suffix .with.ckbi.1.93

%bcond_without tests

Summary:          Network Security Services
Name:             nss
Version:          %{nss_version}
Release: 4%{?dist}.0.2
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}%{nss_util_build}
# TODO: revert to same version as nss once we are done with the merge
Requires:         nss-softokn%{_isa} >= %{nss_softokn_version}%{runtime_required_softokn_build_version}
# Requires:         nss-system-init
Requires(post):   /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}
# TODO: revert to same version as nss once we are done with the merge
# Using '>=' but on RHEL the requires should be '='
BuildRequires:    nss-softokn-devel >= %{nss_softokn_version}%{build_required_softokn_build_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}%{nss_util_build}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl
BuildRequires:    xmlto

# nss-pem used to be bundled with the nss package on Fedora -- make sure that
# programs relying on that continue to work until they are fixed to require
# nss-pem instead.  Once all of them are fixed, the following line can be
# removed.  See https://bugzilla.redhat.com/1346806 for details.
Requires:         nss-pem%{?_isa}

%if %{defined nss_ckbi_suffix}
%define full_nss_version %{version}%{nss_ckbi_suffix}
%else
%define full_nss_version %{version}
%endif

Source0:          %{name}-%{nss_archive_version}.tar.gz
Source1:          nss.pc.in
Source2:          nss-config.in
Source3:          blank-cert8.db
Source4:          blank-key3.db
Source5:          blank-secmod.db
Source6:          blank-cert9.db
Source7:          blank-key4.db
Source8:          system-pkcs11.txt
Source9:          setup-nsssysinit.sh
Source10:         PayPalEE.cert
Source17:         TestCA.ca.cert
Source18:         TestUser50.cert
Source19:         TestUser51.cert
Source20:         nss-config.xml
Source21:         setup-nsssysinit.xml
Source22:         pkcs11.txt.xml
Source23:         cert8.db.xml
Source24:         cert9.db.xml
Source25:         key3.db.xml
Source26:         key4.db.xml
Source27:         secmod.db.xml
Source30:         PayPalRootCA.cert
Source31:         PayPalICA.cert
Source32:         nss-rhel7.config
Source33:         TestOldCA.p12

Patch2:           add-relro-linker-option.patch
Patch3:           renegotiate-transitional.patch
Patch16:          nss-539183.patch
# TODO: Remove this patch when the ocsp test are fixed
Patch40:          nss-3.14.0.0-disble-ocsp-test.patch
# Fedora / RHEL-only patch, the templates directory was originally introduced to support mod_revocator
Patch47:          utilwrap-include-templates.patch
# TODO remove when we switch to building nss without softoken
Patch49:          nss-skip-bltest-and-fipstest.patch
# This patch uses the gcc-iquote dir option documented at
# http://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
# to place the in-tree directories at the head of the list of list of directories
# to be searched for for header files. This ensures a build even when system 
# headers are older. Such is the case when starting an update with API changes or even private export changes.
# Once the buildroot aha been bootstrapped the patch may be removed but it doesn't hurt to keep it.
Patch50:          iquote.patch
Patch52:          Bug-1001841-disable-sslv2-libssl.patch
Patch53:          Bug-1001841-disable-sslv2-tests.patch
# rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1026677
Patch56:          p-ignore-setpolicy.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=943144
Patch62: nss-fix-deadlock-squash.patch
Patch100: fix-min-library-version-in-SSLVersionRange.patch
Patch108: nss-sni-c-v-fix.patch
Patch123: nss-skip-util-gtest.patch
Patch126: nss-reorder-cipher-suites.patch
Patch127: nss-disable-cipher-suites.patch
Patch130: nss-reorder-cipher-suites-gtests.patch
# To revert the change in:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1377940
Patch136: nss-sql-default.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=1453408
Patch139: nss-modutil-skip-changepw-fips.patch
# Work around for yum
# https://bugzilla.redhat.com/show_bug.cgi?id=1469526
Patch141: nss-sysinit-getenv.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=1542207
Patch147: nss-dsa-policy.patch
# To revert the change in:
# https://bugzilla.mozilla.org/show_bug.cgi?id=818686
Patch148: nss-sysinit-userdb.patch
# Disable nss-sysinit test which is sorely to test the above change
Patch149: nss-skip-sysinit-gtests.patch
# Enable SSLv2 compatible ClientHello, disabled in the change:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1483128
Patch150: nss-ssl2-compatible-client-hello.patch
# TLS 1.3 currently doesn't work under FIPS mode:
# https://bugzilla.redhat.com/show_bug.cgi?id=1710372
Patch151: nss-skip-tls13-fips-tests.sh
# For backward compatibility: make -V "ssl3:" continue working, while
# the minimum version is clamped to tls1.0
Patch152: nss-version-range-set.patch
# TLS 1.3 currently doesn't work under FIPS mode:
# https://bugzilla.redhat.com/show_bug.cgi?id=1710372
Patch153: nss-fips-disable-tls13.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=1552208
Patch154: nss-disable-pkcs1-sigalgs-tls13.patch
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=1553443
Patch155: nss-post-handshake-auth-with-tickets.patch
# https://bugzilla.mozilla.org/show_bug.cgi?id=1473806
Patch156: nss-fix-public-key-from-priv.patch
Patch157: nss-add-ipsec-usage-to-manpage.patch


Prefix: %{_prefix}

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Group:            System Environment/Base
Requires:         %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.

%package sysinit
Summary:          System NSS Initialization
Group:            System Environment/Base
# providing nss-system-init without version so that it can
# be replaced by a better one, e.g. supplied by the os vendor
Provides:         nss-system-init
Requires:         nss = %{version}-%{release}
Requires(post):   coreutils
Prefix: %{_prefix}

%description sysinit
Default Operating System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.


%prep
%setup -q -n %{name}-%{nss_archive_version}
%{__cp} %{SOURCE10} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE17} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE18} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE19} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE30} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE31} -f ./nss/tests/libpkix/certs
%{__cp} %{SOURCE33} -f ./nss/tests/tools

%patch2 -p0 -b .relro
%patch3 -p0 -b .transitional
%patch16 -p0 -b .539183
%patch40 -p0 -b .noocsptest
%patch47 -p0 -b .templates
%patch49 -p0 -b .skipthem
%patch50 -p0 -b .iquote
pushd nss
%patch52 -p1 -b .disableSSL2libssl
%patch53 -p1 -b .disableSSL2tests
%patch56 -p1 -b .1026677_ignore_set_policy
%patch62 -p1 -b .fix_deadlock
%patch100 -p0 -b .1171318
popd
%patch108 -p0 -b .sni_c_v_fix
pushd nss
%patch123 -p1 -b .skip-util-gtests
%patch126 -p1 -b .reorder-cipher-suites
%patch127 -p1 -b .disable-cipher-suites
%patch130 -p1 -b .reorder-cipher-suites-gtests
%patch136 -p1 -R -b .sql-default
%patch139 -p1 -b .modutil-skip-changepw-fips
%patch148 -R -p1 -b .sysinit-userdb
%patch141 -p1 -b .sysinit-getenv
%patch147 -p1 -b .dsa-policy
%patch149 -p1 -b .skip-sysinit-gtests
%patch150 -p1 -b .ssl2hello
%patch151 -p1 -b .skip-tls13-fips-mode
%patch152 -p1 -b .version-range-set
%patch153 -p1 -b .fips-disable-tls13
%patch154 -p1 -b .disable-pkcs1-sigalgs-tls13
%patch155 -p1 -b .post-handshake-auth-with-tickets
popd
%patch156 -p1 -b .pub-priv-mechs
%patch157 -p1 -b .ipsec-usage

#########################################################
# Higher-level libraries and test tools need access to
# module-private headers from util, freebl, and softoken
# until fixed upstream we must copy some headers locally
#########################################################

# Copying these header until the upstream bug is accepted
# Upstream https://bugzilla.mozilla.org/show_bug.cgi?id=820207
%{__cp} ./nss/lib/softoken/lowkeyi.h ./nss/cmd/rsaperf
%{__cp} ./nss/lib/softoken/lowkeyti.h ./nss/cmd/rsaperf

# Before removing util directory we must save verref.h
# as it will be needed later during the build phase.
%{__mv} ./nss/lib/util/verref.h ./nss/verref.h

##### Remove util/freebl/softoken and low level tools
######## Remove freebl, softoken and util
%{__rm} -rf ./nss/lib/freebl
%{__rm} -rf ./nss/lib/softoken
%{__rm} -rf ./nss/lib/util
######## Remove nss-softokn test tools as we already ran
# the cipher test suite as part of the nss-softokn build
%{__rm} -rf ./nss/cmd/bltest
%{__rm} -rf ./nss/cmd/fipstest
%{__rm} -rf ./nss/cmd/rsaperf_low

pushd nss/tests/ssl
# Create versions of sslcov.txt and sslstress.txt that disable tests
# for SSL2 and EXPORT ciphers.
cat sslcov.txt| sed -r "s/^([^#].*EXPORT|^[^#].*SSL2)/#disabled \1/" > sslcov.noSSL2orExport.txt
cat sslstress.txt| sed -r "s/^([^#].*EXPORT|^[^#].*SSL2)/#disabled \1/" > sslstress.noSSL2orExport.txt
popd

%build

export NSS_NO_SSL2=1

FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

# Enable compiler optimizations and disable debugging code
export BUILD_OPT=1

# Uncomment to disable optimizations
# RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g' -e 's/ -Wp,-D_FORTIFY_SOURCE=2//g'`
# export RPM_OPT_FLAGS

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS

export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=/usr/lib64

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

export NSSUTIL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
export NSSUTIL_LIB_DIR=/usr/lib64

export FREEBL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-softokn | sed 's/-I//'`
export FREEBL_LIB_DIR=/usr/lib64
export USE_SYSTEM_FREEBL=1
# FIXME choose one or the other style and submit a patch upstream
# wtc has suggested using NSS_USE_SYSTEM_FREEBL
export NSS_USE_SYSTEM_FREEBL=1

export FREEBL_LIBS=`/usr/bin/pkg-config --libs nss-softokn`

export SOFTOKEN_LIB_DIR=/usr/lib64
# use the system ones
export USE_SYSTEM_NSSUTIL=1
export USE_SYSTEM_SOFTOKEN=1

# tell the upstream build system what we are doing
export NSS_BUILD_WITHOUT_SOFTOKEN=1

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE

export NSS_ALLOW_SSLKEYLOGFILE=1

%ifnarch noarch
%if 0%{__isa_bits} == 64
USE_64=1
export USE_64
%endif
%endif

# uncomment if the iquote patch is activated
export IN_TREE_FREEBL_HEADERS_FIRST=1

##### phase 2: build the rest of nss
export NSS_BLTEST_NOT_AVAILABLE=1

export NSS_FORCE_FIPS=1

%{__make} -C ./nss/coreconf
%{__make} -C ./nss/lib/dbm

# Set the policy file location
# if set NSS will always check for the policy file and load if it exists
export POLICY_FILE="nss-rhel7.config"
# location of the policy file
export POLICY_PATH="/etc/pki/nss-legacy"

# nss/nssinit.c, ssl/sslcon.c, smime/smimeutil.c and ckfw/builtins/binst.c
# need nss/lib/util/verref.h which  is exported privately,
# copy the one we saved during prep so it they can find it.
%{__mkdir_p} ./dist/private/nss
%{__mv} ./nss/verref.h ./dist/private/nss/verref.h

%{__make} -C ./nss
unset NSS_BLTEST_NOT_AVAILABLE

# build the man pages clean
pushd ./nss/doc
rm -rf ./nroff
%{__make} clean
echo -n %{manual_date} > date.xml
echo -n %{version} > version.xml
%{__make}
popd

# and copy them to the dist directory for %%install to find them
%{__mkdir_p} ./dist/doc/nroff
%{__cp} ./nss/doc/nroff/* ./dist/doc/nroff

# Set up our package file
# The nspr_version and nss_{util|softokn}_version globals used
# here match the ones nss has for its Requires. 
# Using the current %%{nss_softokn_version} for fedora again
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{nss_softokn_version},g" > \
                          ./dist/pkgconfig/nss.pc

NSS_VMAJOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

export NSS_VMAJOR
export NSS_VMINOR
export NSS_VPATCH

%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./dist/pkgconfig/nss-config

chmod 755 ./dist/pkgconfig/nss-config

%{__cat} %{SOURCE9} > ./dist/pkgconfig/setup-nsssysinit.sh
chmod 755 ./dist/pkgconfig/setup-nsssysinit.sh

%{__cp} ./nss/lib/ckfw/nssck.api ./dist/private/nss/

echo -n %{manual_date} > date.xml
echo -n %{version} > version.xml

# configuration files and setup script
for m in %{SOURCE20} %{SOURCE21} %{SOURCE22}; do
  cp ${m} .
done
for m in nss-config.xml setup-nsssysinit.xml pkcs11.txt.xml; do
  xmlto man ${m}
done

# nss databases considered to be configuration files
for m in %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27}; do
  cp ${m} .
done
for m in cert8.db.xml cert9.db.xml key3.db.xml key4.db.xml secmod.db.xml; do
  xmlto man ${m}
done
 

%install

%{__rm} -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}

touch $RPM_BUILD_ROOT%{_libdir}/libnssckbi.so
%{__install} -p -m 755 dist/*.OBJ/lib/libnssckbi.so $RPM_BUILD_ROOT/%{_libdir}/nss/libnssckbi.so

# Copy the binary libraries we want
for file in libnss3.so libnsssysinit.so libsmime3.so libssl3.so
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Install the empty NSS db files
# Legacy db
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
%{__install} -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
%{__install} -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
%{__install} -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.db
# Shared db
%{__install} -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert9.db
%{__install} -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key4.db
%{__install} -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/pkcs11.txt

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil nss-policy-check pk12util signver ssltap
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump listsuites ocspclnt pp selfserv signtool strsclnt symkeyutil tstclnt vfyserv vfychain
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the pkcs #11 configuration script
%{__install} -p -m 755 ./dist/pkgconfig/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh
# install a symbolic link to it, without the ".sh" suffix,
# that matches the man page documentation
ln -r -s -f $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/pki/nss-legacy
%{__install} -p -m 644 %{SOURCE32} $RPM_BUILD_ROOT%{_sysconfdir}/pki/nss-legacy/nss-rhel7.config

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/alternatives
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/alternatives

%post
# If we upgrade, and the shared filename is a regular file, then we must
# remove it, before we can install the alternatives symbolic link.
if [ $1 -gt 1 ] ; then
  # when upgrading or downgrading
  if ! test -L %{_libdir}/libnssckbi.so; then
    rm -f %{_libdir}/libnssckbi.so
  fi
fi
# Install the symbolic link
# FYI: Certain other packages use alternatives --set to enforce that the first
# installed package is preferred. We don't do that. Highest priority wins.
/usr/sbin/update-alternatives --altdir %{_sysconfdir}/alternatives --admindir %{_sharedstatedir}/alternatives --install %{_libdir}/libnssckbi.so \
  %{alt_ckbi} %{_libdir}/nss/libnssckbi.so 10
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
  # package removal
  /usr/sbin/update-alternatives --altdir %{_sysconfdir}/alternatives --admindir %{_sharedstatedir}/alternatives --remove %{alt_ckbi} %{_libdir}/nss/libnssckbi.so
else
  # upgrade or downgrade
  # If the new installed package uses a regular file (not a symblic link),
  # then cleanup the alternatives link.
  if ! test -L %{_libdir}/libnssckbi.so; then
    /usr/sbin/update-alternatives --altdir %{_sysconfdir}/alternatives --admindir %{_sharedstatedir}/alternatives --remove %{alt_ckbi} %{_libdir}/nss/libnssckbi.so
  fi
fi

%files
%defattr(-,root,root)
%{_libdir}/libnss3.so
%{_libdir}/libssl3.so
%{_libdir}/libsmime3.so
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/nss/libnssckbi.so
%dir %{_sysconfdir}/pki/nssdb
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert8.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key3.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/secmod.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert9.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key4.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/pkcs11.txt
%dir %{_sysconfdir}/pki/nss-legacy
%config(noreplace) %{_sysconfdir}/pki/nss-legacy/nss-rhel7.config
%dir %{_sysconfdir}/alternatives
%dir %{_sharedstatedir}/alternatives

%files sysinit
%defattr(-,root,root)
%{_libdir}/libnsssysinit.so
%{_bindir}/setup-nsssysinit.sh
# symbolic link to setup-nsssysinit.sh
%{_bindir}/setup-nsssysinit

%files tools
%defattr(-,root,root)
%{_bindir}/certutil
%{_bindir}/cmsutil
%{_bindir}/crlutil
%{_bindir}/modutil
%{_bindir}/nss-policy-check
%{_bindir}/pk12util
%{_bindir}/signver
%{_bindir}/ssltap
%{unsupported_tools_directory}/atob
%{unsupported_tools_directory}/btoa
%{unsupported_tools_directory}/derdump
%{unsupported_tools_directory}/listsuites
%{unsupported_tools_directory}/ocspclnt
%{unsupported_tools_directory}/pp
%{unsupported_tools_directory}/selfserv
%{unsupported_tools_directory}/signtool
%{unsupported_tools_directory}/strsclnt
%{unsupported_tools_directory}/symkeyutil
%{unsupported_tools_directory}/tstclnt
%{unsupported_tools_directory}/vfyserv
%{unsupported_tools_directory}/vfychain


%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Jun 5 2019 Bob Relyea <rrelyea@redhat.com> - 3.44.0-4
- Fix certutil man page
- Fix extracting a public key from a private key for dh, ec, and dsa

* Thu May 30 2019 Daiki Ueno <dueno@redhat.com> - 3.44.0-3
- Disable TLS 1.3 under FIPS mode
- Disable RSASSA-PKCS1-v1_5 in TLS 1.3
- Fix post-handshake auth transcript calculation if
  SSL_ENABLE_SESSION_TICKETS is set

* Thu May 16 2019 Daiki Ueno <dueno@redhat.com> - 3.44.0-2
- Skip sysinit gtests properly
- Fix shell syntax error in tests/ssl/ssl.sh
- Regenerate manual pages

* Wed May 15 2019 Daiki Ueno <dueno@redhat.com> - 3.44.0-1
- Rebase to NSS 3.44
- Restore fix-min-library-version-in-SSLVersionRange.patch to keep
  SSL3 supported in the code level while it is disabled by policy
- Skip TLS 1.3 tests under FIPS mode

* Fri May 10 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-9
- Ignore system policy when running %%check

* Fri May  3 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-8
- Fix policy string

* Fri Apr 26 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-7
- Don't override date in man-pages
- Revert the change to use XDG basedirs (mozilla#818686)
- Enable SSL2 compatible ClientHello by default
- Disable SSL3 and RC4 by default

* Mon Apr  8 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-6
- Make "-V ssl3:" option work with tools

* Fri Apr  5 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-5
- Fix regression in MD5 disablement

* Mon Apr 1 2019 Bob Relyea <rrelyea@redhat.com> - 3.43.0-4
- add certutil documentation

* Thu Mar 28 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-3
- Restore complete removal of SSLv2
- Disable SSLv3
- Move signtool to unsupported directory

* Mon Mar 25 2019 Bob Relyea <rrelyea@redhat.com> - 3.43.0-2
- Expand IPSEC usage to include ssl and email certs. Remove special
  processing of the usage based on the critical flag

* Thu Mar 21 2019 Daiki Ueno <dueno@redhat.com> - 3.43.0-1
- Rebase to NSS 3.43

* Mon Feb 25 2019 Bob Relyea <rrelyea@redhat.com> - 3.36.0-8.1
- move key on unwrap failure and retry.

* Mon Nov 12 2018 Bob Relyea <rrelyea@redhat.com> - 3.36.0-8
- Update the cert verify code to allow a new ipsec usage and follow RFC 4945

* Wed Aug 29 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-7
- Backport upstream fix for CVE-2018-12384
- Remove nss-lockcert-api-change.patch, which turned out to be a
  mistake (the symbol was not exported from libnss)

* Thu Apr 19 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-6
- Exercise SSL tests which only run under non-FIPS setting

* Wed Apr 18 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-5
- Restore CERT_LockCertTrust and CERT_UnlockCertTrust back in cert.h

* Fri Apr 13 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-4
- Work around modutil -changepw error if the old and new passwords are
  both empty in FIPS mode

* Tue Mar 27 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-3
- Decrease the iteration count of PKCS#12 for compatibility with Windows
- Fix deadlock when a token is re-inserted while a client process is running

* Mon Mar 12 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-2
- Set NSS_FORCE_FIPS=1 in %%build
- Revert the changes to tests assuming the default DB type

* Fri Mar  9 2018 Daiki Ueno <dueno@redhat.com> - 3.36.0-1
- Rebase to NSS 3.36

* Mon Jan 15 2018 Daiki Ueno <dueno@redhat.com> - 3.34.0-4
- Re-enable nss-is-token-present-race.patch

* Fri Jan  5 2018 Daiki Ueno <dueno@redhat.com> - 3.34.0-3
- Temporarily disable nss-is-token-present-race.patch

* Thu Jan  4 2018 Daiki Ueno <dueno@redhat.com> - 3.34.0-2
- Backport necessary changes from 3.35

* Fri Nov 24 2017 Daiki Ueno <dueno@redhat.com> - 3.34.0-1
- Rebase to NSS 3.34

* Mon Oct 30 2017 Daiki Ueno <dueno@redhat.com> - 3.34.0-0.1.beta1
- Rebase to NSS 3.34.BETA1

* Wed Oct 25 2017 Daiki Ueno <dueno@redhat.com> - 3.33.0-3
- Disable TLS 1.3

* Wed Oct 18 2017 Daiki Ueno <dueno@redhat.com> - 3.33.0-2
- Enable TLS 1.3

* Mon Oct 16 2017 Daiki Ueno <dueno@redhat.com> - 3.33.0-1
- Rebase to NSS 3.33
- Disable TLS 1.3, temporarily disable failing gtests (Skip13Variants)
- Temporarily disable race.patch and nss-3.16-token-init-race.patch,
  which causes a deadlock in newly added test cases
- Remove upstreamed patches: moz-1320932.patch,
  nss-tstclnt-optspec.patch,
  nss-1334976-1336487-1345083-ca-2.14.patch, nss-alert-handler.patch,
  nss-tools-sha256-default.patch, nss-is-token-present-race.patch,
  nss-pk12util.patch, nss-ssl3gthr.patch, and nss-transcript.patch

* Mon Oct 16 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-14
- Add backward compatibility to pk12util regarding faulty PBES2 AES encryption

* Mon Oct 16 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-13
- Update iquote.patch to prefer nss.h from the source

* Mon Oct 16 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-12
- Add backward compatibility to pk12util regarding password encoding

* Thu Aug 10 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-11
- Backport patch to simplify transcript calculation for CertificateVerify
- Enable TLS 1.3 and RSA-PSS
- Disable some upstream tests failing due to downstream ciphersuites changes

* Thu Jul 13 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-10
- Work around yum crash due to new NSPR symbol being used in nss-sysinit,
  patch by Kai Engert

* Fri Jun  2 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-9
- Fix typo in nss-sni-c-v-fix.patch

* Fri May  5 2017 Kai Engert <kaie@redhat.com> - 3.28.4-8
- Include CKBI 2.14 and updated CA constraints from NSS 3.28.5

* Fri May  5 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-7
- Update nss-pk12util.patch to include fix from mozbz#1353724.

* Wed May  3 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-6
- Update nss-alert-handler.patch with the upstream fix from mozbz#1360207.

* Fri Apr 28 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-5
- Fix zero-length record treatment for stream ciphers and SSLv2

* Thu Apr 27 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-4
- Correctly set policy file location when building

* Wed Apr 26 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-3
- Reorder ChaCha20-Poly1305 cipher suites, as suggested in:
  https://bugzilla.redhat.com/show_bug.cgi?id=1373158#c9

* Thu Apr 20 2017 Daiki Ueno <dueno@redhat.com> - 3.28.4-2
- Rebase to NSS 3.28.4
- Update nss-pk12util.patch with backport of mozbz#1353325

* Thu Mar 16 2017 Daiki Ueno <dueno@redhat.com> - 3.28.3-5
- Switch default hash algorithm used by tools from SHA-1 to SHA-256
- Avoid race condition in nssSlot_IsTokenPresent()
- Enable SHA-2 and AES in pk12util
- Disable RSA-PSS for now

* Fri Mar 10 2017 Daiki Ueno <dueno@redhat.com> - 3.28.3-4
- Utilize CKA_NSS_MOZILLA_CA_POLICY attribute, patch by Kai Engert
- Backport changes adding SSL alert callbacks from upstream
- Add nss-check-policy-file.patch from Fedora
- Install policy config in /etc/pki/nss-legacy/nss-rhel7.config

* Mon Mar  6 2017 Daiki Ueno <dueno@redhat.com> - 3.28.3-3
- Make sure 32bit nss-pem always be installed with 32bit nss in
  multlib environment, patch by Kamil Dudka
- Enable new algorithms supported by the new nss-softokn

* Mon Mar  6 2017 Daiki Ueno <dueno@redhat.com> - 3.28.3-2
- Rebase to NSS 3.28.3
- Bump required version of nss-softokn

* Wed Feb 15 2017 Daiki Ueno <dueno@redhat.com> - 3.28.2-3
- Remove %%nss_cycles setting, which was also mistakenly added
- Re-enable BUILD_OPT, mistakenly disabled in the previous build
- Prevent ABI incompatibilty of SECKEYECPublicKey
- Disable TLS_ECDHE_{RSA,ECDSA}_WITH_AES_128_CBC_SHA256 by default
- Enable 4 AES_256_GCM_SHA384 ciphersuites, enabled by the downstream
  patch in the previous release
- Fix crash with tstclnt -W
- Always enable gtests for supported features
- Add patch to fix bash syntax error in tests/ssl.sh
- Build with support for SSLKEYLOGFILE
- Disable the use of RSA-PSS with SSL/TLS

* Tue Feb 14 2017 Daiki Ueno <dueno@redhat.com> - 3.28.2-2
- Decouple nss-pem from the nss package
- Resolves: #1316546

* Mon Feb 13 2017 Daiki Ueno <dueno@redhat.com> - 3.28.2-1.1
- Remove mistakenly added R: nss-pem

* Fri Feb 10 2017 Daiki Ueno <dueno@redhat.com> - 3.28.2-1.0
- Rebase to NSS 3.28.2
- Remove NSS_ENABLE_ECC and NSS_ECC_MORE_THAN_SUITE_B setting, which
  is no-op now
- Enable gtests when requested
- Remove nss-646045.patch and fix-nss-test-filtering.patch, which are
  not necessary
- Remove sslauth-no-v2.patch and
  nss-sslstress-txt-ssl3-lower-value-in-range.patch, as SSLv2 is
  already disabled in upstream
- Remove ssl-server-min-key-sizes.patch, as we decided to support DH
  key size greater than 1023 bits
- Remove local patches for SHA384 cipher suites (now supported in
  upstream): dhe-sha384-dss-support.patch,
  client_auth_for_sha384_prf_support.patch,
  nss-fix-client-auth-init-hashes.patch, nss-map-oid-to-hashalg.patch,
  nss-enable-384-cipher-tests.patch, nss-fix-signature-and-hash.patch,
  fix-allowed-sig-alg.patch, tests-extra.patch
- Remove upstreamed patches: rh1238290.patch,
  fix-reuse-of-session-cache-entry.patch, flexible-certverify.patch,
  call-restartmodules-in-nssinit.patch

* Wed Oct 26 2016 Daiki Ueno <dueno@redhat.com> - 3.21.3-1
- Rebase to NSS 3.21.3
- Resolves: #1383887

* Thu Jun 30 2016 Kai Engert <kaie@redhat.com> - 3.21.0-17
- remove additional false duplicates from sha384 downstream patches

* Tue Jun 28 2016 Kai Engert <kaie@redhat.com> - 3.21.0-16
- enable ssl_gtests (without extended master secret tests), Bug 1298692
- call SECMOD_RestartModules in nss_Init, Bug 1317691

* Fri Jun 17 2016 Kai Engert <kaie@redhat.com> - 3.21.0-15
- escape all percent characters in all changelog comments

* Fri Jun 17 2016 Kai Engert <kaie@redhat.com> - 3.21.0-14
- Support TLS 1.2 certificate_verify hashes other than PRF,
  backported fix from NSS 3.25 (upstream bug 1179338).

* Mon May 23 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-13
- Fix reuse of session cache entry
- Resolves: Bug 1241172 - Certificate verification fails with multiple https urls

* Wed Apr 20 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-12
- Fix a flaw in %%check for nss not building on arm
- Resolves: Bug 1200856

* Wed Apr 20 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-11
- Cleanup: Remove unnecessary %%posttrans script from nss.spec
- Resolves: Bug 1174201

* Wed Apr 20 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-10
- Merge fixes from the rhel-7.2 branch
- Fix a bogus %%changelog entry
- Resolves: Bug 1297941

* Fri Apr 15 2016 Kai Engert <kaie@redhat.com> - 3.21.0-9
- Rebuild to require the latest nss-util build and nss-softokn build.

* Mon Apr 11 2016 Kai Engert <kaie@redhat.com> - 3.21.0-8
- Update the minimum nss-softokn build required at runtime.

* Mon Apr 04 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-7
- Delete duplicates from one table

* Tue Mar 29 2016 Kai Engert <kaie@redhat.com> - 3.21.0-6
- Fix missing support for sha384/dsa in certificate_request

* Wed Mar 23 2016 Kai Engert <kaie@redhat.com> - 3.21.0-5
- Merge fixes from the rhel-7.2 branch
- Fix the SigAlgs sent in certificate_request
- Ensure all ssl.sh tests are executed
- Update sslauth test patch to run additional tests

* Fri Feb 26 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-2
- Fix sha384 support and testing patches

* Wed Feb 17 2016 Elio Maldonado <emaldona@redhat.com> - 3.21.0-1
- Rebase to NSS-3.21

* Tue Dec 15 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-19
- Prevent TLS 1.2 Transcript Collision attacks against MD5 in key exchange protocol
- Fix a mockbuild reported bad %%if condition when using the __isa_bits macro instead of list of 64-bit architectures
- Change the test to %%if 0%%{__isa_bits} == 64 as required for building the srpm which is noarch
- Resolves: Bug 1289884

* Wed Oct 21 2015 Kai Engert <kaie@redhat.com> - 3.19.1-18
- Rebuild against updated NSPR

* Thu Sep 03 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-17
- Change the required_softokn_build_version back to -13
- Ensure we use nss-softokn-3.16.2.3-13.el7_1

* Thu Sep 03 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-16
- Fix check for public key size of DSA certificates
- Use size of prime P not the size of dsa.publicValue

* Mon Aug 31 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-15
- Reorder the cipher suites and enable two more by default

* Sun Aug 30 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-14
- Update the required_softokn_build_version to -14
- Add references to bugs filed upstream for new patches
- Merge ocsp stapling and sslauth sni tests patches into one

* Sat Aug 29 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-13
- Reorder the cipher suites and enable two more by default
- Fix some of the ssauth sni and ocsp stapling tests

* Thu Aug 27 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-12
- Support TLS > 1.0 by support while still allowing to connect to SSL3 only servers
- Enable ECDSA cipher suites by default, a subset of the ones requested

* Wed Aug 26 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-11
- Support TLS > 1.0 by support while still allowing to connect to SSL3 only servers

* Mon Aug 17 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-10
- Fix to correctly report integrity mechanism for TLS_RSA_WITH_AES_256_GCM_SHA384

* Mon Aug 10 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-9
- Fix checks to skip ssl2/export cipher suites tests to not skip needed tests
- Fix libssl ssl2/export disabling patch to handle NULL cipher cases
- Enable additional cipher suites by default

* Thu Jul 16 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-8
- Add links to filed upstream bugs to better track patches in spec file

* Tue Jul 07 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-7
- Package listsuites as part of the unsupported tools

* Thu Jul 02 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-6
- Bump the release tag

* Mon Jun 29 2015 Kai Engert <kaie@redhat.com> - 3.19.1-5
- Incremental patches to fix SSL/TLS test suite execution,
  fix the earlier SHA384 patch, and inform clients to use SHA384 with
  certificate_verify if required by NSS.

* Thu Jun 18 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-4
- Add support for sha384 tls cipher suites
- Add support for server-side hde key exchange
- Add support for DSS+SHA256 ciphersuites

* Wed Jun 10 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-3
- Reenable a patch that had been mistakenly disabled

* Wed Jun 10 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-2
- Build against nss-softokn-3.16.2.3-9

* Fri Jun 05 2015 Elio Maldonado <emaldona@redhat.com> - 3.19.1-1
- Rebase to nss-3.19.1
- Resolves: Bug 1228913 - Rebase to nss-3.19.1 for CVE-2015-4000 [RHEL-7.1]

* Tue Apr 28 2015 Kai Engert <kaie@redhat.com> - 3.18.0-6
- Backport mozbz#1155922 to support SHA512 signatures with TLS 1.2

* Thu Apr 23 2015 Kai Engert <kaie@redhat.com> - 3.18.0-5
- Update to CKBI 2.4 from NSS 3.18.1 (the only change in NSS 3.18.1)

* Fri Apr 17 2015 Elio Maldonado <emaldona@redhat.com> - 3.18.0-4
- Update and reeneable nss-646045.patch on account of the rebase
- Resolves: Bug 1200898 - Rebase nss to 3.18 for Firefox 38 ESR [RHEL7.1]

* Tue Apr 14 2015 Elio Maldonado <emaldona@redhat.com> - 3.18.0-3
- Fix shell syntax error on nss/tests/all.sh
- Resolves: Bug 1200898 - Rebase nss to 3.18 for Firefox 38 ESR [RHEL7.1]

* Fri Apr 10 2015 Elio Maldonado <emaldona@redhat.com> - 3.18.0-2
- Replace expired PayPal test certificate that breaks the build
- Resolves: Bug 1200898 - Rebase nss to 3.18 for Firefox 38 ESR [RHEL7.1]

* Mon Mar 30 2015 Elio Maldonado <emaldona@redhat.com> - 3.18.0-1
- Resolves: Bug 1200898 - Rebase nss to 3.18 for Firefox 38 ESR [RHEL7.1]

* Mon Jan 19 2015 Elio Maldonado <emaldona@redhat.com> - 3.16.2.3-5
- Reverse the sense of a test in patch to fix pk12util segfault
- Resolves: Bug 1174527 - Segfault in pk12util when using -l option with certain .p12 files

* Thu Jan 08 2015 Elio Maldonado <emaldona@redhat.com> - 3.16.2.3-4
- Fix race condition
- Resolves: Bug 1094468 - 389-ds-base server reported crash in stan_GetCERTCertificate
- under the replication replay failure condition

* Wed Jan 07 2015 Elio Maldonado <emaldona@redhat.com> - 3.16.2.3-3
- Resolves: Bug 1174527 - Segfault in pk12util when using -l option with certain .p12 files

* Tue Nov 25 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2.3-2
- Restore patch for certutil man page
- supply missing options descriptions
- Resolves: Bug 1158161 - Upgrade to NSS 3.16.2.3 for Firefox 31.3

* Thu Nov 13 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-10
- Resolves: Bug 1158161 - Upgrade to NSS 3.16.2.3 for Firefox 31.3
- Support TLS_FALLBACK_SCSV in tstclnt and ssltap

* Mon Sep 29 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-9
- Resolves: Bug 1145434 - CVE-2014-1568
- Using a release number higher than on rhel-7.0 branch

* Mon Aug 11 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-4
- Fix crash in stan_GetCERTCertificate
- Resolves: Bug 1094468

* Tue Aug 05 2014 Elio Maldonado <pbrobinson@redhat.com> 3.16.2-3
- Generic 32/64 bit platform detection (fix ppc64le build)
- Resolves: Bug 1125619 - nss fails to build on arch: ppc64le (missing dependencies)
- Fix contributed by Peter Robinson <pbrobinson@redhat.com>

* Fri Aug 01 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-2
- Fix libssl and test patches that disable ssl2 support
- Resolves: Bug 1123435
- Replace expired PayPal test certificate with current one

* Tue Jul 08 2014 Elio Maldonado <emaldona@redhat.com> - 3.16.2-1
- Rebase to nss-3.16.2
- Resolves: Bug 1103252 - Rebase RHEL 7.1 to at least NSS 3.16.1 (FF 31)
- Fix test failure detection in the %%check section
- Move removal of unwanted source directories to the end of the %%prep section
- Update various patches on account of the rebase
- Remove unused patches rendered obsolete by the rebase

* Mon Mar 03 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-6
- Disallow disabling the internal module
- Resolves: Bug 1056036 - nss segfaults with opencryptoki module

* Thu Feb 20 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-5
- Pick up a fix from rhel-6 and fix an rpm conflict
- Don't hold issuer cert handles in crl cache
- Resolves: Bug 1034409 - deadlock in trust domain and object lock
- Move nss shared db files to the main package
- Resolves: Bug 1050163 - Same files in two packages create rpm conflict

* Mon Jan 27 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-4
- Update pem sources to latest from nss-pem upstream
- Pick up pem module fixes verified on RHEL and applied upstream
- Remove no loger needed pem patches on acccount on this update
- Add comments documenting the iquote.patch 
- Resolves: Bug 1054457 - CVE-2013-1740

* Sun Jan 26 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.4-3
- Remove spurious man5 wildcard entry as all manpages are listed by name
- Resolves: Bug 1050163 - Same files in two packages create rpm conflict

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.15.4-2
- Mass rebuild 2014-01-24

* Sun Jan 19 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-9
- Rebase to nss-3.15.4
- Resolves: Bug 1054457 - CVE-2013-1740 nss: false start PR_Recv information disclosure security issue
- Remove no longer needed patches for manpages that were applied upstream
- Remove no longer needed patch to disable ocsp stapling tests
- Update iquote.patch on account of upstream changes
- Update and rename patch to pem/rsawrapr.c on account of upstream changes
- Use the pristine upstream sources for nss without repackaging
- Avoid unneeded manual step which may introduce errors

* Sun Jan 19 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-8
- Fix the spec file to apply the nss ecc list patch for bug 752980
- Resolves: Bug 752980 - Support ECDSA algorithm in the nss package via puggable ecc

* Fri Jan 17 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-7
- Move several nss-sysinit manpages tar archives to the %%files
- Resolves: Bug 1050163 - Same files in two packages create rpm conflict

* Fri Jan 17 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-6
- Fix a coverity scan compile time warning for the pem module
- Resolves: Bug 1002271 - NSS pem module should not require unique base file names

* Wed Jan 15 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-5
- Resolves: Bug 1002271 - NSS pem module should not require unique base file names

* Thu Jan 09 2014 Elio Maldonado <emaldona@redhat.com> - 3.15.3-4
- Improve pluggable ECC support for ECDSA
- Resolves: Bug 752980 - [7.0 FEAT] Support ECDSA algorithm in the nss package

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.15.3-3
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.3-2
- Revoke trust in one mis-issued anssi certificate
- Resolves: Bug 1040284 - nss: Mis-issued ANSSI/DCSSI certificate (MFSA 2013-117) [rhel-7.0]

* Mon Nov 25 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.3-1
- Update to NSS_3_15_3_RTM
- Resolves: Bug 1031463 - CVE-2013-5605 CVE-2013-5606 CVE-2013-1741

* Wed Nov 13 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-10
- Fix path to script and remove -- from some options in nss-sysinit man page
- Resolves: rhbz#982723 - man page of nss-sysinit worong path and other flaws

* Tue Nov 12 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-9
- Fix certutil man page options names to be consistent with help
- Resolves: rhbz#948495 - man page scan results for nss
- Remove incorrect count argument in status description in nss-sysinit man page
- Resolves: rhbz#982723 - man page of nss-sysinit incorrect option descriptions

* Wed Nov 06 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-8
- Fix patch for disabling ssl2 in ssl to correctly set error code
- Fix syntax error reported in the build.log even tough it succeeds
- Add patch top ignore setpolicy result 
- Resolves: rhbz#1001841 - Disable SSL2 and the export cipher suites
- Resolves: rhbz#1026677 - Attempt to run ipa-client-install fails

* Sun Nov 03 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-7
- Fix bash syntax error in patch for disabling ssl2 tests
- Resolves: rhbz#1001841 - Disable SSL2 and the export cipher suites

* Sat Nov 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-6
- Fix errors in ssl disabling patches for both library and tests
- Add s390x to the multilib_arches definition used for alt_ckbi
- Resolves: rhbz#1001841 - Disable SSL2 and the export cipher suites

* Thu Oct 31 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-5
- Fix errors in nss-sysinit manpage options descriptions
- Resolves: rhbz#982723

* Tue Oct 29 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-4
- Enable fips when system is in fips mode
- Resolves: rhbz#852023 - FIPS mode detection does not work

* Tue Oct 29 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-3
- Remove unused and obsoleted patches
- Related: rhbz#1012656

* Mon Oct 28 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-2
- Add description of the certutil's --email option to it's manpage
- Resolves: rhbz#Bug 948495 - Man page scan results for nss

* Mon Oct 21 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.2-1
- Rebase to nss-3.15.2
- Resolves: rhbz#1012656 - pick up NSS 3.15.2 to fix CVE-2013-1739 and disable MD5 in OCSP/CRL

* Fri Oct 11 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-4
- Install symlink to nss-sysinit.sh without the .sh suffix
- Resolves: rhbz#982723 - nss-sysinit man page has wrong path for the script

* Tue Oct 08 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-3
- Resolves: rhbz#1001841 - Disable SSL2 and the export cipher suites

* Tue Aug 06 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-2
- Add upstream bug URL for a patch subitted upstream and remove obsolete script

* Wed Jul 24 2013 Elio Maldonado <emaldona@redhat.com> - 3.15.1-2
- Update to NSS_3_15_1_RTM
- Apply various fixes to the man pages and add new ones
- Enable the iquote.patch to access newly introduced types
- Add man page for pkcs11.txt configuration file and cert and key databases
- Add missing option descriptions for {cert|cms|crl}util
- Resolves: rhbz#948495 - Man page scan results for nss
- Resolves: rhbz#982723 - Fix path to script in man page for nss-sysinit

* Tue Jul 02 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-6
- Use the unstripped source tar ball

* Wed Jun 19 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-5
- Install man pages for nss-tools and the nss-config and setup-nsssysinit scripts
- Resolves: rhbz#606020 - nss security tools lack man pages

* Tue Jun 18 2013 emaldona <emaldona@redhat.com> - 3.15-4
- Build nss without softoken or util sources in the tree
- Resolves: rhbz#689918

* Mon Jun 17 2013 emaldona <emaldona@redhat.com> - 3.15-3
- Update ssl-cbc-random-iv-by-default.patch

* Sun Jun 16 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-2
- Fix generation of NSS_VMAJOR, NSS_VMINOR, and NSS_VPATCH for nss-config

* Sat Jun 15 2013 Elio Maldonado <emaldona@redhat.com> - 3.15-1
- Update to NSS_3_15_RTM

* Tue May 14 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.3-13.0
- Reactivate nss-ssl-cbc-random-iv-off-by-default.patch

* Fri Apr 19 2013 Kai Engert <kaie@redhat.com> - 3.14.3-12.0
- Add upstream patch to fix rhbz#872761

* Sun Mar 24 2013 Kai Engert <kaie@redhat.com> - 3.14.3-11
- Update expired test certificates (fixed in upstream bug 852781)

* Fri Mar 08 2013 Kai Engert <kaie@redhat.com> - 3.14.3-10
- Fix incorrect post/postun scripts. Fix broken links in posttrans.

* Wed Mar 06 2013 Kai Engert <kaie@redhat.com> - 3.14.3-9
- Configure libnssckbi.so to use the alternatives system
  in order to prepare for a drop in replacement.

* Fri Feb 15 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.3-1
- Update to NSS_3_14_3_RTM
- sync up pem rsawrapr.c with softoken upstream changes for nss-3.14.3
- Resolves: rhbz#908257 - CVE-2013-1620 nss: TLS CBC padding timing attack
- Resolves: rhbz#896651 - PEM module trashes private keys if login fails
- Resolves: rhbz#909775 - specfile support for AArch64
- Resolves: rhbz#910584 - certutil -a does not produce ASCII output

* Mon Feb 04 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-2
- Allow building nss against older system sqlite

* Fri Feb 01 2013 Elio Maldonado <emaldona@redhat.com> - 3.14.2-1
- Update to NSS_3_14_2_RTM

* Wed Jan 02 2013 Kai Engert <kaie@redhat.com> - 3.14.1-3
- Update to NSS_3_14_1_WITH_CKBI_1_93_RTM

* Sat Dec 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-2
- Require nspr >= 4.9.4
- Fix changelog invalid dates

* Mon Dec 17 2012 Elio Maldonado <emaldona@redhat.com> - 3.14.1-1
- Update to NSS_3_14_1_RTM

* Wed Dec 12 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-12
- Bug 879978 - Install the nssck.api header template where mod_revocator can access it
- Install nssck.api in /usr/includes/nss3/templates

* Tue Nov 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-11
- Bug 879978 - Install the nssck.api header template in a place where mod_revocator can access it
- Install nssck.api in /usr/includes/nss3

* Mon Nov 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-10
- Bug 870864 - Add support in NSS for Secure Boot

* Sat Nov 10 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-9
- Disable bypass code at build time and return failure on attempts to enable at runtime
- Bug 806588 - Disable SSL PKCS #11 bypass at build time

* Sun Nov 04 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-8
- Fix pk11wrap locking which fixes 'fedpkg new-sources' and 'fedpkg update' hangs
- Bug 872124 - nss-3.14 breaks fedpkg new-sources
- Fix should be considered preliminary since the patch may change upon upstream approval
 
* Thu Nov 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-7
- Add a dummy source file for testing /preventing fedpkg breakage
- Helps test the fedpkg new-sources and upload commands for breakage by nss updates
- Related to Bug 872124 - nss 3.14 breaks fedpkg new-sources

* Thu Nov 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-6
- Fix a previous unwanted merge from f18
- Update the SS_SSL_CBC_RANDOM_IV patch to match new sources while
- Keeping the patch disabled while we are still in rawhide and
- State in comment that patch is needed for both stable and beta branches
- Update .gitignore to download only the new sources

* Wed Oct 31 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-5
- Fix the spec file so sechash.h gets installed
- Resolves: rhbz#871882 - missing header: sechash.h in nss 3.14

* Sat Oct 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-4
- Update the license to MPLv2.0

* Wed Oct 24 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-3
- Use only -f when removing unwanted headers

* Tue Oct 23 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-2
- Add secmodt.h to the headers installed by nss-devel
- nss-devel must install secmodt.h which moved from softoken to pk11wrap with nss-3.14

* Mon Oct 22 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-1
- Update to NSS_3_14_RTM

* Sun Oct 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.14-0.1.rc.1
- Update to NSS_3_14_RC1
- update nss-589636.patch to apply to httpdserv
- turn off ocsp tests for now
- remove no longer needed patches
- remove headers shipped by nss-util

* Fri Oct 05 2012 Kai Engert <kaie@redhat.com> - 3.13.6-1
- Update to NSS_3_13_6_RTM

* Mon Aug 27 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-8
- Rebase pem sources to fedora-hosted upstream to pick up two fixes from rhel-6.3
- Resolves: rhbz#847460 - Fix invalid read and free on invalid cert load
- Resolves: rhbz#847462 - PEM module may attempt to free uninitialized pointer 
- Remove unneeded fix gcc 4.7 c++ issue in secmodt.h that actually undoes the upstream fix

* Mon Aug 13 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-7
- Fix pluggable ecc support

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-5
- Fix checkin comment to prevent unwanted expansions of percents

* Sun Jul 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-4
- Resolves: Bug 830410 - Missing Requires %%{?_isa}
- Use Requires: %%{name}%%{?_isa} = %%{version}-%%{release} on tools
- Drop zlib requires which rpmlint reports as error E: explicit-lib-dependency zlib
- Enable sha224 portion of powerup selftest when running test suites
- Require nspr 4.9.1

* Wed Jun 20 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-3
- Resolves: rhbz#833529 - revert unwanted change to nss.pc.in

* Tue Jun 19 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-2
- Resolves: rhbz#833529 - Remove unwanted space from the Libs: line on nss.pc.in

* Mon Jun 18 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.5-1
- Update to NSS_3_13_5_RTM

* Fri Apr 13 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-3
- Resolves: Bug 812423 - nss_Init leaks memory, fix from RHEL 6.3

* Sun Apr 08 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-2
- Resolves: Bug 805723 - Library needs partial RELRO support added
- Patch coreconf/Linux.mk as done on RHEL 6.2

* Fri Apr 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.4-1
- Update to NSS_3_13_4_RTM
- Update the nss-pem source archive to the latest version
- Remove no longer needed patches
- Resolves: Bug 806043 - use pem files interchangeably in a single process
- Resolves: Bug 806051 - PEM various flaws detected by Coverity
- Resolves: Bug 806058 - PEM pem_CreateObject leaks memory given a non-existing file name

* Wed Mar 21 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-4
- Resolves: Bug 805723 - Library needs partial RELRO support added

* Fri Mar 09 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-3
- Cleanup of the spec file
- Add references to the upstream bugs
- Fix typo in Summary for sysinit

* Thu Mar 08 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-2
- Pick up fixes from RHEL
- Resolves: rhbz#800674 - Unable to contact LDAP Server during winsync
- Resolves: rhbz#800682 - Qpid AMQP daemon fails to load after nss update
- Resolves: rhbz#800676 - NSS workaround for freebl bug that causes openswan to drop connections

* Thu Mar 01 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.3-1
- Update to NSS_3_13_3_RTM

* Mon Jan 30 2012 Tom Callaway <spot@fedoraproject.org> - 3.13.1-13
- fix issue with gcc 4.7 in secmodt.h and C++11 user-defined literals

* Thu Jan 26 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.1-12
- Resolves: Bug 784672 - nss should protect against being called before nss_Init

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jan 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.1-11
- Deactivate a patch currently meant for stable branches only

* Fri Jan 06 2012 Elio Maldonado <emaldona@redhat.com> - 3.13.1-10
- Resolves: Bug 770682 - nss update breaks pidgin-sipe connectivity
- NSS_SSL_CBC_RANDOM_IV set to 0 by default and changed to 1 on user request

* Tue Dec 13 2011 elio maldonado <emaldona@redhat.com> - 3.13.1-9
- Revert to using current nss_softokn_version
- Patch to deal with lack of sha224 is no longer needed

* Tue Dec 13 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-8
- Resolves: Bug 754771 - [PEM] an unregistered callback causes a SIGSEGV

* Mon Dec 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-7
- Resolves: Bug 750376 - nss 3.13 breaks sssd TLS
- Fix how pem is built so that nss-3.13.x works with nss-softokn-3.12.y
- Only patch blapitest for the lack of sha224 on system freebl
- Completed the patch to make pem link against system freebl

* Mon Dec 05 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-6
- Removed unwanted /usr/include/nss3 in front of the normal cflags include path
- Removed unnecessary patch dealing with CERTDB_TERMINAL_RECORD, it's visible

* Sun Dec 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-5
- Statically link the pem module against system freebl found in buildroot
- Disabling sha224-related powerup selftest until we update softokn
- Disable sha224 and pss tests which nss-softokn 3.12.x doesn't support

* Fri Dec 02 2011 Elio Maldonado Batiz <emaldona@redhat.com> - 3.13.1-4
- Rebuild with nss-softokn from 3.12 in the buildroot
- Allows the pem module to statically link against 3.12.x freebl
- Required for using nss-3.13.x with nss-softokn-3.12.y for a merge inrto rhel git repo
- Build will be temprarily placed on buildroot override but not pushed in bodhi

* Fri Nov 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-2
- Fix broken dependencies by updating the nss-util and nss-softokn versions

* Thu Nov 03 2011 Elio Maldonado <emaldona@redhat.com> - 3.13.1-1
- Update to NSS_3_13_1_RTM
- Update builtin certs to those from NSSCKBI_1_88_RTM

* Sat Oct 15 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-1
- Update to NSS_3_13_RTM

* Sat Oct 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.13-0.1.rc0.1
- Update to NSS_3_13_RC0

* Wed Sep 14 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.11-3
- Fix attempt to free initilized pointer (#717338)
- Fix leak on pem_CreateObject when given non-existing file name (#734760)
- Fix pem_Initialize to return CKR_CANT_LOCK on multi-treaded calls (#736410)

* Tue Sep 06 2011 Kai Engert <kaie@redhat.com> - 3.12.11-2
- Update builtins certs to those from NSSCKBI_1_87_RTM

* Tue Aug 09 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.11-1
- Update to NSS_3_12_11_RTM

* Sat Jul 23 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-6
- Indicate the provenance of stripped source tarball (#688015)

* Mon Jun 27 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.12.10-5
- Provide virtual -static package to meet guidelines (#609612).

* Fri Jun 10 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-4
- Enable pluggable ecc support (#712556)
- Disable the nssdb write-access-on-read-only-dir tests when user is root (#646045)

* Fri May 20 2011 Dennis Gilmore <dennis@ausil.us> - 3.12.10-3
- make the testsuite non fatal on arm arches

* Tue May 17 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-2
- Fix crmf hard-coded maximum size for wrapped private keys (#703656)

* Fri May 06 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-1
- Update to NSS_3_12_10_RTM

* Wed Apr 27 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.10-0.1.beta1
- Update to NSS_3_12_10_BETA1

* Mon Apr 11 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-15
- Implement PEM logging using NSPR's own (#695011)

* Wed Mar 23 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-14
- Update to NSS_3.12.9_WITH_CKBI_1_82_RTM

* Thu Feb 24 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-13
- Short-term fix for ssl test suites hangs on ipv6 type connections (#539183)

* Fri Feb 18 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-12
- Add a missing requires for pkcs11-devel (#675196)

* Tue Feb 15 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-11
- Run the test suites in the check section (#677809)

* Thu Feb 10 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-10
- Fix cms headers to not use c++ reserved words (#676036)
- Reenabling Bug 499444 patches
- Fix to swap internal key slot on fips mode switches

* Tue Feb 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-9
- Revert patches for 499444 until all c++ reserved words are found and extirpated

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-7
- Fix cms header to not use c++ reserved word (#676036)
- Reenable patches for bug 499444

* Tue Feb 08 2011 Christopher Aillon <caillon@redhat.com> - 3.12.9-6
- Revert patches for 499444 as they use a C++ reserved word and
  cause compilation of Firefox to fail

* Fri Feb 04 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-5
- Fix the earlier infinite recursion patch (#499444)
- Remove a header that now nss-softokn-freebl-devel ships

* Tue Feb 01 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-4
- Fix infinite recursion when encoding NSS enveloped/digested data (#499444)

* Mon Jan 31 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-3
- Update the cacert trust patch per upstream review requests (#633043)

* Wed Jan 19 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-2
- Fix to honor the user's cert trust preferences (#633043)
- Remove obsoleted patch

* Wed Jan 12 2011 Elio Maldonado <emaldona@redhat.com> - 3.12.9-1
- Update to 3.12.9

* Mon Dec 27 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.9-0.1.beta2
- Rebuilt according to fedora pre-release package naming guidelines

* Fri Dec 10 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.2-1
- Update to NSS_3_12_9_BETA2
- Fix libpnsspem crash when cacert dir contains other directories (#642433)

* Wed Dec 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8.99.1-1
- Update to NSS_3_12_9_BETA1

* Thu Nov 25 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-9
- Update pem source tar with fixes for 614532 and 596674
- Remove no longer needed patches

* Fri Nov 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-8
- Update PayPalEE.cert test certificate which had expired

* Sun Oct 31 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-7
- Tell rpm not to verify md5, size, and modtime of configurations file

* Mon Oct 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-6
- Fix certificates trust order (#643134)
- Apply nss-sysinit-userdb-first.patch last

* Wed Oct 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-5
- Move triggerpostun -n nss-sysinit script ahead of the other ones (#639248)

* Tue Oct 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-4
- Fix invalid %%postun scriptlet (#639248)

* Wed Sep 29 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-3
- Replace posttrans sysinit scriptlet with a triggerpostun one (#636787)
- Fix and cleanup the setup-nsssysinit.sh script (#636792, #636801)

* Mon Sep 27 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-2
- Add posttrans scriptlet (#636787)

* Thu Sep 23 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.8-1
- Update to 3.12.8
- Prevent disabling of nss-sysinit on package upgrade (#636787)
- Create pkcs11.txt with correct permissions regardless of umask (#636792) 
- Setup-nsssysinit.sh reports whether nss-sysinit is turned on or off (#636801)
- Added provides pkcs11-devel-static to comply with packaging guidelines (#609612)

* Sat Sep 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.4-1
- NSS 3.12.8 RC0

* Sun Sep 05 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-2
- Fix nss-util_version and nss_softokn_version required to be 3.12.7.99.3

* Sat Sep 04 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7.99.3-1
- NSS 3.12.8 Beta3
- Fix unclosed comment in renegotiate-transitional.patch

* Sat Aug 28 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-3
- Change BuildRequries to available version of nss-util-devel

* Sat Aug 28 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-2
- Define NSS_USE_SYSTEM_SQLITE and remove unneeded patch
- Add comments regarding an unversioned provides which triggers rpmlint warning
- Build requires nss-softokn-devel >= 3.12.7

* Mon Aug 16 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.7-1
- Update to 3.12.7

* Sat Aug 14 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-12
- Apply the patches to fix rhbz#614532

* Mon Aug 09 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-11
- Removed pem sourecs as they are in the cache

* Mon Aug 09 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-10
- Add support for PKCS#8 encoded PEM RSA private key files (#614532)

* Sat Jul 31 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-9
- Fix nsssysinit to return userdb ahead of systemdb (#603313)

* Tue Jun 08 2010 Dennis Gilmore <dennis@ausil.us> - 3.12.6-8
- Require and BuildRequire >= the listed version not =

* Tue Jun 08 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-7
- Require nss-softoken 3.12.6

* Sun Jun 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-6
- Fix SIGSEGV within CreateObject (#596674)

* Mon Apr 12 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-5
- Update pem source tar to pick up the following bug fixes:
- PEM - Allow collect objects to search through all objects
- PEM - Make CopyObject return a new shallow copy
- PEM - Fix memory leak in pem_mdCryptoOperationRSAPriv

* Wed Apr 07 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-4
- Update the test cert in the setup phase

* Wed Apr 07 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-3
- Add sed to sysinit requires as setup-nsssysinit.sh requires it (#576071)
- Update PayPalEE test cert with unexpired one (#580207)

* Thu Mar 18 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-2
- Fix ns.spec to not require nss-softokn (#575001)

* Sat Mar 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1.2
- rebuilt with all tests enabled

* Sat Mar 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1.1
- Using SSL_RENEGOTIATE_TRANSITIONAL as default while on transition period
- Disabling ssl tests suites until bug 539183 is resolved

* Sat Mar 06 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.6-1
- Update to 3.12.6
- Reactivate all tests
- Patch tools to validate command line options arguments

* Mon Jan 25 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-8
- Fix curl related regression and general patch code clean up

* Wed Jan 13 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-5
-  retagging

* Tue Jan 12 2010 Elio Maldonado <emaldona@redhat.com> - 3.12.5-1.1
- Fix SIGSEGV on call of NSS_Initialize (#553638)

* Wed Jan 06 2010 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.13.2
- New version of patch to allow root to modify ystem database (#547860)

* Thu Dec 31 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.13.1
- Temporarily disabling the ssl tests

* Sat Dec 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.13
- Fix nsssysinit to allow root to modify the nss system database (#547860)

* Fri Dec 25 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.11
- Fix an error introduced when adapting the patch for rhbz #546211

* Sat Dec 19 2009 Elio maldonado<emaldona@redhat.com> - 3.12.5-1.9
- Remove left over trace statements from nsssysinit patching

* Fri Dec 18 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-2.7
- Fix a misconstructed patch

* Thu Dec 17 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.6
- Fix nsssysinit to enable apps to use system cert store, patch contributed by David Woodhouse (#546221)
- Fix spec so sysinit requires coreutils for post install scriplet (#547067)
- Fix segmentation fault when listing keys or certs in the database, patch contributed by Kamil Dudka (#540387)

* Thu Dec 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.5
- Fix nsssysinit to set the default flags on the crypto module (#545779)
- Remove redundant header from the pem module

* Wed Dec 09 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.1
- Remove unneeded patch

* Thu Dec 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1.1
- Retagging to include missing patch

* Thu Dec 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.5-1
- Update to 3.12.5
- Patch to allow ssl/tls clients to interoperate with servers that require renogiation

* Fri Nov 20 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-14.1
- Retagging

* Tue Oct 20 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-13.1
- Require nss-softoken of same architecture as nss (#527867)
- Merge setup-nsssysinit.sh improvements from F-12 (#527051)

* Sat Oct 03 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-13
- User no longer prompted for a password when listing keys an empty system db (#527048)
- Fix setup-nsssysinit to handle more general formats (#527051)

* Sun Sep 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-12
- Fix syntax error in setup-nsssysinit.sh

* Sun Sep 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-11
- Fix sysinit to be under mozilla/security/nss/lib

* Sat Sep 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-10
- Add nss-sysinit activation/deactivation script

* Fri Sep 18 2009 Elio Maldonado<emaldona@redhat.com - 3.12.4-9
- Install blank databases and configuration file for system shared database
- nsssysinit queries system for fips mode before relying on environment variable

* Thu Sep 10 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-8
- Restoring nssutil and -rpath-link to nss-config for now - 522477

* Tue Sep 08 2009 Elio Maldonado<emaldona@redhat.com - 3.12.4-7
- Add the nss-sysinit subpackage

* Tue Sep 08 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-6
- Installing shared libraries to %%{_libdir}

* Mon Sep 07 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-5
- Retagging to pick up new sources

* Mon Sep 07 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-4
- Update pem enabling source tar with latest fixes (509705, 51209)

* Sun Sep 06 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-3
- PEM module implements memory management for internal objects - 509705
- PEM module doesn't crash when processing malformed key files - 512019

* Sat Sep 05 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-2
- Remove symbolic links to shared libraries from devel - 521155
- No rpath-link in nss-softokn-config

* Tue Sep 01 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.4-1
- Update to 3.12.4

* Mon Aug 31 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-30
- Fix FORTIFY_SOURCE buffer overflows in test suite on ppc and ppc64 - bug 519766
- Fixed requires and buildrequires as per recommendations in spec file review

* Sun Aug 30 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-29
- Restoring patches 2 and 7 as we still compile all sources
- Applying the nss-nolocalsql.patch solves nss-tools sqlite dependency problems

* Sun Aug 30 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-28
- restore require sqlite

* Sat Aug 29 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-27
- Don't require sqlite for nss

* Sat Aug 29 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-26
- Ensure versions in the requires match those used when creating nss.pc

* Fri Aug 28 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-25
- Remove nss-prelink.conf as signed all shared libraries moved to nss-softokn
- Add a temprary hack to nss.pc.in to unblock builds

* Fri Aug 28 2009 Warren Togami <wtogami@redhat.com> - 3.12.3.99.3-24
- caolan's nss.pc patch

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-23
- Bump the release number for a chained build of nss-util, nss-softokn and nss

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-22
- Fix nss-config not to include nssutil
- Add BuildRequires on nss-softokn and nss-util since build also runs the test suite

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-21
- disabling all tests while we investigate a buffer overflow bug

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-20
- disabling some tests while we investigate a buffer overflow bug - 519766

* Thu Aug 27 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-19
- remove patches that are now in nss-softokn and
- remove spurious exec-permissions for nss.pc per rpmlint
- single requires line in nss.pc.in

* Wed Aug 26 2009 Elio Maldonado<emaldona@redhat.com> - 3.12.3.99.3-18
- Fix BuildRequires: nss-softokn-devel release number

* Wed Aug 26 2009 Elio Maldonado<emaldona@redhat.com - 3.12.3.99.3-17
- fix nss.pc.in to have one single requires line

* Tue Aug 25 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-16
- cleanups for softokn

* Tue Aug 25 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-15
- remove the softokn subpackages

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-14
- don install the nss-util pkgconfig bits

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-13
- remove from -devel the 3 headers that ship in nss-util-devel

* Mon Aug 24 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-12
- kill off the nss-util nss-util-devel subpackages

* Sun Aug 23 2009 Elio Maldonado+emaldona@redhat.com - 3.12.3.99.3-11
- split off nss-softokn and nss-util as subpackages with their own rpms
- first phase of splitting nss-softokn and nss-util as their own packages

* Thu Aug 20 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-10
- must install libnssutil3.since nss-util is untagged at the moment
- preserve time stamps when installing various files

* Thu Aug 20 2009 Dennis Gilmore <dennis@ausil.us> - 3.12.3.99.3-9
- dont install libnssutil3.so since its now in nss-util

* Thu Aug 06 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-7.1
- Fix spec file problems uncovered by Fedora_12_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.3.99.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-6
- removed two patch files which are no longer needed and fixed previous change log number
* Mon Jun 22 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-5
- updated pem module incorporates various patches
- fix off-by-one error when computing size to reduce memory leak. (483855)
- fix data type to work on x86_64 systems. (429175)
- fix various memory leaks and free internal objects on module unload. (501080)
- fix to not clone internal objects in collect_objects().  (501118)
- fix to not bypass initialization if module arguments are omitted. (501058)
- fix numerous gcc warnings. (500815)
- fix to support arbitrarily long password while loading a private key. (500180) 
- fix memory leak in make_key and memory leaks and return values in pem_mdSession_Login (501191)
* Mon Jun 08 2009 Elio Maldonado <emaldona@redhat.com> - 3.12.3.99.3-4
- add patch for bug 502133 upstream bug 496997
* Fri Jun 05 2009 Kai Engert <kaie@redhat.com> - 3.12.3.99.3-3
- rebuild with higher release number for upgrade sanity
* Fri Jun 05 2009 Kai Engert <kaie@redhat.com> - 3.12.3.99.3-2
- updated to NSS_3_12_4_FIPS1_WITH_CKBI_1_75
* Thu May 07 2009 Kai Engert <kaie@redhat.com> - 3.12.3-7
- re-enable test suite
- add patch for upstream bug 488646 and add newer paypal
  certs in order to make the test suite pass
* Wed May 06 2009 Kai Engert <kaie@redhat.com> - 3.12.3-4
- add conflicts info in order to fix bug 499436
* Tue Apr 14 2009 Kai Engert <kaie@redhat.com> - 3.12.3-3
- ship .chk files instead of running shlibsign at install time
- include .chk file in softokn-freebl subpackage
- add patch for upstream nss bug 488350
* Tue Apr 14 2009 Kai Engert <kaie@redhat.com> - 3.12.3-2
- Update to NSS 3.12.3
* Mon Apr 06 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-7
- temporarily disable the test suite because of bug 494266
* Mon Apr 06 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-6
- fix softokn-freebl dependency for multilib (bug 494122)
* Thu Apr 02 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-5
- introduce separate nss-softokn-freebl package
* Thu Apr 02 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-4
- disable execstack when building freebl
* Tue Mar 31 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-3
- add upstream patch to fix bug 483855
* Tue Mar 31 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-2
- build nspr-less freebl library
* Tue Mar 31 2009 Kai Engert <kaie@redhat.com> - 3.12.2.99.3-1
- Update to NSS_3_12_3_BETA4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Kai Engert <kaie@redhat.com> - 3.12.2.0-3
- update to NSS_3_12_2_RC1
- use system zlib
* Tue Sep 30 2008 Dennis Gilmore <dennis@ausil.us> - 3.12.1.1-4
- add sparc64 to the list of 64 bit arches

* Wed Sep 24 2008 Kai Engert <kaie@redhat.com> - 3.12.1.1-3
- bug 456847, move pkgconfig requirement to devel package
* Fri Sep 05 2008 Kai Engert <kengert@redhat.com> - 3.12.1.1-2
- Update to NSS_3_12_1_RC2
* Fri Aug 22 2008 Kai Engert <kaie@redhat.com> - 3.12.1.0-2
- NSS 3.12.1 RC1
* Fri Aug 15 2008 Kai Engert <kaie@redhat.com> - 3.12.0.3-7
- fix bug bug 429175 in libpem module
* Tue Aug 05 2008 Kai Engert <kengert@redhat.com> - 3.12.0.3-6
- bug 456847, add Requires: pkgconfig
* Tue Jun 24 2008 Kai Engert <kengert@redhat.com> - 3.12.0.3-3
- nss package should own /etc/prelink.conf.d folder, rhbz#452062
- use upstream patch to fix test suite abort
* Mon Jun 02 2008 Kai Engert <kengert@redhat.com> - 3.12.0.3-2
- Update to NSS_3_12_RC4
* Mon Apr 14 2008 Kai Engert <kengert@redhat.com> - 3.12.0.1-1
- Update to NSS_3_12_RC2
* Thu Mar 20 2008 Jesse Keating <jkeating@redhat.com> - 3.11.99.5-2
- Zapping old Obsoletes/Provides.  No longer needed, causes multilib headache.
* Mon Mar 17 2008 Kai Engert <kengert@redhat.com> - 3.11.99.5-1
- Update to NSS_3_12_BETA3
* Fri Feb 22 2008 Kai Engert <kengert@redhat.com> - 3.11.99.4-1
- NSS 3.12 Beta 2
- Use /usr/lib{64} as devel libdir, create symbolic links.
* Sat Feb 16 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-6
- Apply upstream patch for bug 417664, enable test suite on pcc.
* Fri Feb 15 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-5
- Support concurrent runs of the test suite on a single build host.
* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-4
- disable test suite on ppc
* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-3
- disable test suite on ppc64

* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-2
- Build against gcc 4.3.0, use workaround for bug 432146
- Run the test suite after the build and abort on failures.

* Thu Jan 24 2008 Kai Engert <kengert@redhat.com> - 3.11.99.3-1
* NSS 3.12 Beta 1

* Mon Jan 07 2008 Kai Engert <kengert@redhat.com> - 3.11.99.2b-3
- move .so files to /lib

* Wed Dec 12 2007 Kai Engert <kengert@redhat.com> - 3.11.99.2b-2
- NSS 3.12 alpha 2b

* Mon Dec 03 2007 Kai Engert <kengert@redhat.com> - 3.11.99.2-2
- upstream patches to avoid calling netstat for random data

* Wed Nov 07 2007 Kai Engert <kengert@redhat.com> - 3.11.99.2-1
- NSS 3.12 alpha 2

* Wed Oct 10 2007 Kai Engert <kengert@redhat.com> - 3.11.7-10
- Add /etc/prelink.conf.d/nss-prelink.conf in order to blacklist
  our signed libraries and protect them from modification.

* Thu Sep 06 2007 Rob Crittenden <rcritten@redhat.com> - 3.11.7-9
- Fix off-by-one error in the PEM module

* Thu Sep 06 2007 Kai Engert <kengert@redhat.com> - 3.11.7-8
- fix a C++ mode compilation error

* Wed Sep 05 2007 Bob Relyea <rrelyea@redhat.com> - 3.11.7-7
- Add 3.12 ckfw and libnsspem

* Tue Aug 28 2007 Kai Engert <kengert@redhat.com> - 3.11.7-6
- Updated license tag

* Wed Jul 11 2007 Kai Engert <kengert@redhat.com> - 3.11.7-5
- Ensure the workaround for mozilla bug 51429 really get's built.

* Mon Jun 18 2007 Kai Engert <kengert@redhat.com> - 3.11.7-4
- Better approach to ship freebl/softokn based on 3.11.5
- Remove link time dependency on softokn

* Sun Jun 10 2007 Kai Engert <kengert@redhat.com> - 3.11.7-3
- Fix unowned directories, rhbz#233890

* Fri Jun 01 2007 Kai Engert <kengert@redhat.com> - 3.11.7-2
- Update to 3.11.7, but freebl/softokn remain at 3.11.5.
- Use a workaround to avoid mozilla bug 51429.

* Fri Mar 02 2007 Kai Engert <kengert@redhat.com> - 3.11.5-2
- Fix rhbz#230545, failure to enable FIPS mode
- Fix rhbz#220542, make NSS more tolerant of resets when in the 
  middle of prompting for a user password.

* Sat Feb 24 2007 Kai Engert <kengert@redhat.com> - 3.11.5-1
- Update to 3.11.5
- This update fixes two security vulnerabilities with SSL 2
- Do not use -rpath link option
- Added several unsupported tools to tools package

* Tue Jan  9 2007 Bob Relyea <rrelyea@redhat.com> - 3.11.4-4
- disable ECC, cleanout dead code

* Tue Nov 28 2006 Kai Engert <kengert@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Thu Sep 14 2006 Kai Engert <kengert@redhat.com> - 3.11.3-2
- Revert the attempt to require latest NSPR, as it is not yet available
  in the build infrastructure.

* Thu Sep 14 2006 Kai Engert <kengert@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Thu Aug 03 2006 Kai Engert <kengert@redhat.com> - 3.11.2-2
- Add /etc/pki/nssdb

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.11.2-1.1
- rebuild

* Fri Jun 30 2006 Kai Engert <kengert@redhat.com> - 3.11.2-1
- Update to 3.11.2
- Enable executable bit on shared libs, also fixes debug info.

* Wed Jun 14 2006 Kai Engert <kengert@redhat.com> - 3.11.1-2
- Enable Elliptic Curve Cryptography (ECC)

* Fri May 26 2006 Kai Engert <kengert@redhat.com> - 3.11.1-1
- Update to 3.11.1
- Include upstream patch to limit curves

* Wed Feb 15 2006 Kai Engert <kengert@redhat.com> - 3.11-4
- add --noexecstack when compiling assembler on x86_64

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.11-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.11-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 3.11-3
- rebuild

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> 3.11-2
- Update file list for the devel packages

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 3.11-1
- Update to 3.11

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 3.11-0.cvs.2
- Add patch to allow building on ppc*
- Update the pkgconfig file to Require nspr

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 3.11-0.cvs
- Initial import into Fedora Core, based on a CVS snapshot of
  the NSS_3_11_RTM tag
- Fix up the pkcs11-devel subpackage to contain the proper headers
- Build with RPM_OPT_FLAGS
- No need to have rpath of /usr/lib in the pc file

* Thu Dec 15 2005 Kai Engert <kengert@redhat.com>
- Adressed review comments by Wan-Teh Chang, Bob Relyea,
  Christopher Aillon.

* Sat Jul  9 2005 Rob Crittenden <rcritten@redhat.com> 3.10-1
- Initial build
