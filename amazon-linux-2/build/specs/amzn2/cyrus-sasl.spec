%define username	saslauth
%define hint		Saslauthd user
%define homedir		/run/saslauthd

%define _plugindir2 %{_libdir}/sasl2
%define bootstrap_cyrus_sasl 0

%global _performance_build 1

Summary: The Cyrus SASL library
Name: cyrus-sasl
Version: 2.1.26
Release: 23%{?dist}
License: BSD with advertising
Group: System Environment/Libraries
# Source0 originally comes from ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/;
# make-no-dlcompatorsrp-tarball.sh removes the "dlcompat" subdirectory and builds a
# new tarball.
Source0: cyrus-sasl-%{version}-nodlcompatorsrp.tar.gz
Source5: saslauthd.service
Source7: sasl-mechlist.c
Source8: sasl-checkpass.c
Source9: saslauthd.sysconfig
Source10: make-no-dlcompatorsrp-tarball.sh
URL: http://asg.web.cmu.edu/sasl/sasl-library.html
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Patch11: cyrus-sasl-2.1.25-no_rpath.patch
Patch15: cyrus-sasl-2.1.20-saslauthd.conf-path.patch
Patch23: cyrus-sasl-2.1.23-man.patch
Patch24: cyrus-sasl-2.1.21-sizes.patch
Patch31: cyrus-sasl-2.1.22-kerberos4.patch
Patch32: cyrus-sasl-2.1.26-warnings.patch
Patch34: cyrus-sasl-2.1.22-ldap-timeout.patch
# removed due to #759334
#Patch38: cyrus-sasl-2.1.23-pam_rhosts.patch
Patch42: cyrus-sasl-2.1.26-relro.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=816250
Patch43: cyrus-sasl-2.1.26-null-crypt.patch
Patch44: cyrus-sasl-2.1.26-release-server_creds.patch
# AM_CONFIG_HEADER is obsolete, use AC_CONFIG_HEADERS instead
Patch45: cyrus-sasl-2.1.26-obsolete-macro.patch
# missing size_t declaration in sasl.h
Patch46: cyrus-sasl-2.1.26-size_t.patch
# disable incorrect check for MkLinux
Patch47: cyrus-sasl-2.1.26-ppc.patch
# detect gsskrb5_register_acceptor_identity macro (#976538)
Patch48: cyrus-sasl-2.1.26-keytab.patch
Patch49: cyrus-sasl-2.1.26-md5global.patch
# improve sql libraries detection (#1029918)
Patch50: cyrus-sasl-2.1.26-sql.patch
# Treat SCRAM-SHA-1/DIGEST-MD5 as more secure than PLAIN (#970718)
Patch51: cyrus-sasl-2.1.26-prefer-SCRAM-SHA-1-over-PLAIN.patch
# Revert updated GSSAPI flags as in RFC 4752 to restore backward compatibility (#1154566)
Patch52: cyrus-sasl-2.1.26-revert-gssapi-flags.patch
# Document ability to run saslauthd unprivileged (#1188065)
Patch53: cyrus-sasl-2.1.26-saslauthd-user.patch
# Support non-confidentiality/non-integrity requests from AIX SASL GSSAPI implementation (#1174322)
Patch54: cyrus-sasl-2.1.26-gssapi-non-encrypt.patch
# Update client library to be thread safe (#1147659)
Patch55: cyrus-sasl-2.1.26-make-client-thread-sage.patch
# Parsing short prefix matches the whole mechanism name (#1089267)
Patch56: cyrus-sasl-2.1.26-handle-single-character-mechanisms.patch
# Fix confusing message when config file has typo (#1022479)
Patch57: cyrus-sasl-2.1.26-error-message-when-config-has-typo.patch
# GSSAPI: Use per-connection mutex where possible (#1263017)
Patch58: cyrus-sasl-2.1.26-gssapi-use-per-connection-mutex.patch
# GSS-SPNEGO compatible with Windows clients (#1421663)
Patch59: cyrus-sasl-2.1.26-gss-spnego.patch
# Allow cyrus sasl to get the ssf from gssapi (#1431586)
Patch60: cyrus-sasl-2.1.26-gss-ssf.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, libtool, gdbm-devel, groff
BuildRequires: krb5-devel >= 1.2.2, openssl-devel, pam-devel, pkgconfig
BuildRequires: mysql-devel, postgresql-devel, zlib-devel
BuildRequires: libdb-devel
%if ! %{bootstrap_cyrus_sasl}
BuildRequires: openldap-devel
%endif
Requires(post): chkconfig, /sbin/service systemd-units
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd systemd-units
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel systemd-units
Requires: /sbin/nologin
Requires: systemd >= 219
Provides: user(%username)
Provides: group(%username)


%description
The %{name} package contains the Cyrus implementation of SASL.
SASL is the Simple Authentication and Security Layer, a method for
adding authentication support to connection-based protocols.

%package lib
Group: System Environment/Libraries
Summary: Shared libraries needed by applications which use Cyrus SASL

%description lib
The %{name}-lib package contains shared libraries which are needed by
applications which use the Cyrus SASL library.

%package devel
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Group: Development/Libraries
Summary: Files needed for developing applications with Cyrus SASL

%description devel
The %{name}-devel package contains files needed for developing and
compiling applications which use the Cyrus SASL library.

%package gssapi
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: GSSAPI authentication support for Cyrus SASL

%description gssapi
The %{name}-gssapi package contains the Cyrus SASL plugins which
support GSSAPI authentication. GSSAPI is commonly used for Kerberos
authentication.

%package plain
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: PLAIN and LOGIN authentication support for Cyrus SASL

%description plain
The %{name}-plain package contains the Cyrus SASL plugins which support
PLAIN and LOGIN authentication schemes.

%package md5
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: CRAM-MD5 and DIGEST-MD5 authentication support for Cyrus SASL

%description md5
The %{name}-md5 package contains the Cyrus SASL plugins which support
CRAM-MD5 and DIGEST-MD5 authentication schemes.

%package ntlm
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: NTLM authentication support for Cyrus SASL

%description ntlm
The %{name}-ntlm package contains the Cyrus SASL plugin which supports
the NTLM authentication scheme.

# This would more appropriately be named cyrus-sasl-auxprop-sql.
%package sql
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: SQL auxprop support for Cyrus SASL

%description sql
The %{name}-sql package contains the Cyrus SASL plugin which supports
using a RDBMS for storing shared secrets.

%if ! %{bootstrap_cyrus_sasl}
# This was *almost* named cyrus-sasl-auxprop-ldapdb, but that's a lot of typing.
%package ldap
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: LDAP auxprop support for Cyrus SASL

%description ldap
The %{name}-ldap package contains the Cyrus SASL plugin which supports using
a directory server, accessed using LDAP, for storing shared secrets.
%endif

%package scram
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: SCRAM auxprop support for Cyrus SASL

%description scram
The %{name}-scram package contains the Cyrus SASL plugin which supports
the SCRAM authentication scheme.

%package gs2
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries
Summary: GS2 support for Cyrus SASL

%description gs2
The %{name}-gs2 package contains the Cyrus SASL plugin which supports
the GS2 authentication scheme.

###


%prep
%setup -q
chmod -x doc/*.html
chmod -x include/*.h
%patch11 -p1 -b .no_rpath
%patch15 -p1 -b .path
%patch23 -p1 -b .man
%patch24 -p1 -b .sizes
%patch31 -p1 -b .krb4
%patch32 -p1 -b .warnings
%patch34 -p1 -b .ldap-timeout
%patch42 -p1 -b .relro
%patch43 -p1 -b .null-crypt
%patch44 -p1 -b .release-server_creds
%patch45 -p1 -b .obsolete-macro
%patch46 -p1 -b .size_t
%patch47 -p1 -b .ppc
%patch48 -p1 -b .keytab
%patch49 -p1 -b .md5global.h
%patch50 -p1 -b .sql
%patch51 -p1 -b .sha1vsplain
%patch52 -p1 -b .revert
%patch53 -p1 -b .man-unprivileged
%patch54 -p1 -b .gssapi_non_encrypt
%patch55 -p1 -b .threads
%patch56 -p1 -b .prefix
%patch57 -p1 -b .typo
%patch58 -p1 -b .mutex
%patch59 -p1 -b .spnego
%patch60 -p1 -b .ssf


%build
# Find Kerberos.
krb5_prefix=`krb5-config --prefix`
if test x$krb5_prefix = x%{_prefix} ; then
        krb5_prefix=
else
        CPPFLAGS="-I${krb5_prefix}/include $CPPFLAGS"; export CPPFLAGS
        LDFLAGS="-L${krb5_prefix}/%{_lib} $LDFLAGS"; export LDFLAGS
fi

# Find OpenSSL.
LIBS="-lcrypt"; export LIBS
if pkg-config openssl ; then
        CPPFLAGS="`pkg-config --cflags-only-I openssl` $CPPFLAGS"; export CPPFLAGS
        LDFLAGS="`pkg-config --libs-only-L openssl` $LDFLAGS"; export LDFLAGS
fi

# Find the MySQL libraries used needed by the SQL auxprop plugin.
INC_DIR="`mysql_config --include`"
if test x"$INC_DIR" != "x-I%{_includedir}"; then
        CPPFLAGS="$INC_DIR $CPPFLAGS"; export CPPFLAGS
fi
LIB_DIR="`mysql_config --libs | sed -e 's,-[^L][^ ]*,,g' -e 's,^ *,,' -e 's, *$,,' -e 's,  *, ,g'`"
if test x"$LIB_DIR" != "x-L%{_libdir}"; then
        LDFLAGS="$LIB_DIR $LDFLAGS"; export LDFLAGS
fi

# Find the PostgreSQL libraries used needed by the SQL auxprop plugin.
INC_DIR="-I`pg_config --includedir`"
if test x"$INC_DIR" != "x-I%{_includedir}"; then
        CPPFLAGS="$INC_DIR $CPPFLAGS"; export CPPFLAGS
fi
LIB_DIR="-L`pg_config --libdir`"
if test x"$LIB_DIR" != "x-L%{_libdir}"; then
        LDFLAGS="$LIB_DIR $LDFLAGS"; export LDFLAGS
fi

CFLAGS="$RPM_OPT_FLAGS $CFLAGS $CPPFLAGS -fPIE"; export CFLAGS
LDFLAGS="$LDFLAGS -pie -Wl,-z,now"; export LDFLAGS

echo "$CFLAGS"
echo "$CPPFLAGS"
echo "$LDFLAGS"

%configure \
        --enable-shared --disable-static \
        --disable-java \
        --with-plugindir=%{_plugindir2} \
        --with-configdir=%{_plugindir2}:%{_sysconfdir}/sasl2 \
        --disable-krb4 \
        --enable-gssapi${krb5_prefix:+=${krb5_prefix}} \
        --with-gss_impl=mit \
        --with-rc4 \
        --with-dblib=berkeley \
        --with-bdb=db \
        --with-saslauthd=/run/saslauthd --without-pwcheck \
%if ! %{bootstrap_cyrus_sasl}
        --with-ldap \
%endif
        --with-devrandom=/dev/urandom \
        --enable-anon \
        --enable-cram \
        --enable-digest \
        --enable-ntlm \
        --enable-plain \
        --enable-login \
        --enable-alwaystrue \
        --enable-httpform \
        --disable-otp \
%if ! %{bootstrap_cyrus_sasl}
        --enable-ldapdb \
%endif
        --enable-sql --with-mysql=yes --with-pgsql=yes \
        --without-sqlite \
        "$@"
        # --enable-auth-sasldb -- EXPERIMENTAL
make sasldir=%{_plugindir2}
make -C saslauthd testsaslauthd
make -C sample

# Build a small program to list the available mechanisms, because I need it.
pushd lib
../libtool --mode=link %{__cc} -o sasl2-shared-mechlist -I../include $CFLAGS %{SOURCE7} $LDFLAGS ./libsasl2.la


%install
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT sasldir=%{_plugindir2}
make install DESTDIR=$RPM_BUILD_ROOT sasldir=%{_plugindir2} -C plugins

install -m755 -d $RPM_BUILD_ROOT%{_bindir}
./libtool --mode=install \
install -m755 sample/client $RPM_BUILD_ROOT%{_bindir}/sasl2-sample-client
./libtool --mode=install \
install -m755 sample/server $RPM_BUILD_ROOT%{_bindir}/sasl2-sample-server
./libtool --mode=install \
install -m755 saslauthd/testsaslauthd $RPM_BUILD_ROOT%{_sbindir}/testsaslauthd

# Install the saslauthd mdoc page in the expected location.  Sure, it's not
# really a man page, but groff seems to be able to cope with it.
install -m755 -d $RPM_BUILD_ROOT%{_mandir}/man8/
install -m644 -p saslauthd/saslauthd.mdoc $RPM_BUILD_ROOT%{_mandir}/man8/saslauthd.8
install -m644 -p saslauthd/testsaslauthd.8 $RPM_BUILD_ROOT%{_mandir}/man8/testsaslauthd.8

# Install the init script for saslauthd and the init script's config file.
install -m755 -d $RPM_BUILD_ROOT/etc/rc.d/init.d $RPM_BUILD_ROOT/etc/sysconfig
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 -p %{SOURCE5} $RPM_BUILD_ROOT/%{_unitdir}/saslauthd.service
install -m644 -p %{SOURCE9} $RPM_BUILD_ROOT/etc/sysconfig/saslauthd

# Install the config dirs if they're not already there.
install -m755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/sasl2
install -m755 -d $RPM_BUILD_ROOT/%{_plugindir2}

# Provide an easy way to query the list of available mechanisms.
./libtool --mode=install \
install -m755 lib/sasl2-shared-mechlist $RPM_BUILD_ROOT/%{_sbindir}/

# Remove unpackaged files from the buildroot.
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/libotp.*
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_mandir}/cat8/saslauthd.8


%clean
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

%pre
getent group %{username} >/dev/null || groupadd -g 76 -r %{username}
getent passwd %{username} >/dev/null || useradd -r -g %{username} -d %{homedir} -s /sbin/nologin -c "%{hint}" %{username}

%post
%systemd_post saslauthd.service

%preun
%systemd_preun saslauthd.service

%postun
%systemd_postun_with_restart saslauthd.service

%triggerun -n cyrus-sasl -- cyrus-sasl < 2.1.23-32
/usr/bin/systemd-sysv-convert --save saslauthd >/dev/null 2>&1 || :
/sbin/chkconfig --del saslauthd >/dev/null 2>&1 || :
/bin/systemctl try-restart saslauthd.service >/dev/null 2>&1 || :

%post lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc saslauthd/LDAP_SASLAUTHD
%{_mandir}/man8/*
%{_sbindir}/pluginviewer
%{_sbindir}/saslauthd
%{_sbindir}/testsaslauthd
%config(noreplace) /etc/sysconfig/saslauthd
%{_unitdir}/saslauthd.service
%ghost /run/saslauthd

%files lib
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README doc/*.html
%{_libdir}/libsasl*.so.*
%dir %{_sysconfdir}/sasl2
%dir %{_plugindir2}/
%{_plugindir2}/*anonymous*.so*
%{_plugindir2}/*sasldb*.so*
%{_sbindir}/saslpasswd2
%{_sbindir}/sasldblistusers2

%files plain
%defattr(-,root,root)
%{_plugindir2}/*plain*.so*
%{_plugindir2}/*login*.so*

%if ! %{bootstrap_cyrus_sasl}
%files ldap
%defattr(-,root,root)
%{_plugindir2}/*ldapdb*.so*
%endif

%files md5
%defattr(-,root,root)
%{_plugindir2}/*crammd5*.so*
%{_plugindir2}/*digestmd5*.so*

%files ntlm
%defattr(-,root,root)
%{_plugindir2}/*ntlm*.so*

%files sql
%defattr(-,root,root)
%{_plugindir2}/*sql*.so*

%files gssapi
%defattr(-,root,root)
%{_plugindir2}/*gssapi*.so*

%files scram
%defattr(-,root,root)
%{_plugindir2}/libscram.so*

%files gs2
%defattr(-,root,root)
%{_plugindir2}/libgs2.so*

%files devel
%defattr(-,root,root)
%doc doc/*.txt
%{_bindir}/sasl2-sample-client
%{_bindir}/sasl2-sample-server
%{_includedir}/*
%{_libdir}/libsasl*.*so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_sbindir}/sasl2-shared-mechlist

%changelog
* Wed Nov 22 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-23
- Avoid undefined symbols on s390x (#1516193)

* Thu Sep 21 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-22
- Allow cyrus sasl to get the ssf from gssapi (#1431586)

* Mon Mar 06 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-21
- support proper SASL GSS-SPNEGO (#1421663)

* Fri Dec 04 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-20
- GSSAPI: Use per-connection mutex where possible (#1263017)

* Thu Jul 16 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-19.2
- Revert tmpfiles.d and use new systemd feature RuntimeDirectory (#1188065)

* Wed May 20 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-18
- Revert updated GSSAPI flags as in RFC 4752 to restore backward compatibility (#1154566)
- Add and document ability to run saslauth as non-root user (#1188065)
- Support AIX SASL GSSAPI (#1174322)
- Update client library to be thread safe (#1147659)
- Fix problem, that parsing short prefix matches the whole mechanism name (#1089267)
- Don't use unnecessary quotes around user description (#1082564)
- Fix confusing message when config file has typo (#1022479)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.1.26-17
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Honza Horak <hhorak@redhat.com> - 2.1.26-16
- Rebuild for mariadb-libs
  Related: #1045013

* Tue Jan 14 2014 Petr Lautrbach <plautrba@redhat.com> 2.1.26-15
- compile cyrus-sasl with -O3 on ppc64 (#1051063)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.26-14
- Mass rebuild 2013-12-27

* Tue Nov 19 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-13
- Treat SCRAM-SHA-1/DIGEST-MD5 as more secure than PLAIN (#970718)

* Tue Oct 01 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-12.1
- rebuild for https://bugzilla.redhat.com/show_bug.cgi?id=1002625

* Mon Sep 09 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-11
- build with RPM_OPT_FLAGS <ville.skytta@iki.fi> (#1005535)

* Tue Sep 03 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-10
- fix hardening for /usr/sbin/saslauthd
- add testsaslauthd.8 man page to the package
- use static md5global.h file

* Mon Jun 24 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-9
- detect gsskrb5_register_acceptor_identity macro <nalin@redhat.com> (#976538)

* Tue Jun 04 2013 Karsten Hopp <karsten@redhat.com> 2.1.26-8
- disable incorrect check for MkLinux to allow building with shared libraries on PPC

* Tue May 21 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-7
- fix the spec file in order to build the cyrus-sasl-sql plugin
  with support for PostgreSQL and MySQL

* Thu Feb 21 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-6
- don't include system sasl2 library needed for rebuilds after rebase

* Mon Feb 11 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-5
- enable full relro and PIE compiler flags for saslauthd

* Fri Feb 01 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-4
- fix library symlinks

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.26-3
- actually apply size_t patch (#906519)

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.26-2
- sasl.h: +#include<sys/types.h> for missing size_t type (#906519)
- tighten subpkg deps via %%?_isa

* Thu Dec 20 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.26-1
- update to 2.1.26
- fix segfaults in sasl_gss_encode (#886140)

* Mon Dec 10 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.25-2
- always use the current external Berkeley DB when linking

* Fri Dec 07 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.25-1
- update to 2.1.25
- add cyrus-sasl-scram and cyrus-sasl-gs2 packages

* Fri Sep 14 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-36
- replace scriptlets with systemd macros (#856666)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.23-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-34
- move /etc/tmpfiles.d/saslauthd.conf to /usr/lib/tmpfiles.d/saslauthd.conf (#840193)

* Wed Jun 20 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-33
- properly deal with crypt() returning NULL (#816250)
- use fixed gid 76 for saslauth

* Mon Apr 16 2012 Jindrich Novy <jnovy@redhat.com> 2.1.23-32
- re-enable libdb support and utilities

* Wed Apr 04 2012 Jindrich Novy <jnovy@redhat.com> 2.1.23-31
- temporarily disable libdb support to resolve cyrus-sasl
  chicken and egg build problem against libdb

* Tue Apr 03 2012 Jindrich Novy <jnovy@redhat.com> 2.1.23-30
- rebuild against new libdb

* Wed Feb 08 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-29
- Change saslauth user homedir to /run/saslauthd (#752889)
- Change all /var/run/ to /run/
- DAEMONOPTS are not supported any more in systemd units

* Mon Jan 09 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.1.23-28
- Ship with sasl_pwcheck_method: alwaystrue

* Mon Dec 12 2011 Petr Lautrbach <plautrba@redhat.com> 2.1.23-27
- remove support for logging of the remote host via PAM (#759334)
- fix systemd files (#750436)

* Wed Aug 10 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-26
- Add partial relro support for libraries

* Mon Jul 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-25
- Add support for berkeley db 5

* Wed Jun 29 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-23
- Migrate the package to full native systemd unit files, according to the Fedora
  packaging guidelines.

* Wed Jun  1 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-22
- repair rimap support (more packets in response)

* Wed May 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-21
- repair ntlm support

* Mon May 23 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-20
- add logging of the remote host via PAM

* Thu Apr 28 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-19
- temporarilly revert systemd units

* Tue Apr 26 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-18
- update scriptlets

* Fri Apr 22 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-17
- Add systemd units

* Wed Mar 23 2011 Tomas Mraz <tmraz@redhat.com> - 2.1.23-16
- Rebuilt with new mysqlclient

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-15
- set correct license tag
- add ghost to /var/run/saslauthd

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr  9 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-13
- Add /etc/tmpfiles.d element (#662734)

* Fri Apr  9 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-12
- Update init script to impeach pid file

* Thu Mar 11 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-11
- Update pre post preun and postun scripts (#572399)

* Wed Mar 10 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-10
- Rewrite spec file, make corect CFLAGS, CPPFLAGS and LDFLAGS

* Mon Feb 22 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-9
- solve race condition (#566875)

* Wed Feb 17 2010 Stepan Kasal <skasal@redhat.com> - 2.1.23-8
- improve m4 quoting to fix saslauthd/configure (#566088)
- call autotools in build, not in prep

* Fri Feb  5 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-7
- Add man page to testtcpauthd (#526189)

* Fri Oct 16 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-6
- Create the saslauth user according to fedora packaging guide

* Thu Sep 24 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-5
- Repair initscript to make condrestart working properly (#522103)

* Wed Sep 23 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-3
- Add possibility to run the saslauth without root privilegies (#185614)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.23-2
- rebuilt with new openssl

* Fri Aug  7 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-1
- update to 2.1.23

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.22-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.22-24
- repair sasl_encode64 nul termination (#487251)

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> - 2.1.22-23
- Don't build the krb4 plugin as krb5 1.7 will drop it (#225974 #c6)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.22-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.22-21
- fix build with gcc-4.4

* Fri Jan 23 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.22-20
- set LDAP_OPT_TIMEOUT (#326452)
- provide LSB compatible init script (#246900)

* Fri Sep 26 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-19
- always use the current external db4 when linking,
  thanks to Dan Horak for the original patch (#464098)

* Wed Sep 10 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-18
- fix most critical build warnings (#433583)
- use external db4

* Fri Aug 29 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-17
- always link against the internal db4 (#459163)
- rediff patches for no fuzz

* Wed Jul  9 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-16
- update internal db4 (#449737)

* Tue Jul  1 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-15
- drop reload from initscript help (#448154)
- fix hang in rimap auth method (#438533)
- build the krb4 plugin (#154675)

* Fri May 23 2008 Dennis Gilmore <dennis@ausil.us> - 2.1.22-14
- make it so that bootstrap actually works

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.22-13.1
- minor release bump for sparc rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.22-13
- Autorebuild for GCC 4.3

* Thu Feb 14 2008 Steve Conklin <sconklin@redhat.com> - 2.1.22-12
- rebuild for gcc4.3

* Fri Jan 25 2008 Steve Conklin <sconklin@redhat.com> - 2.1.22-11
- Cleanup after merge review bz #225673
- no longer mark /etc/rc.d/init.d/saslauthd as config file
- removed -x permissions on include files
- added devel package dependency on cyrus-sasl
- removed some remaining .la files that were being delivered

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.1.22-10
 - Rebuild for deps

* Wed Nov  7 2007 Steve Conklin <sconklin@redhat.com> - 2.1.22-9
- Fixed a typo in the spec file

* Wed Nov  7 2007 Steve Conklin <sconklin@redhat.com> - 2.1.22-8
- Removed srp plugin source and added dist to NVR

* Tue Sep 18 2007 Steve Conklin <sconklin@redhat.com> 2.1.22-7
- use db4 version 4.6.19 bz#249737

* Mon Feb 26 2007 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-6
- install config files and init scripts using -p
- pull in patch to build with current automake (#229010, Jacek Konieczny
  and Robert Scheck)
- remove prereq on ldconfig, RPM should pick it up based on the -libs
  scriptlets
- pull in patch to correctly detect gsskrb5_register_acceptor_identity
  (#200892, Mirko Streckenbach)
- move sasldb auxprop modules into the -lib subpackage, so that we'll pick
  it up for multilib systems

* Thu Feb 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- pull CVS fix for not tripping over extra commas in digest-md5
  challenges (#229640)

* Fri Feb 16 2007 Nalin Dahyabhai <nalin@redhat.com>
- remove static build, which is no longer a useful option because not all of
  our dependencies are available as static libraries
- drop patches which were needed to keep static builds going
- drop gssapi-generic patch due to lack of interest
- update the bundled copy of db to 4.5.20 (#229012)
- drop dbconverter-2, as we haven't bundled v1 libraries since FC4

* Tue Dec  5 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-5
- rebuild
- add 'authentication' or 'auxprop' to summaries for plugin packages to
  better indicate what the plugin provides
- switch from automake 1.9 to automake 1.7

* Fri Sep 29 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-4
- rebuild without 'dlcompat' bits (#206119)

* Mon Jul 17 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-3
- rebuild

* Tue Jun 20 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-2
- fix a typo in sasl_client_start(3) (#196066)

* Mon May 22 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-1
- update to 2.1.22, adding pluginviewer to %%{_sbindir}

* Tue May 16 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-12
- add conditionalized build dependency on openldap-devel (#191855)
- patch md5global.h to be the same on all architectures

* Thu Apr 27 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-11
- add unapplied patch which makes the DIGEST-MD5 plugin omit the realm
  argument when the environment has $CYRUS_SASL_DIGEST_MD5_OMIT_REALM set to a
  non-zero value, for testing purposes
- add missing buildrequires on zlib-devel (#190113)

* Mon Feb 20 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-10
- add missing buildrequires on gdbm-devel (Karsten Hopp)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.21-9.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.21-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-9
- use --as-needed to avoid linking dbconverter-2 with SQL libraries, which
  it doesn't use because it manipulates files directly (#173321)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-8
- rebuild with new OpenLDAP, overriding the version checks to assume that
  2.3.11 is acceptable
- remove a lingering patch for 1.x which we no longer use

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 2.1.21-7
- Rebuild due to mysql update.

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> 2.1.21-6
- rebuilt with new openssl

* Fri Sep  9 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-5
- add missing buildrequires: on groff (#163032)

* Thu Sep  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-4
- move the ldapdb auxprop support into a subpackage (#167300)
  (note: the ldap password check support in saslauthd doesn't use auxprop)

* Tue Aug 30 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-3
- correct a use of uninitialized memory in the bundled libdb (Arjan van de Ven)

* Mon Aug 29 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-2
- move the ANONYMOUS mech plugin to the -lib subpackage so that multilib
  systems can use it without installing the main package
- build the static libraries without sql auxprop support

* Mon Aug 29 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-1
- update to 2.1.21
- turn off compilation of libsasl v1 (finally)
- explicitly disable sqlite to avoid the build warning
- change the default mechanism which is set for saslauthd from "shadow" to
  "pam" (#159194)
- split the shared library up from saslauthd so that multilib systems don't
  have to pull in every dependency of saslauthd for the compat arch (#166749)

* Wed Apr 13 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-5
- rebuild with new deps

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-4
- rebuild with new deps

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2.1.20-3
- rebuild against db-4.3.21.

* Thu Nov 11 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-2
- build with mysql-devel instead of mysqlclient10

* Mon Nov  1 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-1
- build with mysqlclient10 instead of mysql-devel

* Wed Oct 27 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-0
- update to 2.1.20, including the fix for CAN-2004-0884

* Tue Oct  5 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-3
- use notting's fix for incorrect patch for CAN-2004-0884 for 1.5.28

* Tue Oct  5 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-2
- don't trust the environment in setuid/setgid contexts (CAN-2004-0884, #134660)

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-1
- rebuild (the 2.1.19 changelog for fixing a buffer overflow referred to a CVS
  revision between 2.1.18 and 2.1.19)

* Mon Jul 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-0
- update to 2.1.19, maybe for update

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.18-4
- enable sql auxprop support in a subpackage
- include LDAP_SASLAUTHD documentation file (#124830)

* Fri Jun  4 2004 Nalin Dahyabhai <nalin@redhat.com>
- turn on ntlm in a subpackage

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.1.18-3
- removed rpath

* Tue Mar 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.18-2
- turn on building of libsasl v1 again

* Fri Mar 12 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.18-1
- update to 2.1.18
- saslauthd's ldap code is no longer marked experimental, so we build it

* Mon Mar  8 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-4
- rebuild

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb  3 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-2
- include default /etc/sysconfig/saslauthd configuration file for the init
  script (#114868)

* Thu Jan 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- drop saslauthd_version patch for libsasl2

* Thu Jan 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- add a saslauthd_version option to libsasl's saslauthd client and teach it to
  do the right thing
- enable the saslauthd client code in libsasl version 1 (it's still going away!)
- add saslauthd1-checkpass/saslauthd2-checkpass for testing the above change

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-1
- forcibly disable otp and sql plugins at compile-time

* Fri Dec 19 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.17, forcing the gssapi plugin to be shared now, as before
- use a bundled libdb (#112215)
- build static-with-all-plugins and normal-shared libsasl versions
- add sasl2-{shared,static}-mechlist for very basic sanity checking
- make inclusion of sasl1 stuffs conditional, because it's so going away

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 2.1.15-7
- rebuild against db-4.2.52.

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-6
- use /dev/urandom instead of /dev/random for SASL2 (docs indicate that this is
  safe if you aren't using OTP or SRP, and we build neither); SASL1 appears to
  use it to seed the libc RNG only (#103378)

* Mon Oct 20 2003 Nalin Dahyabhai <nalin@redhat.com>
- obey RPM_OPT_FLAGS again when krb5_prefix != %%{_prefix}

* Fri Oct 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-5
- install saslauthd's mdoc page instead of the pre-formatted man page, which
  would get formatted again

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.1.15-5
- rebuild against db-4.2.42.

* Mon Sep 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- include testsaslauthd
- note in the README that the saslauthd protocol is different for v1 and v2,
  so v1's clients can't talk to the v2 server

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-4
- rebuild

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-3
- add logic to build with gssapi libs in either /usr or /usr/kerberos

* Mon Jul 21 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-2
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-1
- update to 2.1.15

* Mon Jul 14 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.14-1
- update to 2.1.14

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May  9 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.13-3
- change -m argument to saslauthd to be a directory instead of a path

* Thu May  8 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.13-2
- link libsasl2 with -lpthread to ensure that the sasldb plug-in can always
  be loaded

* Tue Apr 29 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.13-1
- update to 2.1.13

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-3
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- consider either des_cbc_encrypt or DES_cbc_encrypt to be sufficient when
  searching for a DES implementation in libcrypto
- pull in CPPFLAGS and LDFLAGS from openssl's pkg-config data, if it exists

* Mon Dec  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-2
- rebuild

* Mon Dec  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-1
- update to 2.1.10, fixing buffer overflows in libsasl2 noted by Timo Sirainen

* Tue Nov 12 2002 Tim Powers <timp@redhat.com> 2.1.7-5
- remove files from $RPM_BUILD_ROOT that we don't intend to include

* Wed Oct  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-4
- update to SASLv1 to final 1.5.28

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-3
- rebuild, overriding sasldir when running make so that on multilib systems
  applications will be able to load modules for the right arch

* Mon Sep  2 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-2
- include dbconverter-2 (#68741)

* Fri Aug  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-1
- update to 2.1.7, fixing a race condition in digest-md5

* Wed Jul 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.6-1
- update to 2.1.6 and 1.5.28

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.5-1
- update to 2.1.5

* Mon Jun 10 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.4-1
- update to 2.1.4

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.2-1
- modify to build with db 4.x

* Thu Apr 18 2002 Nalin Dahyabhai <nalin@redhat.com>
- update cyrus-sasl 2 to 2.1.2
- change buildreq to db3-devel

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.1-3
- suppress output to stdout/stderr in %%postun

* Sun Feb 10 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.1-2
- configure sasldb2 to use berkeley DB instead of gdbm

* Wed Feb  6 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.1-1
- update to 2.1.1

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.0-1
- marge 1.5.24 back in, making a note that it should be removed at some
  point in the future

* Wed Jan 30 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.0, which is designed to be installed in parallel with cyrus sasl
  1.x, so fork the package and rename it to cyrus-sasl2
- add the sasldb auxprop plugin to the main package
- add disabled-by-default saslauthd init script
- move the .la files for plugins into their respective packages -- they're
  needed by the library

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-24
- free ride through the build system

* Fri Nov  2 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-23
- patch to fix possible syslog format-string vulnerability 

* Mon Oct 29 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-22
- add pam-devel as a buildprereq

* Wed Aug 29 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-21
- include sample programs in the -devel subpackage, prefixing their names
  with "sasl-" to reduce future potential naming conflicts

* Tue Aug 14 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-20
- build without -ggdb

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- add gdbm-devel as a build dependency (#44990)
- split off CRAM-MD5 and DIGEST-MD5 into a subpackage of their own (#43079,
  and dialogs with David L. Parsley)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- split out the PLAIN and LOGIN mechanisms into their own package (this allows
  an administrator to disable them by simply removing the package)

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Wed Dec  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix gssapi-over-tls

* Fri Oct 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable static libraries, but always build with -fPIC

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure the version of 1.5.24 in the package matches the masters (#18968)

* Mon Oct  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- re-add the libsasl.so symlink to the -devel package (oops)

* Fri Oct  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- move .so files for modules to their respective packages -- they're not -devel
  links meant for use by ld anyway

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off -devel subpackage
- add a -gssapi subpackage for the gssapi plugins

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the summary text

* Sun Aug 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- re-enable arcfour and CRAM

* Fri Aug  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- force use of gdbm for database files to avoid DB migration weirdness
- enable login mechanism
- disable gssapi until it can coexist peacefully with non-gssapi setups
- actually do a make in the build section (#15410)

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.5.24

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment (release 3)

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- don't muck with syslogd in post
- remove patch for db-3.0 wackiness, no longer needed

* Thu Jun  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS cleanup
- don't strip anything by default

* Fri Feb 11 2000 Tim Powers <timp@redhat.com>
- fixed man pages not being gzipped

* Tue Nov 16 1999 Tim Powers <timp@redhat.com>
- incorporated changes from Mads Kiilerich
- release number is 1, not mk1

* Wed Nov 10 1999 Mads Kiilerich <mads@kiilerich.com>
- updated to sasl 1.5.11
- configure --disable-krb4 --without-rc4 --disable-cram 
  because of missing libraries and pine having cram as default...
- handle changing libsasl.so versions

* Mon Aug 30 1999 Tim Powers <timp@redhat.com>
- changed group

* Fri Aug 13 1999 Tim Powers <timp@redhat.com>
- first build for Powertools
