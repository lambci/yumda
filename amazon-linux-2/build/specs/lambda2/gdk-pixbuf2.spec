%global glib2_version 2.48.0

Name:           gdk-pixbuf2
Version:        2.36.12
Release:        3%{?dist}
Summary:        An image loading library

License:        LGPLv2+
URL:            http://www.gtk.org
#VCS:           git:git://git.gnome.org/gdk-pixbuf
Source0:        http://download.gnome.org/sources/gdk-pixbuf/2.36/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  jasper-devel
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info

# needed for man page generation
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt

Requires: glib2%{?_isa} >= %{glib2_version}

# We also need MIME information at runtime
# Requires: shared-mime-info

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2 <= 2.21.2

Prefix: %{_prefix}

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%prep
%autosetup -n gdk-pixbuf-%{version} -p1

%build
%configure                         \
      --without-x11                \
      --with-libjasper             \
      --with-included-loaders=png  \
      --disable-installed-tests    \
      --disable-man                \
      --disable-silent-rules       \
      --disable-introspection      \
      --disable-static
      
# needed to work around bug in makefile goo
rm -f docs/reference/gdk-pixbuf/*.1
      
make %{?_smp_mflags}


%install
%make_install RUN_QUERY_LOADER_TEST=false

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)


%files
%license COPYING
%{_libdir}/libgdk_pixbuf-2.0.so.*
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_bindir}/gdk-pixbuf-thumbnailer
%{_datadir}/thumbnailers/

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.la
%exclude %{_datadir}/locale
%exclude %{_bindir}/gdk-pixbuf-csource
%exclude %{_bindir}/gdk-pixbuf-pixdata
%exclude %{_datadir}/gir-1.0
%exclude %{_datadir}/gtk-doc


%changelog
* Thu Apr 23 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Jul 26 2018 Ray Strode <rstrode@redhat.com> - 2.36.12-3
- One more crack at generating man pages
  Related: #1569815

* Thu Jul 26 2018 Ray Strode <rstrode@redhat.com> - 2.36.12-2
- Generate man page
  Related: #1569815

* Sun Apr 08 2018 Kalev Lember <klember@redhat.com> - 2.36.12-1
- Update to 2.36.12
- Resolves: #1569815

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 2.36.5-1
- Update to 2.36.5
- Resolves: #1386861

* Mon Jan 16 2017 Kalev Lember <klember@redhat.com> - 2.36.4-1
- Update to 2.36.4
- Resolves: #1386861

* Tue Sep 22 2015 Benjamin Otte <otte@gnome.org> - 2.31.6-3
- Fix testsuite more
- Resolves: #1264466

* Mon Sep 21 2015 Matthias Clasen <mclasen@redhat.com> - 2.31.6-2
- Fix testsuite
- Resolves: #1264466

* Wed Aug 19 2015 Benjamin Otte <otte@redhat.com> - 2.31.6-1
- Update to 2.31.6
- Resolves: #1253214

* Mon Apr 27 2015 Matthias Clasen <mclasen@redhat.com> - 2.31.1-1
- Update to 2.31.1
- Add a -tests subpackage
- Drop an upstreamed patch
- Resolves: #1174438

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.28.2-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.28.2-3
- Mass rebuild 2013-12-27

* Mon Nov 18 2013 Matthias Clasen <mclasen@redhat.com> - 2.28.2-2
- Fix interaction between --update-cache and other args
- Resolves: #1029796

* Fri Jun  7 2013 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 2.28.0-1
- Update to 2.28.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.27.3-1
- Update to 2.27.3

* Mon Mar 04 2013 Richard Hughes <rhughes@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.27.1-1
- Update to 2.27.1

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.27.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Tue Jan 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.26.5-3
- Require glib2 >= 2.34.0 for g_type_ensure().

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.26.5-2
- rebuild against new libjpeg

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.5-1
- Update to 2.26.5

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.4-1
- Update to 2.26.4

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 2.26.2-1
- Update to 2.26.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 2.26.1-1
- Update to 2.26.1

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.0-1
- Update to 2.26.0

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.25.0-1
- Update to 2.25.0

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Rebuild against new libpng

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Jun 27 2011 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5 (fixes CVE-2011-2485)

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Mar 30 2011 Matthias Clasen <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Sat Mar  5 2011 Matthias Clasen <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 2.23.0-1
- Update to 2.23.0

* Fri Nov  5 2010 Matthias Clasen <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Wed Sep 29 2010 jkeating - 2.22.0-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Mon Jul 19 2010 Bastien Nocera <bnocera@redhat.com> 2.21.6-3
- Require libpng for linking

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.21.6-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-4
- Also Require shared-mime-info for same reason

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-3
- BR shared-mime-info; see comment above it

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.21.5-2
- Changes to support snapshot builds

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-2
- Rename to gdk-pixbuf2 to avoid conflict with the
  existing gdk-pixbuf package

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-1
- Update to 2.21.4
- Incorporate package review feedback

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.3-1
- Initial packaging
