Summary: X.Org X11 libXfont runtime library
Name: libXfont
Version: 1.5.2
Release: 1%{?dist}.0.2
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://www.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(fontsproto)
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-3
BuildRequires: libfontenc-devel
BuildRequires: freetype-devel

Prefix: %{_prefix}

%description
X.Org X11 libXfont runtime library

%prep
%setup -q

%build
autoreconf -v --install --force
export CFLAGS="$RPM_OPT_FLAGS -Os"
%configure --disable-static
make %{?_smp_mflags}  

%install
%make_install

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%files
%license COPYING
%{_libdir}/libXfont.so.1
%{_libdir}/libXfont.so.1.4.1

%exclude %{_includedir}
%exclude %{_libdir}/libXfont.so
%exclude %{_libdir}/pkgconfig/xfont.pc

%changelog
* Thu Oct 31 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Jan 23 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.5.2-1
- libXfont 1.5.2

* Tue Jul 28 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.5.1-2
- Add bdfReadCharacters patch to fix XTS compilation problems (rhbz#1241939)

* Wed Mar 18 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.5.1-1
- libXfont 1.5.1 (CVE-2015-1802, CVE-2015-1803, CVE-2015-1804)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.5.0-1
- libXfont 1.5.0

* Wed Jul  9 2014 Hans de Goede <hdegoede@redhat.com> - 1.4.99.901-1
- libXfont 1.4.99.901

* Wed Jul  9 2014 Hans de Goede <hdegoede@redhat.com> - 1.4.8-1
- libXfont 1.4.8 (rhbz#1100441)
- Fixes: CVE-2014-0209, CVE-2014-0210, CVE-2014-0211 (rhbz#1097397)

* Mon Jun 09 2014 Adam Jackson <ajax@redhat.com> 1.4.7-2
- Fix FTBFS against new fontproto

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 08 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.4.7-1
- libXfont 1.4.7 (CVE-2013-6462)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.4.6-1
- libXfont 1.4.6

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.5-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 02 2012 Adam Jackson <ajax@redhat.com> 1.4.5-1
- libXfont 1.4.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 1.4.4-1
- libXfont 1.4.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.4.3-1
- libXfont 1.4.3

* Mon Jun 28 2010 Dave Airlie <airlied@redhat.com> 1.4.2-1
- libXfont 1.4.2

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 1.4.1-1
- libXfont 1.4.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.4.0-4
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Adam Jackson <ajax@redhat.com> 1.4.0-2
- libXfont 1.4.0

* Thu Aug 28 2008 Adam Jackson <ajax@redhat.com> 1.3.3-1
- libXfont 1.3.3.
- libXfont-1.3.1-fast-retry.patch: Retry font server connections faster.
  (#443070)

* Tue Feb 12 2008 Adam Jackson <ajax@redhat.com> 1.3.1-4
- libXfont-1.3.1-visibility.patch: Prevent a symbol collision with
  ghostscript.  (#216124)

* Fri Jan 18 2008 Dave Airlie <airlied@redhat.com> 1.3.1-3
- cve-2008-0006.patch: XFS Integer Overflow Vulnerability

* Sun Jan 13 2008 parag <paragn@fedoraproject.org> 1.3.1-2
- Merge-review #226073 Spec cleanups.

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.3.1-1
- libXfont 1.3.1

* Mon Sep 17 2007 Adam Jackson <ajax@redhat.com> 1.2.9-4
- Rebuild for abstract socket support.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.2.9-3
- Rebuild for PPC toolchain bug

* Tue Jun 26 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.9-2
- Put in stop-gap patch to fix comparing links with no attributes.

* Fri Jun 22 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.9-1
- Pull 1.2.9 down to get the catalogue feature.

* Fri Apr 06 2007 Adam Jackson <ajax@redhat.com> 1.2.8-1
- libXfont 1.2.8.

* Wed Jan 17 2007 Kristian Høgsberg <krh@redhat.com> 1.2.6-2
- Add built-in-scalable.patch to prevent crash when trying to scale
  built-in bitmap fonts.

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.2.6-1
- Update to 1.2.6

* Fri Dec 1 2006 Adam Jackson <ajax@redhat.com> 1.2.5-1
- Update to 1.2.5 from upstream.  Drops CID font support.

* Sat Nov 25 2006 Adam Jackson <ajax@redhat.com> 1.2.3-4.fc7
- Revert the namespace whatsit until xfs is sorted out.

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.2.3-3.fc7
- libXdmcp-1.0.2-namespace-pollution.patch: One more collision avoider.

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.2.3-2.fc7
- libXfont-1.2.3-namespace-pollution.patch: Hide some symbols from the dynamic
  linker to avoid colliding with other libs.

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.2.3-1.fc6
- Update to 1.2.3

* Tue Sep 12 2006 Adam Jackson <ajackson@redhat.com> 1.2.2-1.fc6
- Update to 1.2.2, misc security fixes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.2.0-1.1.fc6
- rebuild

* Mon Jul 10 2006 Mike A. Harris <mharris@redhat.com> 1.2.0-1.fc6
- Update to 1.2.0

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-3
- Remove package ownership of mandir/libdir/etc.

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-2
- Added "Requires: libfontenc-devel" for (#185778)

* Sat Apr 01 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 for crash fix and new headers

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXfont to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libXfont to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.
- Removed libXfont-0.99.2-fontdir-attrib-fix-bug-172997.patch, which is now
  integrated upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Added libXfont-0.99.2-fontdir-attrib-fix-bug-172997.patch to remove
  conditionalization of FONTDIRATTRIB from sources instead of tweaking
  CFLAGS for bug (#172997, fdo#5047).

* Mon Nov 14 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Added "-DFONTDIRATTRIB" to CFLAGS, to work around bug (#172997, fdo#5047)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXfont to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXfont to version 0.99.1 from X11R7 RC1
- Remove libfontcache* from file manifests, as it is static linked into Xfont

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-5
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix BuildRequires to use new libX* style package names

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Added xorg-x11-proto-devel dependency to 'devel' subpackage, because the
  libXfont headers use some of the protocol headers, but the autotooling of
  libXfont doesn't autodetect this yet.  Discovered when bdftopcf failed to
  compile while trying to package xorg-x11-font-utils, even though libXfont
  headers were installed.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Changed all virtual BuildRequires to the "xorg-x11-" prefixed non-virtual
  package names, as we want xorg-x11 libs to explicitly build against
  X.Org supplied libs, rather than "any implementation", which is what the
  virtual provides is intended for.
- Added freetype-devel build dependency

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
