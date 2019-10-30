%define _buildid .5

Summary:        The Ogg bitstream file format library
Name:           libogg
Version:        1.1.4
Release: 2.1%{?_buildid}%{?dist}
Epoch:          2
Group:          System Environment/Libraries
License:        BSD
URL:            http://www.xiph.org/
Source:         http://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)    

Prefix: %{_prefix}

%description
Libogg is a library for manipulating Ogg bitstream file formats.
Libogg supports both making Ogg bitstreams and getting packets from
Ogg bitstreams.


%prep
%setup -q


%build
sed -i "s/-O20/$RPM_OPT_FLAGS/" configure
sed -i "s/-ffast-math//" configure
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libogg.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Fri Jul 9 2010 22:20:11 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libogg-1.1.4-2.1.el6

* Fri May 7 2010 01:54:42 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/libogg-1.1.3-3.el5

* Fri May 7 2010 00:14:31 UTC Cristian Gafton <gafton@amazon.com>
- added submodule prep for package libogg
