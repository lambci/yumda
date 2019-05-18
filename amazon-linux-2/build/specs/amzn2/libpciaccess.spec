#define gitdate 20111109
#define gitrev  a0a53a67c91c698007dcac3e7aba27c999c4f6ed

Name:           libpciaccess
Version:        0.14
Release:        1%{?dist}
Summary:        PCI access library

Group:          System Environment/Libraries
License:        MIT
URL:            http://gitweb.freedesktop.org/?p=xorg/lib/libpciaccess.git

# git snapshot.  To recreate, run
# % ./make-libpciaccess-snapshot.sh %{gitrev}
#Source0:        libpciaccess-%{gitdate}.tar.bz2
Source0:	https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
Source1:        make-libpciaccess-snapshot.sh

Patch2:		libpciaccess-rom-size.patch

BuildRequires:  autoconf automake libtool pkgconfig xorg-x11-util-macros
Requires:       hwdata

%description
libpciaccess is a library for portable PCI access routines across multiple
operating systems.

%package devel
Summary:        PCI access library development package
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development package for libpciaccess.

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
%patch2 -p1 -b .rom-size

%build
# autoreconf -v --install
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_libdir}/libpciaccess.so.0
%{_libdir}/libpciaccess.so.0.11.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/pciaccess.h
%{_libdir}/libpciaccess.so
%{_libdir}/pkgconfig/pciaccess.pc

%changelog
* Mon Oct 23 2017 Adam Jackson <ajax@redhat.com> - 0.14-1
- libpciaccess 0.14

* Mon Nov 14 2016 Dave Airlie <airlied@redhat.com> - 0.13.4-3
- add support to ignore 32-bit domains (#1380184)

* Fri May 22 2015 Dave Airlie <airlied@redhat.com> 0.13.4-2
- rebuild due to ppc64le relro issue

* Thu May 21 2015 Dave Airlie <airlied@redhat.com> 0.13.4-1
- rebase libpciaccess 0.13.4

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 0.13.1-4.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.13.1-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Adam Jackson <ajax@redhat.com> 0.13.1-1
- libpciaccess 0.13.1

* Wed Mar 28 2012 Adam Jackson <ajax@redhat.com> 0.13-2
- libpciaccess-macros.patch: Fix out* macros again

* Wed Mar 28 2012 Adam Jackson <ajax@redhat.com> 0.13-1
- libpciaccess 0.13

* Wed Feb 29 2012 Dan Horák <dan[at]danny.cz> - 0.12.902-6
- fix the out[bwl] compatibility macros

* Thu Feb 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.902-5
- Add ARM arch to libpciaccess-lol-dev-port patch

* Wed Feb 08 2012 Adam Jackson <ajax@redhat.com> 0.12.902-4
- libpciaccess-lol-dev-port.patch: Don't use /dev/port since the kernel insists
  that it remain unusably broken.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.902-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Daniel Drake <dsd@laptop.org> 0.12.902-2
- Add upstream patch to fix ios deletion; fixes X crash on OLPC XO-1.5

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 0.12.902-1
- libpciaccess 0.12.902

* Wed Nov 09 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.12.901-1
- Today's git snapshot

* Wed Feb 09 2011 Adam Jackson <ajax@redhat.com> 0.12.1-1
- libpciaccess 0.12.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Dave Airlie <airlied@redhat.com> 0.12.0-1
- libpciaccess 0.12

* Tue Mar 16 2010 Adam Jackson <ajax@redhat.com> 0.11.0-1
- libpciaccess 0.11

* Wed Dec 09 2009 Adam Jackson <ajax@redhat.com> 0.10.9-2.20091209
- New git snapshot
- Drop the fd cache patch

* Fri Sep 25 2009 Dave Airlie <airlied@redhat.com> 0.10.9-1
- rebase to latest upstream release - drop patches

* Thu Aug 06 2009 Dave Airlie <airlied@redhat.com> 0.10.6-7
- disable rom reading fallbacks

* Wed Aug 05 2009 Adam Jackson <ajax@redhat.com> 0.10.6-6
- D'oh.  Fix obvious sense inversion in the previous patch.

* Wed Aug 05 2009 Adam Jackson <ajax@redhat.com> 0.10.6-5
- libpciaccess-0.10.6-rom-sanity.patch: If we hit the /dev/mem path for
  reading a device's ROM, verify that it looks like it at least might belong
  to the device in question by checking vendor and device ID match.  Fixes
  vbetool post hanging forever (and thus blocking boot) on some dual-gpu
  laptops.

* Mon Aug 03 2009 Dave Airlie <airlied@redhat.com> 0.10.6-4
- Add support for default vga arb device selection
- Update libpciaccess VGA arb code for newer kernel API

* Fri Jul 31 2009 Dave Airlie <airlied@redhat.com> 0.10.6-3
- enable autoreconf to rebuild configure properly

* Fri Jul 31 2009 Dave Airlie <airlied@redhat.com> 0.10.6-2
- libpciaccess-vga-arbiter.patch: add vga arbiter support to libpciaccess

* Mon Jul 27 2009 Dave Airlie <airlied@redhat.com> 0.10.6-1
- rebase to latest release (will do release with VGA bits later)
- libpciaccess-boot-vga.patch: add boot vga patch from upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 21 2009 Adam Jackson <ajax@redhat.com> 0.10.5-1
- libpciaccess 0.10.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Kristian Høgsberg <krh@redhat.com> - 0.10.3-5
- Unbreak the rom-size patch.

* Sun Feb 15 2009 Kristian Høgsberg <krh@redhat.com> - 0.10.3-4
- Don't read more than the advertised rom_size.

* Thu Aug 28 2008 Adam Jackson <ajax@redhat.com> 0.10.3-3
- Rediff for --fuzz=0

* Wed Jul 02 2008 Adam Jackson <ajax@redhat.com> 0.10.3-2
- Fix file access mode in config fd cache. (#452910)

* Tue Jul 01 2008 Adam Jackson <ajax@redhat.com> 0.10.3-1
- libpciaccess 0.10.3

* Tue May 20 2008 Adam Jackson <ajax@redhat.com> 0.10-3
- libpciaccess-no-pci-fix.patch: Fix init when /sys/bus/pci is empty or
  nonexistent.

* Mon Apr 21 2008 Dave Airlie <airlied@redhat.com> 0.10-2
- fix major problem with libpciaccess and write combining.

* Thu Mar 06 2008 Adam Jackson <ajax@redhat.com> 0.10-1
- libpciaccess 0.10

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-4.20071031
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Adam Jackson <ajax@redhat.com> 0.9.1-3.20071031
- libpciaccess-fd-cache.patch: Cache sysfs PCI config space file
  descriptors for great boot speed justice.

* Wed Oct 31 2007 Kristian Høgsberg <krh@redhat.com> 0.9.1-2.20071031
- New snapshot, git revision e392082abb5696c8837224da86cc0af4f21d7010.
- Pick up new .so file.

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 0.9.1-1
- libpciaccess 0.9.1

* Mon Aug 27 2007 Adam Jackson <ajax@redhat.com> 0.8-0.4.20070827git
- New snapshot.

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> 0.8-0.3.20070712git
- Rebuild for PPC toolchain bug

* Thu Jul 12 2007 Adam Jackson <ajax@redhat.com> 0.8-0.2.20070712git
- New snapshot.  Adds VGA ROM support.

* Thu May 24 2007 Adam Jackson <ajax@redhat.com> 0.8-0.1.20070524git
- Initial revision.
