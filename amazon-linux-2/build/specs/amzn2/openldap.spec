%global _hardened_build 1

%global systemctl_bin /usr/bin/systemctl
%global check_password_version 1.1

Name: openldap
Version: 2.4.44
Release: 22%{?dist}
Summary: LDAP support libraries
Group: System Environment/Daemons
License: OpenLDAP
URL: http://www.openldap.org/
Source0: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: slapd.service
Source2: slapd.sysconfig
Source3: slapd.tmpfiles
Source4: slapd.ldif
Source5: ldap.conf
Source6: openldap.tmpfiles
Source10: ltb-project-openldap-ppolicy-check-password-%{check_password_version}.tar.gz
Source50: libexec-functions
Source51: libexec-convert-config.sh
Source52: libexec-check-config.sh
Source53: libexec-upgrade-db.sh
Source54: libexec-create-certdb.sh
Source55: libexec-generate-server-cert.sh
Source56: libexec-update-ppolicy-schema.sh

# patches for 2.4
Patch0: openldap-manpages.patch
Patch1: openldap-ppolicy-loglevels.patch
Patch2: openldap-sql-linking.patch
Patch3: openldap-reentrant-gethostby.patch
Patch4: openldap-smbk5pwd-overlay.patch
Patch5: openldap-ldaprc-currentdir.patch
Patch6: openldap-userconfig-setgid.patch
Patch7: openldap-allop-overlay.patch
Patch8: openldap-syncrepl-unset-tls-options.patch
Patch9: openldap-man-sasl-nocanon.patch
Patch10: openldap-ai-addrconfig.patch
# fix back_perl problems with lt_dlopen()
# might cause crashes because of symbol collisions
# the proper fix is to link all perl modules against libperl
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=327585
Patch19: openldap-switch-to-lt_dlopenadvise-to-get-RTLD_GLOBAL-set.patch
# ldapi sasl fix pending upstream inclusion
Patch20: openldap-ldapi-sasl.patch
# coverity - missin_unlock in servers/slapd/overlays/accesslog.c
Patch21: openldap-missing-unlock-in-accesslog-overlay.patch
Patch23: openldap-module-passwd-sha2.patch
# pending upstream inclusion, ITS #7744
Patch24: openldap-man-tls-reqcert.patch
Patch25: openldap-man-ldap-conf.patch
Patch35: openldap-ITS8428-init-sc_writewait.patch
Patch36: openldap-bdb_idl_fetch_key-correct-key-pointer.patch
Patch37: openldap-ITS8655-fix-double-free-on-paged-search-with-pagesize-0.patch
Patch38: openldap-ITS8720-back-ldap-starttls-timeout.patch
Patch39: openldap-ITS-9202-limit-depth-of-nested-filters.patch

# fixes for DH and ECDH
Patch50: openldap-openssl-its7506-fix-DH-params-1.patch
Patch51: openldap-openssl-its7506-fix-DH-params-2.patch
Patch52: openldap-openssl-ITS7595-Add-EC-support-1.patch
Patch53: openldap-openssl-ITS7595-Add-EC-support-2.patch

# check-password module specific patches
Patch90: check-password-makefile.patch
Patch91: check-password.patch
Patch92: check-password-loglevels.patch

# MozNSS compatibility layer
Patch101: openldap-tlsmc.patch
# Fedora specific patches
Patch102: openldap-fedora-systemd.patch

BuildRequires: cyrus-sasl-devel, nss-devel, openssl-devel, krb5-devel, tcp_wrappers-devel, unixODBC-devel
BuildRequires: glibc-devel, libtool, libtool-ltdl-devel, groff, perl, perl-devel, perl(ExtUtils::Embed)
Requires: nss-tools
Requires(post): rpm, coreutils, findutils

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: LDAP development libraries and header files
Group: Development/Libraries
Requires: openldap%{?_isa} = %{version}-%{release}, cyrus-sasl-devel%{?_isa}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package servers
Summary: LDAP server
License: OpenLDAP
Requires: openldap%{?_isa} = %{version}-%{release}, libdb-utils
Requires(pre): shadow-utils
Requires(post): systemd, systemd-sysv, chkconfig
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: libdb-devel
BuildRequires: systemd-units
BuildRequires: cracklib-devel
Group: System Environment/Daemons
# migrationtools (slapadd functionality):
Provides: ldif2ldbm

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd server and related files.

%package servers-sql
Summary: SQL support module for OpenLDAP server
Requires: openldap-servers%{?_isa} = %{version}-%{release}
Group: System Environment/Daemons

%description servers-sql
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains a loadable module which the
slapd server can use to read data from an RDBMS.

%package clients
Summary: LDAP client utilities
Requires: openldap%{?_isa} = %{version}-%{release}
Group: Applications/Internet

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

%prep
%setup -q -c -a 0 -a 10

pushd openldap-%{version}

%patch101 -p1

# alternative include paths for Mozilla NSS
ln -s %{_includedir}/nss3 include/nss
ln -s %{_includedir}/nspr4 include/nspr

AUTOMAKE=%{_bindir}/true autoreconf -fi

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1

%patch102 -p1

# build smbk5pwd with other overlays
ln -s ../../../contrib/slapd-modules/smbk5pwd/smbk5pwd.c servers/slapd/overlays
mv contrib/slapd-modules/smbk5pwd/README contrib/slapd-modules/smbk5pwd/README.smbk5pwd
# build allop with other overlays
ln -s ../../../contrib/slapd-modules/allop/allop.c servers/slapd/overlays
mv contrib/slapd-modules/allop/README contrib/slapd-modules/allop/README.allop
mv contrib/slapd-modules/allop/slapo-allop.5 doc/man/man5/slapo-allop.5
# build sha2 with other overlays
ln -s ../../../contrib/slapd-modules/passwd/sha2/{sha2.{c,h},slapd-sha2.c} \
      servers/slapd/overlays
ls servers/slapd/overlays
mv contrib/slapd-modules/passwd/sha2/README{,.sha2}

mv servers/slapd/back-perl/README{,.back_perl}

# fix documentation encoding
for filename in doc/drafts/draft-ietf-ldapext-acl-model-xx.txt; do
	iconv -f iso-8859-1 -t utf-8 "$filename" > "$filename.utf8"
	mv "$filename.utf8" "$filename"
done

popd

pushd ltb-project-openldap-ppolicy-check-password-%{check_password_version}
%patch90 -p1
%patch91 -p1
%patch92 -p1
popd

%build

%ifarch s390 s390x
  export CFLAGS="-fPIE"
%else
  export CFLAGS="-fpie"
%endif
export LDFLAGS="-pie"
# avoid stray dependencies (linker flag --as-needed)
# enable experimental support for LDAP over UDP (LDAP_CONNECTIONLESS)
export CFLAGS="${CFLAGS} %{optflags} -Wl,-z,relro,-z,now,--as-needed -DLDAP_CONNECTIONLESS -DLDAP_USE_NON_BLOCKING_TLS"

pushd openldap-%{version}
%configure \
	--enable-debug \
	--enable-dynamic \
	--enable-syslog \
	--enable-proctitle \
	--enable-ipv6 \
	--enable-local \
	\
	--enable-slapd \
	--enable-dynacl \
	--enable-aci \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
	--enable-spasswd \
	--enable-modules \
	--enable-rewrite \
	--enable-rlookups \
	--enable-slapi \
	--disable-slp \
	--enable-wrappers \
	\
	--enable-backends=mod \
	--enable-bdb=yes \
	--enable-hdb=yes \
	--enable-mdb=yes \
	--enable-monitor=yes \
	--disable-ndb \
	\
	--enable-overlays=mod \
	\
	--disable-static \
	--enable-shared \
	\
	--enable-moznss-compatibility=yes \
	\
	--with-cyrus-sasl \
	--without-fetch \
	--with-threads \
	--with-pic \
	--with-gnu-ld \
	\
	--libexecdir=%{_libdir}

make %{_smp_mflags}

# build mdb_* tools
pushd libraries/liblmdb
export XCFLAGS="$CFLAGS"
make %{_smp_mflags}
popd
popd

pushd ltb-project-openldap-ppolicy-check-password-%{check_password_version}
make LDAP_INC="-I../openldap-%{version}/include \
 -I../openldap-%{version}/servers/slapd \
 -I../openldap-%{version}/build-servers/include"
popd

%install

mkdir -p %{buildroot}%{_libdir}/

pushd openldap-%{version}
make install DESTDIR=%{buildroot} STRIP=""
pushd libraries/liblmdb
make install DESTDIR=%{buildroot}
popd
popd

# install check_password module
pushd ltb-project-openldap-ppolicy-check-password-%{check_password_version}
mv check_password.so check_password.so.%{check_password_version}
ln -s check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/check_password.so
install -m 755 check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/
# install -m 644 README %{buildroot}%{_libdir}/openldap
install -d -m 755 %{buildroot}%{_sysconfdir}/openldap
cat > %{buildroot}%{_sysconfdir}/openldap/check_password.conf <<EOF
# OpenLDAP pwdChecker library configuration

#useCracklib 1
#minPoints 3
#minUpper 0
#minLower 0
#minDigit 0
#minPunct 0
EOF
mv README{,.check_pwd}
popd

# setup directories for TLS certificates
mkdir -p %{buildroot}%{_sysconfdir}/openldap/certs

# setup data and runtime directories
mkdir -p %{buildroot}%{_sharedstatedir}
mkdir -p %{buildroot}%{_localstatedir}
install -m 0700 -d %{buildroot}%{_sharedstatedir}/ldap
install -m 0755 -d %{buildroot}%{_localstatedir}/run/openldap

# setup autocreation of runtime directories on tmpfs
mkdir -p %{buildroot}%{_tmpfilesdir}/
install -m 0644 %SOURCE3 %{buildroot}%{_tmpfilesdir}/slapd.conf
install -m 0644 %SOURCE6 %{buildroot}%{_tmpfilesdir}/openldap.conf

# install default ldap.conf (customized)
rm -f %{buildroot}%{_sysconfdir}/openldap/ldap.conf
install -m 0644 %SOURCE5 %{buildroot}%{_sysconfdir}/openldap/ldap.conf

# setup maintainance scripts
mkdir -p %{buildroot}%{_libexecdir}
install -m 0755 -d %{buildroot}%{_libexecdir}/openldap
install -m 0644 %SOURCE50 %{buildroot}%{_libexecdir}/openldap/functions
install -m 0755 %SOURCE51 %{buildroot}%{_libexecdir}/openldap/convert-config.sh
install -m 0755 %SOURCE52 %{buildroot}%{_libexecdir}/openldap/check-config.sh
install -m 0755 %SOURCE53 %{buildroot}%{_libexecdir}/openldap/upgrade-db.sh
install -m 0755 %SOURCE54 %{buildroot}%{_libexecdir}/openldap/create-certdb.sh
install -m 0755 %SOURCE55 %{buildroot}%{_libexecdir}/openldap/generate-server-cert.sh
install -m 0755 %SOURCE56 %{buildroot}%{_libexecdir}/openldap/update-ppolicy-schema.sh

# install mdb_* tools
mv %{buildroot}/usr/local/bin/mdb_{copy,dump,load,stat} %{buildroot}%{_libexecdir}/openldap/
mkdir -p %{buildroot}%{_libexecdir}/openldap/man/man1
mv %{buildroot}/usr/local/share/man/man1/mdb_{copy,dump,load,stat}.1 %{buildroot}%{_libexecdir}/openldap/man/man1/
# we don't want the library itself nor header file
rm -f %{buildroot}/usr/local/include/lmdb.h
rm -f %{buildroot}/usr/local/lib/liblmdb.{a,so}

# remove build root from config files and manual pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_sysconfdir}/openldap/*.conf
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# we don't need the default files -- RPM handles changes
rm -f %{buildroot}%{_sysconfdir}/openldap/*.default
rm -f %{buildroot}%{_sysconfdir}/openldap/schema/*.default

# install an init script for the servers
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/slapd.service

# install syconfig/ldap
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE2 %{buildroot}%{_sysconfdir}/sysconfig/slapd

# move slapd out of _libdir
mv %{buildroot}%{_libdir}/slapd %{buildroot}%{_sbindir}/

# setup tools as symlinks to slapd
rm -f %{buildroot}%{_sbindir}/slap{acl,add,auth,cat,dn,index,passwd,test,schema}
rm -f %{buildroot}%{_libdir}/slap{acl,add,auth,cat,dn,index,passwd,test,schema}
for X in acl add auth cat dn index passwd test schema; do ln -s slapd %{buildroot}%{_sbindir}/slap$X ; done

# tweak permissions on the libraries to make sure they're correct
chmod 0755 %{buildroot}%{_libdir}/lib*.so*
chmod 0644 %{buildroot}%{_libdir}/lib*.*a

# slapd.conf(5) is obsoleted since 2.3, see slapd-config(5)
# new configuration will be generated in %%post
mkdir -p %{buildroot}%{_datadir}
install -m 0755 -d %{buildroot}%{_datadir}/openldap-servers
install -m 0644 %SOURCE4 %{buildroot}%{_datadir}/openldap-servers/slapd.ldif
install -m 0750 -d %{buildroot}%{_sysconfdir}/openldap/slapd.d
rm -f %{buildroot}%{_sysconfdir}/openldap/slapd.conf
rm -f %{buildroot}%{_sysconfdir}/openldap/slapd.ldif

# move doc files out of _sysconfdir
mv %{buildroot}%{_sysconfdir}/openldap/schema/README README.schema
mv %{buildroot}%{_sysconfdir}/openldap/DB_CONFIG.example %{buildroot}%{_datadir}/openldap-servers/DB_CONFIG.example
chmod 0644 openldap-%{version}/servers/slapd/back-sql/rdbms_depend/timesten/*.sh
chmod 0644 %{buildroot}%{_datadir}/openldap-servers/DB_CONFIG.example

# remove files which we don't want packaged
rm -f %{buildroot}%{_libdir}/*.la
mv %{buildroot}%{_libdir}/openldap/check_password.so{,.tmp}
rm -f %{buildroot}%{_libdir}/openldap/*.so
mv %{buildroot}%{_libdir}/openldap/check_password.so{.tmp,}

rm -f %{buildroot}%{_localstatedir}/openldap-data/DB_CONFIG.example
rmdir %{buildroot}%{_localstatedir}/openldap-data

%post
# create certificate database
%{_libexecdir}/openldap/create-certdb.sh >&/dev/null || :

%postun
#update only on package erase
if [ $1 == 0 ]; then
    /sbin/ldconfig
fi

%pre servers

# create ldap user and group
getent group ldap &>/dev/null || groupadd -r -g 55 ldap
getent passwd ldap &>/dev/null || \
	useradd -r -g ldap -u 55 -d %{_sharedstatedir}/ldap -s /sbin/nologin -c "OpenLDAP server" ldap

if [ $1 -eq 2 ]; then
	# package upgrade

	old_version=$(rpm -q --qf=%%{version} openldap-servers)
	new_version=%{version}

	if [ "$old_version" != "$new_version" ]; then
		touch %{_sharedstatedir}/ldap/rpm_upgrade_openldap &>/dev/null
	fi
fi

exit 0


%post servers

/sbin/ldconfig -n %{_libdir}/openldap

%systemd_post slapd.service

# generate sample TLS certificate for server (will not replace)
%{_libexecdir}/openldap/generate-server-cert.sh -o &>/dev/null || :

# generate/upgrade configuration
if [ ! -f %{_sysconfdir}/openldap/slapd.d/cn=config.ldif ]; then
	if [ -f %{_sysconfdir}/openldap/slapd.conf ]; then
		%{_libexecdir}/openldap/convert-config.sh &>/dev/null
		mv %{_sysconfdir}/openldap/slapd.conf %{_sysconfdir}/openldap/slapd.conf.bak
	else
		%{_libexecdir}/openldap/convert-config.sh -f %{_datadir}/openldap-servers/slapd.ldif &>/dev/null
	fi
fi

start_slapd=0

# upgrade the database
if [ -f %{_sharedstatedir}/ldap/rpm_upgrade_openldap ]; then
	if %{systemctl_bin} --quiet is-active slapd.service; then
		%{systemctl_bin} stop slapd.service
		start_slapd=1
	fi

	%{_libexecdir}/openldap/upgrade-db.sh &>/dev/null
	rm -f %{_sharedstatedir}/ldap/rpm_upgrade_openldap
fi

# ensure ppolicy schema updated (bug #1487857)
if [ $1 -eq 2 ]; then
	if [ -f %{_sysconfdir}/openldap/slapd.d/cn=config.ldif ]; then
		%{_libexecdir}/openldap/update-ppolicy-schema.sh &>/dev/null
	fi
fi

# conversion from /etc/sysconfig/ldap to /etc/sysconfig/slapd
if [ $1 -eq 2 ]; then
	# we expect that 'ldap' will be renamed to 'ldap.rpmsave' after removing the old package
	if [ -r %{_sysconfdir}/sysconfig/ldap ]; then
		source %{_sysconfdir}/sysconfig/ldap &>/dev/null

		new_urls=
		[ "$SLAPD_LDAP" != "no" ]   && new_urls="$new_urls ldap:///"
		[ "$SLAPD_LDAPI" != "no" ]  && new_urls="$new_urls ldapi:///"
		[ "$SLAPD_LDAPS" == "yes" ] && new_urls="$new_urls ldaps:///"
		[ -n "$SLAPD_URLS" ]        && new_urls="$new_urls $SLAPD_URLS"

		failure=0
		cp -f %{_sysconfdir}/sysconfig/slapd %{_sysconfdir}/sysconfig/slapd.rpmconvert
		sed -i '/^#\?SLAPD_URLS=/s@.*@SLAPD_URLS="'"$new_urls"'"@' %{_sysconfdir}/sysconfig/slapd.rpmconvert &>/dev/null || failure=1
		[ -n "$SLAPD_OPTIONS" ] && \
			sed -i '/^#\?SLAPD_OPTIONS=/s@.*$@SLAPD_OPTIONS="'"$SLAPD_OPTIONS"'"@' %{_sysconfdir}/sysconfig/slapd.rpmconvert &>/dev/null || failure=1

		if [ $failure -eq 0 ]; then
			mv -f %{_sysconfdir}/sysconfig/slapd.rpmconvert %{_sysconfdir}/sysconfig/slapd
		else
			rm -f %{_sysconfdir}/sysconfig/slapd.rpmconvert
		fi
	fi
fi

# restart after upgrade
if [ $1 -ge 1 ]; then
	if [ $start_slapd -eq 1 ]; then
		%{systemctl_bin} start slapd.service &>/dev/null || :
	else
		%{systemctl_bin} condrestart slapd.service &>/dev/null || :
	fi
fi

exit 0

%preun servers

%systemd_preun slapd.service


%postun servers

/sbin/ldconfig ${_libdir}/openldap
%systemd_postun_with_restart slapd.service


%triggerun servers -- openldap-servers < 2.4.26-6

# migration from SysV to systemd
/usr/bin/systemd-sysv-convert --save slapd &>/dev/null || :
/usr/sbin/chkconfig --del slapd &>/dev/null || :
%{systemctl_bin} try-restart slapd.service &>/dev/null || :


%triggerin servers -- libdb

# libdb upgrade (setup for %%triggerun)
if [ $2 -eq 2 ]; then
	# we are interested in minor version changes (both versions of libdb are installed at this moment)
	if [ "$(rpm -q --qf="%%{version}\n" libdb | sed 's/\.[0-9]*$//' | sort -u | wc -l)" != "1" ]; then
		touch %{_sharedstatedir}/ldap/rpm_upgrade_libdb
	else
		rm -f %{_sharedstatedir}/ldap/rpm_upgrade_libdb
	fi
fi

exit 0


%triggerun servers -- libdb

# libdb upgrade (finish %%triggerin)
if [ -f %{_sharedstatedir}/ldap/rpm_upgrade_libdb ]; then
	if %{systemctl_bin} --quiet is-active slapd.service; then
		%{systemctl_bin} stop slapd.service
		start=1
	else
		start=0
	fi

	%{_libexecdir}/openldap/upgrade-db.sh &>/dev/null
	rm -f %{_sharedstatedir}/ldap/rpm_upgrade_libdb

	[ $start -eq 1 ] && %{systemctl_bin} start slapd.service &>/dev/null
fi

exit 0


%files
%doc openldap-%{version}/ANNOUNCEMENT
%doc openldap-%{version}/CHANGES
%doc openldap-%{version}/COPYRIGHT
%doc openldap-%{version}/LICENSE
%doc openldap-%{version}/README
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/certs
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%config(noreplace) %{_tmpfilesdir}/openldap.conf
%dir %{_libexecdir}/openldap/
%{_libexecdir}/openldap/create-certdb.sh
%{_libdir}/liblber-2.4*.so.*
%{_libdir}/libldap-2.4*.so.*
%{_libdir}/libldap_r-2.4*.so.*
%{_libdir}/libslapi-2.4*.so.*
%{_mandir}/man5/ldif.5*
%{_mandir}/man5/ldap.conf.5*

%files servers
%doc openldap-%{version}/contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%doc openldap-%{version}/doc/guide/admin/*.html
%doc openldap-%{version}/doc/guide/admin/*.png
%doc openldap-%{version}/servers/slapd/back-perl/SampleLDAP.pm
%doc openldap-%{version}/servers/slapd/back-perl/README.back_perl
%doc openldap-%{version}/servers/slapd/back-perl/README.back_perl
%doc ltb-project-openldap-ppolicy-check-password-%{check_password_version}/README.check_pwd
%doc README.schema
%config(noreplace) %dir %attr(0750,ldap,ldap) %{_sysconfdir}/openldap/slapd.d
%config(noreplace) %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/sysconfig/slapd
%config(noreplace) %{_tmpfilesdir}/slapd.conf
%config(noreplace) %{_sysconfdir}/openldap/check_password.conf
%dir %attr(0700,ldap,ldap) %{_sharedstatedir}/ldap
%dir %attr(-,ldap,ldap) %{_localstatedir}/run/openldap
%{_unitdir}/slapd.service
%{_datadir}/openldap-servers/
%{_libdir}/openldap/accesslog*
%{_libdir}/openldap/auditlog*
%{_libdir}/openldap/allop*
%{_libdir}/openldap/back_dnssrv*
%{_libdir}/openldap/back_ldap*
%{_libdir}/openldap/back_meta*
%{_libdir}/openldap/back_null*
%{_libdir}/openldap/back_passwd*
%{_libdir}/openldap/back_relay*
%{_libdir}/openldap/back_shell*
%{_libdir}/openldap/back_sock*
%{_libdir}/openldap/back_perl*
%{_libdir}/openldap/collect*
%{_libdir}/openldap/constraint*
%{_libdir}/openldap/dds*
%{_libdir}/openldap/deref*
%{_libdir}/openldap/dyngroup*
%{_libdir}/openldap/dynlist*
%{_libdir}/openldap/memberof*
%{_libdir}/openldap/pcache*
%{_libdir}/openldap/ppolicy*
%{_libdir}/openldap/refint*
%{_libdir}/openldap/retcode*
%{_libdir}/openldap/rwm*
%{_libdir}/openldap/seqmod*
%{_libdir}/openldap/pw-sha2*
%{_libdir}/openldap/smbk5pwd*
%{_libdir}/openldap/sssvlv*
%{_libdir}/openldap/syncprov*
%{_libdir}/openldap/translucent*
%{_libdir}/openldap/unique*
%{_libdir}/openldap/valsort*
%{_libdir}/openldap/check_password*
%{_libexecdir}/openldap/functions
%{_libexecdir}/openldap/convert-config.sh
%{_libexecdir}/openldap/check-config.sh
%{_libexecdir}/openldap/upgrade-db.sh
%{_libexecdir}/openldap/generate-server-cert.sh
%{_libexecdir}/openldap/update-ppolicy-schema.sh
%{_libexecdir}/openldap/mdb_*
%{_libexecdir}/openldap/man/man1/mdb_*
%{_sbindir}/sl*
%{_mandir}/man8/*
%{_mandir}/man5/slapd*.5*
%{_mandir}/man5/slapo-*.5*
# obsolete configuration
%ghost %config(noreplace,missingok) %attr(0640,ldap,ldap) %{_sysconfdir}/openldap/slapd.conf
%ghost %config(noreplace,missingok) %attr(0640,ldap,ldap) %{_sysconfdir}/openldap/slapd.conf.bak

%files servers-sql
%doc openldap-%{version}/servers/slapd/back-sql/docs/*
%doc openldap-%{version}/servers/slapd/back-sql/rdbms_depend
%{_libdir}/openldap/back_sql*

%files clients
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%doc openldap-%{version}/doc/drafts openldap-%{version}/doc/rfc
%{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Sat Jun  6 2020 Matus Honek <mhonek@redhat.com> - 2.4.44-22
- Fix CVE-2020-12243 openldap: denial of service via nested boolean expressions in LDAP search filters (#1838405)

* Tue Dec 18 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-21
- MozNSS Compat. Layer: Protect /tmp/openldap-tlsmc-* files (#1590184)

* Tue Aug 21 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-20
- Backport upstream fixes for ITS 7595 - add OpenSSL EC support (#1584922)

* Tue Aug 14 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-19
- Backport upstream fixes for ITS 7506 - fix OpenSSL DH params usage (#1584922)

* Thu Jun 21 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-18
- MozNSS Compat. Layer: Make log messages more clear (#1543955)
- Build with LDAP_USE_NON_BLOCKING_TLS (#1471039)

* Thu Jun 21 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-17
- MozNSS Compat. Layer: Fix memleaks reported by valgrind (#1575549)
- Reset OPTIND in libexec/functions for getopts to work in subsequent calls (#1564382)
- MozNSS Compat. Layer: Fix typos, and spelling in the README file header (#1543451)

* Wed Apr  4 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-16
- fix: back-ldap StartTLS short connection timeout with high latency connections (#1540336)

* Thu Mar 29 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-14
- MozNSS Compat. Layer: Enforce fail when cannot extract CA certs (#1547922)

* Wed Jan 31 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-13
- MozNSS Compat. Layer: fix recursive directory deletion (#1516409)
- MozNSS Compat. Layer: fix PIN disclaimer not always shown (#1516409)
- MozNSS Compat. Layer: fix incorrect parsing of CACertDir (#1533955)

* Thu Jan 11 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-12
- MozNSS Compat. Layer: Ensure consistency of a PEM dir before usage (#1516409)
  + Warn just before use of a PIN about key file extraction

* Wed Jan 10 2018 Matus Honek <mhonek@redhat.com> - 2.4.44-11
- MozNSS Compat. Layer: Enable usage of NSS DB with PEM cert/key (#1525485)
  + Fix a possible invalid dereference (covscan)

* Tue Nov 28 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-10
- Drop update-ppolicy-schema.sh scriptlet's output (#1487857)
- Fix issues in MozNSS compatibility layer (#1400578)
  + Force write file with fsync to avoid race conditions
  + Always filestamp both sql and dbm NSS DB variants to not rely on default DB type prefix
  + Allow missing cert and key which is a valid usecase
  + Create extraction folder only in /tmp to simplify selinux rules
  + Fix Covscan issues

* Fri Nov  3 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-9
- Build with OpenSSL and MozNSS compatibility layer instead of MozNSS (#1400578)

* Thu Nov  2 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-8
- fix: Upgrading to OpenLDAP >= 2.4.43 breaks server due to ppolicy changes (#1487857)

* Thu Nov  2 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-7
- fix: Manpage incorrectly states ./ldaprc config file is used (#1498841)

* Thu Nov  2 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-6
- fix: Upgrading openldap-servers does not restart slapd when rebasing (#1479309)

* Tue Jun  6 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-5
- fix CVE-2017-9287 openldap: Double free vulnerability in servers/slapd/back-mdb/search.c (#1458210)

* Fri Mar 24 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-4
- NSS: Include some CHACHA20POLY1305 ciphers (#1432907)

* Wed Mar 15 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-3
- NSS: re-register NSS_Shutdown callback (#1405354)

* Wed Mar 15 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-2
- Include MDB tools in openldap-servers (#1428740)

* Wed Jan  4 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-1
- Rebase to openldap-2.4.44 (#1386365)

* Wed Aug 17 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-13
- fix: Bad log levels in check_password module
- fix: We can't search expected entries from LDAP server
- fix: OpenLDAP ciphersuite parsing doesn't match OpenSSL ciphers man page
  + Add TLS_DHE_DSS_WITH_AES_256_GCM_SHA384 to list of ciphers
  + Add DH cipher string parsing option
  + Correct handling kECDH ciphers with aRSA or aECDSA

* Fri Jul  1 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-12
- fix: slapd crash in do_search (#1316450)
- fix: Setting olcTLSProtocolMin does not change supported protocols (#1249093)

* Mon May 30 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-11
- fix: correct inconsistent slapd.d directory permissions (#1255433)

* Mon May 30 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-10
- fix: slapd fails to start on boot (#1315958)
- fix: id_query option is not available after rebasing openldap to 2.4.39 (#1311832)
- Include sha2 module (#1292568)
- Compile AllOp together with other overlays (#990893)
- Missing mutex unlock in accesslog overlay (#1261003)
- ITS#8337 fix missing olcDbChecksum config attr (#1292590)
- ITS#8003 fix off-by-one in LDIF length (#1292619)

* Mon Feb 22 2016 Matúš Honěk <mhonek@redhat.com> - 2.4.40-9
- fix: nslcd segfaults due to incorrect mutex initialization (#1294385)

* Wed Sep 23 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-8
- NSS does not support string ordering (#1231522)
- implement and correct order of parsing attributes (#1231522)
- add multi_mask and multi_strength to correctly handle sets of attributes (#1231522)
- add new cipher suites and correct AES-GCM attributes (#1245279)
- correct DEFAULT ciphers handling to exclude eNULL cipher suites (#1245279)

* Mon Sep 14 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-7
- Merge two MozNSS cipher suite definition patches into one. (#1245279)
- Use what NSS considers default for DEFAULT cipher string. (#1245279)
- Remove unnecesary defaults from ciphers' definitions (#1245279)

* Tue Sep 01 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-6
- fix: OpenLDAP shared library destructor triggers memory leaks in NSPR (#1249977)

* Fri Jul 24 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-5
- enhancement: support TLS 1.1 and later (#1231522,#1160467)
- fix: openldap ciphersuite parsing code handles masks incorrectly (#1231522)
- fix the patch in commit da1b5c (fix: OpenLDAP crash in NSS shutdown handling) (#1231228)

* Mon Jun 29 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-4
- fix: rpm -V complains (#1230263) -- make the previous fix do what was intended

* Mon Jun 22 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-3
- fix: rpm -V complains (#1230263)

* Wed Jun  3 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-2
- fix: missing frontend database indexing (#1226600)

* Wed May 20 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-1
- new upstream release (#1147982)
- fix: PIE and RELRO check (#1092562)
- fix: slaptest doesn't convert perlModuleConfig lines (#1184585)
- fix: OpenLDAP crash in NSS shutdown handling (#1158005)
- fix: slapd.service may fail to start if binding to NIC ip (#1198781)
- fix: deadlock during SSL_ForceHandshake when getting connection to replica (#1125152)
- improve check_password (#1174723, #1196243)
- provide an unversioned symlink to check_password.so.1.1 (#1174634)
- add findutils to requires (#1209229)

* Thu Dec  4 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-6
- refix: slapd.ldif olcFrontend missing important/required objectclass (#1132094)

* Fri Nov 28 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-5
- add documentation reference to service file (#1087288)
- fix: tls_reqcert try has bad behavior (#1027613)

* Tue Nov 25 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-4
- support TLS 1.1 and later (#1160468)
- fix: /etc/openldap/certs directory is empty after installation (#1064251)
- fix: Typo in script to generate /usr/libexec/openldap/generate-server-cert.sh (#1087490)
- fix: remove correct tmp file when generating server cert (#1103101)
- fix: slapd.ldif olcFrontend missing important/required objectclass (#1132094)

* Wed Feb 26 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-3
- move tmpfiles config to correct location (#1069513)

* Wed Feb  5 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-2
- CVE-2013-4449: segfault on certain queries with rwm overlay (#1061405)

* Thu Jan 30 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-1
- new upstream release (#1040324)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.4.35-12
- Mass rebuild 2014-01-24

* Thu Jan 16 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.35-11
- fix: missing EOL at the end of default /etc/openldap/ldap.conf (#1053005)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4.35-10
- Mass rebuild 2013-12-27

* Tue Dec 17 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.35-9
- fix: more typos in manpages (#948562)

* Wed Nov 13 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.35-8
- fix: slaptest incorrectly handles 'include' directives containing a custom file (#1023415)

* Mon Oct 14 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.35-7
- fix: CLDAP is broken for IPv6 (#1007421)

* Wed Sep  4 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.35-6
- fix: typos in manpages (#948562)

* Fri Jun 14 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.35-5
- fix: using slaptest to convert slapd.conf to LDIF format ignores "loglevel 0"

* Thu May 09 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-4
- do not needlessly run ldconfig after installing openldap-devel
- fix: LDAPI with GSSAPI does not work if SASL_NOCANON=on (#960222)
- fix: lt_dlopen() with back_perl (#960048)

* Tue Apr 09 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-3
- fix: minor documentation fixes
- set SASL_NOCANON to on by default (#949864)
- remove trailing spaces

* Fri Apr 05 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-2
- drop the evolution patch

* Tue Apr 02 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-1
- new upstream release (#947235)
- fix: slapd.service should ensure that network is up before starting (#946921)
- fix: NSS related resource leak (#929357)

* Mon Mar 18 2013 Jan Synáček <jsynacek@redhat.com> 2.4.34-2
- fix: syncrepl push DELETE operation does not recover (#920482)
- run autoreconf every build, drop autoreconf patch (#926280)

* Mon Mar 11 2013 Jan Synáček <jsynacek@redhat.com> 2.4.34-1
- enable perl backend (#820547)
- package ppolicy-check-password (#829749)
- add perl specific BuildRequires
- fix bogus dates

* Wed Mar 06 2013 Jan Vcelak <jvcelak@fedoraproject.org> 2.4.34-1
- new upstream release (#917603)
- fix: slapcat segfaults if cn=config.ldif not present (#872784)
- use systemd-rpm macros in spec file (#850247)

* Thu Jan 31 2013 Jan Synáček <jsynacek@redhat.com> 2.4.33-4
- rebuild against new cyrus-sasl

* Wed Oct 31 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.33-3
- fix update: libldap does not load PEM certificate if certdb is used as TLS_CACERTDIR (#857455)

* Fri Oct 12 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.33-2
- fix: slapd with rwm overlay segfault following ldapmodify (#865685)

* Thu Oct 11 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.33-1
- new upstream release:
  + slapd: ACLs, syncrepl
  + backends: locking and memory management in MDB
  + manpages: slapo-refint
- patch update: MozNSS certificate database in SQL format cannot be used (#860317)
- fix: slapd.service should not use /tmp (#859019)

* Fri Sep 14 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.32-3
- fix: some TLS ciphers cannot be enabled (#852338)
- fix: connection hangs after fallback to second server when certificate hostname verification fails (#852476)
- fix: not all certificates in OpenSSL compatible CA certificate directory format are loaded (#852786)
- fix: MozNSS certificate database in SQL format cannot be used (#857373)
- fix: libldap does not load PEM certificate if certdb is used as TLS_CACERTDIR (#857455)

* Mon Aug 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.32-2
- enhancement: TLS, prefer private keys from authenticated slots
- enhancement: TLS, allow certificate specification including token name
- resolve TLS failures in replication in 389 Directory Server

* Wed Aug 01 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.32-1
- new upstream release
  + library: double free, SASL handling
  + tools: read SASL_NOCANON from config file
  + slapd: config index renumbering, duplicate error response
  + backends: various fixes in mdb, bdb/hdb, ldap
  + accesslog, syncprov: fix memory leaks in with replication
  + sha2: portability, thread safety, support SSHA256,384,512
  + documentation fixes

* Sat Jul 21 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-7
- fix: slapd refuses to set up TLS with self-signed PEM certificate (#842022)

* Fri Jul 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-6
- multilib fix: move libslapi from openldap-servers to openldap package

* Thu Jul 19 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-5
- fix: querying for IPv6 DNS records when IPv6 is disabled on the host (#835013)
- fix: smbk5pwd module computes invalid LM hashes (#841560)

* Wed Jul 18 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-4
- modify the package build process
  + fix autoconfig files to detect Mozilla NSS library using pkg-config
  + remove compiler flags which are not needed currently
  + build server, client and library together
  + avoid stray dependencies by using --as-needed linker flag
  + enable SLAPI interface in slapd

* Wed Jun 27 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-3
- update fix: count constraint broken when using multiple modifications (#795766)
- fix: invalid order of TLS shutdown operations (#808464)
- fix: TLS error messages overwriting in tlsm_verify_cert() (#810462)
- fix: reading pin from file can make all TLS connections hang (#829317)
- CVE-2012-2668: cipher suite selection by name can be ignored (#825875)
- fix: slapd fails to start on reboot (#829272)
- fix: default cipher suite is always selected (#828790)
- fix: less influence between individual TLS contexts:
  - replication with TLS does not work (#795763)
  - possibly others

* Fri May 18 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-2
- fix: nss-tools package is required by the base package, not the server subpackage
- fix: MozNSS CA certdir does not work together with PEM CA cert file (#819536)

* Tue Apr 24 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-1
- new upstream release
  + library: IPv6 url detection
  + library: rebinding to failed connections
  + server: various fixes in mdb backend
  + server: various fixes in replication
  + server: various fixes in overlays and minor backends
  + documentation fixes
- remove patches which were merged upstream

* Thu Apr 05 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.30-3
- rebuild due to libdb rebase

* Mon Mar 26 2012 Jan Synáček <jsynacek@redhat.com> 2.4.30-2
- fix: Re-binding to a failed connection can segfault (#784989)

* Thu Mar 01 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.30-1
- new upstream release
  + server: fixes in mdb backend
  + server: fixes in manual pages
  + server: fixes in syncprov, syncrepl, and pcache
- removed patches which were merged upstream

* Wed Feb 22 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-4
- fix: missing options in manual pages of client tools (#796232)
- fix: SASL_NOCANON option missing in ldap.conf manual page (#732915)

* Tue Feb 21 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-3
- fix: ldap_result does not succeed for sssd (#771484)
- Jan Synáček <jsynacek@redhat.com>:
  + fix: count constraint broken when using multiple modifications (#795766)

* Mon Feb 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-2
- fix update: provide ldif2ldbm, not ldib2ldbm (#437104)
- Jan Synáček <jsynacek@redhat.com>:
  + unify systemctl binary paths throughout the specfile and make them usrmove compliant
  + make path to chkconfig binary usrmove compliant

* Wed Feb 15 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-1
- new upstream release
  + MozNSS fixes
  + connection handling fixes
  + server: buxfixes in mdb backend
  + server: buxfixes in overlays (syncrepl, meta, monitor, perl, sql, dds, rwm)
- openldap-servers now provide ldib2ldbm (#437104)
- certificates management improvements
  + create empty Mozilla NSS certificate database during installation
  + enable builtin Root CA in generated database (#789088)
  + generate server certificate using Mozilla NSS tools instead of OpenSSL tools
  + fix: correct path to check-config.sh in service file (Jan Synáček <jsynacek@redhat.com>)
- temporarily disable certificates checking in check-config.sh script
- fix: check-config.sh get stuck when executing command as a ldap user

* Tue Jan 31 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.28-3
- fix: replication (syncrepl) with TLS causes segfault (#783431)
- fix: slapd segfaults when PEM certificate is used and key is not set (#772890)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.28-1
- new upstream release
  + server: support for delta-syncrepl in multi master replication
  + server: add experimental backend - MDB
  + server: dynamic configuration for passwd, perl, shell, sock, and sql backends
  + server: support passwords in APR1
  + library: support for Wahl (draft)
  + a lot of bugfixes
- remove patches which were merged upstream
- compile backends as modules (except BDB, HDB, and monitor)
- reload systemd daemon after installation

* Tue Nov 01 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-6
- package cleanup:
  + hardened build: switch from LDFLAGS to RPM macros
  + remove old provides and obsoletes
  + add new slapd maintainance scripts
  + drop defattr macros, clean up permissions in specfile
  + fix rpmlint warnings: macros in comments/changelog
  + fix rpmlint warnings: non UTF-8 documentation
  + rename environment file to be more consistent (ldap -> slapd)
- replace sysv initscript with systemd service file (#
- new format of environment file due to switch to systemd
  (automatic conversion is performed)
- patch OpenLDAP to skip empty command line arguments
  (arguments expansion in systemd works different than in shell)
- CVE-2011-4079: one-byte buffer overflow in slapd (#749324)

* Thu Oct 06 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-5
- rebuild: openldap does not work after libdb rebase (#743824)
- regression fix: openldap built without tcp_wrappers (#743213)

* Wed Sep 21 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-4
- new feature update: honor priority/weight with ldap_domain2hostlist (#733078)

* Mon Sep 12 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-3
- fix: SSL_ForceHandshake function is not thread safe (#701678)
- fix: allow unsetting of tls_* syncrepl options (#734187)

* Wed Aug 24 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-2
- security hardening: library needs partial RELRO support added (#733071)
- fix: NSS_Init* functions are not thread safe (#731112)
- fix: incorrect behavior of allow/try options of VerifyCert and TLS_REQCERT (#725819)
- fix: memleak - free the return of tlsm_find_and_verify_cert_key (#725818)
- fix: conversion of constraint overlay settings to cn=config is incorrect (#733067)
- fix: DDS overlay tolerance parametr doesn't function and breakes default TTL (#733069)
- manpage fix: errors in manual page slapo-unique (#733070)
- fix: matching wildcard hostnames in certificate Subject field does not work (#733073)
- new feature: honor priority/weight with ldap_domain2hostlist (#733078)
- manpage fix: wrong ldap_sync_destroy() prototype in ldap_sync(3) manpage (#717722)

* Sun Aug 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.4.26-1.1
- Rebuilt for rpm (#728707)

* Wed Jul 20 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-1
- rebase to new upstream release
- fix: memleak in tlsm_auth_cert_handler (#717730)

* Mon Jun 27 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.25-1
- rebase to new upstream release
- change default database type from BDB to HDB
- enable ldapi:/// interface by default
- set cn=config management ACLs for root user, SASL external schema (#712495)
- fix: server scriptlets require initscripts package (#716857)
- fix: connection fails if TLS_CACERTDIR doesn't exist but TLS_REQCERT
  is set to 'never' (#716854)
- fix: segmentation fault caused by double-free in ldapexop (#699683)
- fix: segmentation fault of client tool when input line in LDIF file
  is splitted but indented incorrectly (#716855)
- fix: segmentation fault of client tool when LDIF input file is not terminated
  by a new line character (#716858)

* Fri Mar 18 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-2
- new: system resource limiting for slapd using ulimit
- fix update: openldap can't use TLS after a fork() (#636956)
- fix: possible null pointer dereference in NSS implementation
- fix: openldap-servers upgrade hangs or do not upgrade the database (#664433)

* Mon Feb 14 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-1
- rebase to 2.4.24
- BDB backend switch from DB4 to DB5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-8
- fix update: openldap can't use TLS after a fork() (#636956)

* Tue Jan 25 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-7
- fix: openldap can't use TLS after a fork() (#636956)
- fix: openldap-server upgrade gets stuck when the database is damaged (#664433)

* Thu Jan 20 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-6
- fix: some server certificates refused with inadequate type error (#668899)
- fix: default encryption strength dropped in switch to using NSS (#669446)
- systemd compatibility: add configuration file (#656647, #668223)

* Thu Jan 06 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-5
- initscript: slaptest with '-u' to skip database opening (#667768)
- removed slurpd options from sysconfig/ldap
- fix: verification of self issued certificates (#657984)

* Mon Nov 22 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-4
- Mozilla NSS - implement full non-blocking semantics
  ldapsearch -Z hangs server if starttls fails (#652822)
- updated list of all overlays in slapd.conf (#655899)
- fix database upgrade process (#656257)

* Thu Nov 18 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-3
- add support for multiple prefixed Mozilla NSS database files in TLS_CACERTDIR
- reject non-file keyfiles in TLS_CACERTDIR (#652315)
- TLS_CACERTDIR precedence over TLS_CACERT (#652304)
- accept only files in hash.0 format in TLS_CACERTDIR (#650288)
- improve SSL/TLS trace messages (#652818)

* Mon Nov 01 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-2
- fix possible infinite loop when checking permissions of TLS files (#641946)
- removed outdated autofs.schema (#643045)
- removed outdated README.upgrade
- removed relics of migrationtools

* Fri Aug 27 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-1
- rebase to 2.4.23
- embeded db4 library removed
- removed bogus links in "SEE ALSO" in several man-pages (#624616)

* Thu Jul 22 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.22-7
- Mozilla NSS - delay token auth until needed (#616552)
- Mozilla NSS - support use of self signed CA certs as server certs (#614545)

* Tue Jul 20 2010 Jan Vcelak <jvcelak@redhat.com> - 2.4.22-6
- CVE-2010-0211 openldap: modrdn processing uninitialized pointer free (#605448)
- CVE-2010-0212 openldap: modrdn processing IA5StringNormalize NULL pointer dereference (#605452)
- obsolete configuration file moved to /usr/share/openldap-servers (#612602)

* Thu Jul 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-5
- another shot at previous fix

* Thu Jul 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-4
- fixed issue with owner of /usr/lib/ldap/__db.* (#609523)

* Thu Jun  3 2010 Rich Megginson <rmeggins@redhat.com> - 2.4.22-3
- added ldif.h to the public api in the devel package
- added -lldif to the public api
- added HAVE_MOZNSS and other flags to use Mozilla NSS for crypto

* Tue May 18 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-2
- rebuild with connectionless support (#587722)
- updated autofs schema (#584808)

* Tue May 04 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-1
- rebased to 2.4.22 (mostly bugfixes, added back-ldif, back-null testing support)
- due to some possible issues pointed out in last update testing phase, I'm
  pulling back the last change (slapd can't be moved since it depends on /usr
  possibly mounted from network)

* Fri Mar 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-6
- moved slapd to start earlier during boot sequence

* Tue Mar 16 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-5
- minor corrections of init script (#571235, #570057, #573804)

* Wed Feb 24 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-4
- fixed SIGSEGV when deleting data using hdb (#562227)

* Mon Feb 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-3
- fixed broken link /usr/sbin/slapschema (#559873)

* Tue Jan 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-2
- removed some static libraries from openldap-devel (#556090)

* Mon Jan 11 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-1
- rebased openldap to 2.4.21
- rebased bdb to 4.8.26

* Mon Nov 23 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-3
- minor corrections in init script

* Mon Nov 16 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-2
- fixed tls connection accepting when TLSVerifyClient = allow
- /etc/openldap/ldap.conf removed from files owned by openldap-servers
- minor changes in spec file to supress warnings
- some changes in init script, so it would be possible to use it when
  using old configuration style

* Fri Nov 06 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-1
- rebased openldap to 2.4.19
- rebased bdb to 4.8.24

* Wed Oct 07 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-4
- updated smbk5pwd patch to be linked with libldap (#526500)
- the last buffer overflow patch replaced with the one from upstream
- added /etc/openldap/slapd.d and /etc/openldap/slapd.conf.bak
  to files owned by openldap-servers

* Thu Sep 24 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-3
- cleanup of previous patch fixing buffer overflow

* Tue Sep 22 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-2
- changed configuration approach. Instead od slapd.conf slapd
  is using slapd.d directory now
- fix of some issues caused by renaming of init script
- fix of buffer overflow issue in ldif.c pointed out by new glibc

* Fri Sep 18 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-1
- rebase of openldap to 2.4.18

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-7
- updated documentation (hashing the cacert dir)

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-6
- updated init script to be LSB-compliant (#523434)
- init script renamed to slapd

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.4.16-5
- rebuilt with new openssl

* Tue Aug 25 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-4
- updated %%pre script to correctly install openldap group

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-1
- rebase of openldap to 2.4.16
- fixed minor issue in spec file (output looking interactive
  when installing servers)

* Tue Jun 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-4
- added $SLAPD_URLS variable to init script (#504504)

* Thu Apr 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-3
- extended previous patch (#481310) to remove options cfMP
  from some client tools
- correction of patch setugid (#494330)

* Thu Mar 26 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-2
- removed -f option from some client tools (#481310)

* Wed Feb 25 2009 Jan Safranek <jsafranek@redhat.com> 2.4.15-1
- new upstream release

* Tue Feb 17 2009 Jan Safranek <jsafranek@redhat.com> 2.4.14-1
- new upstream release
- upgraded to db-4.7.25

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 2.4.12-3
- rebuild with new openssl

* Mon Dec 15 2008 Caolán McNamara <caolanm@redhat.com> 2.4.12-2
- rebuild for libltdl, i.e. copy config.sub|guess from new location

* Wed Oct 15 2008 Jan Safranek <jsafranek@redhat.com> 2.4.12-1
- new upstream release

* Mon Oct 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-3
- add SLAPD_SHUTDOWN_TIMEOUT to /etc/sysconfig/ldap, allowing admins
  to set non-default slapd shutdown timeout
- add checkpoint to default slapd.conf file (#458679)

* Mon Sep  1 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-2
- provide ldif2ldbm functionality for migrationtools
- rediff all patches to get rid of patch fuzz

* Mon Jul 21 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-1
- new upstream release
- apply official bdb-4.6.21 patches

* Wed Jul  2 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-2
- fix CVE-2008-2952 (#453728)

* Thu Jun 12 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-1
- new upstream release

* Wed May 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-5
- use /sbin/nologin as shell of ldap user (#447919)

* Tue May 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-4
- new upstream release
- removed unnecessary MigrationTools patches

* Thu Apr 10 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-4
- bdb upgraded to 4.6.21
- reworked upgrade logic again to run db_upgrade when bdb version
  changes

* Wed Mar  5 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-3
- reworked the upgrade logic, slapcat/slapadd of the whole database
  is needed only if minor version changes (2.3.x -> 2.4.y)
- do not try to save database in LDIF format, if openldap-servers package
  is  being removed (it's up to the admin to do so manually)

* Thu Feb 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-2
- migration tools carved out to standalone package "migrationtools"
  (#236697)

* Fri Feb 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-1
- new upstream release

* Fri Feb  8 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-7
- fix CVE-2008-0658 (#432014)

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-6
- init script fixes

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-5
- init script made LSB-compliant (#247012)

* Fri Jan 25 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-4
- fixed rpmlint warnings and errors
  - /etc/openldap/schema/README moved to /usr/share/doc/openldap

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-3
- obsoleting compat-openldap properly again :)

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-2
- obsoleting compat-openldap properly (#429591)

* Mon Jan 14 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-1
- new upstream version (openldap-2.4.7)

* Mon Dec  3 2007 Jan Safranek <jsafranek@redhat.com> 2.4.6-1
- new upstream version (openldap-2.4)
- deprecating compat- package

* Mon Nov  5 2007 Jan Safranek <jsafranek@redhat.com> 2.3.39-1
- new upstream release

* Tue Oct 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-4
- fixed multilib issues - all platform independent files have the
  same content now (#342791)

* Thu Oct  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-3
- BDB downgraded back to 4.4.20 because 4.6.18 is not supported by
  openldap (#314821)

* Mon Sep 17 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-2
- skeleton /etc/sysconfig/ldap added
- new SLAPD_LDAP option to turn off listening on ldap:/// (#292591)
- fixed checking of SSL (#292611)
- fixed upgrade with empty database

* Thu Sep  6 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-1
- new upstream version
- added images to the guide.html (#273581)

* Wed Aug 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-3
- just rebuild

* Thu Aug  2 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-2
- do not use specific automake and autoconf
- do not distinguish between NPTL and non-NPTL platforms, we have NPTL
  everywhere
- db-4.6.18 integrated
- updated openldap-servers License: field to reference BDB license

* Tue Jul 31 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-1
- new upstream version

* Fri Jul 20 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-7
- MigrationTools-47 integrated

* Wed Jul  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-6
- fix compat-slapcat compilation. Now it can be found in
  /usr/lib/compat-openldap/slapcat, because the tool checks argv[0]
  (#246581)

* Fri Jun 29 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-5
- smbk5pwd added (#220895)
- correctly distribute modules between servers and servers-sql packages

* Mon Jun 25 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-4
- Fix initscript return codes (#242667)
- Provide overlays (as modules; #246036, #245896)
- Add available modules to config file

* Tue May 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-3
- do not create script in /tmp on startup (bz#188298)
- add compat-slapcat to openldap-compat (bz#179378)
- do not import ddp services with migrate_services.pl
  (bz#201183)
- sort the hosts by adders, preventing duplicities
  in migrate*nis*.pl (bz#201540)
- start slupd for each replicated database (bz#210155)
- add ldconfig to devel post/postun (bz#240253)
- include misc.schema in default slapd.conf (bz#147805)

* Mon Apr 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-2
- slapadd during package update is now quiet (bz#224581)
- use _localstatedir instead of var/ during build (bz#220970)
- bind-libbind-devel removed from BuildRequires (bz#216851)
- slaptest is now quiet during service ldap start, if
  there is no error/warning (bz#143697)
- libldap_r.so now links with pthread (bz#198226)
- do not strip binaries to produce correct .debuginfo packages
  (bz#152516)

* Mon Feb 19 2007 Jay Fenlason <fenlason<redhat.com> 2.3.34-1
- New upstream release
- Upgrade the scripts for migrating the database so that they might
  actually work.
- change bind-libbind-devel to bind-devel in BuildPreReq

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> 2.3.30-1.1
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Wed Nov 15 2006 Jay Fenlason <fenlason@redhat.com> 2.3.30-1
- New upstream version

* Wed Oct 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.28-1
- New upstream version

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.3.27-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-3
- Include --enable-multimaster to close
  bz#185821: adding slapd_multimaster to the configure options
- Upgade guide.html to the correct one for openladp-2.3.27, closing
  bz#190383: openldap 2.3 packages contain the administrator's guide for 2.2
- Remove the quotes from around the slaptestflags in ldap.init
  This closes one part of
  bz#204593: service ldap fails after having added entries to ldap
- include __db.* in the list of files to check ownership of in
  ldap.init, as suggested in
  bz#199322: RFE: perform cleanup in ldap.init

* Fri Aug 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-2
- New upstream release
- Include the gethostbyname_r patch so that nss_ldap won't hang
  on recursive attemts to ldap_initialize.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.24-2.1
- rebuild

* Wed Jun 7 2006 Jay Fenlason <fenlason@redhat.com> 2.3.24-2
- New upstream version

* Thu Apr 27 2006 Jay Fenlason <fenlason@redhat.com> 2.3.21-2
- Upgrade to 2.3.21
- Add two upstream patches for db-4.4.20

* Mon Feb 13 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-4
- Re-fix ldap.init

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-3.1
- bump again for double-long bug on ppc(64)

* Thu Feb 9 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-3
- Modify the ldap.init script to call runuser correctly.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-2
- Upgrade to 2.3.19, which upstream now considers stable
- Modify the -config.patch, ldap.init, and this spec file to put the
  pid file and args file in an ldap-owned openldap subdirectory under
  /var/run.
- Move back_sql* out of _sbindir/openldap , which requires
  hand-moving slapd and slurpd to _sbindir, and recreating symlinks
  by hand.
- Retire openldap-2.3.11-ads.patch, which went upstream.
- Update the ldap.init script to run slaptest as the ldap user rather
  than as root.  This solves
  bz#150172 Startup failure after database problem
- Add to the servers post and preun scriptlets so that on preun, the
  database is slapcatted to /var/lib/ldap/upgrade.ldif and the
  database files are saved to /var/lib/ldap/rpmorig.  On post, if
  /var/lib/ldap/upgrade.ldif exists, it is slapadded.  This means that
  on upgrades from 2.3.16-2 to higher versions, the database files may
  be automatically upgraded.  Unfortunatly, because of the changes to
  the preun scriptlet, users have to do the slapcat, etc by hand when
  upgrading to 2.3.16-2.  Also note that the /var/lib/ldap/rpmorig
  files need to be removed by hand because automatically removing your
  emergency fallback files is a bad idea.
- Upgrade internal bdb to db-4.4.20.  For a clean upgrade, this will
  require that users slapcat their databases into a temp file, move
  /var/lib/ldap someplace safe, upgrade the openldap rpms, then
  slapadd the temp file.


* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-3
- Remove Requires: cyrus-sasl and cyrus-sasl-md5 from openldap- and
  compat-openldap- to close
  bz#173313 Remove exlicit 'Requires: cyrus-sasl" + 'Requires: cyrus-sasl-md5'

* Thu Nov 10 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-2
- Upgrade to 2.3.11, which upstream now considers stable.
- Switch compat-openldap to 2.2.29
- remove references to nss_ldap_build from the spec file
- remove references to 2.0 and 2.1 from the spec file.
- reorganize the build() function slightly in the spec file to limit the
  number of redundant and conflicting options passedto configure.
- Remove the attempt to hardlink ldapmodify and ldapadd together, since
  the current make install make ldapadd a symlink to ldapmodify.
- Include the -ads patches to allow SASL binds to an Active Directory
  server to work.  Nalin <nalin@redhat.com> wrote the patch, based on my
  broken first attempt.

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2.2.29-3
- rebuilt against new openssl

* Mon Oct 10 2005 Jay Fenlason <fenlason@redhat.com> 2.2.29-2
- New upstream version.

* Thu Sep 29 2005 Jay Fenlason <fenlason@redhat.com> 2.2.28-2
- Upgrade to nev upstream version.  This makes the 2.2.*-hop patch obsolete.

* Mon Aug 22 2005 Jay Fenlason <fenlason@redhat.com> 2.2.26-2
- Move the slapd.pem file to /etc/pki/tls/certs
  and edit the -config patch to match to close
  bz#143393  Creates certificates + keys at an insecure/bad place
- also use _sysconfdir instead of hard-coding /etc

* Thu Aug 11 2005 Jay Fenlason <fenlason@redhat.com>
- Add the tls-fix-connection-test patch to close
  bz#161991 openldap password disclosure issue
- add the hop patches to prevent infinite looping when chasing referrals.
  OpenLDAP ITS #3578

* Fri Aug  5 2005 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in ldap.init (call $klist instead of klist, from Charles Lopes)

* Thu May 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.26-1
- run slaptest with the -u flag if no id2entry db files are found, because
  you can't check for read-write access to a non-existent database (#156787)
- add _sysconfdir/openldap/cacerts, which authconfig sets as the
  TLS_CACERTDIR path in /etc/openldap/ldap.conf now
- use a temporary wrapper script to launch slapd, in case we have arguments
  with embedded whitespace (#158111)

* Wed May  4 2005 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.26 (stable 20050429)
- enable the lmpasswd scheme
- print a warning if slaptest fails, slaptest -u succeeds, and one of the
  directories listed as the storage location for a given suffix in slapd.conf
  contains a readable file named __db.001 (#118678)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.25-1
- update to 2.2.25 (release)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.24-1
- update to 2.2.24 (stable 20050318)
- export KRB5_KTNAME in the init script, in case it was set in the sysconfig
  file but not exported

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-4
- prefer libresolv to libbind

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-3
- add bind-libbind-devel and libtool-ltdl-devel buildprereqs

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 2.2.23-2
- rebuild with openssl-0.9.7e

* Mon Jan 31 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-1
- update to 2.2.23 (stable-20050125)
- update notes on upgrading from earlier versions
- drop slapcat variations for 2.0/2.1, which choke on 2.2's config files

* Tue Jan  4 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.20-1
- update to 2.2.20 (stable-20050103)
- warn about unreadable krb5 keytab files containing "ldap" keys
- warn about unreadable TLS-related files
- own a ref to subdirectories which we create under _libdir/tls

* Tue Nov  2 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.17-0
- rebuild

* Thu Sep 30 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.17 (stable-20040923) (#135188)
- move nptl libraries into arch-specific subdirectories on x86 boxes
- require a newer glibc which can provide nptl libpthread on i486/i586

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com>
- move slapd startup to earlier in the boot sequence (#103160)
- update to 2.2.15 (stable-20040822)
- change version number on compat-openldap to include the non-compat version
  from which it's compiled, otherwise would have to start 2.2.15 at release 3
  so that it upgrades correctly

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-2
- build a separate, static set of libraries for openldap-devel with the
  non-standard ntlm bind patch applied, for use by the evolution-connector
  package (#125579), and installing them under
  evolution_connector_prefix)
- provide openldap-evolution-devel = version-release in openldap-devel
  so that evolution-connector's source package can require a version of
  openldap-devel which provides what it wants

* Mon Jul 26 2004 Nalin Dahyabhai <nalin@redhat.com>
- update administrator guide

* Wed Jun 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-1
- add compat-openldap subpackage
- default to bdb, as upstream does, gambling that we're only going to be
  on systems with nptl now

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-0
- preliminary 2.2.13 update
- move ucdata to the -servers subpackage where it belongs

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-1
- build experimental sql backend as a loadable module

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-0
- update to 2.1.30

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.1.29-3
- removed rpath
- added pie patch: slapd and slurpd are now pie
- requires libtool >= 1.5.6-2 (PIC libltdl.a)

* Fri Apr 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-2
- move rfc documentation from main to -devel (#121025)

* Wed Apr 14 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-1
- rebuild

* Tue Apr  6 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-0
- update to 2.1.29 (stable 20040329)

* Mon Mar 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- don't build servers with --with-kpasswd, that option hasn't been recognized
  since 2.1.23

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 2.1.25-5.1
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 2.1.25-5
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-4
- remove 'reload' from the init script -- it never worked as intended (#115310)

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-3
- commit that last fix correctly this time

* Tue Feb  3 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-2
- fix incorrect use of find when attempting to detect a common permissions
  error in the init script (#114866)

* Fri Jan 16 2004 Nalin Dahyabhai <nalin@redhat.com>
- add bug fix patch for DB 4.2.52

* Thu Jan  8 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-1
- change logging facility used from daemon to local4 (#112730, reversing #11047)
  BEHAVIOR CHANGE - SHOULD BE MENTIONED IN THE RELEASE NOTES.

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fix for logic quasi-bug in slapd's SASL auxprop code (Dave Jones)

* Thu Dec 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.25, now marked STABLE

* Thu Dec 11 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-9
- update to db-4.2.52.

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-8
- add another section to the ABI note for the TLS libdb so that it's marked as
  not needing an executable stack (from Arjan Van de Ven)

* Thu Oct 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-7
- force bundled libdb to not use O_DIRECT by making it forget that we have it

* Wed Oct 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- build bundled libdb for slapd dynamically to make the package smaller,
  among other things
- on tls-capable arches, build libdb both with and without shared posix
  mutexes, otherwise just without
- disable posix mutexes unconditionally for db 4.0, which shouldn't need
  them for the migration cases where it's used
- update to MigrationTools 45

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-6.1
- upgrade db-4.1.25 to db-4.2.42.

* Fri Sep 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-6
- drop rfc822-MailMember.schema, merged into upstream misc.schema at some point

* Wed Aug 27 2003 Nalin Dahyabhai <nalin@redhat.com>
- actually require newer libtool, as was intended back in 2.1.22-0, noted as
  missed by Jim Richardson

* Fri Jul 25 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-5
- enable rlookups, they don't cost anything unless also enabled in slapd's
  configuration file

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-4
- rebuild

* Thu Jul 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-3
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-2
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-1
- build

* Mon Jul 14 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-0
- 2.1.22 now badged stable
- be more aggressive in what we index by default
- use/require libtool 1.5

* Mon Jun 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.22

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-1
- update to 2.1.21
- enable ldap, meta, monitor, null, rewrite in slapd

* Mon May 19 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-1
- update to 2.1.20

* Thu May  8 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-1
- update to 2.1.19

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-1
- switch to db with crypto

* Fri May  2 2003 Nalin Dahyabhai <nalin@redhat.com>
- install the db utils for the bundled libdb as %%{_sbindir}/slapd_db_*
- install slapcat/slapadd from 2.0.x for migration purposes

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.17
- disable the shell backend, not expected to work well with threads
- drop the kerberosSecurityObject schema, the krbName attribute it
  contains is only used if slapd is built with v2 kbind support

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-8
- back down to db 4.0.x, which 2.0.x can compile with in ldbm-over-db setups
- tweak SuSE patch to fix a few copy-paste errors and a NULL dereference

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-6
- rebuild

* Mon Dec 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-5
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-4
- check for setgid as well

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-3
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fixes from SuSE's security audit, except for fixes to ITS 1963,
  1936, 2007, 2009, which were included in 2.0.26.
- add two more patches for db 4.1.24 from sleepycat's updates page
- use openssl pkgconfig data, if any is available

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-2
- add patches for db 4.1.24 from sleepycat's updates page

* Mon Nov  4 2002 Nalin Dahyabhai <nalin@redhat.com>
- add a sample TLSCACertificateFile directive to the default slapd.conf

* Tue Sep 24 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-1
- update to 2.0.27

* Fri Sep 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.26-1
- update to 2.0.26, db 4.1.24.NC

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-2
- change LD_FLAGS to refer to /usr/kerberos/_libdir instead of
  /usr/kerberos/lib, which might not be right on some arches

* Mon Aug 26 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-1
- update to 2.0.25 "stable", ldbm-over-gdbm (putting off migration of LDBM
  slapd databases until we move to 2.1.x)
- use %%{_smp_mflags} when running make
- update to MigrationTools 44
- enable dynamic module support in slapd

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-5
- rebuild in new environment

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-3
- use the gdbm backend again

* Mon Feb 18 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-2
- make slapd.conf read/write by root, read by ldap

* Sun Feb 17 2002 Nalin Dahyabhai <nalin@redhat.com>
- fix corner case in sendbuf fix
- 2.0.23 now marked "stable"

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-1
- update to 2.0.23

* Fri Feb  8 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-2
- switch to an internalized Berkeley DB as the ldbm back-end  (NOTE: this breaks
  access to existing on-disk directory data)
- add slapcat/slapadd with gdbm for migration purposes
- remove Kerberos dependency in client libs (the direct Kerberos dependency
  is used by the server for checking {kerberos} passwords)

* Fri Feb  1 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-1
- update to 2.0.22

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.0.21-5
- prereq chkconfig for server subpackage

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-4
- update migration tools to version 40

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-3
- free ride through the build system

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-2
- update to 2.0.21, now earmarked as STABLE

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-2
- temporarily disable optimizations for ia64 arches
- specify pthreads at configure-time instead of letting configure guess

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com>
- and one for Raw Hide

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-0.7
- build for RHL 7/7.1

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-1
- update to 2.0.20 (security errata)

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.19-1
- update to 2.0.19

* Tue Nov  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-2
- fix the commented-out replication example in slapd.conf

* Fri Oct 26 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-1
- update to 2.0.18

* Mon Oct 15 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.17-1
- update to 2.0.17

* Wed Oct 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable kbind support (deprecated, and I suspect unused)
- configure with --with-kerberos=k5only instead of --with-kerberos=k5
- build slapd with threads

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-2
- rebuild, 2.0.15 is now designated stable

* Fri Sep 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-1
- update to 2.0.15

* Mon Sep 10 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.14-1
- update to 2.0.14

* Fri Aug 31 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.12-1
- update to 2.0.12 to pull in fixes for setting of default TLS options, among
  other things
- update to migration tools 39
- drop tls patch, which was fixed better in this release

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.11-13
- install saucer correctly

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to fix ldap_set_options not being able to set global options related
  to TLS correctly

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't attempt to create a cert at install-time, it's usually going
  to get the wrong CN (#51352)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a build-time requirement on pam-devel
- add a build-time requirement on a sufficiently-new libtool to link
  shared libraries to other shared libraries (which is needed in order
  for prelinking to work)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- require cyrus-sasl-md5 (support for DIGEST-MD5 is required for RFC
  compliance) by name (follows from #43079, which split cyrus-sasl's
  cram-md5 and digest-md5 modules out into cyrus-sasl-md5)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable passwd back-end (noted by Alan Sparks and Sergio Kessler)

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- start to prep for errata release

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- link libldap with liblber

* Wed Jul  4 2001 Than Ngo <than@redhat.com> 2.0.11-6
- add symlink liblber.so libldap.so and libldap_r.so in /usr/lib

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move shared libraries to /lib
- redo init script for better internationalization (#26154)
- don't use ldaprc files in the current directory (#38402) (patch from
  hps@intermeta.de)
- add BuildPrereq on tcp wrappers since we configure with
  --enable-wrappers (#43707)
- don't overflow debug buffer in mail500 (#41751)
- don't call krb5_free_creds instead of krb5_free_cred_contents any
  more (#43159)

* Mon Jul  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- make config files noreplace (#42831)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually change the default config to use the dummy cert
- update to MigrationTools 38

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- build dummy certificate in %%post, use it in default config
- configure-time shenanigans to help a confused configure script

* Wed Jun 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak migrate_automount and friends so that they can be run from anywhere

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.11

* Wed May 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.10

* Mon May 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.9

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.8
- drop patch which came from upstream

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- back out pidfile patches, which interact weirdly with Linux threads
- mark non-standard schema as such by moving them to a different directory

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to MigrationTools 36, adds netgroup support

* Mon Jan 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix thinko in that last patch

* Thu Jan 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to work around some buffering problems

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Fri Jan 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- move the RFCs to the base package (#21701)
- update to MigrationTools 34

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- add support for additional OPTIONS, SLAPD_OPTIONS, and SLURPD_OPTIONS in
  a /etc/sysconfig/ldap file (#23549)

* Fri Dec 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object OID from 1.3.6.1.1.1.2.9 to 1.3.6.1.1.1.2.13,
  per mail from the ldap-nis mailing list

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC so that shared libraries don't fall over

* Mon Dec  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Norbert Klasen's patch (via Del) to fix searches using ldaps URLs
  (OpenLDAP ITS #889)
- add "-h ldaps:///" to server init when TLS is enabled, in order to support
  ldaps in addition to the regular STARTTLS (suggested by Del)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- correct mismatched-dn-cn bug in migrate_automount.pl

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the correct OIDs for automount and automountInformation
- add notes on upgrading

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.7
- drop chdir patch (went mainstream)

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object classes from auxiliary to structural

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to Migration Tools 27
- change the sense of the last simple patch

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- reorganize the patch list to separate MigrationTools and OpenLDAP patches
- switch to Luke Howard's rfc822MailMember schema instead of the aliases.schema
- configure slapd to run as the non-root user "ldap" (#19370)
- chdir() before chroot() (we don't use chroot, though) (#19369)
- disable saving of the pid file because the parent thread which saves it and
  the child thread which listens have different pids

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add missing required attributes to conversion scripts to comply with schema
- add schema for mail aliases, autofs, and kerberosSecurityObject rooted in
  our own OID tree to define attributes and classes migration scripts expect
- tweak automounter migration script

* Mon Oct  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- try adding the suffix first when doing online migrations
- force ldapadd to use simple authentication in migration scripts
- add indexing of a few attributes to the default configuration
- add commented-out section on using TLS to default configuration

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.6
- add buildprereq on cyrus-sasl-devel, krb5-devel, openssl-devel
- take the -s flag off of slapadd invocations in migration tools
- add the cosine.schema to the default server config, needed by inetorgperson

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the nis.schema and inetorgperson.schema to the default server config
- make ldapadd a hard link to ldapmodify because they're identical binaries

* Fri Sep 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.4

* Fri Sep 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove prereq on /etc/init.d (#17531)
- update to 2.0.3
- add saucer to the included clients

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.1

* Fri Sep  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.0
- patch to build against MIT Kerberos 1.1 and later instead of 1.0.x

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove that pesky default password
- change "Copyright:" to "License:"

* Sun Aug 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- adjust permissions in files lists
- move libexecdir from %%{_prefix}/sbin to %%{_sbindir}

* Fri Aug 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add migrate_automount.pl to the migration scripts set

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- build a semistatic slurpd with threads, everything else without
- disable reverse lookups, per email on OpenLDAP mailing lists
- make sure the execute bits are set on the shared libraries

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- change logging facility used from local4 to daemon (#11047)

* Thu Jul 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off clients and servers to shrink down the package and remove the
  base package's dependency on Perl
- make certain that the binaries have sane permissions

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the init script back

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the init script to only source /etc/sysconfig/network if it's found

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch to gdbm; I'm getting off the db merry-go-round
- tweak the init script some more
- add instdir to @INC in migration scripts

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak init script to return error codes properly
- change initscripts dependency to one on /etc/init.d

* Tue Jul  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- prereq initscripts
- make migration scripts use mktemp

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- do condrestart in post and stop in preun
- move init script to /etc/init.d

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.11
- add condrestart logic to init script
- munge migration scripts so that you don't have to be
  /usr/share/openldap/migration to run them
- add code to create pid files in /var/run

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS tweaks
- fix for compiling with libdb2

* Thu May  4 2000 Bill Nottingham <notting@redhat.com>
- minor tweak so it builds on ia64

* Wed May  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- more minimalistic fix for bug #11111 after consultation with OpenLDAP team
- backport replacement for the ldapuser patch

* Tue May  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix segfaults from queries with commas in them in in.xfingerd (bug #11111)

* Tue Apr 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.10
- add revamped version of patch from kos@bastard.net to allow execution as
  any non-root user
- remove test suite from %%build because of weirdness in the build system

* Wed Apr 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the defaults for databases and whatnot to /var/lib/ldap (bug #10714)
- fix some possible string-handling problems

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- start earlier, stop later.

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- auto rebuild in new environment (release 4)

* Tue Feb  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add -D_REENTRANT to make threaded stuff more stable, even though it looks
  like the sources define it, too
- mark *.ph files in migration tools as config files

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.9

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip files

* Sat Sep 11 1999 Bill Nottingham <notting@redhat.com>
- update to 1.2.7
- fix some bugs from bugzilla (#4885, #4887, #4888, #4967)
- take include files out of base package

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- missing ;; in init script reload) (#4734).

* Tue Aug 24 1999 Cristian Gafton <gafton@redhat.com>
- move stuff from /usr/libexec to /usr/sbin
- relocate config dirs to /etc/openldap

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- add the migration tools to the package

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- upgrade to 1.2.6
- add rc.d script
- split -devel package

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to latest stable (1.1.4), it now uses configure macro.

* Fri Jan 15 1999 Bill Nottingham <notting@redhat.com>
- build on arm, glibc2.1

* Wed Oct 28 1998 Preston Brown <pbrown@redhat.com>
- initial cut.
- patches for signal handling on the alpha
