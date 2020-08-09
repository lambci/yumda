Name:           perl-HTTP-Message
Version:        6.06
Release:        6%{?dist}
Summary:        HTTP style message
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTTP-Message/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/HTTP-Message-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(Encode) >= 2.21
BuildRequires:  perl(Encode::Locale) >= 1
BuildRequires:  perl(Exporter)
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(IO::Compress::Bzip2) >= 2.021
BuildRequires:  perl(IO::Compress::Deflate)
BuildRequires:  perl(IO::Compress::Gzip)
BuildRequires:  perl(IO::HTML)
BuildRequires:  perl(IO::Uncompress::Bunzip2) >= 2.021
BuildRequires:  perl(IO::Uncompress::Gunzip)
BuildRequires:  perl(IO::Uncompress::Inflate)
BuildRequires:  perl(IO::Uncompress::RawInflate)
BuildRequires:  perl(LWP::MediaTypes) >= 6
BuildRequires:  perl(MIME::Base64) >= 2.1
BuildRequires:  perl(MIME::QuotedPrint)
BuildRequires:  perl(Storable)
BuildRequires:  perl(URI) >= 1.10
BuildRequires:  perl(vars)
# Tests only:
BuildRequires:  perl(Config)
BuildRequires:  perl(PerlIO::encoding)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Testing requires Time::Local on MacOS only
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(Encode) >= 2.21
Requires:       perl(Encode::Locale) >= 1
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(IO::Compress::Bzip2) >= 2.021
Requires:       perl(IO::Compress::Deflate)
Requires:       perl(IO::Compress::Gzip)
Requires:       perl(IO::HTML)
Requires:       perl(IO::Uncompress::Bunzip2) >= 2.021
Requires:       perl(IO::Uncompress::Gunzip)
Requires:       perl(IO::Uncompress::Inflate)
Requires:       perl(IO::Uncompress::RawInflate)
Requires:       perl(LWP::MediaTypes) >= 6
Requires:       perl(MIME::Base64) >= 2.1
Requires:       perl(MIME::QuotedPrint)
Requires:       perl(Storable)
Requires:       perl(URI) >= 1.10
Conflicts:      perl-libwww-perl < 6

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((HTTP::Date|URI)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(HTTP::Headers\\)$

%description
The HTTP-Message distribution contains classes useful for representing the
messages passed in HTTP style communication.  These are classes representing
requests, responses and the headers contained within them.

%prep
%setup -q -n HTTP-Message-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6.06-6
- Mass rebuild 2013-12-27

* Tue Jul 23 2013 Petr Šabata <contyk@redhat.com> - 6.06-5
- Add missing dependencies

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 6.06-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Petr Šabata <contyk@redhat.com> - 6.06-2
- BuildRequire perl(Carp)
- Modernize the spec and drop command macros

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 6.06-1
- 6.06 bump

* Tue Oct 02 2012 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 6.03-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.03-3
- Perl 5.16 rebuild

* Fri Apr 06 2012 Petr Pisar <ppisar@redhat.com> - 6.03-2
- Break build-time cycle while boostrapping perl (bug #810223)

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 6.03-1
- 6.03 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.02-3
- add new filter

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.02-2
- Perl mass rebuild

* Wed Mar 23 2011 Petr Pisar <ppisar@redhat.com> - 6.02-1
- 6.02 bump

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> 6.01-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Conflicts with perl-libwww-perl 5* and older
