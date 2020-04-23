%global glib2_version 2.56.1

Name:           gobject-introspection
Version:        1.56.1
Release:        1%{?dist}
Summary:        Introspection system for GObject-based libraries

License:        GPLv2+, LGPLv2+, MIT
URL:            https://wiki.gnome.org/Projects/GObjectIntrospection
Source0:        https://download.gnome.org/sources/gobject-introspection/1.56/%{name}-%{version}.tar.xz

BuildRequires:  bison
BuildRequires:  cairo-gobject-devel
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gettext
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk-doc
BuildRequires:  libffi-devel
BuildRequires:  libX11-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXft-devel
BuildRequires:  libxml2-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  python-devel
BuildRequires:  python-mako

Requires:       glib2%{?_isa} >= %{glib2_version}

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package devel
Summary:        Libraries and headers for gobject-introspection
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Not always, but whatever, it's a tiny dep to pull in
Requires:       libtool
# For g-ir-doctool
Requires:       python-mako

%description devel
Libraries and headers for gobject-introspection

%prep
%autosetup -p1

%build
%configure --enable-gtk-doc --enable-doctool
%make_build

%install
%make_install

# Remove lib64 rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-compiler
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-generate
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-inspect

# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -print -delete
find $RPM_BUILD_ROOT -type f -name "*.a" -print -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING

%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/lib*.so
%{_libdir}/gobject-introspection/
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/gobject-introspection-1.0/
%{_datadir}/aclocal/introspection.m4
%{_mandir}/man1/*.gz
%{_datadir}/gtk-doc/html/gi/

%changelog
* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 1.56.1-1
- Update to 1.56.1
- Resolves: #1569272

* Wed Sep 28 2016 Kalev Lember <klember@redhat.com> - 1.50.0-1
- Update to 1.50.0
- Resolves: #1386972

* Tue Apr 28 2015 Matthias Clasen <mclasen@redhat.com> - 1.42.0-1
- Update to 1.42.0
- Resolves: #1174439

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.36.0-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.36.0-3
- Mass rebuild 2013-12-27

* Thu Oct 31 2013 Colin Walters <walters@redhat.com> - 1.36.0-2
- Backport patch for anonymous unions
  Resolves: #1024947

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 1.36.0-1
- Update to 1.36.0

* Thu Mar 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.35.9-1
- Update to 1.35.9

* Tue Mar 05 2013 Colin Walters <walters@verbum.org> - 1.35.8-2
- Enable g-ir-doctool
- Resolves: #903782

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 1.35.8-1
- Update to 1.35.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 1.35.4-1
- Update to 1.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.35.3-1
- Update to 1.35.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 1.35.2-1
- Update to 1.35.2

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 1.34.2-1
- Update to 1.34.2

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 1.34.1.1-1
- Update to 1.34.1.1

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 1.34.1-1
- Update to 1.34.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.34.0-1
- Update to 1.34.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 1.33.14-1
- Update to 1.33.14

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 1.33.10-1
- Update to 1.33.10

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.33.9-1
- Update to 1.33.9

* Fri Jul 20 2012 Matthias Clasen <mclasen@redhat.com> - 1.33.4-2
- Fix an unintended api break that broke vpn in gnome-shell

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 1.33.4-1
- Update to 1.33.4

* Wed Jun 27 2012 Richard Hughes <hughsient@gmail.com> - 1.33.3-1
- Update to 1.33.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 1.33.2-1
- Update to 1.33.2

* Fri Apr 27 2012 Kalev Lember <kalevlember@gmail.com> - 1.32.1-2
- Move libffi to pkgconfig Requires.private, in order to
  reduce the impact when libffi soname bump lands in rawhide.

* Fri Apr 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.32.1-1
- Update to 1.32.1

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> 0 1.32.0-1
- Update to 1.32.0

* Wed Mar 21 2012 Matthias Clasen <mclasen@redhat.com> 0 1.31.22-1
- Update to 1.31.22

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> 0 1.31.20-1
- Update to 1.31.20

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> 0 1.31.10-1
- Update to 1.31.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redha.com> - 1.31.6-1
- Update to 1.31.6

* Mon Dec 05 2011 Karsten Hopp <karsten@redhat.com> 1.31.0-2
- add fix for PPC failure, bugzilla 749604

* Wed Nov 16 2011 Colin Walters <walters@verbum.org> - 1.31.0-2
- -devel package requires libtool
  https://bugzilla.redhat.com/show_bug.cgi?id=613466

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 1.31.0-1
- Update to 1.31.0

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 1.30.0-1
- Update to 1.30.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 1.30.0-1
- Update to 1.30.0

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.29.0-1
- Update to 1.29.0

* Thu Apr 21 2011 John (J5) Palmieri <johnp@redhat.com> - 0.10.8-1
- Update to 0.10.8

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 0.10.7-1
- Update to 0.10.7

* Fri Mar 25 2011 Owen Taylor <otaylor@redhat.com> - 0.10.6-1
- New upstream release to fix missing cairo typelib

* Fri Mar 25 2011 Colin Walters <walters@verbum.org> - 0.10.5-1
- New upstream release, fixes cairo.gir
  Necessary to avoid gnome-shell having a cairo-devel dependency.
- Also add cairo-gobject-devel dependency, since we really want
  the cairo typelib to link to GObject, since anyone using
  introspection has it anyways.

* Thu Mar 10 2011 Colin Walters <walters@verbum.org> - 0.10.4-1
- Update to 0.10.4

* Wed Feb 23 2011 Colin Walters <walters@verbum.org> - 0.10.3-1
- Update to 0.10.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Colin Walters <walters@verbum.org> - 0.10.2-1
- Update to 0.10.2

* Wed Jan 12 2011 Colin Walters <walters@verbum.org> - 0.10.1-1
- Update to 0.10.1

* Mon Jan 10 2011 Owen Taylor <otaylor@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Thu Sep 30 2010 Colin Walters <walters@verbum.org> - 0.9.10-1
- Update to 0.9.10

* Thu Sep 30 2010 Colin Walters <walters@verbum.org> - 0.9.9-1
- Update to 0.9.9

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.9.8-1
- Update to 0.9.8

* Tue Sep 28 2010 Colin Walters <walters@verbum.org> - 0.9.7-1
- Update to 0.9.7

* Tue Sep 21 2010 Owen Taylor <otaylor@redhat.com> - 0.9.6-1
- Update to 0.9.6

* Thu Sep  2 2010 Colin Walters <walters@verbum.org> - 0.9.3-6
- Strip out test libraries; they're gone in upstream git, and
  create a dependency on cairo (which requires libX11, which makes
  server operating system builders freak out).

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.9.3-1
- Update to 0.9.3

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.2-5
- Cherrypick patch for python 2.7 compatibility (patch 1; rhbz#617782)

* Wed Jul 14 2010 Colin Walters <walters@verbum.org> - 0.9.2-4
- Backport patch from upstream for better errors

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.9.2-1
- New upstream (unstable series) release; requires rebuilds

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 0.9.0-1.4.20100629gitf0599b0a
- Add gtk-doc to files

* Tue Jun 29 2010 Colin Walters <walters@verbum.org>
- Switch to git snapshot; I forgot to enable gtk-doc in the last
  tarball.

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 0.9.0-1
- New upstream development release
- Update to support building git snapshot directly

* Thu Jun 24 2010 Colin Walters <walters@pocket> - 0.6.14-3
- rebuild to pick up new glib changes

* Thu Jun 10 2010 Colin Walters <walters@pocket> - 0.6.14-2
- Obsolete gir-repository{,-devel}

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.14-1
- Update to 0.6.14

* Mon May 24 2010 Colin Walters <walters@verbum.org> - 0.6.12-1
- Update to latest upstream release 0.6.12

* Thu Mar 25 2010 Colin Walters <walters@verbum.org> - 0.6.9-3
- Move python library back into /usr/lib/gobject-introspection.  I put
  it there upstream for a reason, namely that apps need to avoid
  polluting the global Python site-packages with bits of their internals.
  It's not a public API.
  
  Possibly resolves bug #569885

* Wed Mar 24 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.9-2
- Added newly owned files (gobject-introspection-1.0 directory)

* Wed Mar 24 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.9-1
- Update to latest upstream release 0.6.9

* Thu Mar 11 2010 Colin Walters <walters@verbum.org> - 0.6.8-0.3.20100311git2cc97351
- rebuilt

* Thu Mar 11 2010 Colin Walters <walters@verbum.org>
- New upstream snapshot
- rm unneeded rm

* Thu Jan 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.8-0.1.20100128git
- Update to new git snapshot
- Fix Version tag to comply with correct naming use with alphatag

* Fri Jan 15 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.7.20100115git-1
- Update to git snapshot for rawhide 

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.7-1
- Update to 0.6.7

* Fri Sep 11 2009 Colin Walters <walters@verbum.org> - 0.6.5-1
- New upstream
- Drop libtool dep 

* Fri Aug 28 2009 Colin Walters <walters@verbum.org> - 0.6.4-2
- Add dep on libtool temporarily

* Wed Aug 26 2009 Colin Walters <walters@verbum.org> - 0.6.4-1
- New upstream 0.6.4
- Drop upstreamed build fix patch 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-4
- Add upstream patch to fix a build crash

* Thu Jul  2 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-3
- Add -ggdb temporarily so it compiles on ppc64

* Thu Jul  2 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-2
- Add the new source file

* Thu Jul  2 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-1
- Update to 0.6.3

* Mon Jun  1 2009 Dan Williams <dcbw@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Colin Walters <walters@verbum.org> - 0.6.1-1
- Update to 0.6.1

* Fri Oct 31 2008 Colin Walters <walters@verbum.org> - 0.6.0-1
- Create spec goo
