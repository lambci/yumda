%define _buildid .8

Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.18
Release: 2%{?_buildid}%{?dist}
URL: http://www.gnu.org/software/libidn/
License: LGPLv2+ and GPLv3+ and GFDL
Source0: http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig, gettext

Prefix: %{_prefix}

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%prep
%setup -q

%build
%configure --disable-csharp --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT pkgconfigdir=%{_libdir}/pkgconfig

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la \
      $RPM_BUILD_ROOT%{_datadir}/info/*.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING*
%{_bindir}/idn
%{_libdir}/libidn.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_datadir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Fri Jul 9 2010 22:19:40 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libidn-1.18-2.el6

* Fri Jul 9 2010 22:19:39 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libidn-1.9-5.1

* Fri May 7 2010 01:54:18 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/libidn-0.6.5-1.1

* Fri May 7 2010 00:14:26 UTC Cristian Gafton <gafton@amazon.com>
- added submodule prep for package libidn
