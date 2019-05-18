# first two digits of version
%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

%ifarch %{ix86} x86_64 ppc ppc64 ppc64le s390x armv7hl aarch64
%global has_valgrind 1
%endif

Name:           libsecret
Version:        0.18.5
Release: 2%{?dist}.0.2
Summary:        Library for storing and retrieving passwords and other secrets

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Libsecret
Source0:        http://download.gnome.org/sources/libsecret/%{release_version}/libsecret-%{version}.tar.xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1434474
Patch0:         libsecret-0.18.5-fix-invalid-secret-transfer-error.patch

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  intltool
BuildRequires:  libgcrypt-devel >= 1.2.2
BuildRequires:  vala-devel >= 0.17.2.12
BuildRequires:  vala
BuildRequires:  gtk-doc
BuildRequires:  libxslt-devel
BuildRequires:  docbook-style-xsl
%if 0%{?has_valgrind}
BuildRequires:  valgrind-devel
%endif

Provides:       bundled(egglib)

%description
libsecret is a library for storing and retrieving passwords and other secrets.
It communicates with the "Secret Service" using DBus. gnome-keyring and
KSecretService are both implementations of a Secret Service.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

# Use system valgrind headers instead
%if 0%{?has_valgrind}
rm -rf build/valgrind/
%endif


%build
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang libsecret


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libsecret.lang
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/secret-tool
%{_libdir}/libsecret-1.so.*
%{_libdir}/girepository-1.0/Secret-1.typelib
%doc %{_mandir}/man1/secret-tool.1.gz

%files devel
%{_includedir}/libsecret-1/
%{_libdir}/libsecret-1.so
%{_libdir}/pkgconfig/libsecret-1.pc
%{_libdir}/pkgconfig/libsecret-unstable.pc
%{_datadir}/gir-1.0/Secret-1.gir
%{_datadir}/vala/vapi/libsecret-1.deps
%{_datadir}/vala/vapi/libsecret-1.vapi
%doc %{_datadir}/gtk-doc/


%changelog
* Tue Mar 21 2017 David King <dking@redhat.com> - 0.18.5-2
- Fix invalid secret transfer error (#1434474)

* Fri Mar 25 2016 Kalev Lember <klember@redhat.com> - 0.18.5-1
- Update to 0.18.5
- Resolves: #1387018

* Mon May 18 2015 David King <dking@redhat.com> - 0.18.2-2
- Update valgrind.h and memcheck.h (#1142140)

* Thu Apr 30 2015 Richard Hughes <rhughes@redhat.com> - 0.18.2-1
- Update to 0.18.2
- Resolves: #1174539

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.15-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.15-2
- Mass rebuild 2013-12-27

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.15-1
- Update to 0.15

* Wed Mar 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.14-1
- Update to 0.14

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.13-1
- Update to 0.13

* Fri Nov 23 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.12-1
- Update to 0.12

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.11-1
- Update to 0.11

* Wed Sep 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.10-1
- Update to 0.10
- Enable vala

* Mon Aug 06 2012 Stef Walter <stefw@redhat.com> - 0.8-1
- Update to 0.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.7-1
- Update to 0.7

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.6-1
- Update to 0.6

* Thu Jun 28 2012 Kalev Lember <kalevlember@gmail.com> - 0.3-1
- Update to 0.3

* Mon Apr 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.2-1
- Update to 0.2
- Enable parallel make

* Fri Mar 30 2012 Kalev Lember <kalevlember@gmail.com> - 0.1-2
- Add provides bundled(egglib) (#808025)
- Use global instead of define

* Thu Mar 29 2012 Kalev Lember <kalevlember@gmail.com> - 0.1-1
- Initial RPM release
