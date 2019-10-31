Summary:        Library for accessing USB devices
Name:           libusbx
Version:        1.0.21
Release:        1%{?dist}
Source0:        http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
# A couple of fixes from upstream
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://libusb.info/
BuildRequires:  systemd-devel doxygen
Provides:       libusb1 = %{version}-%{release}
Obsoletes:      libusb1 <= 1.0.9

%description
This package provides a way for applications to access USB devices.

Libusbx is a fork of the original libusb, which is a fully API and ABI
compatible drop in for the libusb-1.0.9 release. The libusbx fork was
started by most of the libusb-1.0 developers, after the original libusb
project did not produce a new release for over 18 months.

Note that this library is not compatible with the original libusb-0.1 series,
if you need libusb-0.1 compatibility install the libusb package.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libusb1-devel = %{version}-%{release}
Obsoletes:      libusb1-devel <= 1.0.9

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package devel-doc
Summary:        Development files for %{name}
Group:          Development/Libraries
Provides:       libusb1-devel-doc = %{version}-%{release}
Obsoletes:      libusb1-devel-doc <= 1.0.9
BuildArch:      noarch

%description devel-doc
This package contains API documentation for %{name}.


%prep
%setup -q -n libusb-%{version}

%build
%configure --disable-static --enable-examples-build
# Parallel builds seem to be broken
make
pushd doc
make docs
popd


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/*.so.*

%files devel
%{_includedir}/libusb-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/libusb-1.0.pc

%files devel-doc
%doc doc/html examples/*.c


%changelog
* Thu Sep 21 2017 Victor Toso <victortoso@redhat.com> - 1.0.21-1
- Upgrade to 1.0.21
- Resolves: rhbz#1399752

* Wed Jun  8 2016 Hans de Goede <hdegoede@redhat.com> - 1.0.20-1
- Upgrade to 1.0.20
- Resolves: rhbz#1033092
- Resolves: rhbz#1115797

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.15-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.15-3
- Mass rebuild 2013-12-27

* Fri Apr 19 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.15-2
- Replace tarbal with upstream re-spun tarbal which fixes line-ending and
  permission issues

* Wed Apr 17 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.15-1
- Upgrade to 1.0.15 (rhbz#952575)

* Tue Apr  2 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.14-3
- Drop devel-doc Requires from the devel package (rhbz#947297)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.14-1
- Upgrade to 1.0.14

* Mon Sep 24 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.13-1
- Upgrade to 1.0.13

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.11-2
- Fix URL to actually point to libusbx
- Improve description to explain the relation between libusbx and libusb
- Build the examples (to test linking, they are not packaged)

* Tue May 22 2012 Hans de Goede <hdegoede@redhat.com> - 1.0.11-1
- New libusbx package, replacing libusb1
- Switching to libusbx upstream as that actually does releases (hurray)
- Drop all patches (all upstream)
- Drop -static subpackage (there are no packages using it)
