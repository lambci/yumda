Summary:        The Ogg bitstream file format library
Name:           libogg
Epoch:          2
Version:        1.3.0
Release: 7%{?dist}.0.2
Group:          System Environment/Libraries
License:        BSD
URL:            http://www.xiph.org/

Source:         http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz

Patch0:		libogg-aarch64.patch
Patch1:		libogg-multilib.patch

Prefix: %{_prefix}

%description
Libogg is a library for manipulating Ogg bitstream file formats.
Libogg supports both making Ogg bitstreams and getting packets from
Ogg bitstreams.


%prep
%setup -q

%patch0 -p1
%patch1 -p1

%build
sed -i "s/-O20/$RPM_OPT_FLAGS/" configure
sed -i "s/-ffast-math//" configure
%configure --disable-static
make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install

%files
%license COPYING
%{_libdir}/libogg.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2:1.3.0-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2:1.3.0-6
- Mass rebuild 2013-12-27

* Tue Apr 09 2013 Jaromir Capik <jcapik@redhat.com> - 2:1.3.0-5
- fixing multilib conflict (#831414)

* Tue Mar 26 2013 Jaromir Capik <jcapik@redhat.com> - 2:1.3.0-4
- aarch64 support (#925834)
- minor spec cleaning

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Gregory Maxwell <greg@xiph.org> 1.3.0-1
- libogg 1.3.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Adam Jackson <ajax@redhat.com> 1.2.2-2
- Fix epoch.

* Tue Dec 07 2010 Adam Jackson <ajax@redhat.com> 1.2.2-1
- libogg 1.2.2

* Mon Apr 26 2010 Adam Jackson <ajax@redhat.com> 1.2.0-1
- libogg 1.2.0

* Tue Nov 10 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 2:1.1.4-3
- fixed libogg-devel-docs (BZ #510608) (By Edward Sheldrake)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.1.4-1
- libogg 1.1.4

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 1.1.4-0.1.rc1
- libogg 1.1.4rc1
- split devel docs to noarch subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2:1.1.3-10
- Rebuild for pkgconfig provides

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:1.1.3-9
- Autorebuild for GCC 4.3

* Wed Nov 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2:1.1.3-8
- Some more small specfile cleanups for merge review (bz 226035)

* Wed Nov 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2:1.1.3-7
- Some small specfile cleanups
- Add smpflags to make invocation (bz 226035)

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2:1.1.3-6
- Don't install Makefile's as %%doc, avoiding a multilib conflict (bz 342281)

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2:1.1.3-5
- Rebuild for PPC toolchain bug

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2:1.1.3-4
- Require automake in the -devel package

* Thu Feb  8 2007 Matthias Clasen <mclasen@redhat.com> - 2:1.1.3-3
- Package review cleanups
- Don't ship a static library

* Thu Aug 17 2006 Matthias Clasen <mclasen@redhat.com> - 2:1.1.3-2.fc6
- Fix 202280

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:1.1.3-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:1.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:1.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> 2:1.1.3-1
- Update to 1.1.3
- doc/ogg changed to doc/libogg

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 2:1.1.2-2
- rebuild for gcc 4.0

* Wed Sep 29 2004 Colin Walters <walters@redhat.com> 2:1.1.2-1
- Update to 1.1.2
- Delete upstreamed libogg-1.1-64bit.patch
- Delete upstreamed libogg-underquoted.patch

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 2:1.1-4
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 11 2003 Bill Nottingham <notting@redhat.com> 2:1.1-1
- update to 1.1

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 2:1.0-5.1
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Bill Nottingham <notting@redhat.com> 2:1.0-3
- fix ogg.m4

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2:1.0-2
- remove unpackaged files from the buildroot

* Fri Jul 18 2002 Bill Nottingham <notting@redhat.com> 1.0-1
- one-dot-oh

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.0rc3

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc2

* Fri Jul  6 2001 Bill Nottingham <notting@redhat.com>
- own %%{_includedir}/ogg

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc1

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- fix license tag

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- beta4

* Tue Feb  6 2001 Bill Nottingham <notting@redhat.com>
- update CVS in prep for beta4

* Thu Dec 27 2000 Bill Nottingham <notting@redhat.com>
- update CVS

* Tue Dec 11 2000 Bill Nottingham <notting@redhat.com>
- fix bogus group

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- clean up specfile slightly

* Sat Sep 02 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
