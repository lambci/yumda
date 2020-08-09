# Filter the Perl extension module
%{?perl_default_filter}

Name:           perl-Socket6
Version:        0.23
Release: 15%{?dist}.0.2
Summary:        IPv6 related part of the C socket.h defines and structure manipulators

Group:          Development/Libraries
License:        BSD
URL:            http://search.cpan.org/dist/Socket6/
Source0:        http://www.cpan.org/authors/id/U/UM/UMEMOTO/Socket6-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Tests:
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module supports getaddrinfo() and getnameinfo() to intend to
enable protocol independent programming.
If your environment supports IPv6, IPv6 related defines such as
AF_INET6 are included.


%prep
%setup -q -n Socket6-%{version}
# CPAN RT #66811
sed -i -e '/MAN3PODS/d' Makefile.PL


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{perl_vendorarch}/Socket6*
%{perl_vendorarch}/auto/Socket6/
%{_mandir}/man3/Socket6.3pm*


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.23-15
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.23-14
- Mass rebuild 2013-12-27

* Fri Apr 19 2013 Petr Pisar <ppisar@redhat.com> - 0.23-13
- Produce manual pages (CPAN RT #66811)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 0.23-11
- Specify all dependencies

* Wed Aug 15 2012 Daniel Mach <dmach@redhat.com> - 0.23-10.1
- Rebuild for perl 5.16

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.23-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 0.23-1
- 0.23

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 22 2008 Robert Scheck <robert@fedoraproject.org> - 0.20-1
- Upgrade to 0.20 (#443497)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-7
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.19-6
- Autorebuild for GCC 4.3

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-5
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-4.1
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> - 0.19-4
- rebuild

* Wed Jul 12 2006 Warren Togami <wtogami@redhat.com> - 0.19-3
- import into FC6

* Thu May 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-2
- License: BSD (http://www.opensource.org/licenses/bsd-license.php).

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- First build.
