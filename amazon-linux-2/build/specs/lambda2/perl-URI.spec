Name:           perl-URI
Version:        1.60
Release:        9%{?dist}
Summary:        A Perl module implementing URI parsing and manipulation
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/URI/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/URI-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(MIME::Base64) >= 2
BuildRequires:  perl(Net::Domain)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
# Business::ISBN -> Test::Pod -> Pod::Simple -> HTML::Entities (HTML::Parser) -> URI
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Business::ISBN)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Business::ISBN)
Requires:       perl(Cwd)
Requires:       perl(Data::Dumper)
Requires:       perl(MIME::Base64) >= 2
Requires:       perl(Net::Domain)

%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).

%prep
%setup -q -n URI-%{version}
chmod -c 644 uri-test

%build
perl Makefile.PL INSTALLDIRS=perl
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README uri-test
%{perl_privlib}/URI.pm
%{perl_privlib}/URI/
%{_mandir}/man3/URI.3pm*
%{_mandir}/man3/URI::Escape.3pm*
%{_mandir}/man3/URI::Heuristic.3pm*
%{_mandir}/man3/URI::QueryParam.3pm*
%{_mandir}/man3/URI::Split.3pm*
%{_mandir}/man3/URI::URL.3pm*
%{_mandir}/man3/URI::WithBase.3pm*
%{_mandir}/man3/URI::_punycode.3pm*
%{_mandir}/man3/URI::data.3pm*
%{_mandir}/man3/URI::file.3pm*
%{_mandir}/man3/URI::ldap.3pm*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.60-9
- Mass rebuild 2013-12-27

* Wed Feb 27 2013 Paul Howarth <paul@city-fan.org> - 1.60-8
- Retain runtime dependency of perl(Business::ISBN) when bootstrapping; a
  better fix for the build dependency cycle was to drop LWP::Simple as a
  buildreq of perl-Business-ISBN (needed only for optional tests) when
  bootstrapping

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-6
- Update dependencies

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.60-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.60-2
- Perl 5.16 rebuild

* Mon Mar 26 2012 Paul Howarth <paul@city-fan.org> - 1.60-1
- Update to 1.60
  - Do not reverse the order of new parameters
  - Avoid test failure if the local hostname is 'foo' (CPAN RT#75519)
  - Work around a stupid join bug in 5.8.[12] (CPAN RT#59274)
  - Updated repository URL
- Don't need to remove empty directories from buildroot
- BR: perl(constant)

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 1.59-3
- Break build dependency loop by only using perl(Business::ISBN) if we're not
  bootstrapping
- BR: perl(Carp) and perl(Exporter)
- Make %%files list more explicit
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use %%{_fixperms} macro rather than our own chmod incantation
- Don't use macros for commands

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 1.59-1
- update to 1.59

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.58-2
- Perl mass rebuild

* Wed Mar 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.58-1
- update to 1.58

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.56-1
- update

* Fri Sep 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.55-1
- update

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.54-2
- Mass rebuild with perl-5.12.0

* Mon Apr 19 2010 Petr Pisar <ppisar@redhat.com> - 1.54-1
- version bump
- Changes is in UTF-8 already
- rfc2396.txt removed by upstream

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.40-2
- rebuild against perl 5.10.1

* Tue Oct  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.40-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.37-1
- Upstream update.
- Add BR: perl(Test::More), perl(Business::ISBN).
- Remove requires-filter.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.35-8
- Rebuild for perl 5.10 (again)

* Wed Feb 13 2008 Robin Norwood <rnorwood@redhat.com> - 1.35-7
- rebuild again for new perl

* Wed Feb 13 2008 Robin Norwood <rnorwood@redhat.com> - 1.35-6
- Last update for package review

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.35-5
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.35-4
- Fix various package review issues:
- Remove redundant BR: perl
- remove "|| :" from %%check
- move requires filter into spec file
- remove tabs and fix spacing

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.35-3.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.35-3
- fix License: tag

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.35-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.35-2
- Update to 1.35.
- Spec cleanup (#153205)

* Thu Sep 23 2004 Chip Turner <cturner@redhat.com> 1.30-3
- rebuild

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.30-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.30-1
- update to 1.30

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Aug  6 2002 Chip Turner <cturner@localhost.localdomain>
- update to 1.21

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
