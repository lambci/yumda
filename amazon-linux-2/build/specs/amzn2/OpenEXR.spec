%define _trivial .0
%define _buildid .1

Name:	 OpenEXR
Version: 1.7.1
Release: 8%{?dist}%{?_trivial}%{?_buildid}
Summary: A high dynamic-range (HDR) image file format

Group:	 System Environment/Libraries
License: BSD
URL:	 http://www.openexr.com/
Source0: https://github.com/downloads/openexr/openexr/openexr-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global soname 7

## fedora patches
%if 0%{?fedora} < 19 && 0%{?rhel} < 7 && ! 0%{?amzn} >= 2
# revert soname bump
# upstream missed bumping to so7 for OpenEXR-1.7.0, decided to do so now for
# OpenEXR-1.7.1.  given fedora has shipped OpenEXR-1.7.0 since f15, bumping
# ABI now makes little sense.
%global soname 6
Patch0: openexr-1.7.1-so6.patch
BuildRequires: automake libtool
%endif

Patch1: CVE-2020-11764.patch
Patch2: CVE-2020-11763.patch
Patch3: CVE-2020-11761.patch

Obsoletes: openexr < %{version}-%{release}
Provides:  openexr = %{version}-%{release}

BuildRequires:  ilmbase-devel 
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial
Light & Magic for use in computer imaging applications. This package contains
libraries and sample applications for handling the format.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Group:	 Development/Libraries
Obsoletes: openexr-devel < %{version}-%{release}
Provides:  openexr-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ilmbase-devel
Requires: pkgconfig
%description devel
%{summary}.

%package libs
Summary: %{name} runtime libraries
Group:   System Environment/Libraries
%description libs
%{summary}.


%prep
%setup -q -n openexr-%{version}

%if "%{?soname}" == "6"
%patch0 -p1 -b .so6
./bootstrap
%endif

%patch1 -p1 -b .CVE-2020-11764
%patch2 -p1 -b .CVE-2020-11763
%patch3 -p1 -b .CVE-2020-11761

%build
%configure --disable-static

# hack to omit unused-direct-shlib-dependencies
#sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#unpackaged files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion OpenEXR)" = "%{version}"
make check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*

%post libs -p /sbin/ldconfig
%postun libs  -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE NEWS README
%{_libdir}/libIlmImf.so.%{soname}*

%files devel
%defattr(-,root,root,-)
#omit for now, they're mostly useless, and include multilib conflicts (#342781)
#doc rpmdocs/examples 
%{_datadir}/aclocal/openexr.m4
%{_includedir}/OpenEXR/*
%{_libdir}/libIlmImf.so
%{_libdir}/pkgconfig/OpenEXR.pc


%changelog
* Wed Oct 07 2020 Nikhil Dikshit <nikhildi@amazon.com> - 1.7.1-8
- Adding one more condition for Amazon Linux 2 to avoid using
openexr-1.7.1-so6.patch.

* Tue Jun 02 2020 Josef Ridky <jridky@redhat.com> - 1.7.1-8
- fix CVE-2020-11764 (#1833552)
- fix CVE-2020-11763 (#1833566)
- fix CVE-2020-11761 (#1834461)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.7.1-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.7.1-6
- Mass rebuild 2013-12-27

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-5
- Back to upstream ABI (f19+, el7+)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-3
- Bump to hide revertion

* Fri Aug 31 2012 Rex Dieter <rdieter@fedoraproject.org> 1.7.1-2
- rebuild

* Thu Aug 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-1
- Update to 1.7.1

-* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-5
-- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 Rex Dieter <rdieter@fedoraproject.org> 1.7.0-1
- openexr-1.7.0

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-8
- CVE-2009-1720 OpenEXR: Multiple integer overflows (#513995)
- CVE-2009-1721 OpenEXR: Invalid pointer free by image decompression (#514003)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Caolán McNamara <caolanm@redhat.com> 1.6.1-5
- rebuild to get provides pkgconfig(OpenEXR)

* Fri May 09 2008 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-4
- drop: Obsoletes: OpenEXR-utils (see OpenEXR_Viewers review, bug #428228c3)

* Fri Feb 01 2008 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- gcc43 patch
- purge rpaths

* Wed Jan 09 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.1-2
- hack to omit unused-direct-shlib-dependencies
- conditionalize -libs (f8+)

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.1-1
- openexr-1.6.1

* Mon Oct 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-5
- multiarch conflicts in OpenEXR (#342781)
- don't own %%_includedir/OpenEXR (leave that to ilmbase)

* Mon Oct 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-4
- -libs: %%post/%%postun -p /sbin/ldconfig

* Fri Oct 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.6.0-2
- openexr-1.6.0

* Mon Sep 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.0a-6
- libs: -Requires: %%name

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.4.0a-5
- -libs: new subpkg to be multilib friendly
- -utils: package exrdisplay separately (separate fltk dep)

* Sat Oct 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-4
- Obsoletes/Provides: openexr(-devel) (rpmforge compatibility)

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-3
- pkgconfig patch to use Libs.private

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-2
- -devel: +Requires: pkgconfig

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-1
- openexr-1.4.0a

* Sat Feb 18 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-7
- Further zlib fixes (#165729)

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-6
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-5
- Remove *.a from %%files devel

* Tue Aug 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-4
- Removed -devel dep on zlib-devel (#165729)
- Added --disable-static to %%configure
- Fixed build with GCC 4.0.1
- Added .so links to -devel

* Wed May 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-3
- Add zlib-devel to BR
- Delete all .la files (#157652)

* Mon May  9 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Add disttag

* Sun May  8 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Fix BuildRequires
- Fix Requires on -devel
- Add %%post[un] scriptlets
- Fix ownership in -devel
- Don't have .deps files in %%doc

* Wed Mar 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-1
- Initial RPM release
