%global cpan_version 3.20
Name:           perl-Pod-Perldoc
# let's overwrite the module from perl.srpm
Version:        %(echo '%{cpan_version}' | sed 's/_/./')
Release:        4%{?dist}
Summary:        Look up Perl documentation in Pod format
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Pod-Perldoc/
Source0:        http://www.cpan.org/authors/id/M/MA/MALLEN/Pod-Perldoc-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
# Pod::Perldoc::ToMan executes roff
BuildRequires:  groff-base
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.22
BuildRequires:  perl(HTTP::Tiny)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(lib)
BuildRequires:  perl(parent)
BuildRequires:  perl(Pod::Man) >= 2.18
BuildRequires:  perl(Pod::Simple::Checker)
BuildRequires:  perl(Pod::Simple::RTF) >= 3.16
BuildRequires:  perl(Pod::Simple::XMLOutStream) >= 3.16
BuildRequires:  perl(Pod::Text)
BuildRequires:  perl(Pod::Text::Color)
BuildRequires:  perl(Pod::Text::Termcap)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap}
%if !( 0%{?rhel} >= 7 )
BuildRequires:  perl(Tk)
BuildRequires:  perl(Tk::Pod)
%endif
%endif
# Pod::Perldoc::ToMan executes roff
Requires:       groff-base
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Encode)
Requires:       perl(File::Temp) >= 0.22
Requires:       perl(HTTP::Tiny)
Requires:       perl(IO::Handle)
Requires:       perl(IPC::Open3)
Requires:       perl(lib)
Requires:       perl(Pod::Man) >= 2.18
Requires:       perl(Pod::Simple::Checker)
Requires:       perl(Pod::Simple::RTF) >= 3.16
Requires:       perl(Pod::Simple::XMLOutStream) >= 3.16
Requires:       perl(Text::ParseWords)
# Tk is optional
Requires:       perl(Symbol)

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Pod::Man|Pod::Simple::XMLOutStream|Pod::Simple::RTF\\)\\s*$

%description
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.

%prep
%setup -q -n Pod-Perldoc-%{cpan_version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*
# Correct perldoc.pod location, bug #1015993, CPAN RT#88898
mv ${RPM_BUILD_ROOT}%{perl_vendorlib}/{Pod,}/perldoc.pod

%check
make test

%files
%doc Changes README
%{_bindir}/perldoc
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.20-4
- Mass rebuild 2013-12-27

* Mon Oct 07 2013 Petr Pisar <ppisar@redhat.com> - 3.20-3
- Correct perldoc.pod location (bug #1015993)

* Thu May 23 2013 Petr Pisar <ppisar@redhat.com> - 3.20-2
- Specify all dependencies

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 3.20-1
- 3.20 bump

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 3.19.01-1
- 3.19_01 bump

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 3.19.00-1
- 3.19 bump

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 3.17.00-241
- Do not build-require perl(Tk) on RHEL >= 7
- Depend on perl(HTTP::Tiny)

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.17.00-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.17-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 3.17-7
- Perl 5.16 rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 3.17-6
- Require groff-base because Pod::Perldoc::ToMan executes roff

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.17-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 3.17-4
- Omit optional Tk tests on bootstrap

* Wed May 30 2012 Marcela Mašláňová <mmaslano@redhat.com> - 3.17-3
- conditionalize optional BR tests

* Tue May 15 2012 Petr Pisar <ppisar@redhat.com> - 3.17-2
- Fix perldoc synopsis (bug #821632)

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 3.17-1
- 3.17 bump
- Fix displaying long POD in groff

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> 3.15-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr from spec code.
- perl(Config) BR removed
- Source URL fixed to point to BDFOY author
- Do not require unversioned perl(Pod::Simple::RTF)
