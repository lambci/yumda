%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print(get_python_version())")}

Name: libtalloc
Version: 2.1.14
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: The talloc library
License: LGPLv3+
URL: http://talloc.samba.org/
Source: http://samba.org/ftp/talloc/talloc-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel
BuildRequires: doxygen

Provides: bundled(libreplace)

# Patches


%description
A library that implements a hierarchical allocator with destructors.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%package -n pytalloc
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description -n pytalloc
Pytalloc libraries for creating python bindings using talloc

%package -n pytalloc-devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Requires: pytalloc = %{version}-%{release}

%description -n pytalloc-devel
Development libraries for pytalloc


%prep
%setup -q -n talloc-%{version}

%build
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

make %{?_smp_mflags} V=1
doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtalloc.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/talloc.i

# Install API docs
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libtalloc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz
%{_mandir}/man3/libtalloc*.3.gz

%files -n pytalloc
%defattr(-,root,root,-)
%{_libdir}/libpytalloc-util.so.*
%{python_sitearch}/talloc.so

%files -n pytalloc-devel
%defattr(-,root,root,-)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n pytalloc -p /sbin/ldconfig
%postun -n pytalloc -p /sbin/ldconfig

%changelog
* Tue Jan 15 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.1.14-1
- Rebase to libtalloc 2.1.14
- Resolves: rhbz#1658747 - Rebase libtalloc to version 2.1.14 for Samba

* Tue Apr 10 2018 Jakub Hrozek <jhrozek@redhat.com> - 2.1.13-1
- Rebase to libtalloc 2.1.13
- Resolves: rhbz#1558492 - Rebase libtalloc to enable samba rebase

* Sun Oct 15 2017 Jakub Hrozek <jhrozek@redhat.com> - 2.1.10-1
- Rebase to libtalloc 2.1.10
- Resolves: rhbz#1470053 - Rebase libtalloc to enable samba rebase to
                           version 4.7.x

* Wed Mar  1 2017 Jakub Hrozek <jhrozek@redhat.com> - 2.1.9-1
- Rebase to libtalloc 2.1.9
- Resolves: rhbz#1393811 - Rebase libtalloc to enable samba rebase to
                           version 4.6.x

* Tue Feb 14 2017 Jakub Hrozek <jhrozek@redhat.com> - 2.1.8-1
- Rebase to libtalloc 2.1.8
- Resolves: rhbz#1393811 - Rebase libtalloc to enable samba rebase to
                           version 4.6.x

* Thu Jun  9 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.6-1
- Rebase to libtalloc 2.1.5
- Resolves: rhbz#1320230 - Rebase libtalloc to version 2.1.6

* Fri Apr  1 2016 Jakub Hrozek <jhrozek@redhat.com> - 2.1.5-1
- Rebase to libtalloc 2.1.5
- Related: rhbz#1322691

* Wed Jun  3 2015 Jakub Hrozek <jhrozek@redhat.com> - 2.1.2-1
- Resolves: rhbz#1226046 - Rebase libtalloc to at least 2.1.2 in RHEL-7.2

* Thu Sep 04 2014 Jakub Hrozek <jhrozek@redhat.com> - 2.1.1-1
- New upstream release
- Resolves: rhbz#1133932 - Rebase libtalloc to version 2.1.1 or newer

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.0.8-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.8-3
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 2.0.8-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-3
- Add patch to ignore --disable-silent-rules
- Package API docs into libtalloc-devel

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-2
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120

* Fri Nov 04 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.7-1
- New upstream release
- Required for new Samba 4 alpha builds

* Mon Aug 08 2011 Simo Sorce <ssorce@redhat.com> - 2.0.6-1
- New upstream release
- Fixes various bugs with talloc_free_children and freeing complex
  hierarchies with many siblinbgs.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-7
- Let rpmbuild strip binaries, make build more verbose.
- Resolves rhbz#669477 - libtalloc 2.0.5-6 binaries not stripped,
-                        empty -debuginfo
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-6
- Install python bindings in the correct location

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-5
- Run ldconfig on pytalloc

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-4
- Fix build failure on 32-bit platforms

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 2.0.5-3
- New version from upstream
- Add support for pytalloc
- Convert to new WAF build-system

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 2.0.1-1
- New version from upstream
- Also stop building the compat lib, it is not necessary anymore

* Tue Sep  8 2009 Simo Sorce <ssorce@redhat.com> - 2.0.0-0
- New version from upstream.
- Build also sover 1 compat library to ease packages migration

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Simo Sorce <ssorce@redhat.com> - 1.3.1-1
- Original tarballs had a screw-up, rebuild with new fixed tarballs from
  upstream.

* Tue Jun 16 2009 Simo Sorce <ssorce@redhat.com> - 1.3.1-0
- New Upstream release.

* Wed May 6 2009 Simo Sorce <ssorce@redhat.com> - 1.3.0-0
- First public independent release from upstream
