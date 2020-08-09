Name:           perl-IO-Socket-IP
Version:        0.21
Release:        5%{?dist}
Summary:        Drop-in replacement for IO::Socket::INET supporting both IPv4 and IPv6
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-Socket-IP/
Source0:        http://www.cpan.org/authors/id/P/PE/PEVANS/IO-Socket-IP-%{version}.tar.gz
Patch0:         IO-Socket-IP-so_reuseport.patch
# 1/2 Fix constructing sockets without specifying host or family, bug #1492760,
# CPAN RT#91982, fixed in 0.25
Patch1:         IO-Socket-IP-0.21-Ensure-that-a-Host-Family-less-constructor-still-con.patch
# 2/2 Fix constructing sockets without specifying host or family, bug #1492760,
# fixed in 0.29
Patch2:         IO-Socket-IP-0.21-Correct-prototol-family-in-hints.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Errno)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket) >= 1.97
BuildRequires:  perl(Socket6)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%{?perl_default_filter}

Prefix: %{_prefix}

%description
This module provides a protocol-independent way to use IPv4 and IPv6
sockets, as a drop-in replacement for IO::Socket::INET. Most constructor
arguments and methods are provided in a backward-compatible way.

%prep
%setup -q -n IO-Socket-IP-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
perl Build.PL installdirs=vendor \
  prefix=%{_prefix} \
  installvendorlib=%{perl_vendorlib} \
  installvendorarch=%{perl_vendorarch}
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%files
%license LICENSE
%{perl_vendorlib}/*

%exclude %{_mandir}

%changelog
* Sun Aug 9 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Sep 18 2017 Petr Pisar <ppisar@redhat.com> - 0.21-5
- Fix constructing sockets without specifying host or family (bug #1492760)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.21-4
- Mass rebuild 2013-12-27

* Thu Jul 18 2013 Petr Šabata <contyk@redhat.com> - 0.21-3
- Disable the SO_REUSEPORT test; koji builders don't support this feature yet

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.21-2
- Perl 5.18 rebuild

* Mon Apr 29 2013 Petr Šabata <contyk@redhat.com> - 0.21-1
- 0.21 bump

* Wed Apr 17 2013 Petr Šabata <contyk@redhat.com> - 0.20-1
- 0.20 bump

* Tue Mar 12 2013 Petr Šabata <contyk@redhat.com> - 0.19-1
- 0.19 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Petr Šabata <contyk@redhat.com> - 0.18-1
- 0.18 bump

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 0.17-2
- Fix a typo, sort the deps

* Wed Aug 22 2012 Petr Šabata <contyk@redhat.com> - 0.17-1
- 0.17 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.16-2
- Perl 5.16 rebuild

* Mon Jun 25 2012 Petr Šabata <contyk@redhat.com> - 0.16-1
- 0.16 (IO::Socket::INET compatibility enhancement)

* Thu Jun 21 2012 Petr Šabata <contyk@redhat.com> - 0.15-1
- 0.15 bump

* Tue Jun 19 2012 Petr Šabata <contyk@redhat.com> - 0.14-1
- 0.14 bump

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Šabata <contyk@redhat.com> - 0.11-1
- 0.11 bump

* Fri May 11 2012 Petr Šabata <contyk@redhat.com> - 0.10-1
- 0.10 bump

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 0.09-1
- 0.09 bump

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> 0.08-1
- Specfile autogenerated by cpanspec 1.78.
