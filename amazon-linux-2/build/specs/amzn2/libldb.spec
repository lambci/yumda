%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%define talloc_version 2.1.16
%define tdb_version 1.3.18
%define tevent_version 0.9.39

Name: libldb
Version: 1.5.4
Release: 1%{?dist}
Group: Development/Libraries
Summary: A schema-less, ldap like, API and database
Requires: libtalloc%{?_isa} >= %{talloc_version}
Requires: libtdb%{?_isa} >= %{tdb_version}
Requires: libtevent%{?_isa} >= %{tevent_version}
License: LGPLv3+
URL: http://ldb.samba.org/
Source: http://samba.org/ftp/ldb/ldb-%{version}.tar.gz

BuildRequires: libtalloc-devel >= %{talloc_version}
BuildRequires: libtdb-devel >= %{tdb_version}
BuildRequires: libtevent-devel >= %{tevent_version}
%{?fedora:BuildRequires: popt-devel}
%if 0%{?rhel} <= 5
BuildRequires: popt
%endif
%if 0%{?rhel} >= 6
BuildRequires: popt-devel
%endif
BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel
BuildRequires: python-tdb
BuildRequires: pytalloc-devel
BuildRequires: python-tevent
BuildRequires: doxygen

Provides: bundled(libreplace)
Provides: bundled(libtdb_compat)

# Patches

%description
An extensible library that implements an LDAP like API to access remote LDAP
servers, or use local tdb databases.

%package -n ldb-tools
Group: Development/Libraries
Summary: Tools to manage LDB files
Requires: libldb%{?_isa} = %{version}-%{release}

%description -n ldb-tools
Tools to manage LDB files

%package devel
Group: Development/Libraries
Summary: Developer tools for the LDB library
Requires: libldb%{?_isa} = %{version}-%{release}
Requires: libtdb-devel%{?_isa} >= %{tdb_version}
Requires: libtalloc-devel%{?_isa} >= %{talloc_version}
Requires: libtevent-devel%{?_isa} >= %{tevent_version}
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the LDB library.

%package -n pyldb
Group: Development/Libraries
Summary: Python bindings for the LDB library
Requires: libldb%{?_isa} = %{version}-%{release}
Requires: python-tdb%{?_isa} >= %{tdb_version}

%description -n pyldb
Python bindings for the LDB library

%package -n pyldb-devel
Group: Development/Libraries
Summary: Development files for the Python bindings for the LDB library
Requires: pyldb%{?_isa} = %{version}-%{release}

%description -n pyldb-devel
Development files for the Python bindings for the LDB library

%prep
%setup -q -n ldb-%{version}

%build

export PYTHON=/usr/bin/python2
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=cmocka \
           --builtin-libraries=replace \
           --with-modulesdir=%{_libdir}/ldb/modules \
           --without-ldb-lmdb \
           --with-privatelibdir=%{_libdir}/ldb

# Don't build with multiple processors
# It breaks due to a threading issue in WAF
make V=1
doxygen Doxyfile

%install
export PYTHON=/usr/bin/python2
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/libldb.a
rm -f %{buildroot}%{_libdir}/ldb/libcmocka-ldb.so

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

# Install API docs
cp -a apidocs/man/* $RPM_BUILD_ROOT/%{_mandir}

# LDB 1.1.8+ bug: remove manpage named after full
# file path
rm -f $RPM_BUILD_ROOT/%{_mandir}/man3/_*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_libdir}/ldb
%{_libdir}/libldb.so.*
%{_libdir}/ldb/libldb-key-value.so
%{_libdir}/ldb/libldb-tdb-err-map.so
%{_libdir}/ldb/libldb-tdb-int.so
%dir %{_libdir}/ldb/modules
%dir %{_libdir}/ldb/modules/ldb
%{_libdir}/ldb/modules/ldb/*.so

%files -n ldb-tools
%defattr(-,root,root,-)
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_libdir}/ldb/libldb-cmdline.so
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_version.h
%{_includedir}/ldb.h
%{_libdir}/libldb.so

%{_libdir}/pkgconfig/ldb.pc
%{_mandir}/man3/ldb*.gz
%{_mandir}/man3/ldif*.gz

%files -n pyldb
%defattr(-,root,root,-)
%{python_sitearch}/ldb.so
%{_libdir}/libpyldb-util.so.1*
%{python_sitearch}/_ldb_text.py*

%files -n pyldb-devel
%defattr(-,root,root,-)
%{_includedir}/pyldb.h
%{_libdir}/libpyldb-util.so
%{_libdir}/pkgconfig/pyldb-util.pc
%{_mandir}/man*/Py*.gz

%post -n pyldb -p /sbin/ldconfig
%postun -n pyldb -p /sbin/ldconfig

%changelog
* Thu Aug  1 2019 Jakub Hrozek <jhrozek@redhat.com> - 1.5.4-1
- Resolves: rhbz#1736013 - Rebase libldb to version 1.5.4 for Samba

* Wed Jan 16 2019 Jakub Hrozek <jhrozek@redhat.com> - 1.4.2-1
- Resolves: rhbz#1658758 - Rebase libldb to version 1.4.2 for Samba

* Wed Jun 27 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.3.4-1
- Resolves: rhbz#1558497 - Rebase libldb to enable samba rebase

* Thu May  3 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.3.3-1
- Resolves: rhbz#1558497 - Rebase libldb to enable samba rebase

* Tue Apr 10 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.3.2-1
- Resolves: rhbz#1558497 - Rebase libldb to enable samba rebase

* Sun Oct 15 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.2.2-1
- Resolves: rhbz#1470056 - Rebase libldb to enable samba rebase to
                           version 4.7.x

* Tue Feb 14 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.1.29-1
- Resolves: rhbz#1393810 - Rebase libldb to enable samba rebase to
                           version 4.6.x

* Thu Jun  9 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.1.26-1
- Resolves: rhbz#1320253 - Rebase libldb to version 1.1.26

* Fri Apr  1 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.1.25-1
- Rebase libldb to 1.1.25
- Remove upstreamed patches
- Related: rhbz#1322691

* Mon Dec 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.1.20-3
- Resolves: rhbz#1290715 - CVE-2015-5330 libldb: samba: Remote memory read
                           in Samba LDAP server [rhel-7.3]
- Remove the patch from the previous commit, it doesn't fix a remotely
  eploitable issue. Add patches from upstream #11636 instead.

* Mon Dec 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.1.20-2
- Resolves: rhbz#1290715 - CVE-2015-5330 libldb: samba: Remote memory read
                           in Samba LDAP server [rhel-7.3]

* Wed Jun  3 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.1.20-1
- Related: rhbz#1226047 - Rebase libldb to at least 1.1.20 in RHEL-7.2

* Mon Nov 24 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.1.17-2
- Fix the minimal required tdb version
- Related: rhbz#1133914 - Rebase libldb to version 1.1.17 or newer

* Thu Sep 04 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.1.17-1
- New upstream release 1.1.17
- Resolves: rhbz#1133914 - Rebase libldb to version 1.1.17 or newer

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1.16-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.16-3
- Mass rebuild 2013-12-27

* Mon Jul 08 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.1.16-2
- Make the Requires arch-specific

* Tue Jul 02 2013 - Andreas Schneider <asn@redhat.com> - 1.1.16-1
- New upstream release 1.1.16

* Wed Jun 05 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.1.15-3
- Relax pytdb requirement

* Thu Feb 07 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.1.15-2
- The 1.1.15 rebase obsoletes the patch from 1.1.14-2

* Thu Feb 07 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.1.15-1
- New upstream release 1.1.15

* Wed Jan 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.1.14-2
- Add patch by Stephen Gallagher to include manual pages for
  ldb_connect() and several other functions.

* Sat Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.1.14-1
- New upstream release 1.1.14

* Wed Oct 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.1.13-1
- New upstream release 1.1.13

* Mon Sep 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.1.12-1
- New upstream release 1.1.12

* Tue Aug 28 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.1.11-1
- New upstream release 1.1.11

* Mon Aug 10 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.1.10-1
- New upstream release 1.1.10

* Thu Aug 02 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.1.9-1
- New upstream release 1.1.9
- Required for Samba 4 Beta 5
- Ensure rename target does not exist before deleting old record
- Add parameter to avoid NULL format string flagged by -Werror=format

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.1.8-1
- New upstream release 1.1.8
- Required for latest Samba 4 beta
- Fixes for pyldb
- Revert to using tdb1 by default
- Drop support for tdb_compat
- CCAN is no longer built as a static library

* Tue May 22 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.1.6-1
- New upstream release 1.1.6
- Drop upstream patches
- Required for upcoming Samba 4 beta
- Explicitly build with tdb1 support

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.1.4-1.1
- Do not build with multiple CPUs

* Tue Dec 06 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.1.4-1
- New upstream release
- Add ldb_module_error() routine
- Fedora: work around unreliable configure check for pytevent
- Drop patch to ignore --disable-silent-rules (included in tarball)

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.1.3-4
- Add patch to ignore --disable-silent-rules

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.1.3-3
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120
- Add explicit mention of bundled libtdb_compat and libccan
- https://fedorahosted.org/fpc/ticket/119

* Mon Nov 21 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.1.3-2
- Build and install API documentation
- Build tdb_compat and ccan statically. They have no upstream releases to
  link against yet and their API is in flux. It is unsafe to make them
  public and shared at this time.

* Wed Nov 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.1.3-1
- New upstream release
- Required for building newer samba4 packages

* Tue Aug  2 2011 Simo Sorce <ssorce@redhat.com> - 1.1.0-1
- Update to 1.1.0
  (dependency for samba4 alpha16 snapshot)

* Tue Feb 22 2011 Simo Sorce <ssorce@redhat.com> - 1.0.2-1
- Update to 1.0.2
  (dependency for samba4 alpha15 snapshot)

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-2
- Disable rpath

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-1
- New upstream release 1.0.0
- SOname bump to account for module loading changes
- Rename libldb-tools to ldb-tools to make upgrades easier

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.22-8
- Fixes from package review
- Change Requires: on tools subpackage to be the exact version/release
- Remove unnecessary BuildRoot directive

* Mon Jan 17 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.22-7
- Update to 0.9.22 (first independent release of libldb upstream)

