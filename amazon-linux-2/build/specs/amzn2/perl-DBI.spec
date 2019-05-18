# According to documentation, module using Coro is just:
# A PROOF-OF-CONCEPT IMPLEMENTATION FOR EXPERIMENTATION.
%if 0%{?rhel} >= 7 
%bcond_with coro
%else
%bcond_without coro
%endif

Name:           perl-DBI
Version:        1.627
Release: 4%{?dist}.0.2
Summary:        A database access API for perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
Source0:        http://www.cpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
# Add a security warning about use of RPC::PlClient, bug #1030578, CPAN RT#90475
Patch0:         DBI-1.630-Security-notice-for-Proxy.patch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Carp)
# Clone is optional
BuildRequires:  perl(Clone) >= 0.34
BuildRequires:  perl(Config)
%if %{with coro}
BuildRequires:  perl(Coro)
BuildRequires:  perl(Coro::Handle)
BuildRequires:  perl(Coro::Select)
%endif
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
# DB_File is optional
BuildRequires:  perl(DB_File)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Math::BigInt)
# MLDBM is optional
%if ! ( 0%{?rhel} )
BuildRequires:  perl(MLDBM)
%endif
# Params::Util is optional
# RPC::PlClient is optional
BuildRequires:  perl(RPC::PlClient) >= 0.2000
# RPC::PlServer is optional
BuildRequires:  perl(RPC::PlServer)
BuildRequires:  perl(Scalar::Util)
# SQL::Statement is optional, and it requires DBI
%if 0%{!?perl_bootstrap:1} && ! ( 0%{?rhel} )
BuildRequires:  perl(SQL::Statement) >= 1.402
%endif
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(threads)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(lib)
BuildRequires:  perl(Net::Daemon::Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple) >= 0.90
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Math::BigInt)

# Filter unwanted dependencies
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(RPC::\\)

%description 
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.

%prep
%setup -q -n DBI-%{version} 
%patch0 -p1
iconv -f iso8859-1 -t utf-8 lib/DBD/Gofer.pm >lib/DBD/Gofer.pm.new &&
  mv lib/DBD/Gofer.pm{.new,}
chmod 644 ex/*
chmod 744 dbixs_rev.pl
sed -i 's?#!perl?#!%{__perl}?' ex/corogofer.pl
%if %{without coro}
rm lib/DBD/Gofer/Transport/corostream.pm
sed -i -e '/^lib\/DBD\/Gofer\/Transport\/corostream.pm$/d' MANIFEST
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*
# Remove Win32 specific files and man pages to avoid unwanted dependencies
rm -rf %{buildroot}%{perl_vendorarch}/{Win32,DBI/W32ODBC.pm} \
    %{buildroot}%{_mandir}/man3/{DBI::W32,Win32::DBI}ODBC.3pm
perl -pi -e 's"#!perl -w"#!/usr/bin/perl -w"' \
    %{buildroot}%{perl_vendorarch}/{goferperf,dbixs_rev}.pl

%check
make test

%files
# Changes already packaged as DBI::Changes
%doc README.md ex/
%{_bindir}/dbipro*
%{_bindir}/dbilogstrip
%{perl_vendorarch}/*.p*
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/DBI/
%{perl_vendorarch}/auto/DBI/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.627-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.627-3
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Petr Pisar <ppisar@redhat.com> - 1.627-2
- Add a security warning about use of RPC::PlClient (bug #1030578)

* Mon May 20 2013 Petr Pisar <ppisar@redhat.com> - 1.627-1
- 1.627 bump

* Thu May 16 2013 Petr Pisar <ppisar@redhat.com> - 1.626-1
- 1.626 bump

* Tue Apr 02 2013 Petr Šabata <contyk@redhat.com> - 1.625-1
- 1.625 bump, perl5.17 fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.623-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Petr Šabata <contyk@redhat.com> - 1.623-1
- 1.623 bump

* Mon Aug 27 2012 Petr Pisar <ppisar@redhat.com> - 1.622-6
- Disable Coro properly

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.622-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.622-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.622-3
- Conditionalize usage of Coro, which is used in experimental module
  and MLDB and SLQ::Statement. 
 
* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.622-2
- Perl 5.16 rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.622-1
- 1.622 bump

* Fri Apr 27 2012 Petr Šabata <contyk@redhat.com> - 1.620-1
- 1.620 bump
- Removing some perl-provided explicit dependencies

* Fri Apr  6 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.618-3
- 810370 apply Paul's bootstrap macro

* Mon Feb 27 2012 Petr Pisar <ppisar@redhat.com> - 1.618-2
- Build-require optional Test::Pod::Coverage

* Mon Feb 27 2012 Petr Pisar <ppisar@redhat.com> - 1.618-1
- 1.618 bump

* Tue Jan 31 2012 Petr Šabata <contyk@redhat.com> - 1.617-1
- 1.617 bump
- Modernize spec
- Remove now obsolete perl(DBI) Provides

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.616-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.616-4
- Perl mass rebuild

* Tue Mar 15 2011 Ville SkyttÃ¤ <ville.skytta@iki.fi> - 1.616-3
- Adapt dependency filtering for rpmbuild >= 4.9.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.616-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Petr Sabata <psabata@redhat.com> - 1.616-1
- 1.616 version bump

* Wed Sep 29 2010 jkeating - 1.615-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Petr Sabata <psabata@redhat.com> - 1.615-1
- 1.615 version bump

* Mon Sep 20 2010 Petr Sabata <psabata@redhat.com> - 1.614-1
- 1.614 version bump

* Mon Aug  2 2010 Petr Sabata <psabata@redhat.com> - 1.613-1
- 1.613 version bump

* Mon Jun  7 2010 Petr Pisar <ppisar@redhat.com> - 1.611-1
- 1.611 bump
- Add BuildRequires perl(RPC::PlClient) to cover some optional tests
- Fix indentation

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.609-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.609-4
- rebuild against perl 5.10.1

* Thu Sep 24 2009 Stepan Kasal <skasal@redhat.com> - 1.609-3
- provide versioned perl(DBI)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.609-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 1.609-1
- new upstream version
- drop unneeded build patch
- move the iconv to convert the source

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.607-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.607-1
- update

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.601-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.601-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.601-2
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.601-1
- Update to latest CPAN version: 1.601
- Fix some issues from package review:
  - patch to change #! line in script
  - make script executable
  - fix requires and buildrequires

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 1.58-2
- Rebuild

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 1.58-1
- Update to latest CPAN version: 1.58

* Thu Jun 07 2007 Robin Norwood <rnorwood@redhat.com> - 1.56-1
- Update to latest CPAN version: 1.56
- Move the filter requires step into %%prep
- Remove very old patch (for perl 5.8.1)
- Fix a couple of rpmlint issues (non-UTF8 manpage and script with
  incorrect shebang line

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.53-1
- Upgrade to latest CPAN version: 1.53

* Thu Aug 24 2006 Robin Norwood <rnorwood@redhat.com> - 1.52-1
- Upgrade to 1.52 for bug #202310
        
* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 1.51-1
- Upgrade to 1.51

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.50-3
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.50-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.50-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.50-2
- rebuild for new perl-5.8.8 / gcc / glibc

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 1.50-1
- upgrade to 1.50

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Apr 13 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 1.48-4
- (#154762)
- License information: GPL or Artistic
- Removed the Time::HiRes building requirement (see Changes)
- Removed the empty .bs file
- Corrected file permissions

* Mon Apr 04 2005 Warren Togami <wtogami@redhat.com> 1.48-3
- filter perl(Apache) (#153673)

* Fri Apr 01 2005 Robert Scheck <redhat@linuxnetz.de> 1.48-2
- spec file cleanup (#153164)

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.48-1
- 1.48

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.40-1
- update to 1.40

* Fri Dec 19 2003 Chip Turner <cturner@redhat.com> 1.39-1
- update to 1.39

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 1.37-1
- upgrade to 1.37

* Wed Apr  2 2003 Chip Turner <cturner@redhat.com> 1.32-6
- add buildrequires on perl-Time-HiRes

* Tue Feb 18 2003 Chip Turner <cturner@redhat.com>
- update dependency filter to remove dependency on perl(Apache) that
- crept in (#82927)

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use rpm internal dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.30-1
- 1.30. 

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.28-1
- 1.28
- Building it also fixes #66304

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.23-2
- Tweak dependency finder - filter out a dependency found within the 
  doc section of a module

* Tue Jun  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.23-1
- 1.23
- Some changes to integrate with new Perl
- Update URL

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.21-2
- Rebuild

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.21-1
- 1.21

* Fri Feb  8 2002 Chip Turner <cturner@redhat.com>
- filter out "soft" dependencies: perl(RPC::PlClient) and perl(Win32::ODBC)

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.201-2
- Rebuild

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.201-1
- 1.201

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.20-1
- 1.20
- Proper URL

* Sat Jun 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.18

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.16
- change group to Applications/Databases from Applications/CPAN

* Tue May  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.15

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Cleanups

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- build for main distribution
- use %%{_tmppath}
- change name of specfile
- don't use a find script to generate file lists
- general cleanup
- add descriptive summary and description

* Mon Aug 14 2000 Tim Powers <timp@redhat.com>
- Spec file was autogenerated. 
