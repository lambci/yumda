#define gitdate 20130117

Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.97
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://dri.sourceforge.net
%if 0%{?gitdate}
Source0: %{name}-%{gitdate}.tar.bz2
%else
Source0: https://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2
%endif
Source1: make-git-snapshot.sh
Source2: README.rst

BuildRequires: pkgconfig automake autoconf libtool
BuildRequires: kernel-headers
BuildRequires: libxcb-devel
%if 0%{?fedora} > 17 || 0%{?rhel} > 6
BuildRequires: systemd-devel
%else
BuildRequires: libudev-devel
%endif
BuildRequires: libatomic_ops-devel
BuildRequires: libpciaccess-devel
BuildRequires: libxslt docbook-style-xsl
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le s390x armv7hl aarch64
BuildRequires: valgrind-devel
%endif
BuildRequires: xorg-x11-util-macros

# hardcode the 666 instead of 660 for device nodes
Patch3: libdrm-make-dri-perms-okay.patch
# remove backwards compat not needed on Fedora
Patch4: libdrm-2.4.0-no-bc.patch
# make rule to print the list of test programs
Patch5: libdrm-2.4.25-check-programs.patch

# amdgpu names update
Patch10: 0001-amdgpu-add-some-raven-marketing-names.patch
# intel pciids update
Patch11: 0001-intel-sync-i915_pciids.h-with-kernel.patch

Prefix: %{_prefix}

%description
Direct Rendering Manager runtime library

%prep
%setup -q %{?gitdate:-n %{name}-%{gitdate}}
%patch3 -p1 -b .forceperms
%patch4 -p1 -b .no-bc
%patch5 -p1 -b .check
%patch10 -p1 -b .amdnames
%patch11 -p1 -b .intelid

%build
autoreconf -v --install || exit 1
%configure \
	--disable-install-test-programs \
  --disable-cairo-tests \
	--disable-udev
make %{?_smp_mflags}
cp %{SOURCE2} .

%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

%files
%defattr(-,root,root,-)
%license README.rst
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%{_libdir}/libdrm_intel.so.1
%{_libdir}/libdrm_intel.so.1.0.0
%{_libdir}/libdrm_amdgpu.so.1
%{_libdir}/libdrm_amdgpu.so.1.0.0
%{_libdir}/libdrm_radeon.so.1
%{_libdir}/libdrm_radeon.so.1.0.1
%{_libdir}/libdrm_nouveau.so.2
%{_libdir}/libdrm_nouveau.so.2.0.0
%{_libdir}/libkms.so.1
%{_libdir}/libkms.so.1.0.0
%{_datadir}/libdrm/amdgpu.ids

%exclude %{_bindir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_mandir}

%changelog
* Thu Apr 23 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Feb 20 2019 Dave Airlie <airlied@redhat.com> - 2.4.97-2
- Add some new i915 pci ids, and amd marketing names

* Thu Jan 31 2019 Dave Airlie <airlied@redhat.com> - 2.4.97-1
- libdrm 2.4.97 (readd README)

* Wed Aug 22 2018 Rob Clark <rclark@redhat.com> - 2.4.91-3
- Add WHL, AML, etc PCI IDs

* Tue Apr 24 2018 Adam Jackson <ajax@redhat.com> - 2.4.91-2
- libdrm 2.4.91

* Fri Jan 12 2018 Dave Airlie <airlied@redhat.com> - 2.4.83-2
- Add some Coffeelake PCI IDs

* Fri Oct 06 2017 Dave Airlie <airlied@redhat.com> - 2.4.83-1
- libdrm 2.4.83

* Wed Jan 18 2017 Dave Airlie <airlied@redhat.com> - 2.4.74-1
- libdrm 2.4.74

* Tue Aug 09 2016 Rob Clark <rclark@redhat.com> - 2.4.67-3
- kbl pci ids.

* Tue Jun 14 2016 Dave Airlie <airlied@redhat.com> - 2.4.67-2
- add missing intel pci ids.

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 2.4.67-1
- libdrm 2.4.67

* Fri May 22 2015 Dave Airlie <airlied@redhat.com> 2.4.60-3
- backport nouveau fix from 2.4.61

* Mon May 04 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.4.60-2
- RHEL7 rpmdiff fixes

* Mon Mar 23 2015 Dave Airlie <airlied@redhat.com> 2.4.60-1
- libdrm 2.4.60

* Fri Jan 23 2015 Rob Clark <rclark@redhat.com> 2.4.59-4
- No we don't actually want to install the exynos tests

* Fri Jan 23 2015 Rob Clark <rclark@redhat.com> 2.4.59-3
- Add test apps to drm-utils package

* Thu Jan 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.59-2
- Enable tegra

* Thu Jan 22 2015 Dave Airlie <airlied@redhat.com> 2.4.59-1
- libdrm 2.4.59

* Wed Nov 19 2014 Dan Horák <dan[at]danny.cz> 2.4.58-3
- valgrind available only on selected arches

* Tue Nov 18 2014 Adam Jackson <ajax@redhat.com> 2.4.58-2
- BR: valgrind-devel so we get ioctl annotations

* Thu Oct 02 2014 Adam Jackson <ajax@redhat.com> 2.4.58-1
- libdrm 2.4.58

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Dave Airlie <airlied@redhat.com> 2.4.56-1
- libdrm 2.4.56

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.54-3
- Build freedreno support on aarch64 too

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 Dennis Gilmore <dennis@ausil.us> 2.4.54-1
- libdrm 2.4.54

* Sun Apr 13 2014 Dave Airlie <airlied@redhat.com> 2.4.53-1
- libdrm 2.4.53

* Sat Feb 08 2014 Adel Gadllah <adel.gadllah@gmail.com> 2.4.52-1
- libdrm 2.4.52

* Thu Dec 05 2013 Dave Airlie <airlied@redhat.com> 2.4.50-1
- libdrm 2.4.50

* Mon Dec 02 2013 Dave Airlie <airlied@redhat.com> 2.4.49-2
- backport two fixes from master

* Sun Nov 24 2013 Dave Airlie <airlied@redhat.com> 2.4.49-1
- libdrm 2.4.49

* Fri Nov 08 2013 Dave Airlie <airlied@redhat.com> 2.4.47-1
- libdrm 2.4.47

- add fix for nouveau with gcc 4.8
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Dave Airlie <airlied@redhat.com> 2.4.46-1
- libdrm 2.4.46

* Tue Jun 18 2013 Adam Jackson <ajax@redhat.com> 2.4.45-2
- Sync some Haswell updates from git

* Thu May 16 2013 Dave Airlie <airlied@redhat.com> 2.4.45-1
- libdrm 2.4.45

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.44-2
- enable freedreno support on ARM

* Fri Apr 19 2013 Jerome Glisse <jglisse@redhat.com> 2.4.44-1
- libdrm 2.4.44

* Fri Apr 12 2013 Adam Jackson <ajax@redhat.com> 2.4.43-1
- libdrm 2.4.43

* Tue Mar 12 2013 Dave Airlie <airlied@redhat.com> 2.4.42-2
- add qxl header file

* Tue Feb 05 2013 Adam Jackson <ajax@redhat.com> 2.4.42-1
- libdrm 2.4.42

* Tue Jan 22 2013 Adam Jackson <ajax@redhat.com> 2.4.41-2
- Fix directory ownership in -devel (#894468)

* Thu Jan 17 2013 Adam Jackson <ajax@redhat.com> 2.4.41-1
- libdrm 2.4.41 plus git.  Done as a git snapshot instead of the released
  2.4.41 since the release tarball is missing man/ entirely. 
- Pre-F16 changelog trim

* Wed Jan 09 2013 Ben Skeggs <bskeggs@redhat.com> 2.4.40-2
- nouveau: fix bug causing kernel to reject certain command streams

* Tue Nov 06 2012 Dave Airlie <airlied@redhat.com> 2.4.40-1
- libdrm 2.4.40

* Thu Oct 25 2012 Adam Jackson <ajax@redhat.com> 2.4.39-4
- Rebuild to appease koji and get libkms on F18 again

* Mon Oct 08 2012 Adam Jackson <ajax@redhat.com> 2.4.39-3
- Add exynos to arm

* Mon Aug 27 2012 Dave Airlie <airlied@redhat.com> 2.4.39-1
- upstream 2.4.39 release

* Tue Aug 14 2012 Dave Airlie <airlied@redhat.com> 2.4.38-2
- add radeon prime support

* Sun Aug 12 2012 Dave Airlie <airlied@redhat.com> 2.4.38-1
- upstream 2.4.38 release

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 25 2012 Dave Airlie <airlied@redhat.com> 2.4.37-3
- add libdrm prime support for core, intel, nouveau

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 2.4.37-2
- libdrm-2.4.37-i915-hush.patch: Silence an excessive error message

* Fri Jul 13 2012 Dave Airlie <airlied@redhat.com> 2.4.37-1
- bump to libdrm 2.4.37

* Thu Jun 28 2012 Dave Airlie <airlied@redhat.com> 2.4.36-1
- bump to libdrm 2.4.36

* Mon Jun 25 2012 Adam Jackson <ajax@redhat.com> 2.4.35-2
- Drop libkms. Only used by plymouth, and even that's a mistake.

* Fri Jun 15 2012 Dave Airlie <airlied@redhat.com> 2.4.35-1
- bump to libdrm 2.4.35

* Tue Jun 05 2012 Adam Jackson <ajax@redhat.com> 2.4.34-2
- Rebuild for new libudev
- Conditional BuildReqs for {libudev,systemd}-devel

* Sat May 12 2012 Dave Airlie <airlied@redhat.com> 2.4.34-1
- libdrm 2.4.34

* Fri May 11 2012 Dennis Gilmore <dennis@ausil.us> 2.4.34-0.3
- enable libdrm_omap on arm arches

* Thu May 10 2012 Adam Jackson <ajax@redhat.com> 2.4.34-0.2
- Drop ancient kernel Requires.

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> - 2.4.34-0.1.20120424
- Update to a newer git snapshot

* Sat Mar 31 2012 Dave Airlie <airlied@redhat.com> 2.4.33-1
- libdrm 2.4.33
- drop libdrm-2.4.32-tn-surface.patch

* Wed Mar 21 2012 Adam Jackson <ajax@redhat.com> 2.4.32-1
- libdrm 2.4.32
- libdrm-2.4.32-tn-surface.patch: Sync with git.

* Sat Feb 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.31-4
- Add gem_ binaries to x86 only exclusion too

* Wed Feb 22 2012 Adam Jackson <ajax@redhat.com> 2.4.31-3
- Fix build on non-Intel arches

* Tue Feb 07 2012 Jerome Glisse <jglisse@redhat.com> 2.4.31-2
- Fix missing header file

* Tue Feb 07 2012 Jerome Glisse <jglisse@redhat.com> 2.4.31-1
- upstream 2.4.31 release

* Fri Jan 20 2012 Dave Airlie <airlied@redhat.com> 2.4.30-1
- upstream 2.4.30 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Adam Jackson <ajax@redhat.com> 2.4.27-2
- Fix typo in udev rule

* Tue Nov 01 2011 Adam Jackson <ajax@redhat.com> 2.4.27-1
- libdrm 2.4.27

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.26-4
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Adam Jackson <ajax@redhat.com> 2.4.26-3
- Fix udev rule matching and install location (#748205)

* Fri Oct 21 2011 Dave Airlie <airlied@redhat.com> 2.4.26-2
- fix perms on control node in udev rule

* Mon Jun 06 2011 Adam Jackson <ajax@redhat.com> 2.4.26-1
- libdrm 2.4.26 (#711038)
