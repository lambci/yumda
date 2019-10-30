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

%description
Libogg is a library for manipulating Ogg bitstream file formats.
Libogg supports both making Ogg bitstreams and getting packets from
Ogg bitstreams.


%package devel
Summary:        Files needed for development using libogg
Group:          Development/Libraries
Requires:       libogg = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       automake

%description devel
Libogg is a library used for manipulating Ogg bitstreams. The
libogg-devel package contains the header files and documentation
needed for development using libogg.


%package devel-docs
Summary:	Documentation for developing Ogg applications
Group:		Development/Libraries
BuildArch:	noarch

%description devel-docs
Documentation for developing applications with libogg


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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/libogg.so.*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/ogg
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/libogg.so
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4

%files devel-docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}

%changelog
* Fri Jul 9 2010 22:20:11 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libogg-1.1.4-2.1.el6

* Fri May 7 2010 01:54:42 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/libogg-1.1.3-3.el5

* Fri May 7 2010 00:14:31 UTC Cristian Gafton <gafton@amazon.com>
- added submodule prep for package libogg
