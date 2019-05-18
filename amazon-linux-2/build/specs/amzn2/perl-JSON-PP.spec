Name:		perl-JSON-PP
Version:	2.27202
Release:	2%{?dist}
Summary:	JSON::XS compatible pure-Perl module
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/JSON-PP/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MA/MAKAMAKA/JSON-PP-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(lib)
BuildRequires:	perl(Math::BigFloat)
BuildRequires:	perl(Math::BigInt)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Tie::IxHash)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Data::Dumper)
Conflicts:	perl-JSON < 2.50

%description
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.

JSON::PP is a pure-Perl module and is compatible with JSON::XS.

%prep
%setup -q -n JSON-PP-%{version}

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

%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{_bindir}/json_pp
%{perl_vendorlib}/JSON/
%{_mandir}/man1/json_pp.1*
%{_mandir}/man3/JSON::PP.3pm*
%{_mandir}/man3/JSON::PP::Boolean.3pm*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.27202-2
- Mass rebuild 2013-12-27

* Wed Mar 13 2013 Paul Howarth <paul@city-fan.org> - 2.27202-1
- Update to 2.27202
  - Fix test failures due to hash iterator randomization in perl 5.17.6 onwards
    (CPAN RT#83421)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27200-243
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 2.27200-242
- Correct the URL
- Add a few missing buildtime dependencies
- Drop Getopt::Long dep; json_pp isn't tested

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> - 2.27200-241
- BR: perl(base), perl(constant) and perl(lib)
- Install to vendor directories
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 2.27200-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27200-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.27200-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.27200-4
- Depend of Data::Dumper

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 2.27200-3
- Add buildreqs for perl core modules, which might be dual-lived

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.27200-2
- Perl mass rebuild

* Sun May 22 2011 Paul Howarth <paul@city-fan.org> - 2.27200-1
- Update to 2.27200
  - Fixed incr_parse decoding string more correctly (CPAN RT#68032)

* Tue Mar  8 2011 Paul Howarth <paul@city-fan.org> - 2.27105-1
- Update to 2.27105
  - Removed t/900_pod.t from package because of author test
- Drop buildreq perl(Test::Pod), no longer needed

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27104-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> - 2.27104-3
- Conflict with perl-JSON < 2.50 (#672764)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 2.27104-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 2.27104-1
- Initial RPM version
