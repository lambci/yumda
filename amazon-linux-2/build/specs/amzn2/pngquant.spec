# add some speed-relevant compiler-flags
%global optflags %(echo %{optflags} -fno-math-errno -funroll-loops -fomit-frame-pointer -fPIC )

%global libname libimagequant

Name:       pngquant
Version:    2.7.2
Epoch:      1
Release:    3%{?dist}
Summary:    PNG quantization tool for reducing image file size

License:    GPLv3+

URL:        http://%{name}.org
Source0:    https://github.com/pornel/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  libpng-devel >= 1.2.46-1
BuildRequires:  zlib-devel >= 1.2.3-1
BuildRequires:  lcms2-devel
Requires:       libpng%{?_isa} >= 1.2.46-1
Requires:       zlib%{?_isa} >= 1.2.3-1
Requires:       %{libname}%{?_isa} = %{epoch}:%{version}-%{release}


%description
%{name} converts 24/32-bit RGBA PNG images to 8-bit palette with alpha channel
preserved.  Such images are compatible with all modern web browsers and a
compatibility setting is available to help transparency degrade well in
Internet Explorer 6.  Quantized files are often 40-70 percent smaller than
their 24/32-bit version. %{name} uses the median cut algorithm.


%package -n %{libname}
Summary:    Small, portable C lib for HQ conversion of RGBA to 8-bit indexed-color


%description -n %{libname}
%{libname} converts 24/32-bit RGBA PNG images to 8-bit palette with alpha
channel preserved.  Such images are compatible with all modern web browsers and
a compatibility setting is available to help transparency degrade well in
Internet Explorer 6.  Quantized files are often 40-70 percent smaller than
their 24/32-bit version. %{libname} uses the median cut algorithm.


%package -n %{libname}-devel
Summary:    Development files for %{libname}
Requires:   %{libname}%{?_isa} = %{epoch}:%{version}-%{release}


%description -n %{libname}-devel
This package contains files for development with %{libname}.
There is also some brief API-documentation.


%prep
%setup -q
rm -f lib/configure


%build
%configure --with-openmp
%make_build bin.shared


%install
%make_install

mkdir -p %{buildroot}%{_includedir}/imagequant \
    %{buildroot}%{_libdir}

# install libimagequant
install -pm 0755 lib/%{libname}.so.0 \
    %{buildroot}%{_libdir}
ln -fs %{libname}.so.0 %{buildroot}%{_libdir}/%{libname}.so

install -pm 0644 lib/*.h \
    %{buildroot}%{_includedir}/imagequant

%check
# needed by ld / testsuite to find libimagequant
export LD_LIBRARY_PATH="$(pwd)/lib:$LD_LIBRARY_PATH"
make test.shared


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%doc README.md CHANGELOG
%license COPYRIGHT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%license lib/COPYRIGHT
%{_libdir}/%{libname}.so.*

%files -n %{libname}-devel
%doc lib/MANUAL.md
%{_includedir}/imagequant
%{_libdir}/%{libname}.so


%changelog
* Fri Dec 13 2019 Sérgio Monteiro Basto <sergio@serjux.com> - 1:2.7.2-3
- Add Epoch to respective Requires

* Tue Dec 10 2019 Sérgio Basto <sergio@serjux.com> - 1:2.7.2-2
- Bump Epoch

* Fri Dec 02 2016 Sérgio Basto <sergio@serjux.com> - 2.7.2-1
- Update pngquant 2.7.2

* Fri Jul 15 2016 Sérgio Basto <sergio@serjux.com> - 2.7.1-1
- Update pngquant 2.7.1

* Tue May 10 2016 Sérgio Basto <sergio@serjux.com> - 2.7.0-1
- Update to 2.7.0
- License change to GPLv3+ .

* Thu Mar 17 2016 Sérgio Basto <sergio@serjux.com> - 2.6.0-2
- Compilation with OpenMP

* Sun Feb 21 2016 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0 (#1310413)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Sérgio Basto <sergio@serjux.com> - 2.5.2-6
- Patches from here are upstreamed.

* Sat Dec 19 2015 Sérgio Basto <sergio@serjux.com> - 2.5.2-5
- Following https://fedoraproject.org/wiki/EPEL:Packaging#The_.25license_tag

* Sat Dec 19 2015 Björn Esser <fedora@besser82.io> - 2.5.2-4
- Add '-std=c99' for building the testsuite binary

* Sat Dec 19 2015 Björn Esser <fedora@besser82.io> - 2.5.2-3
- Add Patch1: make the configure-script work with %%configure
- Build and run the testsuite
- Conditionalize %%license
- Remove all el5-related things, since we need gcc >= 4.2 anyways
- Fix %%{?_isa} on (Build)Requires

* Sat Dec 19 2015 Sérgio Basto <sergio@serjux.com> - 2.5.2-2
- Disable pngquant debug (#1291885)

* Thu Nov 26 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2 (#1285589)

* Thu Aug 27 2015 Sérgio Basto <sergio@serjux.com> - 2.5.1-1
- Update to 2.5.1

* Thu Jul 02 2015 Sérgio Basto <sergio@serjux.com> - 2.5.0-1
- Update to 2.5.0 (#1238501)
- Update to pngquant-2.5.0_fix-Makefile.patch .

* Sat Jun 20 2015 Sérgio Basto <sergio@serjux.com> - 2.4.2-3
- pngquant now requires libimagequant with same version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2 (#1232532)
- Add license tag.

* Mon Apr 20 2015 Sérgio Basto <sergio@serjux.com> - 2.4.1-1
- Update to 2.4.1
- Dropped "epel compile fix" patch

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-4
- epel compile fix or compile fix for png15

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-3
- Reenabled SSE on i386, compiling is fixed !
- Better pngquant-2.4.0_fix-Makefile.patch more close to upstream.

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-2
- Fixed dependency of libimagequant.so.0
- Minor fix on ln to %{libname}.so

* Sun Apr 19 2015 Sérgio Basto <sergio@serjux.com> - 2.4.0.1-1
- Update to 2.4.0

* Mon Feb 09 2015 Sérgio Basto <sergio@serjux.com> - 2.3.4-1
- Update to 2.3.4

* Wed Jan 07 2015 Sérgio Basto <sergio@serjux.com> - 2.3.2-1
- New bug fix release.

* Fri Oct 17 2014 Sérgio Basto <sergio@serjux.com> - 2.3.1-1
- New bug fixing release

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.3.0-2
- Disable SSE on i386, to workaround building on i386 ,
  https://github.com/pornel/pngquant/issues/122

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.3.0-1
- New upstream version 2.3.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 23 2013 Björn Esser <bjoern.esser@gmail.com> - 2.0.0-1
- new upstream version 2.0.0 (#989991)
- fixes FTBFS in F20 / rawhide (#992807)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-6
- improved and added more el5-legacy related stuff

* Fri May 24 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-5
- add el5-build related conditonals

* Wed May 22 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-4
- add Group-Tag to make el5-build happy

* Sun May 19 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-3
- add Patch0: respect system compiler-flags
- touch a fake configure-script during prep
- export system cflags invoking configure-macro

* Fri May 17 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-2
- changed License: BSD --> BSD with advertising
- removed -n{name}-{version} from prep
- removed >= 1.2.46-1 from BuildRequires: libpng-devel

* Tue May 14 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.3-1
- Initial RPM release.
