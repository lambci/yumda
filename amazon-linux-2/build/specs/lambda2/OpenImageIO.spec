%global subname oiio

Name:           OpenImageIO
Version:        1.5.24
Release:        3%{?dist}.1
Summary:        Library for reading and writing images

Group:          Development/Libraries
License:        BSD
URL:            https://sites.google.com/site/openimageio/home

Source0:        https://github.com/%{name}/%{subname}/archive/Release-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  txt2man
BuildRequires:  boost-devel
BuildRequires:  glew-devel
BuildRequires:  OpenEXR-devel ilmbase-devel
BuildRequires:  python2-devel
BuildRequires:  libpng-devel libtiff-devel openjpeg-devel giflib-devel
%if ! 0%{?rhel}
BuildRequires:  libwebp-devel
BuildRequires:  Field3D-devel
BuildRequires:  LibRaw-devel
%endif
BuildRequires:  hdf5-devel
BuildRequires:  zlib-devel
BuildRequires:  jasper-devel
BuildRequires:  pugixml-devel
BuildRequires:  opencv-devel

# WARNING: OpenColorIO and OpenImageIO are cross dependent.
# If an ABI incompatible update is done in one, the other also needs to be
# rebuilt.
BuildRequires:  OpenColorIO-devel

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Prefix: %{_prefix}


%description
OpenImageIO is a library for reading and writing images, and a bunch of related
classes, utilities, and applications. Main features include:
- Extremely simple but powerful ImageInput and ImageOutput APIs for reading and
  writing 2D images that is format agnostic.
- Format plugins for TIFF, JPEG/JFIF, OpenEXR, PNG, HDR/RGBE, Targa, JPEG-2000,
  DPX, Cineon, FITS, BMP, ICO, RMan Zfile, Softimage PIC, DDS, SGI,
  PNM/PPM/PGM/PBM, Field3d.
- An ImageCache class that transparently manages a cache so that it can access
  truly vast amounts of image data.


%package utils
Summary:        Command line utilities for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description utils
Command-line tools to manipulate and get information on images using the
%{name} library.


%prep
%setup -q -n oiio-Release-%{version}

# Remove bundled pugixml
rm -f src/include/pugixml.hpp \
      src/include/pugiconfig.hpp \
      src/libutil/pugixml.cpp 

# Remove bundled tbb
rm -rf src/include/tbb

%build
rm -rf build/linux && mkdir -p build/linux && pushd build/linux
# Needed to compile on GCC 7+
export CXXFLAGS="-faligned-new -Wno-error=misleading-indentation -Wno-error=format-truncation $CXXFLAGS"
# CMAKE_SKIP_RPATH is OK here because it is set to FALSE internally and causes
# CMAKE_INSTALL_RPATH to be cleared, which is the desiered result.
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_SKIP_RPATH:BOOL=TRUE \
       -DINCLUDE_INSTALL_DIR:PATH=%{_includedir}/%{name} \
       -DINSTALL_DOCS:BOOL=FALSE \
       -DUSE_EXTERNAL_PUGIXML:BOOL=TRUE \
       -DVERBOSE=TRUE \
       -DUSE_QT=0 \
       -DUSE_PYTHON=0 \
       -DOIIO_BUILD_TESTS=0 \
       ../../

make %{?_smp_mflags}


%install
pushd build/linux
make DESTDIR=%{buildroot} install


%files
%license LICENSE
%{_libdir}/libOpenImageIO.so.*
%{_libdir}/libOpenImageIO_Util.so.*

%files utils
%{_bindir}/*

%exclude %{_includedir}
%exclude %{_libdir}/*.so


%changelog
* Wed Apr 22 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Oct 03 2016 Richard Shaw <hobbes1069@gmail.com> - 1.5.24-3
- Rebuild for pugixml with c++11 enabled.

* Sun Jul  3 2016 Richard Shaw <hobbes1069@gmail.com> - 1.5.24-2
- Rebuild for updated Field3D which broke due to soname bump, fixes BZ#1352267.

* Thu Mar  3 2016 Richard Shaw <hobbes1069@gmail.com> - 1.5.24-1
- Update to latest upstream release.

* Thu Dec 17 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.22-1
- Update to latest upstream release.
- Add LibRaw to build requirements.

* Wed Dec  2 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.21-1
- Update to latest upstream release.
- Move python bindings to their own subpackage.

* Thu Oct 22 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.20-2
- Rebuild for updated pugixml.

* Mon Sep 28 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.20-1
- Update to latest upstream release.

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.5.18-3
- Rebuilt for Boost 1.59

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 1.5.18-2
- Rebuilt for Boost 1.58

* Tue Aug  4 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.18-1
- Update to latest upstream release.

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.17-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.5.17-2
- rebuild for Boost 1.58

* Thu Jul 16 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.17-1
- Update to latest upstream release.

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.14-3
- Rebuild for hdf5 1.8.15

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.14-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Apr 15 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.14-1
- Update to latest upstream release.

* Wed Mar 11 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.13-1
- Update to latest upstream release.

* Sat Feb 21 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.12-3
- Rebuild for undefined symbols

* Thu Feb 12 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.12-2
- Update to latest upstream release.
- Add opencv optional dependency.
- Use new license rpmbuild macro.
- Fix broken conditional which prevented Field3D from being required.

* Wed Feb 11 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.11-3
- Rebuild for Field3D.

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 1.5.11-2
- Bump for rebuild.

* Wed Jan 28 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.11-1
- Update to latest upstream release.

* Tue Jan 27 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5.10-1
- Update to latest upstream release.

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.4.16-2
- Rebuild for boost 1.57.0

* Thu Jan 22 2015 Richard Shaw <hobbes1069@gmail.com> - 1.4.16-1
- Update to latest upstream release.

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 1.4.15-2
- rebuild (openexr)

* Tue Nov 25 2014 Richard Shaw <hobbes1069@gmail.com> - 1.4.15-1
- Update to latest upstream release.

* Fri Nov 14 2014 Richard Shaw <hobbes1069@gmail.com> - 1.4.14-1
- Update to latest upstream release.

* Fri Sep  5 2014 Richard Shaw <hobbes1069@gmail.com> - 1.4.12-4
- Rebuild for Field3D 1.4.3.

* Thu Sep 04 2014 Orion Poplawski <orion@cora.nwra.com> - 1.4.12-3
- Rebuild for pugixml 1.4

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug  1 2014 Richard Shaw <hobbes1069@gmail.com> - 1.4.12-1
- Update to latest upstream release.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.4.7-3
- Rebuild for boost 1.55.0

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 1.4.7-2
- rebuild for boost 1.55.0

* Mon May 19 2014 Richard Shaw <hobbes1069@gmail.com> - 1.4.7-1
>>>>>>> master
- Update to latest upstream release.

* Tue Jan  7 2014 Richard Shaw <hobbes1069@gmail.com> - 1.3.10-1
- Update to latest upstream release.
- Add libgif as build requirement.

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.2.3-3
- rebuild (openexr)

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 1.2.3-2
- rebuilt for GLEW 1.10

* Wed Nov  6 2013 Richard Shaw <hobbes1069@gmail.com> - 1.2.3-1
- Update to latest upstream release.
- Fix ppc builds (BZ#1021977).
- Add conditionals to build requirements for EPEL 6.

* Wed Oct  2 2013 Richard Shaw <hobbes1069@gmail.com> - 1.2.2-1
- Update to latest upstream release.

* Sun Sep 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-2
- rebuild (ilmbase/openexr)

* Thu Aug  8 2013 Richard Shaw <hobbes1069@gmail.com> - 1.2.1-1
- Update to latest upstream release.

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Petr Machata <pmachata@redhat.com> - 1.2.0-2
- Rebuild for boost 1.54.0
