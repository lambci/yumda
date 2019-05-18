Summary: The GNU macro processor
Name: m4
Version: 1.4.16
Release: 10%{?dist}.0.2
License: GPLv3+
Group: Applications/Text
Source0: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz
Source1: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz.sig
URL: http://www.gnu.org/software/m4/
# Patch0: Temporary fix to avoid fails, already fixed in gnulib, this patch
#         should be removed after updating m4 to newer gnulib
Patch0: m4-1.4.16-readlink-einval.patch
# Patch1: Temporary fix to avoid build fails, this patch
#         should be removed after updateing m4 to newer gnulib
Patch1: m4-1.4.16-gnulib-gets.patch
# Patch2: Fixes math tests for little-endian PowerPC,
#         patch by Menanteau Guy and Ulrich Weigand
Patch2: m4-1.4.17-gnulib-ppc64le.patch
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
# Gnulib bundled - the library has been granted an exception, see https://fedorahosted.org/fpc/ticket/174
# Gnulib is not versioned, see m4 ChangeLog for approximate date of Gnulib copy
Provides: bundled(gnulib)

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%setup -q
%patch0 -p1 -b .readlink-einval
%patch1 -p1 -b .gnulib-gets
%patch2 -p1 -b .gnulib-ppc64le
chmod 644 COPYING

%build
%configure
make %{?_smp_mflags}

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%check
make %{?_smp_mflags} check

%files
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/m4
%{_infodir}/*
%{_mandir}/man1/m4.1*

%post
if [ -f %{_infodir}/m4.info ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/m4.info %{_infodir}/dir || :
fi

%preun
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/m4.info ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/m4.info %{_infodir}/dir || :
    fi
fi

%changelog
* Thu Aug 07 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-10
- Fix ppc64le test fails
  Resolves: #1125604

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.4.16-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4.16-8
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-6
- Fix issues found by fedora-review utility in the spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-4
- Fix handling of bundled gnulib in the spec file
  Resolves: #821777

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-2
- Temporarily fix readlink test to accept EINVAL also
  Resolves: #739189

* Wed Mar 02 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-1
- Update to m4-1.4.16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.15-1
- Update to m4-1.4.15 (removed include patch, already applied in upstream source)
  Resolves: #630709

* Mon Mar  1 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.14-1
- Update to m4-1.4.14
  Resolves: #568339

* Thu Sep  3 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.13-4
- Fix errors installing m4 with --excludedocs
  Resolves: #516013

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.4.13-3
- Use xz compressed upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Stepan Kasal <skasal@redhat.com> - 1.4.13-1
- new upstream release
- drop the ununsed Source1: %%{SOURCE0}.sig
- enable %%check again

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov  5 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.12-1
- Update to m4-1.4.12
  Resolves: #469944
- Merge review
  Resolves: #226115

* Wed Apr 23 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.11-1
- Update to m4-1.4.11 (removed vasnprintf patch, it's included in
  upstream source)
  Resolves: #443589

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.10-3
- Fix Buildroot

* Mon Dec 17 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.10-2
- Fix vasnprintf puts %%n into a writeable format string in all cases
  Resolves: #345651

* Wed Aug 22 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.10-1
- Update to m4-1.4.10
- Fix license to GPL version 3 or later

* Tue Jun  5 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-1
- Update to m4-1.4.9

* Thu Apr 19 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.8-2
- Rebuild

* Sun Nov 26 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.8-1
- Update to m4-1.4.8

* Wed Oct 25 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.7-2
- Drop %%check again.  SIGPIPE is set to SIG_IGN in mock, which breaks the
  sysval test.

* Tue Oct 24 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.7-1
- Update to m4-1.4.7
- Add %%check
- Fix a rpmlint warning about Summary:

* Mon Jul 17 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.5-3
- Use the install-info scriptlets recommended in the Fedora Extras wiki
- Move $RPM_BUILD_ROOT cleaning from %%prep to %%install

* Mon Jul 17 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.5-2
- remove infodir/dir so it isn't included in the package

* Mon Jul 17 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.5-1
- Update to m4-1.4.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 22 2005 Miloslav Trmac <mitr@redhat.com> - 1.4.4-1
- Update to m4-1.4.4

* Sun Sep 18 2005 Miloslav Trmac <mitr@redhat.com> - 1.4.3-2
- Ship COPYING and ChangeLog

* Fri Apr  1 2005 Miloslav Trmac <mitr@redhat.com> - 1.4.3-1
- Update to m4-1.4.3

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.4.2-3
- build with gcc-4

* Sun Feb 27 2005 Florian La Roche <laroche@redhat.com>
- rebuild

* Sun Dec 12 2004 Miloslav Trmac <mitr@redhat.com> - 1.4.2-1
- Update to m4-1.4.2

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add french translation file

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not strip apps

* Fri Jun 14 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- use _infodir on popular request #47465

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add URL tag
- improved spec file
- add hack to update config.guess config.sub
- fix to build with newer autoconf versions

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Feb 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- signal patch is not necessary anymore
- fix printf buffer overflow problem

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- added defattr

* Mon Jun  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHS compliance
- 1.4.1
- some fixes to spec file

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added info file handling and BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

