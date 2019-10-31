%global fontname    dejavu
%global archivename %{name}-%{archiveversion}

#global alphatag .20080512svn2226
#global alphatag .rc1

#global archiveversion 2.24-20080512-2226
%global archiveversion %{version}

# Common description
%global common_desc \
The DejaVu font set is based on the “Bitstream Vera” fonts, release 1.10. Its\
purpose is to provide a wider range of characters, while maintaining the \
original style, using an open collaborative development process.


Name:    %{fontname}-fonts
Version: 2.33
Release: 6%{?alphatag}%{?dist}
Summary: DejaVu fonts

Group:     User Interface/X
License:   Bitstream Vera and Public Domain
URL:       http://%{name}.org/
Source0:   %{?!alphatag:http://downloads.sourceforge.net/%{fontname}}%{?alphatag:%{fontname}.sourceforge.net/snapshots}/%{archivename}.tar.bz2


# Older fontforge versions will not work due to sfd format changes
BuildRequires: fontforge >= 20080429
BuildRequires: perl(Font::TTF)
# Needed to compute unicode coverage
BuildRequires: unicode-ucd

BuildArch:     noarch
BuildRequires: fontpackages-devel

%description
%common_desc


%package common
Summary:  Common files for the Dejavu font set
Requires: fontpackages-filesystem

Obsoletes: dejavu-fonts-doc < 2.26-6
Obsoletes: %{name}-compat < 2.29-3
Obsoletes: %{name}-lgc-compat < 2.29-3

%description common
%common_desc

This package consists of files used by other DejaVu packages.


%package -n %{fontname}-sans-fonts
Summary:  Variable-width sans-serif font faces
Requires: %{name}-common = %{version}-%{release}

Conflicts: dejavu-fonts < 2.26-3
Conflicts: dejavu-fonts-experimental < 2.26-3

Obsoletes: %{name}-sans < 2.28-2

%description -n %{fontname}-sans-fonts
%common_desc

This package consists of the DejaVu sans-serif variable-width font faces, in
their unabridged version.

%_font_pkg -n sans -f *-%{fontname}-sans.conf DejaVuSans.ttf DejaVuSans-*.ttf DejaVuSansCondensed*.ttf


%package -n %{fontname}-serif-fonts
Summary:  Variable-width serif font faces
Requires: %{name}-common = %{version}-%{release}

Conflicts: dejavu-fonts < 2.26-3
Conflicts: dejavu-fonts-experimental < 2.26-3

Obsoletes: %{name}-serif < 2.28-2

%description -n %{fontname}-serif-fonts
%common_desc

This package consists of the DejaVu serif variable-width font faces, in their
unabridged version.

%_font_pkg -n serif -f *-%{fontname}-serif.conf DejaVuSerif.ttf DejaVuSerif-*.ttf DejaVuSerifCondensed*.ttf


%package -n %{fontname}-sans-mono-fonts
Summary:  Monospace sans-serif font faces
Requires: %{name}-common = %{version}-%{release}

Conflicts: dejavu-fonts < 2.26-3
Conflicts: dejavu-fonts-experimental < 2.26-3

Obsoletes: %{name}-sans-mono < 2.28-2

%description -n %{fontname}-sans-mono-fonts
%common_desc

This package consists of the DejaVu sans-serif monospace font faces, in their
unabridged version.

%_font_pkg -n sans-mono -f *-%{fontname}-sans-mono.conf DejaVuSansMono*.ttf


%package -n %{fontname}-lgc-sans-fonts
Summary:  Variable-width sans-serif font faces, Latin-Greek-Cyrillic subset
Requires: %{name}-common = %{version}-%{release}

Conflicts: dejavu-lgc-fonts < 2.26-3

Obsoletes: %{name}-lgc-sans < 2.28-2

%description -n %{fontname}-lgc-sans-fonts
%common_desc

This package consists of the DejaVu sans-serif variable-width font faces, with
unicode coverage restricted to Latin, Greek and Cyrillic.

%_font_pkg -n lgc-sans -f *-%{fontname}-lgc-sans.conf DejaVuLGCSans.ttf DejaVuLGCSans-*.ttf DejaVuLGCSansCondensed*.ttf


%package -n %{fontname}-lgc-serif-fonts
Summary:  Variable-width serif font faces, Latin-Greek-Cyrillic subset
Requires: %{name}-common = %{version}-%{release}

Conflicts: dejavu-lgc-fonts < 2.26-3

Obsoletes: %{name}-lgc-serif < 2.28-2

%description -n %{fontname}-lgc-serif-fonts
%common_desc

This package consists of the DejaVu serif variable-width font faces, with
unicode coverage restricted to Latin, Greek and Cyrillic.

%_font_pkg -n lgc-serif -f *-%{fontname}-lgc-serif.conf DejaVuLGCSerif.ttf DejaVuLGCSerif-*.ttf DejaVuLGCSerifCondensed*.ttf


%package -n %{fontname}-lgc-sans-mono-fonts
Summary:  Monospace sans-serif font faces, Latin-Greek-Cyrillic subset
Requires: %{name}-common = %{version}-%{release}

Conflicts: dejavu-lgc-fonts < 2.26-3

Obsoletes: %{name}-lgc-sans-mono < 2.28-2

%description -n %{fontname}-lgc-sans-mono-fonts
%common_desc

This package consists of the DejaVu sans-serif monospace font faces, with
unicode coverage restricted to Latin, Greek and Cyrillic.

%_font_pkg -n lgc-sans-mono -f *-%{fontname}-lgc-sans-mono.conf DejaVuLGCSansMono*.ttf


%prep
%setup -q -n %{archivename}

%build
make %{?_smp_mflags} VERSION=%{version} FC-LANG="" \
     BLOCKS=/usr/share/unicode/ucd/Blocks.txt UNICODEDATA=/usr/share/unicode/ucd/UnicodeData.txt

# Stop the desktop people from complaining this file is too big
bzip2 -9 build/status.txt


%check
make check


%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p build/*.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

cd fontconfig
for fontconf in *conf ; do
  install -m 0644 -p $fontconf %{buildroot}%{_fontconfig_templatedir}
  ln -s %{_fontconfig_templatedir}/$fontconf \
        %{buildroot}%{_fontconfig_confdir}/$fontconf
done


%clean
rm -fr %{buildroot}


%files common
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS LICENSE NEWS README
%doc build/unicover.txt build/status.txt.bz2


%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.33-6
- Mass rebuild 2013-12-27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Paul Flo Williams <paul@frixxon.co.uk>
- 2.33-2
- Get Unicode data from unicode-ucd. Fixes FTBFS bug #748522

* Mon Apr 04 2011 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.33-1
— Improved Hebrew and Armenian

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 2.32-2
– Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.32-1

* Tue Jun  3 2010 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.31-1
— drop Serif Condensed Italic naming patch

* Mon Sep  7 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.30-2
— patch to fix bug #505129 Serif Condensed Italic is not Serif Condensed

* Sun Sep  6 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.30-1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 2.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.29-3
— remove pre-F11 compatibility metapackage

* Sun Mar 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.29-2
— Make sure F11 font packages have been built with F11 fontforge

* Sat Mar 14 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.29-1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 2.28-6
— Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.28-5
— prepare for F11 mass rebuild, new rpm and new fontpackages
— drop compatibility provides as announced at F11 alpha time

* Thu Feb  5 2009 <nicolas.mailhot at laposte.net>
- 2.28-4
✓ Test build with new fontpackages and in-rpm auto-font-provides

* Fri Jan 16 2009 <nicolas.mailhot at laposte.net>
- 2.28-3
— Fix lgc-serif obsoletes

* Thu Jan 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.28-2
— Update URL
— update for new naming guidelines
– warning: provides for the old names will be dropped before F11 beta

* Sun Dec 21 2008 <nicolas.mailhot at laposte.net>
- 2.28-1
❄ Update to latest release
❅ Drop upstreamed fontconfig patch
❆ Remove DejaVu from most summaries


* Sat Dec  6 2008 <nicolas.mailhot at laposte.net>
- 2.27-7
߹ Add explicit conflicts to help yum

* Sun Nov 23 2008 <nicolas.mailhot at laposte.net>
- 2.27-5
ᛤ ‘rpm-fonts’ renamed to “fontpackages”

* Tue Nov 12 2008 <nicolas.mailhot at laposte.net>
- 2.27-4
▤ Tweak using new « rpm-fonts »

* Mon Nov 10 2008 <nicolas.mailhot at laposte.net>
- 2.26-7
▤ Rebuild using new « rpm-fonts »

* Sun Nov 9 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.26-6
⧎ Package split reorganisation, following font family lines
ⵞ Create compat packages to ease switchover at F11 time (to be discontinued
  for F12)
⬳ compress status file

* Wed Sep 3 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.26-2
⚙ Rebuild with pre-F10-freeze fontforge

* Sun Jul 26 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 2.26-1
Բ New release at last

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 2.25-4
- note Public Domain contributions

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 2.25-3
- fix license tag

* Fri Jul 11 2008 <nicolas.mailhot at laposte.net>
- 2.25-2
⌖ Fedora 10 alpha general package cleanup

* Mon May 19 2008 <nicolas.mailhot at laposte.net>
- 2.25-1
❋ 2.25 final

* Fri Apr 4 2008 <nicolas.mailhot at laposte.net>
- 2.24-3
⚕ Fix source URL

* Tue Mar 18 2008 <nicolas.mailhot at laposte.net>
- 2.24-2
✓ rebuild for new fontforge

* Mon Mar 10 2008 <nicolas.mailhot at laposte.net>
☺ 2.24-1
✓ 2.24 final

* Tue Mar 4 2008 <nicolas.mailhot at laposte.net>
☺ 2.24-0.2.rc1
✓ rc time

* Mon Mar 3 2008 <nicolas.mailhot at laposte.net>
☺ 2.24-0.1.20080228svn2189
✓ early 2.24 test build, check new fontforge

* Sun Jan 20 2008 <nicolas.mailhot at laposte.net>
☺ 2.23-1
✓ 2.23 final

* Thu Dec 9 2007 <nicolas.mailhot at laposte.net>
☺ 2.22-1
✓ 2.22 final

* Thu Dec 6 2007 <nicolas.mailhot at laposte.net>
☺ 2.22-0.1.20071206svn2135
✓ 2.22 rc phase started
✓ sync with guidelines

* Sun Oct 28 2007 <nicolas.mailhot at laposte.net>
☺ 2.21-1
✓ 2.21 final

* Sat Oct 27 2007 <nicolas.mailhot at laposte.net>
☺ 2.21-0.4.20071027svn2023
✓ Fedora fontconfig files dropped (merged upstream)

* Wed Oct 25 2007 <nicolas.mailhot at laposte.net>
☺ 2.21-0.3.20071025svn2022
 ✓ Makefile patch dropped (merged upstream)
 ✓ add -f to fc-cache calls
 ✓ completely align LGC and FULL fontconfig rules
 ✓ remove / from directory macros

* Sun Oct 21 2007 <nicolas.mailhot at laposte.net>
☢ 2.21-0.2.20071017svn2019
⚠ Still very experimental version:
  ✓ update makefile patch
  ✓ split lgc hinting file like in the other packages
  ✓ move lgc to prio 58 as should have been done when liberation was added

* Sun Oct 21 2007 <nicolas.mailhot at laposte.net>
☢ 2.21-0.1.20071014svn2016
⚠ Very experimental version to test major changes:
  ✓ new fontforge version
  ✓ use of a real makefile at last
  ✓ replacing standalone lgc package with subpackage generated with the rest

* Tue Sep 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.20-1
✓ 2.20 final
✓ bugfix release (Hebrew fixes mostly)

* Sat Aug 11 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.19-1
✓ 2.19 final
✓ expand macro use

* Sun Jul 1 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.18-1
✓ 2.18 final
✓ Major new release adding Tifinagh (ⵞⵥⴼⴻ), N'ko (ߝߧߜ) and Georgian (ლფჱႫႿ)
  (Georgian created by Besarion Paata Gugushvili ბესარიონ პაატა გუგუშვილი)

* Wed Jun 27 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.18-0.2.rc1
✓ 2.18-rc1

* Sun Jun 3 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☢ 2.18-0.1.20070616svn1889
⚠ early snapshot to test new fontforge

* Sun Jun 3 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.17-5
✓ declare DejaVu a valid Bitstream Prima™ substitute

* Thu May 31 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.17-3
✓ small spec cleanups

* Sat May 26 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.17-2
✓ perl-Font-TTF has been fixed upstream, use perl(Font::TTF) BR
✓ remove comment about /etc/fonts/conf.d ownership, as it's now owned
   by filesystem

* Sun May 13 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.17-1
✓ rebase scriptlets from guidelines
✓ fontforge broke compat: BR the current version, ask for a version bump
  before 2.18 is released
✓ simplify font directory naming
✓ clean up fc5 obsoletes
✓ remove technical mes files from doc

* Fri May 11 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.17-0.3.rc1
✓ fontconfig setup has stabilized and can be marked noreplace now
☺ 2.17-0.2.rc1
✓ mimick Vera unhint conf split
☺ 2.17-0.1.rc1
✓ 2.17 rc1
✓ make room for liberations font conf file

* Mon Apr 2 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.16-1

* Tue Mar 20 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.16-0.1.20070319svn1699
✓ early snapshot to account for F7T3 freeze

* Tue Jan 30 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 2.14-2
✓ Adds Dejavu Sans Oblique small fixes (by Ben Laenen to address Debian
  bug #408311, collected by Davide Viti)

* Sun Jan 21 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
✓ 2.14 final
