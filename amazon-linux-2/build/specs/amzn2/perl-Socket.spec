%global cpan_version 2.010
Name:           perl-Socket
Version:        %(echo '%{cpan_version}' | tr '_' '.')
Release: 4%{?dist}.0.2
Summary:        Networking constants and support functions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Socket/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Socket-%{cpan_version}.tar.gz
# Fix calling getnameinfo() on tainted value BZ#1200167
# Backported fixes from 2.017 and 2.018
Patch0:         Socket-2.018-Fix-calling-getnameinfo-on-tainted-value.patch
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::Constant) >= 0.23
# ExtUtils::Constant::ProxySubs not used
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Scalar::Util is needed only if getaddrinfo(3) does not exist. Not our case.
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(XSLoader)
# Tests only:
BuildRequires:  perl(Errno)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides a variety of constants, structure manipulators and other
functions related to socket-based networking. The values and functions
provided are useful when used in conjunction with Perl core functions such as
socket(), setsockopt() and bind(). It also provides several other support
functions, mostly for dealing with conversions of network addresses between
human-readable and native binary forms, and for hostname resolver operations.

%prep
%setup -q -n Socket-%{cpan_version}
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Artistic Changes Copying LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Socket*
%{_mandir}/man3/*

%changelog
* Thu Mar 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.010-4
- Fix calling getnameinfo on tainted value (bug #1200167)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.010-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.010-2
- Mass rebuild 2013-12-27

* Tue Jun 25 2013 Petr Pisar <ppisar@redhat.com> - 2.010-1
- 2.010 bump

* Fri May 24 2013 Petr Pisar <ppisar@redhat.com> - 2.009-3
- Specify all dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Pisar <ppisar@redhat.com> - 2.009-1
- 2.009 bump

* Thu Jan 03 2013 Petr Pisar <ppisar@redhat.com> - 2.008-1
- 2.008 bump

* Mon Dec 17 2012 Petr Pisar <ppisar@redhat.com> - 2.007-1
- 2.007 bump

* Thu Nov 08 2012 Petr Pisar <ppisar@redhat.com> - 2.006-2
- Update description

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 2.006-1
- 2.006 bump

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 2.005-1
- 2.005 bump

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 2.004-1
- 2.004 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.002-2
- Perl 5.16 rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.002-1
- 2.002 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.001-2
- Perl 5.16 rebuild

* Wed Mar 28 2012 Petr Pisar <ppisar@redhat.com> - 2.001-1
- 2.001 bump (bug-fixing release)

* Tue Mar 27 2012 Petr Pisar <ppisar@redhat.com> - 2.000-3
- Fix invalid write while unpacking AF_UNIX sockaddr (bug #806543)

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 2.000-2
- Increase release number due to F17 build

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 2.000-1
- 2.000 bump
- Fix a buffer overflow (RT#75623)

* Wed Feb 22 2012 Petr Pisar <ppisar@redhat.com> - 1.99-1
- 1.99 bump

* Thu Feb 16 2012 Petr Pisar <ppisar@redhat.com> - 1.98-1
- 1.98 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> - 1.97-1
- 1.97 bump
- License texts added

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 1.96-1
- 1.96 bump

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 1.95-1
- 1.95 bump

* Wed Nov 23 2011 Petr Pisar <ppisar@redhat.com> 1.94.07-1
- 1.94_07 packaged.
