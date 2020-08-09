Name:           perl-libwww-perl
Version:        6.05
Release:        2%{?dist}
Summary:        A Perl interface to the World-Wide Web
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/libwww-perl/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/libwww-perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode) >= 2.12
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Listing) >= 6
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::HeadParser)
BuildRequires:  perl(HTTP::Cookies) >= 6
BuildRequires:  perl(HTTP::Daemon) >= 6
BuildRequires:  perl(HTTP::Date) >= 6
BuildRequires:  perl(HTTP::Negotiate) >= 6
BuildRequires:  perl(HTTP::Request) >= 6
BuildRequires:  perl(HTTP::Request::Common) >= 6
BuildRequires:  perl(HTTP::Response) >= 6
BuildRequires:  perl(HTTP::Status) >= 6
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(LWP::MediaTypes) >= 6
BuildRequires:  perl(MIME::Base64) >= 2.1
BuildRequires:  perl(Net::FTP) >= 2.58
BuildRequires:  perl(Net::HTTP) >= 6.04
BuildRequires:  perl(strict)
BuildRequires:  perl(URI) >= 1.10
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(vars)
BuildRequires:  perl(WWW::RobotRules) >= 6
# Tests only:
BuildRequires:  perl(Config)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Encode) >= 2.12
Requires:       perl(File::Listing) >= 6
Requires:       perl(HTML::Entities)
Requires:       perl(HTML::HeadParser)
Requires:       perl(HTTP::Cookies) >= 6
Requires:       perl(HTTP::Daemon) >= 6
Requires:       perl(HTTP::Date) >= 6
Requires:       perl(HTTP::Negotiate) >= 6
Requires:       perl(HTTP::Request) >= 6
Requires:       perl(HTTP::Request::Common) >= 6
Requires:       perl(HTTP::Response) >= 6
Requires:       perl(HTTP::Status) >= 6
Requires:       perl(LWP::MediaTypes) >= 6
Requires:       perl(MIME::Base64) >= 2.1
Requires:       perl(Net::FTP) >= 2.58
Requires:       perl(Net::HTTP) >= 6.04
Requires:       perl(URI) >= 1.10
Requires:       perl(URI::Escape)
Requires:       perl(WWW::RobotRules) >= 6

Prefix: %{_prefix}

%description
The libwww-perl collection is a set of Perl modules which provides a simple and
consistent application programming interface to the World-Wide Web.  The main
focus of the library is to provide classes and functions that allow you to
write WWW clients. The library also contain modules that are of more general
use and even classes that help you implement simple HTTP servers.

# Remove not-packaged features
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Authen::NTLM\\)
%global __requires_exclude %__requires_exclude|perl\\(HTTP::GHTTP\\)
# Remove underspecified dependencies
%global __requires_exclude %__requires_exclude|^perl\\(Encode\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(File::Listing\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Date\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Negotiate\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Request\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Response\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Status\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(LWP::MediaTypes\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(MIME::Base64\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(Net::HTTP\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(URI\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(WWW::RobotRules\)\\s*$

%prep
%setup -q -n libwww-perl-%{version} 

%build
# Install the aliases by default
perl Makefile.PL INSTALLDIRS=perl --aliases \
  PREFIX=%{_prefix} \
  INSTALLPRIVLIB=%{perl_privlib} \
  < /dev/null
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
chmod -R u+w %{buildroot}/*

sed -i '1 s|^#!/usr/bin/perl|#!%{_bindir}/perl|' %{buildroot}%{_bindir}/*

%files
%license README*
%{_bindir}/*
%{perl_privlib}/lwp*.pod
%{perl_privlib}/LWP.pm
%{perl_privlib}/LWP/

%exclude %{_mandir}

%changelog
* Sun Aug 9 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6.05-2
- Mass rebuild 2013-12-27

* Mon Aug 05 2013 Petr Šabata <contyk@redhat.com> - 6.05-1.1
- Add some missing build-time dependencies
- Fix bogus dates in changelog

* Tue Mar 12 2013 Petr Pisar <ppisar@redhat.com> - 6.05-1
- 6.05 bump

* Fri Mar 08 2013 Petr Pisar <ppisar@redhat.com> - 6.04-5
- Honor time-out (bug #919448)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 6.04-2
- Perl 5.16 rebuild

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Petr Pisar <ppisar@redhat.com> - 6.03-1
- 6.03 bump
- Remove RPM 4.8 dependecy filters

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 6.02-3
- RPM 4.9 dependency filtering added

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 6.02-2
- Perl mass rebuild

* Mon Mar 28 2011 Petr Pisar <ppisar@redhat.com> - 6.02-1
- 6.02 bump
- HTTPS support unbundled by upstream to break depency cycle in CPAN utilities.
  Install or depend on perl(LWP::Protocol::https) explicitly, if you need
  HTTPS support.

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> - 6.01-1
- 6.01 bump
- Remove BuildRoot stuff
- Remove unneeded hacks

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.837-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 5.837-2
- Add missing ':' to filter_from_requires perl(HTTP::GHTTP).
- filter_from_provides /perl(HTTP::Headers)$/d instead of /perl(HTTP::Headers)/d.

* Mon Sep 27 2010 Marcela Mašláňová <mmaslano@redhat.com> 5.837-1
- update

* Mon Jul 12 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.836-1
- update

* Mon Jun 21 2010 Jesse Keating <jkeating@redhat.com> - 5.834-1
- Bump to match what was pushed to F13.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.833-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.833-2
- rebuild against perl 5.10.1

* Fri Nov  6 2009 Marcela Mašláňová <mmaslano@redhat.com> 5.833-1
- update

* Thu Sep 17 2009 Warren Togami <cweyl@alumni.drew.edu> 5.831-1
- update to 5.831

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.825-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.825-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 5.825-1
- update to 5.825

* Thu Jan 22 2009 Marcela Mašláňová <mmaslano@redhat.com> 5.823-1
- update to 5.823

* Mon Oct 13 2008 Marcela Mašláňová <mmaslano@redhat.com> 5.817-1
- update to 5.817

* Tue Oct  7 2008 Marcela Mašláňová <mmaslano@redhat.com> 5.816-1
- update to 5.816
- fix #465855 - install --aliases by default
- use upstream patch for previous problem (see rt 38736)

* Thu Sep 18 2008 Marcela Maslanova <mmaslano@redhat.com> 5.814-2
- use untaint patch from Villa Skyte

* Thu Sep 18 2008 Marcela Maslanova <mmaslano@redhat.com> 5.814-1
- update to 5.814
- remove patch, now we have all upstream tests on

* Fri Mar  7 2008 Ville Skyttä <ville.skytta at iki.fi> - 5.808-7
- Use system /etc/mime.types instead of an outdated private copy.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.808-6
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.808-5
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-4
- Fix various issues from package review:
- Fix tabs and spacing
- Remove unneeded BR: perl
- convert non-utf-8 files to utf-8
- Resolves: bz#226268

* Tue Aug 14 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-3
- Make provides script filter out only the unversioned HTTP::Headers.

* Tue Aug 14 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-2
- Disable some of the tests, with a long explanation.

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 5.808-1
- Update to latest CPAN version
- Re-enable tests.  We'll see if they work now
- Move Requires filter into spec file
- Add Provides filter for unnecessary unversioned provides

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.805-1.1.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.805-1.1
- rebuild for new perl-5.8.8

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 5.805-1
- Upgrade to 5.805-1

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr 02 2005 Warren Togami <wtogami@redhat.com> - 5.803-2
- skip make test (#150363)

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.803-1
- Update to 5.803.
- spec cleanup (#150363)

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 5.79-6
- Convert man page to UTF-8

* Fri Aug 13 2004 Bill Nottingham <notting@redhat.com> 5.76-5
- fix %%defattr

* Mon Aug 09 2004 Alan Cox <alan@redhat.com> 5.76-4
- added missing BuildRequires on perl(HTML::Parser) [Steve Grubb]

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Warren Togami <wtogami@redhat.com> 5.76-2
- #12051 misc fixes from Ville Skyttä

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 5.76-1
- update to 5.76

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Jul 16 2002 Chip Turner <cturner@redhat.com>
- added missing Requires on perl(HTML::Entities)

* Fri Mar 29 2002 Chip Turner <cturner@redhat.com>
- added Requires: for perl-URI and perl-Digest-MD5

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
