%define glib2_version           2.26.0

Name: libnotify
Version: 0.7.7
Release: 1%{?dist}.0.2
Summary: Desktop notification library

License: LGPLv2+
URL: http://www.gnome.org
Source0: http://ftp.gnome.org/pub/GNOME/sources/libnotify/0.7/%{name}-%{version}.tar.xz

BuildRequires: chrpath
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gdk-pixbuf2-devel
BuildRequires: gtk3-devel
BuildRequires: gobject-introspection-devel
Requires: glib2%{?_isa} >= %{glib2_version}

%description
libnotify is a library for sending desktop notifications to a notification
daemon, as defined in the freedesktop.org Desktop Notifications spec. These
notifications can be used to inform the user about an event or display some
form of information without getting in the user's way.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files needed for
development of programs using %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

# Remove lib64 rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/notify-send

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%doc NEWS AUTHORS
%{_bindir}/notify-send
%{_libdir}/libnotify.so.*
%{_libdir}/girepository-1.0/Notify-0.7.typelib

%files devel
%dir %{_includedir}/libnotify
%{_includedir}/libnotify/*
%{_libdir}/libnotify.so
%{_libdir}/pkgconfig/libnotify.pc
%dir %{_datadir}/gtk-doc/html/libnotify
%{_datadir}/gtk-doc/html/libnotify/*
%{_datadir}/gir-1.0/Notify-0.7.gir

%changelog
* Fri Oct 14 2016 Kalev Lember <klember@redhat.com> - 0.7.7-1
- Update to 0.7.7
- Resolves: #1387013

* Tue May 05 2015 Ray Strode <rstrode@redhat.com> 0.7.5-8
- Don't require desktop notification daemon (breaks a build loop with mutter/gnome-shell)
  Related: #1174722

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.7.5-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.7.5-6
- Mass rebuild 2013-12-27

* Fri Mar 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.7.5-5
- Fix RHBZ #925824
- Update source URL
- Fix mix of spaces and tabs in spec file
- Fix bogus changelog date

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.5-2
- Fix glib2 dependency version.

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 0.7.5-1
- Update to 0.7.5

* Sun Mar  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.4-2
- Merge newer F-16 version into rawhide

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1
- Enable introspection

* Mon Jan  3 2011 Bill Nottingham <notting@redhat.com> - 0.7.0-2
- unbreak firefox and similar apps that free pixbufs they send to set_image_from_pixbuf (#654628)

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Tue Jun 29 2010 Bastien Nocera <bnocera@redhat.com> 0.5.1-1
- Update to 0.5.1

* Mon Jun 28 2010 Bastien Nocera <bnocera@redhat.com> 0.5.0-1
- Update to 0.5.0

* Wed Nov 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.4.5-4
- Close notifications with non-default actions on uninit

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.5-1
- Update to 0.4.5
- Drop obsolete patches
- Tweak %%summary and %%description

* Sat Aug 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.4-12
- Handle extra parameter of the closed signal

* Tue Jun 10 2008 Colin Walters <walters@redhat.com> - 0.4.4-11
- Add patch neccessary for reliable notification positioning

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.4-10
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-9
- Rebuild against new dbus-glib

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-8
- Rebuild

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-7
- Update licence field

* Wed Jun  6 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-6
- Re-add notification-daemon requirement again

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-5
- Temporarily remove the notification-daemon requires 
  for bootstrapping

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-4
- Re-add notification-daemon requirement

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-3
- Temporarily remove the notification-daemon requires 
  for bootstrapping

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-2
- Require gtk2-devel in the -devel package (#216946)

* Fri Mar 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-1
- Update to 0.4.4, which contains important bug fixes 
  and memory leak fixes
- Require pkgconfig in the -devel package

* Sat Dec  9 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.3-2
- Another typo (#214275)

* Sat Nov 11 2006 Ray Strode <rstrode@redhat.com> - 0.4.3-1
- Update 0.4.3

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.2-5
- Fix typos in the spec (#214275)
 
* Sun Sep 17 2006 Christopher Aillon <caillon@redhat.com> - 0.4.2-4
- Add upstream patch (r2899) to correct an invalid assertion when
  creating notifications using status icons

* Tue Aug 15 2006 Luke Macken <lmacken@redhat.com> - 0.4.2-3
- Add upstream patch libnotify-0.4.2-status-icon.patch to emit the correct
  property change notification 'status-icon' instead of 'attach-icon'

* Fri Jul 21 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.2-2
- Add developer docs to the devel section

* Fri Jul 21 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.2-1
- Update to upstream version 0.4.2
- Add dist tag to release
- Add Requires to devel package

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3.2
- reinstate desktop-notification dependency

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3.1
- comment out desktop-notification dependency so we can build the
  notification daemon

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3
- Add BR on dbus-glib-devel

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 0.4.0-2
- rebuild
- add missing brs

* Fri May 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Sat Mar 11 2006 Bill Nottingham <notting@redhat.com> - 0.3.0-6
- define %%{glib2_version} if it's in a requirement

* Thu Mar  2 2006 Ray Strode <rstrode@redhat.com> - 0.3.0-5
- patch out config.h include from public header

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 0.3.0-4
- Require a desktop-notification-daemon to be present.  Currently,
  this is notify-daemon, but libnotify doesn't specifically require
  that one.  Require 'desktop-notification-daemon' which daemons
  providing compatible functionality are now expected to provide.

* Wed Jan 11 2006 Christopher Aillon <caillon@redhat.com> - 0.3.0-3
- Let there be libnotify-devel...

* Tue Nov 15 2005 John (J5) Palmieri <johnp@redhat.com> - 0.3.0-2
- Actual release of the 0.3.x series

* Tue Nov 15 2005 John (J5) Palmieri <johnp@redhat.com> - 0.3.0-1
- Bump version to not conflict with older libnotify libraries

* Tue Nov 15 2005 John (J5) Palmieri <johnp@redhat.com> - 0.0.2-1
- inital build
