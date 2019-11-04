Name: libnl3
Version: 3.2.28
Release: 4%{?dist}.0.1
Summary: Convenience library for kernel netlink sockets
Group: Development/Libraries
License: LGPLv2
URL: http://www.infradead.org/~tgr/libnl/

%define fullversion %{version}

Source: http://www.infradead.org/~tgr/libnl/files/libnl-%{fullversion}.tar.gz
Source1: http://www.infradead.org/~tgr/libnl/files/libnl-doc-%{fullversion}.tar.gz

Patch1: 0001-compare-v4-addr-rh1370503.patch
Patch2: 0002-msg-peek-by-default-rh1396882.patch
Patch3: 0003-nl-reserve-integer-overflow-rh1442723.patch

BuildRequires: flex bison
BuildRequires: python
BuildRequires: libtool autoconf automake

Prefix: %{_prefix}

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%package cli
Summary: Command line interface utils for libnl3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description cli
This package contains various libnl3 utils and additional
libraries on which they depend

%prep
%setup -q -n libnl-%{fullversion}
%patch1 -p1
%patch2 -p1
%patch3 -p1

tar -xzf %SOURCE1

%build
autoreconf -vif
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name \*.la -delete

%files
%license COPYING
%exclude %{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl-*.so.*
%config(noreplace) %{_sysconfdir}/*

%files cli
%license COPYING
%{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl/
%{_bindir}/*

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Apr 18 2017 Thomas Haller <thaller@redhat.com> - 3.2.28-4
* lib: check for integer overflow in nl_reserve() (rh#1440788, rh#1442723)

* Mon Jan  9 2017 Thomas Haller <thaller@redhat.com> - 3.2.28-3
- lib: use MSG_PEEK by default for nl_msgrecvs() (rh#1396882)

* Fri Aug 26 2016 Thomas Haller <thaller@redhat.com> - 3.2.28-2
- route: fix nl_object_identical() comparing AF_INET addresses (rh #1370503)

* Sat Jul  9 2016 Thomas Haller <thaller@redhat.com> - 3.2.28-1
- update to latest upstream release 3.2.28 (rh #1296058)

* Thu Jun 30 2016 Thomas Haller <thaller@redhat.com> - 3.2.28-0.1
- update to latest upstream release 3.2.28-rc1 (rh #1296058)

* Fri Jan  8 2016 Thomas Haller <thaller@redhat.com> - 3.2.27-1
- rebase package to upstream version 3.2.27 (rh #1296058)

* Wed Sep 30 2015 Thomas Haller <thaller@redhat.com> - 3.2.21-10
- rtnl: fix lookup in rtnl_neigh_get() to ignore address family (rh #1261028)

* Mon Aug 24 2015 Thomas Haller <thaller@redhat.com> - 3.2.21-9
- improve local port handling for netlink socket with EADDRINUSE (rh #1249158)
- rtnl: backport support for link-netnsid attribute (rh #1255050)

* Mon Jan 12 2015 Lubomir Rintel <lrintel@redhat.com> - 3.2.21-8
- properly propagate EAGAIN error status (rh #1181255)

* Wed Aug 20 2014 Thomas Haller <thaller@redhat.com> - 3.2.21-7
- backport support for IPv6 link local address generation mode (rh #1127718)

* Fri Mar 21 2014 Thomas Haller <thaller@redhat.com> - 3.2.21-6
- fix rtnl_link_get_stat() for IPSTATS_MIB_* after kernel API breakage
- fix parsing IFLA_PROTINFO which broke on older kernels (rh #1062533)
- fix printing in nl_msec2str for whole seconds
- don't reset route scope in rtnl_route_build_msg if set to RT_SCOPE_NOWHERE
- backport nl_has_capability function

* Wed Feb 26 2014 Thomas Graf <tgraf@redhat.com> - 3.2.21-5
- nl-Increase-receive-buffer-size-to-4-pages.patch (rh #1040626)

* Tue Jan 28 2014 Daniel Mach <dmach@redhat.com> - 3.2.21-4
- Mass rebuild 2014-01-24

* Fri Jan 24 2014 Thomas Haller <thaller@redhat.com> - 3.2.21-3
- Backport extended IPv6 address flags (rh #1057024)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.2.21-2
- Mass rebuild 2013-12-27

* Fri Jan 25 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.21-1
- Update to 3.2.21

* Wed Jan 23 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.20-1
- Update to 3.2.20

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-2
- Age fix

* Thu Jan 17 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-1
- Update to 3.2.19

* Tue Oct 30 2012 Dan Williams <dcbw@redhat.com> - 3.2.14-1
- Update to 3.2.14

* Mon Sep 17 2012 Dan Williams <dcbw@redhat.com> - 3.2.13-1
- Update to 3.2.13

* Fri Feb 10 2012 Dan Williams <dcbw@redhat.com> - 3.2.7-1
- Update to 3.2.7

* Tue Jan 17 2012 Jiri Pirko <jpirko@redhat.com> - 3.2.6-1
- Initial build
