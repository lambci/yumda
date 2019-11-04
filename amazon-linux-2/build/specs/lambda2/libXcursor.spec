%global tarball libXcursor
#global gitdate 20130524
%global gitversion 8f677eaea

Summary: Cursor management library
Name: libXcursor
Version: 1.1.15
Release: 1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: https://www.x.org

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source2:    make-git-snapshot.sh
Source3:    commitid
%else
Source0: https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
%endif
Source1: index.theme

Requires: libX11 >= 1.5.99.902

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel >= 1.5.99.902
BuildRequires: libXfixes-devel
BuildRequires: libXrender-devel >= 0.8.2
BuildRequires: autoconf automake libtool pkgconfig

Prefix: %{_prefix}

%description
This is  a simple library designed to help locate and load cursors.
Cursors can be loaded from files or memory. A library of common cursors
exists which map to the standard X cursor names.Cursors can exist in
several sizes and the library automatically picks the best size.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
iconv --from=ISO-8859-2 --to=UTF-8 COPYING > COPYING.new && \
touch -r COPYING COPYING.new && \
mv COPYING.new COPYING

%build
autoreconf -v --install --force
#export CFLAGS="$RPM_OPT_FLAGS -DICONDIR=\"%{_datadir}/icons\""
%configure \
 --disable-static
make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/default
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/default/index.theme

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libXcursor.so.1
%{_libdir}/libXcursor.so.1.0.2
%dir %{_datadir}/icons/default
%{_datadir}/icons/default/index.theme

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_mandir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Apr 24 2018 Adam Jackson <ajax@redhat.com> - 1.1.15-1
- libXcursor 1.1.15

* Fri Feb 17 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.14-8
- Remove RHEL default cursor theme variant (rhbz#1388458)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.1.14-2.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.14-2
- Mass rebuild 2013-12-27

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.1.14-1
- libXCursor 1.1.14

* Mon May 27 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.13-7.20130524git8f677eaea
- Require libX11 1.6RC2 for _XEatDataWords

* Fri May 24 2013 Adam Jackson <ajax@redhat.com> 1.1.13-6
- Fix cursor theme in RHEL

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.1.13-3.20130524git8f677eaea
- Update to fix following CVEs:
- CVE-2013-2003

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.13-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.1.13-1
- libXcursor 1.1.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 1.1.12-1
- libXcursor 1.1.12

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> 1.1.11-2
- Change the default cursor theme
  (also make the dependency a soft one)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 1.1.11-1
- libXcursor 1.1.11

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 1.1.10-5
- The theme file should _not_ be a config file

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 1.1.10-4
- Make default cursor theme inherit dmz-aa instead of Bluecurve
- Also require the cursor theme package

* Wed Oct 21 2009 Parag <paragn@fedoraproject.org> - 1.1.10-3
- Merge-Review #226066
- make is not verbose
- preserve timestamp of index.theme

* Thu Oct 08 2009 Parag <paragn@fedoraproject.org> - 1.1.10-2
- Merge-Review #226066
- Removed XFree86-libs, xorg-x11-libs as Obsoletes
- Removed BR:pkgconfig
- Few spec cleanups

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.10-1
- libXcursor 1.1.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.1.9-5
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.1.9-3
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.9-2
- Autorebuild for GCC 4.3

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.1.9-1
- libXcursor 1.1.9

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.8-3
- Rebuild for PPC toolchain bug

* Sat Jul  7 2007 Matthias Clasen <mclasen@redhat.com> 1.1.8-3
- Don't own /usr/share/icons
- Require pkgconfig in -devel

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.1.8-2
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.1.8-1
- Update to 1.1.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.1.7-1.1
- rebuild

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.1.7-1
- Update to 1.1.7 from X11R7.1

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.1.6-2
- Added "BuildRequires: xorg-x11-proto-devel"
- Added "Requires: xorg-x11-proto-devel" to devel package, needed by xcursor.pc
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.1.6-1
- Update to 1.1.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.1.5.2-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.1.5.2-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.1.5.2-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.1.5.2-1
- Updated libXcursor to version 1.1.5.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 1.1.5.1-1
- Updated libXcursor to version 1.1.5.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.
- Added default index.theme file to set BlueCurve as the default cursor theme
  to fix bug (#175532).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 1.1.5-1
- Updated libXcursor to version 1.1.5 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 1.1.4-1
- Updated libXcursor to version 1.1.4 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 1.1.3-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 1.1.3-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 1.1.3-1
- Initial build.
