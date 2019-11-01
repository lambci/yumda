%global tarball libXtst
#global gitdate 20130524
%global gitversion e7e04b7be

Summary: X.Org X11 libXtst runtime library
Name: libXtst
Version: 1.2.3
Release: 1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}.0.2
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
%endif

Requires: libX11 >= 1.5.99.902

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel >= 1.5.99.902
BuildRequires: libXext-devel
BuildRequires: libXi-devel
BuildRequires: xmlto

%description
X.Org X11 libXtst runtime library

%package devel
Summary: X.Org X11 libXtst development package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libXi-devel%{?_isa}

%description devel
X.Org X11 libXtst development package

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -rf $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libXtst.so.6
%{_libdir}/libXtst.so.6.1.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/XTest.h
%{_includedir}/X11/extensions/record.h
%{_libdir}/libXtst.so
%{_libdir}/pkgconfig/xtst.pc
%{_mandir}/man3/XTest*.3*

%changelog
* Mon Jan 23 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.2.3-1
- libXtst 1.2.3

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.2.2-2.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.2-2
- Mass rebuild 2013-12-27

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-1
- libXtst 1.2.2

* Mon May 27 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.1-7.20130524gite7e04b7be
- Require libX11 1.6RC2 for _XEatDataWords

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-6.20130524gite7e04b7be
- Update to git snapshot to fix CVEs listed below
- CVE-2013-2063

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.1-5
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov  7 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.2.1-3
- Add libXi-devel dep to -devel for XInput.h #inclusion.
- Make main package dep in -devel arch qualified.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.2.1-1
- libXtst 1.2.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.2.0-1
- libXtst 1.2.0

* Mon Aug 31 2009 Caolán McNamara <caolanm@redhat.com> 1.0.99.2-3
- Resolves: rhbz#513753 libXtst-devel requires libXi-devel for 
  included headers

* Tue Aug 25 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.2-2
- libXtst provides record.h now

* Tue Aug 25 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.2-1
- libXtst 1.0.99.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.99.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.99.1-2
- Un-require xorg-x11-filesystem

* Wed Jul 22 2009 Adam Jackson <ajax@redhat.com> 1.0.99.1-1
- libXtst 1.0.99.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.3-4
- Rebuild for pkgconfig provides

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 1.0.3-2
- Merge-Review #226091
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed BR:pkgconfig
- Removed zero-length README AUTHORS file

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.0.3-1
- libXtst 1.0.3

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-2
- Rebuild for PPC toolchain bug

* Sat Jun 23 2007 Adam Jackson <ajax@redhat.com> 1.0.2-1.
- libXtst 1.0.2

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.1-4
- Don't install INSTALL

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-3.1
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added "Requires: xorg-x11-proto-devel" to devel package for xtst.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "BuildRequires: pkgconfig" for (#193504)
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated libXtst to version 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXtst to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libXtst to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXtst to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXtst to version 0.99.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
