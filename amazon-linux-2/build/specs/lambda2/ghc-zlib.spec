# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name zlib

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        0.5.4.1
Release:        27%{?dist}
Summary:        Compression and decompression in the gzip and zlib formats

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  zlib-devel%{?_isa}
# End cabal-rpm deps

Prefix: %{_prefix}

%description
This package provides a pure interface for compressing and decompressing
streams of data represented as lazy 'ByteString's. It uses the zlib C library
so it has high performance. It supports the zlib, gzip and raw
compression formats.

It provides a convenient high level API suitable for most tasks and for the few
cases where more control is needed it provides access to the full zlib feature
set.


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

* Wed Dec  4 2013 Jens Petersen <petersen@redhat.com> - 0.5.4.1-27
- bump release

* Sun Oct 27 2013 Jens Petersen <petersen@redhat.com> - 0.5.4.1-26
- tidy description

* Sun Oct 27 2013 Jens Petersen <petersen@redhat.com> - 0.5.4.1-25
- spec file updated with cabal-rpm-0.8.6

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 0.5.3.3-1
- update to 0.5.3.3

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 0.5.3.1-8
- rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan  2 2012 Jens Petersen <petersen@redhat.com> - 0.5.3.1-6
- update to cabal2spec-0.25.2
- use _isa
- include examples

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.3.1-5.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.5.3.1-5.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 0.5.3.1-5.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 0.5.3.1-5
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 0.5.3.1-4
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 0.5.3.1-3
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.5.3.1-2
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 0.5.3.1-1
- update to 0.5.3.1 for haskell-platform-2011.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 0.5.2.0-6
- update to cabal2spec-0.22.4

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-5
- rebuild with ghc-7.0.1

* Sat Sep  4 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-4
- add hscolour and doc obsolete (cabal2spec-0.22.2)
- part of haskell-platform-2010.2.0.0

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-3
- sync cabal2spec-0.22

* Sat Apr 24 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-2
- part of haskell-platform-2010.1.0.0
- rebuild against ghc-6.12.2

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.2.0-1
- update to 0.5.2.0 (haskell-platform-2009.3.1)
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common summary and common_description
- use ghc_lib_package and ghc_pkg_c_deps

* Sat Dec 26 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-12
- update to cabal2spec-0.20 and ghc-rpm-macros-0.4.0:
- use common_summary and common_description
- reenable debuginfo for stripping
- use ghc_requires, ghc_doc_requires, and ghc_prof_requires

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com>
- fix base Group and devel Summary
- only include docdir in devel if not shared build

* Wed Dec 16 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-11
- build for ghc-6.12.1
- added shared library support: needs ghc-rpm-macros 0.3.1
- use cabal_pkg_conf to generate package.conf.d file and use ghc-pkg recache

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-9
- buildrequires ghc-rpm-macros (cabal2spec-0.16)

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-8
- sync with cabal2spec-0.14

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-7
- update to cabal2spec-0.11:
- add devel subpackage
- use ix86 macro for archs and add alpha
- use global rather than define
- make devel subpackage own docdir for now

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Jens Petersen <petersen@redhat.com> - 0.5.0.0-5
- rebuild to fix unexpanded post preun macros
- add doc subpackage and BR ghc-doc
- add doc requires(post) ghc-doc

* Mon Dec 22 2008 Jens Petersen <petersen@redhat.com> - 0.5.0.0-4
- use bcond for doc and prof build flags (Till Maas, #426751)

* Mon Dec  1 2008 Jens Petersen <petersen@redhat.com> - 0.5.0.0-3
- sync with lib template:
  - add build_prof and build_doc
  - prof requires main package
  - update scriptlet macro names

* Tue Nov 25 2008 Jens Petersen <petersen@redhat.com> - 0.5.0.0-2
- build with ghc-6.10.1
- no longer buildrequire haddock09
- provide devel
- add exclusivearch for current ghc archs
- reindex haddock docs only when uninstalling in postun

* Tue Nov 11 2008 Bryan O'Sullivan <bos@serpentine.com> - 0.5.0.0-1
- Update to 0.5.0.0

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 0.4.0.4-2
- update for current rawhide
- add pkg_docdir and remove hsc_name
- use haddock09

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 0.4.0.4-1
- Revised to follow Haskell packaging guidelines

* Sun Feb 17 2008 Yaakov Nemoy <haskell.rpms@hexago.nl> - 0.4.0.2-1
- added in url

* Sun Feb 17 2008 cabal-rpm <cabal-devel@haskell.org> - 0.4.0.2-1
- spec file autogenerated by cabal-rpm
