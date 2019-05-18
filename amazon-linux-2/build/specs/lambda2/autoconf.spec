Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.69
Release:    11%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
Source0:    http://ftpmirror.gnu.org/autoconf/autoconf-%{version}.tar.xz
Source1:    config.site
URL:        http://www.gnu.org/software/autoconf/
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# run "make check" by default
%bcond_without check

# m4 >= 1.4.6 is required, >= 1.4.14 is recommended:
BuildRequires:      m4 >= 1.4.14
Requires:           m4 >= 1.4.14
BuildRequires:      emacs
# the filtering macros are currently in /etc/rpm/macros.perl:
BuildRequires:      perl-macros
BuildRequires:      perl(Data::Dumper)
# from f19, Text::ParseWords is not the part of 'perl' package
BuildRequires:      perl(Text::ParseWords)

%if %{with check}
# For extended testsuite coverage
BuildRequires:      gcc-gfortran
%if 0%{?fedora} >= 15
BuildRequires:      erlang
%endif
%endif

# filter out bogus perl(Autom4te*) dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Autom4te::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Autom4te::

Prefix: %{_prefix}

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q

%build
%configure
# not parallel safe
make

%files
%license COPYING*
%{_bindir}/*
%{_datadir}/autoconf/
%dir %{_datadir}/emacs/
%{_datadir}/emacs/site-lisp/
%exclude %{_infodir}
%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.69-11
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Pavel Raiskup <praiskup@redhat.com> - 2.69-10
- BR the perl(Text::ParseWords) explicitly to enable build again

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.69-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Pavel Raiskup <praiskup@redhat.com> - 2.69-9
- disable 'config.site' under /usr/share for now

* Tue Jan 15 2013 Pavel Raiskup <praiskup@redhat.com> - 2.69-8
- the 'INSTALL' file can be used as template file for packages which are using
  autoconf - mark it for installation again (#661623)

* Tue Jan 08 2013 Pavel Raiskup <praiskup@redhat.com> - 2.69-7
- Support the 'config.site' file in /usr/share

* Thu Oct 25 2012 Pavel Raiskup <praiskup@redhat.com> - 2.69-6
- fedora-review (minor) fixes and typos: trim lines, remove defattr(,,), do not
  run `rm -rf %%{buildroot} at the beginning of install section, use curly
  brackets only around rpm macros/variables and not around shell variables,
  remove clean section

* Wed Sep 26 2012 Pavel Raiskup <praiskup@redhat.com> - 2.69-5
- do not install the "INSTALL" documentation file (#661623)

* Thu Sep 13 2012 Karsten Hopp <karsten@redhat.com> 2.69-4
- don't require erlang in RHEL

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Karsten Hopp <karsten@redhat.com> 2.69-2
- spec file changes by Ralf Corsépius:
- Use %%bcond_without for --with/out=check.
- Add BR: perl(Data::Dumper).
- Remove BR: automake (Testsuite doesn't need automake).
- Add BR: gcc-gfortran, erlang (Extend testsuite).
- Remove TESTSUITEFLAGS (Was referring to autoconf < 2.69).
- Add rpm-4.9 perl-filters %%__provides_exclude, %%__requires_exclude.
  Remove rpm-4.8 perl-filters (Address RHBZ 823770).
- Reflect autoconf being GPLv3'ed.
- Add BR: perl-macros, Remove BR: perl-devel

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 2.69-1
- update to 2.69

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Karsten Hopp <karsten@redhat.com> 2.68-1
- update to 2.68

* Tue Jul 06 2010 Karsten Hopp <karsten@redhat.com> 2.66-2
- add 2 upstream patches (#611661)
- allow rpmbuild --without check

* Mon Jul  5 2010 Stepan Kasal <kasal@ucw.cz> - 2.66-1
- new upstream version, drop upstreamed patches

* Tue Mar  2 2010 Stepan Kasal <skasal@redhat.com> - 2.65-2
- use perl filtering macros

* Wed Nov 25 2009 Stepan Kasal <skasal@redhat.com> - 2.65-1
- new upstream version
- backported patch: make AC_FUNC_MMAP work with C++ again

* Tue Nov 24 2009 Stepan Kasal <skasal@redhat.com> - 2.64-2
- add back upstream AH_CHECK_HEADERS, backported from upstream
  fixes some build failures

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 2.64-1
- new upstream version
- skip failing test

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.63-4
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 17 2008 Stepan Kasal <skasal@redhat.com> 2.63-1
- upstream bugfix release
- all patches dropped, the issues are fixed upstream

* Mon Jul 07 2008 Karsten Hopp <karsten@redhat.com> 2.62-5
- fix multiline variables (p.e. #449467)

* Fri Jul  4 2008 Stepan Kasal <skasal@redhat.com> 2.62-4
- add a quick fix for #449944
- remove Requires: mktemp, imake, grep; these are required by the generated
  configure, but not by Autoconf.
- switch on make check

* Tue Jun 24 2008 Karsten Hopp <karsten@redhat.com> 2.62-3
- add fix for same line comments #449245 (Ralf Wildenhues)

* Fri Jun 06 2008 Karsten Hopp <karsten@redhat.com> 2.62-2
- add upstream fix from Eric Blake for #449973,
  m4_if releated error message from autotest

* Tue May 13 2008 Karsten Hopp <karsten@redhat.com> 2.62-1
- autoconf-2.62

* Mon Oct 29 2007 Stepan Kasal <skasal@redhat.com> 2.61-10
- require m4 >= 1.4.7
- Resolves: #236073

* Wed Aug 08 2007 Karsten Hopp <karsten@redhat.com> 2.61-9
- update license tag

* Tue Feb 27 2007 Karsten Hopp <karsten@redhat.com> 2.61-8
- own %%{_datadir}/emacs/ (#225296)

* Mon Feb 26 2007 Karsten Hopp <karsten@redhat.com> 2.61-7
- add Requires: grep

* Thu Feb 22 2007 Karsten Hopp <karsten@redhat.com> 2.61-6
- drop gawk, sed requirements (#225296)
- add some comments

* Mon Feb 19 2007 Karsten Hopp <karsten@redhat.com> 2.61-5
- use ./configure
- filter dependencies

* Thu Feb 15 2007 Karsten Hopp <karsten@redhat.com> 2.61-4
- add disttag
- replace  tabs with spaces
- fix buildroot
- use Requires(post), Requires(preun)
- use make install DESTDIR=....
- drop perl requirement as it gets pulled it automatically

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 2.61-3
- don't abort (un)install scriptlets when _excludedocs is set (Ville Skyttä)

* Tue Nov 21 2006 Karsten Hopp <karsten@redhat.com> 2.61-2
- drop obsolete linkX11 patch

* Tue Nov 21 2006 Karsten Hopp <karsten@redhat.com> 2.61-1
- autoconf-2.61

* Thu Nov 09 2006 Karsten Hopp <karsten@redhat.com> 2.60-4
- autoconf-2.60

* Fri Oct 13 2006 Stepan Kasal <skasal@redhat.com> 2.59-12
- Add autoconf-2.59-lock.patch to eliminate a perl warning (#210653).

* Thu Jul 27 2006 Karsten Hopp <karsten@redhat.de> 2.59-11
- Requires imake for _AC_PATH_X

* Thu Jul 20 2006 Karsten Hopp <karsten@redhat.de> 2.59-10
- rebuild

* Wed Jul 19 2006 Karsten Hopp <karsten@redhat.de> 2.59-9
- rebuild

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 2.59-8
- try to link with libX11 instead of libXt

* Wed Feb 15 2006 Karsten Hopp <karsten@redhat.de> 2.59-7
- XrmInitialize takes no argument (#181340)

* Mon Feb 06 2006 Karsten Hopp <karsten@redhat.de> 2.59-6
- check for Xlib.h instead of Intrinsic.h to find X11 headers
  (#176379)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep 21 2004 Daniel Reed <djr@redhat.com> - 2.59-5
- rebuilt for dist-fc3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 18 2003 Jens Petersen <petersen@redhat.com> - 2.59-2
- rebuild with perl-5.8.2 [Harald Hoyer]

* Thu Nov 13 2003 Jens Petersen <petersen@redhat.com> - 2.59-1
- update to 2.59 bugfix release
- remove autoconf-2.58-fix-ac_abs-109267.patch no longer needed

* Fri Nov  7 2003 Jens Petersen <petersen@redhat.com> - 2.58-2
- fix problem with ac_abs_{build,src}dir (#109267) [reported by Joe Orton,
  patch by Alexandre Duret-Lutz]

* Wed Nov  5 2003 Jens Petersen <petersen@redhat.com> - 2.58-1
- 2.58 release

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.57-2
- Fix missing/unpackaged file

* Thu Dec  5 2002 Jens Petersen <petersen@redhat.com> 2.57-1
- update to 2.57 bugfix release
- buildrequire emacs (#79031), sed and m4

* Sat Nov 23 2002 Jens Petersen <petersen@redhat.com> 2.56-2
- add --without check build option to control whether "make check" run
- don't gzip info files explicitly
- use exclude for unwanted info files

* Thu Nov 21 2002 Jens Petersen <petersen@redhat.com>
- no longer obsolete autoconf253

* Mon Nov 18 2002 Jens Petersen <petersen@redhat.com> 2.56-1
- update to 2.56
- obsolete autoheader-warn patch
- no longer provide autoconf253
- include site-lisp and man files
- remove info dir which is not in the manifest
- do not version suffix bin files for now

* Mon Aug 19 2002 Jens Petersen <petersen@redhat.com> 2.53-8
- make check

* Fri Jun 28 2002 Jens Petersen <petersen@redhat.com> 2.53-7
- update url (#66840)
- added doc files

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.53-6
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 2.53-5
- automated rebuild

* Mon May 20 2002 Bill Nottingham <notting@redhat.com> 2.53-4
- provide autoconf253

* Thu May 16 2002 Bill Nottingham <notting@redhat.com> 2.53-3
- obsolete autoconf253

* Wed May  8 2002 Jens Petersen <petersen@redhat.com> 2.53-2
- patch autoheader so that --warnings=CATEGORY works (#64566)
  [reported with fix by hjl@gnu.org]

* Tue Apr 23 2002 Jens Petersen <petersen@redhat.com> 2.53-1
- update to autoconf-2.53
- drop mawk patch again
- version suffix bindir files and add symlinks to unversioned names

* Fri Feb  1 2002 Jens Petersen <petersen@redhat.com> 2.52-7
- revert to 2.52 (also fixes #58210!)
- remove relversion variable
- bring back mawk -> gawk patch

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.52-6
- automated rebuild

* Thu Dec 20 2001 Jens Petersen <petersen@redhat.com> 2.52-5
- update to 2.52f
- add URL
- minor description improvements
- define relversion to carry version number
- mawk.patch no longer needed

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de> 2.52-4
- rebuild

* Wed Sep 19 2001 Jens Petersen <petersen@redhat.com> 2.52-3
- restore patch to prefer gawk to mawk

* Tue Sep 18 2001 Florian La Roche <Florian.LaRoche@redhat.de> 2.52-2
- update to 2.52d

* Mon Sep 17 2001 Jens Petersen <petersen@redhat.com> 2.52-1
- update to 2.52
- remove obsolete patches, since already new version
- dont install install-sh

* Tue Jul 10 2001 Jens Petersen <petersen@redhat.com>
- add patch to include various standard C headers as needed
  by various autoconf tests (#19114)
- add patch to autoscan.pl to get a better choice of init
  file (#42071), to test for CPP after CC (#42072) and to
  detect C++ source and g++ (#42073).

* Tue Jun 26 2001 Jens Petersen <petersen@redhat.com>
- Add a back-port of _AC_PROG_CXX_EXIT_DECLARATION
  from version 2.50 to make detection of C++ exit()
  declaration prototype platform independent.  The check is
  done in AC_PROG_CXX with the result stored in "confdefs.h".
  The exit() prototype in AC_TRY_RUN_NATIVE is no longer needed.
  (fixes #18829)

* Wed Nov 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up interoperability with glibc 2.2 and gcc 2.96:
  AC_TRY_RUN_NATIVE in C++ mode added a prototype for exit() to
  the test code without throwing an exception, causing a conflict
  with stdlib.h --> AC_TRY_RUN_NATIVE for C++ code including stdlib.h
  always failed, returning wrong results

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- add textutils as a dependency (#14439)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix preun

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to help autoconf clean after itself and not leave /tmp clobbered
  with acin.* and acout.* files (can you say annoying?)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)
- use gawk, not mawk

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- moved /usr/lib/autoconf to /usr/share/autoconf (with automake)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.13.

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- requires perl

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- patch for fixing /tmp race conditions

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups
- made a noarch package
- uses autoconf
- uses install-info

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built with glibc
