Name:           perl-DBD-MySQL
Version:        4.023
Release:        6%{?dist}
Summary:        A MySQL interface for Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-mysql/
Source0:        http://www.cpan.org/authors/id/C/CA/CAPTTOFU/DBD-mysql-%{version}.tar.gz
# Fix transferring MYSQL_TYPE_LONG values on 64-bit big endian systems,
# bug #1311646, CPAN RT#57266, in upstream 4.033_03.
Patch0:         DBD-mysql-4.033_02-Fix-transferring-MYSQL_TYPE_LONG-values-on-64-bit-bi.patch
# Tests for transferring MYSQL_TYPE_LONG, bug #1311646, CPAN RT#57266,
# in upstream 4.035_02.
Patch1:         DBD-mysql-4.023-Tests-for-little-endian-platform.patch
BuildRequires:  mariadb, mariadb-devel, zlib-devel
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI) >= 1.08
BuildRequires:  perl(DBI::DBD)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl-DBD-mysql = %{version}-%{release}

%{?perl_default_filter}

%description 
DBD::mysql is the Perl5 Database Interface driver for the MySQL database. In
other words: DBD::mysql is an interface between the Perl programming language
and the MySQL programming API that comes with the MySQL relational database
management system.

%prep
%setup -q -n DBD-mysql-%{version}
%patch0 -p1
%patch1 -p1
# Correct file permissions
find . -type f | xargs chmod -x

for file in lib/DBD/mysql.pm ChangeLog; do
  iconv -f iso-8859-1 -t utf-8 <$file >${file}_
  touch -r ${file}{,_}
  mv -f ${file}{_,}
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" --ssl
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
# Full test coverage requires a live MySQL database
#make test

%files
%doc ChangeLog eg README TODO
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{_mandir}/man3/*.3*

%changelog
* Thu Oct 06 2016 Petr Pisar <ppisar@redhat.com> - 4.023-6
- Fix transferring MYSQL_TYPE_LONG values on 64-bit big endian systems
  (bug #1311646)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.023-5
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Honza Horak <hhorak@redhat.com> - 4.023-4
- Rebuild for mariadb-libs
  Related: #1045013

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.023-3
- Mass rebuild 2013-12-27

* Mon Apr 29 2013 Petr Šabata <contyk@redhat.com> - 4.023-2
- Force MariaDB dependency as a workaround for f19 compose

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 4.023-1
- 4.023 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 4.022-1
- 4.022 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.021-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 4.021-2
- Perl 5.16 rebuild

* Wed May 02 2012 Petr Šabata <contyk@redhat.com> - 4.021-1
- 4.021 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Petr Sabata <contyk@redhat.com> - 4.020-1
- 4.020 bump

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.019-3
- Perl mass rebuild

* Fri May 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.019-2
- apply tested patch from F-15 (is_prefix replaced by strncmp) #703185
- remove deffattr

* Mon May  9 2011 Petr Sabata <psabata@redhat.com> - 4.019-1
- 4.019 bump
- Removing the clean section
- Adding DynaLoader to BR

* Tue Mar 22 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.018-3
- rebuilt for libmysqlclient

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4.018-1
- update

* Thu Aug 12 2010 Petr Pisar <ppisar@redhat.com> - 4.017-1
- 4.017 bump (bug #623614)
- Preserve time stamps while converting character set

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 4.016-1
- 4.016 bump (bug #597759)

* Mon May 31 2010 Petr Pisar <ppisar@redhat.com> - 4.014-1
- 4.014 bump (bug #597759)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.013-5
- Mass rebuild with perl-5.12.0

* Sun Mar 07 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4.013-4
- add perl_default_filter (remove mysql.so provides)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.013-3
- rebuild against perl 5.10.1

* Mon Oct 26 2009 Stepan Kasal <skasal@redhat.com> - 4.013-2
- new upstream version

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.011-3
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 4.011-1
- new upstream version
- apply iconv on primary source

* Mon Apr  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4.010-1
- update to the latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.005-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.005-9
- respin (mysql)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.005-8
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.005-7
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.005-6
- rebuild for new perl

* Wed Dec  5 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-5
- Rebuild for new openssl

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-4
- Fix utf-8 rpmlint warning

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-3
- Use fixperms macro
- Remove BR: perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 4.005-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-2
- rebuild

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 4.005-1
- New version from CPAN: 4.005

* Thu Jun 07 2007 Robin Norwood <rnorwood@redhat.com> - 4.004-1
- New version from CPAN: 4.004
- Move requires filter into spec file

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 3.0008-1
- New version from CPAN: 3.0008

* Fri Sep 29 2006 Robin Norwood <rnorwood@redhat.com> - 3.0007-1
- Bugzilla: 208633
- Upgrade to upstream version 3.0007 version to fix some minor bugs.

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.0006-1.FC6
- Upgrade to 3.0006

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 3.0004-1.FC6
- upgrade to upstream version 3.0004

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0002-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0002-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 3.0002-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> - 3.0002-2
- rebuilt against new openssl

* Mon Jul 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.0002-1
- Update to 3.0002.

* Wed Apr 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.9007-1
- Update to 2.9007. (#156059)

* Thu Apr 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.9006-1
- Update to 2.9006.
- Specfile cleanup. (#154755)

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 2.9004-4
- Convert man page to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 2.9003-1
- update to 2.9003

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 2.9002-1
- move to 2.9002

* Thu Jul  3 2003 Chip Turner <cturner@redhat.com> 2.1021-5
- rebuild

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Wed Jan  1 2003 Chip Turner <cturner@redhat.com>
- turn ssl on and allow Makefile.PL to yse mysql_config to find proper link flags
- update to 2.1021

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use internal rpm dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 2.1017-3
- Rebuild

* Tue Jun 25 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 2.1017-2
- Rebuild, to fix #66304

* Wed Jun  5 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 2.1017-1
- New version - no longer integrated into msql-mysql modules

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-6
- Rebuild

* Fri Feb  8 2002 Chip Turner <cturner@minbar.devel.redhat.com>
- filter out "soft" dependencies: perl(Data::ShowTable)

* Thu Feb  7 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-4
- Rebuild

* Tue Jan 22 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind GlomsrÃ¸d <teg@redhat.com> 1.2219-1
- 1.2219

* Fri Jul 20 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- Add zlib-devel to buildrequires (#49536)

* Sun Jul  1 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- Add perl and perl-DBI to BuildRequires

* Wed May 30 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- Change Group to Applications/Databases

* Tue May  1 2001 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- 1.2216
- Add doc files
- Minor cleanups

* Thu Nov 30 2000 Trond Eivind GlomsrÃ¸d <teg@redhat.com>
- First cut
