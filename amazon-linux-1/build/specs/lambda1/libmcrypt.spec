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

%description
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

%package devel
Group:		Development/Libraries
Summary:	Development libraries and headers for libmcrypt
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries and headers for use in building applications that
use libmcrypt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .uninitialized
%patch2 -p1 -b .prototypes

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} \;

# Multilib fix
sed -i 's|-L%{_libdir}||g' $RPM_BUILD_ROOT%{_bindir}/libmcrypt-config
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/libmcrypt-config

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB ChangeLog KNOWN-BUGS README NEWS THANKS TODO
%{_libdir}/*.so.*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root,-)
%doc doc/README.key doc/README.xtea doc/example.c
%{_bindir}/libmcrypt-config
%{_includedir}/mutils/
%{_includedir}/mcrypt.h
%{_libdir}/*.so
%{_datadir}/aclocal/libmcrypt.m4

%changelog
* Fri Jul 9 2010 22:19:53 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libmcrypt-2.5.8-9.1.el6

* Fri Jul 9 2010 20:47:26 UTC Cristian Gafton <gafton@amazon.com>
- setup complete for package libmcrypt
