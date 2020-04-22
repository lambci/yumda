# Filter provides from Python libraries
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

# Use cmake28 package on EL builds.
%if 0%{?rhel} && 0%{?rhel} <= 6
%global cmake %cmake28 -DCMAKE_SKIP_RPATH=OFF
%endif

Name:           OpenColorIO
Version:        1.0.9
Release:        4%{?dist}
Summary:        Enables color transforms and image display across graphics apps

License:        BSD
URL:            http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.9
Source0:        %{name}-%{version}.tar.gz
Patch0:         OpenColorIO-yaml_cpp3.patch

# Utilities
%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:  cmake28
%else
BuildRequires:  cmake
%endif
BuildRequires:  help2man
BuildRequires:  python-markupsafe

# Libraries
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  libX11-devel libXmu-devel libXi-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  zlib-devel

#######################
# Unbundled libraries #
#######################
BuildRequires:  tinyxml-devel
BuildRequires:  lcms2-devel
BuildRequires:  yaml-cpp03-devel >= 0.3.0

# The following bundled projects are only used for document generation.
#BuildRequires:  python-docutils
#BuildRequires:  python-jinja2
#BuildRequires:  python-pygments
#BuildRequires:  python-setuptools
#BuildRequires:  python-sphinx

Prefix: %{_prefix}

%description
OCIO enables color transforms and image display to be handled in a consistent
manner across multiple graphics applications. Unlike other color management
solutions, OCIO is geared towards motion-picture post production, with an
emphasis on visual effects and animation color pipelines.


%prep
%setup -q
%patch0 -p1 -b .yaml3

# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*


%build
rm -rf build && mkdir build && pushd build
%cmake -DOCIO_BUILD_STATIC=OFF \
       -DOCIO_BUILD_DOCS=OFF \
       -DOCIO_BUILD_TESTS=OFF \
       -DOCIO_PYGLUE_SONAME=OFF \
       -DUSE_EXTERNAL_YAML=TRUE \
       -DUSE_EXTERNAL_TINYXML=TRUE \
       -DUSE_EXTERNAL_LCMS=TRUE \
       -DOCIO_BUILD_PYGLUE=OFF \
       -DOCIO_BUILD_APPS=OFF \
       ../

make %{?_smp_mflags}


%install
pushd build
%make_install

%files
%license LICENSE
%{_libdir}/*.so.*
%dir %{_datadir}/ocio
%{_datadir}/ocio/setup_ocio.sh

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Wed Apr 22 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Oct 04 2016 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-4.1
- Rebuild for updated OpenImageIO.

* Wed Jul 20 2016 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-3.el7.1
- Rebuild for updatd OpenImageIO 1.5.22.

* Wed May 21 2014 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-3
- Rebuild for updated OpenImageIO 1.4.7.

* Mon Jan 13 2014 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-2
- Add OpenImageIO as build requirement to build additional command line tools.
  Fixes BZ#1038860.

* Wed Nov  6 2013 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-1
- Update to latest upstream release.

* Mon Sep 23 2013 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-6
- Rebuild against yaml-cpp03 compatibility package.

* Mon Aug 26 2013 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-5
- Fix for new F20 feature, unversion doc dir. Fixes BZ#1001264

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-1
- Update to latest upstream release.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-4
- Only use SSE instructions on x86_64.

* Wed Apr 25 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-3
- Misc spec cleanup for packaging guidelines.
- Disable testing for now since it fails on the build servers.

* Wed Apr 18 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-1
- Latest upstream release.

* Thu Apr 05 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.6-1
- Latest upstream release.

* Wed Nov 16 2011 Richard Shaw <hobbes1069@gmail.com> - 1.0.2-1
- Initial release.
