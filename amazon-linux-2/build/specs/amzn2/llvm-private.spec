%global maj_ver 6
%global min_ver 0
%global patch_ver 1

# Components enabled if supported by target architecture:
%ifarch %ix86 x86_64
  %bcond_without gold
%else
  %bcond_with gold
%endif

%if 0%{?rhel} == 6
%define rhel6 1
%endif

# llvm works on the 64-bit versions of these, but not the 32 versions.
# consequently we build swrast on them instead of llvmpipe.
ExcludeArch: ppc s390 %{?rhel6:s390x}

%ifarch s390x
%global host_target SystemZ
%endif
%ifarch ppc64 ppc64le
%global host_target PowerPC
# Limit build jobs on ppc64 systems to avoid running out of memory.
%global _smp_mflags -j8
%endif
%ifarch %ix86 x86_64
%global host_target X86
%endif
%ifarch aarch64
%global host_target AArch64
%endif
%ifarch %{arm}
%global host_target ARM
%endif

%ifnarch s390x
%global amdgpu ;AMDGPU
%endif

%global llvm_lib_suffix rhel

Name:		llvm-private
Version:	%{maj_ver}.%{min_ver}.%{patch_ver}
Release:	2%{?dist}
Summary:	llvm engine for Mesa

Group:          System Environment/Libraries
License:	NCSA
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/llvm-%{version}%{?rc_ver:rc%{rc_ver}}.src.tar.xz
Source1:        cmake-3.4.3.tar.gz
Source2:	http://llvm.org/releases/%{version}/cfe-%{version}%{?rc_ver:rc%{rc_ver}}.src.tar.xz
Source100:	llvm-config.h
Source101:	clang-config.h

Patch1: 0001-Fix-CMake-include-patch.patch
Patch5: 0001-Export-LLVM_DYLIB_COMPONENTS-in-LLVMConfig.cmake.patch
Patch6: 0001-Don-t-run-BV-DAG-Combine-before-legalization-if-it-a.patch

BuildRequires:	cmake
BuildRequires:	zlib-devel
%if %{with gold}
BuildRequires:  binutils-devel
%endif
BuildRequires:  python

%description
This package contains the LLVM-based runtime support for Mesa.  It is not a
fully-featured build of LLVM, and use by any package other than Mesa is not
supported.

%package devel
Summary:	Libraries and header files for LLVM
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains library and header files needed to build the LLVM
support in Mesa.

%prep
%setup -T -q -b 2 -n cfe-%{version}%{?rc_ver:rc%{rc_ver}}.src

%setup -q -n llvm-%{version}%{?rc_ver:rc%{rc_ver}}.src

tar xf %{SOURCE1}

%patch1 -p1 -b .fixinc
%patch5 -p1 -b .cmake-fix
%patch6 -p1 -b .p9-fix

%build

BUILD_DIR=`pwd`/cmake_build
cd cmake-3.4.3
cmake . -DCMAKE_INSTALL_PREFIX=$BUILD_DIR
make
make install
cd -


sed -i 's|ActiveIncludeDir = ActivePrefix + "/include|&/llvm-private|g' tools/llvm-config/llvm-config.cpp

mkdir -p _build
cd _build

export PATH=$BUILD_DIR/bin:$PATH
%global __cmake $BUILD_DIR/bin/cmake
# force off shared libs as cmake macros turns it on.
%cmake .. \
	-DINCLUDE_INSTALL_DIR=%{_includedir}/llvm-private \
	-DLLVM_VERSION_SUFFIX="-%{llvm_lib_suffix}" \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if 0%{?__isa_bits} == 64
	-DLLVM_LIBDIR_SUFFIX=64 \
%else
	-DLLVM_LIBDIR_SUFFIX= \
%endif
	\
	-DLLVM_TARGETS_TO_BUILD="%{host_target}%{?amdgpu};BPF" \
	-DLLVM_ENABLE_LIBCXX:BOOL=OFF \
	-DLLVM_ENABLE_ZLIB:BOOL=ON \
	-DLLVM_ENABLE_FFI:BOOL=OFF \
	-DLLVM_ENABLE_RTTI:BOOL=OFF \
%if %{with gold}
	-DLLVM_BINUTILS_INCDIR=%{_includedir} \
%endif
	\
	-DLLVM_BUILD_RUNTIME:BOOL=ON \
	\
	-DLLVM_INCLUDE_TOOLS:BOOL=ON \
	-DLLVM_BUILD_TOOLS:BOOL=ON \
	\
	-DLLVM_INCLUDE_TESTS:BOOL=ON \
	-DLLVM_BUILD_TESTS:BOOL=ON \
	\
	-DLLVM_INCLUDE_EXAMPLES:BOOL=OFF \
	-DLLVM_BUILD_EXAMPLES:BOOL=OFF \
	\
	-DLLVM_INCLUDE_UTILS:BOOL=ON \
	-DLLVM_INSTALL_UTILS:BOOL=OFF \
	\
	-DLLVM_INCLUDE_DOCS:BOOL=OFF \
	-DLLVM_BUILD_DOCS:BOOL=OFF \
	-DLLVM_ENABLE_SPHINX:BOOL=OFF \
	-DLLVM_ENABLE_DOXYGEN:BOOL=OFF \
	\
	-DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
	-DLLVM_DYLIB_EXPORT_ALL:BOOL=ON \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_BUILD_EXTERNAL_COMPILER_RT:BOOL=ON \
	-DLLVM_INSTALL_TOOLCHAIN_ONLY:BOOL=OFF

make %{?_smp_mflags} VERBOSE=1 LLVM llvm-config FileCheck not count gtest gtest_main

# Build clang separately, because we need to build with
# -DBUILD_SHARED_LIBS:BOOL=ON for clang, but we don't want
# this for LLVM.

cd ../../cfe-%{version}%{?rc_ver:rc%{rc_ver}}.src
mkdir -p _build
cd _build
%cmake ..  \
        -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DLLVM_CONFIG:FILEPATH=%{_builddir}/llvm-%{version}%{?rc_ver:rc%{rc_ver}}.src/_build/bin/llvm-config \
        \
        -DCLANG_ENABLE_ARCMT:BOOL=ON \
        -DCLANG_ENABLE_STATIC_ANALYZER:BOOL=ON \
        -DCLANG_INCLUDE_DOCS:BOOL=OFF \
        -DCLANG_INCLUDE_TESTS:BOOL=ON \
        -DCLANG_PLUGIN_SUPPORT:BOOL=ON \
        -DENABLE_LINKER_BUILD_ID:BOOL=ON \
        \
        -DCLANG_BUILD_EXAMPLES:BOOL=OFF \
%if 0%{?__isa_bits} == 64
        -DLLVM_LIBDIR_SUFFIX=64 \
%else
        -DLLVM_LIBDIR_SUFFIX= \
%endif
        -DLIB_SUFFIX=

make %{?_smp_mflags}

%install

# Install LLVM
cd _build
make install-LLVM install-llvm-config install-llvm-headers install-cmake-exports DESTDIR=%{buildroot}

cd ../../cfe-%{version}%{?rc_ver:rc%{rc_ver}}.src/_build
make install DESTDIR=%{buildroot}


# fix multi-lib
mv -v %{buildroot}%{_bindir}/llvm-config %{buildroot}%{_bindir}/%{name}-config-%{__isa_bits}
mv -v %{buildroot}%{_includedir}/llvm-private/llvm/Config/llvm-config{,-%{__isa_bits}}.h
install -m 0644 %{SOURCE100} %{buildroot}%{_includedir}/llvm-private/llvm/Config/llvm-config.h
mv -v %{buildroot}%{_includedir}/clang/Config/config{,-%{__isa_bits}}.h
install -m 0644 %{SOURCE101} %{buildroot}%{_includedir}/clang/Config/config.h

rm -f %{buildroot}%{_libdir}/*.a

rm -f %{buildroot}%{_libdir}/libLLVM.so

# remove documentation makefiles:
# they require the build directory to work
find examples -name 'Makefile' | xargs -0r rm -f

# RHEL: strip out most binaries, most libs, and man pages
ls %{buildroot}%{_bindir}/* | grep -v bin/llvm-private | xargs rm -f
ls %{buildroot}%{_libdir}/* | grep -v libLLVM | grep -v libclang | xargs rm -f
rm -rf %{buildroot}%{_mandir}/man1

# RHEL: Strip out some headers Mesa doesn't need
rm -rf %{buildroot}%{_includedir}/llvm-private/llvm/{Assembly}
rm -rf %{buildroot}%{_includedir}/llvm-private/llvm/TableGen
rm -rf %{buildroot}%{_includedir}/llvm-c/lto.h

# RHEL: Strip out cmake build foo
rm -rf %{buildroot}%{_datadir}/llvm/cmake
rm -rf %{buildroot}%{_libdir}/cmake/llvm/LLVMExports-*
rm -rf %{buildroot}%{_libdir}/cmake/clang

# RHEL: Strip out eveything in _datadir and _libexedir
rm -rf %{buildroot}%{_datadir}/*
rm -rf %{buildroot}%{_libexecdir}/*

# clang seems to ignore INCLUDE_INSTALL_DIR
mv %{buildroot}%{_includedir}/{,llvm-private}/clang
mv %{buildroot}%{_includedir}/{,llvm-private}/clang-c

# Move clang libraries:
mkdir %{buildroot}%{_libdir}/clang-private
for f in `find %{buildroot}%{_libdir} -iname 'libclang*' `; do mv $f %{buildroot}%{_libdir}/clang-private; done

%check
cd _build
make %{?_smp_mflags} check-all || :

cd ../../cfe-%{version}%{?rc_ver:rc%{rc_ver}}.src/_build
make %{?_smp_mflags} check-all

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.TXT
%{_libdir}/libLLVM-%{maj_ver}.%{min_ver}*-%{llvm_lib_suffix}.so
%{_libdir}/clang-private/libclang*.so*

%files devel
%{_bindir}/llvm-private*
%{_includedir}/llvm-private/llvm
%{_includedir}/llvm-private/llvm-c
%{_libdir}/cmake/llvm/
%{_includedir}/llvm-private/clang
%{_includedir}/llvm-private/clang-c
%{_libdir}/clang/%{version}/include

%changelog
* Thu Jul 19 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-2
- Fix crash on power9
- Resolves: rhbz#1595996

* Mon Jul 09 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-1
- 6.0.1 Release

* Thu Jun 07 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.4.rc2
- 6.0.1-rc2 Release

* Wed Jun 06 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.3.rc1
- Fixup cmake files so bcc can use them

* Thu May 31 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.2.rc1
- Keep cmake files in package, because bcc needs them

* Wed Apr 04 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-0.1.rc1
- Rebase to LLVM 6.0.1-rc1

* Thu Dec 14 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-3
- Backport r312612 from upstream llvm: [PowerPC] Don't use xscvdpspn on the P7

* Thu Oct 19 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-2
- Enable BPF target

* Thu Oct 12 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-1
- Update to 5.0.0

* Thu Jun 01 2017 Tilmann Scheller <tschelle@redhat.com> - 3.9.1-9
- Fix two Clang test failures and enable Clang regression tests during build.

* Mon May 08 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-8
- Fix clang headers with multilib.

* Fri Apr 07 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-7
- Add clang libs

* Mon Mar 27 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-6
- Ignore test failures due APFloat unit test failure on AArch64.

* Mon Feb 27 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-5
- Add rust patches

* Mon Feb 27 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-4
- Don't ignore make check failures

* Mon Feb 27 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-3
- Remove old patches

* Mon Feb 27 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-2
- Rename mesa-private-llvm -> llvm-private

* Tue Jan 10 2017 Jeff Law  <law@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Wed Jul 13 2016 Adam Jackson <ajax@redhat.com> - 3.8.1-1
- Update to 3.8.1
- Sync some x86 getHostCPUName updates from trunk

* Tue Jun 14 2016 Dave Airlie <airlied@redhat.com> - 3.8.0-2
- drop private cmake build

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 3.8.0-1
- llvm 3.8.0 final release

* Thu Mar 03 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.2
- llvm 3.8.0 rc3 release

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.1
- llvm 3.8.0 rc2 release

* Tue Feb 16 2016 Dan Horák <dan[at][danny.cz> 3.7.1-7
- recognize s390 as SystemZ when configuring build

* Sat Feb 13 2016 Dave Airlie <airlied@redhat.com> 3.7.1-6
- export C++ API for mesa.

* Sat Feb 13 2016 Dave Airlie <airlied@redhat.com> 3.7.1-5
- reintroduce llvm-static, clang needs it currently.

* Fri Feb 12 2016 Dave Airlie <airlied@redhat.com> 3.7.1-4
- jump back to single llvm library, the split libs aren't working very well.

* Fri Feb 05 2016 Dave Airlie <airlied@redhat.com> 3.7.1-3
- add missing obsoletes (#1303497)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.1-1
- new upstream release
- enable gold linker

* Wed Nov 04 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- fix Requires for subpackages on the main package

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
