Name:           perl-Crypt-OpenSSL-RSA
Version:        0.28
Release: 7%{?dist}.0.2
Summary:        Perl interface to OpenSSL for RSA
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-OpenSSL-RSA/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PERLER/Crypt-OpenSSL-RSA-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl openssl-devel
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Crypt::OpenSSL::Bignum)
BuildRequires:  perl(Crypt::OpenSSL::Random)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Crypt::OpenSSL::Random)
Requires:	perl(Crypt::OpenSSL::Bignum)

Prefix: %{_prefix}

%description
Crypt::OpenSSL::RSA - RSA encoding and decoding, using the openSSL libraries

%prep
%setup -q -n Crypt-OpenSSL-RSA-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Crypt/

%exclude %{_mandir}

%changelog
* Sun Aug 9 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.28-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.28-6
- Mass rebuild 2013-12-27

* Tue Nov 27 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-5
- Update dependencies and source link
- Add perl_default_filter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.28-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 21 2011 Wes Hardaker <wjhns174@hardakers.net> - 0.28-1
- Update to latest upstream: 0.28

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.26-6
- Perl mass rebuild

* Thu May 12 2011 Wes Hardaker <wjhns174@hardakers.net> - 0.26-5
- 704257 Added a patch to correct building with perl 5.14

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.26-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Sep  9 2010 Wes Hardaker <wjhns174@hardakers.net> - 0.26-2
- version bump

* Thu Sep  9 2010 Wes Hardaker <wjhns174@hardakers.net> - 0.26-1
- Updated to the upstream 0.26

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.25-12
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.25-11
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.25-10
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.25-7
- rebuild with new openssl

* Wed Jun 18 2008 Wes Hardaker <wjhns174@hardakers.net> - 0.25-6
- Fix bug 451900: force-require the bignum module

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.25-5
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.25-4
- Autorebuild for GCC 4.3

* Sun Dec 09 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.25-3
- Rebuild for deps

* Thu Dec  6 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.25-2
- Bump to force rebuild with new openssl lib version

* Thu May 31 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.25-1
- head to upstream 0.25
- doc the new LICENSE file

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-4
- Reverse terms in license to match perl rpm exactly

* Mon May 14 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-3
- BuildRequire perl(Test) perl(ExtUtils::MakeMaker) perl(Crypt::OpenSSL::Bignum)
- Fixed source code URL

* Tue May  8 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-2
- Add BuildRequire openssl-devel
- Don't manually require openssl
- Use vendorarch instead of vendorlib 

* Thu Apr 19 2007  Wes Hardaker <wjhns174@hardakers.net> - 0.24-1
- Initial version
