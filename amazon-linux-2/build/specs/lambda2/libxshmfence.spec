Name:           libxshmfence
Version:        1.2
Release: 1%{?dist}.0.2
Summary:        X11 shared memory fences

License:        MIT
URL:            http://www.x.org/
Source0:        http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

# upstream tarball has broken libtool because libtool is never not broken
BuildRequires:  autoconf automake libtool xorg-x11-util-macros
BuildRequires:  pkgconfig(xproto)

Prefix: %{_prefix}

%description
Shared memory fences for X11, as used in DRI3.

%prep
%setup -q

%build
autoreconf -v -i -f
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

%files
%license COPYING
%{_libdir}/libxshmfence.so.1*

%exclude %{_includedir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 02 2015 Adel Gadllah <adel.gadllah@gmail.com> - 1.2-1
- Update to 1.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Adam Jackson <ajax@redhat.com> 1.1-1
- xshmfence 1.1

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> 1.0-1
- Initial packaging

