%define filippov_version 1.0.7pre44
%define fontdir %{_datadir}/fonts/default/Type1
%define catalogue /etc/X11/fontpath.d

Summary: Free versions of the 35 standard PostScript fonts.
Name: urw-fonts
Version: 2.4
Release: 16%{?dist}
Source: %{name}-%{filippov_version}.tar.bz2
URL: http://svn.ghostscript.com/ghostscript/tags/urw-fonts-1.0.7pre44/
# URW holds copyright
# No version specified
License: GPL+
Group: User Interface/X
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires(post): fontconfig
Requires(post): xorg-x11-font-utils
Requires(postun): fontconfig

%description 
Free, good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.

Install the urw-fonts package if you need free versions of standard
PostScript fonts.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{fontdir}
install -m 0644 *.afm *.pfb $RPM_BUILD_ROOT%{fontdir}/

# Touch ghosted files
touch $RPM_BUILD_ROOT%{fontdir}/{fonts.{dir,scale,cache-1},encodings.dir}

# Install catalogue symlink
mkdir -p $RPM_BUILD_ROOT%{catalogue}
ln -sf %{fontdir} $RPM_BUILD_ROOT%{catalogue}/fonts-default

%post
{
   umask 133
   mkfontscale %{fontdir} || :
   mkfontdir %{fontdir} || :
   fc-cache %{_datadir}/fonts
} &> /dev/null || :

%postun
{
   if [ "$1" = "0" ]; then
      fc-cache %{_datadir}/fonts
   fi
} &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc COPYING README README.tweaks
%dir %{_datadir}/fonts/default
%dir %{fontdir}
%{catalogue}/fonts-default
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.scale
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{fontdir}/encodings.dir
%{fontdir}/*.afm
%{fontdir}/*.pfb

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4-16
- Mass rebuild 2013-12-27

* Thu May  2 2013 Tom Callaway <spot@fedoraproject.org> - 2.4-15
- simplify post scriptlet a bit, don't drop output to /dev/null for debugging purposes

* Tue Feb 26 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-14
- Added Requires(post): xorg-x11-font-utils (BZ #478786).

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 27 2009 Than Ngo <than@redhat.com> - 2.4-9
- fix #77314, invalid URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.4-6
- fix license tag

* Mon Feb 11 2008 Than Ngo <than@redhat.com> 2.4-5
- fix description

* Wed Jan 09 2008 Than Ngo <than@redhat.com> 2.4-4
- fix release conflict with f8

* Tue Jan 08 2008 Than Ngo <than@redhat.com> 2.4-2
- update to 1.0.7pre44
- fix #426245, removes two broken lines (two invalid glyph names)

* Fri Aug 10 2007 Than Ngo <than@redhat.com> - 2.4-1
- update to 1.0.7pre43, changed Roman glyphs in all fonts back
  to original metrics. bz#243180, bz#138896, bz#140584
- cleanup BR, bz#227297
- drop chkfontpath dependency and use the catalogue font path mechanism

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3-6.1.1
- rebuild

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 17 2005 Warren Togami <wtogami@redhat.com> 2.3-6
- post and postun on reqs

* Thu Nov 17 2005 Than Ngo <than@redhat.com> 2.3-5
- fix the mkfontdir issue for modular X
- remove unneeded -e option from mkfontdir
- add Prereq on mkfontdir

* Thu Nov 17 2005 Warren Togami <wtogami@redhat.com> 2.3-4
- req mkfontdir
- better way to run mkfontdir

* Thu Nov 17 2005 Than Ngo <than@redhat.com> 2.3-3 
- fix mkfontdir macro for modular X
 
* Mon Nov  7 2005 Jeremy Katz <katzj@redhat.com> - 2.3-2
- require (virtual) mkfontscale instead of path to handle 
  modular xorg (#172562)

* Mon Apr 04 2005 Than Ngo <than@redhat.com> 2.3-1
- Bump for update to 1.0.7pre40

* Thu Feb 24 2005 Than Ngo <than@redhat.com> 2.2-8
- update to 1.0.7pre40

* Thu Feb 24 2005 Than Ngo <than@redhat.com> 2.2-7
- change descender/ascender in "NimbusMonL" #140584

* Tue Sep 21 2004 Than Ngo <than@redhat.com> 2.2-6
- rebuilt

* Mon Sep 06 2004 Than Ngo <than@redhat.com> 2.2-5
- remove fonts, which included in new upstream

* Mon Sep 06 2004 Than Ngo <than@redhat.com> 2.2-4
- update to 1.0.7pre38

* Fri Sep 03 2004 Than Ngo <than@redhat.com> 2.2-3
- own %%{_datadir}/fonts/default #131648

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Than Ngo <than@redhat.com> 2.2-1
- Upgrade to upstream version 1.0.7pre26, bug #122500
- drop NimbusRomNo9L-Medi* fonts that are included in pre26

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 2.1-7
- fixed bug #119844

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Aug 29 2003 Owen Taylor <otaylor@redhat.com> 2.1-5.0
- Add MediItal variant with fixed weight and some of the
  missing baseline hints (for u,t)

* Mon Jul 21 2003 Owen Taylor <otaylor@redhat.com> 2.1-4.1
- Bump for rebuild

* Mon Jul 21 2003 Owen Taylor <otaylor@redhat.com> 2.1-4.0
- Replace the regular not italic bold font with the fixed copy

* Wed Jul  9 2003 Owen Taylor <otaylor@redhat.com> 2.1-3.1
- Bump for rebuild

* Wed Jul  9 2003 Owen Taylor <otaylor@redhat.com> 2.1-3
- Add some obvious missing hints that were resulting in 
  very uneven baselines (#97271)

* Fri Jun 20 2003 Than Ngo <than@redhat.com> 2.1-2
- fix Weight in Nimbus Roman No 9 L (bug #97683)

* Tue Jun 10 2003 Owen Taylor <otaylor@redhat.com> 2.1-1
- Upgrade to upstream version 1.0.7pre22
- Massive cleanups to fonts.dir/fonts.scale handling (use mkfontscale
  instead of fonts.scale from the package, etc.)

* Wed Jan 29 2003 Than Ngo 2.0-29
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 2.0-27
- rebuild 

* Fri Aug 30 2002 Alexander Larsson <alexl@redhat.com> 2.0-26
- Call fc-cache from %%post, prereq fontconfig

* Fri Jul 12 2002 Owen Taylor <otaylor@redhat.com>
- Didn't revert back far enough to fix hints last time; try again.

* Wed Jul 10 2002 Owen Taylor <otaylor@redhat.com>
- Fix packaging error that lost most of the fonts

* Mon Jul  8 2002 Owen Taylor <otaylor@redhat.com>
- Go back to 1.0 URW/cyrillic version to avoid hinting problems

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Newer upstream version
- Fix accidental revert of urw-fontspecific => adobe-fontspecific change
- Tweak hints in "Nimbus Sans Regular L" a bit.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Than Ngo <than@redhat.com> 2.0-19
- update urw fonts
- add missing ZapfDingbats font (bug #65101, #65523)
- fixed metric troubles (bug #65522)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 2.0-17
- rebuild

* Tue Jan 22 2002 Preston Brown <pbrown@redhat.com>
- use adobe-fontspecific instead of urw-fontspecific encoding name for 
  symbol font.  Fixes some java issues.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Dec 13 2001 Than Ngo <than@redhat.com> 2.0-14
- fixed bug #57306

* Wed Sep 26 2001 Than Ngo <than@redhat.com> 2.0-13
- Added new fonts with cyrrilic glyphs
  from ftp://ftp.gnome.ru/fonts/urw/ (bug #52772)
 
* Thu Nov 16 2000 Than Ngo <than@redhat.com>
- zapf dingbats font works now, fixed (Bug #20352)

* Mon Oct 16 2000 Than Ngo <than@redhat.com>
- added font aliases (Bug #17586)
- added missing fonts.alias

* Wed Aug 30 2000 Preston Brown <pbrown@redhat.com>
- enable latin2 encoding
- alias the Nimbus/Courier font to be monospaced
- include a Fontmap

* Fri Jul 14 2000 Preston Brown <pbrown@redhat.com>
- renamed fonts from URW names to Adobe names for better compatibility

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 09 2000 Than Ngo <than@redhat.de>
- update gnu-gs-fonts-std-6.0
- fix Url

* Sat May 27 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0

* Wed Mar 08 2000 Preston Brown <pbrown@redhat.com> 
- argh! fonts.scale shouldn't have been symlinked to fonts.dir.  fixed.

* Mon Feb 28 2000 Preston Brown <pbrown@redhat.com>
- noreplace the fonts.dir config file

* Wed Feb 16 2000 Bill Nottingham <notting@redhat.com>
- need .pfb files too

* Mon Feb 14 2000 Preston Brown <pbrown@redhat.com>
- new URW++ fonts that include extra glyphs.

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- remove vendor tag.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Tue Mar 09 1999 Preston Brown <pbrown@redhat.com>
- fixed up chkfontpath stuff

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb 15 1999 Preston Brown <pbrown@redhat.com>
- added missing fonts.dir, fonts.scale, %post, %postun using chkfontpath
- changed foundary from Adobe (which was a lie) to URW.

* Sat Feb 06 1999 Preston Brown <pbrown@redhat.com>
- fonts now live in /usr/share/fonts/default/Type1

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- eliminated section that adds to XF86Config
- changed fonts to reside in /usr/share/fonts/default/URW, so they can be
  shared between X and Ghostscript (and other, future programs/applications)

* Fri Sep 11 1998 Preston Brown <pbrown@redhat.com>
- integrate adding fontdir to XF86Config

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- eliminate %post output

* Wed Jul  8 1998 Jeff Johnson <jbj@redhat.com>
- create from Stefan Waldherr <swa@cs.cmu.edu> contrib package.
