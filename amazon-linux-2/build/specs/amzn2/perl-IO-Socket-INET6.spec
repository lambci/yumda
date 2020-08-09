Name:           perl-IO-Socket-INET6
Version:        2.69
Release:        5%{?dist}
Summary:        Perl Object interface for AF_INET|AF_INET6 domain sockets
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/~mondejar/IO-Socket-INET6/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/IO-Socket-INET6-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Errno)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
IO::Socket::INET6 provides an object interface to creating and using
sockets in either AF_INET or AF_INET6 domains. It is built upon the
IO::Socket interface and inherits all the methods defined by IO::Socket.

%prep
%setup -q -n IO-Socket-INET6-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}

%check
make test

%files
%doc README ChangeLog
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Socket::INET6.3*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.69-5
- Mass rebuild 2013-12-27

* Thu Aug 01 2013 Petr Šabata <contyk@redhat.com> - 2.69-4.1
- Add a better description
- Fix the dependency list

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 2.69-4
- Modernize the spec a bit and add Carp to BRs

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.69-2
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 2.69-1
- Update to 2.69:
  - Solved symbol clashes in t/io_multihomed6.t (CPAN RT#72769)
  - Fix the imports on t/io_multihomed6.t (CPAN RT#72769)
  - Update the link to the repository in Build.PL
- BR: perl(IO::Socket)
- BR: perl(Socket)
- Use %%{_fixperms} macro instead of our own chmod incantation

* Wed Jul 27 2011 Petr Sabata <contyk@redhat.com> - 2.67-1
- 2.67 bump

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.66-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.66-1
- Update to 2.66
  - Fix inet_pton/inet_ntop import warnings (CPAN RT#55901)
  - Fix listening on :: or 0.0.0.0 (CPAN RT#54656)
  - Add test listen_port_only.t
  - Solved problems with multihomed and family order (CPAN RT#57676)
  - Fix select timeout issue in t/io_multihomed6.t
  - Fix t/io_multihomed6.t on systems with broken getaddrinfo() (CPAN RT#58198)
  - Made the "use Socket" call import constants selectively, and not rely on
    @EXPORT's whims

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.57-4
- s/PERL_INSTALL_ROOT/DESTDIR/
- re-enable the test suite
- BR: perl(Test::More), perl(Test::Pod), perl(Test::Pod::Coverage)

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.57-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.57-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.57-1
- new upstream version

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.56-4
- fix the source url

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.56-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 2.56-1
- 2.56

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 26 2008 Warren Togami <wtogami@redhat.com> - 2.54-1
- 2.54

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-5
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-4
- rebuild for new perl

* Fri Nov 16 2007 Parag Nemade <panemade@gmail.com> - 2.51-3
- Merge Review(#226263) Spec cleanup

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Jul 06 2006 Warren Togami <wtogami@redhat.com> 2.51-2
- minor spec fixes (#197821)

* Thu Jul 06 2006 Warren Togami <wtogami@redhat.com> 2.51-1
- initial Fedora package
