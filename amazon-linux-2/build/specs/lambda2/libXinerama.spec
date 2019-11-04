%global tarball libXinerama
#global gitdate 20130524
%global gitversion 99c644fc8

Summary: X.Org X11 libXinerama runtime library
Name: libXinerama
Version: 1.1.3
Release: 2.1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}.0.2
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
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel >= 1.5.99.902
BuildRequires: libXext-devel

%description
X.Org X11 libXinerama runtime library

%package devel
Summary: X.Org X11 libXinerama development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXinerama development package

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

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libXinerama.so.1
%{_libdir}/libXinerama.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXinerama.so
%{_libdir}/pkgconfig/xinerama.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/Xinerama.h
%{_includedir}/X11/extensions/panoramiXext.h

%changelog
* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.1.3-2.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.3-2
- Mass rebuild 2013-12-27

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.1.3-1
- libXinerama 1.1.3

* Mon May 27 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-6.20130524git99c644fc8
- Require libX11 1.6RC2 for _XEatDataWords

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.1.2-5.20130524git99c644fc8
- Update to git snapshot to fix the CVEs listed below:
- CVE-2013-1985

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.1.2-1
- libXinerama 1.1.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libXinerama 1.1.1

* Thu Feb 04 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.1-2
- Remove unnecessary BR on libXau-devel

* Tue Oct 06 2009 Adam Jackson <ajax@redhat.com> 1.1-1
- libXinerama 1.1

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.1-1
- libXinerama 1.0.99.1

* Mon Aug 03 2009 Adam Jackson <ajax@redhat.com> 1.0.3-6
- Un-require xorg-x11-filesystem

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 1.0.3-3
- Merge review cleanups. (#226075)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.3-2
- Fix license tag.

* Thu Mar 06 2008 Adam Jackson <ajax@redhat.com> 1.0.3-1
- libXinerama 1.0.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.2-2
- Don't install INSTALL

* Mon Mar 26 2007 Adam Jackson <ajax@redhat.com> 1.0.2-1
- libXinerama 1.0.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Replace "makeinstall" with "make install DESTDIR=..."
- Added "Requires: xorg-x11-proto-devel" to devel for xinerama.pc
- Remove package ownership of mandir/libdir/etc.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated libXinerama to version 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXinerama to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXinerama to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Tue Nov 15 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-3
- Added "BuildRequires: libXau-devel", as twm fails without it, but does not
  check for it with ./configure.  Bug (fdo#5065)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXinerama to version 0.99.1 from X11R7 RC1

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
