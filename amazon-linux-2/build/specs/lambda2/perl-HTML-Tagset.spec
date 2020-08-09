Name:           perl-HTML-Tagset
Version:        3.20
Release:        15%{?dist}
Summary:        HTML::Tagset - data tables useful in parsing HTML
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-Tagset/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/HTML-Tagset-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Test::Pod -> Pod::Simple -> HTML::Entities (HTML::Parser) -> HTML::Tagset
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Test::Pod)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module contains several data tables useful in various kinds of
HTML parsing operations, such as tag and entity names.

%prep
%setup -q -n HTML-Tagset-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/HTML/
%{_mandir}/man3/HTML::Tagset.3pm*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.20-15
- Mass rebuild 2013-12-27

* Mon Nov 12 2012 Petr Šabata <contyk@redhat.com> - 3.20-14
- Add a missing dependency

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.20-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 3.20-11
- Perl 5.16 rebuild

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 3.20-10
- Clean up spec file for modern rpmbuild:
  - Drop BuildRoot definition
  - Drop %%defattr
  - Drop %%clean section
  - Drop cleaning of buildroot in %%install
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Don't use macros for commands
- Break build dependency loop by only using perl(Test::Pod) if we're not
  bootstrapping
- BR: perl(Test::More)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.20-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.20-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.20-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.20-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Marcela Mašláňová <mmaslano@redhat.com> - 3.20-1
- update to 3.20

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.10-8
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.10-7
- rebuild for new perl

* Wed Aug 29 2007 Robin Norwood <rnorwood@redhat.com> - 3.10-6
- Update license tag
- Add BuildRequires

* Mon Feb 05 2007 Robin Norwood <rnorwood@redhat.com> - 3.10-5
- perl(Test::Pod) doesn't exist in our buildroots because it isn't in
  core.  Removing for now.

* Sun Feb 04 2007 Robin Norwood <rnorwood@redhat.com> - 3.10-4
- Also add BuildRequires suggested by Jose.

* Sat Feb  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.10-3
- Minor corrections.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.10-2.1.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.10-2.1
- rebuild for new perl-5.8.8

* Tue Jan 10 2006 Jason Vas Dias <jvdias@redhat.com> - 3.10-1
- fix bug 176720: upgrade to 3.10
- make .spec file conform to fedora-rpmdevtools spectemplate-perl.spec

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Mar 30 2005 Warren Togami <wtogami@redhat.com>
- remove brp-compress

* Tue Mar 29 2005 Robert Scheck <redhat@linuxnetz.de> 3.04-1
- upgrade to 3.04 and spec file cleanup (#140914, #150360)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 3.03-30
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 3.03-28
- rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 30 2001 Chip Turner <cturner@redhat.com>
- Spec file was autogenerated. 
