Summary: Conversion between character sets and surfaces
Name: recode
Version: 3.6
Release: 38%{?dist}.0.1
License: GPLv2+
Group: Applications/File
Source: http://recode.progiciels-bpi.ca/archives/recode-%{version}.tar.gz
Patch0: recode.patch
Patch1: recode-3.6-getcwd.patch
Patch2: recode-bool-bitfield.patch
Patch3: recode-flex-m4.patch
Patch4: recode-automake.patch
Url: http://recode.progiciels-bpi.ca/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libtool
BuildRequires: texinfo

Prefix: %{_prefix}

%description
The `recode' converts files between character sets and usages.
It recognises or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations.  Most RFC 1345 character sets
are supported.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .getcwd
%patch2 -p0
%patch3 -p1
%patch4 -p1
rm m4/libtool.m4
rm acinclude.m4

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%install
%makeinstall

%files
%defattr(-,root,root)
%license COPYING*
%{_bindir}/*
%{_libdir}/*.so.0*

%exclude %{_mandir}
%exclude %{_datadir}
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.6-38
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.6-37
- Mass rebuild 2013-12-27

* Mon Feb 25 2013 Zoltan Kota <zoltank[AT]gmail.com> 3.6-36
- Fix failed Fedora_19_Mass_Rebuild [bug #914431].

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-34
- Add patch for fixing build with new automake.
  (Fixes failed Fedora_18_Mass_Rebuild.)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-32
- Corrected summary of the devel subpackage. Fixing bug #817947.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 7 2010 Zoltan Kota <z.kota[AT]gmx.net> 3.6-29
- Fix build on x86_64. Run autoreconf to update config files.
  autoconf >= 2.64 needs to patch the flex.m4 file.
  Fixing FTBFS bug #564601.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6-26
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Zoltan Kota <z.kota[AT]gmx.net> 3.6-25
- add patch for gcc43

* Wed Aug 22 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-24
- update license tag
- rebuild

* Tue Apr 03 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-23
- rebuild

* Fri Sep 01 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-22
- rebuild

* Mon Feb 13 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-21
- rebuild

* Thu Dec 22 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-20
- rebuild

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-19
- fix requires
- disable static libs and remove libtool archives
- add %%doc

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-18
- add dist tag
- specfile cleanup

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 3.6-17
- rebuild for Extras

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.6-16
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.6-15
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.6-14
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Than Ngo <than@redhat.com> 3.6-11 
- add a patch file from kota@szbk.u-szeged.hu (bug #115524)

* Thu Nov 20 2003 Thomas Woerner <twoerner@redhat.com> 3.6-10
- Fixed RPATH (missing make in %%build)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 3.6-7
- rebuild on all arches
- remove unpackaged file from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Bill Nottingham <notting@redhat.com> 3.6-4
- add ldconfig %post/%postun

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 3.6-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 13 2001 Than Ngo <than@redhat.com> 3.6-1
- initial RPM for 8.0
