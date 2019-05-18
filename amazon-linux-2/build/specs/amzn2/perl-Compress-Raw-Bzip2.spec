Name:           perl-Compress-Raw-Bzip2
Summary:        Low-level interface to bzip2 compression library
Version:        2.061
Release: 3%{?dist}.0.2
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Compress-Raw-Bzip2/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/Compress-Raw-Bzip2-%{version}.tar.gz 
BuildRequires:  bzip2-devel
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod)
%endif
# XSLoader or DynaLoader; choose wisely
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# see above
Requires:       perl(XSLoader)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.

%prep
%setup -q -n Compress-Raw-Bzip2-%{version}

%build
BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/Compress/
%{perl_vendorarch}/Compress/
%{_mandir}/man3/Compress::Raw::Bzip2.3pm*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.061-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.061-2
- Mass rebuild 2013-12-27

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Silence compiler warning by making 2nd parameter to DispStream a const char*

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060 (no changes)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - Copy-on-write support (CPAN RT#81352)

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - Compress::Raw::Bzip2 needs to use PERL_NO_GET_CONTEXT (CPAN RT#80318)
  - Install to 'site' instead of 'perl' when perl version is 5.11+
    (CPAN RT#79811)
  - Update to ppport.h that includes SvPV_nomg_nolen (CPAN RT#78080)

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - Fix misuse of magic in API (CPAN RT#78080)
- Drop redundant explicit requires for perl(Exporter) and perl(File::Temp)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.052-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.052-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.052-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.052-2
- Omit optional Test::Pod tests on bootstrap

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052 (no changes)
- Don't need to remove empty directories from buildroot

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049 (no changes)

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048 (set minimum Perl version to 5.6)
- Don't use macros for commands

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Rebuild for gcc 4.7 in Rawhide

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod to IO::Compress

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043 (no changes)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042 (no changes)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Croak if attempt to freeze/thaw compression object (CPAN RT#69985)
- BR: perl(Carp)

* Thu Jul 28 2011 Karsten Hopp <karsten@redhat.com> 2.037-3
- Bump and rebuild, got compiled with old perl on ppc

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (no changes)

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 2.036-1
- 2.036 bump (no changes)

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.035-3
- Perl mass rebuild

* Fri Jun 17 2011 Paul Howarth <paul@city-fan.org> - 2.035-2
- Perl mass rebuild

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (no changes)

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 2.034-1
- 2.034 bump
- Buildroot cleanup, defattr cleanup
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (fixed typos and spelling errors - Perl RT#81782)

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 2.032-1
- 2.032 bump

* Wed Sep 29 2010 jkeating - 2.031-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Petr Pisar <ppisar@redhat.com> - 2.031-1
- 2.031 bump

* Mon Jul 26 2010 Petr Sabata <psabata@redhat.com> - 2.030-1
- 2.030 version bump

* Thu May  6 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.027-1
- update
 
* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.026-2
- Mass rebuild with perl-5.12.0

* Sat Apr 10 2010 Chris Weyl <cweyl@alumni.drew.edu> 2.026-1
- PERL_INSTALL_ROOT => DESTDIR, use _fixperms incantation
- add perl_default_filter (XS package)
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.026)

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.020-2
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.020-1
- update

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.005-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.005-5
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.005-4
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-3
- Update license tag.

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-2
- Bump release to beat F-7 version

* Sun Jul 01 2007 Steven Pritchard <steve@kspei.com> 2.005-1
- Update to 2.005.
- Build against system libbz2 (#246401).

* Tue Jun 05 2007 Robin Norwood <rnorwood@redhat.com> - 2.004-1
- Initial build from CPAN
