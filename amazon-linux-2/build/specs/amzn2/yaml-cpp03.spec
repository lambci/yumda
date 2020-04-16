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

%description
yaml-cpp is a YAML parser and emitter in C++ written around the YAML 1.2 spec.

This is a compatibility package for version 0.3.


%package        devel
Summary:        Development files for %{name}
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       boost-devel

Provides:       yaml-cpp-devel = %{version}-%{release}
Obsoletes:      yaml-cpp-devel < 0.3.0-5

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

This is a compatibility package for version 3.


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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc license.txt
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Oct 30 2013 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-4
- Change package name to yaml-cpp03 per reviewer input.

* Wed Sep  4 2013 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-3
- Add obsoletes/provides for proper upgrade path.
- Fix internal header references to yaml-cpp3.
- Fix pkg-config file to reference yaml-cpp3.

* Mon Aug 26 2013 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-1
- Initial packaging.
