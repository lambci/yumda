Name:           perl-TimeDate
Version:        2.30
Epoch:          1
Release:        2%{?dist}
Summary:        A Perl module for time and date manipulation
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/TimeDate/
Source0:        http://www.cpan.org/authors/id/G/GB/GBARR/TimeDate-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Prefix: %{_prefix}

%description
This module includes a number of smaller modules suited for
manipulation of time and date strings with Perl. In particular, the
Date::Format and Date::Parse modules can display and read times and
dates in various formats, providing a more reliable interface to
textual representations of points in time.

%prep
%setup -q -n TimeDate-%{version}
# ChangeLog is ISO-8859-1 encoded
iconv -f iso-8859-1 -t utf8 < ChangeLog > ChangeLog.utf8
mv ChangeLog.utf8 ChangeLog
# Bogus exec permissions on some language modules
chmod -x lib/Date/Language/{Russian_cp1251,Russian_koi8r,Turkish}.pm

%build
perl Makefile.PL INSTALLDIRS=vendor \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%files 
%license README
%{perl_vendorlib}/Date/
%{perl_vendorlib}/Time/

%exclude %{_mandir}

%changelog
* Sun Aug 9 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:2.30-2
- Mass rebuild 2013-12-27

* Tue Feb 19 2013 Petr Šabata <contyk@redhat.com> - 1:2.30-1
- 2.30 bump
- Fix the buildtime dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.20-10
- Remove perl(base) from BR
- Package README and ChangeLog
- Replace PERL_INSTALL_ROOT with DESTDIR
- Remove deleting empty directories

* Thu Aug 16 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.20-9
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:1.20-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 1:1.20-5
- Perl mass rebuild
- Buildroot and defattr cleanup

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.20-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.20-2
- Mass rebuild with perl-5.12.0

* Wed Dec 23 2009 Paul Howarth <paul@city-fan.org> - 1:1.20-1
- update to 1.20
- recode documentation as UTF-8
- fix bogus exec permissions to placate rpmlint

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.16-12
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.16-9
- fix license tag

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.16-8
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:1.16-7
- rebuild for new perl

* Thu Jun 28 2007 Robin Norwood <rnorwood@redhat.com> 1:1.16-6
- Bump release to outpace RHEL5
- Add dist tag to release field

* Tue Mar 20 2007 Steven Pritchard <steve@kspei.com> 1:1.16-4
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.
- Remove check macro cruft.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.16-3.2.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1:1.16-3.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Mon Apr 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:1.16-3
- Bring up to date with current Fedora.Extras perl spec template. (#155914)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1:1.16-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1:1.16-1
- update to 1.16, bump epoch since previous version was 1.1301

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Aug  6 2002 Chip Turner <cturner@localhost.localdomain>
- update to 1.301

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Oct 24 2001 root <root@redhat.com>
- Spec file was autogenerated. 
