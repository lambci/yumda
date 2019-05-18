Summary: Sample Authorization Protocol for X
Name: libXau
Version: 1.0.8
Release: 2.1%{?dist}.0.2
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

#Patch0: xau-1.0.4-local.patch

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel

%description
This is a very simple mechanism for providing individual access to an X Window
System display.It uses existing core protocol and library hooks for specifying
authorization data in the connection setup block to restrict use of the display
to only those clients that show that they know a server-specific key 
called a "magic cookie".

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: xorg-x11-proto-devel
Requires: pkgconfig
BuildRequires: xorg-x11-proto-devel

%description devel
X.Org X11 libXau development package

%prep
%setup -q
#patch0 -p1 -b .local

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXau.so.6
%{_libdir}/libXau.so.6.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/Xauth.h
%{_libdir}/libXau.so
%{_libdir}/pkgconfig/xau.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.0.8-2.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.8-2
- Mass rebuild 2013-12-27

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-1
- libXau 1.0.8

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.6-7
- autoreconf needs xorg-x11-util-macros

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.6-6
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.6-1
- libXau 1.0.6

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.5-1
- libXau 1.0.5

* Wed Aug 12 2009 Parag <paragn@fedoraproject.org> 1.0.4-8
- Merge review cleanups. (#226063)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.4-6
- Remove useless %%dir
- Un-require xorg-x11-filesystem

* Wed Mar 18 2009 Adam Jackson <ajax@redhat.com> 1.0.4-5
- Disable local auth patch.  Apparently it _can_ possibly help.

* Wed Mar 11 2009 Adam Jackson <ajax@redhat.com> 1.0.4-4
- xau-1.0.4-local.patch: When looking for an auth cookie on local transport,
  don't bother checking hostname, it can't possibly help.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 1.0.4-2
- Merge review cleanups. (#226063)

* Thu Sep 04 2008 Adam Jackson <ajax@redhat.com> 1.0.4-1
- libXau 1.0.4

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.3-6
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-5
- Autorebuild for GCC 4.3

* Thu Sep 27 2007 Adam Jackson <ajax@redhat.com> 1.0.3-4
- libXau-devel Requires: xorg-x11-proto-devel (#235563)

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.3-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.0.3-1
- Update to 1.0.3

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.2-1
- Update to 1.0.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-3.1
- rebuild

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Remove package ownership of mandir/libdir/etc.
- Added "BuildRequires: xorg-x11-proto-devel" needed by xau.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "BuildRequires: pkgconfig" for (#193422)
- Replace "makeinstall" with "make install DESTDIR=..." to fix (#192718)

* Fri May 12 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Bump to 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXau to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXau to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Fri Oct 21 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Update to libXau-0.99.1 from X11R7 RC1 release.
- Added manpages that were absent in X11R7 RC0, and updated the file lists
  to find them in section "man3x".

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
