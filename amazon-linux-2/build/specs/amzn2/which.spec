Summary: Displays where a particular program in your path is located
Name: which
Version: 2.20
Release: 7%{?dist}.0.2
License: GPLv3
Group: Applications/System
Source0: http://www.xs4all.nl/~carlo17/which/%{name}-%{version}.tar.gz
Source1: which2.sh
Source2: which2.csh
Url: http://www.xs4all.nl/~carlo17/which/
Patch: which-2.19-afs.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: readline-devel
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%prep
%setup -q

%patch -p1 -b .afs

%build
%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%post
/sbin/install-info --quiet --info-dir=%{_infodir} %{_infodir}/which.info.gz
exit 0

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/which.info.gz
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING EXAMPLES README AUTHORS NEWS
%attr(0644,root,root) %{_sysconfdir}/profile.d/which2.*
%{_bindir}/*
%{_infodir}/which.info.gz
%{_mandir}/*/*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.20-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.20-6
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Than Ngo <than@redhat.com> - 2.20-1
- 2.2.0
- disable alias which for cshell

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Warren Togami <wtogami@redhat.com> 2.19-3
- install-info should exit gracefully when --nodocs

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 2.19-2
- rebuilt

* Fri Jan 25 2008 Than Ngo <than@redhat.com> 2.19-1
- 2.19, fix #399551, #430159

* Tue Nov 27 2007 Than Ngo <than@redhat.com> - 2.18-5
- fix permission which-2 scripts

* Tue Nov 27 2007 Than Ngo <than@redhat.com> 2.18-4
- fix permission which-2 scripts

* Mon Nov 26 2007 Karsten Hopp <karsten@redhat.com> 2.18-3
- add dir entry for info page

* Tue Nov 20 2007 Than Ngo <than@redhat.com> 2.18-2
- cleanup specfile

* Tue Nov 13 2007 Than Ngo <than@redhat.com> 2.18-1
- 2.18

* Tue Nov 13 2007 Than Ngo <than@redhat.com> 2.16-10
- cleanup specfile
- get rid of dev dependency

* Mon Apr 23 2007 Than Ngo <than@redhat.com> - 2.16-9
- add missing which-2 script for csh
- cleanup specfile #226539

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 2.16-8
- install-info scriptlet failures

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 2.16-7
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.16-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.16-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 2.16-6
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 2.16-5
- rebuilt

* Sat Aug 07 2004 Than Ngo <than@redhat.com> 2.16-4
- add missing URL (thanks to  Robert Scheck)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.16
- fix %%preun

* Thu Jul 17 2003 Than Ngo <than@redhat.com> 2.14-8
- rebuild

* Thu Jul 17 2003 Than Ngo <than@redhat.com> 2.14-7
- added Prereq: dev (bug #99275)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 10 2002 Than Ngo <than@redhat.com> 2.14-4
- cleanup code (bug #78478)

* Thu Nov 14 2002 Tim Powers <timp@redhat.com> 2.14-3
- redirect info dir warnings to /dev/null

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 2.14-1
- add missing info file

* Mon Jul 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.14 wih better support for current bash

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Than Ngo <than@redhat.com> 2.13-3
- use access instead stat in AFS environment (bug #60353)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.13

* Sat Aug  4 2001 Than Ngo <than@redhat.com>
- fix bug 50844

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Sep 10 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- 2.12 (only man-page fix)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- FHS packaging.

* Sun May 21 2000 Ngo Than <than@redhat.de>
- put man pages in /usr/share/man/*

* Thu Apr 20 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.11
- change from root:bin -> root:root

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Sun Jan 16 2000 Preston Brown <pbrown@redhat.com>
- newer stuff rom Carlo (2.10).  Author's email: carlo@gnu.org

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- adopted Carlo's specfile.

* Fri Sep 24 1999 Carlo Wood <carlo@gnu.org>
- There should not be a reason anymore to include README.alias in the rpm docs.
- Don't install as root.root in RPM_BUILD_ROOT, in order to allow to build
  rpm as non-root.
- Bug fix
- Added /etc/profile.d for automatic alias inclusion.

* Wed Aug 25 1999 Carlo Wood <carlo@gnu.org>
- Added README.alias.

* Wed Aug 11 1999 Carlo Wood <carlo@gnu.org>
- Typo in comment.

* Thu May 27 1999 Carlo Wood <carlo@gnu.org>
- Typo fix
- Moved maintainer targets from makefile to Makefile.am.

* Tue May 18 1999 Carlo Wood <carlo@gnu.org>
- Typo in appended changelog.
- Appended the old change log of `which-2.0.spec' to (this) changelog,
  which is generated from the CVS log of `which-2.0.spec.in'.
- Generate which-2.spec from which-2.spec.in with automatic VERSION
  and CHANGELOG substitution.

* Tue May 14 1999 Carlo Wood <carlo@gnu.org>
- Moved assignment of CFLAGS to the configure line, using RPM_OPT_FLAGS now.
- Corrected Source: line to point to ftp.gnu.org.

* Sat Apr 17 1999 Carlo Wood <carlo@gnu.org>
- Started to use automake and autoconf

* Fri Apr 09 1999 Carlo Wood <carlo@gnu.org>
- Renamed which-2.0.spec to which-2.spec

