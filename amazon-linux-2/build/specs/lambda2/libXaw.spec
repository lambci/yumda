%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary: X Athena Widget Set
Name: libXaw
Version: 1.0.13
Release: 4%{?dist}.0.2
License: MIT
URL: http://www.x.org
Group: System Environment/Libraries

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(xproto) pkgconfig(x11) pkgconfig(xt)
BuildRequires: pkgconfig(xmu) pkgconfig(xpm) pkgconfig(xext)
BuildRequires: xorg-x11-util-macros xmlto lynx

Prefix: %{_prefix}

%description
Xaw is a widget set based on the X Toolkit Intrinsics (Xt) Library.

%prep
%setup -q

%build
autoreconf -v --install --force
export CFLAGS="$RPM_OPT_FLAGS -Os"
%configure \
	    --docdir=%{_pkgdocdir} \
	    --disable-xaw8 --disable-static \
	    --disable-xaw6 \
	    --without-fop --without-xmlto
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libXaw.so.7
%{_libdir}/libXaw7.so.7
%{_libdir}/libXaw7.so.7.0.0

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_mandir}
%exclude %{_pkgdocdir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Mar 25 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.0.13-4
- Force disable documentation generation

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Adam Jackson <ajax@redhat.com> 1.0.13-1
- libXaw 1.0.13

* Fri Apr 10 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.0.12-5
- Re-add missing changelog dropped in 1.0.12-4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Jaromir Capik <jcapik@redhat.com> - 1.0.12-2
- Fixing format-security flaws (#1037174)

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.0.12-1
- libXaw 1.0.12
- Drop pre-F18 changelog

* Sat Nov  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.0.11-7
- Install docs to %%{_pkgdocdir} where available (#993836).
- Fix bogus date in %%changelog.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.0.11-5
- Drop ed from BR, see upstream 0b6058db1ce

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.11-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Adam Jackson <ajax@redhat.com> 1.0.11-1
- libXaw 1.0.11

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Adam Jackson <ajax@redhat.com> 1.0.9-1
- libXaw 1.0.9
- Remove with_compat, always disable xaw6.

* Mon Dec 06 2010 Adam Jackson <ajax@redhat.com> 1.0.8-2
- Add BR: lynx so xmlto can generate text doc, fixes FTBFS.

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com>
- Drop BuildRoot

* Tue Oct 26 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-1
- libXaw 1.0.8

* Mon Oct 19 2009 Adam Jackson <ajax@redhat.com> 1.0.7-1
- libXaw 1.0.7

* Thu Aug 13 2009 Parag <paragn@fedoraproject.org> 1.0.6-4
- Merge-review cleanups #226064
- Updated summary, added Requires: pkgconfig
- removed zero length file AUTHORS 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.6-2
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.0.6-1
- libXaw 1.0.6

* Thu Jun 11 2009 Adam Jackson <ajax@redhat.com> 1.0.4-5
- Hide libXaw6 behind with_compat, disable by default.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.4-3
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-2
- Autorebuild for GCC 4.3

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.0.4-1
- libXaw 1.0.4

* Thu Sep 06 2007 Adam Jackson <ajax@redhat.com> 1.0.2-10
- Move Xaw6 to a compat package, nothing in the distro needs it.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-9
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.2-9
- Don't install INSTALL

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-8.1
- rebuild

* Fri Jul  7 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-8
- Rebuild, brew doesn't pick up buildroot changes fast enough. 

* Wed Jun 28 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-7
- Rebuild for libXt pkgconfig fixes.

* Thu Jun 22 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-6
- Added "Requires: libXpm-devel" to devel subpackage to attempt to fix
  bug (#192040).

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-5
- Remove package ownership of mandir/libdir/etc.

* Tue Jun 06 2006 Bill Nottingham <notting@redhat.com> 1.0.2-4
- Add "BuildRequires: ed" to fix library sonames

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-3
- Added "Requires: xorg-x11-proto-devel" to devel package to try to fix
  indirect bug (#192040)

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-2
- Added "BuildRequires: pkgconfig" for (#193423)
- Replace "makeinstall" with "make install DESTDIR=..."
- Added "BuildRequires: libXt-devel" for (#190169)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update to 1.0.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated libXaw to version 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXaw to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libXaw to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Added libXaw-0.99.2-bug-173027-libtool-sucks.patch to fix bug #173027,
  added 'autoconf' invocation prior to configure, and conditionalized it
  all with with_libtool_sucks_workaround macro.
- Added _smp_mflags to make invocation.
- Use *.h glob in file manifest instead of listing each header individually.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXaw to version 0.99.2 from X11R7 RC2

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXaw to version 0.99.1 from X11R7 RC1
- Update file manifest to find manpages in "man3x"
- Added {_includedir}/X11/Xaw/Template.c to file manifest

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-5
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix all "BuildRequires:" deps with s/xorg-x11-//g

* Thu Aug 25 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Added dependency on xorg-x11-libXmu-devel to devel subpackage, as libXaw
  headers include libXmu headers directly which caused xkbutils to fail to
  build.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Changed all virtual BuildRequires to the "xorg-x11-" prefixed non-virtual
  package names, as we want xorg-x11 libs to explicitly build against
  X.Org supplied libs, rather than "any implementation", which is what the
  virtual provides is intended for.

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
