Summary: The GNU data compression program
Name: gzip
Version: 1.5
Release: 10%{?dist}
# info pages are under GFDL license
License: GPLv3+ and GFDL
Group: Applications/File
Source: http://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.xz
Patch0: gzip-1.3.12-openbsd-owl-tmp.patch
Patch1: gzip-1.3.5-zforce.patch
Patch4: gzip-1.3.13-rsync.patch
Patch5: gzip-1.3.9-addsuffix.patch
Patch6: gzip-1.3.5-cve-2006-4338.patch
Patch7: gzip-1.3.13-cve-2006-4337.patch
Patch8: gzip-1.3.5-cve-2006-4337_len.patch
Patch9: gzip-1.5-nonblock.patch
Patch10: gzip-1.5-overwrite.patch
Patch11: gzip-1.5-missing-grep-options-part1.patch
Patch12: gzip-1.5-missing-grep-options-part2.patch
# Fixed in upstream code.
# http://thread.gmane.org/gmane.comp.gnu.gzip.bugs/378
URL: http://www.gzip.org/
# Requires should not be added for gzip wrappers (eg. zdiff, zgrep,
# zless) of another tools, because gzip "extends" the tools by its
# wrappers much more than it "requires" them.
Requires: /sbin/install-info
Requires: coreutils
BuildRequires: texinfo
Conflicts: filesystem < 3
Provides: /bin/gunzip
Provides: /bin/gzip
Provides: /bin/zcat
# Gzip contains bundled Gnulib
# exception https://fedorahosted.org/fpc/ticket/174 
Provides: bundled(gnulib)

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.

%prep
%setup -q
%patch0 -p1 -b .owl-tmp
%patch1 -p1 -b .zforce
%patch4 -p1 -b .rsync
%patch5 -p1 -b .addsuffix
%patch6 -p1 -b .4338
%patch7 -p1 -b .4337
%patch8 -p1 -b .4337l
%patch9 -p1 -b .nonblock
%patch10 -p1 -b .overwrite
%patch11 -p1 -b .options1
%patch12 -p1 -b .options2

%build
export DEFS="NO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
%configure 

make
#make gzip.info

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall 

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/gzip.info*

# we don't ship it, so let's remove it from ${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
# uncompress is a part of ncompress package
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/uncompress

%post
if [ -f %{_infodir}/gzip.info* ]; then
    /sbin/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/gzip.info* ]; then
        /sbin/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir || :
    fi
fi

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/gzip.info*

%changelog
* Mon Sep 11 2017 Jakub Martisko <jamartis@redhat.com> - 1.5-10
- doc change: missing grep options are now mentioned in the zgrep 
  man pages/help message
  Resolves: #1437002

* Tue Feb 28 2017 Petr Stodulka <pstodulk@redhat.com> - 1.5-9
- fix zfoce
  Resolves: #1382054

* Mon Mar 16 2015 Petr Stodulka <pstodulk@redhat.com> - 1.5-8
- Gzip overwrite existing files when user choose "no" on yes/no question.
  It's due to wrong dupicit declaration of yesno() function in gzip.h
  which is compiled wrong with -O2 option.
  Resolves: rhbz#1201689

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.5-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.5-6
- Mass rebuild 2013-12-27

* Fri Nov 15 2013 Petr Stodulka <pstodulk@redhat.com> - 1.5-5
- fix issue with nonblocking open for PAR and OFL file
  Resolves: rhbz#1028052

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Daniel Drake <dsd@laptop.org> - 1.5-3
- Fix "gzip --rsyncable" functionality by removing a spurious blank line from
  the patch.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Michal Luscon <mluscon@redhat.com>
- Added bundled(glib) 

* Tue Jun 19 2012 Michal Luscon <mluscon@redhat.com> 1.5-1
- New upstream version
- Removed gzip-1.3.9-stderr.patch
- Removed gzip-1.3.10-zgreppipe.patch
- Removed gzip-1.3.13-noemptysuffix.patch

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 1.4-6
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 1.4-5
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep  6 2010 Karel Klic <kklic@redhat.com> - 1.4-2
- Removed the dependency on less (rhbz#629580)
- Removed the BuildRoot tag
- Removed the %%clean section

* Tue Mar 16 2010 Karel Klic <kklic@redhat.com> - 1.4-1
- New upstream release
- Use XZ upstream source archive
- Removed cve-2010-0001 patch as it's fixed in this release
- Removed zdiff patch as it's fixed in this release

* Mon Feb 22 2010 Karel Klic <kklic@redhat.com> - 1.3.13-3
- Added a patch to disallow -S '' parameter (noemptysuffix)

* Fri Jan 22 2010 Karel Klic <kklic@redhat.com> - 1.3.13-2
- Fixed CVE-2010-0001 (rhbz#554418)

* Tue Dec  1 2009 Karel Klic <kklic@redhat.com> - 1.3.13-1
- New upstream version
- Updated license from GPLv2 to GPLv3+
- Removed gzip-1.3.12-futimens.patch, as it is fixed in the new version
- Updated rsync patch to the new upstream version
- Updated cve-2006-4337 patch to use gzip_error instead of error

* Fri Oct  9 2009 Ivana Varekova <varekova@redhat.com> - 1.3.12-12
- change the source tag

* Tue Aug 11 2009 Ivana Varekova <varekova redhat com> - 1.3.12-11
- fix installation with --excludedocs option (#515975)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Ivana Varekova <varekova@redhat.com> - 1.3.12-9
- fix #484213 - zdiff shows no output

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  1 2008 Ivana Varekova <varekova@redhat.com> - 1.3.12-7
- update patches

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.12-6
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Ivana Varekova <varekova@redhat.com> - 1.3.12-5
- rebuild

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.3.12-4
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 Ivana Varekova <varekova@redhat.com> - 1.3.12-3
- remove useless patches (fixed in upstream version)

* Mon Jun 11 2007 Ivana Varekova <varekova@redhat.com> - 1.3.12-2
- remove useless patches

* Mon Jun  4 2007 Ivana Varekova <varekova@redhat.com> - 1.3.12-1
- update to 1.3.12

* Mon Mar  5 2007 Ivana Varekova <varekova@redhat.com> - 1.3.11-1
- update to 1.3.11
  remove uncompress

* Tue Feb  6 2007 Ivana Varekova <varekova@redhat.com> - 1.3.10-1
- Resolves: 225878
  update to 1.3.10
  change BuildRoot

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 1.3.9-2
- Resolves: 223702
  fix non-failsafe install-info problem

* Mon Jan 15 2007 Ivana Varekova <varekova@redhat.com> - 1.3.9-1
- rebuild to 1.3.9
- spec cleanup

* Wed Nov 22 2006 Ivana Varekova <varekova@redhat.com> - 1.3.5-11
- fix too strict uncompress function

* Mon Oct 23 2006 Ivana Varekova <varekova@redhat.com> - 1.3.5-10
- fix package description (#208924)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-9
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Ivana Varekova <varekova@redhat.com> 1.3.5-8
- fix bug 204676 (patches by Tavis Ormandy)
  - cve-2006-4334 - null dereference problem
  - cve-2006-4335 - buffer overflow problem
  - cve-2006-4336 - buffer underflow problem
  - cve-2006-4338 - infinite loop problem
  - cve-2006-4337 - buffer overflow problem

* Fri Jul 14 2006 Karsten Hopp <karsten@redhat.de> 1.3.5-7
- buildrequire texinfo, otherwise gzip.info will be empty

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-6.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon May 02 2005 Ivana Varekova <varekova@redhat.com> 1.3.5-6
- rebuilt

* Fri Apr 29 2005 Ivana Varekova <varekova@redhat.com> 1.3.5-5
- fix bug 156269 - CAN-2005-1228 directory traversal bug
 (using the patch from Ulf Harnhammar)

* Tue Apr 26 2005 Ivana Varekova <varekova@redhat.com> 1.3.5-4
- fix bug 155746 - CAN-2005-0988 Race condition in gzip (patch9)

* Wed Mar 23 2005 Tomas Mraz <tmraz@redhat.com> 1.3.5-3
- don't use the asm code again as it's slower than the gcc compiled one
- convert the .spec to UTF-8

* Tue Mar 22 2005 Tomas Mraz <tmraz@redhat.com> 1.3.5-2
- upstream 1.3.5
- dropped long ago obsolete dirinfo patch
- escape file names in zgrep (#123012)
- make stack in match.S nonexecutable

* Fri Mar 04 2005 Jiri Ryska <jryska@redhat.com>
- rebuilt

* Mon Dec 13 2004 Ivana Varekova <varekova@redhat.com>
- fix patch - remove brackets

* Mon Dec 13 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #106551 problem with zmore which requires the suffix .gz in file name

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct 28 2003 Jeff Johnson <jbj@redhat.com> 1.3.3-11
- rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 31 2003 Jeff Johnson <jbj@redhat.com> 1.3.3-9
- enlarge window buffer to avoid accessing beyond end-of-buffer (#78413,#83095).
- re-enable rsync ready patch.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 22 2002 Jeff Johnson <jbj@redhat.com> 1.3.3-7
- workaround mis-compilation with gcc-3.2-4 on alpha for now (#78413).

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches
- remove file from buildroot we aren't shipping

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-4
- Fix the reading of unitialized memory problem (#66913)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-2
- Rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-1
- 1.3.3

* Sun Mar 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add rsyncable patch #58888

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.2-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.3.2-1
- 1.3.2: no need for autoconf 2.5x hacks anymore

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.3.1:
- disable patch2

* Fri Oct 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.3.0-16
- replace tempfile patches with improved ones solar@openwall.com
- Add less to the dependency chain - zless needs it

* Thu Aug 23 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.3.0-15
- Fix typo in comment in zgrep (#52465) 
- Copyright -> License

* Tue Jun  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Patch various uses of $$ in the bundled scripts

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix the SIGPIPE patch to avoid blank lines (#43319)

* Thu Feb 08 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed buzilla bug #26680. Wrong skip value after mktemp patch and forced
  overwrite for output file during decompression.

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- trap SIGPIPE in zgrep, so "zgrep | less" gets a happy ending
  (#24104)

* Sun Dec 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add HAVE_LSTAT define, to avoid it doing weird things to symlinks
  instead of ignoring them as the docs say it should (#22045)

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Thu Nov 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patch all scripts so usage error messages are written to 
  stderr (#20597)

* Mon Oct 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable assembly, as it is faster without it (bug #19910)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%{_mandir}, %%{_infodir},  %%configure, %%makeinstall
  and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add root as default owner of the files, permits building 
  as non-root user

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Build system handles stripping
- Don't do thing the system does, like creating directories
- use --bindir /bin
- Added URL
- skip unnecesarry sed step
- Include THANKS, AUTHORS, ChangeLog, TODO

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3
- handle RPM_OPT_FLAGS

* Tue Feb 15 2000 Cristian Gafton <gafton@redhat.com>
- handle compressed man pages even better

* Tue Feb 08 2000 Cristian Gafton <gafton@redhat.com>
- adopt patch from Paul Eggert to fix detection of the improper tables in
  inflate.c(huft_build)
- the latest released version 1.2.4a, which provides documentation updates
  only. But it lets us use small revision numbers again
- add an dirinfo entry for gzip.info so we can get rid of the ugly --entry
  args to install-info

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Fix bug #7970

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- built against gliibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/bin/gzip and /usr/bin/gunzip symlinks as some programs are too
  brain dead to figure out they should be at least trying to use $PATH
- added BuildRoot

* Wed Jan 28 1998 Erik Troan <ewt@redhat.com>
- fix /tmp races

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info
- applied patch for gzexe

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Marc Ewing <marc@redhat.com>
- (Entry added for Marc by Erik) fixed gzexe to use /bin/gzip

