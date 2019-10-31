Name: libusb
Epoch: 1
Version: 0.1.4
Release: 3%{?dist}.0.2
Summary: A library which allows userspace access to USB devices
Group: System Environment/Libraries
License: LGPLv2+
URL: http://sourceforge.net/projects/libusb/
Source0: http://downloads.sourceforge.net/libusb/libusb-compat-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0: libusb-config-multilib.patch

BuildRequires: libusb1-devel

%description
This package provides a way for applications to access USB devices.
Legacy libusb-0.1 is no longer supported by upstream, therefore content of this
package was replaced by libusb-compat. It provides compatibility layer allowing
applications written for libusb-0.1 to work with libusb-1.0.

%package devel
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb-0.1. However new applications should use
libusb-1.0 library instead of this one.

%package static
Summary: Static development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description static
This package contains static libraries needed to develop applications that use
libusb-0.1. However new applications should use libusb-1.0 library instead of
this one.

%prep
%setup -q -n libusb-compat-%{version}
%patch0 -p1 -b .config-multilib

%build
%configure --libdir=/%{_lib}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_lib}/libusb.la

mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}/%{_lib}/pkgconfig/* %{buildroot}%{_libdir}/pkgconfig/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/%{_lib}/libusb-0.1.so.*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_includedir}/usb.h
/%{_lib}/libusb.so
%{_libdir}/pkgconfig/libusb.pc
%{_bindir}/libusb-config

%files static
%defattr(-,root,root,-)
/%{_lib}/libusb.a

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:0.1.4-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:0.1.4-2
- Mass rebuild 2013-12-27

* Mon Jan 28 2013 Jindrich Novy <jnovy@redhat.com> 0.1.4-1
- update to 0.1.4 (#904748)
- drop upstreamed patches
- fix changelog dates

* Mon Nov 19 2012 Nils Philippsen <nils@redhat.com> - 1:0.1.3-12
- update sourceforge download URL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 22 2011 Jan Vcelak <jvcelak@redhat.com> 0.1.3-9
- resolve multilib conflict in 'libusb-config' script

* Tue Jun 21 2011 Jan Vcelak <jvcelak@redhat.com> 0.1.3-8
- add libusb-config into -devel subpackage (#713483)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Jan Vcelak <jvcelak@redhat.com> 1:0.1.3-6
- pkg-config file has to be in /usr/lib/pkgconfig

* Tue Jan 25 2011 Jan Vcelak <jvcelak@redhat.com> 1:0.1.3-5
- move libraries from /usr/lib to /lib (#519716)

* Wed Sep 29 2010 jkeating - 1:0.1.3-4
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Jan Vcelak <jvcelak@redhat.com> 0.1.3-3
- add USB access error logging (#628356)
- update README

* Sat Aug 28 2010 Rex Dieter <rdieter@fedoraproject.org> 1:0.1.3-2
- fix epoch-related bustage

* Fri Aug 27 2010 Jan Vcelak <jvcelak@redhat.com> 0.1.3-1
- legacy libusb-0.1 replaced with libusb-compat

* Wed Jun 23 2010 Jan Vcelak <jvcelak@redhat.com> 0.1.12-23
- fixes invalid read causing segfault (#565904)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-20
- remove ExcludeArch: s390 s390x, libusb works fine there (#467768)

* Tue Oct 14 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-19
- don't apply the concurrency timeout handling patch, it breaks
  pilot-link (#456811)

* Mon Oct  6 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-18
- fix multiarch conflict in libusb-devel (#465209)

* Sat Aug  2 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-17
- apply patch from Graeme Gill to fix concurrency timeout
  handling (#456811)

* Fri Apr 18 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-16
- rebuild to fix broken ppc build

* Tue Feb 26 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-15
- don't apply wakeups patch until it's fixed, it causes problems
  with Eye-One Pro (#434950)

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-14
- manual rebuild because of gcc-4.3 (#434189)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.12-13
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-12
- remove unnecessary 1ms wakeups while USB transfers are in progress,
  thanks to Scott Lamb (#408131)

* Tue Nov  6 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-11
- fix multilib conflict in manual.ps (#342461)
- drop useless BR: gawk

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-10
- optimize usb_find_devices() and use openat() instead of open()
 (#273901), thanks to Ulrich Drepper
- BR gawk

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-9
- update License
- rebuild for BuildID

* Wed Aug  1 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-8
- don't use uninitialized buffers on stack (#250274)

* Thu Feb 08 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-7
- merge review spec fixes (#226053)
- create -static subpackage to ship static libs separately
- don't use auto* stuff, drop automake, libtool deps
- BuildRequire openjade, fix Requires

* Tue Dec 12 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-6
- fix BuildRoot, add dist tag, rpmlint warnfixes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.1.12-5.1
- rebuild

* Thu Jun 08 2006 Jesse Keating <jkeating@redhat.com> 0.1.12-5
- Add missing BR automake, libtool.
- Add missing Requires in -devel on pkgconfig

* Thu Jun  1 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-4
- remove .la files from libusb-devel (#172643)

* Thu May 30 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-3
- use pkg-config calls in libusb-config instead of hardcoded
  defaults to avoid multiarch conflicts (#192714)

* Fri May  5 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-2
- add docbook-utils-pdf BuildRequires (#191744)

* Mon Mar  6 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-1
- update to 0.1.12
- drop .format, .searchorder patches, applied upstream

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.1.11-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.1.11-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Jindrich Novy <jnovy@redhat.com> 0.1.11-2
- change device search order, /dev/bus/usb is tried first,
  then /proc/bus/usb, and never try /sys/bus/usb (#178994)

* Fri Jan 20 2006 Jindrich Novy <jnovy@redhat.com> 0.1.11-1
- 0.1.11
- require pkgconfig, package libusb.pc
- fix printf format in linux.c so that libusb can be built with -Werror (default)

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 0.1.10a-3
- Rebuild.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Mon Nov 21 2005 Tim Waugh <twaugh@redhat.com> 0.1.10a-2
- Build does not require xorg-x11-devel.  Fixes rebuild problem (no more
  xorg-x11-devel package).

* Wed Mar  9 2005 Tim Waugh <twaugh@redhat.com> 0.1.10a-1
- 0.1.10a.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.1.10-2
- Rebuild for new GCC.

* Fri Feb 11 2005 Tim Waugh <twaugh@redhat.com> 0.1.10-1
- 0.1.10.

* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 0.1.9-1
- Build requires xorg-x11-devel.
- 0.1.9.

* Sat Jan 08 2005 Florian La Roche <laroche@redhat.com>
- rebuilt to get rid of legacy selinux filecontexts

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Tim Waugh <twaugh@redhat.com> 0.1.8-3
- Run aclocal/autoconf to make shared libraries work again.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 11 2004 Tim Waugh <twaugh@redhat.com> 0.1.8-1
- 0.1.8.

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 0.1.7-3
- Fixed spec file.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com>
- Use the CFLAGS from the environment.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 0.1.7-1
- 0.1.7.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe

* Tue Jun 25 2002 Tim Waugh <twaugh@redhat.com> 0.1.6-1
- 0.1.6.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.1.5-6
- automated rebuild

* Fri Jun 21 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-5
- Rebuild to fix broken deps.

* Thu May 23 2002 Tim Powers <timp@redhat.com> 0.1.5-4
- automated rebuild

* Thu Apr 11 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-3
- Rebuild (fixes bug #63196).

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-2
- Rebuild in new environment.

* Thu Feb  7 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-1
- 0.1.5.

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 0.1.4-2
- Rebuild in new environment.
- Work around tarball brokenness (doc directory was not automade).

* Mon Oct 29 2001 Tim Waugh <twaugh@redhat.com> 0.1.4-1
- Adapted for Red Hat Linux.
- 0.1.4.

* Thu Mar  1 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.1.3b-1mdk
- Initial Mandrake release
