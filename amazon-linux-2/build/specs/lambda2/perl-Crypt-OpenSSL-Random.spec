Name:           perl-Crypt-OpenSSL-Random
Version:        0.04
Release: 21%{?dist}.0.2
Summary:        Perl interface to OpenSSL for Random
License:        GPL+ or Artistic 
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-OpenSSL-Random/
Source0:        http://www.cpan.org/authors/id/I/IR/IROBERTS/Crypt-OpenSSL-Random-%{version}.tar.gz
Patch0:         perl-Crypt-OpenSSL-Random-name.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Crypt::OpenSSL::Random - Routines for accessing the OpenSSL
pseudo-random number generator

%prep
%setup -q -n Crypt-OpenSSL-Random-%{version}
%patch0 -p1 -b name

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f \( -name .packlist -o \
        -name '*.bs' -empty \) -exec rm {} \;
find %{buildroot} -depth -type d -empty -exec rmdir {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%doc LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.04-21
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.04-20
- Mass rebuild 2013-12-27

* Tue Nov 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-19
- Update dependencies
- Add perl_default_filter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.04-17
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-15
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-13
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-12
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 0.04-11
- fix the package name for error messages

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.04-10
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.04-9
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.04-6
- rebuild with new openssl

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.04-5
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.04-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.04-3
 - Rebuild for deps

* Wed May 23 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.04-2
- Add document file: LICENSE

* Mon May 21 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.04-1
- Update to upstream 0.4 with proper license

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.03-3
- BuildRequire perl(ExtUtils::MakeMaker)

* Tue May  8 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.03-2
- Add BuildRequire openssl-devel
- Don't manually require openssl
- Use vendorarch instead of vendorlib 

* Thu Apr 19 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.03-1
- Initial version
