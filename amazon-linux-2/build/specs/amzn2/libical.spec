%define _trivial .0
%define _buildid .1
%define compat_build_dir libical-1.0.1

Summary:	Reference implementation of the iCalendar data type and serialization format
Name:		libical
Version:	3.0.3
Release:	2%{?dist}%{?_trivial}%{?_buildid}
License:	LGPLv2 or MPLv2.0
URL:		https://libical.github.io/libical/
Source:		https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/%{name}/%{name}/archive/v1.0.1/%{name}-1.0.1.tar.gz
Patch0:		libical-1.0-avoid-putenv.patch
Patch1:		libical-3.0.3-cmake-version.patch

# because 'Version:' in compat-libical subpackage overrides %%{version} value
%global gir_version %{version}

BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	perl
#BuildRequires:	python
#BuildRequires:	python-gobject
BuildRequires:	vala
Requires:	tzdata

%description
Reference implementation of the iCalendar data type and serialization format
used in dozens of calendaring and scheduling products.

%package devel
Summary:	Development files for libical
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(icu-i18n)
Requires:	pkgconfig(icu-uc)

%description devel
The libical-devel package contains libraries and header files for developing
applications that use libical.

%package glib
Summary:	GObject wrapper for libical library
Provides:	libical-glib%{?_isa} = %{version}-%{release}
Obsoletes:	libical-glib < 3.0.0
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description glib
This package provides a GObject wrapper for libical library with support
of GObject Introspection.

%package glib-doc
Summary:	Documentation files for %{name}-glib
Group:		Development/Libraries
Provides:	libical-glib-doc = %{version}-%{release}
Obsoletes:	libical-glib-doc < 3.0.0
BuildArch:	noarch

%description glib-doc
This package contains developer documentation for %{name}-glib.

%package glib-devel
Summary:	Development files for building against %{name}-glib
Group:		Development/Libraries
Provides:	libical-glib-devel%{?_isa} = %{version}-%{release}
Obsoletes:	libical-glib-devel < 3.0.0
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-glib%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(gobject-2.0)

%description glib-devel
Development files needed for building things which link against %{name}-glib.

%package -n compat-libical1
Summary:	Compat package with libical 1.0.1 libraries
Version:	1.0.1
License:	LGPLv2 or MPLv1.1
# Explicitly conflict with older libical packages that ship libraries
# with the same soname as this compat package
Conflicts:	libical < 3.0.0

%description -n compat-libical1
Compatibility package with libical libraries ABI version 1.

%prep
%setup -q
%patch1 -p1 -b .cmake-version

%setup -T -D -a 1

pushd %{compat_build_dir}
%patch0 -p1 -b .avoid-putenv
popd

%build

# the compat package first
pushd %{compat_build_dir}
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd
make %{?_smp_mflags} -C %{_target_platform}
popd

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DUSE_INTEROPERABLE_VTIMEZONES:BOOL=true \
  -DICAL_ALLOW_EMPTY_PROPERTIES:BOOL=true \
  -DGOBJECT_INTROSPECTION:BOOL=true \
  -DICAL_GLIB:BOOL=true \
  -DICAL_GLIB_VAPI:BOOL=true \
  -DSHARED_ONLY:BOOL=true
popd

make %{?_smp_mflags} -C %{_target_platform} -j1

%install

# the compat package first
pushd %{compat_build_dir}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
# omit static libs
rm -fv %{buildroot}%{_libdir}/lib*.a
# Remove files that aren't needed for the compat package
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_libdir}/cmake/
rm -rf %{buildroot}%{_libdir}/pkgconfig/
popd

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%check
# the compat package first
# Test fails on 32 bits https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=919571
%ifnarch i686
pushd %{compat_build_dir}
make test ARGS="-V" -C %{_target_platform}
popd
%endif

make test ARGS="-V" -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE ReadMe.txt THANKS
%{_libdir}/libical.so.3*
%{_libdir}/libical_cxx.so.3*
%{_libdir}/libicalss.so.3*
%{_libdir}/libicalss_cxx.so.3*
%{_libdir}/libicalvcal.so.3*
%{_libdir}/girepository-1.0/libical-%{gir_version}.typelib
%{_datadir}/gir-1.0/libical-%{gir_version}.gir

%files devel
%doc doc/UsingLibical.txt
%{_libdir}/libical.so
%{_libdir}/libical_cxx.so
%{_libdir}/libicalss.so
%{_libdir}/libicalss_cxx.so
%{_libdir}/libicalvcal.so
%{_libdir}/pkgconfig/libical.pc
%{_libdir}/cmake/LibIcal/
%{_includedir}/libical/

%files glib
%{_libdir}/libical-glib.so.3*
%{_libdir}/girepository-1.0/ICalGLib-3.0.typelib
%{_datadir}/gir-1.0/ICalGLib-3.0.gir

%files glib-devel
%{_libdir}/libical-glib.so
%{_libdir}/pkgconfig/libical-glib.pc
%{_includedir}/libical-glib/
%{_datadir}/vala/vapi/libical-glib.vapi

%files glib-doc
%{_datadir}/gtk-doc/html/%{name}-glib

%files -n compat-libical1
%doc %{compat_build_dir}/LICENSE
%{_libdir}/libical.so.1*
%{_libdir}/libicalss.so.1*
%{_libdir}/libicalvcal.so.1*

%changelog
* Mon Sep 9 2019 Andrew Egelhofer <egelhofe@amazon.com> - 3.0.3-2.amzn2.0.1
- Disable %check on compat_build_dir when building on 32 bits
  https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=919571

* Tue Jun 19 2018 Milan Crha <mcrha@redhat.com> - 3.0.3-2
- Update Requires of libical-glib-devel

* Thu May 31 2018 Milan Crha <mcrha@redhat.com> - 3.0.3-1
- Update to 3.0.3 and build compat-libical1 subpackage
- Resolves: #1584655

* Wed Jul 08 2015 Milan Crha <mcrha@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.48-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.48-5
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Robert Scheck <robert@fedoraproject.org> 0.48-1
- Upgrade to 0.48 (#664412, #696891, #743236)

* Mon Oct 24 2011 Robert Scheck <robert@fedoraproject.org> 0.47-1
- Upgrade to 0.47 (#743236)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Robert Scheck <robert@fedoraproject.org> 0.46-2
- Added patch to work around upstream's broken AC_PROG_MKDIR_P

* Sun Dec 19 2010 Robert Scheck <robert@fedoraproject.org> 0.46-1
- Upgrade to 0.46 (#525933, #628893)
- Fixed race in populating builtin timezone components (#637150)
- Fixed wrong ICAL_ERRORS_ARE_FATAL preprocessor check (#575715)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-4
- Updated patch to fix #includes in the headers to work with
  'pkg-config --cflags libical'. (Red Hat Bugzilla #484091)

* Wed Feb 25 2009 Release Engineering <rel-eng@.fedoraproject.org> - 0.43-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-2
- Added patch to fix CFLAGS in libical.pc. (Red Hat Bugzilla #484091)

* Tue Jan 13 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.43-1
- Version bump to 0.43.
- Added patch to fix implicit pointer conversion from Debian. (Debian BTS
  #511598)
- Upstream has switched off ICAL_ERRORS_ARE_FATAL by default. This behaviour
  is being retained across all distributions, including Fedora 11.
- Added 'Requires: tzdata'.
- Enabled backtrace dumps in the syslog.

* Thu Jan 08 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.41-2
- Switched off ICAL_ERRORS_ARE_FATAL for all distributions, except Fedora 11.
  (Red Hat Bugzilla #478331)

* Sun Nov 23 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.41-1
- Version bump to 0.41. (Red Hat Bugzilla #469252)
- Disabled C++ bindings.

* Tue Oct 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.40-1
- Version bump to 0.40. (Red Hat Bugzilla #466359)
- Add patch from upstream to fix crash in icalvalue.c.
- Update makefile patch, remove the test part (already applied).
- Package libical.pc, add Requires: pkgconfig to -devel.

* Tue Sep 02 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.32-1
- Version bump to 0.32.
- Parallel build problems fixed.

* Sun Jul 27 2008 Jeff Perry <jeffperry_fedora@sourcesink.com> - 0.31-3
- Added 'BuildRequires: bison byacc flex'.

* Sun Jul 27 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.31-2
- Fixed linkage problems and disabled parallel build till upstream accepts fix.

* Thu Jul 17 2008 Jeff Perry <jeffperry_fedora@sourcesink.com> - 0.31-1
- Version bump to 0.31.

* Thu Jul 17 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.30-4
- Changed value of License according to Fedora licensing guidelines.
- Enabled reentrant system calls and C++ bindings.
- Omitted unused direct shared library dependencies.
- Added ChangeLog, COPYING, LICENSE, NEWS and README to doc and dropped
  examples.

* Wed Apr 02 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.30-3
- Source URL... Fixed

* Wed Apr 02 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.30-2
- Removed untrue note about libical's homepage (to get rid of eventuall mess)

* Sat Feb 23 2008 David Nielsen <gnomeuser@gmail.com> - 0.30-1
- Switch to freeassociation libical
- bump to 0.30

* Sat Feb 09 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-5
- Mass rebuild for new GCC... Done

* Sat Jan 19 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-4
- Licence... Fixed

* Fri Jan 18 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-3
- Files section... Fixed

* Thu Jan 17 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-2
- Source... Changed
- Debug information in libical main package... Excluded
- Non-numbered .so files in libical main package... Moved
- libical-devel documentation... Added

* Mon Dec 24 2007 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.27-1
- Initial release
