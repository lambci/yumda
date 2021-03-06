# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name primitive

Name:           ghc-%{pkg_name}
Version:        0.5.0.1
Release:        4%{?dist}
Summary:        Primitive memory-related operations

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros

Prefix: %{_prefix}

%description
This package provides various primitive memory-related operations.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install

for file in $(grep -v package.conf.d %{name}-devel.files); do rm -rf %{buildroot}$file || :; done


%files -f %{name}.files
%license LICENSE
%exclude %{ghclibdir}/package.conf.d


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jens Petersen <petersen@redhat.com> - 0.5.0.1-3
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Jens Petersen <petersen@redhat.com> - 0.5.0.1-1
- update to 0.5.0.1

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com>
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.4.1-2
- change prof BRs to devel

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.4.1-1
- update to 0.4.1

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 0.4.0.1-1
- update to 0.4.0.1 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.1-2.1
- rebuild with new gmp without compat lib

* Tue Sep 13 2011 Jens Petersen <petersen@redhat.com> - 0.3.1-2
- rebuild against newer ghc-rpm-macros

* Thu Sep  8 2011 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- BSD license

* Thu Sep  8 2011 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 0.3.1-0
- initial packaging for Fedora automatically generated by cabal2spec-0.24.1
