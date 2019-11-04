%define gettext_package dbus

%define expat_version           1.95.5
%define glib2_version           2.2.0
%define gtk2_version 2.4.0
%define dbus_version 1.1

Summary: GLib bindings for D-Bus
Name: dbus-glib
Version: 0.100
Release: 7.2%{?dist}
URL: http://www.freedesktop.org/software/dbus/
#VCS: git:git://git.freedesktop.org/git/dbus/dbus-glib
Source0: http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
License: AFL and GPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: chkconfig >= 1.3.26
BuildRequires: libtool
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: libxml2-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gettext

Patch0: 0001-CVE-2013-0292-dbus-gproxy-Verify-sender-of-NameOwner.patch

Prefix: %{_prefix}

%description

D-Bus add-on library to integrate the standard D-Bus library with
the GLib thread abstraction and main loop.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-tests \
	--enable-verbose-mode=yes \
	--enable-asserts=yes \
	--disable-gtk-doc

#build with checks for right now but disable checks for final release
#%configure  --disable-tests --disable-verbose-mode --disable-asserts
make

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)

%license COPYING

%{_libdir}/*glib*.so.*
%{_bindir}/dbus-binding-tool

%exclude %{_includedir}
%exclude %{_datadir}
%exclude %{_mandir}
%exclude %{_sysconfdir}
%exclude %{_libexecdir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.100-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.100-6
- Mass rebuild 2013-12-27

* Mon Jul 01 2013 Colin Walters <walters@redhat.com> - 0.100-5
- CVE-2013-0292  (previous patch was not actually applied)
- Resolves: #911714

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.100-4
- Don't install ChangeLog (need to save space on the live image)

* Wed Feb 20 2013 Colin Walters <walters@redhat.com> - 0.100-3
- CVE-2013-0292
  Resolves: #911714

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Colin Walters <walters@verbum.org> - 0.100-1
- Update to 0.100

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Christopher Aillon <caillon@redhat.com> - 0.92-1
- Update to 0.92

* Wed Sep 29 2010 jkeating - 0.88-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Colin Walters <walters@verbum.org> - 0.88-2
- Drop .gir file, it's now in gobject-introspection

* Thu Aug 12 2010 Colin Walters <walters@verbum.org> - 0.88-1
- New upstream version
- drop now-merged shadow props patch

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.86-4
- Rebuild against new gobject-introspection

* Tue Jun 29 2010 Dan Williams <dcbw@redhat.com> - 0.86-3
- Fix shadow property access (fdo #28835)

* Tue Jun 29 2010 Bastien Nocera <bnocera@redhat.com> 0.86-2
- Add introspection data from gir-repository
- Remove unneeded autotools calls

* Thu Mar 18 2010 Colin Walters <walters@verbum.org> - 0.86-1
- New upstream
  Drop upstreamed patch

* Tue Mar 02 2010 Colin Walters <walters@verbum.org> - 0.84-3
- Revert previous broken patch for error names, add better fix

* Mon Feb 15 2010 Colin Walters <walters@verbum.org> - 0.84-2
- Add patch to avoid assertions when setting a GError that
  includes a '-' in the enumeration value.  Should fix #528897

* Wed Jan 27 2010 Colin Walters <walters@verbum.org> - 0.84-1
- New upstream
  Has introspect.xml internally, drop it from here

* Fri Jan 15 2010 Colin Walters <walters@verbum.org> - 0.82-3
- Add ListActivatableNames to dbus-bus-introspect.xml to help tracker build

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Colin Walters <walters@verbum.org> - 0.82-1
- New upstream 0.82
- Remove mclasen accidental commit of CFLAGS="-O0 -g3"

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 0.80-3
- Minor directory ownership cleanup

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Colin Walters <walters@verbum.org> - 0.80-1
- New upstream release
- Adjust to new bash completion dir
- Includes patch noreply patch

* Wed Jan 07 2009 Colin Walters <walters@verbum.org> - 0.78-2
- Add patch to avoid sending reply to noreply messages; this avoids
  some spurious dbus denial logs during system startup from NM

* Thu Dec 04 2008 Colin Walters <walters@verbum.org> - 0.78-1
- New upstream release, drop upstreamed patches

* Tue Nov 25 2008 Matthias Clasen <mclasen@redhat.com> - 0.76-4
- Avoid some spurious linkage

* Mon Nov 17 2008 Dan Williams <dcbw@redhat.com> - 0.76-3
- Fix crashes when a tracked service restarts too quickly (fdo #18573)

* Thu Jul 31 2008 David Zeuthen <davidz@redhat.com> - 0.76-2
- Add bash completion for dbus-send(1)

* Thu Jun 05 2008 Colin Walters <walters@redhat.com> - 0.76-1
- New upstream 0.76
- Drop all upstreamed patches

* Tue May 27 2008 Dan Williams <dcbw@redhat.com> - 0.74-9
- Handle unknown object properties without asserting (fdo #16079)
- Handle GetAll() property names correctly (fdo #16114)
- Enable the freeze-abi patch
- Cherry-pick some fixes from upstream git

* Thu May  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.74-8
- Fix license field

* Tue Apr 15 2008 Colin Walters <walters@redhat.com> - 0.74-7
- Ensure ABI is frozen as it stands now

* Fri Apr  4 2008 David Zeuthen <davidz@redhat.com> - 0.74-6
- Add another upstreamed patch for setting the default timeout
  on a proxy

* Fri Apr  4 2008 David Zeuthen <davidz@redhat.com> - 0.74-5
- Add an already upstreamed patch to export the GetAll() method on
  the org.freedesktop.DBus.Properties interface

* Wed Mar 19 2008 Dan Williams <dcbw@redhat.com> - 0.74-4
- Ignore children of namespaced nodes too

* Tue Feb 12 2008 Dan Williams <dcbw@redhat.com> - 0.74-3
- Ignore namespaces in introspection XML

* Sun Nov 18 2007 Dan Williams <dcbw@redhat.com> - 0.74-2
- Actually apply the patch for fdo #12505

* Mon Oct 22 2007 Ray Strode <rstrode@redhat.com> - 0.74-1
- Update to 0.74

* Mon Sep 24 2007 Dan Williams <dcbw@redhat.com> - 0.73-4
- Dispatch NameOwnerChanged signals to proxies only once (fdo #12505)

* Sat Sep 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-3
- Rebuild against new expat

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-2
- Fix a bug in introspection support (#248150)

* Wed Apr  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-1
- Update to 0.73 (#233631)
- Drop upstreamed patches

* Tue Dec 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.71-4
- Add dbus-glib-0.70-use-default-threads.patch
- Partial fix to #219257

* Wed Nov 29 2006 David Zeuthen <davidz@redhat.com> - 0.71-3%{?dist}
- Add dbus-glib-0.70-fix-info-leak.patch
- Resolves: #216034

* Sun Nov  5 2006 Matthias Clasen <mclasen@redhat.com> - 0.71-2
- Fix up Requires for the -devel package

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.71-1
- Update to 0.71

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-4
- remove improper obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Pregenerate the xml introspect file so you don't need dbus running during
  the build 

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial dbus-glib package
