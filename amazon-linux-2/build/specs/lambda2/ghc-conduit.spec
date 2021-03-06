# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name conduit

Name:           ghc-%{pkg_name}
Version:        1.0.3
Release:        2%{?dist}
Summary:        Streaming data processing library

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-lifted-base-devel
BuildRequires:  ghc-monad-control-devel
BuildRequires:  ghc-resourcet-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-transformers-base-devel
BuildRequires:  ghc-void-devel
# End cabal-rpm deps

Prefix: %{_prefix}

%description
Conduit is a solution to the streaming data problem, allowing for production,
transformation, and consumption of streams of data in constant memory.
It is an alternative to lazy I/O which guarantees deterministic resource
handling, and fits in the same general solution space as enumerator, iteratee,
and pipes.


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

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 1.0.3-1
- update to 1.0.3
- update to new simplified Haskell Packaging Guidelines

* Tue Mar 12 2013 Jens Petersen <petersen@redhat.com> - 1.0.2-1
- update to 1.0.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Jens Petersen <petersen@redhat.com> - 0.5.2.7-1
- update to 0.5.2.7 with cabal-rpm
- update description

* Thu Jul 26 2012 Jens Petersen <petersen@redhat.com> - 0.4.2-3
- rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Jens Petersen <petersen@redhat.com> - 0.4.2-1
- update to 0.4.2

* Tue May  1 2012 Jens Petersen <petersen@redhat.com> - 0.4.1.1-2
- rebuild

* Wed Apr 25 2012 Jens Petersen <petersen@redhat.com> - 0.4.1.1-1
- update to 0.4.1.1
- depends on void

* Tue Apr 10 2012 Jens Petersen <petersen@redhat.com> - 0.3.0-1
- update to 0.3.0
- depends on resourcet

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.2.2-2
- add license to ghc_files

* Tue Mar  6 2012 Jens Petersen <petersen@redhat.com> - 0.2.2-1
- update to 0.2.2

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 0.2.0-1
- BSD license
- needs lifted-base

* Tue Feb  7 2012 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org>
- spec file template generated by cabal2spec-0.25.4
