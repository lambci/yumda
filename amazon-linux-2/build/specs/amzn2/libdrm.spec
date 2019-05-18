#define gitdate 20130117

Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.83
Release: 2%{?dist}.0.2
License: MIT
Group: System Environment/Libraries
URL: http://dri.sourceforge.net
%if 0%{?gitdate}
Source0: %{name}-%{gitdate}.tar.bz2
%else
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2
%endif
Source1: make-git-snapshot.sh

Requires: udev

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

Source2: 91-drm-modeset.rules

# backport from upstream master seems like it should be in here.
Patch1: 0001-intel-Change-a-KBL-pci-id-to-GT2-from-GT1.5.patch
# hardcode the 666 instead of 660 for device nodes
Patch3: libdrm-make-dri-perms-okay.patch
# remove backwards compat not needed on Fedora
Patch4: libdrm-2.4.0-no-bc.patch
# make rule to print the list of test programs
Patch5: libdrm-2.4.25-check-programs.patch

#Backport some intel pci ids.
Patch10: 0002-intel-Add-more-Coffeelake-PCI-IDs.patch

%description
Direct Rendering Manager runtime library

%package devel
Summary: Direct Rendering Manager development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers >= 2.6.27-0.144.rc0.git2.fc10
Requires: pkgconfig

%description devel
Direct Rendering Manager development package

%package -n drm-utils
Summary: Direct Rendering Manager utilities
Group: Development/Tools
Requires: libdrm = %{version}-%{release}

%description -n drm-utils
Utility programs for the kernel DRM interface.  Will void your warranty.

%prep
%setup -q %{?gitdate:-n %{name}-%{gitdate}}
%patch1 -p1 -b .intelfix
%patch3 -p1 -b .forceperms
%patch4 -p1 -b .no-bc
%patch5 -p1 -b .check

%patch10 -p1 -b .cfl

%build
autoreconf -v --install || exit 1
%configure \
%ifarch %{arm}
	--enable-exynos-experimental-api \
	--enable-omap-experimental-api \
	--enable-tegra-experimental-api \
%endif
	--enable-install-test-programs \
	--enable-udev
make %{?_smp_mflags}
pushd tests
make %{?smp_mflags} `make check-programs`
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd tests
mkdir -p $RPM_BUILD_ROOT%{_bindir}
for foo in $(make check-programs) ; do
libtool --mode=install install -m 0755 $foo %{buildroot}%{_bindir}
done
popd
# SUBDIRS=libdrm
mkdir -p $RPM_BUILD_ROOT/usr/lib/udev/rules.d/
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/udev/rules.d/

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :
for i in r300_reg.h via_3d_reg.h
do
rm -f $RPM_BUILD_ROOT/usr/include/libdrm/$i
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so.1
%{_libdir}/libdrm_intel.so.1.0.0
%endif
%ifarch %{arm}
%{_libdir}/libdrm_exynos.so.1
%{_libdir}/libdrm_exynos.so.1.0.0
%{_libdir}/libdrm_omap.so.1
%{_libdir}/libdrm_omap.so.1.0.0
%{_libdir}/libdrm_tegra.so.0
%{_libdir}/libdrm_tegra.so.0.0.0
%endif
%ifarch %{arm} aarch64
%{_libdir}/libdrm_freedreno.so.1
%{_libdir}/libdrm_freedreno.so.1.0.0
%endif
%{_libdir}/libdrm_amdgpu.so.1
%{_libdir}/libdrm_amdgpu.so.1.0.0
%{_libdir}/libdrm_radeon.so.1
%{_libdir}/libdrm_radeon.so.1.0.1
%{_libdir}/libdrm_nouveau.so.2
%{_libdir}/libdrm_nouveau.so.2.0.0
%{_libdir}/libkms.so.1
%{_libdir}/libkms.so.1.0.0
%{_datadir}/libdrm/amdgpu.ids
/usr/lib/udev/rules.d/91-drm-modeset.rules

%files -n drm-utils
%defattr(-,root,root,-)
%{_bindir}/drmdevice
%{_bindir}/modetest
%{_bindir}/modeprint
%{_bindir}/vbltest
%{_bindir}/kmstest
%{_bindir}/kms-steal-crtc
%{_bindir}/kms-universal-planes
%exclude %{_bindir}/exynos*
%exclude %{_bindir}/drmsl
%exclude %{_bindir}/hash
%exclude %{_bindir}/proptest
%exclude %{_bindir}/random

%files devel
%defattr(-,root,root,-)
# FIXME should be in drm/ too
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%{_includedir}/libsync.h
%dir %{_includedir}/libdrm
%{_includedir}/libdrm/drm.h
%{_includedir}/libdrm/drm_fourcc.h
%{_includedir}/libdrm/drm_mode.h
%{_includedir}/libdrm/drm_sarea.h
%ifarch %{ix86} x86_64 ia64
%{_includedir}/libdrm/intel_aub.h
%{_includedir}/libdrm/intel_bufmgr.h
%{_includedir}/libdrm/intel_debug.h
%endif
%ifarch %{arm}
%{_includedir}/libdrm/exynos_drmif.h
%{_includedir}/libdrm/omap_drmif.h
%{_includedir}/libdrm/tegra.h
%{_includedir}/exynos/
%{_includedir}/omap/
%endif
%ifarch %{arm} aarch64
%{_includedir}/freedreno/
%{_includedir}/libdrm/vc4_packet.h
%{_includedir}/libdrm/vc4_qpu_defines.h
%endif
%{_includedir}/libdrm/amdgpu.h
%{_includedir}/libdrm/radeon_bo.h
%{_includedir}/libdrm/radeon_bo_gem.h
%{_includedir}/libdrm/radeon_bo_int.h
%{_includedir}/libdrm/radeon_cs.h
%{_includedir}/libdrm/radeon_cs_gem.h
%{_includedir}/libdrm/radeon_cs_int.h
%{_includedir}/libdrm/radeon_surface.h
%{_includedir}/libdrm/r600_pci_ids.h
%{_includedir}/libdrm/*_drm.h
%{_includedir}/libdrm/nouveau/*.h
%{_includedir}/libdrm/nouveau/nvif/*.h
%{_includedir}/libkms
%{_libdir}/libdrm.so
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so
%endif
%ifarch %{arm}
%{_libdir}/libdrm_exynos.so
%{_libdir}/libdrm_omap.so
%{_libdir}/libdrm_tegra.so
%endif
%ifarch %{arm} aarch64
%{_libdir}/libdrm_freedreno.so
%endif
%{_libdir}/libdrm_radeon.so
%{_libdir}/libdrm_amdgpu.so
%{_libdir}/libdrm_nouveau.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm.pc
%ifarch %{ix86} x86_64 ia64
%{_libdir}/pkgconfig/libdrm_intel.pc
%endif
%ifarch %{arm}
%{_libdir}/pkgconfig/libdrm_exynos.pc
%{_libdir}/pkgconfig/libdrm_omap.pc
%{_libdir}/pkgconfig/libdrm_tegra.pc
%endif
%ifarch %{arm} aarch64
%{_libdir}/pkgconfig/libdrm_freedreno.pc
%{_libdir}/pkgconfig/libdrm_vc4.pc
%endif
%{_libdir}/pkgconfig/libdrm_radeon.pc
%{_libdir}/pkgconfig/libdrm_amdgpu.pc
%{_libdir}/pkgconfig/libdrm_nouveau.pc
%{_libdir}/pkgconfig/libkms.pc
%{_mandir}/man3/drm*.3*
%{_mandir}/man7/drm*.7*

%changelog
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
