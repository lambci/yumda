%global _trivial .0
%global _buildid .1
#global indice   a

Name:           opencv
Version:        2.4.5
Release: 3%{?dist}.0.2
Summary:        Collection of algorithms for computer vision

Group:          Development/Libraries
# This is normal three clause BSD.
License:        BSD
URL:            http://opencv.org
# Need to remove SIFT/SURF from source tarball, due to legal concerns
# rm -rf opencv-%%{version}/modules/nonfree/src/sift.cpp
# rm -rf opencv-%%{version}/modules/nonfree/src/surf.cpp
# Source0:        http://downloads.sourceforge.net/opencvlibrary/%{name}-%{version}%{?indice}.tar.bz2
Source0:	%{name}-%{version}%{?indice}-clean.tar.xz
Source1:        opencv-samples-Makefile
Patch0:         opencv-pkgcmake.patch
Patch1:         opencv-pkgcmake2.patch
#http://code.opencv.org/issues/2720
Patch2:         OpenCV-2.4.4-pillow.patch

Patch1000:	opencv-gcc7-fix.patch

BuildRequires:  libtool
BuildRequires:  cmake >= 2.6.3
BuildRequires:  chrpath

%{?_with_eigen2:BuildRequires:  eigen2-devel}
%{?_with_eigen3:BuildRequires:  eigen3-devel}
BuildRequires:  gtk2-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%if 0%{?fedora} >= 1
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
%endif
BuildRequires:  jasper-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libv4l-devel
BuildRequires:  OpenEXR-devel
%{?_with_openni:
%ifarch %{ix86} x86_64
BuildRequires:  openni-devel
BuildRequires:  openni-primesense
%endif
}
%{?_with_ttb:
%ifarch %{ix86} x86_64 ia64 ppc ppc64
BuildRequires:  tbb-devel
%endif
}
BuildRequires:  zlib-devel, pkgconfig
BuildRequires:  python-devel
BuildRequires:  numpy, swig >= 1.3.24
BuildRequires:  python-sphinx
%{?_with_ffmpeg:BuildRequires:  ffmpeg-devel >= 0.4.9}
%{!?_without_gstreamer:BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel}
%{?_with_xine:BuildRequires:  xine-lib-devel}


Requires:       opencv-core%{_isa} = %{version}-%{release}


%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package core
Summary:        OpenCV core libraries
Group:          Development/Libraries

%description core
This package contains the OpenCV C/C++ core libraries.

%package devel
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-devel-docs
package.

%package devel-docs
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv-devel = %{version}-%{release}
Requires:       pkgconfig
BuildArch:      noarch

%description devel-docs
This package contains the OpenCV documentation and examples programs.

%package python
Summary:        Python bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv = %{version}-%{release}
Requires:       numpy

%description python
This package contains Python bindings for the OpenCV library.


%prep
%setup -q
%patch0 -p1 -b .pkgcmake
%patch1 -p1 -b .pkgcmake2
%patch2 -p1 -b .pillow

%patch1000 -p1 -b .gcc7

# fix dos end of lines
sed -i 's|\r||g'  samples/c/adaptiveskindetector.cpp


%build
# enabled by default if libraries are presents at build time:
# GTK, GSTREAMER, UNICAP, 1394, V4L
# non available on Fedora: FFMPEG, XINE
mkdir -p build
pushd build
%cmake CMAKE_VERBOSE=1 \
 -DPYTHON_PACKAGES_PATH=%{python_sitearch} \
 -DCMAKE_SKIP_RPATH=ON \
%ifnarch x86_64 ia64
 -DENABLE_SSE=0 \
 -DENABLE_SSE2=0 \
%endif
 %{!?_with_sse3:-DENABLE_SSE3=0} \
 -DCMAKE_BUILD_TYPE=ReleaseWithDebInfo \
 -DBUILD_TEST=1 \
 -DBUILD_opencv_java=0 \
%{?_with_ttb:
%ifarch %{ix86} x86_64 ia64
 -DWITH_TBB=1 -DTBB_LIB_DIR=%{_libdir} \
%endif
} \
 %{?_without_gstreamer:-DWITH_GSTREAMER=0} \
 %{!?_with_ffmpeg:-DWITH_FFMPEG=0} \
 -DBUILD_opencv_nonfree=0 \
%{!?_with_cuda:-DBUILD_opencv_gpu=0} \
%{?_with_cuda: \
 -DCUDA_TOOLKIT_ROOT_DIR=%{?_cuda_topdir} \
 -DCUDA_VERBOSE_BUILD=1 \
 -DCUDA_PROPAGATE_HOST_FLAGS=0 \
} \
%ifarch %{ix86} x86_64
%{?_with_openni: \
 -DWITH_OPENNI=ON \
} \
%endif
 %{!?_with_xine:-DWITH_XINE=0} \
 -DINSTALL_C_EXAMPLES=1 \
 -DINSTALL_PYTHON_EXAMPLES=1 \
 -DENABLE_PRECOMPILED_HEADERS=OFF \
 ..

make VERBOSE=1 %{?_smp_mflags}

popd


%install
rm -rf __devel-doc
pushd build
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" CPPROG="cp -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


rm -f $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/build_all.sh \
      $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/cvsample.dsp \
      $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/cvsample.vcproj \
      $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/facedetect.cmd
install -pm644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/GNUmakefile

# remove unnecessary documentation
rm -rf $RPM_BUILD_ROOT%{_datadir}/OpenCV/doc

popd

#Cmake mess
mkdir -p  $RPM_BUILD_ROOT%{_libdir}/cmake/OpenCV
mv $RPM_BUILD_ROOT%{_datadir}/OpenCV/*.cmake \
  $RPM_BUILD_ROOT%{_libdir}/cmake/OpenCV


%check
# Check fails since we don't support most video
# read/write capability and we don't provide a display
# ARGS=-V increases output verbosity
# Make test is unavailble as of 2.3.1
%if 0
#ifnarch ppc64
pushd build
    LD_LIBRARY_PATH=%{_builddir}/%{tar_name}-%{version}/lib:$LD_LIBARY_PATH make test ARGS=-V || :
popd
%endif


%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig



%files
%doc doc/license.txt
%{_bindir}/opencv_*
%{_libdir}/libopencv_calib3d.so.2.4*
%{_libdir}/libopencv_contrib.so.2.4*
%{_libdir}/libopencv_features2d.so.2.4*
%{_libdir}/libopencv_highgui.so.2.4*
%{_libdir}/libopencv_legacy.so.2.4*
%{_libdir}/libopencv_objdetect.so.2.4*
%{_libdir}/libopencv_stitching.so.2.4*
%{_libdir}/libopencv_ts.so.2.4*
%{_libdir}/libopencv_superres.so.2.4*
%{_libdir}/libopencv_videostab.so.2.4*
%dir %{_datadir}/OpenCV
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files core
%{_libdir}/libopencv_core.so.2.4*
%{_libdir}/libopencv_flann.so.2.4*
%{_libdir}/libopencv_imgproc.so.2.4*
%{_libdir}/libopencv_ml.so.2.4*
%{_libdir}/libopencv_photo.so.2.4*
%{_libdir}/libopencv_video.so.2.4*


%files devel
%{_includedir}/opencv
%{_includedir}/opencv2
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/opencv.pc
# own cmake dir avoiding dep on cmake
%{_libdir}/cmake/


%files devel-docs
%doc doc/*.{htm,png,jpg}
%doc %{_datadir}/OpenCV/samples
%doc %{_datadir}/opencv/samples

%files python
%{python_sitearch}/cv.py*
%{python_sitearch}/cv2.so


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.4.5-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4.5-2
- Mass rebuild 2013-12-27

* Thu May 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.5-1
- Update to 2.4.5-clean
- Spec file clean-up
- Split core libraries into a sub-package

* Sat May 11 2013 François Cami <fcami@fedoraproject.org> - 2.4.4-3
- change project URL.

* Tue Apr 02 2013 Tom Callaway <spot@fedoraproject.org> - 2.4.4-2
- make clean source without SIFT/SURF

* Sat Mar 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-1
- Update to 2.4.4a
- Fix ttb-devel architecture conditionals

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.4-0.2.beta
- rebuild (OpenEXR)

* Mon Feb 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-0.1.beta
- Update to 2.4.4 beta
- Drop python-imaging also from requires
- Drop merged patch for additionals codecs
- Disable the java binding for now (untested)

* Fri Jan 25 2013 Honza Horak <hhorak@redhat.com> - 2.4.3-7
- Do not build with 1394 libs in rhel

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2.4.3-6
- rebuild due to "jpeg8-ABI" feature drop

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-5
- Add more FourCC for gstreamer - rhbz#812628
- Allow to use python-pillow - rhbz#895767

* Mon Nov 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-3
- Switch Build Type to ReleaseWithDebInfo to avoid -03

* Sun Nov 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-2
- Disable SSE3 and allow --with sse3 build conditional.
- Disable gpu module as we don't build cuda
- Update to 2.4.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Honza Horak <hhorak@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Fri Jun 29 2012 Honza Horak <hhorak@redhat.com> - 2.4.1-2
- Fixed cmake script for generating opencv.pc file
- Fixed OpenCVConfig script file

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-1
- Update to 2.4.1
- Rework dependencies - rhbz#828087
  Re-enable using --with tbb,opennpi,eigen2,eigen3

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-8
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-7
- Update gcc46 patch for ARM FTBFS

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 2.3.1-5
- Rebuild for new libpng

* Thu Oct 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for tbb silent ABI change

* Mon Oct 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Update to 2.3.1a

* Mon Sep 26 2011 Dan Horák <dan[at]danny.cz> - 2.3.1-2
- openni is exclusive for x86/x86_64

* Fri Aug 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-1
- Update to 2.3.1
- Add BR openni-devel python-sphinx
- Remove deprecated cmake options
- Add --with cuda conditional (wip)
- Disable make test (unavailable)

* Thu May 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-6
- Backport fixes from branch 2.2 to date

* Tue May 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-5
- Re-enable v4l on f15
- Remove unused cmake options

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-2
- Fix with gcc46
- Disable V4L as V4L1 is disabled for Fedora 15

* Thu Jan 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0
- Disable -msse and -msse2 on x86_32

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.1.0-5
- -devel: include OpenCVConfig.cmake (#627359)

* Thu Jul 22 2010 Dan Horák <dan[at]danny.cz> - 2.1.0-4
- TBB is available only on x86/x86_64 and ia64

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 25 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Move samples from main to -devel
- Fix spurious permission
- Add BR tbb-devel
- Fix CFLAGS

* Fri Apr 23 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Update libdir patch

* Tue Apr 13 2010 Karel Klic <kklic@redhat.com> - 2.0.0-10
- Fix nonstandard executable permissions

* Mon Mar 09 2010 Karel Klic <kklic@redhat.com> - 2.0.0-9
- apply the previously added patch

* Mon Mar 08 2010 Karel Klic <kklic@redhat.com> - 2.0.0-8
- re-enable testing on CMake build system
- fix memory corruption in the gaussian random number generator

* Sat Feb 27 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-7
- replaced BR unicap-devel by libucil-devel (unicap split)

* Thu Feb 25 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-6
- use cmake build system
- applications renamed to opencv_xxx instead of opencv-xxx
- add devel-docs subpackage #546605
- add OpenCVConfig.cmake
- enable openmp build
- enable old SWIG based python wrappers
- opencv package is a good boy and use global instead of define

* Tue Feb 16 2010 Karel Klic <kklic@redhat.com> - 2.0.0-5
- Set CXXFLAXS without -match=i386 for i386 architecture #565074

* Sat Jan 09 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 2.0.0-4
- Updated opencv-samples-Makefile (Thanks Scott Tsai) #553697

* Wed Jan 06 2010 Karel Klic <kklic@redhat.com> - 2.0.0-3
- Fixed spec file issues detected by rpmlint

* Sun Dec 06 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-2
- Fix autotools scripts (missing LBP features) - #544167

* Fri Nov 27 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-1
- Updated to 2.0.0
- Removed upstream-ed patches
- Ugly hack (added cvconfig.h)
- Disable %%check on ppc64

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> - 1.1.0-0.7.pre1
- fix build on s390x where we don't have libraw1394 and devel

* Fri Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.6.pre1
- Fix typo I introduced that prevented build on i386/i586

* Fri Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.5.pre1
- Added 1394 libs and unicap support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.3.pre1
- Build with gstreamer support - #491223
- Backport gcc43 fix from trunk

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.2.pre1
- Fix FTBFS #511705

* Fri Apr 24 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.1.pre1
- Update to 1.1pre1
- Disable CXXFLAGS hardcoded optimization
- Add BR: python-imaging, numpy
- Disable make check failure for now

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 1.0.0-14
- Fix for gcc44
- Enable BR jasper-devel
- Disable ldconfig run on python modules (uneeded)
- Prevent timestamp change on install

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.0.0-12
- fix URL field

* Fri Dec 19 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.0.0-11
- Adopt latest python spec rules.
- Rebuild for Python 2.6 once again.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.0-10
- Rebuild for Python 2.6

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.0-9
- fix license tag

* Sun May 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-8
- Adjust library order in opencv.pc.in (BZ 445937).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-7
- Autorebuild for GCC 4.3

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-6
- Rebuild for gcc43.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0.0-5
- Rebuild for selinux ppc32 issue.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-4
- Mass rebuild.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-3
- Fix %%{_datadir}/opencv/samples ownership.
- Adjust timestamp of cvconfig.h.in to avoid re-running autoheader.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-2
- Move all of the python module to pyexecdir (BZ 233128).
- Activate the testsuite.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-1
- Upstream update.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-4
- Remove python-abi.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.9-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-2
- Stop configure.in from hacking CXXFLAGS.
- Activate testsuite.
- Let *-devel require pkgconfig.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-1
- Upstream update.
- Don't BR: autotools.
- Install samples' Makefile as GNUmakefile.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-18
- Un'%%ghost *.pyo.
- Separate %%{pythondir} from %%{pyexecdir}.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-17
- Rebuild for FC6.
- BR: libtool.

* Fri Mar 17 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-16
- Rebuild.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-15
- Force a re-run of Autotools by calling autoreconf.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-14
- Added build dependency on Autotools.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-13
- Changed intrinsics patch so that it matches upstream.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-12
- More intrinsics patch fixing.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-11
- Don't do "make check" because it doesn't run any tests anyway.
- Back to main intrinsics patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-10
- Using simple intrinsincs patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-9
- Still more fixing of intrinsics patch for Python bindings on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-8
- Again fixed intrinsics patch so that Python modules build on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-7
- Fixed intrinsics patch so that it works.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-6
- Fixed Python bindings location on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-5
- SSE2 support on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-4
- Rebuild

* Sun Oct 16 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-3
- Removed useless sample compilation makefiles/project files and replaced them
  with one that works on Fedora Core.
- Removed shellbang from Python modules.

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-2
- Made FFMPEG dependency optional (needs to be disabled for inclusion in FE).

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-1
- Initial package.
