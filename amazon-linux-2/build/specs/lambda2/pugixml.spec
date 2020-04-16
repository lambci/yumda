#global prerel rc

Name:           pugixml
Version:        1.8
Release:        1%{?prerel:.%{prerel}}%{?dist}
Summary:        A light-weight C++ XML processing library
Group:          Development/Libraries
License:        MIT
URL:            http://pugixml.org

Source0:        https://github.com/zeux/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake gcc-c++

%description
pugixml is a light-weight C++ XML processing library.
It features:
- DOM-like interface with rich traversal/modification capabilities
- Extremely fast non-validating XML parser which constructs the DOM tree from
  an XML file/buffer
- XPath 1.0 implementation for complex data-driven tree queries
- Full Unicode support with Unicode interface variants and automatic encoding
  conversions


%prep
%setup -q -n %{name}-%{version}%{?prerel:%{prerel}}


%build
rm -rf build && mkdir build && pushd build
export CXXFLAGS='%{optflags} -std=c++11'
%cmake ../
make %{?_smp_mflags}


%install
pushd build
%make_install
popd

if [ -d "%{buildroot}%{_prefix}/lib64" ] && [ "%{_libdir}" != "%{_prefix}/lib64" ]; then
  mv %{buildroot}%{_prefix}/lib64 %{buildroot}%{_libdir}
fi

%files
%license readme.txt
%{_libdir}/*.so.*

%exclude %{_libdir}/*.so
%exclude %{_libdir}/cmake
%exclude %{_datadir}
%exclude %{_includedir}

%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Nov 24 2016 Richard Shaw <hobbes1069@gmail.com> - 1.8-1
- Update to latest upstream release.

* Tue Sep 27 2016 Richard Shaw <hobbes1069@gmail.com> - 1.7-3
- Add build flags for c++11 for mkvtoolnix.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Richard Shaw <hobbes1069@gmail.com> - 1.7-1
- Update to latest upstream release.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Richard Shaw <hobbes1069@gmail.com> - 1.6-1
- Update to latest upstream release.

* Tue Feb  3 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5-1
- Update to latest upstream release.

* Wed Sep 03 2014 Orion Poplawski <orion@cora.nwra.com> - 1.4-1
- Update to 1.4
- Split documentation out into -doc sub-package
- Add cmake export information

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jan 05 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0-2
- Rebuild for GCC 4.7.0.

* Fri Jul 08 2011 Richard Shaw <hobbes1069@gmail.com> - 1.0-1
- Initial Release
