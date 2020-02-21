# -*- coding: utf-8 -*-
Summary: A GNU tool which simplifies the build process for users
Name: make
Epoch: 1
Version: 3.82
Release: 24%{?dist}
License: GPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/make/
Source: ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2

Patch1: make-3.82-noclock_gettime.patch
Patch2: make-3.82-j8k.patch
Patch3: make-3.82-getcwd.patch
Patch4: make-3.82-err-reporting.patch

# Upstream: https://savannah.gnu.org/bugs/?30748
Patch6: make-3.82-weird-shell.patch

Patch7: make-3.82-newlines.patch
Patch8: make-3.82-jobserver.patch

# Upstream: https://savannah.gnu.org/bugs/?30612
# Upstream: https://savannah.gnu.org/bugs/?30723
Patch9: make-3.82-bugfixes.patch

Patch10: make-3.82-sort-blank.patch
Patch11: make-3.82-copy-on-expand.patch

# Upstream: https://savannah.gnu.org/bugs/?33873
Patch12: make-3.82-parallel-remake.patch

# http://savannah.gnu.org/bugs/?34335
Patch13: make-3.82-warn_undefined_function.patch

# http://lists.gnu.org/archive/html/bug-make/2011-06/msg00032.html
Patch14: make-3.82-trace.patch

# http://lists.gnu.org/archive/html/bug-make/2011-04/msg00002.html
Patch15: make-3.82-expensive_glob.patch

# Upstream: https://savannah.gnu.org/bugs/?30653
Patch16: make-3.82-dont-prune-intermediate.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=926115
Patch17: make-3.82-aarch64.patch

# Additional fix for https://savannah.gnu.org/bugs/?30612
Patch18: make-3.82-empty-members.patch

# Can't use a stem and a glob in the same dependency.
# https://savannah.gnu.org/bugs/?39310
# https://bugzilla.redhat.com/show_bug.cgi?id=987672
Patch19: make-3.82-stem_glob.patch

# Stack limit not restored for processes spawned through $(shell)
# https://savannah.gnu.org/bugs/index.php?39851
Patch20: make-3.82-func_shell-rlimit.patch

# This to make the test targets/SECONDARY deterministic.  The above
# patch causes this to occasionally fail.
Patch21: make-3.82-tests-SECONDARY.patch

# BZ 1323206
# Check if the target-specific variable is the same as the global
# variable, and if it is, don't free it.  Savannah bug #31743.
Patch22: make-3.82-var.patch

# BZ 1322670
# In very obscure situations we may write the free token back to the pipe.
Patch23: make-3.82-jobserver-tokens.patch

# BZ 1582545
# A mix of explicit and implicit targets (in that order) in the same
# rule is no longer fatal (but still deprecated).
Patch24: make-3.82-mixed-implicit.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: procps

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p0
%patch13 -p2
%patch14 -p1
%patch15 -p0
%patch16 -p0
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

rm -f tests/scripts/features/parallelism.orig

%build
%configure
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/gmake.1
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang %name

%check
echo ============TESTING===============
/usr/bin/env LANG=C make check
echo ============END TESTING===========

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if [ -f %{_infodir}/make.info.gz ]; then # for --excludedocs
   /sbin/install-info %{_infodir}/make.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility." || :
fi

%preun
if [ $1 = 0 ]; then
   if [ -f %{_infodir}/make.info.gz ]; then # for --excludedocs
      /sbin/install-info --delete %{_infodir}/make.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility." || :
   fi
fi

%files  -f %{name}.lang
%defattr(-,root,root)
%doc NEWS README COPYING AUTHORS
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*

%changelog
* Wed Dec 05 2018 DJ Delorie <dj@redhat.com> - 1:3.82-24
- Change fatal() to error() when a mix of explicit and implicit
  targets (in that order) is detected.
  Resolves: #1582545

* Thu Jul 07 2016 Patsy Franklin <pfrankli@redhat.com> - 1:3.82-23
- In very obscure situations we may incorrectly write the free token
  back to the pipe.
  Resolves: #1322670

* Thu Jun 30 2016 Patsy Franklin <pfrankli@redhat.com> - 1:3.82-22
- Check if the target-specific variable is the same as the global
  variable, and if it is, don't free it.  Savannah bug #31743.
  Resolves: #1323206

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:3.82-21
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:3.82-20
- Mass rebuild 2013-12-27

* Thu Aug 22 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-19
- make now restores rlimit to its original values before launching
  subprocess via $(shell) (make-3.82-func_shell-rlimit.patch)
- Determinize one test (make-3.82-tests-SECONDARY.patch)

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-18
- Backport upstream patch that adds wildcard expansion to pattern
  rules. (make-3.82-stem_glob.patch)

* Wed Jun 19 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-17
- Add another fix for upstream bug 30612

* Thu Apr  4 2013 Petr Machata <pmachata@redhat.com> - 1:3.82-16
- Update config.sub and config.guess to support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-14
- Drop patch5, which hasn't been applied for years

* Mon Sep 10 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-13
- Add fix for upstream bug 30653
- Resolves: #835424

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-11
- Add a patch for avoiding glob if possible by Michael Meeks

* Mon Mar 12 2012 Petr Machata <pmachata@redhat.com> - 1:3.82-10
- Apply the following patches, proposed upstream by Norbert Thiebaud:
  - A patch for warning on call of undefined function
  - A patch for tracing calls to "eval" and "call"

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov  3 2011 Petr Machata <pmachata@redhat.com> - 1:3.82-8
- Add a patch for preserving -j across Makefile rebuild
- Resolves: #698702

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-7
- Rebuilt for glibc bug#747377

* Tue May 12 2011 Lubomir Rintel <lkundrak@v3.sk> - 1:3.82-6
- Fix free-after-use with nested assignments (#703104)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.82-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Petr Machata <pmachata@redhat.com> - 1:3.82-4
- Fix a discrepancy between behavior of find_next_token and
  pre-allocation of token memory in func_sort.
- Resolves: #643359

* Wed Sep 29 2010 jkeating - 1:3.82-3
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Petr Machata <pmachata@redhat.com> - 1:3.82-2
- Add upstream fixes for upstream bugs 30612 and 30723
- Resolves: #631552

* Wed Aug 11 2010 Petr Machata <pmachata@redhat.com> - 1:3.82-1
- Upstream 3.82:
  - Drop rlimit, fdleak, strcpy-overlap, recursion-test, double-free
    patches, make supports this functionality now
  - Disable the memory patch for the time being
  - Port remaining patches
  - Add weird-shell patch, upstream bug 30748
- Resolves: #618998

* Wed Aug 11 2010 Petr Machata <pmachata@redhat.com> - 1:3.81-21
- Add BR procps
- Resolves: #616813

* Thu Jul  1 2010 Petr Machata <pmachata@redhat.com> - 1:3.81-20
- Add a patch by Steve Kemp @debian that might fix the double free
  problem.
- Related: #609806

* Fri Jun  4 2010 Petr Machata <pmachata@redhat.com> - 1:3.81-19
- Fix testsuite on F13
- Resolves: #600004

* Tue Aug 11 2009 Petr Machata <pmachata@redhat.com> - 1:3.81-18
- Fix installation with --excludedocs
- Resolves: #515917

* Fri Jul 31 2009 Petr Machata <pmachata@redhat.com> - 1:3.81-17
- Replace the use of strcpy on overlapping areas with memmove
- Resolves: #514721

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.81-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.81-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Petr Machata <pmachata@redhat.com> - 1:3.81-14
- Fix patches to apply cleanly with fuzz=0

* Tue Sep 16 2008 Petr Machata <pmachata@redhat.com> - 1:3.81-13
- Mark opened files as cloexec to prevent their leaking through fork
- Resolves: #462090

* Tue Mar 25 2008 Petr Machata <pmachata@redhat.com> - 1:3.81-12
- Fix the rlimit patch.  The success flag is kept in memory shared
  with parent process after vfork, and so cannot be reset.
- Related: #214033

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.81-11
- Autorebuild for GCC 4.3

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-10
- Fix parallel builds with reexec.
- Related: #212111, #211290

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-8
- Cleaned up per merge review.
- Related: #226120

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-7
- Fix licensing tag.

* Fri Mar 16 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-6
- Always run testsuite with C locale.
- Resolves: #232607

* Thu Feb 22 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-5
- Fix newline handling for quoted SHELL.
- Resolves: #219409

* Fri Feb  2 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-4
- Tidy up the specfile per rpmlint comments
- Use utf-8 and fix national characters in contributor's names

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-3
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223709

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 1:3.81-2
- make now restores rlimit to its original values before launching
  subprocess (#214033)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.81-1.1
- rebuild

* Tue May 23 2006 Petr Machata <pmachata@redhat.com> - 1:3.81-1
- Upstream 3.81:
  - Contains several backwards incompatible changes.  See NEWS inside
    the source package to find out more.
- memory patch and error reporting patch were ported to this version.

* Wed Mar 15 2006 Petr Machata <pmachata@redhat.com> 1:3.80-11
- Applied (five years old) patch from Jonathan Kamens to allow make to
  handle several pattern-specific variables (#52962).

  The patch was changed so that it forces make to process pattern
  specific variables in the same order as they appear in file.
  (Upstream make behaves this way, too.)  This is change from old make
  behavior, which processed the variables in reverse order.  In case
  you used only x=a assignments, this had the effect of using the
  first pattern specific variable that matched.  For x+=a this just
  doesn't work, and it produces absolutely nonintuitive results.

- (It would be great if make's target-specific variables were handled
  the same way as pattern-specific ones, just without the pattern
  component.  However current handling is documented and considered a
  feature.)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.80-10.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.80-10.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 02 2006 Petr Machata <pmachata@redhat.com> 3.80-10
- H.J. Lu caught a typo in the patch and provided a new one. (#175376)

* Mon Jan 09 2006 Petr Machata <pmachata@redhat.com> 3.80-9
- Applied patch from H.J. Lu.  Somehow reduces make's enormous memory
  consumption. (#175376)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 22 2005 Jakub Jelinek <jakub@redhat.com> 3.80-8
- make sure errno for error reporting is not lost accross _() calls
- report EOF on read pipe differently from read returning < 0 reporting

* Mon Mar  7 2005 Jakub Jelinek <jakub@redhat.com> 3.80-7
- rebuilt with GCC 4

* Mon Dec 13 2004 Jakub Jelinek <jakub@redhat.com> 3.80-6
- refuse -jN where N is bigger than PIPE_BUF (#142691, #17374)

* Thu Oct  7 2004 Jakub Jelinek <jakub@redhat.com> 3.80-5
- add URL rpm tag (#134799)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add important bug-fixes from make home-page

* Sun Nov 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.80

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 29 2002 Tim Powers <timp@redhat.com>
- fix references to %%install in the changelog so that the package will build

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com> 3.79.1-15
- _smp_mflags
- Fix ppc build (sys_siglist issues in patch2)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Jakub Jelinek <jakub@redhat.com>
- Run make check during build

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build with current auto* tools

* Fri Jan 25 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt with gcc 3.1

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- langify
- Make sure it isn't setgid if built as root

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Aug  7 2000 Tim Waugh <twaugh@redhat.com>
- change info-dir entry so that 'info make' works (#15029).

* Tue Aug  1 2000 Jakub Jelinek <jakub@redhat.com>
- assume we don't have clock_gettime in configure, so that
  make is not linked against -lpthread (and thus does not
  limit stack to 2MB).

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- add locale files (#14362).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 24 2000 Preston Brown <pbrown@redhat.com>
- 3.79.1 bugfix release

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun May  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build for some odd situations, such as
  - previously installed make != GNU make
  - /bin/sh != bash

* Mon Apr 17 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.79

* Thu Feb 24 2000 Cristian Gafton <gafton@redhat.com>
- add patch from Andreas Jaeger to fix dtype lookups (for glibc 2.1.3
  builds)

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Fri Jan 21 2000 Cristian Gafton <gafton@redhat.com>
- apply patch to fix a /tmp race condition from Thomas Biege
- simplify %%install

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.78.1.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob
 
* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
