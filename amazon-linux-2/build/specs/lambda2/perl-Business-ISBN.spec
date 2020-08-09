Name:           perl-Business-ISBN
%global cpan_version 2.06
Version:        %(echo '%{cpan_version}' | tr '_' '.'})
Release:        2%{?dist}
Summary:        Perl module to work with International Standard Book Numbers

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Business-ISBN/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Business-ISBN-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Test::Manifest 1.21 is optional
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Business::ISBN::Data) >= 20120719.001
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(subs)
BuildRequires:  perl(vars)
# Optinonal run-time
BuildRequires:  perl(GD::Barcode::EAN13)
# Break build dependency cycle involving LWP::Simple and URI
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(LWP::Simple)
%endif
# Tests:
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Test::More) >= 0.95
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(warnings)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Prefix: %{_prefix}

%description
This modules handles International Standard Book Numbers, including
ISBN-10 and ISBN-13.

%prep
%setup -q -n Business-ISBN-%{cpan_version}

%build
perl Makefile.PL INSTALLDIRS=vendor \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%files
%license LICENSE
%{perl_vendorlib}/*

%exclude %{_mandir}

%changelog
* Sun Aug 9 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.06-2
- Mass rebuild 2013-12-27

* Mon Jun 03 2013 Petr Pisar <ppisar@redhat.com> - 2.06-1
- 2.06 bump

* Wed Feb 27 2013 Paul Howarth <paul@city-fan.org> - 2.05.03-3
- Don't BR: perl(LWP::Simple) for optional tests when bootstrapping; this is a
  cleaner fix than nobbling perl-URI's runtime dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.05.03-1
- 2.05_03 bump. Fix failing tests (RT#78671, RT#75686)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.05-8
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.05-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.05-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.05-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04_01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04_01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Stepan Kasal <skasal@redhat.com> - 2.04_01-1
- new upstream version
- drop integrated patch

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.03-4
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-3
- Apply patch to fix barcode test

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-2
- Fix buildrequires and doc list

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-1
- Initial build
