%global use_git 0

%global commit  d4cd34fd49caa759cf01cafa5fa271401b17c3b9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global srcname Vulkan-LoaderAndValidationLayers

%global commit1 3a21c880500eac21cdf79bef5b80f970a55ac6af
%global srcname1 glslang

%global commit2 2bb92e6fe2c6aa410152fc6c63443f452acb1a65
%global srcname2 SPIRV-Headers

%global commit3 7e2d26c77b606b21af839b37fd21381c4a669f23
%global srcname3 SPIRV-Tools

Name:           vulkan
Version:        1.0.61.1
%if 0%{?use_git}
Release:        0.1.git%{shortcommit}%{?dist}
%else
Release:        2%{?dist}
%endif
Summary:        Vulkan loader and validation layers

License:        ASL 2.0
URL:            https://github.com/KhronosGroup

%if 0%{?use_git}
Source0:        %url/%{srcname}/archive/%{commit}.tar.gz#/%{srcname}-%{commit}.tar.gz
%else
Source0:        %url/%{srcname}/archive/sdk-%{version}.tar.gz#/%{srcname}-sdk-%{version}.tar.gz
%endif
Source1:        %url/%{srcname1}/archive/%{commit1}.tar.gz#/%{srcname1}-%{commit1}.tar.gz
Source2:        %url/%{srcname2}/archive/%{commit2}.tar.gz#/%{srcname2}-%{commit2}.tar.gz
Source3:        %url/%{srcname3}/archive/%{commit3}.tar.gz#/%{srcname3}-%{commit3}.tar.gz

Patch0:         0003-layers-Don-t-set-an-rpath.patch
Patch1:         0008-demos-Don-t-build-tri-or-cube.patch
Patch2:		hacked-python2.patch
Patch3:		no-smoke-demo.patch
Patch4:		0001-loader-Fix-TEXTREL-on-32-bit-linux-loader.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  /usr/bin/chrpath
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(pciaccess)
%if 0%{?fedora}
BuildRequires:  python3
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
%else
BuildRequires:  python
%endif
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xrandr)

Requires:       vulkan-filesystem = %{version}-%{release}

%if 0%{?fedora}
Recommends:     mesa-vulkan-drivers
%endif

Prefix: %{_prefix}

%description
Vulkan is a new generation graphics and compute API that provides
high-efficiency, cross-platform access to modern GPUs used in a wide variety of
devices from PCs and consoles to mobile phones and embedded platforms.

This package contains the reference ICD loader and validation layers for
Vulkan.

%package filesystem
Summary:        Vulkan filesystem package
BuildArch:      noarch
Prefix: %{_prefix}

%description filesystem
Filesystem for Vulkan.

%prep
%if 0%{?use_git}
%autosetup -p1 -n %{srcname}-%{commit}
%else
%autosetup -p1 -n %{srcname}-sdk-%{version}
%endif

mkdir -p build/ external/glslang/build/install external/spirv-tools/build/ external/spirv-tools/external/spirv-headers
tar -xf %{SOURCE1} -C external/glslang --strip 1
tar -xf %{SOURCE2} -C external/spirv-tools/external/spirv-headers --strip 1
tar -xf %{SOURCE3} -C external/spirv-tools --strip 1
# fix spurious-executable-perm
chmod 0644 README.md
chmod 0644 external/glslang/SPIRV/spirv.hpp
chmod +x scripts/lvl_genvk.py
# fix wrong-script-end-of-line-encoding
sed -i 's/\r//' README.md

# sigh inttypes
sed -i 's/inttypes.h/cinttypes/' layers/*.{cpp,h}

%build
pushd external/glslang/build/
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS ; 
CXXFLAGS="$RPM_OPT_FLAGS" ; export CXXFLAGS ; 
LDFLAGS="$RPM_LD_FLAGS" ; export LDFLAGS ;
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=./install -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON ..
%make_build
make install
popd

pushd external/spirv-tools/build/
cmake -DSPIRV_WERROR=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON ..
%make_build
popd

pushd build/
%cmake -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=yes \
       -DCMAKE_SKIP_RPATH:BOOL=yes \
       -DBUILD_VKJSON=OFF \
       -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_datadir} \
       -DBUILD_WSI_MIR_SUPPORT=OFF \
%if 0%{?rhel}
       -DBUILD_WSI_WAYLAND_SUPPORT=OFF \
%endif
 ..
%make_build
popd

%install
pushd build/
%{make_install}
popd

%if "%{_lib}" != "lib64"
  mv $RPM_BUILD_ROOT%{_prefix}/lib64 $RPM_BUILD_ROOT%{_libdir}
%endif

# create the filesystem
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}%{_datadir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}{%{_sysconfdir},%{_datadir}}/vulkan/icd.d

# remove RPATH
chrpath -d %{buildroot}%{_bindir}/vulkaninfo

%files
%license LICENSE.txt COPYRIGHT.txt
%{_bindir}/vulkaninfo
%{_datadir}/vulkan/explicit_layer.d/*.json
%{_libdir}/libVkLayer_*.so
%{_libdir}/libvulkan.so.*

%files filesystem
%dir %{_sysconfdir}/vulkan/
%dir %{_sysconfdir}/vulkan/explicit_layer.d/
%dir %{_sysconfdir}/vulkan/icd.d/
%dir %{_sysconfdir}/vulkan/implicit_layer.d/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/vulkan/explicit_layer.d/
%dir %{_datadir}/vulkan/icd.d/
%dir %{_datadir}/vulkan/implicit_layer.d/

%exclude %{_includedir}
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/libvulkan.so

%changelog
* Fri Nov 1 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Oct 10 2017 Dave Airlie <airlied@redhat.com> - 1.0.61.1-2
- fix 32-bit textrels

* Thu Sep 21 2017 Dave Airlie <airlied@redhat.com> - 1.0.61.1-1
- Update to 1.0.61.1 release
- bring spec updates in from Fedora spec.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.39.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.39.1-1
- Update to 1.0.39.1 release

* Tue Jan 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.39.0-1
- Update to 1.0.39.0 release
- Add build requires libXrandr-devel

* Fri Dec 16 2016 leigh scott <leigh123linux@googlemail.com> - 1.0.37.0-1
- Update to 1.0.37.0 release
- Disable Mir as it's lame ubuntu rubbish

* Fri Dec 02 2016 leigh scott <leigh123linux@googlemail.com> - 1.0.34.0-0.1.gitd4cd34f
- Update to latest git

* Thu Dec 01 2016 leigh scott <leigh123linux@googlemail.com> - 1.0.30.0-2
- Fix VkLayer undefined symbol: util_GetExtensionProperties

* Sat Oct 15 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.30.0-1
- Update to 1.0.30.0 release

* Mon Oct 10 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-4
- Build with wayland support (rhbz 1383115)

* Tue Sep 27 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-3
- Move unversioned libraries
- Disable vkjson build
- Fix license tag

* Sun Sep 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-2
- Make layers conditional. 

* Sun Sep 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-1
- Update to 1.0.26.0 release

* Thu Sep 08 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-0.3.gitfbb8667
- Clean up

* Thu Sep 08 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-0.2.gitfbb8667
- Change build requires python3
- Use release for cmake
- Make build verbose

* Wed Sep 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.26.0-0.1.gitfbb8667
- Update to latest git

* Tue Feb 16 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.3-0.1.git1affe90
- Add ldconfig in post/postun
- Use upstream tarball from commit + patches
- Fix versioning. In fact it was never released
- Fixup mixing of spaces/tabs
- Remove rpath from vulkaninfo
- Make filesystem subpkg noarch (it is really noarch)
- BuildRequire gcc and gcc-c++ explicitly
- Require main pkg with isa tag
- Fix perms and perm of README.md
- Use %%license tag

* Tue Feb 16 2016 Adam Jackson <ajax@redhat.com> - 1.0.3-0
- Update loader to not build cube or tri. Drop bundled LunarGLASS and llvm
  since they're only needed for those demos.

* Tue Feb 16 2016 Adam Jackson <ajax@redhat.com> - 1.0.3-0
- Initial packaging
