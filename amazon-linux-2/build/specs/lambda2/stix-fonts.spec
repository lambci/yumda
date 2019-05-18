%global fontname stix
%global fontconf 61-%{fontname}

%global archivename STIXv%{version}

%global common_desc \
The mission of the Scientific and Technical Information Exchange (STIX) font \
creation project is the preparation of a comprehensive set of fonts that serve \
the scientific and engineering community in the process from manuscript \
creation through final publication, both in electronic and print formats.

Name:    %{fontname}-fonts
Version: 1.1.0
Release: 5%{?dist}
Summary: Scientific and engineering fonts

Group:   User Interface/X
License: OFL
URL:     http://www.stixfonts.org/
Source0:  http://downloads.sourceforge.net/stixfonts/%{archivename}.zip
Source10: stix-fonts-fontconfig.conf
Source11: stix-fonts-math-fontconfig.conf

BuildArch:     noarch
BuildRequires: fontpackages-devel
Requires:      fontpackages-filesystem

Obsoletes:     stix-fonts-doc < 1.1.0

Prefix: %{_prefix}

%description
%common_desc

This package includes base Unicode fonts containing most glyphs for standard
use in the usual four styles.

%_font_pkg -f %{fontconf}.conf STIX-*otf
%doc License/*.pdf *.pdf


%package -n %{fontname}-math-fonts
Summary:   Scientific and engineering fonts, PUA glyphs
Requires:  %{name} = %{version}-%{release}

Obsoletes: stix-integrals-fonts < 1.1.0
Obsoletes: stix-pua-fonts < 1.1.0
Obsoletes: stix-sizes-fonts < 1.1.0
Obsoletes: stix-variants-fonts < 1.1.0

Prefix: %{_prefix}

%description -n %{fontname}-math-fonts
%common_desc

This package includes one symbol font completing the four faces in the main
%{name} package. It replaces the heap of confusing fontlets in the first Stix
release.

%_font_pkg -n math -f %{fontconf}-math.conf STIXMath*otf


%prep
%setup -q -c


%build


%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p Fonts/STIX-Word/*.otf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE10} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}.conf
install -m 0644 -p %{SOURCE11} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-math.conf

for fconf in %{fontconf}.conf \
             %{fontconf}-math.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.0-5
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.0-3
- Upstream changed their tarball with new pdf, rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 8 2012 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.1.0-1
— Update to new stable release
— Major refactoring now that some sanity prevailed upstream in font naming
  Be careful if you used the old font family names

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 25 2010 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.0.0-1
— Update to non-beta release
— Switch licensing to OFL
— Add -doc subpackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 0.9-13
— Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 0.9-12
— Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-11
— prepare for F11 mass rebuild, new rpm and new fontpackages

* Fri Jan 16 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-10
‣ Convert to new naming guidelines

* Sun Nov 23 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-9
ᛤ ‘rpm-fonts’ renamed to “fontpackages”

* Fri Nov 14 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-8
▤ Rebuild using new « rpm-fonts »

* Fri Jul 11 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.9-7
⌖ Fedora 10 alpha general package cleanup

* Thu Nov 1 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☺ 0.9-6
 ✓ Add some fontconfig aliasing rules
☢ 0.9-4
⚠ Initial experimental packaging
