%define _buildid .10

Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.0.35
Release: 11%{?_buildid}%{?dist}
Group:         System Environment/Libraries
License:       MIT
URL:           http://www.libgd.org/Main_Page
Source0:       http://www.libgd.org/releases/%{name}-%{version}.tar.bz2
Patch0:        gd-2.0.33-freetype.patch
Patch3:        gd-2.0.34-multilib.patch
Patch4:        gd-loop.patch
Patch5:        gd-2.0.34-sparc64.patch
Patch6:        gd-2.0.35-overflow.patch
Patch7:        gd-2.0.35-AALineThick.patch
Patch8:        gd-2.0.33-BoxBound.patch
Patch9:        gd-2.0.34-fonts.patch
Patch10:       gd-2.0.35-time.patch
Patch11:       gd-2.0.35-security3.patch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: freetype-devel, fontconfig-devel, libX11-devel, libXpm-devel
BuildRequires: libjpeg-devel, libpng-devel, zlib-devel, pkgconfig
BuildRequires: libtool, automake, automake19, autoconf, gettext-devel

%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.


%package progs
Requires:       gd = %{version}-%{release}
Summary:        Utility programs that use libgd
Group:          Applications/Multimedia

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images. 


%package devel
Summary:  The development libraries and header files for gd
Group:    Development/Libraries
Requires: gd = %{version}-%{release}
Requires: libX11-devel, libXpm-devel, libjpeg-devel, freetype-devel
Requires: libpng-devel, zlib-devel, fontconfig-devel
Requires: pkgconfig

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.

%prep
%setup -q
%patch0 -p1 -b .freetype
%patch3 -p1 -b .mlib
%patch4 -p1 -b .loop
%patch6 -p1 -b .overflow
%patch5 -p1 -b .sparc64 
%patch7 -p1 -b .AALineThick
%patch8 -p1 -b .bb
%patch9 -p1 -b .fonts
%patch10 -p1 -b .time
%patch11 -p1 -b .sec3

%build
# we can't run autoreconf because some stupid patches we inherited patch
# generated files instead of configure.ac and Makefile.am
libtoolize --copy --install --force
%configure --disable-rpath
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL='install -p' DESTDIR=$RPM_BUILD_ROOT 
rm $RPM_BUILD_ROOT/%{_libdir}/libgd.la
rm $RPM_BUILD_ROOT/%{_libdir}/libgd.a
install -m 755 -d $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
install config/gdlib.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README-JPEG.TXT index.html NEWS
%{_libdir}/*.so.*

%files progs
%defattr(-,root,root,-)
%{_bindir}/*
%exclude %{_bindir}/gdlib-config

%files devel
%defattr(-,root,root,-)
%doc index.html
%{_bindir}/gdlib-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdlib.pc

%changelog
* Fri Sep 21 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/gd-2.0.35-11.el6

* Mon Sep 10 2012 Honza Horak <hhorak@redhat.com> - 2.0.35-11
- fix AALineThick.patch to draw line with inversed coordinates correctly
  Resolves: #790400

* Sat Jul 24 2010 Cristian Gafton <gafton@amazon.com>
- update build deps
- update buildreqs

* Fri Jul 23 2010 Cristian Gafton <gafton@amazon.com>
- install the generated pkgconfig file

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/gd-2.0.35-10.el6
- import source package RHEL6/gd-2.0.35-9.1.el6

* Fri May 7 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/gd-2.0.33-9.4.el5_4.2
- import source package RHEL5/gd-2.0.33-9.4.el5_1.1
- import source package RHEL5/gd-2.0.33-9.3.fc6
- added submodule prep for package gd

* Mon Feb 22 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.35-10
- fixed CVE-2009-3546 gd: insufficient input validation in _gdGetColors()
- Resolves: #548502

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.0.35-9.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan  6 2009 Ivana Varekova <varekova@redhat.com> - 2.0.35-7
- do minor spec file cleanup

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.35-6
- fix license tag (nothing in this is GPL)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.35-5
- Autorebuild for GCC 4.3

* Tue Nov 20 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-4
- remove static library

* Mon Nov 19 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-3
- spec file cleanup

* Mon Nov 19 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-2
- fix gdlib.pc file

* Tue Sep 18 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-1
- update to 2.0.35

* Tue Sep  4 2007 Ivana Varekova <varekova@redhat.com> 2.0.34-3
- fix font paths (#225786#5)
- fix pkgconfig Libs flag (#225786#4)

* Thu Feb 22 2007 Ivana Varekova <varekova@redhat.com> 2.0.34-2
- incorporate package review feedback

* Thu Feb  8 2007 Ivana Varekova <varekova@redhat.com> 2.0.34-1
- update to 2.0.34

* Mon Jan 29 2007 Ivana Varekova <varekova@redhat.com> 2.0.33-12
- Resolves: #224610
  CVE-2007-0455 gd buffer overrun

* Tue Nov 21 2006 Ivana Varekova <varekova@redhat.com> 2.0.33-11
- Fix problem with to large box boundaries
  Resolves: #197747

* Thu Nov 16 2006 Ivana Varekova <varekova@redhat.com> 2.0.33-10
- added 'thick' - variable support for AA line (#198042)

* Tue Oct 31 2006 Adam Tkac <atkac@redhat.com> 2.0.33-9.4
- patched some additionals overflows in gd (#175414)

* Wed Sep 13 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 2.0.33 - 9.3
- gd-devel now requires fontconfig-devel (#205834)

* Wed Jul 19 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 2.0.33 - 9.2
- use CFLAGS on sparc64 (#199363)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.33 - 9.1
- rebuild

* Mon Jul 10 2006 Jitka Kudrnacova <jkudrnac@redhat.com> 2.0.33-9
- prevent from an infinite loop when decoding bad GIF images (#194520)

* Thu May 25 2006 Ivana Varekova <varekova@redhat.com> - 2.0.33-7
- fix multilib problem (add pkgconfig)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.33-6.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.33-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Phil Knirsch <pknirsch@redhat.com> 2.0.33-6
- Included a few more overflow checks (#177907)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 02 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.33-5
- Switched BuildPreReqs and Requires to modular xorg-x11 style

* Mon Oct 10 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.33-4
- Fixed possible gd crash when drawing AA line near image borders (#167843)

* Wed Sep 07 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.33-3
- Fixed broken freetype-config --libs flags in configure (#165875)

* Sun Apr 17 2005 Warren Togami <wtogami@redhat.com> 2.0.33-2
- devel reqs (#155183 thias)

* Tue Mar 22 2005 Than Ngo <than@redhat.com> 2.0.33-1
- 2.0.33 #150717
- apply the patch from Jose Pedro Oliveira
  - Added the release macro to the subpackages requirements versioning
  - Handled the gdlib-config movement to gd-devel in a differment manner
  - Added fontconfig-devel to the build requirements
  - Added xorg-x11-devel to the build requirements (Xpm)
  - Removed explicit /sbin/ldconfig requirement (gd rpm)
  - Removed explicit perl requirement (gd-progs rpm)
  - Added several missing documentation files (including the license file)
  - Replaced %%makeinstall by make install DESTDIR=...

* Thu Mar 10 2005 Than Ngo <than@redhat.com> 2.0.32-3
- move gdlib-config in devel

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.32-2
- bump release and rebuild with gcc 4

* Wed Nov 03 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.32-1
- Update to 2.0.32 which includes all the security fixes

* Wed Oct 27 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.28-2
- Fixed several buffer overflows for gdMalloc() calls

* Tue Jul 27 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.28-1
- Update to 2.0.28

* Fri Jul 02 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.27-1
- Updated to 2.0.27 due to:
  o Potential memory overruns in gdImageFilledPolygon. Thanks to John Ellson.
  o The sign of Y-axis values returned in the bounding box by gdImageStringFT
    was incorrect. Thanks to John Ellson and Riccardo Cohen.

* Wed Jun 30 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.26-1
- Update to 2.0.26

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.21-3
- Disable rpath usage.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 02 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.21-1
- Updated to 2.0.21

* Tue Aug 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.0.15

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 06 2003 Phil Knirsch <pknirsch@redhat.com> 2.0.12-1
- Update to 2.0.12

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.8.4-11
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.8.4-10
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Phil Knirsch <pknirsch@redhat.com>
- Specfile update to add URL for homepage (#54608)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Oct 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.8.4-5
- Rebuild with current libpng

* Mon Aug 13 2001 Philipp Knirsch <pknirsch@redhat.de> 1.8.4-4
- Fixed a wrong double ownership of libgd.so (#51599).

* Fri Jul 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.8.4-3
- There's really no reason to link against both freetype 1.x and 2.x,
  especially when gd is configured to use just freetype 2.x. ;)

* Mon Jun 25 2001 Philipp Knirsch <pknirsch@redhat.de>
- Forgot to include the freetype library in the shared library linking. Fixed.

* Thu Jun 21 2001 Philipp Knirsch <pknirsch@redhat.de>
- Update to 1.8.4

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- Updates the descriptions to get rid of al references to gif

* Tue Dec 12 2000 Philipp Knirsch <Philipp.Knirsch@redhat.de>
- Fixed bug #22001 where during installation the .so.1 and the so.1.8 links
  didn't get installed and therefore updates had problems.

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- define HAVE_LIBTTF to actually enable ttf support (oops, #18299)
- remove explicit dependencies on libpng, libjpeg, et. al.
- add BuildPrereq: freetype-devel

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add %%postun run of ldconfig (#14915)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com> 
- update to 1.8.3

* Sat Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com> 
- rebuild in new environment

* Mon May 22 2000 Nalin Dahyabhai <nalin@redhat.com> 
- break out a -progs subpackage
- disable freetype support

* Fri May 19 2000 Nalin Dahyabhai <nalin@redhat.com> 
- update to latest version (1.8.2)
- disable xpm support

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- buiuld for glibc 2.1

* Fri Sep 11 1998 Cristian Gafton <gafton@redhat.com>
- built for 5.2
