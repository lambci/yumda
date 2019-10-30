%define _buildid .2

Name:		libmcrypt
Version:	2.5.8
Release: 9.1%{?_buildid}%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Summary:	Encryption algorithms library
URL:		http://mcrypt.sourceforge.net/
Source0:	http://download.sourceforge.net/mcrypt/libmcrypt-%{version}.tar.gz
Patch0:		libmcrypt-2.5.8-nolibltdl.patch
# Upstream:
# http://sourceforge.net/tracker/index.php?func=detail&aid=1872801&group_id=87941&atid=584895
Patch1:		libmcrypt-2.5.8-uninitialized.patch
# Upstream:
# http://sourceforge.net/tracker/index.php?func=detail&aid=1872799&group_id=87941&atid=584895
Patch2:		libmcrypt-2.5.8-prototypes.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool-ltdl-devel

Prefix: %{_prefix}

%description
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .uninitialized
%patch2 -p1 -b .prototypes

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING.LIB
%{_libdir}/*.so.*
%{_mandir}/man3/*

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_bindir}/libmcrypt-config
%exclude %{_libdir}/*.so
%exclude %{_datadir}

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Fri Jul 9 2010 22:19:53 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libmcrypt-2.5.8-9.1.el6

* Fri Jul 9 2010 20:47:26 UTC Cristian Gafton <gafton@amazon.com>
- setup complete for package libmcrypt
