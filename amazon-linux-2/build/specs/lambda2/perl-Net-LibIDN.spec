%global pkgname Net-LibIDN

Summary:    Perl bindings for GNU LibIDN
Name:       perl-Net-LibIDN
Version:    0.12
Release: 15%{?dist}.0.2
License:    GPL+ or Artistic
Group:      Development/Libraries
URL:        http://search.cpan.org/dist/%{pkgname}/
Source:     http://search.cpan.org/CPAN/authors/id/T/TH/THOR/%{pkgname}-%{version}.tar.gz
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:  libidn-devel >= 0.4.0
BuildRequires:  perl >= 5.8.0
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
# Run-time:
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Tests:
BuildRequires:  perl(Test)

# Filter the Perl extension module
%{?perl_default_filter}

%description
Provides perl bindings for GNU Libidn, a C library for handling
Internationalized Domain Names according to IDNA (RFC 3490), in
a way very much inspired by Turbo Fredriksson's PHP-IDN.

%prep
%setup -q -n %{pkgname}-%{version}
# Change man page encoding into UTF-8
for F in _LibIDN.pm; do
    iconv -f latin1 -t utf-8 < "$F" > "${F}.utf"
    sed -i -e '/^=encoding\s/ s/latin1/utf-8/' "${F}.utf"
    touch -r "$F" "${F}.utf"
    mv "${F}.utf" "$F"
done;

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} +
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} +
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Artistic Changes README
%{_mandir}/man3/*.3pm*
%{perl_vendorarch}/Net
%{perl_vendorarch}/auto/Net

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.12-15
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.12-14
- Mass rebuild 2013-12-27

* Tue Nov 27 2012 Petr Pisar <ppisar@redhat.com> - 0.12-13
- Modernize spec file

* Mon Aug 13 2012 Petr Pisar <ppisar@redhat.com> - 0.12-12
- Build-require Carp

* Mon Aug 13 2012 Petr Pisar <ppisar@redhat.com> - 0.12-11
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.12-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.12-1
- Upgrade to 0.12

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.11-2
- Rebuilt against gcc 4.4 and rpm 4.6

* Sun Jan 25 2009 Robert Scheck <robert@fedoraproject.org> 0.11-1
- Upgrade to 0.11

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-2
- Rebuild for new perl

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 0.10-1
- Upgrade to 0.10

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 0.09-4
- Updated the license tag according to the guidelines

* Mon May 07 2007 Robert Scheck <robert@fedoraproject.org> 0.09-3
- Rebuild

* Thu Apr 26 2007 Robert Scheck <robert@fedoraproject.org> 0.09-2
- Added build requirement to perl(ExtUtils::MakeMaker)

* Sun Sep 03 2006 Robert Scheck <robert@fedoraproject.org> 0.09-1
- Upgrade to 0.0.9 and rebuild for Fedora Core 6

* Fri Jun 23 2006 Robert Scheck <robert@fedoraproject.org> 0.08-5
- Changes to match with Fedora Packaging Guidelines (#193960)

* Sun Dec 25 2005 Robert Scheck <robert@fedoraproject.org> 0.08-4
- Rebuilt against gcc 4.1 and libidn 0.6.0

* Fri Apr 01 2005 Robert Scheck <robert@fedoraproject.org> 0.08-3
- Some spec file cleanup

* Mon Mar 14 2005 Robert Scheck <robert@fedoraproject.org> 0.08-2
- Rebuilt against gcc 4.0

* Thu Jan 20 2005 Robert Scheck <robert@fedoraproject.org> 0.08-1
- Upgrade to 0.0.8

* Sun Oct 03 2004 Robert Scheck <robert@fedoraproject.org> 0.07-2
- Use perl(:MODULE_COMPAT_*) as requirement for perl
- Lots of spec file cleanups

* Mon May 24 2004 Robert Scheck <robert@fedoraproject.org> 0.07-1
- Upgrade to 0.0.7

* Mon Apr 05 2004 Robert Scheck <robert@fedoraproject.org> 0.06-1
- Upgrade to 0.0.6
- Initial spec file for Red Hat Linux and Fedora Core
