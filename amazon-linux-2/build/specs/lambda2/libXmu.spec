# TODO: libXmuu split and/or elf filter emulation

Summary: X.Org X11 libXmu/libXmuu runtime libraries
Name: libXmu
Version: 1.1.2
Release: 2%{?dist}.0.2
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-util-macros
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: xmlto

Prefix: %{_prefix}

%description
X.Org X11 libXmu/libXmuu runtime libraries

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --disable-static
make  %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# fixup later
rm -rf $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libXmu.so.6
%{_libdir}/libXmu.so.6.2.0
%{_libdir}/libXmuu.so.1
%{_libdir}/libXmuu.so.1.0.0

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.2-1
- libXmu 1.1.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.1-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libXmu 1.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.1.0-1
- libXmu 1.1.0

* Fri Feb 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.5-2
- Remove BR of libXau-devel, not needed.

* Thu Sep 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.5-1
- libXmu 1.0.5

* Wed Jul 29 2009 Adam Jackson <ajax@redhat.com> 1.0.4-5
- -devel doesn't Require: xorg-x11-util-macros, don't say it does.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.4-3
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 22 2008 Adam Jackson <ajax@redhat.com> 1.0.4-1
- libXmu 1.0.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-5
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 1.0.3-4
- Merge-Review #226080
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed BR:pkgconfig
- Removed zero-length AUTHORS file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.3-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-2
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.3-1.fc7
- Update to 1.0.3

* Fri Oct 13 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-6.fc7
- Also add Requires for libXext-devel for development package (#210123)
- Add pkgconfig dependency for -devel package.

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.2-5
- Add Requires on libXt (bug 202558)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jul  7 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-4
- Rebuild, brew doesn't pick up buildroot changes fast enough.

* Wed Jun 28 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-3
- Rebuild for libXt pkgconfig fixes.

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-2
- Replace "makeinstall" with "make install DESTDIR=..."
- Added "Requires: xorg-x11-proto-devel, libX11-devel, libXt-devel" to devel
  subpackage needed by xmu.pc, xmuu.pc
- Remove package ownership of mandir/libdir/etc.

* Fri May 12 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update to 1.0.2

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Update to 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXmu to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXmu to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.
- Added "BuildRequires: pkgconfig, libXau-devel, xorg-x11-util-macros" to
  fix build dependencies.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXmu to version 0.99.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix BuildRequires to use new style X library package names

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
