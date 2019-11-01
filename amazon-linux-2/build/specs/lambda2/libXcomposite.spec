Summary: X Composite Extension library
Name: libXcomposite
Version: 0.4.4
Release: 4.1%{?dist}.0.2
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(compositeproto) >= 0.4
BuildRequires: pkgconfig(xfixes) pkgconfig(xext)

Prefix: %{_prefix}

%description
X Composite Extension library

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libXcomposite.so.1
%{_libdir}/libXcomposite.so.1.0.0

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_mandir}

%changelog
* Thu Oct 31 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 0.4.4-4.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.4.4-4
- Mass rebuild 2013-12-27

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.4-3
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.4.4-1
- libXcomposite 0.4.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 0.4.3-1
- libXcomposite 0.4.3

* Wed Jun 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.4.2-1
- libXcomposite 0.4.2

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 0.4.1-2
- build fix

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 0.4.1-1
- libXcomposite 0.4.1

* Thu Aug 13 2009 Parag <paragn@fedoraproject.org> 0.4.0-10
- Merge-review cleanups #226065

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 0.4.0-8
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 10 2008 Adam Jackson <ajax@redhat.com> 0.4.0-6
- Fix BuildRequires.

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 0.4.0-5
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-4
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 0.4.0-3
- Rebuild for PPC toolchain bug

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 0.4.0-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Adam Jackson <ajax@redhat.com> 0.4.0-1
- libXcomposite 0.4.0

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.3.1-2
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 0.3.1-1
- Update to 0.3.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 0.3-5.1
- rebuild

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 0.3-5
- Replace "makeinstall" with "make install DESTDIR=..."
- Added "Requires: xorg-x11-proto-devel >= 7.0-10, libXfixes-devel to devel
  subpackage needed by xcomposite.pc
- Remove package ownership of mandir/libdir/etc.

* Mon Apr 10 2006 Kristian Høgsberg <krh@redhat.com> 0.3-4
- Bump for build in fc5-bling.

* Fri Apr  7 2006 Adam Jackson <ajackson@redhat.com> 0.3-3
- Note the necessary -proto-devel version in BuildRequires.

* Fri Apr  7 2006 Adam Jackson <ajackson@redhat.com> 0.3-2
- Rebuild to pick up new compositeproto headers.

* Mon Apr  3 2006 Adam Jackson <ajackson@redhat.com> - 0.3-1
- Update to 0.3 from upstream.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.2.2-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.2.2-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 0.2.2.2-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 0.2.2.2-1
- Updated libXcomposite to version 0.2.2.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.2.2.1-1
- Updated libXcomposite to version 0.2.2.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.2.2-1
- Updated libXcomposite to version 0.2.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.2.1-1
- Updated libXcomposite to version 0.2.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.2.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.2.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.2.0-1
- Initial build.
