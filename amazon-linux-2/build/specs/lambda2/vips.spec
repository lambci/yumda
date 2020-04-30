# remirepo spec file for vips, from:
#
# Fedora spec file for vips
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global vips_version_base 8.9
%global vips_version %{vips_version_base}.2
%global vips_soname_major 42
#global vips_prever rc4
%global vips_tarver %{vips_version}%{?vips_prever:-%{vips_prever}}

%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_libimagequant 1
%else
%global with_libimagequant 0
%endif

# from mock config, when rpmfusion enabled
%global with_libheif       0%{?_with_rpmfusion:1}

%if %{with_libheif}
Name:		vips-full
# Keep vips-full release > vips release
Release:	2%{?dist}
%else
Name:		vips
Release:	1%{?dist}
%endif
Version:	%{vips_version}%{?vips_prever:~%{vips_prever}}
Summary:	C/C++ library for processing large images

License:	LGPLv2+
URL:		https://libvips.github.io/libvips/
Source0:	https://github.com/libvips/libvips/releases/download/v%{vips_version}%{?vips_prever:-%{vips_prever}}/vips-%{vips_tarver}.tar.gz

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fftw3)
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
BuildRequires:	ImageMagick-devel
%else
# Ensure we use version 6 (same as imagick ext).
BuildRequires:	ImageMagick6-devel
%endif
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(matio)
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng) >= 1.2.9
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(openslide)
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(librsvg-2.0) >= 2.40.3
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(libjpeg)
%if %{with_libheif}
BuildRequires:	pkgconfig(libheif)
%endif
%if %{with_libimagequant}
#BuildRequires:	pkgconfig(imagequant) TODO only in 2.12+
BuildRequires:	libimagequant-devel
%endif
BuildRequires:	giflib-devel
BuildRequires:	pkgconfig(gthread-2.0)

BuildRequires:	gcc-c++
BuildRequires:	pkgconfig gettext

%if %{with_libheif}
Conflicts:      vips         < %{version}-%{release}
Provides:       vips         = %{version}-%{release}
Provides:       vips%{?_isa} = %{version}-%{release}
%endif

Prefix: %{_prefix}

%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.


%package tools
Summary:	Command-line tools for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if %{with_libheif}
Conflicts:  vips-tools < %{version}-%{release}
%endif
Prefix: %{_prefix}

%description tools
The %{name}-tools package contains command-line tools for working with VIPS.


%prep
%setup -q -n vips-%{vips_version}

# make the version string consistent for multiarch
export FAKE_BUILD_DATE=$(date -r %{SOURCE0})
sed -i "s/\\(VIPS_VERSION_STRING=\\)\$VIPS_VERSION-\`date\`/\\1\"\$VIPS_VERSION-$FAKE_BUILD_DATE\"/g" \
	configure
unset FAKE_BUILD_DATE

# Avoid setting RPATH to /usr/lib64 on 64-bit builds
# The DIE_RPATH_DIE trick breaks the build wrt gobject-introspection
sed -i 's|sys_lib_dlsearch_path_spec="|sys_lib_dlsearch_path_spec="/%{_lib} %{_libdir} |' configure


%build
# Upstream recommends enabling auto-vectorization of inner loops:
# https://github.com/jcupitt/libvips/pull/212#issuecomment-68177930
export CFLAGS="%{optflags} -ftree-vectorize"
export CXXFLAGS="%{optflags} -ftree-vectorize"
%configure \
%if %{with_libheif}
    --with-heif \
%else
    --without-heif \
%endif
    --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
find %{buildroot} \( -name '*.la' -o -name '*.a' \) -exec rm -f {} ';'

# delete doc (we will get it later with %%doc)
rm -rf %{buildroot}%{_datadir}/doc/vips

sed -e 's:/usr/bin/python:%{_bindir}/python3:' -i %{buildroot}/%{_bindir}/vipsprofile


%files
%license COPYING
%{_libdir}/*.so.%{vips_soname_major}*
%{_libdir}/girepository-1.0

%files tools
%{_bindir}/*

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}


%changelog
* Thu Apr 30 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Apr 21 2020 Remi Collet <remi@remirepo.net> - 8.9.2-1
- update to 8.9.2

* Tue Apr 21 2020 Remi Collet <remi@remirepo.net> - 8.9.1-3
- build against ImageMagick on EL-7

* Tue Jan 28 2020 Remi Collet <remi@remirepo.net> - 8.9.1-1
- update to 8.9.1
- ensure vips-devel pull right ImageMagick-devel version
  https://github.com/remicollet/remirepo/issues/134

* Wed Jan  8 2020 Remi Collet <remi@remirepo.net> - 8.9.0-1
- update to 8.9.0

* Fri Jan  3 2020 Remi Collet <remi@remirepo.net> - 8.9.0~rc4-1
- update to 8.9.0-rc4
- open https://github.com/libvips/libvips/issues/1513
  ABI compatibility with 8.8.0

* Fri Dec  6 2019 Remi Collet <remi@remirepo.net> - 8.8.4-1
- update to 8.8.4

* Tue Oct  1 2019 Remi Collet <remi@remirepo.net> - 8.8.3-3
- rebuild with matio / hdf5 fom EPEL

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 8.8.3-1
- update to 8.8.3

* Fri Aug 30 2019 Remi Collet <remi@remirepo.net> - 8.8.2-1
- update to 8.8.2

* Mon Jul  8 2019 Remi Collet <remi@remirepo.net> - 8.8.1-1
- update to 8.8.1

* Wed May 22 2019 Remi Collet <remi@remirepo.net> - 8.8.0-1
- update to 8.8.0

* Thu May 16 2019 Remi Collet <remi@remirepo.net> - 8.8.0~rc3-1
- update to 8.8.0-rc3

* Thu May  9 2019 Remi Collet <remi@remirepo.net> - 8.8.0~rc2-1
- update to 8.8.0-rc2

* Mon May  6 2019 Remi Collet <remi@remirepo.net> - 8.8.0~rc1-1
- update to 8.8.0-rc1
- drop libvipsCC
- drop python support

* Mon Mar 18 2019 Remi Collet <remi@remirepo.net> - 8.7.4-2
- rebuild using libwebp7

* Fri Jan 18 2019 Remi Collet <remi@remirepo.net> - 8.7.4-1
- update to 8.7.4

* Fri Jan  4 2019 Remi Collet <remi@remirepo.net> - 8.7.3-1
- update to 8.7.3

* Wed Dec 19 2018 Remi Collet <remi@remirepo.net> - 8.7.2-1
- update to 8.7.2
- rename vips-python to python2-vips
- rename vips-python3 to python3-vips
- drop python2 on F30 and EL8

* Tue Dec 18 2018 Remi Collet <remi@remirepo.net> - 8.7.0-3
- fix URL and sources (from jcupitt to libvips)
- requires pkgconfig(libjpeg) instead of libjpeg-turbo-devel

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 8.7.0-2
- EL-8 build

* Thu Sep 20 2018 Remi Collet <remi@remirepo.net> - 8.7.0-1
- update to 8.7.0

* Thu Aug 30 2018 Remi Collet <remi@remirepo.net> - 8.7.0~rc3-1
- update to 8.7.0~rc3

* Mon Aug 27 2018 Remi Collet <remi@remirepo.net> - 8.7.0~rc2-1
- update to 8.7.0~rc2

* Thu Jul 26 2018 Remi Collet <remi@remirepo.net> - 8.6.5-1
- update to 8.6.5

* Thu Jun 14 2018 Remi Collet <remi@remirepo.net> - 8.6.4-1
- Update to 8.6.4

* Wed Jun 13 2018 Remi Collet <remi@remirepo.net> - 8.6.3-3
- rebuild against ImageMagick6 (6.9.10-0)

* Tue May 29 2018 Remi Collet <remi@remirepo.net> - 8.6.3-2
- rebuild against ImageMagick6 new soname (6.9.9-47)

* Fri Mar  9 2018 Remi Collet <remi@remirepo.net> - 8.6.3-1
- Update to 8.6.3

* Thu Feb  1 2018 Remi Collet <remi@remirepo.net> - 8.6.2-1
- Update to 8.6.2

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 8.6.1-1
- Update to 8.6.1
- open https://github.com/jcupitt/libvips/issues/854

* Fri Dec  8 2017 Remi Collet <remi@remirepo.net> - 8.6.0-1
- Update to 8.6.0

* Wed Oct 11 2017 Remi Collet <remi@remirepo.net> - 8.5.9-1
- Update to 8.5.9

* Mon Oct  2 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha5-1
- update to 8.6.0-alpha5

* Mon Sep 11 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha4-1
- update to 8.6.0-alpha4

* Fri Sep  8 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha3-1
- update to 8.6.0-alpha3

* Thu Sep  7 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha2-1
- update to 8.6.0-alpha2

* Wed Sep  6 2017 Remi Collet <remi@remirepo.net> - 8.5.8-4
- rebuild using ImageMagick on F27+

* Fri Aug 25 2017 Remi Collet <remi@remirepo.net> - 8.5.8-3
- rebuild using ImageMagick on F25+

* Tue Aug 22 2017 Remi Collet <remi@remirepo.net> - 8.5.8-2
- F27 rebuild

* Tue Aug 22 2017 Remi Collet <remi@remirepo.net> - 8.5.8-1
- Update to 8.5.8

* Sat Aug  5 2017 Remi Collet <remi@remirepo.net> - 8.5.7-2
- rebuild against ImageMagick6 new soname (6.9.9-5)

* Wed Aug  2 2017 Remi Collet <remi@remirepo.net> - 8.5.7-1
- Update to 8.5.7

* Thu Jun  8 2017 Remi Collet <remi@remirepo.net> - 8.5.6-1
- Update to 8.5.6

* Mon May 15 2017 Remi Collet <remi@remirepo.net> - 8.5.5-1
- Update to 8.5.5

* Sun Apr 23 2017 Remi Collet <remi@remirepo.net> - 8.5.4-1
- Update to 8.5.4

* Fri Apr 21 2017 Remi Collet <remi@remirepo.net> - 8.5.3-1
- update to 8.5.3

* Mon Apr 10 2017 Remi Collet <remi@remirepo.net> - 8.5.2-1
- update to 8.5.2
- new site http://jcupitt.github.io/libvips/
- drop dependency on libxml2
- add dependency on expat

* Sun Jan 29 2017 Remi Collet <remi@remirepo.net> - 8.4.4-4
- rebuild against ImageMagick6 new soname (6.9.7-6)

* Mon Dec 12 2016 Remi Collet <remi@remirepo.net> - 8.4.4-3
- rebuild against ImageMagick6

* Tue Dec  6 2016 Remi Collet <remi@remirepo.net> - 8.4.4-2
- ensure ImageMagick v6 is used

* Thu Nov 24 2016 Remi Collet <remi@remirepo.net> - 8.4.4-1
- backport for repo repository
- disable python3 and doc sub-package

* Sun Nov 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.4-1
- New release

* Thu Oct 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.2-1
- New release

* Sun Sep 25 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.1-1
- New release

* Sat Aug 06 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.3-1
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 05 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-2
- Rebuilt for matio 1.5.7

* Tue May 10 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-1
- New release
- Verify that wrapper script name matches base version

* Thu Apr 14 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.0-1
- New release
- Add giflib, librsvg2, poppler-glib dependencies

* Mon Mar 28 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.3-1
- New release

* Sun Feb 21 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-3
- BuildRequire gcc-c++ per new policy

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-1
- New release

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 8.2.1-2
- Rebuild for hdf5 1.8.16

* Mon Jan 11 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.1-1
- New release

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.1.1-3
- Rebuilt for libwebp soname bump

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 18 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.1.1-1
- New release
- Update to new Python guidelines

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 8.0.2-2
- Rebuild for hdf5 1.8.15

* Wed May 06 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.0.2-1
- New release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.42.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 14 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.3-1
- New release

* Thu Feb 05 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.2-1
- New release
- Move license files to %%license

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 7.42.1-2
- Rebuild for hdf5 1.8.14

* Sun Dec 28 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.1-1
- New release
- Package new Python bindings
- Build with auto-vectorization

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 7.40.11-2
- rebuild (openexr)

* Wed Nov 05 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.11-1
- New release

* Thu Sep 25 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.9-1
- New release

* Fri Aug 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.6-1
- New release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.40.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.5-1
- New release

* Sat Jul 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.4-1
- New release

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 7.40.3-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 08 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.3-1
- New release

* Sun Jun 29 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.2-1
- New release
- Add libgsf dependency
- Fix version string consistency across architectures
- Use macros for package and soname versions

* Sun Jun 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.6-1
- New release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.38.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-2
- Rebuild for ImageMagick

* Wed Mar 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-1
- New release

* Tue Jan 21 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.1-1
- New release

* Thu Jan 09 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-3
- Rebuild for cfitsio

* Thu Jan 02 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-2
- Rebuild for libwebp

* Mon Dec 23 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-1
- New release

* Thu Nov 28 2013 Rex Dieter <rdieter@fedoraproject.org> 7.36.3-2
- rebuild (openexr)

* Wed Nov 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.3-1
- New release
- BuildRequire libwebp

* Sat Oct 05 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.0-1
- New release

* Tue Sep 10 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-2
- Rebuild for ilmbase 2.0

* Tue Aug 06 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-1
- New release
- Update -devel description: there are no man pages anymore

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Orion Poplawski <orion@cora.nwra.com> - 7.34.0-2
- Rebuild for cfitsio 3.350

* Sat Jun 29 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.0-1
- New release

* Fri Jun 28 2013 Kalev Lember <kalevlember@gmail.com> - 7.32.4-2
- Rebuilt with libpng 1.6

* Thu Jun 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.4-1
- New release

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 7.32.3-2
- Rebuild for hdf5 1.8.11

* Fri Apr 26 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.3-1
- New release

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.1-1
- New release

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-4
- Rebuild for cfitsio

* Sun Mar 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-3
- Rebuild for ImageMagick

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 7.32.0-2
- rebuild (OpenEXR)

* Thu Mar 07 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-1
- New release
- Stop setting rpath on 64-bit builds

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.30.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 7.30.7-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.7-1
- New release
- Modify %%files glob to catch accidental soname bumps
- Update BuildRequires

* Wed Nov 14 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.5-1
- New release

* Mon Oct 15 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.3-1
- New release
- Enable gobject introspection
- Add versioned dependency on base package
- Minor specfile cleanups

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 7.28.2-2
- Rebuild for new libmatio

* Fri Apr 13 2012 Adam Goode <adam@spicenitz.org> - 7.28.2-1
- New upstream release
   * libvips rewrite
   * OpenSlide support
   * better jpeg, png, tiff support
   * sequential mode read
   * operation cache

* Mon Jan 16 2012 Adam Goode <adam@spicenitz.org> - 7.26.7-1
- New upstream release
   * Minor fixes, mostly with reading and writing

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 7.26.3-2
- Rebuild for new libpng

* Sat Sep  3 2011 Adam Goode <adam@spicenitz.org> - 7.26.3-1
- New upstream release
   * More permissive operators
   * Better TIFF, JPEG, PNG, FITS support
   * VIPS rewrite!

* Fri Aug 12 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-2
- Clean up Requires and BuildRequires

* Wed Aug 10 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-1
- New upstream release

* Mon Feb 14 2011 Adam Goode <adam@spicenitz.org> - 7.24.2-1
- New upstream release
   * Run-time code generation, for 4x speedup in some operations
   * Open via disc mode, saving memory
   * FITS supported
   * Improved TIFF and JPEG load

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.22.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 jkeating - 7.22.2-1.2
- Rebuilt for gcc bug 634757

* Wed Sep 29 2010 jkeating - 7.22.2-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 7.22.2-2
- rebuild against ImageMagick

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 7.22.2-1.1
- rebuild (ImageMagick)

* Fri Aug  6 2010 Adam Goode <adam@spicenitz.org> - 7.22.2-1
- New upstream release (a few minor fixes)

* Tue Jul 27 2010 Adam Goode <adam@spicenitz.org> - 7.22.1-2
- Add COPYING to doc subpackage

* Tue Jul 27 2010 Adam Goode <adam@spicenitz.org> - 7.22.1-1
- New upstream release
   + More revision of VIPS library
   + New threading system
   + New command-line program, vipsthumbnail
   + Improved interpolators
   + German translation
   + PFM (portable float map) image format read and write
   + Much lower VM use with many small images open
   + Rewritten flood-fill

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.20.7-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-3
- Don't require gtk-doc anymore (resolves #604421)

* Sun Mar  7 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-2
- Rebuild for imagemagick soname change
- Remove some old RPM stuff

* Tue Feb  2 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-1
- New upstream release
   + C++ and Python bindings now have support for deprecated functions
   + Bugfixes for YCbCr JPEG TIFF files

* Wed Jan  6 2010 Adam Goode <adam@spicenitz.org> - 7.20.6-1
- New upstream release
   + About half of the VIPS library has been revised
   + Now using gtk-doc
   + Better image file support
   + MATLAB file read supported
   + New interpolation system
   + Support for Radiance files

* Fri Sep  4 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 7.18.2-1
- Update to 7.18.2 to sync with fixed nip2 FTBFS.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.16.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Adam Goode <adam@spicenitz.org> - 7.16.4-3
- Rebuild for ImageMagick soname change

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 28 2008 Adam Goode <adam@spicenitz.org> - 7.16.4-1
- New release

* Sun Dec 21 2008 Adam Goode <adam@spicenitz.org> - 7.16.3-1
- New release
- Update description

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.14.5-2
- Rebuild for Python 2.6

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 7.14.5-1
- New release

* Fri Jun 20 2008 Adam Goode <adam@spicenitz.org> - 7.14.4-1
- New release

* Sat Mar 15 2008 Adam Goode <adam@spicenitz.org> - 7.14.1-1
- New release

* Mon Mar 10 2008 Adam Goode <adam@spicenitz.org> - 7.14.0-1
- New release
- Remove GCC 4.3 patch (upstream)

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 7.12.5-5
- Fix GCC 4.3 build

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 7.12.5-4
- GCC 4.3 mass rebuild

* Tue Oct 23 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-3
- Eliminate build differences in version.h to work on multiarch

* Mon Oct 15 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-2
- Rebuild for OpenEXR update

* Fri Sep 21 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-1
- New upstream release

* Thu Aug 16 2007 Adam Goode <adam@spicenitz.org> - 7.12.4-2
- Add Conflicts for doc
- Update doc package description

* Thu Aug 16 2007 Adam Goode <adam@spicenitz.org> - 7.12.4-1
- New upstream release
- Update License tag

* Tue Jul 24 2007 Adam Goode <adam@spicenitz.org> - 7.12.2-1
- New stable release 7.12

* Sat May  5 2007 Adam Goode <adam@spicenitz.org> - 7.12.0-1
- New upstream release

* Thu Aug 31 2006 Adam Goode <adam@spicenitz.org> - 7.10.21-1
- New upstream release

* Fri Jul 28 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-3
- Include results of running automake in the patch for undefined symbols
- No longer run automake or autoconf (autoconf was never actually necessary)

* Mon Jul 24 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-2
- Eliminate undefined non-weak symbols in libvipsCC.so

* Fri Jul 21 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-1
- New upstream release
- Updated for FC5

* Tue Dec 14 2004 John Cupitt <john.cupitt@ng-london.org.uk> 7.10.8
- updated for 7.10.8
- now updated from configure
- implicit deps and files

* Wed Jul 16 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.10
- updated for 7.8.10
- updated %%files
- copies formatted docs to install area

* Wed Mar 12 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.8
- updated for 7.8.8, adding libdrfftw

* Mon Feb 3 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.7-2
- hack to change default install prefix to /usr/local

* Thu Jan 30 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.7-1
- first stab at an rpm package for vips
