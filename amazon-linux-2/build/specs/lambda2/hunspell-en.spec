%define _trivial .0
%define _buildid .1

Name: hunspell-en
Summary: English hunspell dictionaries
%define upstreamid 20121024
Version: 0.%{upstreamid}
Release: 6%{?dist}%{?_trivial}%{?_buildid}
#svn export https://wordlist.svn.sourceforge.net/svnroot/wordlist/trunk wordlist
Source0: wordlist-%{upstreamid}.tar.xz
Source1: http://en-gb.pyxidium.co.uk/dictionary/en_GB.zip
#See http://mxr.mozilla.org/mozilla/source/extensions/spellcheck/locales/en-US/hunspell/mozilla_words.diff?raw=1
Patch0: mozilla_words.patch
Patch1: en_GB-singleletters.patch
Patch2: en_GB.two_initial_caps.patch
#See http://sourceforge.net/tracker/?func=detail&aid=2355344&group_id=10079&atid=1014602
#filter removes words with "." in them
Patch3: en_US-strippedabbrevs.patch
#See https://sourceforge.net/tracker/?func=detail&aid=2987192&group_id=143754&atid=756397
#to allow "didn't" instead of suggesting change to typographical apostrophe
Patch4: hunspell-en-allow-non-typographical.marks.patch
#See https://sourceforge.net/tracker/?func=detail&aid=3012183&group_id=10079&atid=1014602
#See https://bugzilla.redhat.com/show_bug.cgi?id=619577 add SI and IEC prefixes
Patch5: hunspell-en-SI_and_IEC.patch
#See https://sourceforge.net/tracker/?func=detail&aid=3175662&group_id=10079&atid=1014602 obscure Calender hides misspelling of Calendar
Patch6: hunspell-en-calender.patch
#valid English words that are archaic or rare in en-GB but not in en-IE
Patch7: en_IE.supplemental.patch

# Amazon Patches
Patch1000: 0001-adjust-C-03-standard.patch 

Group: Applications/Text
URL: http://wordlist.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License: LGPLv2+ and LGPLv2 and BSD
BuildArch: noarch
BuildRequires: aspell, zip
Requires: hunspell
Requires: hunspell-en-US = %{version}-%{release}
Requires: hunspell-en-GB = %{version}-%{release}

Prefix: %{_prefix}

%description
English (US, UK, etc.) hunspell dictionaries

%package US
Requires: hunspell
Summary: US English hunspell dictionaries
Group: Applications/Text
Prefix: %{_prefix}

%description US
US English hunspell dictionaries

%package GB
Requires: hunspell
Summary: UK English hunspell dictionaries
Group: Applications/Text
Prefix: %{_prefix}

%description GB
UK English hunspell dictionaries

%prep
%setup -q -n wordlist
%setup -q -T -D -a 1 -n wordlist
%patch0 -p1 -b .mozilla
%patch1 -p1 -b .singleletters
%patch2 -p1 -b .two_initial_cap
%patch3 -p1 -b .strippedabbrevs
%patch4 -p1 -b .allow-non-typographical
%patch5 -p1 -b .SI_and_IEC
%patch6 -p1 -b .calender
%patch7 -p1 -b .en_IE

%patch1000 -p3

%build
export CXXFLAGS="-std=c++03"
make
cd scowl/speller
make hunspell
for i in README_en_CA.txt README_en_US.txt; do
  if ! iconv -f utf-8 -t utf-8 -o /dev/null $i > /dev/null 2>&1; then
    iconv -f ISO-8859-1 -t UTF-8 $i > $i.new
    touch -r $i $i.new
    mv -f $i.new $i
  fi
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/myspell
cp -p en_*.dic en_*.aff $RPM_BUILD_ROOT%{_datadir}/myspell
cd scowl/speller
cp -p en_*.dic en_*.aff $RPM_BUILD_ROOT%{_datadir}/myspell

pushd $RPM_BUILD_ROOT%{_datadir}/myspell/
en_GB_aliases="en_AG en_AU en_BS en_BW en_BZ en_DK en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NG en_NZ en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_GB_aliases; do
	ln -s en_GB.aff $lang.aff
	ln -s en_GB.dic $lang.dic
done
en_US_aliases="en_PH"
for lang in $en_US_aliases; do
	ln -s en_US.aff $lang.aff
	ln -s en_US.dic $lang.dic
done
popd

%files
%defattr(-,root,root,-)
%license scowl/speller/README_en_CA.txt
%{_datadir}/myspell/*
%exclude %{_datadir}/myspell/en_GB.*
%exclude %{_datadir}/myspell/en_US.*

%files US
%defattr(-,root,root,-)
%license scowl/speller/README_en_US.txt
%{_datadir}/myspell/en_US.*

%files GB
%defattr(-,root,root,-)
%license README_en_GB.txt
%{_datadir}/myspell/en_GB.*

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Feb 20 2017 Caolán McNamara <caolanm@redhat.com> - 0.20121024-6
- Resolves: rhbz#1376031 Zambia english is named with dash instead of underscore

* Wed Jan 08 2014 Caolán McNamara <caolanm@redhat.com> - 0.20121024-5
- Resolves: rhbz#1048864 accidentally included prebuilt binary

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.20121024-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121024-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Caolán McNamara <caolanm@redhat.com> - 0.20121024-2
- wordlist/scowl/speller/aspell/en_phonet.dat under bare LGPLv2

* Wed Oct 24 2012 Caolán McNamara <caolanm@redhat.com> - 0.20121024-1
- latest version
- drop integrated hunspell-en-irregular-plural-possessive.patch

* Thu Oct 11 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-9
- add possessive forms of irregular plurals for en-US, e.g. men's, women's

* Mon Aug 27 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-8
- Related: rhbz#850709 fix requires

* Mon Aug 27 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-7
- Resolves: rhbz#850709 allow installation of en-US and en-GB standalone

* Wed Aug 1 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-6
- Related: rhbz#573516 we don't need hunspell to build hunspell-en

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110318-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-4
- add Malawian alias

* Tue Apr 10 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-3
- making a hames of it
- add Zambian alias

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110318-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 18 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110318-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110112-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110112-3
- Resolves: rhbz#675550 add Haskell as a known proper noun

* Thu Jan 13 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110112-1
- latest version

* Sun Jan 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110108-1
- latest version

* Tue Jan 04 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110104-1
- latest version

* Tue Dec 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101221-1
- latest version

* Tue Dec 14 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101211-1
- latest version

* Wed Dec 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101207-1
- latest version

* Fri Jul 30 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-6
- Resolves: rhbz#619577 add JEDEC prefixes

* Fri Jul 30 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-5
- Resolves: rhbz#619577 add SI and IEC prefixes

* Mon Jun 14 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-4
- Resolves: rhbz#603773 allow just non-typographical apostrophes

* Sun Jun 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-3
- Resolves: rhbz#600860 generate a higher level en-US dict

* Thu Apr 15 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-2
- allow non-typographical apostrophes

* Wed Mar 31 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-1
- latest version

* Mon Mar 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100308-1
- latest version

* Sat Jul 25 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-7
- add extra mozilla REPs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090216-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-5
- tidy spec

* Fri Jun 12 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-4
- extend coverage

* Sat Jun 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-3
- Change two suspicious words with two initial capitals in en_GB
  from ADte TEirtza to ADTe Teirtza

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090216-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-1
- fix upstreamed

* Mon Feb 16 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090208-1
- latest version

* Wed Jan 14 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090114-1
- latest version

* Sun Jan 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090110-1
- latest version

* Thu Dec 18 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081216-1
- latest version

* Sat Dec 06 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081205-1
- latest version

* Tue Dec 02 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081202-1
- latest version

* Sat Nov 29 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081129-1
- mozilla blog ... webmistresses signature range integrated

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081127-2
- abbrevs are always stripped out from US/CA dicts
- some single characters are missing from en_GB

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081127-1
- hardcoded path dropped upstream

* Tue Nov 25 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081124-1
- latest version, i.e +Barack +Obama and co.

* Fri Aug 29 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080829-1
- latest version

* Fri Feb 08 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080207-1
- canonical upstream source

* Thu Feb 07 2008 Caolán McNamara <caolanm@redhat.com> - 0.20061130-5
- apply mozilla word diff

* Tue Jan 15 2008 Caolán McNamara <caolanm@redhat.com> - 0.20061130-4
- clean up spec

* Mon Sep 17 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061130-3
- new varient alias

* Thu Aug 09 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061130-2
- clarify licence

* Fri Jun 01 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061130-1
- update to latest dictionaries

* Thu Feb 08 2007 Caolán McNamara <caolanm@redhat.com> - 0.20040623-2
- update to new spec guidelines

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20040623-1
- initial version
