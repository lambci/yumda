%define _buildid .16

%bcond_with rsvg
%bcond_with magick_compat
%bcond_with X11
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if 0%{?fedora} || 0%{?rhel} > 6
%global _with_quantum_depth --with-quantum-depth=16
%endif

%if 0%{?fedora} || 0%{?rhel} > 5 || 0%{?amzn}
%global lcms2 --with-lcms2
%endif

%if 0%{?fedora} || 0%{?rhel} > 6
%global _enable_quantum_library_names --enable-quantum-library-names
%global libQ -Q16
%endif

%global multilib_archs x86_64 %{ix86} ppc64 ppc64le ppc s390x s390 sparc64 sparcv9
# hack for older platforms/rpm-versions that do not support %%__isa_bits (like el5)
%ifarch %{multilib_archs}
%if ! 0%{?__isa_bits:1}
%ifarch x86_64 s390x ia64 ppc64 sparc64
%global __isa_bits 64
%else
%global __isa_bits 32
%endif
%endif
%endif

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

%global __provides_exclude_from ^%{_libdir}/GraphicsMagick-%{version}/.*\\.(la|so)$

Summary: An ImageMagick fork, offering faster image generation and better quality
Name: GraphicsMagick
Version: 1.3.32
Release: 1%{?_buildid}%{?dist}

License: MIT
Source0: http://downloads.sourceforge.net/sourceforge/graphicsmagick/GraphicsMagick-%{version}.tar.xz
Source2000: magick_types.h
Url: http://www.graphicsmagick.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## downstream patches
# workaround multilib conflicts with GraphicsMagick-config
Patch100: GraphicsMagick-1.3.16-multilib.patch

## upstreamable patches
Patch50: GraphicsMagick-1.3.31-perl_linkage.patch

BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: giflib-devel
BuildRequires: jasper-devel
%if 0%{?lcms2:1}
BuildRequires: lcms2-devel
%endif
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
%if %{with rsvg}
BuildRequires: librsvg2-devel
%endif
BuildRequires: libtiff-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libwmf-devel
BuildRequires: libxml2-devel
#BuildRequires: lpr
#BuildRequires: p7zip
BuildRequires: perl-devel
#BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::MakeMaker)
%if %{with X11}
BuildRequires: xdg-utils
%endif
BuildRequires: xz-devel
BuildRequires: zlib-devel
## conditional deps
%if 0%{?fedora} || 0%{?rhel} > 6 || 0%{?amzn}
BuildRequires: jbigkit-devel
BuildRequires: libwebp-devel
%endif

# upgrade path for introduction of -doc subpkg in 1.3.19-4
Obsoletes: GraphicsMagick < 1.3.19-4

# depend on stuff referenced below
# --with-gs-font-dir=%%{_datadir}/fonts/default/Type1
Requires: urw-fonts

Prefix: %{_prefix}

%description
GraphicsMagick is a comprehensive image processing package which is initially
based on ImageMagick 5.5.2, but which has undergone significant re-work by
the GraphicsMagick Group to significantly improve the quality and performance
of the software.

%package c++
Summary: GraphicsMagick Magick++ library (C++ bindings)
Requires: %{name}%{?_isa} = %{version}-%{release}

%description c++
This package contains the GraphicsMagick++ library, a C++ binding to the 
GraphicsMagick graphics manipulation library.

Install GraphicsMagick-c++ if you want to use any applications that use 
GraphicsMagick++.

%prep
%setup -q

%patch50 -p1 -b .perl_linkage
%patch100 -p1 -b .multilib

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
%if "%{_libdir}" != "/usr/lib"
sed -i.rpath -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build

## hopefully, temporary workaround for freetype bug,
## https://bugzilla.redhat.com/show_bug.cgi?id=1651788
%if 0%{?rhel} == 7
CFLAGS="$RPM_OPT_FLAGS -DFT_ENCODING_PRC=FT_ENCODING_GB2312"
%endif

%configure --enable-shared --disable-static \
           %{?lcms2} \
           --with-magick_plus_plus \
%if %{with magick_compat}
           --enable-magick-compat \
%endif
           --with-modules \
           --without-perl \
           %{?_with_quantum_depth} \
           %{?_enable_quantum_library_names} \
           --with-threads \
           --with-wmf \
           --without-x \
           --with-xml \
           --without-dps \
           --with-gs-font-dir=%{_datadir}/fonts/default/Type1

%make_build


%install
%make_install

%files
%license Copyright.txt
%{_libdir}/libGraphicsMagick%{?libQ}.so.3*
%{_libdir}/libGraphicsMagickWand%{?libQ}.so.2*
%{_bindir}/gm
%if %{with magick_compat}
%{_bindir}/animate
%{_bindir}/compare
%{_bindir}/composite
%{_bindir}/conjure
%{_bindir}/convert
%{_bindir}/display
%{_bindir}/identify
%{_bindir}/import
%{_bindir}/mogrify
%{_bindir}/montage
%endif
%{_libdir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}
%{_mandir}/man1/gm.1.gz
%{_mandir}/man4/miff.4.gz
%{_mandir}/man5/quantize.5.gz

%files c++
%{_libdir}/libGraphicsMagick++%{?libQ}.so.12*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_docdir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_bindir}/*-config

%changelog
* Tue Oct 29 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Mon Jul 8 2019 kaos-source-imports <nobody@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.32-1.el6

* Mon Jun 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.3.32-1
- 1.3.32

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.31-6
- Perl 5.30 rebuild

* Tue Feb 19 2019 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.31-2.el6

* Fri Feb 01 2019 Caolán McNamara <caolanm@redhat.com> - 1.3.31-5
- Rebuilt for fixed libwmf soname

* Thu Jan 31 2019 Kalev Lember <klember@redhat.com> - 1.3.31-4
- Rebuilt for libwmf soname bump

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.31-2
- GraphicsMagic-perl 1.3.31 is broken (#1655294)

* Tue Nov 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.31-1
- GraphicsMasgick-1.3.31

* Mon Sep 10 2018 Trinity Quirk <tquirk@amazon.com>
- Add patch for bug #542, Improper call to JPEG library in state 201

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.30-2
- Perl 5.28 rebuild

* Sun Jul 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.30-1
- GraphicsMagick-1.3.30

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.29-2
- Perl 5.28 rebuild

* Wed May 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.29-1
- 1.3.29 (#1574031])

* Fri Mar 16 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.28-1.el6

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.28-4
- BR: gcc-c++, %%make_build %%make_install %%ldconfig_scriptlets

* Tue Mar 6 2018 Andrew Egelhofer <egelhofe@amazon.com>
- Merge branch 'epel6'

* Fri Feb 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.28-3
- use %%ldconfig_scriptlets
- s/libungif/giflib

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.28-1
- 1.3.28

* Mon Dec 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.27-1
- 1.3.27

* Sat Aug 12 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.26-3.el6

* Sat Aug 12 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.3.26-10
- Own doc dir

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.3.26-8
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-7
- 2017-11643 (#1475497)

* Thu Jul 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-6
- CVE-2017-11102 (#1473728)
- CVE-2017-11139 (#1473739)
- CVE-2017-11140 (#1473750)
- CVE-2017-11636 (#1475456)
- CVE-2017-11637 (#1475452)
- CVE-2017-11638 (#1475708)
- CVE-2017-11641 (#1475489)

* Thu Jul 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-5
- .spec cleanup, drop deprecated stuff
- update filtering
- restore %%check

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.26-1.el6

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-3
- CVE-2017-11403 (#1472214)

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.26-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-1
- 1.3.26
- CVE-2017-10794 (#1467655)
- CVE-2017-10799 (#1467372)
- CVE-2017-10800 (#1467381)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.25-7
- Perl 5.26 rebuild

* Sat Mar 18 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.25-6.el6

* Thu Mar 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.25-6
- CVE-2017-6335 (#1427975)

* Thu Mar 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.25-5
- CVE-2016-7800 (#1381148)
- CVE-2016-7996, CVE-2016-7997 (#1383223)
- CVE-2016-8682, CVE-2016-8683, CVE-2016-8684 (#1385583)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 1.3.25-3
- Rebuild (libwebp)

* Thu Dec 01 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.25-2
- Rebuild for jasper 2.0

* Sun Sep 25 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.25-1.el6

* Thu Sep 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.25-1
- 1.3.25
- -doc: fix case where %%licensedir is undefined

* Sat Jun 18 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.24-1.el6

* Mon May 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.24-1
- 1.3.24

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.23-6
- Perl 5.24 rebuild

* Wed Mar 30 2016 Praveen K Paladugu <praween@amazon.com>
- Remove unnecessary macro invocations

* Thu Mar 24 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.23-5.el6

* Fri Mar 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.23-5
- LCMS support broken in GraphicsMagick 1.3.23 (#1314898)
- simplify .spec conditionals (EOL fedora releases mostly)

* Tue Mar 1 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.23-4.el6

* Mon Feb 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.23-4
- make .spec el5/el6-compatible again

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.3.23-2
- Rebuilt for libwebp soname bump

* Sat Nov 07 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.23-1
- 1.3.23

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.22-1
- 1.3.22, filter provides

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.21-3
- Perl 5.22 rebuild

* Fri Apr 24 2015 Orion Poplawski <orion@cora.nwra.com> - 1.3.21-2
- Rebuild for gcc 5 C++11 again

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.21-1
- 1.3.21

* Wed Feb 18 2015 Orion Poplawski <orion@cora.nwra.com> - 1.3.20-5
- Rebuild for gcc 5 C++11

* Tue Sep 30 2014 Lee Trager <ltrager@amazon.com>
- Conditionalize X11 support

* Sat Sep 13 2014 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.20-3.el6

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.20-4
- Perl 5.20 rebuild

* Thu Aug 28 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.20-3
- go back to original L%02d format variant

* Mon Aug 25 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.20-2
- better fix for CVE-2014-1947 (#1064098,#1083082)

* Wed Aug 20 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.20-1
- 1.3.20, CVE-2014-1947 (#1064098,#1083082)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Orion Poplawski <orion@cora.nwra.com> - 1.3.19-8
- Rebuild for libjbig soname bump

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-6
- handle upgrade path for introduction of -doc subpkg in 1.3.19-4

* Fri Mar 14 2014 Jamie Anderson <jamieand@amazon.com>
- Use built-in SVG support instead of librsvg2 Explicitly list installed files Convert multilib magick_types.h into a SOURCE

* Mon Feb 03 2014 Remi Collet <remi@fedoraproject.org> - 1.3.19-5
- upstream patch, drop debug output (#1060665)

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.3.19-4
- Split docs into -doc subpackage, drop README.txt (#1056306).
- Drop no longer needed BrowseDelegateDefault modification.
- Convert docs to UTF-8.

* Thu Jan 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-3
- ppc64le is a multilib arch (#1051208)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-2
- BR: jbigkit, libwebp, xdg-utils, xz

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-1
- 1.3.19 (#1047676)

* Sat Nov 2 2013 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.18-2.el6

* Tue Oct 15 2013 Rex Dieter <rdieter@fedoraproject.org> 1.3.18-5
- trim changelog

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.18-3
- Perl 5.18 rebuild

* Wed Jun 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1.3.18-2
- GraphicsMagick needs to recognize aarch64 as 64bit arch (#978351)

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.3.18-1
- 1.3.18 (#920064)
- add %%rhel conditionals

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.3.17-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.3.17-2
- rebuild against new libjpeg

* Sat Nov 3 2012 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.17-1.el6

* Tue Oct 16 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.3.17-1
- GraphicsMagick-1.3.17 (#866377)
- GraphicsMagick 1.3.13 update breaks some PNGs (#788246)
- --enable-quantum-library-names on f19+

* Wed Sep 12 2012 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.16-5.el6

* Mon Aug 20 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.16-5
- CVE-2012-3438 GraphicsMagick: png_IM_malloc() size argument (#844106, #844107)

* Mon Aug 20 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.16-4
- link GraphicsMagick against lcms2 instead of lcms1 (#849778)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 1.3.16-2
- Perl 5.16 rebuild

* Sun Jun 24 2012 Rex Dieter <rdieter@fedoraproject.org>
- 1.3.16-1
- GraphicsMagick-1.3.16
- GraphicsMagick-devel and GraphicsMagick-c++-devel multilib conflict (#566361)

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.3.15-3
- Perl 5.16 rebuild

* Fri Jun 8 2012 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.14-1.el6

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.15-2
- rebuild (libtiff)

* Sat Apr 28 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.15-1
- 1.3.15

* Sun Feb 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.14-1
- 1.3.14

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-4
- -devel: omit seemingly extraneous dependencies

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-3
- BR: perl(ExtUtils::MakeMaker)

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-2
- Bad font configuration (#783906)
- re-introduce perl_linkage patch, fixes %%check

* Thu Jan 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-1
- 1.3.13

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.3.12-7
- Rebuild for new libpng

* Tue Jul 19 2011 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/GraphicsMagick-1.3.12-1.el6
- setup complete for package GraphicsMagick

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.12-6
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.12-5
- Perl 5.14 mass rebuild

* Tue Apr 26 2011 Rex Dieter <rdieter@fedoraproject.org> 1.3.12-4
- delegates.mgk could use some care (#527117)
- -perl build is bad (#527143)
- wrong default font paths (#661664)
- need for 16-bit support, f16+ for now (#699414)
- tighten subpkg deps via %%_isa

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.12-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.12-1
- GraphicsMagick-1.3.12

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.11-1
- GraphicsMagick-1.3.11

* Mon Dec 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-4
- CVE-2009-1882 (#503017)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.3.7-3
- rebuild against perl 5.10.1

* Fri Nov 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-2
- cleanup/uncruftify .spec

* Thu Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-1
- GraphicsMagick-1.3.7

* Mon Aug  3 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.3.6-2
- Use lzma-compressed upstream source tarball.

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> 1.3.6-1
- GraphicsMagick-1.3.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.5-1
- GraphicsMagick-1.3.5, ABI break (#487605)
- --without-libgs (for now, per upstream advice)
- BR: jasper-devel

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.15-1
- GraphicsMagick-1.1.15
- fix BuildRoot
- multiarch conflicts in GraphicsMagick (#341381)
- broken -L in GraphicsMagick.pc (#456466)
- %%files: track sonames

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-3
- own all files properly

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-2
- turns out we do need gcc43 patch

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-1
- update to 1.1.14
- fix perl issue (bz 454087)

* Sun Jun 01 2008 Dennis Gilmore <dennis@ausil.us> - 1.1.10-4
- sparc64 is a 64 bit arch

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-3
- Added patch to include cstring instead of string, fixing gcc4.3 build issue

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-2
- Rebuilt against gcc 4.3

* Mon Jan 28 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-1
- Upgraded to 1.1.10
- Fixed linking problem with the Perl module. #365901

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.1.8-3
- Rebuild for selinux ppc32 issue.

* Sun Jul 29 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.8-2
- Building without gslib support as it results in segfaults.

* Sat Jul 28 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.8-1
- Update to new maintainance release 1.1.8

* Wed Mar 07 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.7-7
- Fix potential CVE-2007-0770 issue.
- Added perl-devel BuildReq

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.7-6
- *really* fix magick_config-64.h (bug #217959)
- make buildable on rhel4 too.

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.7-5
- fix magick-config-64.h (bug #217959)

* Wed Nov 29 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-3
- Fixed devel requirement.

* Sun Nov 26 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-2
- Fixed various stuff

* Mon Jul 24 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-1
- Initial Package for FE based on ImageMagick.spec
