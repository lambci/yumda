%define _buildid .8

Summary: X Display Manager Control Protocol library
Name: libXdmcp
Version: 1.1.1
Release: 3%{?_buildid}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Patch0: REVERT-libXdmcp-1.1.1-xalloc.patch

BuildRequires: xorg-x11-proto-devel
BuildRequires: xmlto
BuildRequires: xorg-x11-util-macros autoconf automake libtool

Prefix: %{_prefix}

%description
X Display Manager Control Protocol library.

%prep
%setup -q
%patch0 -R -p1 -b .xalloc

%build
autoreconf -f -i -v || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# manual fixup later
rm -rf $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libXdmcp.so.6
%{_libdir}/libXdmcp.so.6.0.0

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Mon Feb 25 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libXdmcp-1.1.1-3.el6

* Mon Aug 27 2012 Adam Jackson <ajax@redhat.com> 1.1.1-3
- REVERT-libXdmcp-1.1.1-xalloc.patch: Restore definitions (but not
  declarations) of Xalloc and friends for RHEL6 ABI compat.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libXdmcp 1.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.1.0-1
- libXdmcp 1.1.0

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libXdmcp-1.0.3-1.el6

* Fri May 7 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/libXdmcp-1.0.1-2.1
- added submodule prep for package libXdmcp

* Wed Oct 21 2009 Parag <paragn@fedoraproject.org> - 1.0.3-3
- Merge-Review #226068
- make is not verbose

* Thu Oct 08 2009 Parag <paragn@fedoraproject.org> - 1.0.3-2
- Merge-Review #226068
- Removed BR:pkgconfig
- Few spec cleanups.

* Thu Sep 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.3-1
- libXdmcp 1.0.3
- libXdmcp-1.0.2-namespace-pollution.patch: drop

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.2-10
- Un-require xorg-x11-filesystem

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.2-9
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 1.0.2-7
- Merge review cleanups. (#226068)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.2-6
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-5
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-4
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.2-3
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.2-2.fc7
- libXdmcp-1.0.2-namespace-pollution.patch: Hide Xalloc and friends from the
  dynamic linker.

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.2-1
- Update to 1.0.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-2.1
- rebuild

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "BuildRequires: xorg-x11-proto-devel"
- Added "Requires: xorg-x11-proto-devel" to devel package, needed by xdmcp.pc
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Update to 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXdmcp to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXdmcp to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Fri Oct 21 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Update to libXdmcp-0.99.1 from X11R7 RC1 release.

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
