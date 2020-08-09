Name:           perl-NetAddr-IP
Version:        4.069
Release: 3%{?dist}.0.2
Summary:        Manages IPv4 and IPv6 addresses and subnets
# Lite/Util/Util.xs is GPLv2+
# Other files are (GPLv2+ or Artistic clarified)
License:        GPLv2+ and (GPLv2+ or Artistic clarified)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/NetAddr-IP/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIKER/NetAddr-IP-%{version}.tar.gz
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Math::BigInt)

# Don't "provide" private Perl libs or redundant unversioned provides
%global __provides_exclude ^(perl\\(NetAddr::IP(::(InetBase|Util(PP)?))?\\)$|Util\\.so)

%description
This module provides an object-oriented abstraction on top of IP addresses
or IP subnets, that allows for easy manipulations.

%prep
%setup -q -n NetAddr-IP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%doc About-NetAddr-IP.txt Artistic Changes Copying TODO docs/rfc1884.txt
%{perl_vendorarch}/auto/NetAddr/
%{perl_vendorarch}/NetAddr/
%{_mandir}/man3/NetAddr::IP.3pm*
%{_mandir}/man3/NetAddr::IP::InetBase.3pm*
%{_mandir}/man3/NetAddr::IP::Lite.3pm*
%{_mandir}/man3/NetAddr::IP::Util.3pm*
%{_mandir}/man3/NetAddr::IP::UtilPP.3pm*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.069-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.069-2
- Mass rebuild 2013-12-27

* Sun May 26 2013 Paul Howarth <paul@city-fan.org> - 4.069-1
- Update to 4.069
  - Add proper pod encoding in Lite.pm
  - Changed Makefile.PL to check for config.h when building for XS with 'gcc',
    try building with 'cc', and check again; if config.h is not found, force
    Pure Perl mode
  - Kill XS in winduhs and Darwin, both of which misbehave when compiling XS
    code
- Drop UTF8 patch, no longer needed

* Wed Apr  3 2013 Paul Howarth <paul@city-fan.org> - 4.068-1
- Update to 4.068
  - Update Makefile.PL in Util.pm to better detect 'winduhs'

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 4.067-1
- Update to 4.067
  - Improved diagnostic message for "die" with bad mask for hostenum,
    hostenumref, split, splitref, rsplit, rsplitref
- Include new docfile About-NetAddr-IP.txt

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.066-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Petr Pisar <ppisar@redhat.com> - 4.066-2
- Change license to reflect some files allow Artistic license

* Tue Oct 30 2012 Paul Howarth <paul@city-fan.org> - 4.066-1
- Update to 4.066
  - Support bracketed IPv6 URI notation as described in RFC-3986

* Wed Oct  3 2012 Paul Howarth <paul@city-fan.org> - 4.065-1
- Update to 4.065
  - Correct format for IPv6 embedded IPv4 addresses (CPAN RT#79964)

* Thu Sep 27 2012 Paul Howarth <paul@city-fan.org> - 4.064-1
- Update to 4.064
  - Updated GPL v2.0 text and address in all modules
  - Added support for rfc3021 /31 networks to hostenum
- Update UTF8 patch

* Thu Aug 09 2012 Petr Pisar <ppisar@redhat.com> - 4.062-5
- Declare encoding of POD

* Thu Aug 09 2012 Petr Pisar <ppisar@redhat.com> - 4.062-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.062-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 4.062-2
- Perl 5.16 rebuild

* Fri Jun  8 2012 Paul Howarth <paul@city-fan.org> 4.062-1
- update to 4.062 (#802994)
  - add is_rfc1918 to Lite.pm v1.42
  - fix change in behavior introduced in v4.050 where an empty string supplied
    to "new" previously returned 'undef' and now returns 'default' for ipV4 or
    ipV6 (CPAN RT#75976)
  - documentation updates
- don't need to remove empty directories from the buildroot
- recode NetAddr::IP::Lite module and manpage as UTF-8
- don't use macros for commands

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 4.058-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Paul Howarth <paul@city-fan.org> 4.058-1
- update to 4.058
  - in Lite.pm v1.40:
    - add call to InetBase::fillIPv4 to all uses of gethostbyname
  - in InetBase.pm v0.06:
    - break out the code that expands short IPv4 addresses into dotquad format
      to account for broken BSD implementations of inet_aton and gethostbyname
      that do not recognize the short format, and EXPORT this as sub 'fillIPv4'
  - in Util.pm v1.45:
    - add 'fillIPv4' to calls to gethostbyname to work around broken inet_aton
      and gethostbyname implementations in certain BSD implementations

* Fri Nov  4 2011 Paul Howarth <paul@city-fan.org> 4.056-1
- update to 4.056
  - in InetBase.pm v0.04:
    - improve inet_aton to overcome broken gethostbyname found in NetBSD and
      OpenBSD

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> 4.055-1
- update to 4.055
  - in Lite.pm v1.38:
    - patch for CPAN RT#71869: issues with Math::BigInt variants

* Fri Oct 28 2011 Paul Howarth <paul@city-fan.org> 4.054-1
- update to 4.054
  - in Lite.pm v1.37:
    - fix CPAN RT#71925, a sub-variant of CPAN RT#62521 that showed up only for
      short notation for IPv4, e.g. 127/n, 127.0/n, 127.0.0/n but not
      127.0.0.0/n
    - remove Calc.pm
    - add detection of early Math::BigInt object structure
    - fix CPAN RT#71869 - a failed test routine
- upstream no longer ships README so no need to fix its encoding

* Wed Oct 26 2011 Paul Howarth <paul@city-fan.org> 4.052-1
- update to 4.052
  - in InetBase.pm v0.03:
    - Socket6 prior to version 0.23 does not have AF_INET6 in the EXPORT_OK
      array; modify InetBase.pm to work around this
    - remove reference to Config{osname}
  - in Lite.pm v1.35:
    - add support for Math::BigInt to NetAddr::IP::Lite
    - use Math::BigInt::Calc for creating BigInt values and fall back to
      NetAddr::IP::Calc if Math::BigInt is not present (fixes CPAN RT#71869)
- BR: perl(Data::Dumper) and perl(Math::BigInt)
- add runtime dependency on perl(Math::BigInt) for performance and consistency
- update UTF-8 patch to apply cleanly

* Thu Oct 20 2011 Paul Howarth <paul@city-fan.org> - 4.049-1
- update to 4.049
  - in Lite v1.32:
    - add capability to parse input of the form ->new6(12345,1); this should
      have been there but was missing (CPAN RT#68723)
  - in Util v1.41:
    - add inet_pton, inet_ntop, AF_INET, AF_INET6
    - modify inet_n2dx and inet_n2ad to recognize the new 128-bit IPv4 format
      ::FFFF:FFFF:0:0
    - replace isIPv4 with a pure perl version for portability
  - split the following into NetAddr::IP::InetBase v0.01 to provide better
    long-term support for IPv6:
    - inet_aton
    - inet_ntoa
    - ipv6_aton
    - ipv6_n2x
    - ipv6_n2d
    - inet_any2n
    - inet_n2dx
    - inet_n2ad
    - inet_ntop
    - inet_pton
    - packzeros
    - isIPv4
    - isNewIPv4
    - isAnyIPv4
    - AF_INET
    - AF_INET6
- BR: perl(Carp)
- BR: perl(Socket6) for test suite
- update UTF-8 patch to apply cleanly
- license is now GPL+ or Artistic in most of the code but Util.xs is GPLv2+ so
  we ship the whole thing under that license

* Fri Oct 07 2011 Petr Sabata <contyk@redhat.com> - 4.047-1
- 4.047 bump

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 4.044-4
- Fix RPM 4.9 dependency filtering

* Thu Jul 21 2011 Paul Howarth <paul@city-fan.org> - 4.044-3
- use a patch rather than scripted iconv to fix character encoding
- use rpm native provides filtering
- make %%files list more explicit

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.044-2
- Perl mass rebuild

* Tue Jun  7 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.044-1
- update to 4.044
- clean specfile

* Wed Apr  6 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.042-1
- update to 4.042, because we had terribly old release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.027-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.027-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.027-4
- Mass rebuild with perl-5.12.0

* Wed Feb 17 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4.027-3
- make rpmlint happy

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.027-2
- rebuild against perl 5.10.1

* Wed Sep 16 2009 Warren Togami <wtogami@redhat.com> - 4.027-1
- 4.027

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.007-3
- fix license tag

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.007-2
- rebuild for new perl

* Tue Feb 12 2008 Andreas Thienemann <athienem@redhat.com> 4.007-1
- Updated to 4.007
- Rebuilt against gcc-4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 4.004-4
- Rebuild for selinux ppc32 issue.

* Tue Jul 10 2007 Andreas Thienemann <andreas@bawue.net> 4.004-3
- Fixed missing BR on rawhide

* Thu Apr 26 2007 Andreas Thienemann <andreas@bawue.net> 4.004-2
- Moar docs!

* Thu Apr 12 2007 Andreas Thienemann <andreas@bawue.net> 4.004-1
- Specfile autogenerated by cpanspec 1.69.1.
- Cleand up for FE
