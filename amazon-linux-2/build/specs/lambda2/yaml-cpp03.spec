%global realname yaml-cpp

Name:           yaml-cpp03
Version:        0.3.0
Release:        4%{?dist}
Summary:        A YAML parser and emitter for C++
License:        MIT 
URL:            http://code.google.com/p/yaml-cpp/
Source0:        http://yaml-cpp.googlecode.com/files/%{realname}-%{version}.tar.gz

Patch0:         yaml-cpp03-pkgconf.patch

BuildRequires:  cmake

Provides:       yaml-cpp = %{version}-%{release}
Obsoletes:      yaml-cpp < 0.3.0-5

Prefix: %{_prefix}

%description
yaml-cpp is a YAML parser and emitter in C++ written around the YAML 1.2 spec.

This is a compatibility package for version 0.3.


%prep
%setup -q -n %{realname}
%patch0 -p1 -b .pkgconf

# Fix eol 
sed -i 's/\r//' license.txt


%build
# ask cmake to not strip binaries
%cmake . -DYAML_CPP_BUILD_TOOLS=0
make VERBOSE=1 %{?_smp_mflags}


%install
%make_install
#find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Move things as to not conflict with the main package
mv %{buildroot}%{_includedir}/yaml-cpp %{buildroot}%{_includedir}/%{name}
mv %{buildroot}%{_libdir}/libyaml-cpp.so %{buildroot}%{_libdir}/lib%{name}.so
mv %{buildroot}%{_libdir}/pkgconfig/yaml-cpp.pc \
   %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Correct paths in yaml headers
for header in %{buildroot}%{_includedir}/%{name}/*.h; do
    sed -i "s|#include \"yaml-cpp|#include \"%{name}|g" $header
done


%files
%license license.txt
%{_libdir}/*.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Thu Apr 16 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Oct 30 2013 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-4
- Change package name to yaml-cpp03 per reviewer input.

* Wed Sep  4 2013 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-3
- Add obsoletes/provides for proper upgrade path.
- Fix internal header references to yaml-cpp3.
- Fix pkg-config file to reference yaml-cpp3.

* Mon Aug 26 2013 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-1
- Initial packaging.
