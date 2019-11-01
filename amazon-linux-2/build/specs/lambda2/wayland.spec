Name:           wayland
Version:        1.14.0
Release: 2%{?dist}.0.1
Summary:        Wayland Compositor Infrastructure

License:        MIT
URL:            http://wayland.freedesktop.org/
Source0:        http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz

Patch1: 0001-cursor-Fix-heap-overflows-when-parsing-malicious-fil.patch

BuildRequires:  chrpath
BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  graphviz
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  pkgconfig(libffi)
BuildRequires:  xmlto

Prefix: %{_prefix}

%description
Wayland is a protocol for a compositor to talk to its clients as well as a C
library implementation of that protocol. The compositor can be a standalone
display server running on Linux kernel modesetting and evdev input devices,
an X application, or a wayland client itself. The clients can be traditional
applications, X servers (rootless or fullscreen) or other display servers.

%package -n libwayland-client
Summary: Wayland client library
Prefix: %{_prefix}
%description -n libwayland-client
Wayland client library

%package -n libwayland-cursor
Summary: Wayland cursor library
Requires: libwayland-client%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}
%description -n libwayland-cursor
Wayland cursor library

%package -n libwayland-server
Summary: Wayland server library
Prefix: %{_prefix}
%description -n libwayland-server
Wayland server library


%prep
%setup -q
%patch1 -p1 -b .xcursor

%build
%configure --disable-static --disable-documentation
make %{?_smp_mflags}


%install
%make_install

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

# Remove lib64 rpaths
chrpath -d $RPM_BUILD_ROOT%{_libdir}/libwayland-cursor.so

%files -n libwayland-client
%license COPYING
%{_libdir}/libwayland-client.so.0*

%files -n libwayland-cursor
%license COPYING
%{_libdir}/libwayland-cursor.so.0*

%files -n libwayland-server
%license COPYING
%{_libdir}/libwayland-server.so.0*

%exclude %{_bindir}/wayland-scanner
%exclude %{_includedir}
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/*.so
%exclude %{_datadir}
%exclude %{_mandir}

%changelog
* Fri Nov 1 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Nov 29 2017 Olivier Fourdan <ofourdan@redhat.com> - 1.14.0-2
- Add libwayland-cursor heap overflow fix (#1518615)

* Fri Sep 22 2017 Olivier Fourdan <ofourdan@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Thu Jun 1 2017 Owen Taylor <otaylor@redhat.com> - 1.13.0-2
- Add a patch fixing a build error with newer versions of graphviz

* Wed Feb 22 2017 Kalev Lember <klember@redhat.com> - 1.13.0-1
- Update to 1.13.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Kalev Lember <klember@redhat.com> - 1.12.91-1
- Update to 1.12.91

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 1.11.94-1
- Update to 1.11.94

* Thu Sep 08 2016 Kalev Lember <klember@redhat.com> - 1.11.93-1
- Update to 1.11.93

* Wed Aug 31 2016 Kalev Lember <klember@redhat.com> - 1.11.92-1
- Update to 1.11.92

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 1.11.91-1
- Update to 1.11.91
- Simplify -devel subpackage packaging
- Include license files in packaging

* Wed Jun 01 2016 Kalev Lember <klember@redhat.com> - 1.11.0-1
- Update to 1.11.0

* Wed May 25 2016 Kalev Lember <klember@redhat.com> - 1.10.93-1
- Update to 1.10.93

* Wed May 18 2016 Kalev Lember <klember@redhat.com> - 1.10.92-1
- Update to 1.10.92

* Sun May 08 2016 Kalev Lember <klember@redhat.com> - 1.10.91-1
- Update to 1.10.91

* Thu Feb 18 2016 Kalev Lember <klember@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Thu Feb 04 2016 Kalev Lember <klember@redhat.com> - 1.9.92-1
- Update to 1.9.92

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 1.9.91-1
- Update to 1.9.91

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.9.0-1
- Update to 1.9.0
- Use make_install macro

* Wed Sep 16 2015 Kalev Lember <klember@redhat.com> - 1.8.93-1
- Update to 1.8.93

* Wed Sep 02 2015 Kalev Lember <klember@redhat.com> - 1.8.92-1
- Update to 1.8.92

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.8.91-2
- Split out wayland-doc subpackage for documentation

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.8.91-1
- Update to 1.8.91

* Mon Jul 20 2015 Adam Jackson <ajax@redhat.com> 1.8.0-1
- wayland 1.8.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Adam Jackson <ajax@redhat.com> 1.7.92-1
- wayland 1.7.92

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.7.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 1.7.0-1
- Wayland 1.7.0

* Fri Sep 19 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.0-1
- Update to 1.6.0
- Remove lib64 rpaths

* Fri Aug 22 2014 Kevin Fenzi <kevin@scrye.com> 1.5.91-1
- Update to 1.5.90

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Adam Jackson <ajax@redhat.com> 1.5.0-4
- Update protocol: new surface error enums

* Mon Jun 30 2014 Adam Jackson <ajax@redhat.com> 1.5.0-3
- Remove blocking flush patch as it actually introduces deadlocks now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Richard Hughes <rhughes@redhat.com> - 1.5.0-1
- Wayland 1.5.0

* Tue May 13 2014 Richard Hughes <rhughes@redhat.com> - 1.4.93-1
- Wayland 1.4.93

* Fri Jan 24 2014 Richard Hughes <rhughes@redhat.com> - 1.4.0-1
- Wayland 1.4.0

* Mon Jan 20 2014 Richard Hughes <rhughes@redhat.com> - 1.3.93-1
- Wayland 1.3.93

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.3.91-2
- Call ldconfig in libwayland-cursor %%post* scripts.
- Run test suite during build.
- Compress snapshot tarballs with xz.

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 1.3.91-1
- Wayland 1.3.91

* Mon Nov 25 2013 Lubomir Rintel <lkundrak@v3.sk> - 1.3.0-1
- Wayland 1.3.0

* Mon Oct 07 2013 Adam Jackson <ajax@redhat.com> 1.2.0-3
- Don't use MSG_DONTWAIT in wl_connection_flush.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Richard Hughes <rhughes@redhat.com> - 1.2.0-1
- wayland 1.2.0

* Wed May 15 2013 Richard Hughes <rhughes@redhat.com> - 1.1.90-0.1.20130515
- Update to a git snapshot based on what will become 1.1.90

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 1.1.0-1
- wayland 1.1.0

* Wed Mar 27 2013 Richard Hughes <rhughes@redhat.com> - 1.0.6-1
- wayland 1.0.6

* Thu Feb 21 2013 Adam Jackson <ajax@redhat.com> 1.0.5-1
- wayland 1.0.5

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Adam Jackson <ajax@redhat.com> 1.0.3-1
- wayland 1.0.3

* Tue Oct 23 2012 Adam Jackson <ajax@redhat.com> 1.0.0-1
- wayland 1.0

* Thu Oct 18 2012 Adam Jackson <ajax@redhat.com> 0.99.0-1
- wayland 0.99.0

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 0.95.0-1
- wayland 0.95.0 (#843738)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89.0-2.20120424
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> - 0.89.0-1
- Update to a git snapshot based on 0.89.0

* Sat Feb 18 2012 Thorsten Leemhuis <fedora@leemhuis.info> - 0.85.0-1
- update to 0.85.0
- adjust license, as upstream changed it to MIT
- update make-git-snapshot.sh to current locations and scheme
- drop common package, not needed anymore
- compositor is now in a separate package, hence reduce BuildRequires to what
  is actually needed (a lot less) and adjust summary
- make usage of a git checkout in spec file optional
- a %%{?_isa} to requires where it makes sense

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.6.20101221
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1-0.5.20101221
- Rebuild for new libpng

* Wed Jun 15 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.1-0.4.20101221
- Install real compositor binary instead of a libtool wrapper

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.3.20101221
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Adam Jackson <ajax@redhat.com> 0.1-0.2.20101221
- Today's git snap

* Tue Nov 23 2010 Adam Jackson <ajax@redhat.com> 0.1-0.2.20101123
- Today's git snap
- Fix udev rule install (#653353)

* Mon Nov 15 2010 Adam Jackson <ajax@redhat.com> 0.1-0.1.20101111
- Initial packaging
