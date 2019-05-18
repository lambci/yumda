Summary: A text file browser similar to more, but better
Name: less
Version: 458
Release: 9%{?dist}.0.2
License: GPLv3+
Group: Applications/Text
Source: http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
Source1: lesspipe.sh
Source2: less.sh
Source3: less.csh
Patch1:	less-444-Foption.v2.patch
Patch2: less-394-search.patch
Patch4: less-394-time.patch
Patch5: less-418-fsync.patch
Patch6: less-436-manpage-add-old-bot-option.patch
Patch7: less-436-help.patch
Patch8: less-458-lessecho-usage.patch
Patch9: less-458-less-filters-man.patch
Patch10: less-458-lesskey-usage.patch
Patch11: less-458-old-bot-in-help.patch
Patch12: less-458-use-backslash.patch
URL: http://www.greenwoodsoftware.com/less/
Requires: groff-base
BuildRequires: ncurses-devel
BuildRequires: autoconf automake libtool

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi). 

You should install less because it is a basic utility for viewing text
files, and you'll use it frequently.

%prep
%setup -q
%patch1 -p1 -b .Foption
%patch2 -p1 -b .search
%patch4 -p1 -b .time
%patch5 -p1 -b .fsync
%patch6 -p1 -b .manpage-add-old-bot-option
%patch7 -p1 -b .help
%patch8 -p1 -b .lessecho-usage
%patch9 -p1 -b .less-filters-man
%patch10 -p1 -b .lesskey-usage
%patch11 -p1 -b .oldbothelp
%patch12 -p2 -b .use-backslash
autoreconf

chmod -R a+w *
chmod 644 *.c *.h LICENSE README

%build
%configure
make CC="gcc $RPM_OPT_FLAGS -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64" datadir=%{_docdir}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -p -c -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}
install -p -c -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d
install -p -c -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d
ls -la $RPM_BUILD_ROOT/etc/profile.d

%files
%defattr(-,root,root,-)
%doc LICENSE
/etc/profile.d/*
%{_bindir}/*
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu May 21 2015 Jozef Mlich <jmlich@redhat.com> - 458-9
- The --use-backslash option documented in the man page
  was missing from online help for less.
  Resolves: #1109090

* Mon Feb 03 2014 Jozef Mlich <jmlich@redhat.com> - 458-8
- changes introduced in less-458-old-bot-in-help.patch
  wasn't compiled in. It is necessary to use mkhelp tool.
  Resolves: #948597

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 458-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 458-6
- Mass rebuild 2013-12-27

* Mon Dec 02 2013 Jozef Mlich <jmlich@redhat.com> - 458-5
- fixing regression in 72dfd3f63594e1d4c9416180a95c47ae583934c6
  incorrect parsing of commandline arguments
- Resolves #948597

* Thu Jul 11 2013 Ondrej Vasik <ovasik@redhat.com> - 458-4
- apply the --old-bot patch (#983167)

* Tue May 07 2013 Fridolin Pokorny <fpokorny@redhat.com> - 458-3
- Expanded lessecho usage (#948597)
- Added lessfilter info to man (#948597)
- Expanded lesskey usage (#948597)
- Added --old-bot to help (#948597)

* Thu Apr 11 2013 Fridolin Pokorny <fpokorny@redhat.com> - 458-2
- Added gpg support to lesspipe.sh (#885122)
- Added ~/.lessfilter support (#885122)

* Thu Apr 11 2013 Fridolin Pokorny <fpokorny@redhat.com> - 458-1
- Update to 458

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 451-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Martin Briza <mbriza@redhat.com> - 451-2
- Changed unnecessary groff dependency to groff-base (#868376)

* Tue Sep 11 2012 Martin Briza <mbriza@redhat.com> - 451-1
- Rebase to 451 (#835802)
- Removed the empty-lessopen-pipe patch as the issue is now fixed upstream.

* Mon May 14 2012 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-7
- Fix less.sh not to override user-defined LESSOPEN variable (#802757)
- Use POSIX regcomp instead of PCRE - revert 406-11, commit 4b961c7 (#643233)
- Merge Foption changes by Colin Guthrie to Foption.v2.patch (#805735)

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 444-6
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 444-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-4
- Avoid some unnecessary stat calls and commands in lesspipe.sh,
  patch by Ville Skyttä (#741440)
- Use `groff' instead of `man -s' for rendering manpages to prevent
  options incompatibility between man and man-db packages (#718498)
- Add groff to Requires

* Tue Aug 23 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-3
- Substitute %%makeinstall macro with make DESTDIR* install (#732557)

* Fri Aug 12 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-2
- Fix debuginfo source files permissions
- Remove strip after %%makeinstall to fix debuginfo package

* Thu Jul 14 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 444-1
- Rebase to 444 (#713406)

* Wed Apr 20 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 443-1
- Rebase to 443
- Foption patch made applicable against 443
- Manpage extra line patch removed; fixed upstream (#697451)

* Wed Apr 13 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-13
- Don't convert files with UTF-16/UTF-32 string in filename (#638312)

* Tue Feb 15 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-12
- Enable LESSOPEN exit statuses as default also in less.sh (#666084, #676057)

* Tue Feb 15 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-11
- Clean lesspipe.sh script
- Split case for compressed and plain troff files
- Add support for *.xz and *.lzma man pages (#676057)
- Add support for reading UTF-16 and UTF-32 files (#638312)
- Don't require correct exit status from LESSOPEN scripts until
  it gets accepted by upstream (preserve backward compatibility) (#666084, #676057)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 436-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-9
- Fix regression in lesspipe.sh script (*.gz files etc.) (#615303 comment #9)

* Wed Dec 22 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-8
- The new "--old-bot" option is not documented in the man page (#510724)
- Fix descriptions of some options in online help
  (#578289, patch by Jeff Bastian <jbastian@redhat.com> [IT603793])

* Tue Dec 21 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 436-7
- Fix for valid empty LESSOPEN pipe output (#579251, #615303)

* Wed Jan 20 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 436-6
- RFE: lesspipe.sh could use a support for *.xz file

* Mon Jan 4 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 436-5
- patched wrong manpage. Resolves: #537746.

* Sat Dec 12 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 436-4
- #546613 - RFE: add *.jar *.nbm to lesspipe.sh

* Wed Dec 9 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 436-3
- Resolves: #537746 - Two different descriptions about the default value of LESSBINFMT

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 436-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Zdenek Prikryl <zprikryl@redhat.com> - 436-1
- Foption patch is more optimal now
- Update to 436

* Tue Apr 14 2009 Zdenek Prikryl <zprikryl@redhat.com> - 429-1
- Update to 429

* Tue Mar 31 2009 Zdenek Prikryl <zprikryl@redhat.com> - 424-4
- Added GraphicsMagick support (#492695)

* Tue Mar 17 2009 Zdenek Prikryl <zprikryl@redhat.com> - 424-3
- Added lzma support
- Added test if fsync produces EIVAL on tty

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 424-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jun 25 2008 Zdenek Prikryl <zprikryl@redhat.com> - 424-1
- Update to 424

* Wed Jun 11 2008 Zdenek Prikryl <zprikryl@redhat.com> - 423-1
- Update to 423

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 418-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Zdenek Prikryl <zprikryl@redhat.com> - 418-2
- Fixed -F option
- Resolves: #427551

* Fri Jan 04 2008 Zdenek Prikryl <zprikryl@redhat.com> - 418-1
- Update to 418

* Fri Nov 23 2007 Zdenek Prikryl <zprikryl@redhat.com> - 416-1
- Update to 416
- Fixed SIGABORT caused by UTF-8 related bug
- Resolves #395591

* Wed Nov 21 2007 Zdenek Prikryl <zprikryl@redhat.com> - 415-1
- Update to 415

* Tue Nov 13 2007 Ivana Varekova <varekova@redhat.com> - 409-2
- remove which usage (#312591)

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 409-1
- upgrade to 409
- remove useless/obsolete patches
- add autoconf buildrequires

* Mon Oct  1 2007 Ivana Varekova <varekova@redhat.com> - 406-12
- change license tag
- fix 312591 - add which dependency

* Thu Aug  9 2007 Ivana Varekova <varekova@redhat.com> - 406-11
- configure a regular expression library

* Tue Jun 26 2007 Ivana Varekova <varekova@redhat.com> - 406-10
- update to 406

* Mon Jun  4 2007 Ivana Varekova <varekova@redhat.com> - 394-10
- Resolves: #242077
  remove "-" option from lesspipe.sh script

* Tue Feb 20 2007 Ivana Varekova <varekova@redhat.com> - 394-9
- change /etc/profile.d script's permissions

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 394-8
- change LICENSE permissions

* Wed Feb  7 2007 Ivana Varekova <varekova@redhat.com> - 394-7
- incorporate the package review

* Wed Nov 22 2006 Ivana Varekova <varekova@redhat.com> - 394-6
- fix permissions of debuginfo source code

* Wed Oct 25 2006 Ivana Varekova <varekova@redhat.com> - 394-5
- fix command ">" (#120916)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 394-4.1
- rebuild

* Fri May 05 2006 Ivana Varekova <varekova@redhat.com> - 394-4
- fix problem with unassigned variable DECOMPRESSOR (#190619)

* Wed Feb 15 2006 Ivana Varekova <varekova@redhat.com> - 394-3
- add patch for search problem (search did not find string which
  occurs in a line after '\0')

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 394-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 394-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Jindrich Novy <jnovy@redhat.com> 394-2
- apply better fix for #120916 from Avi Kivity (#177819)
  to avoid flickering when '>' is pressed multiple times

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Jindrich Novy <jnovy@redhat.com> 394-1
- update to less-394

* Mon Nov  7 2005 Jindrich Novy <jnovy@redhat.com> 393-1
- update to less-393
- groom Foption patch a bit
- remove obsolete ncursesw and utf8detect patches

* Fri Oct 21 2005 Jindrich Novy <jnovy@redhat.com> 392-2
- fix the -F option (#79650), thanks to Petr Raszyk

* Wed Oct 19 2005 Jindrich Novy <jnovy@redhat.com> 392-1
- update to less-392 - fixes #122847 and enhances UTF8 support

* Fri Sep  2 2005 Jindrich Novy <jnovy@redhat.com> 382-8
- fix displaying of bogus newline for growing files (#120916)

* Fri Mar  4 2005 Jindrich Novy <jnovy@redhat.com> 382-7
- rebuilt with gcc4

* Wed Feb 16 2005 Jindrich Novy <jnovy@redhat.com> 382-6
- add patch for proper detection of UTF-8 locale,
  patch from Peter Rockai

* Tue Nov 16 2004 Karsten Hopp <karsten@redhat.de> 382-5 
- minor fix in lesspipe.sh (#73215)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 29 2004 Karsten Hopp <karsten@redhat.de> 382-3
- remove old stuff from /etc/profile.d/less.*, fixes #109011

* Tue Mar 02 2004 Karsten Hopp <karsten@redhat.de> 382-1.1 
- build for FC1

* Sat Feb 14 2004 Karsten Hopp <karsten@redhat.de> 382-1
- new upstream version

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 15 2004 Karsten Hopp <karsten@redhat.de> 381-2 
- drop iso247 patch, doesn't work

* Wed Jun 11 2003 Karsten Hopp <karsten@redhat.de> 381-1
- new version with rewritten iso247 patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix korean #79977
- add new less.sh from #89780, s/ko/korean/ and write .csh script
- add patch from #91661: /japanses/japanese-euc/

* Tue Feb  4 2003 Tim Waugh <twaugh@redhat.com> 378-7
- Part of multibyte patch was missing; fixed.

* Mon Feb  3 2003 Tim Waugh <twaugh@redhat.com> 378-6
- Fix underlining multibyte characters (bug #83377).

* Thu Jan 30 2003 Karsten Hopp <karsten@redhat.de> 378-5
- removed older, unused patches
- add patch from Yukihiro Nakai to fix display of japanese text
  (#79977)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 18 2002 Karsten Hopp <karsten@redhat.de>č
- removed default 'cat' from lesspipe.sh as it breaks 'v' and 'F' keys 
  (#79921)

* Fri Dec  6 2002 Nalin Dahyabhai <nalin@redhat.com> 378-2
- add a default case to lesspipe so that it shows other kinds of files

* Mon Nov 04 2002 Karsten Hopp <karsten@redhat.de>
- less-378
- added some debian patches
- show image info instead of binary garbage when viewing images

* Fri Oct 05 2001 Karsten Hopp <karsten@redhat.de>
- fix line numbering (less -N filename), caused by
  a broken i18n patch

* Tue Sep 04 2001 Karsten Hopp <karsten@redhat.de>
- recompile with large file support (#52945)

* Tue Jul 24 2001 Karsten Hopp <karsten@redhat.de>
- fix #49506 (BuildRequires)

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- fixup eline patch to initialize result correctly

* Mon Jun 25 2001 Karsten Hopp <karsten@redhat.de>
- update URLs
- Copyright -> License
- fix #43348 (crashes when searching for /<)
- fix #39849 (
  _ ignores LESSCHARDEF in displaying characters,
  _ prefaces sequences of one or "high" characters with a capital "A")

* Mon Feb  5 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update less.sh, less.csh to set JLESSCHARSET=japanese
  when LANG=ja??

* Mon Feb  5 2001 Matt Wilson <msw@redhat.com>
- changed the less-358+iso247-20001210.diff patch to use strcasecmp when
  comparing locale names

* Thu Feb 01 2001 Karsten Hopp <karsten@redhat.de>
- fixed character translations (bugzilla #24463)

* Wed Jan 31 2001 Karsten Hopp <karsten@redhat.de>
- fixed lesspipe (bugzilla #17456 #25324)

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new ncurses

* Mon Dec 11 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch with ia64 support.

* Mon Nov 27 2000 Karsten Hopp <karsten@redhat.de>
- rebuild with new ncurses
- fix Bug #21288

* Mon Nov 13 2000 Karsten Hopp <karsten@redhat.de>
- fixed handling of manpages of type *.1x.gz
- added support for cpio packages

* Thu Sep 14 2000 Than Ngo <than@redhat.com>
- added new lesspipe.sh (Bug #17456)

* Wed Aug 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- support files with spaces in their names (Bug #16777)

* Tue Aug  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Support gzipped man pages in lesspipe.sh (Bug #15610)

* Thu Aug  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Tweak init script (Bug #14622)

* Thu Jul 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Oops, actually apply the patch for 9443. ;)

* Wed Jul 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up messed output if a user outputs anything in ~/.bashrc or the
  likes (Bug #9443)
- handle RPM_OPT_FLAGS

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 358

* Mon Jun 26 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 354

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to v352

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Jan 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to v346
- Update download URL
- use the configure marcro
- strip binary
- fix up lesspipe stuff (Bug #8750 and a couple of non-reported bugs)
  (Karsten, did I mention I'll kill you when you return from SAP? ;) )

* Fri Jan 07 2000 Karsten Hopp <karsten@redhat.de>
- added lesspipe.sh to show listings of package
  contents instead of binary output.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- less finally gets maintenance, upgraded to 340

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Tue Mar 16 1999 Preston Brown <pbrown@redhat.com>
- removed ifarch axp stuff for /bin/more, more now works on alpha properly.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 332 and built for Manhattan
- added buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
