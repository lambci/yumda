%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       libxcb
Version:    1.12
Release: 1%{?dist}.0.2
Summary:    A C binding to the X11 protocol
License:    MIT
URL:        http://xcb.freedesktop.org/

Source0:    http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2

# This is stolen straight from the pthread-stubs source:
# http://cgit.freedesktop.org/xcb/pthread-stubs/blob/?id=6900598192bacf5fd9a34619b11328f746a5956d
# we don't need the library because glibc has working pthreads, but we need
# the pkgconfig file so libs that link against libxcb know this...
Source1:    pthread-stubs.pc.in

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(xau) >= 0.99.2
BuildRequires:  pkgconfig(xcb-proto) >= 1.12
BuildRequires:  pkgconfig(xorg-macros) >= 1.18
#BuildRequires:  xorg-x11-proto-devel

Prefix: %{_prefix}

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%prep
%autosetup -p1

%build
sed -i 's/pthread-stubs //' configure.ac
# autoreconf -f needed to expunge rpaths
autoreconf -v -f --install
%configure \
  --enable-shm \
  --enable-render \
  --disable-static \
  --disable-silent-rules \
  --disable-devel-docs \
  --without-doxygen \
  --disable-damage \
  --disable-dpms \
  --disable-dri2 \
  --disable-dri3 \
  --disable-glx \
  --disable-present \
  --disable-randr \
  --disable-record \
  --disable-resource \
  --disable-screensaver \
  --disable-shape \
  --enable-sync \
  --disable-xevie \
  --disable-xfixes \
  --disable-xfree86-dri \
  --disable-xinerama \
  --disable-xinput \
  --disable-xkb \
  --disable-xprint \
  --disable-selinux \
  --disable-xtest \
  --disable-xv \
  --disable-xvmc

# Remove rpath from libtool (extra insurance if autoreconf is ever dropped)
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%license COPYING
%{_libdir}/libxcb-composite.so.0*
%{_libdir}/libxcb-render.so.0*
%{_libdir}/libxcb-shm.so.0*
%{_libdir}/libxcb.so.1*
%{_libdir}/libxcb-sync.so.1*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed May 18 2016 Adam Jackson <ajax@redhat.com> - 1.12-1
- libxcb 1.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Adam Jackson <ajax@redhat.com> 1.11.1-1
- libxcb 1.11.1

* Thu Jun 25 2015 Rex Dieter <rdieter@fedoraproject.org> 1.11-8
- followup fix for thread deadlocks (#1193742, fdo#84252)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Rex Dieter <rdieter@fedoraproject.org> 1.11-6
- pull in (partial?) upstream fix for deadlocks (#1193742, fdo#84252)

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.11-5
- fix rpath harder (#1136546)
- %%build: --disable-silent-rules

* Tue May 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.11-4
- fix fpath (use autoreconf -f)
- -devel: tighten deps via %%{?_isa}, drop Requires: pkgconfig (add explicit BR: pkgconfig)

* Thu Jan 08 2015 Simone Caronni <negativo17@gmail.com> - 1.11-3
- Clean up SPEC file, fix rpmlint warnings.
- Enable XInput extension (#1177701).

* Fri Oct 24 2014 Dan Horák <dan@danny.cz> - 1.11-2
- rebuilt for broken koji db - no buildroot info

* Wed Oct 01 2014 Adam Jackson <ajax@redhat.com> 1.11-1
- libxcb 1.11

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Adam Jackson <ajax@redhat.com> 1.10-1
- libxcb 1.10 plus one. Updated ABIs: sync, xkb. New libs: dri3, present.

* Tue Aug  6 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.9.1-3
- Install docs to %%{_pkgdocdir} where available.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- libxcb 1.9.1

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.9-3
- Fix integer overflow in read_packet (CVE-2013-2064)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Adam Jackson <ajax@redhat.com> 1.9-1
- libxcb 1.9

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.8.1-4
- --enable-xkb for weston
- --disable-xprint instead of manual rm
- BuildRequire an updated xcb-proto for XKB and DRI2 fixes

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 09 2012 Adam Jackson <ajax@redhat.com> 1.8.1-1
- libxcb 1.8.1

* Fri Jan 13 2012 Adam Jackson <ajax@redhat.com> 1.8-2
- Don't %%doc in the base package, that pulls in copies of things we only
  want in -doc subpackage.

* Wed Jan 11 2012 Adam Jackson <ajax@redhat.com> 1.8-1
- libxcb 1.8
