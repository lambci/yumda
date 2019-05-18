# We need to patch the test suite if we have Test::More < 0.88
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-CPAN-Meta-YAML
Version:	0.008
Release:	14%{?dist}
Summary:	Read and write a subset of YAML for CPAN Meta files
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/CPAN-Meta-YAML/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-YAML-%{version}.tar.gz
Patch1:		CPAN-Meta-YAML-0.006-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
# Tests:
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(YAML)
# Don't run extra tests when bootstrapping as many of those
# tests' dependencies build-require this package
%if 0%{!?perl_bootstrap:1}
# RHEL-7 package cannot have buildreqs from EPEL-7 (aspell-en, Pod::Wordlist::hanekomu),
# so skip the spell check there
%if 0%{?rhel} < 7
# Version 1.113620 needed for "UTF"
BuildRequires:	perl(Pod::Wordlist::hanekomu) >= 1.113620
BuildRequires:	perl(Test::Spelling), aspell-en
%endif
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Requires)
# RHEL ≤ 6 doesn't have a recent enough perl(version) for perl(Test::Version) in EPEL
# RHEL ≥ 7 includes this package but does not have perl(Test::Version)
%if 0%{?fedora}
BuildRequires:	perl(Test::Version)
%endif
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
Requires:	perl(Exporter)

%description
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.

%prep
%setup -q -n CPAN-Meta-YAML-%{version}

# We need to patch the test suite if we have Test::More < 0.88
%if %{old_test_more}
%patch1 -p1
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor \
  prefix=%{_prefix} \
  installvendorlib=%{perl_vendorlib} \
  installvendorarch=%{perl_vendorarch}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%files
%license LICENSE
%{perl_vendorlib}/CPAN/

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.008-14
- Mass rebuild 2013-12-27

* Tue Nov 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-13
- Update dependencies

* Thu Oct 11 2012 Paul Howarth <paul@city-fan.org> - 0.008-12
- Never BR: perl(Test::Version) for EL builds as perl(version) is too old
  prior to EL-7 and this package is included in RHEL ≥ 7 but Test::Version
  is only in EPEL

* Thu Oct 11 2012 Petr Pisar <ppisar@redhat.com> - 0.008-11
- Restrict Test::Version optional test on RHEL to version 6 only

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.008-9
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.008-8
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.008-7
- Run the extra tests in a separate test run, and only when not bootstrapping
- Don't BR: perl(Test::Spelling) with RHEL ≥ 7 as we don't have the other
  dependencies needed do the spell check test

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-6
- Conditionalize dependency on aspell

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.008-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 0.008-4
- Disable author tests on bootstrap

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-3
- Data::Dumper is not really needed, dependencies must be fixed in YAML

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-2
- Don't BR: Pod::Wordlist::hanekomu for RHEL-7+ builds; RHEL package cannot
  have buildreq from EPEL
- Add missing Data::Dumper dependency

* Thu Mar 15 2012 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008:
  - Generated from ADAMK/YAML-Tiny-1.51.tar.gz
  - Updated from YAML-Tiny to fix compatibility with older Scalar::Util
- Drop upstreamed patch for old Scalar::Util versions
- Don't need to remove empty directories from the buildroot

* Wed Feb  8 2012 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007:
  - Documentation fix to replace missing abstract

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006:
  - Set back configure_requires prerequisite for ExtUtils::MakeMaker
    from 6.30 to 6.17
- BR: perl(Test::Requires)
- BR: perl(Test::Spelling), perl(Pod::Wordlist::hanekomu) and aspell-en to
  enable the spell checker test
- Drop patch for building with old ExtUtils::MakeMaker versions, no longer
  needed
- Drop support for soon-to-be-EOL RHEL-4:
  - Drop %%defattr, redundant since rpm 4.4
- Update patch for building with Test::More < 0.88

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.005-2
- Fedora 17 mass rebuild

* Tue Dec 13 2011 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005:
  - Fix documentation to clarify that users are responsible for UTF-8
    encoding/decoding

* Wed Sep  7 2011 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004:
  - Generated from ADAMK/YAML-Tiny-1.50.tar.gz
- BR: perl(Test::Version) for additional test coverage
- Update patch for building with ExtUtils::MakeMaker < 6.30
- Add patch to support building with Test::More < 0.88
- Add patch to fix operation with Scalar::Util < 1.18

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.003-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.003-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> - 0.003-3
- Trim %%description (#672807)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 0.003-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 0.003-1
- Initial RPM version
