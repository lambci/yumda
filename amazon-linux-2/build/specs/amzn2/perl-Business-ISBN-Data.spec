Name:           perl-Business-ISBN-Data
Version:        20120719.001
Release:        2%{?dist}
Summary:        The data pack for Business::ISBN
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Business-ISBN-Data/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Business-ISBN-Data-%{version}.tar.gz
Patch0:         Business-ISBN-Data-20120719-shellbang.patch
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::Manifest) >= 1.21
BuildRequires:  perl(Test::More) >= 0.95
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Remove bogus provide of perl(Business::ISBN)
%global __provides_exclude ^perl\\(Business::ISBN\\)$

# LWP::Simple not needed in normal operation
%global __requires_exclude ^perl\\(LWP::Simple\\)$

%description
This is a data pack for Business::ISBN.  You can update
the ISBN data without changing the version of Business::ISBN.
Most of the interesting stuff is in Business::ISBN.

%prep
%setup -q -n Business-ISBN-Data-%{version}

# Fix shellbang and script permissions for make_data.pl
%patch0
chmod -c +x make_data.pl

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README LICENSE examples/ t/
%{perl_vendorlib}/Business/
%{_mandir}/man3/Business::ISBN::Data.3*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 20120719.001-2
- Mass rebuild 2013-12-27

* Thu Jul 26 2012 Paul Howarth <paul@city-fan.org> - 20120719.001-1
- Update to 20120719.001:
  - Require Test::More ≥ 0.95 for subtest support
  - No code or feature changes
- Bump Test::Manifest version requirement to 1.21
- Bump Test::More version requirement to 0.95
- Drop redundant buildreq perl(Test::Prereq)

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 20120719-1
- Update to 20120719:
  - Support using data from RangeMessage.xml, so you can use the latest data
    from ISBN without updating this module
- Fix shellbang and permissions of make_data.pl script to placate rpmlint
- Filter dependency on perl(LWP::Simple), required only by make_data.pl script,
  not in normal operation
- Don't need to remove empty directories from the buildroot
- BR: perl(Carp), perl(File::Spec::Functions) and perl(Test::Manifest) ≥ 1.14
- BR: at least version 1.00 of perl(Test::Pod)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 20081208-9
- Perl 5.16 rebuild

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 20081208-8
- Clean up for modern rpmbuild:
  - Drop BuildRoot specification
  - Drop %%clean section
  - Don't bother cleaning buildroot in %%install section
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Replace provides filter with version that works with rpm ≥ 4.9
- Include tests as %%doc since they're referred to by examples/README

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20081208-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 20081208-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 20081208-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 20081208-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 20081208-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081020-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Stepan Kasal <skasal@redhat.com> - 20081020-1
- new upstream version

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-4
- rebuild for new perl

* Thu Nov 15 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-3
- Should not provide perl(Business::ISBN)

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-2
- Fix BuildRequires

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-1
- Initial build
