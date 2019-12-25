%global freetype_version 2.1.4

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.10.95
Release: 11%{?dist}.0.2
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
Source:		http://fontconfig.org/release/%{name}-%{version}.tar.bz2
URL:		http://fontconfig.org
Source1:	25-no-bitmap-fedora.conf
Source2:	FcStrListFirst.3

# https://bugzilla.redhat.com/show_bug.cgi?id=140335
Patch0:		fontconfig-2.8.0-sleep-less.patch
Patch1:		fontconfig-no-dir-when-no-conf.patch
Patch2:		fontconfig-fix-memleak.patch
Patch3:		fontconfig-copy-all-value.patch
Patch4:		fontconfig-fix-crash-on-fcfontsort.patch
Patch5:		fontconfig-fix-race-condition.patch
Patch6:		fontconfig-update-45-latin.patch
Patch7:		fontconfig-validate-offset-in-cache.patch
Patch8:		fontconfig-offset-in-elts.patch

# Amazon Patches
Patch100:	0001-Avoid-conflicts-with-integer-width-macros-from-TS-18.patch

BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= %{freetype_version}
BuildRequires:	fontpackages-devel

Requires:	fontpackages-filesystem
Requires(post):	grep coreutils
Requires:	font(:lang=en)

Prefix: %{_prefix}

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%prep
%setup -q
%patch0 -p1 -b .sleep-less
%patch1 -p1 -b .nodir
%patch2 -p1 -b .memleak
%patch3 -p1 -b .copy-all
%patch4 -p1 -b .fix-crash
%patch5 -p1 -b .fix-race
%patch6 -p1 -b .update-45-latin
%patch7 -p1 -b .validate-offset
%patch8 -p1 -b .offset-elts
%patch100 -p1
cp %{SOURCE2} doc/

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%configure \
  --with-default-fonts=%{_datadir}/fonts \
  --with-add-fonts=%{_prefix}/local/share/fonts \
  --disable-static \
  --disable-docs

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" V=1

install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_fontconfig_templatedir}/25-unhint-nonlatin.conf $RPM_BUILD_ROOT%{_fontconfig_confdir}/

%post
umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/root fc-cache -f
fi

%files
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-pattern
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-validate
%{_fontconfig_templatedir}/*.conf
%{_datadir}/xml/fontconfig
# fonts.conf is not supposed to be modified.
# If you want to do so, you should use local.conf instead.
%config %{_fontconfig_masterdir}/fonts.conf
%config(noreplace) %{_fontconfig_confdir}/*.conf
%dir %{_localstatedir}/cache/fontconfig

%exclude %{_includedir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_fontconfig_confdir}/README

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Feb 24 2017 Akira TAGOH <tagoh@redhat.com> - 2.10.95-11
- Add Requires: font(:lang=en) (#1403957)

* Fri Sep 23 2016 Akira TAGOH <tagoh@redhat.com> - 2.10.95-10
- Fix a regression in the previous change. (#1355930)

* Fri Aug  5 2016 Akira TAGOH <tagoh@redhat.com> - 2.10.95-9
- CVE-2016-5384: Validate offsets in cache files properly. (#1355930)

* Fri Jun 10 2016 Akira TAGOH <tagoh@redhat.com> - 2.10.95-8
- Update 45-latin.conf to add some hints to fall back for Windows fonts (#1073460)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.10.95-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.10.95-6
- Mass rebuild 2013-12-27

* Tue Oct  8 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-5
- Fix the race condition issue on updating cache (#1011510)
- Fix crash issue in FcFontSort()
- Fix an issue not copying all values from the font.

* Fri Sep 13 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-4
- Fix memory leaks in FcFreeTypeQueryFace().

* Mon Sep  2 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-3
- Do not create a directory for migration when no old config file and directory.
  (#1003495)

* Sat Aug 31 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-1
- Fix a crash issue (#1003069)

* Fri Aug 30 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.94-1
- New upstream release.
- migrate the configuration for XDG Base Directory spec automatically (#882267)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.93-1
- New upstream release.

* Thu Apr 11 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.92-3
- Fix a web font issue in firefox. (#946859)

* Mon Apr  1 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.92-2
- Fix font matching issue. (#929372)

* Fri Mar 29 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.92-1
- New upstream release.

* Tue Feb 12 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.91-3
- Improve the spec to meet the latest packaging guidelines (#225759)
  - add -devel-doc subpackage.
- Fix a build issue with automake 1.13

* Fri Feb  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.10.91-2
- Own the %%{_datadir}/xml/fontconfig dir.
- Fix bogus dates in %%changelog.

* Fri Jan 11 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.91-1
- New upstream release (#894109)
  - threadsafe
  - new tool to validate the glyph coverage
  - add new rule to scale the bitmap font.

* Mon Nov 26 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.2-1
- New upstream release.
  - Fix an regression on FcFontMatch with namelang. (#876970)

* Thu Oct 25 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.1-2
- Update License field (#869614)

* Fri Jul 27 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.1-1
- New upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.0-1
- New upstream release.

* Mon Jun 25 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.92-1
- New upstream release.

* Mon Jun 11 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.91-1
- New upstream release.
  - docs are generated with the fixed docbook (#826145)
  - handle whitespace in family name correctly (#468565, #591634)
  - Updated ne.orth. (#586763)

* Wed May 16 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.0-2
- Add grep and coreutils to Requires(post). (#821957)

* Fri Mar 23 2012 Akira TAGOH <tagoh@redhat.com>
- backport patch to make 'result' from FcFontMatch() and FcFontSort()
  more reliable.

* Wed Mar 21 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.0-1
- New upstream release (#803559)
  - Update ks.orth (#790471)
  - Add brx.orth (#790460)
  - Update ur.orth (#757985)
  - No Apple Roman cmap support anymore. should works. (#681808)
  - Update ne.orth (#586763)
  - Add a workaround for ZapfDingbats. (#562952, #497648, #468565)
- clean up the spec file.
- Add BR: fontpackages-devel.
- Add R: fontpackages-filesystem.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 31 2011 Adam Jackson <ajax@redhat.com> 2.8.0-4
- fontconfig-2.8.0-dingbats.patch: Hack for dingbats font matching. (#468565)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 24 2010 Adam Jackson <ajax@redhat.com> 2.8.0-2
- fontconfig-2.8.0-sleep-less.patch: Make a stupid sleep() in fc-cache
  slightly less stupid.

* Thu Dec  3 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Tue Sep  8 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Mon Aug 31 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Mon Jul  27 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.0
- Update to 2.7.0

* Mon Jun  1 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090601-1
- Update to 2.6.99.behdad.20090601

* Fri May  8 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090508-1
- Update to 2.6.99.behdad.20090508
- Resolves #497984

* Wed Mar 18 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090318-1
- Update to 2.6.99.behdad.20090318
- Resolves #490888

* Tue Mar 17 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090317-1
- Update to 2.6.99.behdad.20090317
- Resolves #485685

* Sat Mar 14 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad-3
- New tarball with version fixed in the header

* Fri Mar 13 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad-2
- Previous tarball was broken.  Rebuild with respinned ball.

* Fri Mar 13 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad-1
- Update to 2.6.99.behdad

* Tue Mar 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.98-1.gb39c36a
- Update to 2.6.98-1.gb39c36a

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.97-5.g945d6a4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 2.6.97-4.g945d6a4
— global-ization

* Mon Feb 16 2009 Richard Hughes <rhughes@redhat.com> - 2.6.97-3.g945d6a4
- Correct the rpm provide name to be font(), not Font().

* Sun Feb 15 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.97-2.g945d6a4
- Another try.

* Sun Feb 15 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.97-1.g945d6a4
- Update to 2.6.97-1.g945d6a4

* Sun Feb 15 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.96-1.g0b290a6
- Update to 2.6.96-1.g0b290a6

* Tue Jan 27 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.95-1.git.66.gb162bfb
- Update to 2.6.95-1.git.66.gb162bfb

* Fri Jan 23 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.94-1.git.65.g628ee83
- Update to 2.6.94-1.git.65.g628ee83

* Wed Jan 21 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.93-1.git.64.g6aa4dce
- Update to 2.6.93-1.git.64.g6aa4dce

* Mon Jan 19 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.92-1.git.64.g167bb82
- Update to 2.6.92-1.git.64.g167bb82

* Mon Jan 19 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.91-1.git.64.g9feaf34
- Update to 2.6.91-1.git.64.g9feaf34

* Fri Jan 16 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.90-3.git.63.g6bb4b9a
- Install fc-scan and fc-query

* Fri Jan 16 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.90-2.git.63.g6bb4b9a
- Update to 2.6.90-1.git.63.g6bb4b9a
- Remove upstreamed patch

* Mon Oct 20 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-3
- Add fontconfig-2.6.0-indic.patch
- Resolves: #464470

* Sun Jun 01 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-2
- Fix build.

* Sat May 31 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-1
- Update to 2.6.0.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.0-2
- Autorebuild for GCC 4.3

* Wed Nov 14 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.5.0-1
- Update to 2.5.0.

* Tue Nov 06 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.92-1
- Update to 2.4.92.
- Mark /etc/fonts/conf.d/* as config(noreplace).
- Remove most of our conf file, all upstreamed except for
  75-blacklist-fedora.conf that I'm happily dropping.  Who has
  Hershey fonts these days...
- ln upstream'ed 25-unhint-nonlatin.conf from conf.avail in conf.d
- Add 25-no-bitmap-fedora.conf which is the tiny remaining bit
  of conf that didn't end up upstream.  Can get rid of it in the
  future, but not just yet.

* Thu Oct 25 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.91-1
- Update to 2.4.91.
- Add /usr/local/share/fonts to default config. (#147004)
- Don't rebuild docs, to fix multilib conflicts. (#313011)
- Remove docbook and elinks BuildRequires and stuff as we don't
  rebuild docs.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2.4.2-5
- Rebuild for PPC toolchain bug
- Add BuildRequires: gawk

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.4.2-4
- /etc/fonts/conf.d is now owned by filesystem

* Fri May 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.4.2-3
- Add Liberation fonts to 30-aliases-fedora.conf

* Fri Jan 12 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.2-2
- Change /usr/share/X11/fonts/OTF to /usr/share/X11/fonts/TTF
- Resolves: #220809

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Wed Oct  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.4.1-4
- Fix a multilib upgrade problem (#208151)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.4.1-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.1-2
- Update 30-aliases-fedora.conf to correctly alias MS and StarOffice
  fonts. (#207460)

* Fri Sep 15 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.1-1
- Update to 2.4.1, a public API was dropped from 2.4.0
- Remove upstreamed patch

* Mon Sep 11 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.0-1
- Update to 2.4.0
- Rename/order our configuration stuff to match the new scheme.
  Breaks expected :-(

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-3
- Add missing file.  Previous update didn't go through

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-2
- Add fontconfig-2.3.97-ppc64.patch, for ppc64 arch signature

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-1
- update to 2.3.97
- Drop upstreamed patches
- Regenerate defaultconfig patch
- Don't touch stamp as it was not ever needed

* Thu Aug 17 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.95-11
- inclusion of zhong yi font and rearranged font prefer list. (bug# 201300)

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-10
- use "%%5x" instead of " %%4x" to support 64k instead of
  clamping.  Idea from Behdad.

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-9
- tweak last patch to give a more reasonable page size
  value if 64k page size is in effect.

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-8
- maybe fix buffer overflow (bug 202152).

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-7
- Update configs to provide better openoffice/staroffice
  compatibility (bug 200723)

* Thu Jul 27 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.95-6
- Do umask 0022 in post
- Update configs to reflect addition of new Indic fonts (#200381, #200397)

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-5
- Plug a small memory leak

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.95-4.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.95-4.1
- rebuild

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-4
- Fix the handling of TTF font collections

* Thu May 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-3
- Apply a patch by David Turner to speed up cache generation

* Wed Apr 26 2006 Bill Nottingham <notting@redhat.com> - 2.3.95-2
- fix fonts.conf typo

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-1
- Update to 2.3.95

* Fri Feb 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.94-1
- Update to 2.3.94

* Sat Feb 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060211-1
- Newer cvs snapshot

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.93.cvs20060208-1.1
- bump again for double-long bug on ppc(64)

* Wed Feb  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060208-1
- Newer cvs snapshot

* Tue Feb  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060207-1
- Newer cvs snapshot
- Drop upstreamed patches, pick up some new ones

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.93.cvs20060131-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Ray Strode <rstrode@redhat.com> - 2.3.93.cvs20060131-3
- Move user cache to a subdirectory (bug 160275)

* Thu Feb  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060131-2
- Accumulated patches

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060131-1
- Newer cvs snapshot

* Tue Jan 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060124-1
- Newer cvs snapshot

* Tue Jan 17 2006 Ray Strode <rstrode@redhat.com> - 2.3.93-4
- apply patch from Tim Mayberry to correct aliasing and disable
  hinting for the two Chinese font names AR PL ShanHeiSun Uni 
  and AR PL Zenkai Uni

* Tue Jan 10 2006 Bill Nottingham <notting@redhat.com> - 2.3.93-3
- prereq coreutils for mkdir/touch in %%post

* Wed Dec 21 2005 Carl Worth <cworth@redhat.com> - 2.3.93-2
- Fix to create /var/cache/fontconfig/stamp in the post install stage.

* Wed Dec 21 2005 Carl Worth <cworth@redhat.com> - 2.3.93-1
- New upstream version.

* Tue Dec 13 2005 Carl Worth <cworth@redhat.com> - 2.3.92.cvs20051129-3
- Disable hinting for Lohit Gujarati

* Fri Dec  9 2005 Carl Worth <cworth@redhat.com> - 2.3.92.cvs20051129-2
- Add two new Chinese font names to the default fonts.conf file:
    AR PL ShanHeiSun Uni
    AR PL Zenkai Uni

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051129-1
- Update to a newer cvs snapshot

* Sat Nov 19 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051119-1
- Update to a newer cvs snapshot

* Wed Nov 16 2005 Bill Nottingham <notting@redhat.com> - 2.3.93-3
- modular X moved fonts from /usr/X11R6/lib/X11/fonts to
  /usr/share/X11/fonts, adjust %%configure accordingly and 
  conflict with older font packages

* Wed Nov  9 2005 Carl Worth <cworth@redhat.com> - 2.3.92-2
- Remove inadvertent rejection of Luxi Mono from 40-blacklist-fonts.conf.
  Fixes #172437

* Fri Nov  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92-1
- Update to 2.3.92

* Mon Oct 31 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051031-1
- Update to a newer cvs snapshot
- Add a patch which should help to understand broken cache problems

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051017-2
- Add new Chinese fonts
- Fix the 40-blacklist-fonts.conf file to use the documented
  fonts.conf syntax, and exclude the Hershey fonts by family
  name.

* Fri Oct 14 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051017-1
- Update to the mmap branch of fontconfig

* Fri Jul 22 2005 Kristian Høgsberg <krh@redhat.com> - 2.3.2-1
- Update to fontconfig-2.3.2.  Drop

	fontconfig-2.1-slighthint.patch,
	fontconfig-2.2.3-timestamp.patch,
	fontconfig-2.2.3-names.patch,
	fontconfig-2.2.3-ta-pa-orth.patch, and
	fontconfig-2.2.3-timestamp.patch,

  as they are now merged upstream.

- Fold fontconfig-2.2.3-add-sazanami.patch into
  fontconfig-2.3.2-defaultconfig.patch and split rules to disable CJK
  hinting out into /etc/fonts/conf.d/50-no-hint-fonts.conf.

- Drop fontconfig-0.0.1.020826.1330-blacklist.patch and use the new
  rejectfont directive to reject those fonts in 40-blacklist-fonts.conf.

- Add fontconfig-2.3.2-only-parse-conf-files.patch to avoid parsing
  .rpmsave files.

- Renable s390 documentation now that #97079 has been fixed and add
  BuildRequires: for docbook-utils and docbook-utils-pdf.

- Drop code to iconv and custom install man pages, upstream does the
  right thing now.

- Add workaround from hell to make elinks cooperate so we can build
  txt documentation.

* Tue Apr 19 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-13
- Add another font family name Sazanami Gothic/Mincho (#148748)

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-12
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-11
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-10
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-9
- Disable docs for s390 for now

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-8
- Rebuild

* Wed Dec  1 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-6
- Sleep a second before the exit of fc-cache to fix problems with fast 
  serial installs of fonts (#140335)
- Turn off hinting for Lohit Hindi/Bengali/Punjabi (#139816)

* Tue Oct 19 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-5
- Add Lohit fonts for Indic languages (#134492)
- Add Punjabi converage, fix Tamil coverage

* Wed Sep 22 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-4
- Update fonts-hebrew names to include CLM suffix

* Thu Sep  2 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-3
- Backport code from head branch of fontconfig CVS to parse names 
  for postscript fonts (fixes #127500, J. J. Ramsey)
- Own /usr/share/fonts (#110956, David K. Levine)
- Add KacstQura to serif/sans-serif/monospace aliases (#101182)

* Mon Aug 16 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-2
- Don't run fc-cache if the binary isn't there (#128072, tracked
  down by Jay Turner)

* Tue Aug  3 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-1
- Upgrade to 2.2.3
- Convert man pages to UTF-8 (#108730, Peter van Egdom)
- Renable docs on s390

* Mon Jul 26 2004 Owen Taylor <otaylor@redhat.com> - 2.2.1-12
- Rebuild for RHEL
- Back freetype required version down to 2.1.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-10
- Require recent freetype (#109592, Peter Oliver)
- Remove fonts.conf timestamp to fix multiarch conflict (#118182)
- Disable hinting for Mukti Narrow (#120915, Sayamindu Dasgupta)

* Wed Mar 10 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-8.1
- Rebuild

* Wed Mar 10 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-8.0
- Add Albany/Cumberland/Thorndale as fallbacks for Microsoft core fonts and 
  as non-preferred alternatives for Sans/Serif/Monospace
- Fix FreeType includes for recent FreeType

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Sep 22 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-6.0
- Should have been passing --with-add-fonts, not --with-add-dirs to 
  configure ... caused wrong version of Luxi to be used. (#100862)

* Fri Sep 19 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-5.0
- Tweak fonts.conf to get right hinting for CJK fonts (#97337)

* Tue Jun 17 2003 Bill Nottingham <notting@redhat.com> 2.2.1-3
- handle null config->cache correctly

* Thu Jun 12 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-2
- Update default config to include Hebrew fonts (#90501, Dov Grobgeld)

* Tue Jun 10 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-2
- As a workaround disable doc builds on s390

* Mon Jun  9 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-1
- Version 2.2.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com> 2.1-8
- Fix segfault in fc-cache from .dircache patch

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com>
- Back out patch that wrote fonts.conf entries that crash RH-8.0 
  gnome-terminal, go with patch from fontconfig CVS instead.
  (#84863)

* Tue Feb 11 2003 Owen Taylor <otaylor@redhat.com>
- Move fontconfig man page to main package, since it contains non-devel 
  information (#76189)
- Look in the OTF subdirectory of /usr/X11R6/lib/fonts as well
  so we find Syriac fonts (#82627)

* Thu Feb  6 2003 Matt Wilson <msw@redhat.com> 2.1-5
- modified fontconfig-0.0.1.020626.1517-fontdir.patch to hard code
  /usr/X11R6/lib/X11/fonts instead of using $(X_FONT_DIR).  This is
  because on lib64 machines, fonts are not in /usr/X11R6/lib64/....

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Owen Taylor <otaylor@redhat.com>
- Try a different tack when fixing cache problem

* Tue Jan 14 2003 Owen Taylor <otaylor@redhat.com>
- Try to fix bug where empty cache entries would be found in 
  ~/.fonts.cache-1 during scanning (#81335)

* Thu Nov 21 2002 Mike A. Harris <mharris@redhat.com> 2.1-1
- Updated to version 2.1
- Updated slighthint patch to fontconfig-2.1-slighthint.patch
- Updated freetype version required to 2.1.2-7

* Mon Sep  2 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0
- Correct capitalization/spacing for ZYSong18030 name (#73272)

* Fri Aug 30 2002 Owen Taylor <otaylor@redhat.com>
- Blacklist fonts from ghostscript-fonts that don't render correctly

* Mon Aug 26 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to fcpackage rc3
- Fix bug in comparisons for xx_XX language tags
- Compensate for a minor config file change in rc3

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Add an explicit PreReq for freetype
- Move fonts we don't ship to the end of the fonts.conf aliases so
  installing them doesn't change the look.

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Memory leak fix when parsing config files
- Set rh_prefer_bitmaps for .ja fonts to key off of in Xft
- Fix some groff warnings for fontconfig.man (#72138)

* Thu Aug 15 2002 Owen Taylor <otaylor@redhat.com>
- Try once more to get the right default Sans-serif font :-(
- Switch the Sans/Monospace aliases for Korean to Gulim, not Dotum

* Wed Aug 14 2002 Owen Taylor <otaylor@redhat.com>
- Fix %%post

* Tue Aug 13 2002 Owen Taylor <otaylor@redhat.com>
- Fix lost Luxi Sans default

* Mon Aug 12 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to rc2
- Turn off hinting for all CJK fonts
- Fix typo in %%post
- Remove the custom language tag stuff in favor of Keith's standard 
  solution.

* Mon Jul 15 2002 Owen Taylor <otaylor@redhat.com>
- Prefer Luxi Sans to Nimbus Sans again

* Fri Jul 12 2002 Owen Taylor <otaylor@redhat.com>
- Add FC_HINT_STYLE to FcBaseObjectTypes
- Switch Chinese fonts to always using Sung-ti / Ming-ti, and never Kai-ti
- Add ZYSong18030 to aliases (#68428)

* Wed Jul 10 2002 Owen Taylor <otaylor@redhat.com>
- Fix a typo in the langtag patch (caught by Erik van der Poel)

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- Add FC_HINT_STYLE tag

* Thu Jun 27 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version, with fix for problems with
  ghostscript-fonts (Fonts don't work for Qt+CJK,
  etc.)

* Wed Jun 26 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version, fixing locale problem

* Mon Jun 24 2002 Owen Taylor <otaylor@redhat.com>
- Add a hack where we set the "language" fontconfig property based on the locale, then 
  we conditionalize base on that in the fonts.conf file.

* Sun Jun 23 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version

* Tue Jun 18 2002 Owen Taylor <otaylor@redhat.com>
- Fix crash from FcObjectSetAdd

* Tue Jun 11 2002 Owen Taylor <otaylor@redhat.com>
- make fonts.conf %%config, not %%config(noreplace)
- Another try at the CJK aliases
- Add some CJK fonts to the config
- Prefer Luxi Mono to Nimbus Mono

* Mon Jun 10 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version
- Fix matching for bitmap fonts

* Mon Jun  3 2002 Owen Taylor <otaylor@redhat.com>
- New version, new upstream mega-tarball

* Tue May 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem with FcConfigSort

* Fri May 24 2002 Owen Taylor <otaylor@redhat.com>
- Initial specfile

