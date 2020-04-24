Summary: A free and portable font rendering engine
Name: freetype
Version: 2.8
Release: 14%{?dist}
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
Group: System Environment/Libraries
URL: http://www.freetype.org
Source:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
Source3: ftconfig.h

Patch0:  freetype-2.3.0-enable-spr.patch

# Enable otvalid and gxvalid modules
Patch1:  freetype-2.2.1-enable-valid.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1197740
Patch2:  freetype-2.4.11-inode-overflow.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1381678
Patch3:  freetype-2.4.11-signed.patch

# Enable additional demos
Patch4:  freetype-2.3.11-more-demos.patch

Patch5:  freetype-2.4.11-libtool.patch

Patch6:  freetype-2.8-pcf-encoding.patch

Patch7:  freetype-2.8-loop-counter.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1497443
Patch8:  freetype-multilib.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1544775
Patch9:  freetype-2.8-getvariation.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1576504
Patch10:  freetype-2.8-2.4.11-API.patch
Patch11:  freetype-2.8-avar-table-load.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1657479
Patch12:  freetype-2.8-bw-rendering.patch
Patch13:  freetype-2.8-bw-hinting.patch

BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel

Provides: %{name}-bytecode
Provides: %{name}-subpixel

Prefix: %{_prefix}

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%prep
%setup -q -b 1 -a 2

%patch0  -p1 -b .enable-spr

%patch1  -p1 -b .enable-valid
%patch2  -p1 -b .inode-overflow
%patch3  -p1 -b .signed

pushd ft2demos-%{version}
%patch4  -p1 -b .more-demos
popd

%patch5 -p1 -b .libtool
%patch6 -p1 -b .pcf-encoding
%patch7 -p1 -b .loop-counter
%patch8 -p1 -b .multilib
%patch9 -p1 -b .getvariation
%patch10 -p1 -b .2.4.11-api
%patch11 -p1 -b .avar-table-load
%patch12 -p1 -b .bw-rendering
%patch13 -p1 -b .bw-hinting

%build

%configure --disable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --with-harfbuzz=no \
           CFLAGS="%optflags -D_FILE_OFFSET_BITS=64"

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
make %{?_smp_mflags}


%install
%make_install

%files
%license docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%{_libdir}/libfreetype.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_bindir}/freetype-config
%exclude %{_datadir}/aclocal


%changelog
* Thu Apr 23 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Mar 11 2019 Marek Kasik <mkasik@redhat.com> - 2.8-14
- Fix rendering in monochrome mode
- Resolves: #1657479

* Tue Nov 13 2018 Marek Kasik <mkasik@redhat.com> - 2.8-13
- Fix definition of constant ft_encoding_gb2312 in freetype.h
- Resolves: #1645218

* Fri Jun 08 2018 Marek Kasik <mkasik@redhat.com> - 2.8-12
- Fix loading of avar tables
- Resolves: #1576504

* Thu Jun 07 2018 Marek Kasik <mkasik@redhat.com> - 2.8-11
- Preserve API/ABI compatibility for public symbols
- Resolves: #1576504

* Wed Jun 06 2018 Richard Hughes <rhughes@redhat.com> - 2.8-10
- Update to 2.8
- Resolves: #1576504

* Mon Feb 20 2017 Marek Kasik <mkasik@redhat.com> - 2.4.11-15
- Fix shellcheck warning (coverity)
- Related: #1368141

* Mon Feb 20 2017 Marek Kasik <mkasik@redhat.com> - 2.4.11-14
- Backport functions for reading signed values from stream
- Resolves: #1381678

* Fri Feb 17 2017 Marek Kasik <mkasik@redhat.com> - 2.4.11-13
- Don't show path of non-existing libtool file
- Resolves: #1368141

* Tue Mar 22 2016 Marek Kasik <mkasik@redhat.com> - 2.4.11-12
- Define _FILE_OFFSET_BITS=64 to handle inodes higher than or equal to 2^31
- Resolves: #1303268

* Tue Mar 10 2015 Marek Kasik <mkasik@redhat.com> - 2.4.11-11
- Fixes CVE-2014-9657
   - Check minimum size of `record_size'.
- Fixes CVE-2014-9658
   - Use correct value for minimum table length test.
- Fixes CVE-2014-9675
   - New macro that checks one character more than `strncmp'.
- Fixes CVE-2014-9660
   - Check `_BDF_GLYPH_BITS'.
- Fixes CVE-2014-9661
   - Initialize `face->ttf_size'.
   - Always set `face->ttf_size' directly.
   - Exclusively use the `truetype' font driver for loading
     the font contained in the `sfnts' array.
- Fixes CVE-2014-9663
   - Fix order of validity tests.
- Fixes CVE-2014-9664
   - Add another boundary testing.
   - Fix boundary testing.
- Fixes CVE-2014-9667
   - Protect against addition overflow.
- Fixes CVE-2014-9669
   - Protect against overflow in additions and multiplications.
- Fixes CVE-2014-9670
   - Add sanity checks for row and column values.
- Fixes CVE-2014-9671
   - Check `size' and `offset' values.
- Fixes CVE-2014-9673
   - Fix integer overflow by a broken POST table in resource-fork.
- Fixes CVE-2014-9674
   - Fix integer overflow by a broken POST table in resource-fork.
   - Additional overflow check in the summation of POST fragment lengths.
- Work around behaviour of X11's `pcfWriteFont' and `pcfReadFont' functions
- Resolves: #1197740

* Mon Aug 18 2014 Peter Robinson <pbrobinson@redhat.com> - 2.4.11-10
- Generic 32/64 bit platform detection (fix ppc64le build)
- Resolves: #1126099

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.4.11-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4.11-8
- Mass rebuild 2013-12-27

* Thu Oct  3 2013 Marek Kasik <mkasik@redhat.com> - 2.4.11-7
- Fix vertical size of emboldened glyphs
- Resolves: #1010341

* Wed May 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.11-6
- Add aarch64 to 64 bit arch list

* Thu May 16 2013 Marek Kasik <mkasik@redhat.com> - 2.4.11-5
- Change encoding of "docs/tutorial/example3.cpp" to UTF-8

* Thu May 16 2013 Marek Kasik <mkasik@redhat.com> - 2.4.11-4
- Package ftconfig.h as source file

* Tue Mar 19 2013 Marek Kasik <mkasik@redhat.com> - 2.4.11-3
- Fix emboldening:
    - split out MSB function
    - fix integer overflows
    - fix broken emboldening at small sizes
- Resolves: #891457

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Marek Kasik <mkasik@redhat.com> - 2.4.11-1
- Update to 2.4.11
- Resolves: #889177

* Wed Oct 24 2012 Marek Kasik <mkasik@redhat.com> - 2.4.10-3
- Update License field

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Marek Kasik <mkasik@redhat.com> 2.4.10-1
- Update to 2.4.10
- Remove patches which are already included in upstream
- Resolves: #832651

* Fri Mar 30 2012 Marek Kasik <mkasik@redhat.com> 2.4.9-1
- Update to 2.4.9
- Fixes various CVEs
- Resolves: #806270

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Marek Kasik <mkasik@redhat.com> 2.4.8-1
- Update to 2.4.8
- Remove an unneeded patch

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7-2
- Rebuilt for glibc bug#747377

* Thu Oct 20 2011 Marek Kasik <mkasik@redhat.com> 2.4.7-1
- Update to 2.4.7
- Fixes CVE-2011-3256
- Resolves: #747262

* Thu Aug  4 2011 Marek Kasik <mkasik@redhat.com> 2.4.6-1
- Update to 2.4.6

* Wed Jul 20 2011 Marek Kasik <mkasik@redhat.com> 2.4.5-2
- Add freetype-2.4.5-CVE-2011-0226.patch
    (Add better argument check for `callothersubr'.)
    - based on patches by Werner Lemberg,
      Alexei Podtelezhnikov and Matthias Drochner
- Resolves: #723469

* Tue Jun 28 2011 Marek Kasik <mkasik@redhat.com> 2.4.5-1
- Update to 2.4.5

* Tue Mar  8 2011 Marek Kasik <mkasik@redhat.com> 2.4.4-4
- Fix autohinting fallback (#547532).
- Ignore CFF-based OTFs.

* Sun Feb 20 2011 Marek Kasik <mkasik@redhat.com> 2.4.4-3
- Enable bytecode interpreter (#547532).
- Fall back to autohinting if a TTF/OTF doesn't contain any bytecode.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Marek Kasik <mkasik@redhat.com> 2.4.4-1
- Update to 2.4.4
- Remove freetype-2.4.3-CVE-2010-3855.patch
- Resolves: #659020

* Mon Nov 15 2010 Marek Kasik <mkasik@redhat.com> 2.4.3-2
- Add freetype-2.4.3-CVE-2010-3855.patch
    (Protect against invalid `runcnt' values.)
- Resolves: #651764

* Tue Oct 26 2010 Marek Kasik <mkasik@redhat.com> 2.4.3-1
- Update to 2.4.3
- Resolves: #639906

* Wed Oct  6 2010 Marek Kasik <mkasik@redhat.com> 2.4.2-3
- Add freetype-2.4.2-CVE-2010-3311.patch
    (Don't seek behind end of stream.)
- Resolves: #638522

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> 2.4.2-2
- Fix a thinko, we still want to disable the bytecode interpreter
  by default

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> 2.4.2-1
- Update to 2.4.2
- Drop upstreamed patch, bytecode interpreter now on by default

* Thu Feb 23 2010 Behdad Esfahbod <behdad@redhat.com> 2.3.12-1
- Update to 2.3.12
- Drop mathlib patch

* Thu Dec  3 2009 Behdad Esfahbod <behdad@redhat.com> 2.3.11-2
- Drop upstreamed patch.
- Enable patented bytecode interpretter now that the patents are expired.

* Thu Oct 22 2009 Behdad Esfahbod <behdad@redhat.com> 2.3.11-1
- Update to 2.3.11.
- Add freetype-2.3.11-more-demos.patch
- New demo programs ftmemchk, ftpatchk, and fttimer

* Thu Oct 08 2009 Behdad Esfahbod <behdad@redhat.com> 2.3.10-1
- Drop freetype-2.3.9-aliasing.patch
- Update to 2.3.10.

* Thu Jul 30 2009 Behdad Esfahbod <behdad@redhat.com> 2.3.9-6
- Add freetype-2.3.9-aliasing.patch
- Resolves: 513582

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 Matthias Clasen <mclasen@redhat.com> 2.3.9-4
- Don't own /usr/lib/pkgconfig

* Wed Mar 27 2009 Behdad Esfahbod <besfahbo@redhat.com> 2.3.9-3
- Disable subpixel hinting by default.  Was turned on unintentionally.

* Wed Mar 25 2009 Behdad Esfahbod <besfahbo@redhat.com> 2.3.9-2
- Add Provides: freetype-bytecode and freetype-subpixel if built
  with those options.
- Resolves: #155210

* Thu Mar 13 2009 Behdad Esfahbod <besfahbo@redhat.com> 2.3.9-1
- Update to 2.3.9.
- Resolves #489928

* Thu Mar 09 2009 Behdad Esfahbod <besfahbo@redhat.com> 2.3.8-2.1
- Preserve timestamp of FTL.TXT when converting to UTF-8.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Behdad Esfahbod <besfahbo@redhat.com> 2.3.8-1
- Update to 2.3.8
- Remove freetype-autohinter-ligature.patch

* Tue Dec 09 2008 Behdad Esfahbod <besfahbo@redhat.com> 2.3.7-3
- Add full source URL to Source lines.
- Add docs to main and devel package.
- rpmlint is happy now.
- Resolves: #225770

* Fri Dec 05 2008 Behdad Esfahbod <besfahbo@redhat.com> 2.3.7-2
- Add freetype-autohinter-ligature.patch
- Resolves: #368561

* Tue Aug 14 2008 Behdad Esfahbod <besfahbo@redhat.com> 2.3.7-1
- Update to 2.3.7

* Tue Jun 10 2008 Behdad Esfahbod <besfahbo@redhat.com> 2.3.6-1
- Update to 2.3.6

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.5-5
- fix license tag
- add sparc64 to list of 64bit arches

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.5-4
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.3.5-3
- Rebuild for build ID

* Tue Jul 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.5-2
- Change spec file to permit enabling bytecode-interpreter and
  subpixel-rendering without editing spec file.
- Resolves: 249986

* Wed Jul 25 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.5-1
- Update to 2.3.5.
- Drop freetype-2.3.4-ttf-overflow.patch

* Fri Jun 29 2007 Adam Jackson <ajax@redhat.com> 2.3.4-4
- Fix builds/unix/libtool to not emit rpath into binaries. (#225770)

* Thu May 31 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.4-3
- Add freetype-2.3.4-ttf-overflow.patch

* Thu Apr 12 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.4-2
- Add alpha to 64-bit archs (#236166)

* Tue Apr 05 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.4-1
- Update to 2.3.4.

* Thu Apr 05 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.3-2
- Include new demos ftgrid and ftdiff in freetype-demos. (#235478)

* Thu Apr 05 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.3-1
- Update to 2.3.3.

* Fri Mar 09 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.2-1
- Update to 2.3.2.

* Fri Feb 02 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.1-1
- Update to 2.3.1.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.0-2
- Add without_subpixel_rendering.
- Drop X11_PATH=/usr.  Not needed anymore.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.0-1
- Update to 2.3.0.
- Drop upstream patches.
- Drop -fno-strict-aliasing, it should just work.
- Fix typo in ftconfig.h generation.

* Tue Jan 09 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-16
- Backport binary-search fixes from HEAD
- Add freetype-2.2.1-ttcmap.patch
- Resolves: #208734

- Fix rendering issue with some Asian fonts.
- Add freetype-2.2.1-fix-get-orientation.patch
- Resolves: #207261

- Copy non-X demos even if not compiling with_xfree86.

- Add freetype-2.2.1-zero-item-size.patch, to fix crasher.
- Resolves #214048

- Add X11_PATH=/usr to "make"s, to find modern X.
- Resolves #212199

* Mon Sep 11 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-10
- Fix crasher https://bugs.freedesktop.org/show_bug.cgi?id=6841
- Add freetype-2.2.1-memcpy-fix.patch

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-9
- Add BuildRequires: libX11-devel (#205355)

* Tue Aug 29 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-8
- Add freetype-composite.patch and freetype-more-composite.patch
  from upstream. (#131851)

* Mon Aug 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.1-7
- Require pkgconfig in the -devel package

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-6
- pass --disable-static to %%configure. (#172628)

* Thu Aug 17 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-5
- don't package static libs

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.1-4.fc6
- fix a problem with the multilib patch (#202366)

* Thu Jul 27 2006 Matthias Clasen  <mclasen@redhat.com> - 2.2.1-3
- fix multilib issues

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-2.1
- rebuild

* Fri Jul 07 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-2
- Remove unused BuildRequires

* Fri Jul 07 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-1
- Update to 2.2.1
- Remove FreeType 1, to move to extras
- Install new demos ftbench, ftchkwd, ftgamma, and ftvalid
- Enable modules gxvalid and otvalid

* Wed May 17 2006 Karsten Hopp <karsten@redhat.de> 2.1.10-6
- add buildrequires libICE-devel, libSM-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.10-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.10-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham  <notting@redhat.com> 2.1.10-5
- Remove references to obsolete /usr/X11R6 paths

* Tue Nov  1 2005 Matthias Clasen  <mclasen@redhat.com> 2.1.10-4
- Switch requires to modular X

* Fri Oct 21 2005 Matthias Clasen  <mclasen@redhat.com> 2.1.10-3
- BuildRequire gettext 

* Wed Oct 12 2005 Jason Vas Dias <jvdias@redhat.com> 2.1.10-2
- fix 'without_bytecode_interpreter 0' build: freetype-2.1.10-enable-ft2-bci.patch

* Fri Oct  7 2005 Matthias Clasen  <mclasen@redhat.com> 2.1.10-1
- Update to 2.1.10
- Add necessary fixes

* Tue Aug 16 2005 Kristian Høgsberg <krh@redhat.com> 2.1.9-4
- Fix freetype-config on 64 bit platforms.

* Thu Jul 07 2005 Karsten Hopp <karsten@redhat.de> 2.1.9-3
- BuildRequires xorg-x11-devel

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.1.9-2
- Rebuild

* Wed Aug  4 2004 Owen Taylor <otaylor@redhat.com> - 2.1.9-1
- Upgrade to 2.1.9
- Since we are just using automake for aclocal, use it unversioned,
  instead of specifying 1.4.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 Owen Taylor <otaylor@redhat.com> 2.1.7-4
- Add patch from freetype CVS to fix problem with eexec (#117743)
- Add freetype-devel to buildrequires and -devel requires
  (Maxim Dzumanenko, #111108)

* Wed Mar 10 2004 Mike A. Harris <mharris@redhat.com> 2.1.7-3
- Added -fno-strict-aliasing to CFLAGS and CXXFLAGS to try to fix SEGV and
  SIGILL crashes in mkfontscale which have been traced into freetype and seem
  to be caused by aliasing issues in freetype macros (#118021)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 2.1.7-2.1
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 2.1.7-2
- rebuilt

* Fri Jan 23 2004 Owen Taylor <otaylor@redhat.com> 2.1.7-1
- Upgrade to 2.1.7

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without the demos as that requires XFree86
  (this allows bootstrapping XFree86 on new archs)

* Fri Aug  8 2003 Elliot Lee <sopwith@redhat.com> 2.1.4-4.1
- Rebuilt

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 2.1.4-4.0
- Bump for rebuild

* Wed Jun 25 2003 Owen Taylor <otaylor@redhat.com> 2.1.4-3
- Fix crash with non-format-0 hdmx tables (found by David Woodhouse)

* Mon Jun  9 2003 Owen Taylor <otaylor@redhat.com> 2.1.4-1
- Version 2.1.4
- Relibtoolize to get deplibs right for x86_64
- Use autoconf-2.5x for freetype-1.4 to fix libtool-1.5 compat problem (#91781)
- Relativize absolute symlinks to fix the -debuginfo package 
  (#83521, Mike Harris)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 2.1.3-9
- fix build with gcc 3.3

* Tue Feb 25 2003 Owen Taylor <otaylor@redhat.com>
- Add a memleak fix for the gzip backend from Federic Crozat

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 2.1.3-7
- Run libtoolize/aclocal/autoconf so that libtool knows to generate shared libraries 
  on ppc64.
- Use _smp_mflags (for freetype 2.x only)

* Tue Feb  4 2003 Owen Taylor <otaylor@redhat.com>
- Switch to using %%configure (should fix #82330)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan  6 2003 Owen Taylor <otaylor@redhat.com> 2.1.3-4
- Make FreeType robust against corrupt fonts with recursive composite 
  glyphs (#74782, James Antill)

* Thu Jan  2 2003 Owen Taylor <otaylor@redhat.com> 2.1.3-3
- Add a patch to implement FT_LOAD_TARGET_LIGHT
- Fix up freetype-1.4-libtool.patch 

* Sat Dec 12 2002 Mike A. Harris <mharris@redhat.com> 2.1.3-2
- Update to freetype 2.1.3
- Removed ttmkfdir sources and patches, as they have been moved from the
  freetype packaging to XFree86 packaging, and now to the ttmkfdir package
- Removed patches that are now included in 2.1.3:
  freetype-2.1.1-primaryhints.patch, freetype-2.1.2-slighthint.patch,
  freetype-2.1.2-bluefuzz.patch, freetype-2.1.2-stdw.patch,
  freetype-2.1.2-transform.patch, freetype-2.1.2-autohint.patch,
  freetype-2.1.2-leftright.patch
- Conditionalized inclusion of freetype 1.4 library.

* Wed Dec 04 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- disable perl, it is not used at all

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com> 2.1.2-11
- Instead of removing unpackaged file, include it in the package.

* Sat Nov 30 2002 Mike A. Harris <mharris@redhat.com> 2.1.2-10
- Attempted to fix lib64 issue in freetype-demos build with X11_LINKLIBS
- Cleaned up various _foodir macros throughtout specfile
- Removed with_ttmkfdir build option as it is way obsolete

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2.1.2-8
- remove unpackaged files from the buildroot

* Wed Aug 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix a bug with PCF metrics

* Fri Aug  9 2002 Owen Taylor <otaylor@redhat.com>
- Backport autohinter improvements from CVS

* Tue Jul 23 2002 Owen Taylor <otaylor@redhat.com>
- Fix from CVS for transformations (#68964)

* Tue Jul  9 2002 Owen Taylor <otaylor@redhat.com>
- Add another bugfix for the postscript hinter

* Mon Jul  8 2002 Owen Taylor <otaylor@redhat.com>
- Add support for BlueFuzz private dict value, fixing rendering 
  glitch for Luxi Mono.

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- Add an experimental FT_Set_Hint_Flags() call

* Mon Jul  1 2002 Owen Taylor <otaylor@redhat.com>
- Update to 2.1.2
- Add a patch fixing freetype PS hinter bug

* Fri Jun 21 2002 Mike A. Harris <mharris@redhat.com> 2.1.1-2
- Added ft rpm build time conditionalizations upon user requests

* Tue Jun 11 2002 Owen Taylor <otaylor@redhat.com> 2.1.1-1
- Version 2.1.1

* Mon Jun 10 2002 Owen Taylor <otaylor@redhat.com>
- Add a fix for PCF character maps

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Mike A. Harris <mharris@redhat.com> 2.1.0-2
- Updated freetype to version 2.1.0
- Added libtool fix for freetype 1.4 (#64631)

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.9-2
- use "libtool install" instead of "install" to install some binaries (#62005)

* Mon Mar 11 2002 Mike A. Harris <mharris@redhat.com> 2.0.9-1
- Updated to freetype 2.0.9

* Sun Feb 24 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-4
- Added proper docs+demos source for 2.0.8.

* Sat Feb 23 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-3
- Added compat patch so 2.x works more like 1.x
- Rebuilt with new build toolchain

* Fri Feb 22 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-2
- Updated to freetype 2.0.8, however docs and demos are stuck at 2.0.7
  on the freetype website.  Munged specfile to deal with the problem by using
  {oldversion} instead of version where appropriate.  <sigh>

* Sat Feb  2 2002 Tim Powers <timp@redhat.com> 2.0.6-3
- bumping release so that we don't collide with another build of
  freetype, make sure to change the release requirement in the XFree86
  package

* Fri Feb  1 2002 Mike A. Harris <mharris@redhat.com> 2.0.6-2
- Made ttmkfdir inclusion conditional, and set up a define to include
  ttmkfdir in RHL 7.x builds, since ttmkfdir is now moving to the new
  XFree86-font-utils package.

* Wed Jan 16 2002 Mike A. Harris <mharris@redhat.com> 2.0.6-1
- Updated freetype to version 2.0.6

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.0.5-4
- automated rebuild

* Fri Nov 30 2001 Elliot Lee <sopwith@redhat.com> 2.0.5-3
- Fix bug #56901 (ttmkfdir needed to list Unicode encoding when generating
  font list). (ttmkfdir-iso10646.patch)
- Use _smp_mflags macro everywhere relevant. (freetype-pre1.4-make.patch)
- Undo fix for #24253, assume compiler was fixed.

* Mon Nov 12 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.5-2
- Fix build with gcc 3.1 (#56079)

* Sun Nov 11 2001 Mike A. Harris <mharris@redhat.com> 2.0.5-1
- Updated freetype to version 2.0.5

* Sat Sep 22 2001 Mike A. Harris <mharris@redhat.com> 2.0.4-2
- Added new subpackage freetype-demos, added demos to build
- Disabled ftdump, ftlint in utils package favoring the newer utils in
  demos package.

* Tue Sep 11 2001 Mike A. Harris <mharris@redhat.com> 2.0.4-1
- Updated source to 2.0.4
- Added freetype demo's back into src.rpm, but not building yet.

* Wed Aug 15 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-7
- Changed package to use {findlang} macro to fix bug (#50676)

* Sun Jul 15 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-6
- Changed freetype-devel to group Development/Libraries (#47625)

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.3-5
- Fix up FT1 headers to please Qt 3.0.0 beta 2

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.3-4
- Add ft2build.h to -devel package, since it's included by all other
  freetype headers, the package is useless without it

* Thu Jun 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.3-3
- Change "Requires: freetype = name/ver" to "freetype = version/release",
  and move the requirements to the subpackages.

* Mon Jun 18 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-2
- Added "Requires: freetype = name/ver"

* Tue Jun 12 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-1
- Updated to Freetype 2.0.3, minor specfile tweaks.
- Freetype2 docs are is in a separate tarball now. Integrated it.
- Built in new environment.

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Sat Jan 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Build ttmkfdir with -O0, workaround for Bug #24253

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- libtool is used to build libttf, so use libtool to link ttmkfdir with it
- fixup a paths for a couple of missing docs

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update ttmkfdir

* Wed Dec 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 2.0.1 and 1.4
- Mark locale files as such

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- move .la file to devel pkg
- FHS paths

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- revert spaces patch, fix up some foundry names to match X ones

* Mon Feb 07 2000 Nalin Dahyabhai <nalin@redhat.com>
- add defattr, ftmetric, ftsbit, ftstrtto per bug #9174

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- make ttmkfdir replace spaces in family names with underscores (#7613)

* Tue Jan 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.1
- handle RPM_OPT_FLAGS

* Wed Nov 10 1999 Preston Brown <pbrown@redhat.com>
- fix a path for ttmkfdir Makefile

* Thu Aug 19 1999 Preston Brown <pbrown@redhat.com>
- newer ttmkfdir that works better, moved ttmkfdir to /usr/bin from /usr/sbin
- freetype utilities moved to subpkg, X dependency removed from main pkg
- libttf.so symlink moved to devel pkg

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- fixed the doc file list

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb 15 1999 Preston Brown <pbrown@redhat.com>
- added ttmkfdir

* Tue Feb 02 1999 Preston Brown <pbrown@redhat.com>
- update to 1.2

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to sanitize config.sub and get ARM support
- dispoze of the patch (not necessary anymore)

* Wed Oct 21 1998 Preston Brown <pbrown@redhat.com>
- post/postun sections for ldconfig action.

* Tue Oct 20 1998 Preston Brown <pbrown@redhat.com>
- initial RPM, includes normal and development packages.
