# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name network

%bcond_with tests

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        2.4.1.2
Release:        32%{?dist}
Summary:        Low-level networking interface

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-parsec-devel
BuildRequires:  ghc-unix-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-test-framework-quickcheck2-devel
%endif
# End cabal-rpm deps

%description
Haskell basic networking library.


%package devel
Summary:        Haskell %{pkg_name} library development files
Provides:       %{name}-static = %{version}-%{release}
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the Haskell %{pkg_name} library development files.


%prep
%setup -q -n %{pkg_name}-%{version}
# Use rpm's config.* to support new archs like ppc64le
cp -f /usr/lib/rpm/config.{guess,sub} .

%build
%ghc_lib_build


%install
%ghc_lib_install


%check
%if %{with tests}
%cabal test
%endif


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files
%doc examples


%changelog
* Mon Jun  9 2014 Jens Petersen <petersen@redhat.com> - 2.4.1.2-32
- update to cabalrpm-0.8.11
- Use rpm's config.* to support new archs like ppc64le (Karsten Hopp)

* Mon Mar 17 2014 Jens Petersen <petersen@redhat.com> - 2.4.1.2-31
- bump release over haskell-platform

* Fri Jan 31 2014 Jens Petersen <petersen@redhat.com> - 2.4.1.2-30
- spec file revived using cabal-rpm-0.8.8

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 2.3.0.11-1
- update to 2.3.0.11

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 2.3.0.5-1
- update to 2.3.0.5 for haskell-platform-2011.4.0.0
- cabal2spec-0.25.1
- includes examples in devel doc

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.3.0.2-5.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.3.0.2-5.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 2.3.0.2-5.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 2.3.0.2-5
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 2.3.0.2-4
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 2.3.0.2-3
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.3.0.2-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 2.3.0.2-1
- update to 2.3.0.2 for haskell-platform-2011.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 2.3-2
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 2.3-1
- update to 2.3

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 2.2.1.7-5
- update url and drop -o obsoletes

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 2.2.1.7-4
- update to latest macros, hscolour and drop doc pkg (cabal2spec-0.22.2)
- part of haskell-platform-2010.2.0.0

* Fri Jun 25 2010 Jens Petersen <petersen@redhat.com> - 2.2.1.7-3
- strip shared library (cabal2spec-0.21.4)

* Mon Apr 26 2010 Jens Petersen <petersen@redhat.com> - 2.2.1.7-2
- rebuild against ghc-6.12.2
- condition ghc_lib_package

* Tue Mar 23 2010 Jens Petersen <petersen@redhat.com> - 2.2.1.7-1
- update to 2.2.1.7 for haskell-platform-2010.1.0.0

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 2.2.1.5-1
- update to 2.2.1.5 (haskell-platform-2009.3.1)
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_lib_package and ghc_pkg_deps
- build shared library
- drop redundant buildroot and its install cleaning

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 2.2.1.4-2
- version ghcdocdir to avoid conflict with ghc-doc-6.10.4 (#523884)

* Wed Sep 16 2009 Jens Petersen <petersen@redhat.com> - 2.2.1.4-1
- initial packaging for Fedora created by cabal2spec
