Name:           perl-Net-Daemon
Version:        0.48
Release:        5%{?dist}
Summary:        Perl extension for portable daemons

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Net-Daemon/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MN/MNOONING/Net-Daemon-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-Pod-Perldoc
# Run-time:
BuildRequires:  perl(Getopt::Long)
# Tests:
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Test::More)
# Network tests:
%{?_with_network_tests:
BuildRequires:  perl(lib)
}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Net::Daemon is an abstract base class for implementing portable server 
applications in a very simple way. The module is designed for Perl 5.006 and 
ithreads (and higher), but can work with fork() and Perl 5.004.

The Net::Daemon class offers methods for the most common tasks a daemon 
needs: Starting up, logging, accepting clients, authorization, restricting 
its own environment for security and doing the true work. You only have to 
override those methods that aren't appropriate for you, but typically 
inheriting will safe you a lot of work anyways.


%prep
%setup -q -n Net-Daemon-%{version}
# Convert EOL
sed -i 's/\r//' README

# generate our other two licenses...
perldoc perlgpl > LICENSE.GPL
perldoc perlartistic > LICENSE.Artistic


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
%{?!_with_network_tests:
# Disable tests which will fail under mock
  rm t/config*
  rm t/fork*
  rm t/ithread*
  rm t/loop*
  rm t/single.t
  rm t/unix.t
}

make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README LICENSE.*
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.48-5
- Mass rebuild 2013-12-27

* Tue Oct 23 2012 Petr Pisar <ppisar@redhat.com> - 0.48-4
- Specify all dependencies
- Correct README end-of-lines

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 0.48-2
- Perl 5.16 rebuild

* Mon Jan 16 2012 Petr Lautrbach <plautrba@redhat.com> 0.48-1
- Update to 0.48 version
- Fix build requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.44-13
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.44-12
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-10
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.44-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Petr Lautrbach <plautrba@redhat.com> 0.44-5
- "--with network_tests" - don't remove network tests 
* Mon Oct  6 2008 Petr Lautrbach <plautrba@redhat.com> 0.44-4
- Description and License fixed
- Patch without backup 
* Mon Oct  6 2008 Petr Lautrbach <lautrba@redhat.com> 0.44-3
- Requires: fixed 
* Fri Oct  3 2008 Petr Lautrbach <lautrba@redhat.com> 0.44-2
- only-ithreads patch added
- disabled tests which fail under mock
* Fri Sep 26 2008 Petr Lautrbach <lautrba@redhat.com>
- initial rpm release
