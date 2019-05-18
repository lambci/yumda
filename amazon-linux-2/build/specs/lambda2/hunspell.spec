Name:      hunspell
Summary:   A spell checker and morphological analyzer library
Version:   1.3.2
Release: 15%{?dist}.0.2
Source:    http://downloads.sourceforge.net/%{name}/hunspell-%{version}.tar.gz
Group:     System Environment/Libraries
URL:       http://hunspell.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:   LGPLv2+ or GPLv2+ or MPLv1.1
BuildRequires: ncurses-devel
%ifarch %{ix86} x86_64
BuildRequires: valgrind
%endif
Requires:  hunspell-en-US
Patch0: hunspell.rhbz759647.patch
Patch1: hunspell.rhbz918938.patch
Patch2: hunspell-aarch64.patch
Patch3: 0001-Resolves-rhbz-1261421-crash-on-mashing-hangul-korean.patch
Patch4: hunspell.rhbz915448.patch

Prefix: %{_prefix}

%description
Hunspell is a spell checker and morphological analyzer library and program 
designed for languages with rich morphology and complex word compounding or 
character encoding. Hunspell interfaces: Ispell-like terminal interface using 
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

%prep
%setup -q
%patch0 -p0 -b .rhbz759647
%patch1 -p0 -b .rhbz918938
%patch2 -p1 -b .aarch64
%patch3 -p1 -b .rhbz-1261421-crash-on-mashing-hangul-korean
%patch4 -p0 -b .rhbz915448

%build
configureflags="--disable-rpath --disable-static --without-ui --without-readline"

%define profilegenerate \
    CFLAGS="${RPM_OPT_FLAGS} -fprofile-generate"\
    CXXFLAGS="${RPM_OPT_FLAGS} -fprofile-generate"
%define profileuse \
    CFLAGS="${RPM_OPT_FLAGS} -fprofile-use"\
    CXXFLAGS="${RPM_OPT_FLAGS} -fprofile-use"

%configure $configureflags
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir $RPM_BUILD_ROOT%{_datadir}/myspell

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LGPL COPYING.MPL license.hunspell license.myspell
%{_libdir}/*.so.*
%{_datadir}/myspell
%{_bindir}/hunspell

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}/locale
%exclude %{_bindir}/affixcompress
%exclude %{_bindir}/makealias
%exclude %{_bindir}/munch
%exclude %{_bindir}/unmunch
%exclude %{_bindir}/analyze
%exclude %{_bindir}/chmorph
%exclude %{_bindir}/hzip
%exclude %{_bindir}/hunzip
%exclude %{_bindir}/ispellaff2myspell
%exclude %{_bindir}/wordlist2hunspell
%exclude %{_bindir}/wordforms

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 10 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.2-15
- Resolves: rhbz#1262755 bad UTF-8 char count in pipe mode

* Tue Mar 01 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.2-14
- Resolves: rhbz#1261421 crash on mashing hangul keyboard

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.3.2-13
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.2-12
- Mass rebuild 2013-12-27

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> - 1.3.2-11
- Resolves: rhbz#925562 support aarch64

* Wed Mar 13 2013 Caolán McNamara <caolanm@redhat.com> - 1.3.2-10
- Resolves: rhbz#918938 crash in danish thesaurus/spell interaction

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Caolán McNamara <caolanm@redhat.com> - 1.3.2-8
- Related: rhbz#850709 en-US available standalone

* Wed Aug 01 2012 Caolán McNamara <caolanm@redhat.com> - 1.3.2-6
- Resolves: rhbz#573516 have hunspell require hunspell-en to ensure
  at least one dictionary exists

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Caolán McNamara <caolanm@redhat.com> - 1.3.2-4
- Resolves: rhbz#813478 x86_64 valgrind spews, see rhbz#813780

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Caolán McNamara <caolanm@redhat.com> - 1.3.2-2
- Resolves: rhbz#759647 temp file name collision

* Tue May 24 2011 Caolán McNamara <caolanm@redhat.com> - 1.3.2-1
- Resolves: rhbz#706686 latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Caolán McNamara <caolanm@redhat.com> - 1.2.15-1
- latest version

* Fri Jan 07 2011 Caolán McNamara <caolanm@redhat.com> - 1.2.14-1
- latest version

* Wed Jan 05 2011 Caolán McNamara <caolanm@redhat.com> - 1.2.13-1
- latest version
- drop integrated backport.warnings.patch
- drop integrated backport.rhbz650503.patch

* Mon Nov 08 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.12-3
- Resolves: rhbz#650503 Arabic spellchecking crash

* Fri Nov 05 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.12-2
- Resolves: rhbz#648740 thousands of trailing empty rules spew

* Thu Jul 15 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.12-1
- latest version
- drop integrated hunspell-1.2.11-valgrind.patch
- drop integrated hunspell-1.2.11-koreansupport.patch

* Fri Jul 09 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.11-4
- use -fprofile-generate and -fprofile-use

* Mon Jul 05 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.11-3
- add korean Hangul syllable support

* Tue Jun 22 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.11-2
- use valgrind in make check

* Thu May 06 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.11-1
- Resolves: rhbz#589326 wrong malloc

* Fri Apr 30 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.10-1
- latest version

* Thu Mar 04 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.9-2
- Resolves: ooo#107768 hunspell-1.2.9-stacksmash.patch

* Wed Mar 03 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.9-1
- latest version, drop all upstreamed patchs

* Mon Mar 01 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.8-17
- Resolves: rhbz#569449 hu man dir now exists in filesystem

* Mon Jan 18 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.8-16
- Resolves: rhbz#554876 fix suggestmgr crash

* Tue Jan 05 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.8-15
- Remove bad const warnings

* Mon Dec 21 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-14
- Preserve timestamps

* Tue Dec 08 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-13
- Resolves: rhbz#544372 survive having no HOME

* Thu Jul 30 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-12
- handle some other interesting edge-cases

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-10
- run tests in check

* Thu Jul 09 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-9
- Resolves: rhbz#510360 unowned dirs
- fix up rpmlint warnings

* Tue Jul 07 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-8
- Resolves: rhbz#509882 ignore an empty LANGUAGE variable

* Fri Jun 26 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-7
- Related: rhbz#498556 default to something sensible in "C" locale
  for language

* Wed Jun 24 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-6
- Resolves: rhbz#507829 fortify fixes

* Fri May 01 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.8-5
- Resolves: rhbz#498556 fix default language detection

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.8-3
- tweak summary

* Wed Nov 19 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.8-2
- Resolves: rhbz#471085 in ispell compatible mode (-a), ignore
  -m option which means something different to ispell

* Sun Nov 02 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.8-1
- latest version

* Sat Oct 18 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.7-5
- sort as per "C" locale

* Fri Oct 17 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.7-4
- make wordlist2hunspell remove blank lines 

* Mon Sep 15 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.7-3
- Workaround rhbz#462184 uniq/sort problems with viramas

* Tue Sep 09 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.7-2
- add wordlist2hunspell

* Sat Aug 23 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.7-1
- latest version

* Tue Jul 29 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.6-1
- latest version

* Sun Jul 27 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.5-1
- latest version

* Tue Jul 22 2008 Kristian Høgsberg <krh@redhat.com> - 1.2.4.2-2
- Drop ABI breaking hunspell-1.2.2-xulrunner.pita.patch and fix the
  hunspell include in xulrunner.

* Fri Jun 18 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.4.2-1
- latest version

* Thu Jun 17 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.4-1
- latest version

* Fri May 16 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.2-3
- Resolves: rhbz#446821 fix crash

* Wed May 14 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.2-2
- give xulrunner what it needs so we can get on with it

* Fri Apr 18 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.2-1
- latest version
- drop integrated hunspell-1.2.1-1863239.badstructs.patch

* Wed Mar 05 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.1-6
- add ispellaff2myspell to devel

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-5
- Autorebuild for GCC 4.3

* Thu Jan 03 2008 Caolán McNamara <caolanm@redhat.com> - 1.2.1-4
- add hunspell-1.2.1-1863239.badstructs.patch

* Fri Nov 09 2007 Caolán McNamara <caolanm@redhat.com> - 1.2.1-2
- pkg-config cockup

* Mon Nov 05 2007 Caolán McNamara <caolanm@redhat.com> - 1.2.1-1
- latest version

* Mon Oct 08 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.12.2-2
- lang fix for man pages from Ville Skyttä

* Wed Sep 05 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.12.2-1
- next version

* Tue Aug 28 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.11.2-1
- next version

* Fri Aug 24 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.10-1
- next version

* Thu Aug 02 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.9-2
- clarify license

* Wed Jul 25 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.9-1
- latest version

* Wed Jul 18 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.8.2-1
- latest version

* Tue Jul 17 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.8-1
- latest version

* Sat Jul 07 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.7-1
- latest version
- drop integrated hunspell-1.1.5.freem.patch

* Fri Jun 29 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.6-1
- latest version
- drop integrated hunspell-1.1.4-defaultdictfromlang.patch
- drop integrated hunspell-1.1.5-badheader.patch
- drop integrated hunspell-1.1.5.encoding.patch

* Fri Jun 29 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5.3-5
- fix memory leak
  http://sourceforge.net/tracker/index.php?func=detail&aid=1745263&group_id=143754&atid=756395

* Wed Jun 06 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5.3-4
- Resolves: rhbz#212984 discovered problem with missing wordchars

* Tue May 22 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5.3-3
- Resolves: rhbz#240696 extend encoding patch to promote and add
  dictionary 8bit WORDCHARS to the ucs-2 word char list

* Mon May 21 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5.3-2
- Resolves: rhbz#240696 add hunspell-1.1.5.encoding.patch

* Mon May 21 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5.3-1
- patchlevel release

* Tue Mar 20 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5-2
- some junk in delivered headers

* Tue Mar 20 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.5-1
- next version

* Fri Feb 09 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.4-6
- some spec cleanups

* Fri Jan 19 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.4-5
- .pc

* Thu Jan 11 2007 Caolán McNamara <caolanm@redhat.com> - 1.1.4-4
- fix out of range

* Fri Dec 15 2006 Caolán McNamara <caolanm@redhat.com> - 1.1.4-3
- hunspell#1616353 simple c api for hunspell

* Wed Nov 29 2006 Caolán McNamara <caolanm@redhat.com> - 1.1.4-2
- add hunspell-1.1.4-defaultdictfromlang.patch to take locale as default
  dictionary

* Wed Oct 25 2006 Caolán McNamara <caolanm@redhat.com> - 1.1.4-1
- initial version
