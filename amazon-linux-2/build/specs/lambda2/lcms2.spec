Name:           lcms2
Version:        2.6
Release: 3%{?dist}.0.2
Summary:        Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/
Source0:        http://www.littlecms.com/lcms2-2.6.tar.gz
Patch0:		endianness.patch
Patch1:         test_library_path.patch

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel

Prefix: %{_prefix}

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package        utils
Summary:        Utility applications for %{name}
Group:          Applications/Productivity
Requires:       %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description    utils
The %{name}-utils package contains utility applications for %{name}.

%prep
%setup -q -n lcms2-2.6
%patch0 -p1
%patch1

%build
export CFLAGS='-fno-strict-aliasing %optflags'
%configure --disable-static --program-suffix=2

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/*.so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_datadir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Oct 16 2015 Andrew Hughes <gnu.andrew@redhat.com> - 2.6-3
- Run tests as part of %%check, fixing Makefile to set LD_LIBRARY_PATH
- Use upstream endianness fix to avoid ppc64le being built big-endian
- Resolves: #1250914

* Tue May 26 2015 Matthias Clasen <mclasen@redhat.com> 2.6-2
- Build with -fno-strict-aliasing
Related: #1174406

* Tue Mar 17 2015 Richard Hughes <richard@hughsie.com> 2.6-1
 Update to new upstream version.
 Resolves: #1174406

* Thu Aug 14 2014 Richard Hughes <rhughes@redhat.com> - 2.5-5
- Backport a patch for ppc64le support, many thanks to Tim Waugh.
- Resolves: #1125723

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.5-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.5-3
- Mass rebuild 2013-12-27

* Tue Oct  8 2013 Matthias Clasen <mclasen@redhat.com> 2.5-2
- Disable strict aliasing (related: #884068)

* Mon Jul 01 2013 Richard Hughes <richard@hughsie.com> 2.5-1
- Update to new upstream version.
- Added a reference for Mac MLU tag
- Added a way to read the profile creator from header
- Added error descriptions on cmsSmoothToneCurve
- Added identity curves support for write V2 LUT
- Added new cmsPlugInTHR() and fixed some race conditions
- Added TIFF Lab16 handling on tifficc
- Fixed a bug on big endian platforms not supporting uint64 or long long.
- Fixed a multithead bug on optimization
- Fixed devicelink generation for 8 bits
- Fixed some 64 bit warnings on size_t to uint32 conversions
- Rendering intent used when creating the transform is now propagated to profile
- RGB profiles store only one copy of the curve to save space
- Transform2Devicelink now keeps white point when guessing deviceclass is enabled
- Update black point detection algorithm to reflect ICC changes
- User defined parametric curves can now be saved in ICC profiles

* Thu Apr 25 2013 Tim Waugh <twaugh@redhat.com> - 2.4-6
- Applied upstream fixes for threading (bug #951984).

* Thu Mar  7 2013 Tim Waugh <twaugh@redhat.com> - 2.4-5
- Added upstream fix for threading issue with plugin registration
  (bug #912307).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.4-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.4-2
- rebuild against new libjpeg

* Sat Sep 15 2012 Richard Hughes <richard@hughsie.com> 2.4-1
- Update to new upstream version.
- Black point detection from the algorithm disclosed by Adobe
- Added support for transforms on planar data with different stride
- Added a new plug-in type for optimizing full transforms
- Linear (gamma 1.0) profiles can now operate in unbounded mode
- Added "half" float support

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.3-1
- Update to new upstream version which incorporates many bugfixes.

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.2-2
- Actually update the sources...

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.2-1
- Update to new upstream version
- Stability and efficienty fixes
- Adds support for dictionary metatag

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Richard Hughes <richard@hughsie.com> 2.1-1
- Update to new upstream version.

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-3
- Address some more review comments.
- Resolves #590387

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-2
- Address some review comments.
- Resolves #590387

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-1
- Initial package for Fedora review
