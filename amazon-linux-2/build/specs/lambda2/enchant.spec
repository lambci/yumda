Summary: An Enchanting Spell Checking Library
Name: enchant
Version: 1.6.0
Release: 8%{?dist}.0.2
Epoch: 1
Group: System Environment/Libraries
License: LGPLv2+
Source: http://www.abisource.com/downloads/enchant/%{version}/enchant-%{version}.tar.gz
URL: http://www.abisource.com/
BuildRequires: glib2-devel >= 2.6.0
BuildRequires: aspell-devel
BuildRequires: hunspell-devel
BuildRequires: libvoikko-devel
BuildRequires: automake, libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Prefix: %{_prefix}

%description
A library that wraps other spell checking backends.

%package aspell
Summary: Integration with aspell for libenchant
Group: System Environment/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}
Prefix: %{_prefix}

%description aspell
Libraries necessary to integrate applications using libenchant with aspell.

%package voikko
Summary: Integration with voikko for libenchant
Group: System Environment/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}
Prefix: %{_prefix}

%description voikko
Libraries necessary to integrate applications using libenchant with voikko.


%prep
%setup -q

%build
%configure --enable-myspell --with-myspell-dir=%{_datadir}/myspell --disable-static --disable-ispell --disable-hspell --disable-zemberek
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/enchant/*.la

%files
%defattr(-,root,root)
%license COPYING.LIB
%{_bindir}/*
%{_libdir}/lib*.so.*
%dir %{_libdir}/enchant
%{_libdir}/enchant/lib*myspell.so*
%{_datadir}/enchant

%files aspell
%{_libdir}/enchant/lib*aspell.so*

%files voikko
%{_libdir}/enchant/lib*_voikko.so*

%exclude %{_mandir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_includedir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:1.6.0-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.6.0-7
- Mass rebuild 2013-12-27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 24 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:1.6.0-3
- Rebuild for new hunspell

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 01 2010 Marc Maurer <uwog@abisource.com> 1:1.6.0-1
- New upstream version.
- Drop all shipped patches, as they are included upstream.

* Tue Jan  5 2010 Michael Schwendt <mschwendt@fedoraproject.org> 1:1.5.0-5
- Revert 544473: Move libenchant.so back into the -devel package.

* Sat Dec 05 2009 Marc Maurer <uwog@abisource.com> 1:1.5.0-4
- Fix 544473: Move enchant.so from the devel to the main package

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Caolán McNamara <caolanm@redhat.com> 1:1.5.0-2
- Resolves: rhbz#508781 improve enchant quality, leaks, and edge-case language
  dict selection

* Mon Jun 22 2009 Caolán McNamara <caolanm@redhat.com> 1:1.5.0-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jul 26 2008 Michael Schwendt <mschwendt@fedoraproject.org> 1:1.4.2-4
- Rebuild for ABI-incompatible hunspell-1.2.4.2-2.fc10

* Thu Jul 10 2008 Marc Maurer <uwog@abisource.com> 1:1.4.2-3
- Fix 426712: don't build static libs (patch from Michael Schwendt)

* Wed May 21 2008 Marc Maurer <uwog@abisource.com> 1:1.4.2-2
- Rebuild

* Wed May 21 2008 Marc Maurer <uwog@abisource.com> 1:1.4.2-1
- New upstream release
- Add voikko support in an enchant-voikko package
- Bump glib-devel BR to 2.6.0

* Fri Feb 08 2008 Caolan McNamara <caolanm@redhat.com> 1:1.3.0-4.fc9
- minor cockup

* Sat Jan 26 2008 Caolan McNamara <caolanm@redhat.com> 1:1.3.0-3.fc9
- Resolves: rhbz#426402 use system hunspell not internal one and 
  split out aspell backend.
- See: rhbz#430354 hspell backend disabled until pic issue fixed

* Wed Dec 19 2007 Caolan McNamara <caolanm@redhat.com> 1:1.3.0-2.fc9
- tell enchant where the myspell dictionaries are

* Thu Oct 12 2006 Marc Maurer <uwog@abisource.com> 1:1.3.0-1.fc6
- Update to 1.3.0

* Mon Sep 11 2006 Marc Maurer <uwog@abisource.com> 1:1.2.5-3.fc6
- Rebuild for FC6

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 1:1.2.5-2.fc6
- Rebuild

* Mon Apr 10 2006 Marc Maurer <uwog@abisource.com> 1:1.2.5-1.fc6
- Package the data dir as well (bug 188516)
- New upstream version
- Add hspell requirement/support

* Tue Feb 14 2006 Marc Maurer <uwog@abisource.com> 1:1.2.2-2.fc5
- Rebuild for Fedora Extras 5

* Sun Feb 05 2006 Marc Maurer <uwog@abisource.com> 1:1.2.2-1.fc5
- Update to 1.2.2

* Mon Jan 30 2006 Marc Maurer <uwog@abisource.com> 1:1.2.1-1.fc5
- Update to 1.2.1
- Drop glib Require

* Sat Oct 22 2005 Marc Maurer <uwog@abisource.com> 1:1.2.0-1.fc5
- Update to 1.2.0

* Wed Oct  5 2005 Marc Maurer <uwog@abisource.com> 1:1.1.6-4.fc5
- Add dist flag to the release number

* Mon Apr  4 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1:1.1.6-3
- make in %%build
- disable bad buildroot rpaths in libs, don't use %%makeinstall
- require %%{epoch} of main package in -devel package (Fridrich Strba)

* Thu Mar 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1:1.1.6-2
- add dep glib2-devel for pkgconfig in -devel package
- include %%{_libdir}/enchant dir in main package
- make -devel package require exact VR of main package
- use -p /sbin/ldconfig in scriptlets

* Mon Mar 28 2005 Marc Maurer <uwog@abisource.com> 1:1.1.6-1
- update to 1.1.6
- drop the manpage patch (RH#145010#)
- fix version numbers in the spec changelog

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.1.5-3
- rebuild with gcc4

* Fri Jan 14 2005 Caolan McNamara <caolanm@redhat.com> 1:1.1.5-2
- RH#145010# misformatted manpage

* Mon Dec 20 2004 Caolan McNamara <caolanm@redhat.com> 1:1.1.5-1
- initial fedora import

* Sun Aug 24 2003 Rui Miguel Seabra <rms@1407.org>
- update spec to current stat of affairs
- building from source rpm is now aware of --with and --without flags:
- --without aspell --without ispell --without myspell --with uspell

* Wed Jul 16 2003 Rui Miguel Seabra <rms@1407.org>
- take advantage of environment rpm macros

* Sun Jul 13 2003 Dom Lachowicz <cinamod@hotmail.com>
- Initial version
