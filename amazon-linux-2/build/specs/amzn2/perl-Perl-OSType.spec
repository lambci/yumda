# We don't really need ExtUtils::MakeMaker ≥ 6.30
%global old_eumm %(perl -MExtUtils::MakeMaker -e 'print (($ExtUtils::MakeMaker::VERSION < 6.30) ? 1 : 0);' 2>/dev/null || echo 0)

# Test suite needs patching if we have Test::More < 0.88
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

# Select the appropriate system speller
%if %(perl -e 'print (($] >= 5.010000) ? 1 : 0);')
%global speller hunspell
%else
%global speller aspell
%endif

Name:		perl-Perl-OSType
Version:	1.003
Release:	3%{?dist}
Summary:	Map Perl operating system names to generic types
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Perl-OSType/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Perl-OSType-%{version}.tar.gz
Patch0:		Perl-OSType-1.003-old-EU::MM.patch
Patch1:		Perl-OSType-1.003-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Exporter)
# Test Suite
BuildRequires:	perl(constant)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::More)
# Optional tests, not run for this dual-lived module when bootstrapping
# Also not run for EPEL-5/6 builds due to package unavailability
%if !%{defined perl_bootstrap} && 0%{?fedora}
BuildRequires:	perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Pod::Wordlist::hanekomu)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Spelling), %{speller}-en
BuildRequires:	perl(Test::Version)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.

This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').

%prep
%setup -q -n Perl-OSType-%{version}

# We don't really need ExtUtils::MakeMaker ≥ 6.30
%if %{old_eumm}
%patch0
%endif

# Fix test suite for Test::More < 0.88
%if %{old_test_more}
%patch1
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test
%if !%{defined perl_bootstrap} && 0%{?fedora}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes CONTRIBUTING LICENSE README
%{perl_vendorlib}/Perl/
%{_mandir}/man3/Perl::OSType.3pm*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.003-3
- Mass rebuild 2013-12-27

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 1.003-2
- Disable optional tests on RHEL 7 too

* Thu Mar 21 2013 Paul Howarth <paul@city-fan.org> - 1.003-1
- Update to 1.003
  - Fixed detection of VOS; $^O reports 'vos', not 'VOS'
  - Additional release tests
- BR: perl(File::Spec::Functions), perl(List::Util),
  perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire),
  perl(Pod::Wordlist::hanekomu), perl(Test::MinimumVersion),
  perl(Test::Perl::Critic), perl(Test::Spelling) and perl(Test::Version)
- Identify purpose of each build requirement
- Update patches for building on old distributions
- Don't run extra tests for EPEL-5/6 builds

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-242
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> - 1.002-241
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't delete the extra tests when bootstrapping, but don't run them either

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.002-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.002-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.002-11
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.002-10
- Skip author tests on bootstrap

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.002-9
- Fedora 17 mass rebuild

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 1.002-8
- BR: perl(Pod::Coverage::TrustPod) unconditionally now that it's available in
  EPEL-4

* Tue Aug 16 2011 Marcela Maslanova <mmaslano@redhat.com> - 1.002-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.002-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.002-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-3
- BR: perl(constant), perl(Exporter), perl(File::Temp) in case they are
  dual-lived at some point (#672801)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.002-1
- Initial RPM version
