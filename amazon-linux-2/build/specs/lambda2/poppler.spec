Summary: PDF rendering library
Name:    poppler
Version: 0.26.5
Release: 43%{?dist}
License: (GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
Group:   Development/Libraries
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1164389
Patch0: poppler-0.26.2-pdfdetach.patch

Patch1: poppler-0.26.2-fofitype1.patch
Patch2: poppler-0.26.2-pdfdoc-getpage.patch
Patch3: poppler-0.26.2-xref-getentry.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1167020
Patch4: poppler-0.26.2-invalid-matrix.patch

Patch5: poppler-0.26.5-pdfseparate.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1053616
Patch6: poppler-0.22.5-rotated-words-selection.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1174537
Patch7: poppler-0.26.5-soname-bump.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1241488
Patch8: poppler-0.26.5-pfb-headers.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299503
Patch9: poppler-0.26.5-fix-creating-poppleraction.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299500
Patch10: poppler-0.26.5-do-not-assert-broken-document.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299496
Patch11: poppler-0.26.5-check-for-int-overflow.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299490
Patch12: poppler-0.26.5-check-GfxSeparationColorSpace-existance.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299481
Patch13: poppler-0.26.5-move-array-reallocation.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299479
Patch14: poppler-0.26.5-check-groupColorSpaceStack-existance.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1298616
Patch15: poppler-0.26.5-show-some-non-ASCII-characters.patch
Patch16: poppler-0.26.5-find-correct-glyph.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299506
Patch17: poppler-0.26.5-check-array-length.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1299492
Patch18: poppler-0.26.5-fix-splash.patch

Patch19: CVE-2017-9776.patch
Patch20: CVE-2017-9775-1.patch
Patch21: CVE-2017-9775-2.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1588610
Patch22: poppler-0.26.5-annotink.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1579180
Patch23: poppler-0.26.5-infinite-recursion.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1602838
Patch24: poppler-0.26.5-negative-object-number.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1626618
# https://bugzilla.redhat.com/show_bug.cgi?id=1665266
Patch25: poppler-0.26.5-cycles-in-pdf-parsing.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1649457
Patch26: poppler-0.26.5-embedded-file-check.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1649435
Patch27: poppler-0.26.5-stream-check.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1649440
Patch28: poppler-0.26.5-valid-embedded-file.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1649450
Patch29: poppler-0.26.5-valid-embedded-file-name.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1639595
Patch30: poppler-0.26.5-add-font-substitute-name-to-qt-bindings.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1672419
Patch31: poppler-0.26.5-dummy-xref-entry.patch
Patch32: poppler-0.26.5-negative-xref-indices.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1665263
Patch33:  poppler-0.26.5-filespec.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1665273
Patch34:  poppler-0.26.5-pdfunite-missing-pages.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1646546
Patch35:  poppler-0.26.5-display-profile.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1683632
Patch36:  poppler-0.26.5-image-stream-getline.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1636103
Patch37: poppler-0.26.5-color-space.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1658304
Patch38: poppler-0.26.5-glib-print-scaling.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1378961
Patch39: poppler-0.26.5-tiling-patterns.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1686802
Patch40: poppler-0.26.5-coverage-values.patch
Patch41: poppler-0.26.5-rescale-filter.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1696636
Patch42: poppler-0.26.5-PSOutputDev-rgb.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1713582
Patch43:  poppler-0.26.5-jpeg2000-component-size.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1732340
Patch44: poppler-0.26.5-JPXStream-length.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1753850
Patch45: poppler-0.26.5-parser-integer-overflow.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1797453
Patch46: poppler-0.26.5-tilingpatternfill-crash.patch

Requires: poppler-data >= 0.4.0
BuildRequires: automake libtool
BuildRequires: gettext-devel
BuildRequires: libjpeg-devel
BuildRequires: openjpeg-devel >= 1.3-5
BuildRequires: pkgconfig(cairo) >= 1.10.0
BuildRequires: pkgconfig(gobject-introspection-1.0) 
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(QtGui) pkgconfig(QtXml)
BuildRequires: pkgconfig(libtiff-4)

Prefix: %{_prefix}


%description
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

%package glib
Summary: Glib wrapper for poppler
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description glib
%{summary}.


%package cpp
Summary: Pure C++ wrapper for poppler
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description cpp
%{summary}.

%package utils
Summary: Command line utilities for converting PDF files
Group: Applications/Text
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} < 11 && 0%{?rhel} < 6
#  last seen in fc8
Provides: pdftohtml = 0.36-11
Obsoletes: pdftohtml < 0.36-11
#  last seen in fc7
Provides: xpdf-utils = 1:3.01-27
Obsoletes: xpdf-utils < 1:3.01-27
# even earlier?
Conflicts: xpdf <= 1:3.01-8
%endif
Prefix: %{_prefix}

%description utils
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

This utils package installs a number of command line tools for
converting PDF files to a number of other formats.

%prep
%setup -q
%patch0 -p1 -b .pdfdetach
%patch1 -p1 -b .fofitype1
%patch2 -p1 -b .pdfdoc-getpage
%patch3 -p1 -b .xref-getentry
%patch4 -p1 -b .invalid-matrix
%patch5 -p1 -b .pdfseparate
%patch6 -p1 -b .rotated-word-selection
%patch7 -p1 -b .soname-bump
%patch8 -p1 -b .pfb-headers
%patch9 -p1 -b .fix-creating-poppleraction
%patch10 -p1 -b .do-not-assert-broken-document
%patch11 -p1 -b .check-for-int-overflow
%patch12 -p1 -b .check-GfxSeparationColorSpace-existance
%patch13 -p1 -b .move-array-reallocation
%patch14 -p1 -b .check-groupColorSpaceStack-existance
%patch15 -p1 -b .show-some-non-ASCII-characters
%patch16 -p1 -b .find-correct-glyph
%patch17 -p1 -b .check-array-length
%patch18 -p1 -b .fix-splash
%patch19 -p1 -b .CVE-2017-9776
%patch20 -p1 -b .CVE-2017-9775-1
%patch21 -p1 -b .CVE-2017-9775-1
%patch22 -p1 -b .annotink
%patch23 -p1 -b .infinite-recursion
%patch24 -p1 -b .negative-object-number
%patch25 -p1 -b .cycles-in-pdf-parsing
%patch26 -p1 -b .embedded-file-check
%patch27 -p1 -b .stream-check
%patch28 -p1 -b .valid-embedded-file
%patch29 -p1 -b .valid-embedded-file-name
%patch30 -p1 -b .add-font-substitute-name-to-qt-bindings
%patch31 -p1 -b .dummy-xref-entry
%patch32 -p1 -b .negative-xref-indices
%patch33 -p1 -b .filespec
%patch34 -p1 -b .pdfunite-missing-pages
%patch35 -p1 -b .display-profile
%patch36 -p1 -b .image-getstream-getline
%patch37 -p1 -b .color-space
%patch38 -p1 -b .glib-print-scaling
%patch39 -p1 -b .tiling-pattern
%patch40 -p1 -b .coverage-values
%patch41 -p1 -b .rescale-filter
%patch42 -p1 -b .psoutputdev-rgb
%patch43 -p1 -b .jpeg2000-component-size
%patch44 -p1 -b .jpxstream-length
%patch45 -p1 -b .parser-integer-overflow
%patch46 -p1 -b .divide-by-zero

# hammer to nuke rpaths, recheck on new releases
autoreconf -i -f


%build

# Hack around borkage, http://cgit.freedesktop.org/poppler/poppler/commit/configure.ac?id=9250449aaa279840d789b3a7cef75d06a0fd88e7
PATH=%{_qt4_bindir}:$PATH; export PATH

%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-cairo-output \
  --enable-libjpeg \
  --enable-libopenjpeg \
  --disable-poppler-qt4 \
  --disable-poppler-qt5 \
  --disable-xpdf-headers \
  --disable-zlib \
  --disable-introspection

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libpoppler.so.46*

%files glib
%defattr(-,root,root,-)
%{_libdir}/libpoppler-glib.so.18*

%files cpp
%defattr(-,root,root,-)
%{_libdir}/libpoppler-cpp.so.10*

%files utils
%defattr(-,root,root,-)
%{_bindir}/pdf*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/girepository-1.0
%exclude %{_bindir}/poppler-glib-demo
%exclude %{_datadir}


%changelog
* Thu Oct 29 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Apr 15 2020 Marek Kasik <mkasik@redhat.com> - 0.26.5-43
- Fix crash on broken file in tilingPatternFill()
- Resolves: #1801340

* Fri Nov 15 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-42
- Fix potential integer overflow and check length for negative values
- Resolves: #1757283

* Tue Aug 13 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-41
- Ignore dict Length if it is broken
- Resolves: #1733026

* Tue Aug 13 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-40
- Fail gracefully if not all components of JPEG2000Stream
- have the same size
- Resolves: #1723504

* Tue Aug 13 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-39
- Check whether input is RGB in PSOutputDev::checkPageSlice()
- Resolves: #1697575

* Fri Mar 29 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-38
- Constrain number of cycles in rescale filter
- Compute correct coverage values for box filter
- Resolves: #1688417

* Wed Mar 20 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-37
- Fix tiling patterns when pattern cell is too far
- Resolves: #1378961

* Mon Mar 18 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-36
- Fix version from which PrintScaling is available
- Resolves: #1658304

* Mon Mar 18 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-35
- Export PrintScaling viewer preference in glib frontend
- Related: #1658304

* Fri Mar 15 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-34
- Fix a memory leak detected by Coverity Scan
- Related: #1636103

* Wed Mar 13 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-33
- Only embed mime data for gray/rgb/cmyk colorspaces
- if image decode map is identity
- Resolves: #1636103

* Fri Mar 8 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-32
- Fix possible crash on broken files in ImageStream::getLine()
- Resolves: #1685267

* Fri Mar 8 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-31
- Avoid global display profile state becoming an uncontrolled
- memory leak
- Resolves: #1648860

* Fri Feb 22 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-30
- Check for missing pages in documents passed to pdfunite
- Resolves: #1677348

* Fri Feb 22 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-29
- Don't reuse "entry" in Parser::makeStream
- Resolves: #1677058

* Fri Feb 22 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-28
- Move the fileSpec.dictLookup call inside fileSpec.isDict if
- Resolves: #1677029

* Fri Feb 22 2019 Marek Kasik <mkasik@redhat.com> - 0.26.5-27
- Defend against requests for negative XRef indices
- Resolves: #1673700

* Tue Jan 15 2019 Jan Grulich <jgrulich@redhat.com> - 0.26.5-26
- Add font substituteName() getter to Qt bindings
- Resolves: bz#1639595

* Wed Nov 21 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-25
- Check for valid file name of embedded file
- Resolves: #1651307

* Wed Nov 21 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-24
- Check for valid embedded file before trying to save it
- Resolves: #1651306

* Wed Nov 21 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-23
- Check for stream before calling stream methods
- when saving an embedded file
- Resolves: #1651305

* Wed Nov 21 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-22
- Fix crash on missing embedded file
- Resolves: #1651309

* Tue Nov 13 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-21
- Avoid cycles in PDF parsing
- Resolves: #1640295

* Mon Jul 30 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-20
- Fix crash when Object has negative number (CVE-2018-13988)
- Resolves: #1609036

* Thu Jun 21 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-19
- Fix infinite recursion on malformed documents (CVE-2017-18267)
- Resolves: #1579180

* Thu Jun 21 2018 Marek Kasik <mkasik@redhat.com> - 0.26.5-18
- Fix crash inn AnnotInk::draw() (CVE-2018-10768)
- Resolves: #1588610

* Thu Aug 18 2016 Caolán McNamara <caolanm@redhat.com> - 0.26.5-17
- Resolves:rhbz#1482935 CVE-2017-9776

* Wed Mar  9 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-16
- Fix crash in Splash
- Resolves: #1299492

* Wed Mar  9 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-15
- Check array length
- Resolves: #1299506

* Tue Mar  8 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-14
- Show correct glyph or none instead of 'fi'
- Resolves: #1298616

* Tue Mar  8 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-13
- Check for groupColorSpace existance
- Resolves: #1299479

* Tue Mar  8 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-12
- Move array reallocation from visitLine to startLine
- Resolves: #1299481

* Mon Mar  7 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-11
- Repair patch
- Resolves: #1299490

* Mon Mar  7 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-10
- Check for GfxSeparationColorSpace existance
- Resolves: #1299490

* Mon Mar  7 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-9
- Check for int overflow
- Resolves: #1299496

* Wed Mar  2 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-8
- Do not assert on broken document
- Resolves: #1299500

* Tue Mar  1 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-7
- Add missing patch
- Resolves: #1299503

* Tue Mar  1 2016 Martin Hatina <mhatina@redhat.com> - 0.26.5-6
- Fix segfault when creating PopplerAction
- Resolves: #1299503

* Thu Jul  9 2015 Marek Kasik <mkasik@redhat.com> - 0.26.5-5
- Remove PFB headers from embedded Type1 fonts
- before embedding them into a PostScript file.
- Resolves: #1241488

* Fri Apr 24 2015 Marek Kasik <mkasik@redhat.com> - 0.26.5-4
- Bump sonames of all frontends so that they loads symbols
- from correct libpoppler.so.* when the compat-poppler022
- package is installed.
- Resolves: #1174537

* Wed Apr  8 2015 Marek Kasik <mkasik@redhat.com> - 0.26.5-3
- Add missing patch
- Resolves: #1174537

* Thu Mar 26 2015 Marek Kasik <mkasik@redhat.com> - 0.26.5-2
- Initialize x1 and y1 in TextSelectionPainter::visitLine()
- Resolves: #1174537

* Wed Mar 25 2015 Marek Kasik <mkasik@redhat.com> - 0.26.5-1
- Update to 0.26.5
- Remove unused patches
- Rereview patches from fedora
- Modify RHEL patches so that they apply
- Disable Qt5 explicitly
- Resolves: #1174537

* Thu Mar 19 2015 Richard Hughes <rhughes@redhat.com> - 0.26.2-1
- Update to 0.26.2
- Resolves: #1174537

* Fri Feb 14 2014 Marek Kasik <mkasik@redhat.com> - 0.22.5-6
- Add explicit requirement of poppler to poppler-demos (RPMDiff)
- Related: #1053616

* Fri Feb 14 2014 Marek Kasik <mkasik@redhat.com> - 0.22.5-5
- Fix selection of words rotated by multiples of 90 degrees
- Resolves: #1053616

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.22.5-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.22.5-3
- Mass rebuild 2013-12-27

* Thu Oct 31 2013 Marek Kasik <mkasik@redhat.com> 0.22.5-2
- Add poppler-0.22.5-CVE-2013-4473.patch
    (Limit length of output to pathName buffer)
- Add poppler-0.22.5-CVE-2013-4474.patch
    (Check file pattern)
- Resolves: #1025160

* Mon Jun 24 2013 Marek Kasik <mkasik@redhat.com> 0.22.5-1
- Update to 0.22.5

* Thu Jun 20 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-5
- Switch from LCMS to LCMS2
- Resolves: #975465

* Wed Jun  5 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-4
- Fix changelog dates

* Fri Apr 12 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-3
- Enable generating of TIFF files by pdftoppm

* Thu Apr 11 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-2
- Fix man pages of pdftops and pdfseparate

* Wed Feb 27 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-1
- Update to 0.22.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> 0.22.0-2
- -demos: omit extraneous (and broken) dep

* Fri Jan 18 2013 Marek Kasik <mkasik@redhat.com> 0.22.0-1
- Update to 0.22.0

* Tue Nov 13 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-9
- Move poppler-glib-demo to new sub-package demos
- Resolves: #872338

* Mon Nov 12 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-8
- Add references to corresponding bugs for poppler-0.20.3-5.patch

* Tue Nov  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-7
- Add missing hunk to patch poppler-0.20.3-5.patch

* Tue Nov  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-6
- Backport most of the changes from poppler-0.20.3 - poppler-0.20.5
-   (those which doesn't change API or ABI and are important)
- See poppler-0.20.3-5.patch for detailed list of included commits

* Wed Oct 31 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-5
- Remove unused patch

* Wed Oct 31 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-4
- Update License field

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-3
- Fix conversion to ps when having multiple strips

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-2
- Make sure xScale and yScale are always initialized
- Resolves: #840515

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-1
- Update to 0.20.2

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.1-3
- Try empty string instead of NULL as password if needed
- Resolves: #845578

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> 0.20.1-1
- Update to 0.20.1

* Mon Jun 25 2012 Nils Philippsen <nils@redhat.com>
- license is "GPLv2 or GPLv3" from poppler-0.20.0 on (based off xpdf-3.03)

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> 0.20.0-1
- Update to 0.20.0

* Fri May  4 2012 Marek Kasik <mkasik@redhat.com> 0.18.4-3
- Backport of a patch which sets mask matrix before drawing an image with a mask
- Resolves: #817378

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-2
- Rebuilt for c++ ABI breakage

* Sat Feb 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.4-1
- 0.18.4

* Thu Feb 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.3-3
- rebuild (openjpeg)

* Tue Jan 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.3-2
- -devel: don't own all headers

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.3-1
- 0.18.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Marek Kasik <mkasik@redhat.com> - 0.18.2-1
- Update to 0.18.2
- Remove upstreamed patches

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 0.18.1-3
- Rebuild for new libpng

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 0.18.1-2
- poppler-glib.pc pkgconfig file broken (#749898)
- %%check: verify pkgconfig sanity

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 0.18.1-1
- Update to 0.18.1
- pkgconfig-style deps
- tighten deps with %%_isa

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 0.18.0-2
- rebuild 

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 0.18.0-1
- Update to 0.18.0

* Mon Sep 26 2011 Marek Kasik <mkasik@redhat.com> - 0.17.3-2
- Don't include pdfextract and pdfmerge in resulting packages for now
- since they conflict with packages pdfmerge and mupdf (#740906)

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 0.17.3-1
- Update to 0.17.3

* Wed Aug 17 2011 Marek Kasik <mkasik@redhat.com> - 0.17.0-2
- Fix a problem with freeing of memory in PreScanOutputDev (#730941)

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 0.17.0-1
- Update to 0.17.0

* Thu Jun 30 2011 Rex Dieter <rdieter@fedoraproject.org> 0.16.7-1
- 0.16.7

* Wed Jun 22 2011 Marek Kasik <mkasik@redhat.com> - 0.16.6-2
- Drop dependency on gtk-doc (#604412)

* Thu Jun  2 2011 Marek Kasik <mkasik@redhat.com> - 0.16.6-1
- Update to 0.16.6

* Thu May  5 2011 Marek Kasik <mkasik@redhat.com> - 0.16.5-1
- Update to 0.16.5

* Thu Mar 31 2011 Marek Kasik <mkasik@redhat.com> - 0.16.4-1
- Update to 0.16.4

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.16.3-2
- Update to 0.16.3

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.16.3-1
- Update to 0.16.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Marek Kasik <mkasik@redhat.com> - 0.16.2-1
- Update to 0.16.2

* Tue Jan 18 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-3
- drop qt3 bindings
- rename -qt4 -> -qt

* Wed Jan 12 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-2
- rebuild (openjpeg)

* Mon Dec 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-1
- 0.16.0

* Fri Dec 10 2010 Marek Kasik <mkasik@redhat.com> - 0.15.3-1
- Update to 0.15.3

* Mon Nov  1 2010 Marek Kasik <mkasik@redhat.com> - 0.15.1-1
- Update to 0.15.1
- Remove CVE-2010-3702, 3703 and 3704 patches (they are already in 0.15.1)

* Thu Oct  7 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-5
- Add poppler-0.15.0-CVE-2010-3702.patch
    (Properly initialize parser)
- Add poppler-0.15.0-CVE-2010-3703.patch
    (Properly initialize stack)
- Add poppler-0.15.0-CVE-2010-3704.patch
    (Fix crash in broken pdf (code < 0))
- Resolves: #639861

* Wed Sep 29 2010 jkeating - 0.15.0-4
- Rebuilt for gcc bug 634757

* Mon Sep 27 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-3
- Remove explicit requirement of gobject-introspection

* Fri Sep 24 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-2
- Move requirement of gobject-introspection to glib sub-package

* Fri Sep 24 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-1
- Update to 0.15.0
- Enable introspection

* Sat Sep 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.14.3-1
- Update to 0.14.3

* Thu Aug 19 2010 Marek Kasik <mkasik@redhat.com> - 0.14.2-1
- Update to 0.14.2
- Remove poppler-0.12.1-objstream.patch

* Fri Jul 16 2010 Marek Kasik <mkasik@redhat.com> - 0.14.1-1
- Update to 0.14.1
- Don't apply poppler-0.12.1-objstream.patch, it is not needed anymore

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Wed May 26 2010 Marek Kasik <mkasik@redhat.com> - 0.13.4-1
- poppler-0.13.4

* Mon May  3 2010 Marek Kasik <mkasik@redhat.com> - 0.13.3-2
- Update "sources" file
- Add BuildRequires "gettext-devel"

* Fri Apr 30 2010 Marek Kasik <mkasik@redhat.com> - 0.13.3-1
- poppler-0.13.3

* Thu Mar  4 2010 Marek Kasik <mkasik@redhat.com> - 0.12.4-2
- Fix showing of radio buttons (#480868)

* Thu Feb 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.4-1
- popper-0.12.4

* Tue Feb 16 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-9
- Fix downscaling of rotated pages (#563353)

* Thu Jan 28 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-8
- Get current FcConfig before using it (#533992)

* Sun Jan 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-7
- use alternative/upstream downscale patch (#556549, fdo#5589)

* Wed Jan 20 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-6
- Add dependency on poppler-data (#553991)

* Tue Jan 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-5
- cairo backend, scale images correctly (#556549, fdo#5589)

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-4
- Sanitize versioned Obsoletes/Provides

* Fri Jan 15 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-3
- Correct permissions of goo/GooTimer.h
- Convert pdftohtml.1 to utf8
- Make the pdftohtml's Provides/Obsoletes versioned

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-1
- poppler-0.12.3

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.2-1
- poppler-0.12.2

* Sun Oct 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-3
- CVE-2009-3607 poppler: create_surface_from_thumbnail_data
  integer overflow (#526924)

* Mon Oct 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-1
- poppler-0.12.1
- deprecate xpdf/pdftohtml Conflicts/Obsoletes

* Wed Sep 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0

* Tue Aug 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.3-1
- Update to 0.11.3

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-2
- omit poppler-data (#507675)

* Tue Jun 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-1
- poppler-0.11.1

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-6
- reduce lib deps in qt/qt4 pkg-config support

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-5
- --enable-libjpeg
- (explicitly) --disable-zlib

* Fri Jun 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-3
- --enable-libopenjpeg, --disable-zlib

* Sun May 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-2
- update changelog
- track sonames

* Tue May 19 2009 Bastien Nocera <bnocera@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.5-1
- Update to 0.10.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.4-1
- Update to 0.10.4

* Tue Jan 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-2
- add needed scriptlets
- nuke rpaths

* Tue Jan 13 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.3-1
- Update to 0.10.3

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.2-1
- Update to 0.10.2

* Tue Nov 11 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.1-1
- Update to 0.10.1 and  -data 0.2.1

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.8.7-2
- cleanup qt3 hack
- %%description cosmetics

* Sun Sep  7 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.7-1
- Update to 0.8.7

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.6-1
- Update to 0.8.6

* Tue Aug 05 2008 Colin Walters <walters@redhat.com> - 0.8.5-1
- Update to 0.8.5

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Mon Apr 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Sun Apr 06 2008 Adam Jackson <ajax@redhat.com> 0.8.0-3
- poppler-0.8.0-ocg-crash.patch: Fix a crash when no optional content
  groups are defined.
- Mangle configure to account for the new directory for qt3 libs.
- Fix grammar in %%description.

* Tue Apr 01 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- -qt-devel: Requires: qt3-devel

* Sun Mar 30 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Sun Mar 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Wed Mar 12 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Thu Feb 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Thu Feb 21 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.4-4
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Jindrich Novy <jnovy@redhat.com> - 0.6.4-3
- apply ObjStream patch (#433090)

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.4-2
- Add some required inter-subpackge deps

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.4-1
- Update to 0.6.4
- Split off poppler-glib

* Sun Dec  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-3
- Fix the qt3 checks some more

* Wed Nov 28 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-2
- package xpdf headers in poppler-devel (Jindrich Novy)
- Fix qt3 detection (Denis Leroy)

* Thu Nov 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Thu Oct 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.6-2
- include qt4 wrapper

* Tue Sep  4 2007 Kristian Høgsberg <krh@redhat.com> - 0.6-1
- Update to 0.6

* Wed Aug 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.91-2
- Remove debug spew

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.91-1
- Update to 0.5.91

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-2
- Update the license field

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-1
- Update to 0.5.9

* Thu Mar  1 2007 Bill Nottingham <notting@redhat.com> - 0.5.4-7
- fix it so the qt pkgconfig/.so aren't in the main poppler-devel

* Fri Dec 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-5
- Include epoch in the Provides/Obsoletes for xpdf-utils

* Wed Dec 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-4
- Add Provides/Obsoletes for xpdf-utils (#219033)

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.5.4-3
- drop hard-wired: Req: gtk2
- --disable-static
- enable qt wrapper
- -devel: Requires: pkgconfig

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.5.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.4-1.fc6
- Rebase to 0.5.4, drop poppler-0.5.3-libs.patch, fixes #205813,
  #205549, #200613, #172137, #172138, #161293 and more.

* Wed Sep 13 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.3-3.fc6
- Move .so to -devel (#203637).

* Mon Aug 14 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.3-2.fc6
- link against fontconfig (see bug 202256)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.3-1.1
- rebuild

* Wed May 31 2006 Kristian Høgsberg <krh@redhat.com> 0.5.3-1
- Update to 0.5.3.

* Mon May 22 2006 Kristian Høgsberg <krh@redhat.com> 0.5.2-1
- Update to 0.5.2.

* Wed Mar  1 2006 Kristian Høgsberg <krh@redhat.com> 0.5.1-2
- Rebuild the get rid of old soname dependency.

* Tue Feb 28 2006 Kristian Høgsberg <krh@redhat.com> 0.5.1-1
- Update to version 0.5.1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 0.5.0-4
- change xpdf conflict version to be <= instead of <

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 0.5.0-3
- update conflicts: xpdf line to be versioned

* Wed Jan 11 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.0-2.0
- Update to 0.5.0 and add poppler-utils subpackage.
- Flesh out poppler-utils subpackage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Sep  4 2005 Kristian Høgsberg <krh@redhat.com> - 0.4.2-1
- Update to 0.4.2 and disable splash backend so we don't build it.

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.4.1-2
- Rebuild

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Wed Aug 17 2005 Kristian Høgsberg <krh@redhat.com> - 0.4.0-2
- Bump release and rebuild.

* Wed Aug 17 2005 Marco Pesenti gritti <mpg@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Aug 15 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.3-2
- Rebuild to pick up new cairo soname.

* Mon Jun 20 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.3-1
- Update to 0.3.3 and change to build cairo backend.

* Sun May 22 2005 Marco Pesenti gritti <mpg@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May  7 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.1
- Update to 0.3.1

* Sat Apr 23 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.0
- Update to 0.3.0

* Wed Apr 13 2005 Florian La Roche <laroche@redhat.com>
- remove empty post/postun scripts

* Wed Apr  6 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Sat Mar 12 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Use tar.gz because there are not bz of poppler

* Wed Mar  2 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.1-1
- Initial build
