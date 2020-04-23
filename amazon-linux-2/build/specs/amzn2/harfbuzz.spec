Name:           harfbuzz
Version:        1.7.5
Release:        2%{?dist}
Summary:        Text shaping library

License:        MIT
URL:            http://freedesktop.org/wiki/Software/HarfBuzz
Source0:        http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-%{version}.tar.bz2

BuildRequires:  cairo-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  libicu-devel
BuildRequires:  graphite2-devel
BuildRequires:  gtk-doc

%description
HarfBuzz is an implementation of the OpenType Layout engine.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-icu%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        icu
Summary:        Harfbuzz ICU support library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    icu
This package contains Harfbuzz ICU support library.

%prep
%setup -q


%build
%configure --disable-static --with-graphite2

# Remove lib64 rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post icu -p /sbin/ldconfig
%postun icu -p /sbin/ldconfig


%files
%license COPYING
%doc NEWS AUTHORS README
%{_libdir}/libharfbuzz.so.*

%files devel
%doc %{_datadir}/gtk-doc
%{_bindir}/hb-view
%{_bindir}/hb-ot-shape-closure
%{_bindir}/hb-shape
%{_includedir}/harfbuzz/
%{_libdir}/libharfbuzz.so
%{_libdir}/pkgconfig/harfbuzz.pc
%{_libdir}/libharfbuzz-icu.so
%{_libdir}/pkgconfig/harfbuzz-icu.pc

%files icu
%{_libdir}/libharfbuzz-icu.so.*

%changelog
* Tue Jun 05 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.7.5-2
- Simply rebuild
- Resolves: #1576536

* Tue Jun 05 2018 Parag Nemade <pnemade AT redhat DOT com> - 1.7.5-1
- Update to 1.7.5
- Resolves: #1576536

* Mon Oct 17 2016 Kalev Lember <klember@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Resolves: #1386994

* Tue Apr 28 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.9.36-1
- Update to 0.9.36 upstream release
- Resolves: #1201148

* Mon Aug 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.9.20-4
- Resolves:rh#998812 - gedit segfaults when loading a certain file

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.20-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.20-2
- Mass rebuild 2013-12-27

* Fri Aug 30 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.20-1
- Update to 0.9.20 upstream release

* Wed Jul 17 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.19-1
- Update to 0.9.19 upstream release

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.18-3
- Don't ship a (humongous) ChangeLog

* Fri Jun 07 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.18-2
- Resolves:rh#971795:Merge -icu-devel subpackage into -devel subpackage

* Wed Jun 05 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.18-1
- Update to 0.9.18 upstream release

* Tue May 21 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.17-1
- Update to 0.9.17 upstream release

* Sat Apr 20 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.16-1
- Update to 0.9.16 upstream release

* Fri Mar 22 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.14-1
- Update to 0.9.14 upstream release

* Tue Feb 26 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.9.13-1
- Update to 0.9.13 upstream release

* Wed Jan 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.12-6
- Kill icu-config hack and rebuild against new icu again

* Tue Jan 29 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-5
- Resolves:rh#905334 - Please rebuild harfbuzz for new graphite-1.2.0

* Sun Jan 27 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-4
- Resolves:rh#904700-Enable additional shaper graphite2

* Sat Jan 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.12-3
- Add "icu-config --cppflags" to compiler flags to fix build

* Fri Jan 25 2013 Orion Poplawski <orion@cora.nwra.com> - 0.9.12-2
- Rebuild for libicu 50

* Sun Jan 20 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.12-1
- Update to 0.9.12 upstream release

* Fri Jan 11 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.11-1
- Update to 0.9.11 upstream release

* Thu Jan 03 2013 Parag Nemade <pnemade AT pnemade DOT com> - 0.9.10-1
- Update to 0.9.10 upstream release

* Thu Dec 06 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.9-1
- Update to 0.9.9 upstream release

* Wed Dec 05 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.8-1
- Update to 0.9.8 upstream release

* Wed Nov 21 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.7-1
- Update to 0.9.7 upstream release

* Wed Nov 14 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.6-1
- Update to 0.9.6 upstream release

* Mon Oct 15 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.5-1
- Update to 0.9.5 upstream release

* Mon Sep 10 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.4-1
- Update to 0.9.4 upstream release

* Sun Aug 19 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.3-1
- Update to 0.9.3 upstream release

* Mon Aug 13 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.2-1
- Update to 0.9.2 upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.0-6
- Rebuilt for libicu 49

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6.0-4
- Rebuild for new libpng

* Sat Sep 10 2011 Kalev Lember <kalevlember@gmail.com> - 0.6.0-3
- Rebuilt for libicu 4.8

* Thu Jun 16 2011 Kalev Lember <kalev@smartlink.ee> - 0.6.0-2
- Moved hb-view to -devel subpackage (#713126)

* Tue Jun 14 2011 Kalev Lember <kalev@smartlink.ee> - 0.6.0-1
- Initial RPM release
