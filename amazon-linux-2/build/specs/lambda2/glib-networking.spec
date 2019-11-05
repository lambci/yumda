%define glib2_version 2.46.0

Name:           glib-networking
Version:        2.50.0
Release: 1%{?dist}.0.2
Summary:        Networking support for GLib

License:        LGPLv2+
URL:            http://www.gnome.org
Source0:        http://download.gnome.org/sources/glib-networking/2.50/%{name}-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libproxy-devel
BuildRequires:  gnutls-devel
BuildRequires:  intltool
BuildRequires:  ca-certificates
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  systemd

Requires:       ca-certificates
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gsettings-desktop-schemas

Prefix: %{_prefix}

%description
This package contains modules that extend the networking support in
GIO. In particular, it contains libproxy- and GSettings-based
GProxyResolver implementations and a gnutls-based GTlsConnection
implementation.

%prep
%autosetup -p1

%build
%configure --disable-static --with-libproxy --disable-installed-tests

make %{?_smp_mflags} V=1

%install
%make_install

%if "%{_prefix}" != "/usr"
  if [ -d $RPM_BUILD_ROOT/usr/lib64 ]; then mv $RPM_BUILD_ROOT/usr/lib64/* $RPM_BUILD_ROOT%{_libdir}/; fi
  if [ -d $RPM_BUILD_ROOT/usr ]; then mv $RPM_BUILD_ROOT/usr/* $RPM_BUILD_ROOT%{_prefix}/; fi
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

%files
%license COPYING
%{_libdir}/gio/modules/libgiolibproxy.so
%{_libdir}/gio/modules/libgiognomeproxy.so
%{_libdir}/gio/modules/libgiognutls.so
%{_libexecdir}/glib-pacrunner

%exclude %{_datadir}
%exclude %{_libdir}/systemd

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0
- Resolves: #1386876
- Resolves: #1367484

* Mon Apr 27 2015 Dan Winship <danw@redhat.com> - 2.42.0-1
- Update to 2.42.0
- Resolves: #1174447

* Wed Jul 23 2014 Dan Winship <danw@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.36.2-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.36.2-2
- Mass rebuild 2013-12-27

* Mon May 13 2013 Matthias Clasen <mclasen@redhat.com> - 2.36.2-1
- Update to 2.36.2

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 2.36.1-1
- Update to 2.36.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.9-1
- Update to 2.35.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.8-1
- Update to 2.35.8

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.6-1
- Update to 2.35.6

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.4-1
- Update to 2.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.3-1
- Update to 2.35.3

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.1-1
- Update to 2.35.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.0-1
- Update to 2.34.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.14-1
- Update to 2.33.14

* Wed Sep  5 2012 Debarshi Ray <rishi@fedoraproject.org> - 2.33.12-1
- Update to 2.33.12

* Mon Sep  3 2012 Matthias Clasen <mclasen@redhat.com> - 2.33.10-1
- Update to 2.33.10

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 2.33.3-1
- Update to 2.33.3

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.2-1
- Update to 2.33.2
- Use --disable-static instead of removing built static libs in %%install

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.1-1
- Update to 2.32.1

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 2.32.0-1
- Update to 2.32.0

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.22-1
- Update to 2.31.22

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 2.31.20-1
- Update to 2.31.20

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 2.31.16-1
- Update to 2.31.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.6
- Update to 2.31.6

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.2
- Update to 2.31.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.0
- Update to 2.31.0

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.1-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> 2.29.92-1
- Update to 2.29.92

* Tue Jul 05 2011 Bastien Nocera <bnocera@redhat.com> 2.29.9-1
- Update to 2.29.9

* Wed Apr 27 2011 Dan Winship <danw@redhat.com> - 2.28.6.1-2
- Require gsettings-desktop-schemas, for GNOME proxy support

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.6.1-1
- Update to 2.28.6.1

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.6-1
- Update to 2.28.6

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.5-1
- Update to 2.28.5

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-1
- Update to 2.28.4

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Dan Winship <danw@redhat.com> - 2.27.90-1
- Update to 2.27.90, including TLS support

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Oct  7 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.0-1
- Initial packaging
