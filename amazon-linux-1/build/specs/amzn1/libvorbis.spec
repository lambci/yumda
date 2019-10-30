%define _buildid .7

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary:	The Vorbis General Audio Compression Codec
Name:		libvorbis
Version:	1.3.3
Release: 8%{?_buildid}%{?dist}
Epoch:		1
Group:		System Environment/Libraries
License:	BSD
URL:		http://www.xiph.org/
Source:		http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.xz
BuildRequires:	libogg-devel >= 2:1.1
Patch2:		libvorbis-1.2.3-add-needed.patch
Patch3:     CVE-2018-5146.diff

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates.

The libvorbis package contains runtime libraries for use in programs
that support Ogg Vorbis.

%package devel
Summary: Development tools for Vorbis applications
Group: Development/Libraries
Requires:	libogg-devel >= 2:1.1
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	vorbis-devel

%description devel
The libvorbis-devel package contains the header files and documentation
needed to develop applications with Ogg Vorbis.

%package devel-docs
Summary: Documentation for developing Vorbis applications
Group: Development/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description devel-docs
Documentation for developing applications with libvorbis.

%prep

%setup -q
%patch2 -p1
%patch3 -p1
sed -i "s/-O20/$RPM_OPT_FLAGS/" configure
sed -i "s/-ffast-math//" configure
sed -i "s/-mcpu=750//" configure

%build
%configure --with-ogg-libraries=%{_libdir} --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install docdir=%{_pkgdocdir}
install -pm 644 -t $RPM_BUILD_ROOT%{_pkgdocdir} AUTHORS COPYING README
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check

%files
%defattr(-,root,root)
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/COPYING
%{_libdir}/libvorbis.so.*
%{_libdir}/libvorbisfile.so.*
%{_libdir}/libvorbisenc.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vorbis
%{_libdir}/libvorbis.so
%{_libdir}/libvorbisfile.so
%{_libdir}/libvorbisenc.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/vorbis.m4

%files devel-docs
%defattr(-,root,root)
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/COPYING
%exclude %{_pkgdocdir}/doxygen-build.stamp

%clean 
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Apr 2 2018 Andrew Egelhofer <egelhofe@amazon.com>
- Import Upstream 1.3.3-8 and apply CVE-2018-5146 patch

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:1.3.3-8
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Adam Jackson <ajax@redhat.com> 1.3.3-7
- Nuke -mcpu=750 from cflags for PPC, that plus -mcpu=power7 confuses gcc.

* Thu Aug  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3.3-6
- Install docs to %%{_pkgdocdir} where available (#993967).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3.3-3
- Run test suite during build.
- Fix doc file permissions and duplicate doc dir ownership.
- rpmlint warning fixes.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libvorbis-1.2.3-4.el6_2.1

* Mon Feb 13 2012 Adam Jackson <ajax@redhat.com> 1.3.3-1
- libvorbis 1.3.3 (#787635)

* Wed Jan 04 2012 Jindrich Novy <jnovy@redhat.com> 1.3.2-2
- ship documentation only in -doc subpackage and only license
  in -devel (#540634) - thanks to Edward Sheldrake
- -devel-doc subpackage requires -devel

* Wed Feb 09 2011 Adam Jackson <ajax@redhat.com> 1.3.2-1
- libvorbis 1.3.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libvorbis-1.2.3-4.el6

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 1.3.1-2
- Include COPYING in base package too.

* Fri May 7 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/libvorbis-1.1.2-3.el5_4.4
- import source package RHEL5/libvorbis-1.1.2-3.el5_3.3
- import source package RHEL5/libvorbis-1.1.2-3.el5_1.2
- import source package RHEL5/libvorbis-1.1.2-3.el5.0
- import source package RHEL5/libvorbis-1.1.2-2
- added submodule prep for package libvorbis

* Mon Mar 29 2010 Adam Jackson <ajax@redhat.com> 1.3.1-1
- libvorbis 1.3.1.  Fixes surround.

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 1.2.3-5
- libvorbis-1.2.3-add-needed.patch: Fix FTBFS from --no-add-needed

* Mon Nov 23 2009 Adam Jackson <ajax@redhat.com> 1.2.3-4
- Fix doc subpackage build (#540634)

* Mon Nov  2 2009 Jindrich Novy <jnovy@redhat.com> 1.2.3-3
- backport patches to fix CVE-2009-3379 (#531765) from upstream

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Adam Jackson <ajax@redhat.com> 1.2.3-1
- libvorbis 1.2.3

* Wed Jul 08 2009 Adam Jackson <ajax@redhat.com> 1.2.2-2
- libvorbis-1.2.2-svn16228.patch: Backport a fix from pre-1.2.3 to hopefully
  fix small sound file playback. (#505610)

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.2.2-1
- libvorbis 1.2.2

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 1.2.2-0.1.rc1
- libvorbis 1.2.2rc1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Caolán McNamara <caolanm@redhat.com> -1:1.2.0-6
- rebuild to get provides pkgconfig(vorbisenc)

* Sun Sep  7 2008 Hans de Goede <hdegoede@redhat.com> -1:1.2.0-5
- Fix patch fuzz build failure

* Wed May 14 2008 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-4
- fix CVE-2008-1420, CVE-2008-1419, CVE-2008-1423 (#446344)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.2.0-3
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:1.2.0-2
- Don't include Makefile's in %%doc, avoiding a multilib conflict (bz 342481)

* Mon Oct 15 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1:1.2.0-1
- Update to 1.2.0
- Resolves: #250115

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1:1.1.2-4
- Rebuild for build ID

* Mon Jun 25 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.1.2-3
- Fix typos in %%description (#245471)

* Thu Feb  8 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.1.2-2
- Package review cleanups
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.2-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.2-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> 1:1.1.2-1
- Update to 1.1.2

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.1-1
- Update to 1.1.1

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.0-2
- rebuild with gcc 4.0

* Wed Sep 29 2004 Colin Walters <walters@redhat.com> 1:1.1.0-1
- Update to 1.1.0
- Remove upstreamed patch libvorbis-underquoted.patch

* Wed Sep 29 2004 Warren Togami <wtogami@redhat.com> 1:1.0.1-5
- link to .pdf spec rather than ship redundant copy
- spec cleanups

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.0.1-4
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 11 2003 Bill Nottingham <notting@redhat.com> 1:1.0.1-1
- update to 1.0.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Elliot lee <sopwith@redhat.com> 1:1.0-6
- Fix #81026 by updating libvorbis-1.0-m4.patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Bill Nottingham <notting@redhat.com> 1:1.0-4
- add epochs to dependencies, to avoid 1.0rc3 >= 1.0 miscomparisons
  (#79374)
- fix vorbis.m4

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1:1.0-2
- remove unpackaged files from the buildroot
- tell configure where ogg libs are
- lib64'ize

* Fri Jul 18 2002 Bill Nottingham <notting@redhat.com>
- one-dot-oh
- libtool strikes again (#66110)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.0rc3

* Thu Aug 16 2001 Bill Nottingham <notting@redhat.com>
- fix bug in floor backend (<michael@stroucken.org>)

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc2

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- split out from the main vorbis package

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- own %%{_libdir}/ao
- I love libtool

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add links from library major version numbers in rpms

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- update to rc1

* Fri May  4 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- fixed perl line in spec file to set optims correctly

* Tue Mar 20 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64, again
- use optflags, not -O20 -ffast-math (especially on alpha...)

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- fix license tag
- beta4

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64

* Thu Feb  8 2001 Bill Nottingham <notting@redhat.com>
- update CVS in prep for beta4

* Wed Feb 07 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #25391. ogg123 now usses the OSS driver by default if
  none was specified.

* Tue Jan  9 2001 Bill Nottingham <notting@redhat.com>
- update CVS, grab aRts backend for libao

* Thu Dec 27 2000 Bill Nottingham <notting@redhat.com>
- update CVS

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- hack up specfile some, merge some packages

* Sat Oct 21 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
