Name:		perl-Module-Metadata
Version:	1.000018
Release:	2%{?dist}
Summary:	Gather package and POD information from perl module files
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Module-Metadata/
Source0:	http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Module-Metadata-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(version) >= 0.87
BuildRequires:	perl(warnings)
# Regular test suite
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More)
# Release tests
%if !%{defined perl_bootstrap}
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Prefix: %{_prefix}

%description
This module provides a standard way to gather metadata about a .pm file
through (mostly) static analysis and (some) code execution. When
determining the version of a module, the $VERSION assignment is evaled, as
is traditional in the CPAN toolchain.

%prep
%setup -q -n Module-Metadata-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%files
%license README
%{perl_vendorlib}/Module/

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.000018-2
- Mass rebuild 2013-12-27

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.000018-1
- Update to 1.000018
  - Re-release of de-tainting fix without unstated non-core test dependencies
- Drop BR: perl(Test::Fatal)

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.000017-1
- Update to 1.000017
  - De-taint version, if needed (CPAN RT#88576)
- BR: perl(Test::Fatal)

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.000016-1
- Update to 1.000016
  - Re-release to fix prereqs and other metadata
- This release by ETHER -> update source URL
- Specify all dependencies

* Wed Aug 21 2013 Paul Howarth <paul@city-fan.org> - 1.000015-1
- Update to 1.000015
  - Change wording about safety/security to satisfy CVE-2013-1437

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.000014-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.000014-2
- Perl 5.18 rebuild

* Thu May  9 2013 Paul Howarth <paul@city-fan.org> - 1.000014-1
- Update to 1.000014
  - Fix reliance on recent Test::Builder
  - Make tests perl 5.6 compatible
- This release by BOBTFISH -> update source URL

* Sun May  5 2013 Paul Howarth <paul@city-fan.org> - 1.000012-1
- Update to 1.000012
  - Improved package detection heuristics
  - Fix ->contains_pod (CPAN RT#84932)
  - Fix detection of pod after __END__ (CPAN RT#79656)
- This release by ETHER -> update source URL
- Package new upstream README file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 1.000011-1
- Update to 1.000011
  - Fix various warning messages
- This release by APEIRON -> update source URL

* Mon Jul 30 2012 Paul Howarth <paul@city-fan.org> - 1.000010-1
- Update to 1.000010
  - Performance improvement: the creation of a Module::Metadata object
    for a typical module file has been sped up by about 40%%
  - Fix t/metadata.t failure under Cygwin
  - Portability fix-ups for new_from_module() and test failures on VMS
- This release by VPIT -> update source URL
- Drop buildreqs for Perl core modules that aren't dual-lived
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-2
- Skip optional POD tests on bootstrap

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 1.000009-1
- Update to 1.000009
  - Adds 'provides' method to generate a CPAN META provides data structure
    correctly; use of package_versions_from_directory is discouraged
  - Fatal errors now use 'croak' instead of 'die'; Carp added as
    prerequisite
- Improve %%description
- Include all buildreqs explicitly required and classify them by Build,
  Module, Regular test suite, and Release tests
- Run main test suite and release tests separately
- Drop explicit versioned runtime dependency on perl(version) as no supported
  release now requires it

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.000007-2
- Fedora 17 mass rebuild

* Wed Sep  7 2011 Paul Howarth <paul@city-fan.org> - 1.000007-1
- Update to 1.000007
  - Apply VMS fixes backported from blead

* Sun Sep  4 2011 Paul Howarth <paul@city-fan.org> - 1.000006-1
- Update to 1.000006
  - Support PACKAGE BLOCK syntax

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 1.000005-1
- Update to 1.000005
  - Localize $package::VERSION during version discovery
  - Fix references to Module::Build::ModuleInfo (CPAN RT#66133)
  - Added 'new_from_handle()' method (CPAN RT#68875)
  - Improved documentation (SYNOPSIS, broke out class/object method, and
    other minor edits)
- Install to vendor directories rather than perl directories

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 1.000004-5
- Bump and rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.000004-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Paul Howarth <paul@city-fan.org> - 1.000004-2
- Tweaks from package review (#672779)
  - Explicitly duplicate %%summary in %%description as upstream provides
    nothing particularly useful
  - Drop redundant BuildRoot tag
  - Add BuildRequires for possibly dual-lived perl modules:
    Cwd Data::Dumper Exporter File::Path File::Spec File::Temp IO::File
- Explicitly require perl(version) >= 0.87 for builds on OS releases older
  than Fedora 15 where the versioned dependency isn't picked up automatically

* Thu Feb  3 2011 Paul Howarth <paul@city-fan.org> - 1.000004-1
- Update to 1.000004
  - Fix broken metadata.t when @INC has relative paths

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.000003-2
- Sanitize for Fedora submission
- Drop support for releases prior to F-15 due to needing perl(version) >= 0.87

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.000003-1
- Initial RPM version
