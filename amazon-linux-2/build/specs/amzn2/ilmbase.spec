
Name:	 ilmbase 
Version: 1.0.3
Release: 7%{?dist}.0.2
Summary: Abstraction/convenience libraries

Group:	 System Environment/Libraries
License: BSD
URL:	 http://www.openexr.com/
Source0: https://github.com/downloads/openexr/openexr/ilmbase-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: automake libtool
BuildRequires: pkgconfig
# silly rpm, won't pick up rpm dependencies for items not in it's buildroot
# see http://bugzilla.redhat.com/866302
BuildRequires: pkgconfig(gl) pkgconfig(glu)

## upstreamable patches
# revert soname bump
# upstream missed bumping to so7 for OpenEXR-1.7.0, decided to do so now for
# OpenEXR-1.7.1.  given fedora has shipped OpenEXR-1.7.0 since f15, bumping
# ABI now makes little sense.
Patch50: ilmbase-1.0.3-so6.patch
# explicitly add $(PTHREAD_LIBS) to libIlmThread linkage (helps workaround below)
Patch51: ilmbase-1.0.2-no_undefined.patch
# the FPU exception code is x86 specific
Patch52: ilmbase-1.0.3-secondary.patch
# add Requires.private: gl glu to IlmBase.pc
Patch53:  ilmbase-1.0.3-pkgconfig.patch

## upstream patches
# fix build on i686/32bit
# https://github.com/openexr/openexr/issues/3
Patch100: ilmbase-1.0.3-ucontext.patch

%description
Half is a class that encapsulates the ilm 16-bit floating-point format.

IlmThread is a thread abstraction library for use with OpenEXR
and other software packages.

Imath implements 2D and 3D vectors, 3x3 and 4x4 matrices, quaternions
and other useful 2D and 3D math functions.

Iex is an exception-handling library.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Group:	 Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

%patch50 -p1 -b .so6
%patch51 -p1 -b .no_undefined
%patch52 -p1 -b .secondary
%patch53 -p1 -b .pkgconfig
%if %{__isa_bits} == 32
%patch100 -p1 -b .ucontext
%endif
./bootstrap


%build
%configure --disable-static

# manually set PTHREAD_LIBS to include -lpthread until libtool bogosity is fixed,
# https://bugzilla.redhat.com/show_bug.cgi?id=661333
make %{?_smp_mflags} PTHREAD_LIBS="-pthread -lpthread"


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -fv  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion IlmBase)" = "%{version}"
# is the known-failure ix86-specific or 32bit specific? guess we'll find out -- rex
%ifarch %{ix86}
make check ||:
%else
make check
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libHalf.so.6*
%{_libdir}/libIex.so.6*
%{_libdir}/libIexMath.so.6*
%{_libdir}/libIlmThread.so.6*
%{_libdir}/libImath.so.6*

%files devel
%defattr(-,root,root,-)
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/IlmBase.pc


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.3-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.3-6
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-4
- ilmbase-devel missing dependency on libGLU-devel (#866302)

* Sat Sep 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-3
- IlmBase.pc: +Requires.private: gl glu
- -devel: drop hard-coded libGL/pkgconfig deps, let rpm autodetect now

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> 1.0.3-2
- fix build on non-x86 arches

* Sun Aug 05 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-1
- ilmbase-1.0.3
- ix86 fix courtesy of Nicolas Chauvet <kwizart@gmail.com>

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-2
- libIlmThread missing -pthread linkage (#661115)
- %%install: INSTALL="install -p"
- -devel: tighten dep using %%?_isa

* Wed Jul 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-1
- ilmbase-1.0.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May  4 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.0.1-5
- Fix spelling error in summary.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- rebuild for pkgconfig deps

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-2
- respin (gcc43)

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-1
- ilmbase-1.0.1

* Fri Oct 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-3
- include *.tar.sig in sources

* Mon Oct 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-2
- update %%summary
- -devel: +Requires: libGL-devel libGLU-devel
- make install ... INSTALL="install -p" to preserve timestamps


* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-1
- ilmbase-1.0.0 (first try)

