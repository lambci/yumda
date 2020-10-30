Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 4.0.3
Release: 35%{?dist}

License: libtiff
Group: System Environment/Libraries
URL: http://www.remotesensing.org/libtiff/

Source: ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz

Patch0: libtiff-am-version.patch
Patch1: libtiff-CVE-2012-4447.patch
Patch2: libtiff-CVE-2012-4564.patch
Patch3: libtiff-printdir-width.patch
Patch4: libtiff-jpeg-test.patch
Patch5: libtiff-CVE-2013-1960.patch
Patch6: libtiff-CVE-2013-1961.patch
Patch7: libtiff-manpage-update.patch
Patch8: libtiff-make-check.patch
Patch9: libtiff-CVE-2013-4231.patch
Patch10: libtiff-CVE-2013-4232.patch
Patch11: libtiff-CVE-2013-4244.patch
Patch12: libtiff-CVE-2013-4243.patch
Patch13: libtiff-CVE-2014-9330.patch
Patch14: libtiff-CVE-2014-8127.patch
Patch15: libtiff-CVE-2014-8129.patch
Patch16: libtiff-CVE-2014-8130.patch
Patch17: libtiff-CVE-2014-9655.patch
Patch18: libtiff-CVE-2015-1547_8784.patch
Patch19: libtiff-CVE-2015-7554.patch
Patch20: libtiff-CVE-2015-8683_8665.patch
Patch21: libtiff-CVE-2015-8668.patch
Patch22: libtiff-CVE-2015-8781.patch
Patch23: libtiff-CVE-2016-3632.patch
Patch24: libtiff-CVE-2016-3945.patch
Patch25: libtiff-CVE-2016-3990.patch
Patch26: libtiff-CVE-2016-3991.patch
Patch27: libtiff-CVE-2016-5320.patch
Patch28: libtiff-CVE-2016-9533_9534_9536_9537.patch
Patch29: libtiff-CVE-2016-9535.patch
Patch30: libtiff-CVE-2016-9540.patch
Patch31: libtiff-CVE-2016-5652.patch
Patch32: libtiff-CVE-2015-8870.patch
Patch33: libtiff-CVE-2016-3186.patch
Patch34: libtiff-CVE-2018-7456.patch
Patch35: libtiff-CVE-2018-8905.patch
Patch36: libtiff-CVE-2018-10779.patch
Patch37: libtiff-CVE-2018-10963.patch
Patch38: libtiff-CVE-2018-12900.patch
Patch39: libtiff-CVE-2018-17100.patch
Patch40: libtiff-CVE-2018-17101.patch
Patch41: libtiff-CVE-2018-18557.patch
Patch42: libtiff-CVE-2018-18661.patch
Patch43: libtiff-coverity.patch
Patch44: libtiff-CVE-2019-14973.patch
Patch45: libtiff-CVE-2019-17546.patch

BuildRequires: zlib-devel libjpeg-devel jbigkit-devel
BuildRequires: libtool automake autoconf pkgconfig

Prefix: %{_prefix}

%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package tools
Summary: Command-line utility programs for manipulating TIFF files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description tools
This package contains command-line programs for manipulating TIFF format
image files using the libtiff library.

%prep
%setup -q -n tiff-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1

# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4

libtoolize --force  --copy
aclocal -I . -I m4
automake --add-missing --copy
autoconf
autoheader

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure --enable-ld-version-script --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

%files
%license COPYRIGHT
%{_libdir}/libtiff.so.*
%{_libdir}/libtiffxx.so.*

%files tools
%exclude %{_bindir}/tiffgt
%exclude %{_bindir}/sgi2tiff
%exclude %{_bindir}/tiffsv
%{_bindir}/*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Thu Oct 29 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Apr 06 2020 Nikola Forró <nforro@redhat.com> - 4.0.3-35
- Fix two resource leaks
  Related: #1771371

* Thu Feb 20 2020 Nikola Forró <nforro@redhat.com> - 4.0.3-34
- Fix CVE-2019-17546
  Resolves: #1771371

* Thu Feb 20 2020 Nikola Forró <nforro@redhat.com> - 4.0.3-33
- Fix CVE-2019-14973
  Resolves: #1755704

* Tue Apr 30 2019 Nikola Forró <nforro@redhat.com> - 4.0.3-32
- Fix one more Covscan defect
- Related: #1647965

* Tue Apr 30 2019 Nikola Forró <nforro@redhat.com> - 4.0.3-31
- Fix processing of RAS files without colormap 
- Related: #1647965

* Thu Dec 13 2018 Nikola Forró <nforro@redhat.com> - 4.0.3-30
- Fix various Covscan defects
- Related: #1647965

* Thu Dec 13 2018 Nikola Forró <nforro@redhat.com> - 4.0.3-29
- Fix compiler warning introduced by patch for CVE-2018-18661
- Related: #1647965

* Thu Dec 06 2018 Nikola Forró <nforro@redhat.com> - 4.0.3-28
- Fix CVE-2016-3186
- Resolves: #1319503
- Fix CVE-2018-7456
- Resolves: #1561318
- Fix CVE-2018-8905
- Resolves: #1574548
- Fix CVE-2018-10779
- Resolves: #1598503
- Fix CVE-2018-10963
- Resolves: #1598726
- Fix CVE-2018-12900
- Resolves: #1600430
- Fix CVE-2018-17100
- Resolves: #1632578
- Fix CVE-2018-17101
- Resolves: #1632579
- Fix CVE-2018-18557
- Resolves: #1647737
- Fix CVE-2018-18661
- Resolves: #1647965

* Wed Jan 18 2017 Nikola Forró <nforro@redhat.com> - 4.0.3-27
- Fix CWE-476 defect found by covscan
- Related: #1412081
 
* Wed Jan 11 2017 Nikola Forró <nforro@redhat.com> - 4.0.3-26
- Add patches for CVEs:
  CVE-2016-9533, CVE-2016-9534, CVE-2016-9535,
  CVE-2016-9536, CVE-2016-9537, CVE-2016-9540,
  CVE-2016-5652, CVE-2015-8870
- Resolves: #1412081
 
* Wed Jul 27 2016 Nikola Forró <nforro@redhat.com> - 4.0.3-25
- Add patches for CVEs:
  CVE-2015-7554, CVE-2015-8683, CVE-2015-8665,
  CVE-2015-8781, CVE-2015-8782, CVE-2015-8783,
  CVE-2015-8784
- Related: #1299921

* Tue Jul 26 2016 Nikola Forró <nforro@redhat.com> - 4.0.3-24
- Update patches for CVEs:
  CVE-2014-8127, CVE-2014-8130
- Related: #1299921

* Mon Jul 25 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-23
- Update patches:
  CVE-2014-9330, CVE-2014-8127, CVE-2014-8129
  CVE-2014-8130
- Related: #1299921

* Tue Jul 19 2016 Nikola Forró <nforro@redhat.com> - 4.0.3-22
- Update patch for CVE-2015-8668
- Related: #1299921

* Mon Jul 11 2016 Nikola Forró <nforro@redhat.com> - 4.0.3-21
- Remove patches for CVEs:
  CVE-2014-8127, CVE-2014-8129, CVE-2014-8130,
  CVE-2014-9330, CVE-2015-7554, CVE-2015-8665,
  CVE-2015-8683, CVE-2015-8781, CVE-2015-8784
- Add patches for CVEs:
  CVE-2016-3632, CVE-2016-3945, CVE-2016-3990,
  CVE-2016-3991, CVE-2016-5320
- Update patches for CVEs:
  CVE-2014-9655, CVE-2015-1547, CVE-2015-8668
- Related: #1299921

* Tue Apr 19 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-20
- CVE-2014-8127 should contain only two fixes
- Related: #1299921

* Fri Apr 01 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-19
- Revert previous patch CVE-2014-8127
- Related: #1299921

* Thu Mar 31 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-18
- Fixed wrongly applied patch CVE-2014-8127
- Related: #1299921

* Tue Mar 15 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-17
- Fixed patch CVE-2015-8668. Wrongly applied by me
- Related: #1299921

* Tue Mar 08 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-16
- Fixed patches on preview CVEs
- Related: #1299921

* Wed Feb 03 2016 Petr Hracek <phracek@redhat.com> - 4.0.3-15
- This resolves several CVEs
- CVE-2014-8127, CVE-2014-8129, CVE-2014-8130
- CVE-2014-9330, CVE-2014-9655, CVE-2015-8781
- CVE-2015-8784, CVE-2015-1547, CVE-2015-8683
- CVE-2015-8665, CVE-2015-7554, CVE-2015-8668
- Resolves: #1299921

* Thu Feb 13 2014 Petr Hracek <phracek@redhat.com> - 4.0.3-14
- Resolves: #996827 CVE-2013-4243 libtiff various flaws

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.0.3-13
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.0.3-12
- Mass rebuild 2013-12-27

* Wed Dec 18 2013 Petr Hracek <phracek@redhat.com> - 4.0.3-11
- Correct man page option -W
Resolves: #510240

* Thu Dec 12 2013 Petr Hracek <phracek@redhat.com> - 4.0.3-10
- Resolves: #996827  CVE-2013-4231 CVE-2013-4232 CVE-2013-4243 CVE-2013-4244
  libtiff various flaws

* Mon Oct 21 2013 Petr Hracek <phracek@redhat.com> - 4.0.3-9
- Resolves: #1017070 - make check moved to %check section

* Tue Oct 08 2013 Petr Hracek <phracek@redhat.com> - 4.0.3-8
- tiff2ps manual page doesn't contain help for all options
- tiffcp options differ in program help and manual page
Resolves: #510240
Resolves: #510258

* Mon Aug 12 2013 Jaromír Končický <jkoncick@redhat.com> - 4.0.3-7
- man page fixing (#510240 #510258)

* Thu May  2 2013 Tom Lane <tgl@redhat.com> 4.0.3-6
- Add upstream patches for CVE-2013-1960, CVE-2013-1961
Resolves: #958609

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 4.0.3-4
- rebuild due to "jpeg8-ABI" feature drop

* Wed Dec 19 2012 Tom Lane <tgl@redhat.com> 4.0.3-3
- Add upstream patch to avoid bogus self-test failure with libjpeg-turbo v8

* Thu Dec 13 2012 Tom Lane <tgl@redhat.com> 4.0.3-2
- Add upstream patches for CVE-2012-4447, CVE-2012-4564
  (note: CVE-2012-5581 is already fixed in 4.0.3)
Resolves: #880907

* Thu Oct  4 2012 Tom Lane <tgl@redhat.com> 4.0.3-1
- Update to libtiff 4.0.3

* Fri Aug  3 2012 Tom Lane <tgl@redhat.com> 4.0.2-6
- Remove compat subpackage; no longer needed
- Minor specfile cleanup per suggestions from Tom Callaway
Related: #845110

* Thu Aug  2 2012 Tom Lane <tgl@redhat.com> 4.0.2-5
- Add accessor functions for opaque type TIFFField (backport of not-yet-released
  upstream feature addition; needed to fix freeimage)

* Sun Jul 22 2012 Tom Lane <tgl@redhat.com> 4.0.2-4
- Add patches for CVE-2012-3401
Resolves: #841736

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Karsten Hopp <karsten@redhat.com> 4.0.2-2
- add opensuse bigendian patch to fix raw_decode self check failure on ppc*, s390*

* Thu Jun 28 2012 Tom Lane <tgl@redhat.com> 4.0.2-1
- Update to libtiff 4.0.2, includes fix for CVE-2012-2113
  (note that CVE-2012-2088 does not apply to 4.0.x)
- Update libtiff-compat to 3.9.6 and add patches to it for
  CVE-2012-2088, CVE-2012-2113
Resolves: #832866

* Fri Jun  1 2012 Tom Lane <tgl@redhat.com> 4.0.1-2
- Enable JBIG support
Resolves: #826240

* Sun May  6 2012 Tom Lane <tgl@redhat.com> 4.0.1-1
- Update to libtiff 4.0.1, adds BigTIFF support and other features;
  library soname is bumped from libtiff.so.3 to libtiff.so.5
Resolves: #782383
- Temporarily package 3.9.5 shared library (only) in libtiff-compat subpackage
  so that dependent packages won't be broken while rebuilding proceeds

* Thu Apr  5 2012 Tom Lane <tgl@redhat.com> 3.9.5-3
- Add fix for CVE-2012-1173
Resolves: #CVE-2012-1173

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 12 2011 Tom Lane <tgl@redhat.com> 3.9.5-1
- Update to libtiff 3.9.5, incorporating all our previous patches plus other
  fixes, notably the fix for CVE-2009-5022
Related: #695885

* Mon Mar 21 2011 Tom Lane <tgl@redhat.com> 3.9.4-4
- Fix incorrect fix for CVE-2011-0192
Resolves: #684007
Related: #688825
- Add fix for CVE-2011-1167
Resolves: #689574

* Wed Mar  2 2011 Tom Lane <tgl@redhat.com> 3.9.4-3
- Add patch for CVE-2011-0192
Resolves: #681672
- Fix non-security-critical potential SIGSEGV in gif2tiff
Related: #648820

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 22 2010 Tom Lane <tgl@redhat.com> 3.9.4-1
- Update to libtiff 3.9.4, for numerous bug fixes including fixes for
  CVE-2010-1411, CVE-2010-2065, CVE-2010-2067
Resolves: #554371
Related: #460653, #588784, #601274, #599576, #592361, #603024
- Add fixes for multiple SIGSEGV problems
Resolves: #583081
Related: #603081, #603699, #603703

* Tue Jan  5 2010 Tom Lane <tgl@redhat.com> 3.9.2-3
- Apply Adam Goode's fix for Warmerdam's fix
Resolves: #552360
Resolves: #533353
- Add some defenses to prevent tiffcmp from crashing on downsampled JPEG
  images; this isn't enough to make it really work correctly though
Related: #460322

* Wed Dec 16 2009 Tom Lane <tgl@redhat.com> 3.9.2-2
- Apply Warmerdam's partial fix for bug #460322 ... better than nothing.
Related: #460322

* Thu Dec  3 2009 Tom Lane <tgl@redhat.com> 3.9.2-1
- Update to libtiff 3.9.2; stop carrying a lot of old patches
Resolves: #520734
- Split command-line tools into libtiff-tools subpackage
Resolves: #515170
- Use build system's libtool instead of what package contains;
  among other cleanup this gets rid of unwanted rpath specs in executables
Related: #226049

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 3.8.2-16
- add sparc/sparc64 to multilib header support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Tom Lane <tgl@redhat.com> 3.8.2-14
- Fix buffer overrun risks caused by unchecked integer overflow (CVE-2009-2347)
Related: #510041

* Wed Jul  1 2009 Tom Lane <tgl@redhat.com> 3.8.2-13
- Fix some more LZW decoding vulnerabilities (CVE-2009-2285)
Related: #507465
- Update upstream URL

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Tom Lane <tgl@redhat.com> 3.8.2-11
- Fix LZW decoding vulnerabilities (CVE-2008-2327)
Related: #458674
- Use -fno-strict-aliasing per rpmdiff recommendation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.2-10
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Tom Lane <tgl@redhat.com> 3.8.2-9
- Update License tag
- Rebuild to fix Fedora toolchain issues

* Thu Jul 19 2007 Tom Lane <tgl@redhat.com> 3.8.2-8
- Restore static library to distribution, in a separate -static subpackage
Resolves: #219905
- Don't apply multilib header hack to unrecognized architectures
Resolves: #233091
- Remove documentation for programs we don't ship
Resolves: #205079
Related: #185145

* Tue Jan 16 2007 Tom Lane <tgl@redhat.com> 3.8.2-7
- Remove Makefiles from the shipped /usr/share/doc/html directories
Resolves: bz #222729

* Tue Sep  5 2006 Jindrich Novy <jnovy@redhat.com> - 3.8.2-6
- fix CVE-2006-2193, tiff2pdf buffer overflow (#194362)
- fix typo in man page for tiffset (#186297)
- use %%{?dist}

* Mon Jul 24 2006 Matthias Clasen <mclasen@redhat.com>
- Fix several vulnerabilities (CVE-2006-3460 CVE-2006-3461
  CVE-2006-3462 CVE-2006-3463 CVE-2006-3464 CVE-2006-3465)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.8.2-4.1
- rebuild

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-3
- Fix multilib conflict

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-3
- Fix overflows in tiffsplit

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-2
- Drop tiffgt to get rid of the libGL dependency (#190768)

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Matthias Clasen <mclasen@redhat.com> 3.7.4-3
- Don't ship static libs

* Fri Nov 11 2005 Matthias Saou <http://freshrpms.net/> 3.7.4-2
- Remove useless explicit dependencies.
- Minor spec file cleanups.
- Move make check to %%check.
- Add _smp_mflags.

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4
- Drop upstreamed patches

* Wed Jun 29 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.2-1
- Update to 3.7.2
- Drop upstreamed patches

* Fri May  6 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-6
- Fix a stack overflow

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-5
- Don't use mktemp

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-4
- Rebuild with gcc4

* Wed Jan  5 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-3
- Drop the largefile patch again
- Fix a problem with the handling of alpha channels
- Fix an integer overflow in tiffdump (#143576)

* Wed Dec 22 2004 Matthias Clasen <mclasen@redhat.com> - 3.7.1-2
- Readd the largefile patch (#143560)

* Wed Dec 22 2004 Matthias Clasen <mclasen@redhat.com> - 3.7.1-1
- Upgrade to 3.7.1
- Remove upstreamed patches
- Remove specfile cruft
- make check

* Thu Oct 14 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-7
- fix some integer and buffer overflows (#134853, #134848)

* Tue Oct 12 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-6
- fix http://bugzilla.remotesensing.org/show_bug.cgi?id=483

* Mon Sep 27 2004 Rik van Riel <riel@redhat.com> 3.6.1-4
- compile using RPM_OPT_FLAGS (bz #133650)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-2
- Fix and use the makeflags patch

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-1
- Upgrade to 3.6.1
- Adjust patches
- Don't install tiffgt man page  (#104864)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- really add symlink to shared lib by running ldconfig at compile time

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- link shared lib against -lm (Jakub Jelinek)

* Thu Sep 25 2003 Jeremy Katz <katzj@redhat.com> 3.5.7-13
- rebuild to fix gzipped file md5sum (#91281)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 3.5.7-11
- Fixed rebuild problems.

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared lib

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 3.5.7-8
- rebuild on all arches

* Mon Aug 19 2002 Phil Knirsch <pknirsch@redhat.com> 3.5.7-7
- Added LFS support (#71593)

* Tue Jun 25 2002 Phil Knirsch <pknirsch@redhat.com> 3.5.7-6
- Fixed wrong exit code of tiffcp app (#67240)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 15 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed segfault in fax2tiff tool (#64708).

* Mon Feb 25 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed problem with newer bash versions setting CDPATH (#59741)

* Tue Feb 19 2002 Phil Knirsch <pknirsch@redhat.com>
- Update to current release 3.5.7

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Aug 28 2001 Phil Knirsch <phil@redhat.de>
- Fixed ia64 problem with tiffinfo. Was general 64 bit arch problem where s390x
  and ia64 were missing (#52129).

* Tue Jun 26 2001 Philipp Knirsch <pknirsch@redhat.de>
- Hopefully final symlink fix

* Thu Jun 21 2001 Than Ngo <than@redhat.com>
- add missing libtiff symlink

* Fri Mar 16 2001 Crutcher Dunnavant <crutcher@redhat.com>
- killed tiff-to-ps.fpi filter

* Wed Feb 28 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed missing devel version dependancy.

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- rebuild

* Mon Aug  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- added a tiff-to-ps.fpi filter for printing

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply Peter Skarpetis's fix for the 32-bit conversion

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- make man pages non-executable (#12811)

* Mon Jun 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove CVS repo info from data directories

* Thu May 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix build rooting
- fix syntax error in configure script
- move man pages to {_mandir}

* Wed May 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild for an errata release

* Wed Mar 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.5.5, which integrates our fax2ps fixes and the glibc fix

* Tue Mar 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix fax2ps swapping height and width in the bounding box

* Mon Mar 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages from devel package to the regular one
- integrate Frank Warmerdam's fixed .fax handling code (keep until next release
  of libtiff)
- fix fax2ps breakage (bug #8345)

* Sat Feb 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- set MANDIR=man3 to make multifunction man pages friendlier

* Mon Jan 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix URLs

* Fri Jan 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- link shared library against libjpeg and libz

* Tue Jan 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable zip and jpeg codecs
- change defattr in normal package to 0755
- add defattr to -devel package

* Wed Dec 22 1999 Bill Nottingham <notting@redhat.com>
- update to 3.5.4

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 6)

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against fixed jpeg libs (libjpeg-6b)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- new version to replace the one from libgr
- patched for glibc
- added shlib support
