# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name HTTP

%bcond_with tests

# no useful debuginfo for Haskell packages without C sources
%global debug_package %{nil}

Name:           ghc-%{pkg_name}
# part of haskell-platform
Version:        4000.2.8
Release:        33%{?dist}
Summary:        A library for client-side HTTP

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-network-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-parsec-devel
%if %{with tests}
BuildRequires:  ghc-HUnit-devel
BuildRequires:  ghc-case-insensitive-devel
BuildRequires:  ghc-conduit-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-http-types-devel
BuildRequires:  ghc-httpd-shed-devel
BuildRequires:  ghc-pureMD5-devel
BuildRequires:  ghc-split-devel
BuildRequires:  ghc-test-framework-devel
BuildRequires:  ghc-test-framework-hunit-devel
BuildRequires:  ghc-wai-devel
BuildRequires:  ghc-warp-devel
%endif
# End cabal-rpm deps

Prefix: %{_prefix}

%description
The HTTP package supports client-side web programming in Haskell. It lets you
set up HTTP connections, transmitting requests and processing the responses
coming back, all from within the comforts of Haskell. It's dependent on the
network package to operate, but other than that, the implementation is all
written in Haskell.

A basic API for issuing single HTTP requests + receiving responses is provided.
On top of that, a session-level abstraction is also on offer (the
'BrowserAction' monad); it taking care of handling the management of persistent
connections, proxies, state (cookies) and authentication credentials required
to handle multi-step interactions with a web server.

The representation of the bytes flowing across is extensible via the use of a
type class, letting you pick the representation of requests and responses that
best fits your use. Some pre-packaged, common instances are provided for you
('ByteString', 'String').


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

* Tue Jul  8 2014 Jens Petersen <petersen@redhat.com> - 4000.2.8-33
- f21 rebuild


* Wed Mar 26 2014 Jens Petersen <petersen@redhat.com> - 4000.2.8-32
- bump over haskell-platform

* Tue Feb 18 2014 Jens Petersen <petersen@redhat.com> - 4000.2.8-31
- update to 4000.2.8
- bump release over haskell-platform
- revive package with cblrpm-0.8.9

* Tue Mar 20 2012 Jens Petersen <petersen@redhat.com> - 4000.2.2-1
- update to 4000.2.2

* Mon Jan 23 2012 Jens Petersen <petersen@redhat.com> - 4000.1.2-3
- update url

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4000.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 4000.1.2-1
- update to 4000.1.2 for haskell-platform-2011.4.0.0
- update to cabal2spec-0.25.1

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4000.1.1-8.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4000.1.1-8.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 4000.1.1-8.1
- rebuild with new gmp

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 4000.1.1-8
- ghc_arches replaces ghc_excluded_archs

* Mon Jun 20 2011 Jens Petersen <petersen@redhat.com> - 4000.1.1-7
- BR ghc-Cabal-devel and use ghc_excluded_archs

* Fri May 27 2011 Jens Petersen <petersen@redhat.com> - 4000.1.1-6
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 4000.1.1-5
- Enable build on sparcv9

* Tue Feb 15 2011 Jens Petersen <petersen@redhat.com> - 4000.1.1-4
- rebuild for haskell-platform-2011.1 updates

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4000.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Jens Petersen <petersen@redhat.com> - 4000.1.1-2
- update to cabal2spec-0.22.4

* Sun Dec  5 2010 Jens Petersen <petersen@redhat.com> - 4000.1.1-1
- update to 4000.1.1

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 4000.1.0-1
- update to 4000.1.0

* Thu Nov 25 2010 Jens Petersen <petersen@redhat.com> - 4000.0.9-6
- drop -o obsoletes

* Sat Jul 31 2010 Jens Petersen <petersen@redhat.com> - 4000.0.9-5
- ghc-rpm-macros-0.8.1 for doc obsoletes
- part of haskell-platform-2010.2.0.0
- add hscolour

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 4000.0.9-4
- sync cabal2spec-0.22

* Tue Apr 27 2010 Jens Petersen <petersen@redhat.com> - 4000.0.9-3
- rebuild against ghc-6.12.2

* Wed Mar 24 2010 Jens Petersen <petersen@redhat.com> - 4000.0.9-2
- rebuild against network-2.2.1.7

* Tue Mar 23 2010 Jens Petersen <petersen@redhat.com> - 4000.0.9-1
- update to 4000.0.9 for haskell-platform-2010.1.0.0

* Tue Jan 12 2010 Jens Petersen <petersen@redhat.com> - 4000.0.8-2
- rebuild against ghc-mtl package

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 4000.0.8-1
- update to 4000.0.8 (haskell-platform-2009.3.1)
- update to ghc-rpm-macros-0.5.1 and cabal2spec-0.21.1:
- drop doc and prof bcond
- use common_summary and common_description
- use ghc_lib_package and ghc_pkg_deps
- build shared library
- drop redundant buildroot and its install cleaning
- buildrequires mtl

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 4000.0.6-6
- use %%ghc_pkg_ver for requires

* Mon Sep 28 2009 Jens Petersen <petersen@redhat.com> - 4000.0.6-5
- buildrequire the new ghc-network library

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4000.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Jens Petersen <petersen@redhat.com> - 4000.0.6-3
- ppc workaround no longer needed with ghc-6.10.3
- provide ghc-HTTP (cabal2spec-0.17)

* Wed May 13 2009 Jens Petersen <petersen@redhat.com> - 4000.0.6-2
- rebuild with ghc-rpm-macros and ghc-6.10.3 (cabal2spec-0.16)

* Sat Apr 25 2009 Jens Petersen <petersen@redhat.com> - 4000.0.6-1
- update to 4000.0.6
- sync with cabal2spec-0.14
- compile Setup on ppc to workaround runghc failure

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 4000.0.4-3
- update url
- update to cabal2spec-0.12:
- use ix86 in archs and add alpha
- add devel subpackage
- use global rather than define
- devel owns docdir

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4000.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Jens Petersen <petersen@redhat.com> - 4000.0.4-1
- update to 4000.0.4

* Fri Feb 13 2009 Jens Petersen <petersen@redhat.com> - 3001.1.5-2
- sync with latest template and add a doc subpackage

* Tue Dec 23 2008 Jens Petersen <petersen@redhat.com> - 3001.1.5-1
- update to 3001.1.5
- use bcond for doc and prof
- minor tweaks for latest packaging guidelines

* Fri Nov 28 2008 Jens Petersen <petersen@redhat.com> - 3001.1.4-4
- drop LICENSE from -prof subpackage

* Tue Nov 25 2008 Jens Petersen <petersen@redhat.com> - 3001.1.4-3
- add build_doc and build_prof switches
- provide -devel
- drop redundant pre script
- only regenerate doc index in postun if uninstalling

* Mon Nov 10 2008 Jens Petersen <petersen@redhat.com> - 3001.1.4-2
- only build on ghc archs
- version install script requires

* Mon Nov 10 2008 Jens Petersen <petersen@redhat.com> - 3001.1.4-1
- initial packaging for fedora
