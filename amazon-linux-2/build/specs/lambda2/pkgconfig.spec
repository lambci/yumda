Summary: A tool for determining compilation options
Name: pkgconfig
Version: 0.27.1
Release: 4%{?dist}.0.2
Epoch: 1
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Source:  http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz

# https://bugs.freedesktop.org/show_bug.cgi?id=66155
Patch0: pkg-config-man-cleanup.patch

BuildRequires: glib2-devel

Provides: pkgconfig(pkg-config) = %{version}

Prefix: %{_prefix}

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%prep
%setup -n pkg-config-%{version} -q
%patch0 -p1 -b .man-cleanup

%build
%configure \
        --disable-shared \
        --with-installed-glib \
        --with-pc-path=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig

# we include this below, already
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/pkg-config

%files
%license COPYING
%{_bindir}/*
%{_libdir}/pkgconfig
%{_datadir}/pkgconfig
%{_datadir}/aclocal/*

%exclude %{_mandir}

%changelog
* Thu Oct 31 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:0.27.1-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:0.27.1-3
- Mass rebuild 2013-12-27

* Tue Jun 25 2013 Matthias Clasen <mclasen@redhat.com> - 0.27.1-2
- Fix a few errors in the man page

* Wed Mar 27 2013 Christophe Fergeau <cfergeau@redhat.com> 0.27.1-1
- Update to 0.27.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Kalev Lember <kalevlember@gmail.com> - 1:0.27-1
- Update to 0.27
- Drop deps on popt, 0.27 no longer uses it

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Christophe Fergeau <cfergeau@redhat.com> - 1:0.26-1
- Update to 0.26 (#802480)
- Drop upstreamed patches

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Matthias Clasen <mclasen@redhat.com> 0.25-2
- Workaround breakage with autoconf 2.66

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> 0.25-1
- Update to 0.25

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 0.24-6
- Avoid segfaults

* Wed May 26 2010 Matthias Clasen <mclasen@redhat.com> 0.24-5
- Expand the popt-compat patch to cover empty Libs: as well

* Wed May 26 2010 Matthias Clasen <mclasen@redhat.com> 0.24-4
- Go back to using system popt

* Wed May 26 2010 Matthias Clasen <mclasen@redhat.com> 0.24-3
- Revert the escaping change that is causing a lot of problems

* Sun May 23 2010 Matthias Clasen <mclasen@redhat.com> 0.24-2
- Go back to using the included popt

* Sun May 23 2010 Matthias Clasen <mclasen@redhat.com> 0.24-1
- Update to 0.24
- Use system glib, popt

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Matthias Clasen  <mclasen@redhat.com> - 1:0.23-7
- Add an explict pkgconfig provides (#476199)

* Mon Dec  8 2008 Matthias Clasen  <mclasen@redhat.com> - 1:0.23-6
- Remove a patch that is no longer necessary and causes more
  problems than it solves (#224148)
- Include Requires.private in --print-requires (#426106)

* Fri Jun 06 2008 Colin Walters <walters@redhat.com> - 1:0.23-3
- Add patch pkg-config-lib64-excludes.patch to make my jhbuild happier

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 1:0.23-2
- Readd the requires.private fix that was dropped prematurely

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 1:0.23-1
- Update to 0.23

* Thu Nov 15 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.22-4
- Fix handling of conflicts (#384421)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.22-3
- Rebuild for selinux ppc32 issue.

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.22-2
- Update license field

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.22-1
- Update to 0.22
- Drop upstreamed patch

* Thu Mar 29 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.21-5
- Fix --exists to ignore Requires.private
- Fix Requires.private to operate fully recursive

* Fri Feb  2 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.21-4
- Address some package review complaints

* Mon Jan 29 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.21-3
- Fix a problem where calling glib-config can lead
  to an infinite loop 

* Thu Dec  7 2006 Matthias Clasen <mclasen@redhat.com> - 1:0.21-2
- Small spec file cleanups

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 1:0.21-1.fc6
- Update to 0.21

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:0.20-4.1
- rebuild

* Mon Jun 12 2006 Bill Nottingham <notting@redhat.com> - 1:0.20-4
- don't call auto*

* Thu Jun  1 2006 Matthias Clasen <mclasen@redhat.com> - 1:0.20-3
- Add missing BuildRequires

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.20-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.20-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Matthias Clasen <mclasen@redhat.com> 1:0.20-2
- Rebuild

* Tue Oct 25 2005 Matthias Clasen <mclasen@redhat.com> 1:0.20-1
- Update to 0.20
- Drop upstreamed patches

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> 1:0.19-1
- Update to 0.19
- Take ownership of /usr/share/pkgconfig (#169335)

* Tue Aug  9 2005 Matthias Clasen <mclasen@redhat.com> 1:0.18.1-4
- Fix a segfault which curiously hits only bigendian platforms

* Sun Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 1:0.18.1-3
- Remove unncessary dependencies

* Fri Jul  8 2005 Matthias Clasen <mclasen@redhat.com> 1:0.18.1-2
- Fix the default search path

* Thu Jul  7 2005 Matthias Clasen <mclasen@redhat.com> 1:0.18.1-1
- Update to 0.18.1

* Wed Mar 30 2005 Matthias Clasen <mclasen@redhat.com> 1:0.15.0-6
- add --print-requires and --print-provide options

* Mon Mar  7 2005 Matthias Clasen <mclasen@redhat.com> 1:0.15.0-5
- fix an overflow

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com>
- rebuild with gcc4

* Wed Jun 23 2004 Matthias Clasen <mclasen@redhat.com> 1:0.15.0-3
- fix underquoted definition in pkg.m4  (#116128)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Mark McLoughlin <markmc@redhat.com>
- Update to 0.15.0
- Fix datadir patch conflict

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 23 2003 Owen Taylor <otaylor@redhat.com> 1:0.14.0-6
- Make pkgconfig look in /usr/share/pkgconfig as well by default (#98595)

* Thu Jun 26 2003 Havoc Pennington <hp@redhat.com> 1:0.14.0-5
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com>
- suppress /usr/lib64 (instead of /usr/lib) from LIBS by default on multilib
  arches where the default is to use lib64

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- 0.14

* Tue Oct  8 2002 Havoc Pennington <hp@redhat.com>
- use libdir, so we do move .pc files to /usr/lib64

* Tue Oct  8 2002 Havoc Pennington <hp@redhat.com>
- use prefix/lib not libdir, so we don't move .pc files to /usr/lib64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar  7 2002 Havoc Pennington <hp@redhat.com>
- 0.12.0

* Thu Feb  7 2002 Havoc Pennington <hp@redhat.com>
- 0.11.0

* Sun Feb  3 2002 Havoc Pennington <hp@redhat.com>
- backbuild in gnomehide

* Sun Feb  3 2002 Havoc Pennington <hp@redhat.com>
- 0.10.0

* Sun Feb  3 2002 Havoc Pennington <hp@redhat.com>
- 0.9.0

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- call libtoolize to make porting to new archs easier

* Thu Jun 07 2001 Havoc Pennington <hp@redhat.com>
- put pkg.m4 in file list

* Wed Jun 06 2001 Havoc Pennington <hp@redhat.com>
- Upgrade to 0.7
- add man page

* Wed Jan 03 2001 Havoc Pennington <hp@redhat.com>
- Upgrade to 0.5

* Thu Dec 14 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Wed Oct 04 2000 Owen Taylor <otaylor@redhat.com>
- Initial package
