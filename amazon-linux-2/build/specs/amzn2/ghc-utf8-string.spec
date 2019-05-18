# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name utf8-string

Name:           ghc-%{pkg_name}
Version:        0.3.7
Release:        8%{?dist}
Summary:        Support for reading and writing UTF8 Strings

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
Patch0:         utf8-string-0.3.7-bytestring-in-base-flag.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
# End cabal-rpm deps

%description
A UTF8 layer for IO and Strings. The utf8-string package provides operations
for encoding UTF8 strings to Word8 lists and back, and for reading and writing
UTF8 without truncation.


%package devel
Summary:        Haskell %{pkg_name} library development files
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides the Haskell utf8-string library development files.


%prep
%setup -q -n %{pkg_name}-%{version}
%patch0 -p1 -b .orig


%build
%ghc_lib_build


%install
%ghc_lib_install


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun  3 2013 Jens Petersen <petersen@redhat.com> - 0.3.7-7
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.3.7-5
- update with cabal-rpm
- unset bytestring-in-base flag

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 0.3.7-3
- change prof BRs to devel

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 0.3.7-2
- add license to ghc_files

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.3.7-1
- update to 0.3.7 and cabal2spec-0.25.2

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.6-11.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.3.6-11.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.3.6-11.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.3.6-11
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 0.3.6-10
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.3.6-9
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 0.3.6-7
- update to cabal2spec-0.22.4

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-6
- drop -o obsoletes
- build with hscolour

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-5
- update to latest macros, hscolour and drop doc pkg (cabal2spec-0.22.2)

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-4
- use ghc_strip_dynlinked (ghc-rpm-macros-0.6.0)

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-3
- ghc-6.12.2 doesn't provide utf8-string again
- condition ghc_lib_package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.3.6-2
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 0.3.6-1
- update to 0.3.6
- update packaging for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.5-2
- Added patch from Jens Petersen for better descriptions

* Fri Jun 12 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.5-1
- Updated to version 0.3.5

* Fri Jun  5 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.4-2
- Updated to new cabal2spec

* Fri May 29 2009 Zachary Oglesby <zoglesby@fedoraproject.org> - 0.3.4-1
- initial packaging for Fedora created by cabal2spec

