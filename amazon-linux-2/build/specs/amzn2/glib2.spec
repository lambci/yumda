%global _changelog_trimtime %(date +%s -d "1 year ago")

Name: glib2
Version: 2.56.1
Release: 4%{?dist}
Summary: A library of handy utility functions

License: LGPLv2+
URL: http://www.gtk.org
Source0: http://download.gnome.org/sources/glib/2.56/glib-%{version}.tar.xz

BuildRequires: chrpath
BuildRequires: gettext
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: libattr-devel
BuildRequires: libselinux-devel
# for sys/sdt.h
BuildRequires: systemtap-sdt-devel
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(libffi)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(mount)
BuildRequires: pkgconfig(zlib)
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
BuildRequires: gtk-doc
BuildRequires: python-devel

# Patches we're carrying specifically for RHEL7:
# Avoid deprecating things introduced since the first version of glib
# built in RHEL7, as some projects use `-Werror` and such.
Patch0: revert-g-source-remove-critical.patch
Patch1: add-back-g-memmove.patch

# Patches added by Amazon
Patch10001: 0001-codegen-Change-pointer-casting-to-remove-type-punnin.patch
Patch10002: 0002-gdbus-codegen-honor-Property.EmitsChangedSignal-anno.patch
Patch10003: 0003-gfile-Limit-access-to-files-when-copying.patch

# for GIO content-type support
Requires: shared-mime-info

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.


%package devel
Summary: A library of handy utility functions
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for the GLib library.

%package doc
Summary: A library of handy utility functions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The glib2-doc package includes documentation for the GLib library.

%package fam
Summary: FAM monitoring module for GIO
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: gamin-devel

%description fam
The glib2-fam package contains the FAM (File Alteration Monitor) module for GIO.

%package static
Summary: glib static
Requires: %{name}-devel = %{version}-%{release}

%description static
The %{name}-static subpackage contains static libraries for %{name}.

%package tests
Summary: Tests for the glib2 package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The glib2-tests package contains tests that can be used to verify
the functionality of the installed glib2 package.

%prep
%autosetup -n glib-%{version} -p1

# restore timestamps after patching to appease multilib for .pyc files
tar vtf %{SOURCE0} | while read mode user size date time name; do touch -d "$date $time" ../$name; done

autoreconf -i -f

%build
# Bug 1324770: Also explicitly remove PCRE sources since we use --with-pcre=system
rm glib/pcre/*.[ch]
# Support builds of both git snapshots and tarballs packed with autogoo
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
           --disable-silent-rules \
           --with-pcre=system \
           --enable-systemtap \
           --enable-static \
           --enable-installed-tests
)

%make_build

%install
# Use -p to preserve timestamps on .py files to ensure
# they're not recompiled with different timestamps
# to help multilib: https://bugzilla.redhat.com/show_bug.cgi?id=718404
%make_install INSTALL="install -p"
# Also since this is a generated .py file, set it to a known timestamp,
# otherwise it will vary by build time, and thus break multilib -devel
# installs.
touch -r gio/gdbus-2.0/codegen/config.py.in $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/codegen/config.py
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.{pyc,pyo}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.{pyc,pyo}

mv  $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-%{__isa_bits}

touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache

# bash-completion scripts need not be executable
chmod 644 $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/*

%find_lang glib20


%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%postun
/sbin/ldconfig
[ ! -x %{_bindir}/gio-querymodules-%{__isa_bits} ] || \
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%files -f glib20.lang
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gsettings
%{_datadir}/bash-completion/completions/gapplication
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%{_bindir}/gio
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gapplication
%{_mandir}/man1/gio.1*
%{_mandir}/man1/gio-querymodules.1*
%{_mandir}/man1/glib-compile-schemas.1*
%{_mandir}/man1/gsettings.1*
%{_mandir}/man1/gdbus.1*
%{_mandir}/man1/gapplication.1*

%files devel
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/glib-2.0/valgrind/glib.supp
%{_datadir}/bash-completion/completions/gresource
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%{_datadir}/glib-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%{_mandir}/man1/glib-genmarshal.1*
%{_mandir}/man1/glib-gettextize.1*
%{_mandir}/man1/glib-mkenums.1*
%{_mandir}/man1/gobject-query.1*
%{_mandir}/man1/gtester-report.1*
%{_mandir}/man1/gtester.1*
%{_mandir}/man1/gdbus-codegen.1*
%{_mandir}/man1/glib-compile-resources.1*
%{_mandir}/man1/gresource.1*
%{_datadir}/gdb/
%{_datadir}/gettext/
%{_datadir}/systemtap/

%files doc
%doc %{_datadir}/gtk-doc/html/*

%files fam
%{_libdir}/gio/modules/libgiofam.so

%files static
%{_libdir}/libgio-2.0.a
%{_libdir}/libglib-2.0.a
%{_libdir}/libgmodule-2.0.a
%{_libdir}/libgobject-2.0.a
%{_libdir}/libgthread-2.0.a

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
* Fri May 10 2019 Ray Strode <rstrode@redhat.com> - 2.56.1-4
- Backport glib2 change needed for accountsservice dbus
  codegen fix
  Related: #1709190

* Mon Aug 27 2018 Colin Walters <walters@verbum.org> - 2.56.1-2
- Add --disable-silent-rules

* Sun Apr 08 2018 Kalev Lember <klember@redhat.com> - 2.56.1-1
- Update to 2.56.1
- Resolves #1567375

* Fri Nov 10 2017 Kalev Lember <klember@redhat.com> - 2.54.2-2
- Backport patch to fix race condition in GDBusObjectManagerClient
- Resolves: #1494065

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 2.54.2-1
- Update to 2.54.2
- Related: #1481386

* Tue Oct 31 2017 Colin Walters <walters@verbum.org> - 2.54.1-3
- Backport patch to fix invocations of /bin/gdbus-codegen
- Related: #1481386
  See also bug 1507661

* Wed Oct 18 2017 Florian Müllner <fmuellner@redhat.com> - 2.54.1-1
- Update to 2.54.1
- Related: #1481386

* Tue Jun 06 2017 Colin Walters <walters@verbum.org> - 2.50.3-3
- Add patch to fix use-after-free in GDBus
- Resolves: #1437669

* Thu Mar 16 2017 Colin Walters <walters@verbum.org> - 2.50.3-2
- Add patch to remove debug print in fam
- Resolves: #1396386

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 2.50.3-1
- Update to 2.50.3
- Resolves: #1386874

* Thu Nov 10 2016 Kalev Lember <klember@redhat.com> - 2.50.2-1
- Update to 2.50.2
- Resolves: #1386874

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 2.46.2-4
- Backport a patch to fix a segfault in file monitor code
- Resolves: #1375753

* Tue Mar 08 2016 Colin Walters <walters@redhat.com> - 2.46.2-3
- Rebase to 2.46.2
- Backport two additional notable+applicable patches from upstream
  branch
- Resolves: #1305515

* Tue Sep 29 2015 Colin Walters <walters@redhat.com> - 2.42.2-5
- Add patch to fix FFI marshaling on BE architectures
- Resolves: #1260577

* Thu Aug 06 2015 Colin Walters <walters@redhat.com> - 2.42.2-4
- Add patch to silence gdbus exit-on-disconnect; Resolves #1177076

* Thu Jul 02 2015 Colin Walters <walters@redhat.com> - 2.42.2-3
- rebuilt; Resolves #1238463

* Thu Mar 19 2015 Richard Hughes <rhughes@redhat.com> - 2.42.2-2
- Update to 2.42.2
- [walters] Switch to autosetup -Sgit for less painful patch management
- [walters] Actually forward port patches
- Resolves: #1203755

* Wed Sep 03 2014 Ray Strode <rstrode@redhat.com> 2.40.0-4
- Add back g_memmove define for backward compat
  Related: #1104372

* Wed Sep 03 2014 Ray Strode <rstrode@redhat.com> 2.40.0-3
- Revert glib2 critical for better bug-for-bug 2.36.3 backward compatibility
  Resolves: #1132624

* Mon Mar 24 2014 Colin Walters <walters@redhat.com> - 2.40.0-1
- Update to 2.40.0
- Resolves: #1104372

* Tue Feb 11 2014 Colin Walters <walters@redhat.com> - 2.36.3-5
- Backport patch to fix gnome-shell lockups
  Resolves: #1030601
- Backport patch to fix vmtoolsd hangs
  Resolves: #1063789

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.36.3-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.36.3-3
- Mass rebuild 2013-12-27

* Thu Jun 20 2013 Colin Walters <walters@redhat.com> - 2.36.3-2
- Backport patch from upstream to fix dconf corruption, among
  other failures. (#975521)

* Sun Jun  9 2013 Matthias Clasen <mclasen@redhat.com> - 2.36.3-1
- Update to 2.36.3

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 2.36.2-1
- Update to 2.36.2

* Sat Apr 27 2013 Thorsten Leemhuis <fedora@leemhuis.info> - 2.36.1-2
- Fix pidgin freezes by applying patch from master (#956872)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.9-1
- Update to 2.35.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.8-1
- Update to 2.35.8

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.7-1
- Update to 2.35.7

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.4-1
- Update to 2.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.3-1
- Update to 2.35.3

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.2-1
- Update to 2.35.2

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.1-1
- Update to 2.35.1
- Drop upstreamed codegen-in-datadir.patch

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.1-1
- Update to 2.34.1

* Wed Oct 10 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.34.0-4
- Re-enable fam, put it in separate subpackage

* Wed Oct 10 2012 Matthias Clasen <mclasen@redhat.com> - 2.34.0-3
- Disable fam. We use the inotify implementation at runtime anyway.
  See http://lists.fedoraproject.org/pipermail/devel/2012-October/172438.htm

* Thu Sep 27 2012 Colin Walters <walters@verbum.org> - 2.34.0-2
- Use install -p to preserve timestamps on .py files
- Rename systemtap tapsets with architecture-specific prefix
- Pull upstream patch to avoid conflict on /usr/bin/gdbus-codegen
- Split gtk-doc off into -doc package to avoid multilib conflicts
- Resolves: #718404

* Mon Sep 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.0-1
- Update to 2.34.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.14-1
- Update to 2.33.14

* Wed Sep 12 2012 Lennart Poettering <lpoetter@redhat.com> - 2.33.12-2
- Drop explicit dependency on eject, as it is included in util-linux now, which is available in the base set

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 2.33.12-1
- Update to 2.33.12

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 2.33.10-1
- Update to 2.33.10

* Mon Aug 13 2012 Colin Walters <walters@verbum.org> - 2.33.6-3
- Re-add code to strip RPATHs (#840414)

* Fri Jul 20 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.33.6-2
- Add runtime dependency on eject (#748007)

* Wed Jul 18 2012 Matthias Clasen <mclasen@redhat.com> - 2.33.6-1
- Update to 2.33.6

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 2.33.4-1
- Update to 2.33.4

* Tue Jun 26 2012 Matthias Clsaen <mclasen@redhat.com> - 2.33.3-1
- Update to 2.33.3

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 2.33.2-1
- Update to 2.33.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.1-1
- Update to 2.33.1

* Mon Apr 30 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.1-3
- Obsolete the removed -static subpackage

* Mon Apr 30 2012 Colin Walters <walters@verbum.org> - 2.32.1-2
- Drop glib2-static subpackage; anaconda hasn't required it since
  2007.  See bug 193143.

* Fri Apr 13 2012 Matthias Clasen <mclasen@redhat.com> 2.32.1-1
- Update to 2.32.1

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> 2.31.22-1
- Update to 2.31.22

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> 2.31.20-1
- Update to 2.31.20

* Fri Feb 24 2012 Matthias Clasen <mclasen@redhat.com> 2.31.18-1
- Update to 2.31.18

* Tue Feb 21 2012 Richard Hughes <rhughes@redhat.com> 2.31.16-2
- Add BR: elfutils-libelf-devel for the GResource functionality

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> 2.31.16-1
- Update to 2.31.16
- Drop --with-runtime-libdir, since we have /lib -> /usr/lib now

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> 2.31.12-1
- Update to 2.31.12

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> 2.31.10-2
- Fix a header problem that was causing build failures

* Mon Jan 16 2012 Matthias Clasen <mclasen@redhat.com> - 2.31.10-1
- Update to 2.31.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.2-2
- Fix a GDBus regression leading to segfaults

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Fri Oct 21 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.31.0-1
- Update to 2.31.0

* Fri Oct 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Wed Oct 05 2011 Dan Williams <dcbw@redhat.com> - 2.30.0-2
- Fix signal marshalling on 64-bit big-endian platforms (rh #736489)

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.90-1
- Update to 2.29.90

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.18-1
- Update to 2.29.18

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.16-1
- Update to 2.29.16

* Sat Jul 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.14-1
- Update to 2.29.14

* Tue Jul  5 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.10-1
- Update to 2.29.10

* Tue Jun 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.8-1
- Update to 2.29.8

* Thu Jun  9 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.29.6-4
- Own %%ghost /usr/lib*/gio/modules/giomodule.cache.

* Mon Jun  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.6-3
- Fix a deadlock when finalizing e.g. widgets

* Sun Jun  5 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Fri May 27 2011 Colin Walters <walters@verbum.org> - 2.29.4-2
- Remove G_BROKEN_FILENAMES; Closes: #708536

* Fri May  6 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.29.4-1
- Update to 2.29.4

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.6-2
- Include byte-compiled files, it seems to be required (#670861)

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.6-1
- Update to 2.28.6

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.5-1
- Update to 2.28.5

* Tue Mar 29 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-2
- Fix some introspection annotations

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-1
- Update to 2.28.4

* Fri Mar 18 2011 Colin Walters <walters@verbum.org> - 2.28.3-2
- Rebuild to hopefully pick up new systemtap mark ABI
  The current version doesn't seem to be triggering the stock
  marks; a local rebuild of the RPM does, so let's do a rebuild
  here.

* Mon Mar 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.3-1
- Update to 2.28.3

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Fri Feb 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1
- Drop another space-saving hack from the spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Sat Jan 29 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.93-1
- Update to 2.27.93

* Mon Jan 24 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.27.92-2
- Don't run gio-querymodules* in %%postun if it no longer exists.

* Sat Jan 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92
- Drop update-gio-modules wrapper

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Thu Jan  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Wed Dec  1 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Wed Sep 29 2010 jkeating - 2.27.0-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.0-2
- Make /usr/bin/update-gio-modules executable
- Make /etc/bash_completion.d/*.sh not executable

* Mon Sep 20 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.15-1
- Update to 2.25.15

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.14-2
- Fix a PolicyKit problem

* Tue Aug 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.14-1
- Update to 2.25.14

* Mon Aug  9 2010 Colin Walters <walters@verbum.org> - 2.25.13-2
- Add patch from mjw to enable systemtap
  For background, see: https://bugzilla.gnome.org/show_bug.cgi?id=606044

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.13-1
- Update to 2.25.13

* Mon Aug  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.12-1
- Update to 2.25.12

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.11-1
- Update to 2.25.11

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 2.25.10-4
- Include gsettings bash completion

* Mon Jun 28 2010 Colin Walters <walters@verbum.org> - 2.25.10-3
- Revert rpath change; Fedora's libtool is supposed to not generate
  them for system paths.
- Add changes to spec file to support being built from snapshot as
  well as "make dist"-ball.  This includes BuildRequires and autogen.sh
  handling, and gtk-doc enabling if we're bootstrapping.

* Sun Jun 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.10-2
- Fix an evince crash

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.10-1
- Update to 2.25.10

* Wed Jun 23 2010 Colin Walters <walters@verbum.org> - 2.25.9-3
- Only strip rpath at install time, not before build.  Neutering
  libtool sabotages gtk-doc, since it needs those rpaths to run
  an in-tree binary.

* Tue Jun 22 2010 Richard Hughes <rhughes@redhat.com> - 2.25.9-2
- Backport a patch from git master to avoid a segfault when doing the
  schema file check for several GNOME projects.

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.9-1
- Update to 2.25.9

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.8-1
- Update to 2.25.8

* Tue May 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.7-2
- Require shared-mime-info

* Mon May 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.7-1
- Update to 2.25.7

* Wed May 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.6-1
- Update to 2.25.6
- Simplify gio-querymodules handling

* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.5-2
- Remove an erroneous removal

* Fri May 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Fri Apr 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3
- Move schema compiler to the main package, since it is
  needed by other rpm's %%post at runtime
- Split up man pages to go along with their binaries

* Mon Apr 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Add a multilib wrapper for gio-querymodules

* Mon Apr 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Mar 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Wed Mar 10 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Fix some rpmlint complaints

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Sun Feb 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Thu Feb 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.2-3
- Actually apply the patch, too

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Drop the dependency on a GLIBC_PRIVATE symbol

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Mon Dec 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Nov 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.23.0-1
- Update to 2.23.0

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-4
- Avoid multilib conflicts even harder

* Thu Sep 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-3
- Avoid multilib conflicts (#525213)

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Fix location of gdb macros

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Fri Sep  4 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.4-3
- Save some space

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Mon Jul  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.3-2
- Use --with-runtime-libdir

* Mon Jul  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Mon Jun 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Fri May 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Fri May 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.0-1
- Update to 2.21.0

* Thu Apr  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1
- See http://download.gnome.org/sources/glib/2.20/glib-2.20.1.news

* Fri Mar 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.10-2
- Fix integer overflows in the base64 handling functions. CVE-2008-4316

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.10-1
- Update to 2.19.10

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.8-1
- Update to 2.19.8
- Drop atomic patch, since we are building for i586 now

* Mon Feb 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.7-1
- Update to 2.19.7

* Mon Feb  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Mon Jan  5 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Mon Dec 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Tue Dec  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.2-2
- Rebuild

* Mon Dec  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Mon Dec  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.1-2
- Update to 2.19.1

* Mon Oct 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.2-3
- Use asm implementation for atomic ops on x86

* Fri Oct 24 2008 Alexander Larsson <alexl@redhat.com> - 2.18.2-2
- Don't return generic fallback icons for files,
  as this means custom mimetypes don't work (from svn)

* Thu Oct 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Wed Oct  1 2008 David Zeuthen <davidz@redhat.com> - 2.18.1-2
- Update the patch to always pass FUSE POSIX URI's

* Wed Sep 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.7-1
- Update to 2.17.7

* Thu Jul 24 2008 David Zeuthen <davidz@redhat.com> - 2.17.4-5
- rebuild

* Thu Jul 24 2008 David Zeuthen <davidz@redhat.com> - 2.17.4-4
- autoreconf

* Thu Jul 24 2008 David Zeuthen <davidz@redhat.com> - 2.17.4-3
- Backport patch for g_mount_guess_content_type_sync

* Mon Jul 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.4-2
- Fix statfs configure check

* Mon Jul 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Thu Jul  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.3-3
- Fix a stupid crash

* Wed Jul  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Mon Jun 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.2-2
- Fix a directory ownership oversight

* Thu Jun 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Thu Apr 24 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.16.3-5
- Add support for GIO to set selinux attributes (gnome #529694)

* Thu Apr 17 2008 David Zeuthen <davidz@redhat.com> - 2.16.3-4
- Only pass URI's for gio apps (#442835)

* Sun Apr 13 2008 Dan Williams <dcbw@redhat.com> - 2.16.3-3
- Revert upstream changes to g_static_mutex_get_mutex_impl_shortcut that broke
    users of GMutex and GStaticMutex (bgo#316221)

* Wed Apr  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.3-2
- Fix a possible crash in application launching (bgo#527132)

* Tue Apr  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.3-1
- Update to 2.16.3

* Thu Apr  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.2-2
- Fix occasional misbehaviour of g_timeout_add_seconds

* Tue Apr  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.2-1
- Update to 2.16.2

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Mon Mar  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.6-2
- Fix inline support

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.6-1
- Update to 2.15.6

* Mon Feb 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.5-1
- Update to 2.15.5

* Thu Feb  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.4-2
- Update PCRE to 7.6

* Mon Jan 28 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Mon Jan 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- 2.15.1
- add new BuildRequires

* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-4
- Another attempt

* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-3
- Fix some errors in desktop files handling

* Fri Dec 21 2007 Caolan McNamara <caolanm@redhat.com> - 2.15.0-2
- add jakubs patch in so xulrunner will build and so gcc too

* Thu Dec 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-1
- Update to 2.15.0

* Sat Nov 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.4-1
- Update to 2.14.4

* Wed Nov  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.3-1
- Update to 2.14.3, including a new version of PCRE that
  fixes several vulnerabilities

* Tue Oct 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1
- Update to 2.14.2 (bug fixes)

* Sun Sep 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.1-1
- Update to 2.14.1

* Sat Aug  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-3
- Update License field
- Don't ship ChangeLog

* Thu Jul 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-2
- Fix build issues on ppc

* Thu Jul 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-1
- Update to 2.13.7

* Fri Jun 29 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.6-1
- Update to 2.13.6
- Drop an ancient Conflict

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.5-1
- Update to 2.13.5

* Wed Jun  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.3-1
- Update to 2.13.3

* Wed May 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.1-1
- Update to 2.13.1

* Fri Mar  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.11-1
- Update to 2.12.11

* Wed Mar  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.10-1
- Update to 2.12.10

* Fri Feb  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-4
- More package review demands:
 * keep all -devel content in /usr/lib

* Sun Feb  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-3
- More package review feedback:
 * install /etc/profile.d snipplets as 644
 * explain Conflict with libgnomeui
 * remove stale Conflict with glib-devel

* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-2
- Incorporate package review feedback:
 * drop an obsolete Provides:
 * add a -static subpackage
 * explain %%check ppc exception
 * align summaries

* Tue Jan 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-1
- Update to 2.12.9

* Mon Jan 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.8-1
- Update to 2.12.8

* Thu Jan  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.7-1
- Update to 2.12.7
- Fix bit-test on x86-64

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.6-1
- Update to 2.12.6

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.5-2
- Fix the configure check for broken poll

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.5-1
- Update to 2.12.5

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.4-1
- Update to 2.12.4

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.3-1.fc6
- Update to 2.12.3
- Drop upstreamed patch

* Sun Aug 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.2-2.fc6
- Use Posix monotonic timers for GTimer

* Tue Aug 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.2-1.fc6
- Update to 2.12.2

* Sat Jul 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.12.0-1.1
- rebuild

* Sun Jul  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Jun 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1
- Update to 2.11.4

* Mon Jun 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.3-1
- Update to 2.11.3

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Thu Jun  1 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-6
- Rebuild

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-5
- Fix some fallout

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-4
- Include static libraries, since anaconda needs them (#193143)

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-3
- Keep glibconfig.h in /usr/lib

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-2
- Move glib to /lib

* Mon May 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Tue May 2 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.0-1
- Update to 2.11.0

* Fri Apr 7 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.2-2
- Update to 2.10.2

* Tue Mar 7 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Fri Feb 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Sat Feb 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.6-1
- Update to 2.9.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.9.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.9.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- Update to 2.9.5

* Wed Jan 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.3-1
- Update to 2.9.3

* Fri Jan  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.2-2
- Update to 2.9.2

* Sun Dec 11 2005 Matthias Clasen <mclasen@redhat.com>
- Specfile cosmetics

* Sat Dec 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.1-1
- New upstream version

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.0-1
- New upstream version

* Tue Nov 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.4-1
- New upstream version

* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.3-1
- New upstream version

* Mon Sep 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.2-1
- New upstream version

* Sat Aug 23 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.1-1
- New upstream version
- Drop patches

* Sat Aug 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.0-1
- New stable upstream version
- Drop patches

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-3
- Fix C++ guards in gstdio.h

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-2
- Another attempt to fix atomic ops on s390

* Tue Aug  3 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-1
- Update to 2.7.6

* Tue Aug  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Fri Jul 22 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Fri Jul 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Fri Jul  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Fri Jul  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Mon Jun 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.0-1
- Update to 2.7.0

* Wed Apr  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.4-1
- Update to 2.6.4
- Drop upstreamed patches

* Fri Mar 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-4
- Fix #150817

* Wed Mar  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-3
- Rebuild

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-2
- Rebuild with gcc4

* Mon Feb 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-1
- Upgrade to 2.6.3

* Fri Feb  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.2-1
- Upgrade to 2.6.2

* Mon Jan 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.1-1
- Upgrade to 2.6.1

* Mon Dec 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.6.0-1
- Upgrade to 2.6.0

* Mon Dec 06 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.8-1
- Upgrade to 2.4.8

* Wed Oct 13 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.7-1
- Upgrade to 2.4.7

* Fri Aug 13 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.6-1
- Update to 2.4.6

* Sun Aug 1 2004 ALan Cox <alan@redhat.com> - 2.4.5-2
- Fixed BuildRoot to use % macro not hardcode /var/tmp

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.5-1
- Update to 2.4.5
- Escape macros in changelog section

* Fri Jul 09 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.4-1
- Update to 2.4.4

* Mon Jun 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.2-1
- Require gettext at build time  (#125320)
- Update to 2.4.2 (#125736)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 2.4.1-1
- Update to 2.4.1

* Tue Mar 16 2004 Owen Taylor <otaylor@redhat.com> 2.4.0-1
- Update to 2.4.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.3.6-1
- Update to 2.3.6
- Remove gatomic build fix

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Mark McLoughlin <markmc@redhat.com> 2.3.5-1
- Update to 2.3.5
- Fix build on ppc64
- Disable make check on s390 as well - test-thread failing

* Wed Feb 25 2004 Mark McLoughlin <markmc@redhat.com> 2.3.3-1
- Update to 2.3.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Jonathan Blandford <jrb@redhat.com> 2.3.2-1
- new version
- remove 'make check' temporarily

* Mon Sep  8 2003 Owen Taylor <otaylor@redhat.com> 2.2.3-2.0
- Conflict with libgnomeui <= 2.2.0 (#83581, Göran Uddeborg)

* Tue Aug 26 2003 Owen Taylor <otaylor@redhat.com> 2.2.3-1.1
- Version 2.2.3

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 2.2.2-2.0
- Bump for rebuild

* Sun Jun  8 2003 Owen Taylor <otaylor@redhat.com>
- Version 2.2.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Sun Feb  2 2003 Owen Taylor <otaylor@redhat.com>
- Version 2.2.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Owen Taylor <otaylor@redhat.com>
- Add static libraries to build (#78685, Bernd Kischnick)
- Bump-and-rebuild for new redhat-rpm-config

* Fri Dec 20 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.2.0
- Add make check to the build process

* Mon Dec 16 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.5

* Wed Dec 11 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.4

* Mon Dec  2 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.3

* Mon Oct 07 2002 Havoc Pennington <hp@redhat.com>
- Try rebuilding with new arches

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- install glib2.sh and glib2.csh to set G_BROKEN_FILENAMES
- blow away unpackaged files in install

* Thu Aug  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.6
- Remove fixed-ltmain.sh; shouldn't be needed any more.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.4

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 24 2002 Havoc Pennington <hp@redhat.com>
 - rebuild in different environment

* Mon Apr 15 2002 Owen Taylor <otaylor@redhat.com>
- Fix missing .po files (#63336)

* Wed Apr  3 2002 Alex Larsson <alexl@redhat.com>
- Update to version 2.0.1

* Fri Mar  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.0

* Mon Feb 25 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.3.15

* Thu Feb 21 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Mon Feb 18 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.3.14

* Fri Feb 15 2002 Havoc Pennington <hp@redhat.com>
- add horrible buildrequires hack

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.3.13.91 cvs snap

* Mon Feb 11 2002 Matt Wilson <msw@redhat.com>
- rebuild from CVS snapshot
- use setup -q

* Thu Jan 31 2002 Jeremy Katz <katzj@redhat.com>
- rebuild

* Tue Jan 29 2002 Owen Taylor <otaylor@redhat.com>
- 1.3.13

* Tue Jan 22 2002 Havoc Pennington <hp@redhat.com>
- attempting rebuild in rawhide

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- remove 64-bit patch now upstream, 1.3.12.90

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- add some missing files to file list, langify

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- add temporary patch to fix GTypeFundamentals on 64-bit

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- Version 1.3.11

* Thu Oct 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.10

* Tue Sep 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.9

* Wed Sep 19 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.8

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Make -devel package require main package (#45388)
- Fix description and summary
- Configure with --disable-gtk-doc

* Wed Jun 20 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add some portability fixes needed at least on s390
- copy config.{guess,sub} instead of calling libtoolize

* Wed Jun 13 2001 Havoc Pennington <hp@redhat.com>
- try a new glib tarball with Makefile changes to work around
  libtool linking to installed .la files
- make -devel require pkgconfig

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- either libtool or the bad libtool hacks caused link
  against glib-gobject 1.3.2, rebuild

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- 1.3.6
- bad libtool workarounds

* Fri May 04 2001 Owen Taylor <otaylor@redhat.com>
- 1.3.5, rename to glib2

* Fri Nov 17 2000 Owen Taylor <otaylor@redhat.com>
- Final 1.3.2

* Mon Nov 13 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.3.2pre1
- Remove pkgconfig

* Sun Aug 13 2000 Owen Taylor <otaylor@redhat.com>
- Call 1.3.1b instead of snap... the snap* naming doesn't
  order correctly.

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- new snapshot with fixed .pc files

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- include .pc files in file list

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- Include pkg-config
- Upgrade to a glib CVS snapshot

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Fri Jul 14 2000 Owen Taylor <otaylor@redhat.com>
- Remove glib-config.1 manpage from build since
  it conflicts with glib-devel. When we go to
  glib glib1.2 setup, we should add it back

* Fri Jul 07 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.3.1
- Move back to standard %%{prefix}

* Thu Jun 8 2000 Owen Taylor <otaylor@redhat.com>
- Rebuild in /opt/gtk-beta

* Tue May 30 2000 Owen Taylor <otaylor@redhat.com>
- New version (adds gobject)

* Wed Apr 25 2000 Owen Taylor <otaylor@redhat.com>
- Don't blow away /etc/ld.so.conf (sorry!)

* Tue Apr 24 2000 Owen Taylor <otaylor@redhat.com>
- Snapshot RPM for Pango testing

* Fri Feb 04 2000 Owen Taylor <otaylor@redhat.com>
- Added fixes from stable branch of CVS

* Thu Oct 7  1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.6

* Fri Sep 24 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.5

* Fri Sep 17 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.4

* Mon Jun 7 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.3

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.1

* Fri Feb 26 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.2

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.0pre1

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- new description tags

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- removed libtoolize from %%build

* Thu Feb 11 1999 Michael Fulbright <drmike@redhat.com>
- added libgthread to file list

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.15

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.14

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.13

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.12

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated in preparation for the GNOME freeze

* Mon Apr 13 1998 Marc Ewing <marc@redhat.com>
- Split out glib package
