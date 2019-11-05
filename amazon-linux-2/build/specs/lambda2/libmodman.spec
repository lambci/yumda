Name:           libmodman
Version:        2.0.1
Release: 8%{?dist}.0.2
Summary:        A simple library for managing C++ modules (plug-ins)

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libmodman/
Source0:        http://libmodman.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake >= 2.8.0
BuildRequires:  zlib-devel

Prefix: %{_prefix}

%description
libmodman is a simple library for managing C++ modules (plug-ins).

%prep
%setup -q
#sed -i 's|-Werror||' libmodman/CMakeLists.txt

%build
%{cmake}
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/*.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.0.1-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.1-7
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Tue Aug 31 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Sat Jul 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.1-5
- Remove conflict with libproxy, its not really necessary since
  we already have the latest libproxy in rawhide.

* Sun Jun 20 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.1-4
- Remove docs from -devel package
- Upgrade cmake requirement to 2.8.0
- Add cmake to -devel requires

* Fri Jun 18 2010 Nathaniel McCallum - 1.0.1-3
- Add docs to -devel package
- Fix include directory ownership

* Fri Jun 18 2010 Nathaniel McCallum - 1.0.1-2
- Added BuildRequires on zlib-devel (used for tests)

* Sun Jun 13 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.1-1
- First release
