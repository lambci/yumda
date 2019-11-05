%global         majorminor      1.0

%global         _glib2                  2.32.0
%global         _libxml2                2.4.0
%global         _gobject_introspection  1.31.1

Name:           gstreamer1
Version:        1.10.4
Release: 2%{?dist}.0.2
Summary:        GStreamer streaming media framework runtime

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
## For GStreamer RPM provides
Patch0:         gstreamer-inspect-rpm-format.patch
Source1:        gstreamer1.prov
Source2:        gstreamer1.attr

BuildRequires:  glib2-devel >= %{_glib2}
BuildRequires:  libxml2-devel >= %{_libxml2}
BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  m4
BuildRequires:  check-devel
BuildRequires:  gtk-doc >= 1.3
BuildRequires:  gettext
BuildRequires:  pkgconfig

BuildRequires:  chrpath

### documentation requirements
BuildRequires:  python2
BuildRequires:  openjade
BuildRequires:  jadetex
BuildRequires:  libxslt
BuildRequires:  docbook-style-dsssl
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:  transfig
BuildRequires:  netpbm-progs
BuildRequires:  tetex-dvips
BuildRequires:  ghostscript
%if !0%{?rhel}
BuildRequires:  xfig
%endif

Prefix: %{_prefix}

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.


%prep
%setup -q -n gstreamer-%{version}
%patch0 -p1 -b .rpm-provides


%build
%configure \
  --with-package-name='GStreamer package' \
  --with-package-origin='http://www.redhat.com' \
  --enable-gtk-doc \
  --enable-debug \
  --disable-tests --disable-examples
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstbase-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcheck-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstcontroller-1.0.so.* 
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstnet-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/gstreamer-%{majorminor}/gst-plugin-scanner
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/gstreamer-%{majorminor}/gst-ptp-helper
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-inspect-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-launch-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-stats-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-typefind-1.0
chrpath --delete $RPM_BUILD_ROOT%{_datadir}/bash-completion/helpers/gst-completion-helper-%{majorminor}

# Clean out files that should not be part of the rpm.
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'


%files
%license COPYING
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcheck-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*

%{_libexecdir}/gstreamer-%{majorminor}/

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoretracers.so

%{_libdir}/girepository-1.0/Gst-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstBase-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstController-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstNet-%{majorminor}.typelib

%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-stats-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}

%exclude %{_localedir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}


%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Mar 09 2017 Wim Taymans <wtaymans@redhat.com> - 1.10.4-2
- fix origin
- Resolves: #1420650

* Fri Feb 24 2017 Wim Taymans <wtaymans@redhat.com> - 1.10.4-1
- Update to 1.10.4
- update patches
- Resolves: #1420650

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> 1.4.5-1
- Update to 1.4.5
- Add patch to gst-inspect to generate RPM provides
- Resolves: #1174394

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.7-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.7-3
- Mass rebuild 2013-12-27

* Mon Nov 18 2013 Adam Jackson <ajax@redhat.com> 1.0.7-2
- Fix plugin scanner to not fork continuously (#1030853)

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com>
- Tweak BRs for RHEL

* Fri Mar 22 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Remove BR on PyXML.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2.

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Sat Sep  8 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-2
- Add patch to gst-inspect to generate RPM provides
- Add RPM find-provides script

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Bump minimum version of glib2 needed.

* Fri Aug  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-2
- Use %%global instead of %%define.
- Remove rpath.

* Tue Jul 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.

