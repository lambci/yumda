%global _rebuild .1
%global api_version 1.13

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake
Version:    %{api_version}.4
Release: 3%{?_rebuild}%{?dist}

# docs ~> GFDL, sources ~> GPLv2+, mkinstalldirs ~> PD and install-sh ~> MIT
License:    GPLv2+ and GFDL and Public Domain and MIT

Group:      Development/Tools
Source:     ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz

# Disable tests for broken vala installation
# ~> downstream
Patch0:     %{name}-1.13.1-disable-tests.patch

URL:        http://www.gnu.org/software/automake/
Requires:   autoconf >= 2.65

# requirements not detected automatically (#919810)
Requires:   perl(Thread::Queue)
Requires:   perl(threads)

BuildRequires:  autoconf >= 2.65
BuildRequires:  automake
BuildArch:  noarch

# run "make check" by default
%bcond_without check

# for better tests coverage:
%if %{with check}
BuildRequires: libtool gettext-devel flex bison texinfo-tex texlive-dvips
BuildRequires: java-devel-openjdk gcc-gfortran
# /usr/bin/g77 is not in RHEL7
%if !0%{?rhel}
%ifnarch %{arm}
# g77 is also not present on arm systems
BuildRequires: /usr/bin/g77
%endif
%endif
BuildRequires: dejagnu expect emacs imake python-docutils vala
BuildRequires: cscope ncompress sharutils help2man
BuildRequires: gcc-objc gcc-objc++
%if !0%{?rhel:1}
# gcc-java was disabled in RHEL >= 7
BuildRequires: gcc-java python-virtualenv lzip
%endif
%endif

# the filtering macros are currently in /etc/rpm/macros.perl:
BuildRequires: perl-macros

# remove bogus Automake perl dependencies and provides
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Automake::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Automake::

Prefix: %{_prefix}

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles.

%prep
%setup -q -n automake-%{version}
%patch0 -p1 -b .disable_tests
autoreconf -iv

# Fedora only to add ppc64p7 (Power7 optimized) arch:
perl -pi -e "s/ppc64-\*/ppc64-\* \| ppc64p7-\*/" lib/config.sub

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
   --bindir=%{_bindir} --datadir=%{_datadir} --libdir=%{_libdir} \
   --docdir=%{_docdir}/%{name}-%{version} --disable-silent-rules
make V=0 %{?_smp_mflags}
cp m4/acdir/README README.aclocal
cp contrib/multilib/README README.multilib

%install
make install DESTDIR=%{buildroot}

sed -i 's|/usr/bin/perl|%{_bindir}/perl|g' %{buildroot}%{_bindir}/*

%files
%license COPYING*
%exclude %{_datadir}/aclocal
%{_bindir}/*
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
%exclude %{_infodir}
%exclude %{_mandir}
%exclude %{_docdir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.13.4-3
- Mass rebuild 2013-12-27

* Tue Nov 05 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.4-2
- don't BR g77 in arm and RHEL build roots (#1023781)

* Mon Jun 17 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.4-1
- update to automake 1.13.4

* Thu May 16 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.2-1
- update to automake 1.13.2 (#963556), remove (now) redundant patches

* Thu May 02 2013 Petr Hracek <phracek@redhat.com> - 1.13.1-18
- Patch pax hang up with big UID corrected on the base of upstream(#843379)

* Wed Apr 24 2013 Petr Hracek <phracek@redhat.com> - 1.13.1-17
- Patch pax hang up with big UID was removed(#843379)

* Wed Apr 24 2013 Petr Hracek <phracek@redhat.com> - 1.13.1-16
- configure stops when run by big UID (#843379)

* Thu Apr 11 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-15
- tune %%check to show testsuite.log when failed

* Tue Apr 02 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-14
- fix another requirement on perl package which may cause problems in future,
  thanks to Paul Howarth (#924938)
- f-r: remove Buildroot tag, fix license tag

* Mon Mar 18 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-13
- remove old build dependency comment
- fix bogus dates in changelog
- use the %%{_smp_mflags} also by `make check`

* Mon Mar 18 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-11
- do not BR gcc-java in RHEL (change C&Ped from libtool)

* Sun Mar 10 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-10
- add the 'perl(Thread::Queue)' dependency (#919810)

* Sat Feb 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.1-9
- Bump build for ARM

* Fri Feb 22 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-8
- update the patch for the non-existent 'm4' directory issue to the one already
  committed in upstream repository

* Thu Feb 21 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-7
- do not run 'autoreconf --force' (#913279)

* Wed Feb 20 2013 Karsten Hopp <karsten@redhat.com> 1.13.1-6
- add support for ppc64p7 arch (Power7 optimized)

* Thu Feb 14 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-5
- Do not fail in aclocal when the first include directory does not exist
  (#901333)
- do not require texlive-latex-fonts (rawhide texinfo repaired)
- use macros in Patch statements

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-3
- re-enable AM_CONFIG_HEADER macro in Fedora distribution (#896442)
- disable testing for non-existence of this macros (join with vala)

* Mon Jan 14 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-2
- allow to run bigger subset of tests in testsuite

* Sat Jan 12 2013 Pavel Raiskup <praiskup@redhat.com> - 1.13.1-1
- update to recent automake-1.13.1
- minimum required autoconf is 2.65 (based on upstream suggestion)
- make check is run now parallel (based on 't/README' it helps also on
  single-thread machines)
- drop old sleep-patch and better disable vala tests (requires autoreconf)
- add temporary BR dependency on texlive-latex-fonts for rawhide (f19 only)
  (should be implicitly pulled by texlive-dvips probably)

* Thu Oct 25 2012 Pavel Raiskup <praiskup@redhat.com> - 1.12.2-6
- fedora-review -> s/define/global/, s/RPM_BUILD_ROOT/buildroot/,
  remove defattr() from %%files section

* Wed Sep 26 2012 Pavel Raiskup <praiskup@redhat.com> - 1.12.2-5
- rather skip failing tests than disabling - previous solution required
  autoreconf (#860577)

* Wed Sep 26 2012 Pavel Raiskup <praiskup@redhat.com> - 1.12.2-4
- ups, forgot to add patch for (#860577)

* Wed Sep 26 2012 Pavel Raiskup <praiskup@redhat.com> - 1.12.2-3
- temporarily disable vala checks in testsuite because of vala rebase to
  vala-0.18.0 (#860577)

* Tue Sep 25 2012 Pavel Raiskup <praiskup@redhat.com> - 1.12.2-3
- Thanks to Ralf Corsépius <corsepiu@fedoraproject.org> - these fixes are
  slightly reworked changes (due to rebase of automake) from his patch attached
  to bug #823766
- Include COPYING.
- Add rpm-4.9 perl-filters %%__provides_exclude, %%__requires_exclude.
  Remove rpm-4.8 perl-filters (Address RHBZ 823766).
- Remove utf-8 conversion of NEWS (Already utf-8 encoded).
- Add BR: perl-macros, Remove BR: perl-devel.
- Add support for --with/out=check.
- Append --disable-silent-rules to configure.
- remove trailing white spaces

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Karsten Hopp <karsten@redhat.com> 1.12.2-1
- automake-1.12.2

* Mon Apr 16 2012 Karsten Hopp <karsten@redhat.com> 1.11.5-1
- automake-1.11.5

* Tue Apr 03 2012 Karsten Hopp <karsten@redhat.com> 1.11.4-1
- automake-1.11.4

* Thu Feb 02 2012 Karsten Hopp <karsten@redhat.com> 1.11.3-1
- automake 1.11.3

* Mon Jan 30 2012 Karsten Hopp <karsten@redhat.com> 1.11.2-1
- automake 1.11.2, enable all checks again

* Wed Dec 07 2011 Karsten Hopp <karsten@redhat.com> 1.11.1-7
- disable some erroneous checks (660739, 756957)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 29 2010 Karsten Hopp <karsten@redhat.com> 1.11.1-5
- removed redundant text about installing autoconf from package
  description (#225302)
- don't create /usr/share/aclocal as it is owned be the filesystem
  package (#570744, #225302)

* Fri Mar 05 2010 Karsten Hopp <karsten@redhat.com> 1.11.1-4
- Directory /usr/share/aclocal now owned by filesystem
   (#570744)

* Tue Mar  2 2010 Stepan Kasal <skasal@redhat.com> - 1.11.1-3
- use perl filtering macros

* Tue Mar 02 2010 Karsten Hopp <karsten@redhat.com> 1.11.1-2
- better method of fixing the perl requires/provides (Paul Howarth, #225302)
- fix variable usage in spec file (#225302)
- use pregenerated manpages from automake-1.11 (#225302)
- update URL (#225302)

* Wed Dec 09 2009 Karsten Hopp <karsten@redhat.com> 1.11.1-1
- update to version 1.11.1 to fix CVE-2009-4029

* Tue Dec 01 2009 Karsten Hopp <karsten@redhat.com> 1.11-6
- preserve time stamps of man pages (#225302)
- drop MIT from list of licenses

* Wed Nov  4 2009 Stepan Kasal <skasal@redhat.com> - 1.11-5
- add even more testsuite build requires

* Wed Nov  4 2009 Stepan Kasal <skasal@redhat.com> - 1.11-4
- add build requires for testsuite

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Stepan Kasal <skasal@redhat.com> 1.11-2
- re-enable make check
- Automake 1.11 requires autoconf 2.62 or later

* Mon May 25 2009 Karsten Hopp <karsten@redhat.com> 1.11-1
- update to automake 1.11

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Karsten Hopp <karsten@redhat.com> 1.10.2-2
- convert NEWS file to UTF-8 (#225302)

* Wed Jan 14 2009 Karsten Hopp <karsten@redhat.com> 1.10.2-1
- version 1.10.2

* Mon Feb  4 2008 Stepan Kasal <skasal@redhat.com> 1.10.1-2
- require autoconf 2.60 or later

* Sat Jan 26 2008 Stepan Kasal <skasal@redhat.com> 1.10.1-1
- automake-1.10.1

* Mon Oct 29 2007 Stepan Kasal <skasal@redhat.com> 1.10-7
- keep amhello-1.0.tar.gz in the installed documentation

* Thu Aug 09 2007 Karsten Hopp <karsten@redhat.com> 1.10-6
- update license tag
- add Debian man pages for aclocal and automake (#246087)

* Tue Feb 20 2007 Karsten Hopp <karsten@redhat.com> 1.10-5
- fix some rpmlint warnings

* Tue Feb 20 2007 Karsten Hopp <karsten@redhat.com> 1.10-4
- bz 225302:
- make install DESTDIR=...
- fix BuildRoot
- fix post/preun requirements
- define all directories on ./configure line
- filter perl(Automake*) dependencies
- replace all tabs with spaces
- remove trailing dot from summary

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 1.10-3
- don't abort (un)install scriptlets when _excludedocs is set (Ville Skyttä)

* Tue Nov 21 2006 Karsten Hopp <karsten@redhat.com> 1.10-2
- rebuild

* Fri Nov 10 2006 Karsten Hopp <karsten@redhat.de> 1.10-1
- automake 1.10

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.9.6-2.1
- rebuild

* Mon Dec 19 2005 Karsten Hopp <karsten@redhat.de> 1.9.6-2
- include NEWS file (#174674)
- add %%check (#174674)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Karsten Hopp <karsten@redhat.de> 1.9.6-1
- Automake 1.9.6

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com>
- 1.9.5 bug-fix release

* Tue Feb  1 2005 Daniel Reed <djr@redhat.com> 1.9.4-1
- version bump
  - Portability nits in install-sh and mdata-sh.
  - Don't let `make install' fails if a _JAVA primary becomes empty
    because of conditionals.
  - Do not confuse CHANGELOG with ChangeLog on case-insensitive
    case-preserving file systems (likewise for all automatically
    distributed files).
  - Do not embed $DESTDIR in Python's byte-code files.
  - Work around programs that read stdin when checking for --version
    and --help options (when the `std-options' is used).
  - Fix AM_PATH_PYTHON to correctly define PYTHON as `:' when no minimum
    version was supplied and no interpreter is found.

* Mon Nov  1 2004 Daniel Reed <djr@redhat.com> 1.9.3-1
- version bump
  - Dependency tracking using mode "dashmstdout" or "dashXmstdout" did not work for libtool objects compiled with --tag (i.e., compiled with Libtool 1.5 or later). The compilation would succeed, but `depcomp' would emit a warning and not output any dependency information.
  - Ignore comments from augmented variables ...
  - `install-sh -d a/b/' failed to create `a/b/' because of the trailing `/'.
  - _PROGRAMS now always create programs. Before 1.9 it would mistakenly create a libtool library if the name of the program ended in `.la'.
  - `compile' now handles `*.obj' objects.
  - `aclocal' recognizes AC_DEFUN_ONCE.

* Tue Sep 28 2004 Warren Togami <wtogami@redhat.com> - 1.9.2-3
- trim docs

* Mon Sep 20 2004 Daniel Reed <djr@redhat.com> - 1.9.2-1
- version bump
  - Sort rm commands output for mostlyclean-generic, clean-generic, distclean-generic and maintainer-clean-generic, so that the produced Makefile is not sensitive to the way Perl sorts its hashes.
  - Support `+' in the name of directories given to `include'.
  - Preserve spaces in the arguments of `compile'.
  - `missing' will no longer try to emulate a tool that is run with `--version' or `--help' as argument.
  - There is a new chapter about the history of Automake.

* Wed Aug 11 2004 Daniel Reed <djr@redhat.com> - 1.9.1-1
- version bump
  - Adjust #line directives in `parser.h' (when ylwrap is not used). (PR/432)
  - Fix definition of YLWRAP when ylwrap is installed in a default aux directory found in a parent package.
  - Properly recognize AC_CANONICAL_BUILD and AC_CANONICAL_TARGET.

* Fri Jul 30 2004 Daniel Reed <djr@redhat.com> - 1.9-1
- version bump

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 17 2004 Jens Petersen <petersen@redhat.com> - 1.8.5-1
- update to 1.8.5

* Thu May 13 2004 Jens Petersen <petersen@redhat.com> - 1.8.4-1
- update to 1.8.4

* Fri Mar 12 2004 Jens Petersen <petersen@redhat.com> - 1.8.3-1
- update to 1.8.3 bugfix release

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 13 2004 Jens Petersen <petersen@redhat.com> - 1.8.2-1
- 1.8.2 bugfix release
- do not pass VERBOSE=xNO to "make check" as non-empty means be verbose

* Thu Dec 11 2003 Jens Petersen <petersen@redhat.com> - 1.8-1
- update to 1.8 release
- require autoconf 2.58 or later
- don't use %%configure for now to prevent very recent configure from running
  "config.sub noarch-redhat-linux"

* Mon Nov 10 2003 Jens Petersen <petersen@redhat.com> - 1.7.9-1
- update to 1.7.9 bugfix release
- require autoconf 2.54 or later

* Tue Oct  7 2003 Jens Petersen <petersen@redhat.com> - 1.7.8-1
- update to 1.7.8 bugfix release

* Wed Sep 10 2003 Jens Petersen <petersen@redhat.com> - 1.7.7-1
- update to 1.7.7 bugfix release

* Fri Jul 11 2003 Jens Petersen <petersen@redhat.com> - 1.7.6-1
- update to 1.7.6 bugfix release

* Tue May 20 2003 Jens Petersen <petersen@redhat.com> - 1.7.5-1
- update to 1.7.5 bugfix release

* Thu Apr 24 2003 Jens Petersen <petersen@redhat.com> - 1.7.4-1
- update to 1.7.4

* Thu Mar  6 2003 Jens Petersen <petersen@redhat.com> - 1.7.3-1
- update to 1.7.3
- python dir lib64 patch no longer needed
- build requires Autoconf 2.54 or later

* Mon Jan 27 2003 Jens Petersen <petersen@redhat.com> - 1.6.3-5
- patch from 1.7-branch to try python distutils for setting pythondir (#80994)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 1.6.3-3
- Fix unpackaged file

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com> 1.6.3-2
- add "--without check" rpmbuild option to switch "make check" off
- exclude info dir file
- don't gzip info files explicitly

* Mon Nov 18 2002 Jens Petersen <petersen@redhat.com>
- use api_version in version

* Mon Jul 29 2002 Jens Petersen <petersen@redhat.com> 1.6.3-1
- bug fix release 1.6.3

* Thu Jul 11 2002 Jens Petersen <petersen@redhat.com> 1.6.2-2
- add buildrequires autoconf 2.52 or greater [reported by Edward Avis]

* Wed Jun 19 2002 Jens Petersen <petersen@redhat.com> 1.6.2-1
- 1.6.2 (bug fix release)
- do "make check" after building

* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.6.1-2
- automated rebuild

* Tue Apr 23 2002 Jens Petersen <petersen@redhat.com> 1.6.1-1
- 1.6.1

* Tue Mar 12 2002 Jens Petersen <petersen@redhat.com> 1.6-1
- new package based on automake15
- 1.6

* Wed Jan 23 2002 Jens Petersen <petersen@redhat.com> 1.5-8
- better aclocal versioning

* Wed Jan 23 2002 Jens Petersen <petersen@redhat.com> 1.5-7
- don't version datadir/automake

* Tue Jan 15 2002 Jens Petersen <petersen@redhat.com> 1.5-6
- version suffix programs and data directories
- own symlinks to programs and /usr/share/aclocal

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.5-5
- automated rebuild

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-4
- Completely back out the fix for #56624 for now, it causes more problems
  than it fixes in either form.

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-3
- Don't use AS_DIRNAME, it doesn't work.

* Tue Jan  8 2002 Jens Petersen <petersen@redhat.com> 1.5-2
- Patch depout.m4 to handle makefiles passed to make with "-f" (#56624)

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-1
- Update to 1.5 - much better to coexist with autoconf 2.52...
- Fix specfile
- No patches

* Fri Aug 24 2001 Jens Petersen <petersen@redhat.com> - 1.4p5-2
- dont raise error when there is source in a subdirectory (bug #35156).
  This was preventing automake from working in binutuls/gas
  [patch from HJ Lu <hjl@gnu.org>]
- format long lines of output properly with backslash + newlines as in 1.4
  (bug #35259) [patch from HJ Lu <hjl@gnu.org>]

* Sat Jul 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.4-p5, fixes #48788

* Tue Jun 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add the patch from #20559
- really update to 1.4-p4

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.4-p4

* Sat May 12 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.4-p1 to work with libtool-1.4

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #8870

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- revert to pristine automake-1.4.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)
