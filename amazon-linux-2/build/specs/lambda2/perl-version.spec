Name:           perl-version
Epoch:          3
Version:        0.99.07
%global module_version 0.9907
Release:        3%{?dist}
Summary:        Perl extension for Version Objects
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/version/
Source0:        http://www.cpan.org/authors/id/J/JP/JPEACOCK/version-%{module_version}.tar.gz
# Support parsing tainted values, bug #1378885, in upstream 0.9908
Patch0:         version-0.9907-Deal-with-certain-tiedscalars-e.g.-created-by-Readon.patch
# Support stringifying version objects made from a tainted value, bug #1378885,
# CPAN RT#118087
Patch1:         version-0.9907-Stringify-tainted-version-object-on-perl-older-than-.patch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.13
# IO::Handle is optional
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(locale)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.45
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(UNIVERSAL)
Requires:       perl(XSLoader)

%{?perl_default_filter}
# version::vxs is private module (see bug #633775)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(version::vxs\\)

Prefix: %{_prefix}

%description
Version objects were added to Perl in 5.10. This module implements version
objects for older version of Perl and provides the version object API for
all versions of Perl. All previous releases before 0.74 are deprecated and
should not be used due to incompatible API changes. Version 0.77 introduces
the new 'parse' and 'declare' methods to standardize usage. You are
strongly urged to set 0.77 as a minimum in your code.

%prep
%setup -q -n version-%{module_version}
%patch0 -p1
%patch1 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} +
%{_fixperms} %{buildroot}/*

%files
%license README
%doc %{perl_vendorarch}/version.pod
%dir %{perl_vendorarch}/version/
%doc %{perl_vendorarch}/version/Internals.pod
%{perl_vendorarch}/auto/version/
%{perl_vendorarch}/version.pm
%{perl_vendorarch}/version/vpp.pm
%{perl_vendorarch}/version/vxs.pm
%{perl_vendorarch}/version/regex.pm

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Sep 27 2016 Petr Pisar <ppisar@redhat.com> - 3:0.99.07-3
- Support making version objects from tainted strings (bug #1378885)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3:0.99.07-2
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Petr Šabata <contyk@redhat.com> - 3:0.99.07-1
- 0.9907 bugfix bump

* Tue Jan 07 2014 Petr Šabata <contyk@redhat.com> - 3:0.99.06-1
- 0.9906 bump

* Tue Sep 10 2013 Petr Šabata <contyk@redhat.com> - 3:0.99.04-2
- Release bump to (hopefully) fix the build

* Tue Sep 10 2013 Petr Šabata <contyk@redhat.com> - 3:0.99.04-1
- 0.9904 bump

* Mon Aug 26 2013 Petr Šabata <contyk@redhat.com> - 3:0.99.03-1
- 0.9903 bump
- Prefer %%global over %%define

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.99.02-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 3:0.99.02-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3:0.99.02-3
- Perl 5.18 rebuild
>>>>>>> fc/master

* Tue Jul 02 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.02-2
- Specify all dependencies

* Thu Mar  7 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.02-1
- 0.9902 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.99.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99.01-1
- 0.9901 bump

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 3:0.99-241
- Add test BR perl(Test::Harness)
- Remove %%defattr

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 3:0.99-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 3:0.99-1
- 0.99 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.88-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3:0.88-9
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 3:0.88-8
- Fix dependencies

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.88-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3:0.88-6
- change path on vendor, so our debuginfo are not conflicting with
  perl core debuginfos

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 3:0.88-5
- update filtering for rpm 4.9

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3:0.88-4
- Perl mass rebuild

* Fri Apr 08 2011 Petr Pisar <ppisar@redhat.com> - 3:0.88-3
- Unexport private version::vxs module (bug #633775)
- Remove BuildRoot stuff

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:0.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> 3:0.88-1
- Update to 0.88
- Revert to Makefile.PL flow as upstream dropped Build.PL to avoid circular
  dependencies
- Install into perl directories rather than vendor directories
- Mark Pod files as %%doc

* Tue Mar 09 2010 Marcela Mašláňová <mmaslano@redhat.com> 3:0.82-1
- Specfile autogenerated by cpanspec 1.78.
