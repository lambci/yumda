%global tarball libXrender
#global gitdate 20130524
%global gitversion 786f78fd8

Summary: X.Org X11 libXrender runtime library
Name: libXrender
Version: 0.9.10
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
BuildRequires: pkgconfig
BuildRequires: libX11-devel >= 1.5.99.902

%description
X.Org X11 libXrender runtime library

%package devel
Summary: X.Org X11 libXrender development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXrender development package

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
# undo this, we'll add it ourselves in %%doc
rm $RPM_BUILD_ROOT/%{_docdir}/*/libXrender.txt

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/libXrender.so.1
%{_libdir}/libXrender.so.1.3.0

%files devel
%defattr(-,root,root,-)
%doc doc/libXrender.txt
%{_includedir}/X11/extensions/Xrender.h
%{_libdir}/libXrender.so
%{_libdir}/pkgconfig/xrender.pc

%changelog
* Mon Jan 23 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.9.10-1
- libXrender 0.9.10

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 0.9.8-2.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.8-2
- Mass rebuild 2013-12-27

* Mon Jul 08 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.9.8-1
- libXrender 0.9.8

* Mon May 27 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.7-6.20130524git786f78fd8
- Require libX11 1.6RC2 for _XEatDataWords

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.9.7-5.20130524git786f78fd8
- Update to git snapshot to fix CVEs listed below:
- CVE-2013-1987

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.9.7-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 0.9.7-1
- libXrender 0.9.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.9.6-1
- libXrender 0.9.6

* Tue Oct 06 2009 Adam Jackson <ajax@redhat.com> 0.9.5-1
- libXrender 0.9.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 0.9.4-6
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 03 2008 Caolán McNamara <caolanm@redhat.com> - 0.9.4-4
- rebuild to get provides pkgconfig(xrender)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.4-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> 0.9.4-2
- Merge-Review #226084
- Removed BR:pkgconfig 
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed zero-length README file

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 0.9.4-1
- libXrender 0.9.4

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> 0.9.3-1
- libXrender 0.9.3

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 0.9.2-2
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 0.9.2-1
- Update to 0.9.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 0.9.1-3.1
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 0.9.1-3
- Added "Requires: libX11-devel" to devel package for xrender.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 0.9.1-2
- Added "BuildRequires: pkgconfig" for (#193429)
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 0.9.1-1
- Update to 0.9.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.0.2-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.0.2-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 0.9.0.2-3
- Bump and rebuild

* Mon Jan 16 2006 Mike A. Harris <mharris@redhat.com> 0.9.0.2-2
- Added "Requires: xorg-x11-proto-devel" to resolve bug (#176742)

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 0.9.0.2-1
- Updated libXrender to version 0.9.0.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.9.0.1-1
- Updated libXrender to version 0.9.0.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.9.0-5
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.9.0-4
- Updated libXrender to version 0.9.0 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.9.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.9.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.9.0-1
- Initial build.
