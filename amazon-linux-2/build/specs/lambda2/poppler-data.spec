%global _trivial .0
%global _buildid .1
## to bootstrap and avoid the circular dependency with ghostscript
## define this to be the ghostscript version
#define gs_bootstrap 9.06

Summary: Encoding files 
Name:    poppler-data
Version: 0.4.6
Release: 3%{?dist}%{?_trivial}%{?_buildid}
# The cMap data files installed by the poppler-data package are
# under the COPYING.adobe license
# cidToUnicode, nameToUnicode and unicodeMap data files
# are under the COPYING.gpl2 license
# Identity-UTF16-H is under GPLv3+ license
License: BSD and GPLv2 and GPLv3+
Group:   Development/Libraries
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-data-%{version}.tar.gz
Source1: http://downloads.sourceforge.net/project/cmap.adobe/cmapresources_identity0.tar.z
# extracted from ghostscript-9.05 tarball
Source2: Identity-UTF16-H
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

%if ! 0%{?gs_bootstrap:1}
BuildRequires: ghostscript
%endif
%global gs_ver %(gs --version 2>/dev/null || echo %{gs_bootstrap})

Prefix: %{_prefix}

%description
This package consists of encoding files for poppler.  When installed,
the encoding files enables poppler to correctly render CJK and Cyrillic 
properly.


%prep
%setup -q -a 1

%build
# intentionally left blank

%install
make install  DESTDIR=$RPM_BUILD_ROOT datadir=%{_datadir}

# manually install Identity-* files
# http://bugzilla.redhat.com/842351
install -m644 -p %{SOURCE2} ai0/CMap/Identity-* $RPM_BUILD_ROOT%{_datadir}/poppler/cMap/

# create cmap symlinks for ghostscript
mkdir -p %{buildroot}%{_datadir}/ghostscript/%{gs_ver}/Resource/CMap/
cmap_files=$(find %{buildroot}%{_datadir}/poppler/cMap/ -type f | sed -e "s|%{buildroot}%{_datadir}|../../../..|g")
pushd %{buildroot}%{_datadir}/ghostscript/%{gs_ver}/Resource/CMap/
for target in ${cmap_files} ; do
ln -s $target
test -f $(basename $target)
done
popd


%files
%defattr(-,root,root,-)
%license COPYING COPYING.adobe COPYING.gpl2
%{_datadir}/poppler/
%dir %{_datadir}/ghostscript/%{gs_ver}
%dir %{_datadir}/ghostscript/%{gs_ver}/Resource
%{_datadir}/ghostscript/%{gs_ver}/Resource/CMap/


%changelog
* Thu Jun 27 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Jun 20 2019 Paul Ezvan <paulezva@amazon.com> - 0.4.6-3.1
- Rebuild to match Ghostscript version

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.4.6-3
- Mass rebuild 2013-12-27

* Mon Apr  8 2013 Marek Kasik <mkasik@redhat.com> 0.4.6-2.1
- Update License field
- Resolves: #905472

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.6-1
- poppler-data-0.4.6

* Tue Sep 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-6
- create ghostscript cmap symlinks (#842351)

* Sat Sep 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-5
- Identity-UTF16-H too (#842351)

* Sat Sep 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-4
- CMap file "Identity-H" missing due to poppler-data change/cleanup (#842351)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-1
- poppler-data-0.4.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.4-1
- poppler-data-0.4.4

* Thu Jul 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.3-1
- poppler-data-0.4.3

* Sat May 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-1
- poppler-data-0.4.2

* Mon Dec 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-1
- poppler-data-0.4.0

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.3.1-1
- poppler-data-0.3.1

* Tue Sep 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.3.0-1
- poppler-data-0.3.0
- License: BSD and GPLv2

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.1-1
- first try at separate poppler-data

