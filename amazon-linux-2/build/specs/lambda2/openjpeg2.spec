# Conformance tests disabled by default since it requires 1 GB of test data
#global runcheck 1

#global optional_components 1

Name:           openjpeg2
Version:        2.3.1
Release:        1%{?dist}
Summary:        C-Library for JPEG 2000

# windirent.h is MIT, the rest is BSD
License:        BSD and MIT
URL:            https://github.com/uclouvain/openjpeg
Source0:        https://github.com/uclouvain/openjpeg/archive/v%{version}/openjpeg-%{version}.tar.gz
%if 0%{?runcheck}
# git clone git@github.com:uclouvain/openjpeg-data.git
Source1:        data.tar.xz
%endif

# Remove bundled libraries
Patch0:         openjpeg2_remove-thirdparty.patch
# Rename tool names to avoid conflicts with openjpeg-1.x
Patch1:         openjpeg2_opj2.patch


BuildRequires:  cmake
# The library itself is C only, but there is some optional C++ stuff, hence the project is not marked as C-only in cmake and hence cmake looks for a c++ compiler
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  lcms2-devel
BuildRequires:  doxygen

%if 0%{?optional_components}
BuildRequires:  java-devel
BuildRequires:  xerces-j2
%endif

Prefix: %{_prefix}

%description
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains
* JPEG 2000 codec compliant with the Part 1 of the standard (Class-1 Profile-1
  compliance).
* JP2 (JPEG 2000 standard Part 2 - Handling of JP2 boxes and extended multiple
  component transforms for multispectral and hyperspectral imagery)


%package tools
Summary:        OpenJPEG 2 command line tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Command line tools for JPEG 2000 file manipulation, using OpenJPEG2:
 * opj2_compress
 * opj2_decompress
 * opj2_dump


%prep
%autosetup -p1 -n openjpeg-%{version} %{?runcheck:-a 1}

# Remove all third party libraries just to be sure
rm -rf thirdparty


%build
mkdir %{_target_platform}
pushd %{_target_platform}
# TODO: Consider
# -DBUILD_JPIP_SERVER=ON -DBUILD_JAVA=ON
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPENJPEG_INSTALL_LIB_DIR=%{_lib} \
    %{?optional_components:-DBUILD_MJ2=ON -DBUILD_JPWL=ON -DBUILD_JPIP=ON -DBUILD_JP3D=ON} \
    -DBUILD_DOC=ON \
    -DBUILD_STATIC_LIBS=OFF \
    -DBUILD_SHARED_LIBS=ON \
    %{?runcheck:-DBUILD_TESTING:BOOL=ON -DOPJ_DATA_ROOT=$PWD/../data} \
    ..
popd

%make_build VERBOSE=1 -C %{_target_platform}


%install
%make_install -C %{_target_platform}

mv %{buildroot}%{_mandir}/man1/opj_compress.1 %{buildroot}%{_mandir}/man1/opj2_compress.1
mv %{buildroot}%{_mandir}/man1/opj_decompress.1 %{buildroot}%{_mandir}/man1/opj2_decompress.1
mv %{buildroot}%{_mandir}/man1/opj_dump.1 %{buildroot}%{_mandir}/man1/opj2_dump.1

# Docs are installed through %%doc
rm -rf %{buildroot}%{_datadir}/doc/


%files
%license LICENSE
%{_libdir}/libopenjp2.so.*

%files tools
%{_bindir}/opj2_compress
%{_bindir}/opj2_decompress
%{_bindir}/opj2_dump
%{_mandir}/man1/opj2_compress.1*
%{_mandir}/man1/opj2_decompress.1*
%{_mandir}/man1/opj2_dump.1*

%exclude %{_mandir}
%exclude %{_includedir}/openjpeg-2.3/
%exclude %{_libdir}/*.so
%exclude %{_libdir}/openjpeg-2.3/
%exclude %{_libdir}/pkgconfig


%changelog
* Fri Jul 24 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Apr 02 2019 Sandro Mani <manisandro@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 20 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-10
- Backport patches for CVE-2018-18088, CVE-2018-6616

* Thu Oct 04 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-9
- Backport patch for CVE-2018-5785 (#1537758)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-7
- BR: gcc-c++

* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.com> - 2.3.0-6
- Add missing BR: gcc, make

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.0-4
- Switch to %%ldconfig_scriptlets

* Mon Dec 25 2017 Sandro Mani <manisandro@gmail.com> - 2.3.0-3
- Rename tool names at cmake level to ensure OpenJPEGTargets.cmake refers to the renamed files

* Mon Dec 25 2017 Sandro Mani <manisandro@gmail.com> - 2.3.0-2
- Use BUILD_STATIC_LIBS=OFF instead of deleting the static library after build

* Thu Oct 05 2017 Sandro Mani <manisandro@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Thu Sep 07 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-4
- Backport fix for CVE-2017-14039

* Thu Aug 31 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-3
- Backport more security fixes, including for CVE-2017-14041 and CVE-2017-14040

* Thu Aug 31 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-2
- Backport patch for CVE-2017-12982

* Thu Aug 10 2017 Sandro Mani <manisandro@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 17 2016 Sandro Mani <manisandro@gmail.com> - 2.1.2-3
- Add patch for CVE-2016-9580 (#1405128) and CVE-2016-9581 (#1405135)

* Thu Dec 08 2016 Sandro Mani <manisandro@gmail.com> - 2.1.2-2
- Add patch for CVE-2016-9572 (#1402714) and CVE-2016-9573 (#1402711)

* Wed Sep 28 2016 Sandro Mani <manisandro@gmail.com> - 2.1.2-1
- Update to 2.1.2
- Fixes: CVE-2016-7445

* Fri Sep 09 2016 Sandro Mani <manisandro@gmail.com> - 2.1.1-3
- Backport: Add sanity check for tile coordinates (#1374337)

* Fri Sep 09 2016 Sandro Mani <manisandro@gmail.com> - 2.1.1-2
- Backport fixes for CVE-2016-7163

* Wed Jul 06 2016 Sandro Mani <manisandro@gmail.com> - 2.1.1-1
- Update to 2.1.1
- Fixes: CVE-2016-3183, CVE-2016-3181, CVE-2016-3182, CVE-2016-4796, CVE-2016-4797, CVE-2015-8871

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 01 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-7
- Backport fix for possible double-free (#1267983)

* Tue Sep 15 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-6
- Backport fix for use after free vulnerability (#1263359)

* Thu Jun 25 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-5
- Add openjpeg2_bigendian.patch (#1232739)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Sandro Mani <manisandro@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Wed Apr 16 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-5
- Switch to official 2.0 release and backport pkg-config patch

* Thu Apr 10 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-4.svn20140403
- Replace define with global
- Fix #define optional_components 1S typo
- Fix %%(pwd) -> $PWD for test data
- Added some BR for optional components
- Include opj2_jpip_viewer.jar in %%files

* Wed Apr 09 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-3.svn20140403
- Fix source url
- Fix mixed tabs and spaces
- Fix description too long

* Wed Apr 09 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-2.svn20140403
- Remove thirdparty libraries folder in prep
- Own %%{_libdir}/openjpeg-2.0/
- Fix Requires
- Add missing ldconfig
- Add possibility to run conformance tests if desired
 
* Thu Apr 03 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-1.svn20140403
- Initial package
