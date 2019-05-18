Name:		libmetalink
Version:	0.1.2
Release: 7%{?dist}.0.2
Summary:	Metalink library written in C
Group:		System Environment/Libraries
License:	MIT
URL:		https://launchpad.net/libmetalink
Source0:	http://launchpad.net/libmetalink/trunk/packagingfix/+download/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	expat-devel
BuildRequires:	CUnit-devel

Prefix: %{_prefix}

%description
libmetalink is a Metalink C library. It adds Metalink functionality such as
parsing Metalink XML files to programs written in C.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%license COPYING
%{_libdir}/libmetalink.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 0.1.2-6
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Alejandro Alvarez <aalvarez@cern.ch> - 0.1.2-3
- Added BuildRequires: CUnit-devel
- Added %%check section
- Removed %%defattr
- Moved man pages to devel package. There is no need for -doc

* Mon Jun 10 2013 Alejandro Alvarez <aalvarez@cern.ch> - 0.1.2-2
- Escaped macros in changelog
- Changed packages summaries
- Renamed -docs to -doc, and changed its group to Documentation
- Fixed -devel dependencies
- Removed -docs dependency on the main package
- All header files specified explicitly

* Mon Apr 22 2013 Alejandro Alvarez <aalvarez@cern.ch> - 0.1.2-1
- Updated for new upstream release
- Man pages moved to libmetalink-docs package

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 07 2009 Ant Bryan <anthonybryan at gmail.com> - 0.0.3-4
- Remove Provides: libmetalink-static = %%{version}-%%{release}

* Tue May 06 2009 Ant Bryan <anthonybryan at gmail.com> - 0.0.3-3
- Use %%{_docdir} instead of /usr/share/doc
- Own /usr/include/metalink

* Wed Apr 29 2009 Ant Bryan <anthonybryan at gmail.com> - 0.0.3-2
- Incorporate suggested changes: remove .la files, --disable static.

* Mon Apr 27 2009 Ant Bryan <anthonybryan at gmail.com> - 0.0.3-1
- Initial package, 0.0.3.

