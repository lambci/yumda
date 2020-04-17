Name:           v4l-utils
Version:        0.9.5
Release: 4%{?dist}.0.1
Summary:        Utilities for video4linux and DVB devices
Group:          Applications/System
# ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
Patch1:         0001-rds-ctl-fix-percentage-handling.patch
Patch2:         0002-libv4l2rds-support-RDS-EON-and-TMC-tuning-info.patch
Patch3:         0003-rds-ctl-support-RDS-EON-and-TMC-tuning-info.patch
Patch4:         0004-libv4l2rds.c-moving-functions-to-get-rid-of-declarat.patch
Patch5:         0005-rds-ctl-support-d10-to-refer-to-radio10.patch
Patch6:         0006-libv4l2-Add-logging-of-dqbuf-timestamps-to-debug-log.patch
BuildRequires:  libjpeg-devel qt4-devel kernel-headers desktop-file-utils
# For /lib/udev/rules.d ownership
Requires:       udev
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package -n     libv4l
Summary:        Collection of video4linux support libraries 
Group:          System Environment/Libraries
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html
Prefix: %{_prefix}

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1


%build
%configure --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm $RPM_BUILD_ROOT%{_libdir}/{v4l1compat.so,v4l2convert.so}


%files -n libv4l
%license COPYING.LIB COPYING
%{_libdir}/libdvbv5.so.*
%{_libdir}/libv4l
%{_libdir}/libv4l*.so.*

%exclude %{_bindir}
%exclude %{_sbindir}
%exclude %{_datadir}
%exclude %{_sysconfdir}
%exclude %{_udevrulesdir}
%exclude %{_mandir}
%exclude %{_includedir}
%exclude /usr/lib/udev
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.5-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.5-3
- Mass rebuild 2013-12-27

* Fri Jun 14 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.5-2
- Add a few libv4l2rds patches from upstream, which bring libv4l2rds to its
  final API / ABI, so that apps build against it won't need a rebuild in the
  future

* Sun Jun  9 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.5-1
- New upstream release 0.9.5 (rhbz#970412)
- Modernize specfile a bit

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.8.8-5
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.8.8-4
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.8-2
- Cherry-pick 2 patches from upstream git fixing an exotic crash (rhbz#838279)

* Tue May 22 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.8-1
- New upstream release 0.8.8
- Add patches from upstream git to improve Pixart JPEG decoding
- Add patch from upstream git to fix building with latest kernels (rhbz#823863)

* Mon Apr  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.7-1
- New upstream release 0.8.7
- Fixes rhbz#807656

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Hans de Goede <hdegoede@redhat.com> 0.8.5-1
- New upstream release 0.8.5
- Fixes rhbz#711492

* Wed Jun  1 2011 Hans de Goede <hdegoede@redhat.com> 0.8.4-1
- New upstream release 0.8.4

* Sat Mar 12 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-2
- Add a .desktop file for qv4l2
- Add fully versioned Requires on libv4l to other (sub)packages

* Thu Feb 10 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-1
- New upstream release 0.8.3

* Wed Jan 26 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-3
- Add missing BuildRequires: kernel-headers

* Mon Jan 24 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-2
- Change tarbal to official upstream 0.8.2 release
- This fixes multiple Makefile issues pointed out in the review (#671883)
- Add ir-keytable config files
- Explicitly specify CXXFLAGS so that qv4l2 gets build with rpm_opt_flags too

* Sat Jan 22 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-1
- Initial Fedora package
