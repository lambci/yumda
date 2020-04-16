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

# Sources were downloaded using:
# yumdownloader OpenColorIO.x86_64
# And then queried using:
# rpm -qp --qf 'Name: %{name}\n[Requires: %{requires}\n][Conflicts: %{conflicts}\n][Obsoletes: %{obsoletes}\n][Provides: %{provides}\n]' OpenColorIO*.x86_64.rpm | uniq
Source0: OpenColorIO-1.0.9-4.el7.x86_64.rpm

BuildRequires: rpm
BuildRequires: cpio

Prefix: %{_prefix}


%description
OCIO enables color transforms and image display to be handled in a consistent
manner across multiple graphics applications. Unlike other color management
solutions, OCIO is geared towards motion-picture post production, with an
emphasis on visual effects and animation color pipelines.


%install
rm -rf %{buildroot} && mkdir -p %{buildroot}

pushd %{buildroot}
  rpm2cpio %{SOURCE0} | cpio -idm
popd

mv %{buildroot}/usr %{buildroot}%{_prefix}
mv %{buildroot}%{_prefix}/lib64 %{buildroot}%{_libdir}


%files
%license %{_datadir}/doc/OpenColorIO-%{version}/LICENSE
%{_libdir}/*.so.*
%dir %{_datadir}/ocio
%{_datadir}/ocio/setup_ocio.sh

%exclude %{_datadir}
%exclude %{_libdir}/python2.7


%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
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
