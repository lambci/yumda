Summary: A GNU collection of diff utilities
Name: diffutils
Version: 3.3
Release: 5%{?dist}
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.xz
Patch1: diffutils-cmp-s-empty.patch
Patch2: diffutils-mkdir_p.patch
Patch4: diffutils-i18n.patch
Patch5: diffutils-3.3-diffseq.patch
License: GPLv3+
Requires(post): info
Requires(preun): info
Provides: bundled(gnulib)
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: help2man

Prefix: %{_prefix}

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

%prep
%setup -q
# For 'cmp -s', compare file sizes only if both non-zero (bug #563618).
%patch1 -p1 -b .cmp-s-empty

# Work around @mkdir_p@ build issue.
%patch2 -p1 -b .mkdir_p

%patch4 -p1 -b .i18n

%patch5 -p1 -b .diffseq

%build
%configure
make PR_PROGRAM=%{_bindir}/pr

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*

%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_datadir}

%changelog
* Tue Feb 11 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Nov 21 2018 Than Ngo <than@redhat.com> - 3.3-5
- Resolves: #1611281, diff -y produces garbage

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.3-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.3-3
- Mass rebuild 2013-12-27

* Wed Oct 23 2013 Tim Waugh <twaugh@redhat.com> 3.3-2
- Fixed multibyte handling logic for diff -Z (bug #1022417).

* Tue Mar 26 2013 Tim Waugh <twaugh@redhat.com> 3.3-1
- 3.3 (bug #927560).

* Fri Feb 22 2013 Tim Waugh <twaugh@redhat.com> 3.2-13
- Fixed i18n handling of 'diff -E' (bug #914666).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Tim Waugh <twaugh@redhat.com> 3.2-11
- Ported i18n patch and reinstated it (bug #870460).

* Wed Sep 19 2012 Tim Waugh <twaugh@redhat.com> 3.2-10
- Fixed license as current source says GPLv3+.

* Mon Jul 23 2012 Tim Waugh <twaugh@redhat.com> 3.2-9
- Fixed build failure.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21  2012 Tim Waugh <twaugh@redhat.com> 3.2-7
- Provides bundled(gnulib) (bug #821751).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec  8 2011 Tim Waugh <twaugh@redhat.com> 3.2-5
- Fix bug #747969 again.

* Tue Nov 29 2011 Tim Waugh <twaugh@redhat.com> 3.2-4
- Real fix for bug #747969: the diffutils info file changed name in
  3.1.  Updated the scriptlets to install/remove the correct filename
  from the info directory.

* Fri Nov 25 2011 Tim Waugh <twaugh@redhat.com> 3.2-3
- Fixed up reference to info page in man pages (bug #747969).

* Fri Nov 25 2011 Tim Waugh <twaugh@redhat.com> 3.2-2
- Applied upstream gnulib fix for float test on ppc, as well as
  correction for LDBL_MANT_DIG definition (bug #733536).

* Fri Sep  2 2011 Tim Waugh <twaugh@redhat.com> 3.2-1
- 3.2.

* Thu Aug 11 2011 Tim Waugh <twaugh@redhat.com> 3.1-1
- 3.1.

* Wed Apr 13 2011 Tim Waugh <twaugh@redhat.com> 3.0-1
- 3.0 (bug #566482).
- The i18n patch is dropped for the time being.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 25 2010 Tim Waugh <twaugh@redhat.com> 2.8.1-29
- For 'cmp -s', compare file sizes only if both non-zero (bug #563618).

* Wed Apr 21 2010 Tim Waugh <twaugh@redhat.com> - 2.8.1-28
- Build requires help2man (bug #577325).  Fixes empty diff man page.

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 2.8.1-27
- Added comments for all patches.

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 2.8.1-26
- Use upstream man pages.
- Ship COPYING file.

* Tue Aug 11 2009 Tim Waugh <twaugh@redhat.com> 2.8.1-25
- Only try to install the info file if it exists so that package
  installation does not fail with --excludedocs (bug #515919).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.1-22
- Fixed 'sdiff -E' (bug #484892).

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 2.8.1-21
- Rebuild for GCC 4.3.

* Wed Jan  2 2008 Tim Waugh <twaugh@redhat.com> 2.8.1-20
- Converted spec file to UTF-8 (bug #225696).
- Fixed summary (bug #225696).
- Fixed PreReq (bug #225696).
- Removed Prefix (bug #225696).
- Fixed build root (bug #225696).
- Avoid %%makeinstall (bug #225696).
- Fixed license tag (bug #225696).

* Tue Nov  6 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-19
- Rebuilt.

* Tue Nov  6 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-18
- Fixed multibyte speed improvement patch (bug #363831).

* Tue Aug 14 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-17
- Multibyte speed improvement (bug #252117).

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 2.8.1-16
- Make scriptlet unconditionally succeed (bug #223683).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.1-15.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.8.1-15.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.1-15.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Apr  6 2005 Tim Waugh <twaugh@redhat.com> 2.8.1-15
- Fixed sdiff exit code handling (bug #152967).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.8.1-14
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 2.8.1-13
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan  8 2004 Tim Waugh <twaugh@redhat.com> 2.8.1-10
- Fix mistaken use of '|' instead of '||'.

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 2.8.1-9
- Rebuilt.

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 2.8.1-8
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 19 2002 Tim Waugh <twaugh@redhat.com> 2.8.1-5
- i18n patch.

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 2.8.1-4
- Ship translations.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 22 2002 Tim Waugh <twaugh@redhat.com> 2.8.1-1
- 2.8.1.
- No longer need immunix-owl-tmp patch.

* Wed Feb 27 2002 Tim Waugh <twaugh@redhat.com> 2.7.2-5
- Rebuild in new environment.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Nov 02 2001 Tim Waugh <twaugh@redhat.com> 2.7.2-3
- Make sure %%post scriplet doesn't fail if --excludedocs is used.

* Fri Jun 01 2001 Tim Waugh <twaugh@redhat.com> 2.7.2-2
- Install diff.1, since it's no longer in man-pages.

* Fri Mar 30 2001 Tim Waugh <twaugh@redhat.com> 2.7.2-1
- 2.7.2.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix %%changelog entries (escape them)
- update source location
- remove manual stripping
- add URL

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- add %%defattr
- use rpm macros

* Wed May 31 2000 Ngo Than <than@redhat.de>
- put man pages and info files in correct place
- cleanup specfile

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages.

* Mon Apr 19 1999 Jeff Johnson <jbj@redhat.com>
- man pages not in %%files.
- but avoid conflict for diff.1

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Sun Mar 14 1999 Jeff Johnson <jbj@redhat.com>
- add man pages (#831).
- add %%configure and Prefix.

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul 14 1998 Bill Kawakami <billk@home.com>
- included the four man pages stolen from Slackware

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun May 03 1998 Cristian Gafton <gafton@redhat.com>
- fixed spec file to reference/use the $RPM_BUILD_ROOT always
    
* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed where it looks for 'pr' (/usr/bin, rather than /bin)

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
