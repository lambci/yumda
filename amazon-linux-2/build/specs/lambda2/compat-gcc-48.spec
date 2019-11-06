%define _trivial .0
%define _buildid .1

%global gccv 48
%global gcc_version 4.8.5
%global gcc_release 16

Name: compat-gcc-48
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}.0.2
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Group: Development/Languages
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL: http://gcc.gnu.org

# Sources were downloaded using:
# yumdownloader compat-gcc-48.x86_64 compat-gcc-48-c++.x86_64 compat-gcc-48-gfortran.x86_64 compat-gcc-48-libgfortran.x86_64
# And then queried using:
# rpm -qp --qf 'Name: %{name}\n[Requires: %{requires}\n][Conflicts: %{conflicts}\n][Obsoletes: %{obsoletes}\n][Provides: %{provides}\n]' *.rpm | uniq
Source0: %{name}-%{version}-%{gcc_release}.amzn2.0.2.x86_64.rpm
Source1: %{name}-c++-%{version}-%{gcc_release}.amzn2.0.2.x86_64.rpm
Source2: %{name}-gfortran-%{version}-%{gcc_release}.amzn2.0.2.x86_64.rpm
Source3: %{name}-libgfortran-%{version}-%{gcc_release}.amzn2.0.2.x86_64.rpm

BuildRequires: rpm
BuildRequires: cpio

Requires: cpp >= %{version}-%{release}
Requires: libgcc >= %{version}-%{release}
Requires: binutils >= 2.20.51.0.2-12
Requires: glibc-devel%{?_isa} >= 2.2.90-12
Requires: libgomp%{?_isa} >= %{version}-%{release}

Conflicts: gdb < 5.1-2

Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}

Provides: bundled(libiberty)
Provides: gcc = %{version}-%{release}

%global _gnu %{nil}
%global gcc_target_platform %{_target_platform}

# Main package now inclues static libraries for which we used to have
# versioned subpackages
Obsoletes: libatomic%{gccv}-static
Provides: libatomic%{gccv}-static = %{version}-%{release}
Obsoletes: libitm%{gccv}-static
Provides: libitm%{gccv}-static = %{version}-%{release}
Obsoletes: libitm%{gccv}-devel
Provides: libitm%{gccv}-devel = %{version}-%{release}
Obsoletes: libmudflap%{gccv}-devel
Provides: libmudflap%{gccv}-devel = %{version}-%{release}
Obsoletes: libmudflap%{gccv}-static
Provides: libmudflap%{gccv}-static = %{version}-%{release}
Obsoletes: libquadmath%{gccv}-devel
Provides: libquadmath%{gccv}-devel = %{version}-%{release}
Obsoletes: libquadmath%{gccv}-static
Provides: libquadmath%{gccv}-static = %{version}-%{release}
Obsoletes: libasan%{gccv}-static
Provides: libasan%{gccv}-static = %{version}-%{release}
Obsoletes: libtsan%{gccv}-static
Provides: libtsan%{gccv}-static = %{version}-%{release}

%description
The gcc package contains the GNU Compiler Collection version 4.8.
You'll need this package in order to compile C code.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libstdc++ >= %{version}-%{release}, libstdc++ < 7.4.0

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Requires: libquadmath >= %{version}-%{release}, libquadmath < 7.4

%description libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%install

pushd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idm
rpm2cpio %{SOURCE1} | cpio -idm
rpm2cpio %{SOURCE2} | cpio -idm
rpm2cpio %{SOURCE3} | cpio -idm
popd

mv %{buildroot}/usr %{buildroot}%{_prefix}

mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib64/* %{buildroot}%{_libdir}/
rm -rf %{buildroot}%{_prefix}/lib64

mv %{buildroot}%{_docdir}/%{name}-%{version}/COPYING* ./

grep -lr /usr/libexec/gcc %{buildroot} | xargs sed -i 's|/usr/libexec/gcc|%{_prefix}/libexec/gcc|g'
grep -lr /usr/lib/gcc %{buildroot} | xargs sed -i 's|/usr/lib/gcc|%{_prefix}/lib/gcc|g'

%files
%defattr(-,root,root,-)
%license COPYING*
%{_prefix}/bin/%{name}-c89
%{_prefix}/bin/%{name}-c99
%{_prefix}/bin/gcc%{gccv}
%{_prefix}/bin/gcov%{gccv}
%{_prefix}/bin/%{_target_platform}-gcc%{gccv}
%{_prefix}/bin/%{_target_platform}-gcc-%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcloog-isl.so.*
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++%{gccv}
%{_prefix}/bin/g++%{gccv}
%{_prefix}/bin/c++%{gccv}
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{version}
%{_prefix}/include/c++/%{version}/[^gjos]*
%{_prefix}/include/c++/%{version}/os*
%{_prefix}/include/c++/%{version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*

%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran%{gccv}
%{_prefix}/bin/%{_target_platform}-gfortran%{gccv}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a

%files libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.3*

%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_docdir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 31 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-11
- on aarch64 emit scheduling barriers before stack deallocation in
  function epilogues (#1362635, PR target/63293)

* Wed Aug 10 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-10
- include vecintrin.h intrinsic header on s390 (#1182152)

* Fri Jul 15 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-9
- backport OpenMP 4.5 support to libgomp (library only; #1357060,
  PRs libgomp/68579, libgomp/64625)

* Wed Jun 15 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-8
- fix a bug in C++ ref-to-ptr conversion (#1344807)
- fix combiner handling of jumps on aarch64 (#1344672,
  PR rtl-optimization/52714)

* Thu Jun  9 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-7
- ensure the timestamp on printers.py is always the same (#1344291)

* Mon Jun  6 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-6
- backport s390 z13 support (#1182152)
- fix up -fsanitize=address on powerpc64 with 46-bit virtual address space
  (#1312850)
- throw exception on std::random_device::_M_getval() failure (#1262846,
  PR libstdc++/65142, CVE-2015-5276)

* Tue May 10 2016 Jakub Jelinek <jakub@redhat.com> 4.8.5-5
- fix up libitm HTM fastpath (#1180633)
- on ppc64le default to -mcpu=power8 instead of -mcpu=power7 (#1213268)
- fix up size in .debug_pubnames (#1278872)
- turn powerpc* HTM insns into memory barriers (#1282755, PR target/67281)
- make sure to handle __builtin_alloca_with_align like alloca in
  -fstack-protector* (#1289022, PR tree-optimization/68680)
- improve DW_AT_abstract_origin of DW_TAG_GNU_call_site on s390 with -fPIC
  (#1312436)
- fix up libstdc++ pretty-printers (#1076690, PR libstdc++/53477)
- don't pass explicit --oformat option to ld on powerpc* (#1296211)
- backport Intel Memory Protection Keys ISA support - -mpku (#1304449)

* Wed Jul 15 2015 Jakub Jelinek <jakub@redhat.com> 4.8.5-4
- fix up basic_streambuf copy constructor and assignment operator
  (#1243366)

* Thu Jul  2 2015 Jakub Jelinek <jakub@redhat.com> 4.8.5-3
- backport aarch64 crc enablement - -mcpu=generic+crc (#1179935)
- rebuild against fixed binutils to fix up systemtap markers on aarch64
  (#1238462)

* Wed Jul  1 2015 Jakub Jelinek <jakub@redhat.com> 4.8.5-2
- add --enable-targets=powerpcle-linux on ppc64le (#1237363)

* Tue Jun 23 2015 Jakub Jelinek <jakub@redhat.com> 4.8.5-1
- update from the 4.8 branch (#1230103)
  - GCC 4.8.5 release
  - fix -imacros handling (#1004526, PR c/57653)
  - fix up IPA type handling (#1217267, PRs ipa/63551, ipa/64153)
  - add PowerPC analyze swaps optimization pass (#1208103, #1200336)
  - fix PowerPC vsx_extract_<mode>* patterns (#1206341)
  - fix PowerPC -mcrypto handling (#1200335)
  - Power8 unaligned vectorization improvements (#1199221, PR target/65456)
  - PRs ada/47500, ada/63225, bootstrap/64213, c++/56710, c++/58624,
	c++/63415, c++/63455, c++/64251, c++/64297, c++/64487, c++/65721,
	c++/65727, c/52769, c/61553, c/64766, debug/63342, debug/65549,
	fortran/56674, fortran/56867, fortran/57023, fortran/58813,
	fortran/59016, fortran/59024, fortran/59488, fortran/60898,
	fortran/61138, fortran/61407, fortran/63733, fortran/63744,
	fortran/63938, fortran/64244, fortran/64528, fortran/65024,
	gcov-profile/64634, inline-asm/63282, ipa/59626, ipa/63838,
	libfortran/63589, libgfortran/59513, libgfortran/60956, libgomp/61200,
	libstdc++/57440, libstdc++/59603, libstdc++/61947, libstdc++/63449,
	libstdc++/63840, libstdc++/65279, libstdc++/65543, lto/65015,
	lto/65193, middle-end/43631, middle-end/56917, middle-end/57748,
	middle-end/58624, middle-end/59990, middle-end/63608,
	middle-end/63665, middle-end/63704, middle-end/64067,
	middle-end/64111, middle-end/64199, middle-end/64225,
	middle-end/65409, middle-end/65680, middle-end/66133,
	middle-end/66251, pch/65550, preprocessor/60436,
	rtl-optimization/61058, rtl-optimization/63475,
	rtl-optimization/63483, rtl-optimization/63659,
	rtl-optimization/64037, rtl-optimization/64557, sanitizer/64265,
	target/49423, target/52941, target/53988, target/55351, target/56846,
	target/59593, target/60111, target/61413, target/62218, target/62642,
	target/63335, target/63428, target/63673, target/63947, target/64113,
	target/64115, target/64304, target/64358, target/64387, target/64409,
	target/64452, target/64453, target/64479, target/64513, target/64579,
	target/64580, target/64795, target/64882, target/64979, target/65138,
	target/65163, target/65196, target/65286, target/65368, target/65787,
	target/65849, target/66140, target/66148, target/66215, target/66275,
	target/66470, target/66474, tree-optimization/59124,
	tree-optimization/60656, tree-optimization/61634,
	tree-optimization/61686, tree-optimization/61969,
	tree-optimization/62031, tree-optimization/62167,
	tree-optimization/63375, tree-optimization/63379,
	tree-optimization/63551, tree-optimization/63593,
	tree-optimization/63605, tree-optimization/63841,
	tree-optimization/63844, tree-optimization/64269,
	tree-optimization/64277, tree-optimization/64493,
	tree-optimization/64495, tree-optimization/64563,
	tree-optimization/65063, tree-optimization/65388,
	tree-optimization/65518, tree-optimization/66123,
	tree-optimization/66233, tree-optimization/66251,
	tree-optimization/66272

* Fri Nov 14 2014 Richard Henderson <rth@redhat.com> 4.8.3-9
- enable Ada for ppc64le (#1162196)

* Fri Sep 26 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-8
- fix PowerPC unaligned vectorization bug (#1146871,
  PR tree-optimization/63341)
- fix another -fcompare-debug issue (PR debug/63284)

* Thu Sep 11 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-7
- update from the 4.8 branch
  - fix ppc32 libgo.so.4 to avoid RWE PT_GNU_STACK

* Wed Sep 10 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-6
- update from the 4.8 branch (#1140019)
  - PRs c++/58714, c++/59823, c++/59956, c++/60241, c++/60361, c++/61959,
	c/61271, debug/55794, debug/60655, debug/61923, fortran/61999,
	fortran/62214, fortran/62270, ipa/61986, ipa/62015, libgfortran/62188,
	libstdc++/58962, libstdc++/61946, middle-end/61010, middle-end/61045,
	middle-end/62103, rtl-optimization/62004, rtl-optimization/62030,
	target/61996, target/62038, target/62195, testsuite/56194,
	tree-optimization/60196, tree-optimization/60707,
	tree-optimization/61452, tree-optimization/62073,
	tree-optimization/62075, tree-optimization/63189

* Thu Aug 21 2014 Richard Henderson <rth@redhat.com> 4.8.3-5
- backport aarch64 unwind info improvements (#1132636)

* Fri Aug  1 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-4
- update from the 4.8 branch
  - PRs fortran/61780, libobjc/61920, target/47230, tree-optimization/61375,
	tree-optimization/61964
  - fix libgfortran overflows on allocation (CVE-2014-5044)
- backport ibm-ldouble performance improvements (#1090620)

* Wed Jul 30 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-3
- on ppc64le use -mtune=power8 by default (#1123484)

* Thu Jul 17 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-2
- update from the 4.8 branch
  - PRs c++/61500, c++/61539, c++/61647, fortran/58883, fortran/61459,
	middle-end/53590, rtl-optimization/61801, target/61542, target/61586,
	tree-optimization/61306, tree-optimization/61684
- for rhel 7.1 keep the old 4.8.2 pathnames and use 4.8.3 symlinks
- merge in aarch64 support (#1070290)
- small improvements on s390x for z196 and later (#1088542)
- make sure OpenMP outlined artificial functions have DW_AT_name (#844959)

* Tue Jun 24 2014 Jakub Jelinek <jakub@redhat.com> 4.8.3-1
- update from the 4.8 branch
  - GCC 4.8.3 release
  - PRs c++/60605, c++/60731, c++/61134, fortran/45187, ipa/61393,
	libfortran/61187, libfortran/61310, libstdc++/60734, libstdc++/60966,
	rtl-optimization/60866, rtl-optimization/60901, rtl-optimization/61094,
	rtl-optimization/61446, target/61044, target/61193, target/61202,
	target/61208, target/61231, target/61239, target/61249, target/61300,
	target/61415, target/61423, target/61431, target/61443, target/61483,
	target/61545, target/61570, tree-optimization/61383

* Thu May 15 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-18
- update from the 4.8 branch
  - PRs c++/60367, c++/60628, c++/60689, c++/60708, c++/60713, debug/60603,
	driver/61106, libfortran/56919, libfortran/60810, libstdc++/60497,
	libstdc++/60594, libstdc++/61117, middle-end/36282, middle-end/55022,
	middle-end/60635, middle-end/60729, middle-end/60750,
	middle-end/60849, middle-end/60895, rtl-optimization/60769,
	target/57589, target/58595, target/59952, target/60516, target/60609,
	target/60672, target/60693, target/60839, target/60909, target/60941,
	target/60991, target/61026, target/61055, tree-optimization/57864,
	tree-optimization/59817, tree-optimization/60453,
	tree-optimization/60502, tree-optimization/60740,
	tree-optimization/60766, tree-optimization/60836,
	tree-optimization/60903, tree-optimization/60930,
	tree-optimization/60960
- backport OpenMP 4.0 support to libgomp (library only; PR libgomp/58691)

* Fri Apr 11 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-17
- update from the 4.8 branch
  - PRs ada/51483, ada/60703, c/37743, c/59891, c/60101, c++/37140, c++/41174,
	c++/54652, c++/55800, c++/57043, c++/57524, c++/57899, c++/58466,
	c++/58504, c++/58606, c++/58632, c++/58639, c++/58672, c++/58812,
	c++/58814, c++/58835, c++/58837, c++/58845, c++/58873, c++/58965,
	c++/59097, c++/59224, c++/59646, c++/59989, c++/60108, c++/60146,
	c++/60182, c++/60187, c++/60216, c++/60219, c++/60248, debug/59776,
	fortran/49397, fortran/52370, fortran/55907, fortran/57033,
	fortran/58007, fortran/58803, fortran/59395, fortran/59414,
	fortran/59599, fortran/59700, fortran/59906, fortran/60231,
	fortran/60283, fortran/60341, fortran/60450, fortran/60522,
	fortran/60543, fortran/60576, fortran/60677, ipa/55260, ipa/60026,
	ipa/60419, ipa/60640, libfortran/38199, libfortran/58324,
	libfortran/59700, libfortran/59764, libfortran/59771,
	libfortran/59774, libfortran/59836, libfortran/60128, libgcc/60166,
	libgcj/55637, libstdc++/59215, libstdc++/59392, libstdc++/59548,
	libstdc++/59680, libstdc++/59738, libstdc++/60564, libstdc++/60658,
	middle-end/57499, middle-end/58809, middle-end/60004,
	middle-end/60221, middle-end/60291, objc/56870, other/56653,
	preprocessor/56824, preprocessor/58844, preprocessor/60400,
	rtl-optimization/56356, rtl-optimization/57422,
	rtl-optimization/57425, rtl-optimization/57569,
	rtl-optimization/57637, rtl-optimization/60116,
	rtl-optimization/60452, rtl-optimization/60601,
	rtl-optimization/60700, target/43546, target/48094, target/54083,
	target/54407, target/55426, target/56843, target/57052, target/57935,
	target/57949, target/58675, target/58710, target/59054, target/59379,
	target/59396, target/59462, target/59718, target/59777, target/59844,
	target/59880, target/59909, target/59929, target/60017, target/60032,
	target/60039, target/60062, target/60151, target/60193, target/60203,
	target/60207, target/60486, target/60568, target/60735,
	tree-optimization/56490, tree-optimization/59903,
	tree-optimization/60115, tree-optimization/60183,
	tree-optimization/60276, tree-optimization/60382,
	tree-optimization/60429, tree-optimization/60454,
	tree-optimization/60485
  - powerpc64 little endian support
- enable ppc64le in the spec file

* Mon Mar  3 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-16
- fix up compare_exchange_* in libatomic too (PR c++/60272)

* Thu Feb 20 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-15
- fix exception spec instantiation ICE (#1067398, PR c++/60046)
- fix pch on aarch64 (#1058991, PR pch/60010)
- configure with --enable-gnu-indirect-function on architectures
  and distros that support it and don't support it by default
  yet (#1067245)
- fix vector permutation handling on i?86/x86_64 (PR target/57896)
- fix __atomic_compare_exchange_* not to store into *expected
  on success (PR c++/60272)
- fix -march=native on VMs where saving/restoring of YMM state
  is not supported, yet CPU supports f16c (PR driver/60233)
- add ref7.C testcase (PR c++/60274)

* Wed Feb 19 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-14
- remove libgo P.224 elliptic curve (#1066539)
- fix -mcpu=power8 ICE (#1064242, PR target/60137)

* Tue Jan 21 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-13
- when removing -Wall from CXXFLAGS, if -Werror=format-security
  is present, add -Wformat to it, so that GCC builds on F21

* Mon Jan 20 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-12
- update from the 4.8 branch (#1052892)
  - PRs c++/59838, debug/54694, fortran/34547, fortran/58410,
	middle-end/59827, middle-end/59860, target/58139, target/59142,
	target/59695, target/59794, target/59826, target/59839
- fix handling of initialized vars with flexible array members
  (#1035413, PR middle-end/28865)

* Wed Jan 15 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-11
- update from the 4.8 branch
  - fix s390x reload bug (#1052372, PR target/59803)

* Tue Jan 14 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-10
- update from the 4.8 branch (#1052892)
  - PRs ada/55946, ada/59772, c++/56060, c++/58954, c++/59255, c++/59730,
	fortran/57042, fortran/58998, fortran/59493, fortran/59612,
	fortran/59654, ipa/59610, middle-end/59584, pch/59436,
	rtl-optimization/54300, rtl-optimization/58668,
	rtl-optimization/59137, rtl-optimization/59647,
	rtl-optimization/59724, target/57386, target/59587, target/59625,
	target/59652, testsuite/58630, tree-optimization/54570,
	tree-optimization/59125, tree-optimization/59362,
	tree-optimization/59715, tree-optimization/59745
- default to -march=z196 instead of -march=z10 on s390/s390x (#1052890)

* Fri Jan 10 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-9
- define %%global _performance_build 1 (#1051064)

* Tue Jan  7 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-8
- treat ppc64p7 as ppc64 (#1048859)

* Thu Dec 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-7
- update from the 4.8 branch
  - PRs libgomp/59467, rtl-optimization/58295, target/56807,
	testsuite/59442
  - fix LRA coalescing for real (PR middle-end/59470)

* Wed Dec 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-6
- temporarily revert PR middle-end/58956 to avoid libstdc++
  miscompilation on i?86 (PR middle-end/59470)

* Mon Dec  9 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-5
- update from the 4.8 branch
  - PRs ada/59382, bootstrap/57683, c++/58162, c++/59031, c++/59032,
	c++/59044, c++/59052, c++/59268, c++/59297, c/59280, c/59351,
	fortran/57445, fortran/58099, fortran/58471, fortran/58771,
	middle-end/58742, middle-end/58941, middle-end/58956,
	middle-end/59011, middle-end/59037, middle-end/59138,
	rtl-optimization/58726, target/50751, target/51244, target/56788,
	target/58854, target/58864, target/59021, target/59088,
	target/59101, target/59153, target/59163, target/59207,
	target/59343, target/59405, tree-optimization/57517,
	tree-optimization/58137, tree-optimization/58143,
	tree-optimization/58653, tree-optimization/58794,
	tree-optimization/59014, tree-optimization/59047,
	tree-optimization/59139, tree-optimization/59164,
	tree-optimization/59288, tree-optimization/59330,
	tree-optimization/59334, tree-optimization/59358,
	tree-optimization/59388
- aarch64 gcj enablement (#1023789)
- look for libgfortran.spec and libitm.spec in %%{_lib} rather than lib
  subdirs (#1023789)

* Mon Nov 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-4
- update from the 4.8 branch
  - PRs plugins/52872, regression/58985, target/59034

* Wed Nov  6 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-3
- update from the 4.8 branch
  - PRs c++/58282, c++/58979, fortran/58355, fortran/58989, libstdc++/58839,
	libstdc++/58912, libstdc++/58952, lto/57084, middle-end/58789,
	rtl-optimization/58079, rtl-optimization/58831, rtl/58542,
	target/58690, target/58779, target/58792, target/58838,
	tree-optimization/57488, tree-optimization/58805,
	tree-optimization/58984
- fix ICEs in get_bit_range (PR middle-end/58970)
- fix ICEs in RTL loop unswitching (PR rtl-optimization/58997)

* Sun Oct 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-2
- update from the 4.8 branch
  - PRs c++/58596, libstdc++/58800
- power8 TImode fix (#1014053, PR target/58673)

* Thu Oct 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-1
- update from the 4.8 branch
  - GCC 4.8.2 release
  - PRs c++/57850, c++/58633, libstdc++/58191

* Thu Oct 10 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-12
- update from the 4.8 branch
  - PRs c++/58568, fortran/55469, fortran/57697, fortran/58469,
	libstdc++/57465, libstdc++/57641, libstdc++/58659, target/58460,
	tree-optimization/58539
  - fix asm goto handling (#1017704, PR middle-end/58670)

* Wed Oct  2 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-11
- update from the 4.8 branch
  - PRs c++/58535, libstdc++/58437, libstdc++/58569, middle-end/56791,
	middle-end/58463, middle-end/58564, target/58330,
	tree-optimization/56716
  - fix s390x z10+ chunkification (#1012870, PR target/58574)
- disable ppc{,64} -mvsx-timode by default (#1014053, PR target/58587)

* Fri Sep 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-10
- update from the 4.8 branch
  - PRs ada/58264, c++/58457, c++/58458, libstdc++/58358,
	tree-optimization/58088
- on RHEL7, configure on ppc/ppc64 with default -mcpu=power7,
  on s390/s390x with default -march=z10 -mtune=zEC12 and
  on i?86 default to -march=x86-64 -mtune=generic (#805157)
- on Fedora 20+ and RHEL7 default to -fdiagnostics-color=auto
  rather than -fdiagnostics-color=never, if GCC_COLORS isn't
  in the environment; to turn it off by default, set GCC_COLORS=
  in the environment

* Sun Sep 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-9
- update from the 4.8 branch
  - PRs c++/58273, libstdc++/58415, middle-end/58377, rtl-optimization/58365,
	target/58314, target/58361, target/58382, tree-optimization/58385
- add arm_neon.h on aarch64 (#1007490)

* Mon Sep  9 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-8
- update from the 4.8 branch
  - PRs c++/58325, libstdc++/58302, libstdc++/58341, middle-end/57656,
	other/12081, target/57735, tree-optimization/57521,
	tree-optimization/57685, tree-optimization/58010,
	tree-optimization/58223, tree-optimization/58228,
	tree-optimization/58246, tree-optimization/58277,
	tree-optimization/58364

* Thu Aug 29 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-7
- update from the 4.8 branch
  - PRs c++/58083, c++/58119, c++/58190, fortran/57798, fortran/58185,
	middle-end/56977, middle-end/57381, middle-end/58257, target/56979,
	target/57865, target/57927, target/58218, tree-optimization/57343,
	tree-optimization/57396, tree-optimization/57417,
	tree-optimization/58006, tree-optimization/58164,
	tree-optimization/58165, tree-optimization/58209
- fix up x86-64 -mcmodel=large -fpic TLS GD and LD model
  (#994244, PR target/58067)
- power8 fusion support fixes (#731884, PR target/58160)

* Wed Aug 14 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-6
- update from the 4.8 branch
  - PRs c++/57825, c++/57901, c++/57981, c++/58022, fortran/57435,
	fortran/58058, libstdc++/56627, libstdc++/57914, libstdc++/58098,
	middle-end/58041, rtl-optimization/57459, rtl-optimization/57708,
	rtl-optimization/57878, sanitizer/56417, target/51784, target/57516,
	target/58067, target/58132, tree-optimization/57980
- power8 fusion support (#731884)
- fix up ABI alignment patch (#947197)
- fix up SRA with volatile struct accesses (PR tree-optimization/58145)

* Wed Jul 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-5
- update from the 4.8 branch
  - PRs target/55656, target/55657
  - update to Go 1.1.1
- backport power8 HTM support from trunk (#731884)
- backport s390 zEC12 HTM support from trunk

* Mon Jul 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-4
- update from the 4.8 branch
  - PRs c++/57437, c++/57526, c++/57532, c++/57545, c++/57550, c++/57551,
	c++/57645, c++/57771, c++/57831, fortran/57785,
	rtl-optimization/57829, target/56102, target/56892, target/56987,
	target/57506, target/57631, target/57736, target/57744,
	target/57777, target/57792, target/57844
- backport some raw-string literal handling fixes (#981029,
  PRs preprocessor/57757, preprocessor/57824)
- improve convert_to_* (PR c++/56493)
- tune for power7 on RHEL7

* Fri Jun 28 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-3
- update from the 4.8 branch
  - PRs c++/53211, c++/56544, driver/57652, libstdc++/57619, libstdc++/57666,
	libstdc++/57674, rtl-optimization/57518, target/57623, target/57655,
	tree-optimization/57358, tree-optimization/57537
  - fix up gcc-{ar,nm,ranlib} (#974853, PR driver/57651)
- fix two libitm HTM handling bugs (PR libitm/57643)
- speed up __popcount[sdt]i2 library function (PR middle-end/36041)
- backport power8 support from trunk (#731884, PR target/57615)
- for Fedora 20+ test -fstack-protector-strong during %%check instead
  of -fstack-protector

* Wed Jun 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-2
- update from the 4.8 branch
  - PRs fortran/57364, fortran/57508, target/56547, target/57379, target/57568
- backport backwards compatible alignment ABI fixes (#947197, PR target/56564)
- fix up widening multiplication vectorization on big-endian
  (PR tree-optimization/57537)

* Mon Jun  3 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-1
- update from the 4.8 branch
  - GCC 4.8.1 release
  - PRs c++/56930, c++/57319, fortran/57217, target/49146, target/56742
- backport Intel Silvermont enablement and tuning from trunk
- backport 3 small AMD improvement patches from trunk

* Sun May 26 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-8
- update from the 4.8 branch
  - std::chrono::steady_clock ABI fixes from 4.8.0-7

* Fri May 24 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-7
- update from the 4.8 branch
  - PRs c++/57016, c++/57317, c++/57325, c++/57388, libffi/56033,
	libstdc++/57336, middle-end/57344, middle-end/57347, plugins/56754,
	rtl-optimization/57341, target/56732, target/57356,
	tree-optimization/57303, tree-optimization/57318,
	tree-optimization/57321, tree-optimization/57330, tree-ssa/57385
  - std::chrono::steady_clock now really steady

* Fri May 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-6
- update from the 4.8 branch
  - PRs c++/56782, c++/56998, c++/57041, c++/57196, c++/57243, c++/57252,
	c++/57253, c++/57254, c++/57274, c++/57279, middle-end/57251,
	rtl-optimization/57281, rtl-optimization/57300, target/45359,
	target/46396, target/57264
- backport color diagnostics support from trunk, enable with
  -fdiagnostics-color=auto, -fdiagnostics-color=always or
  having non-empty GCC_COLORS variable in environment
- backport -fstack-protector-strong support from trunk

* Fri May 10 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-5
- update from the 4.8 branch
  - PRs bootstrap/54281, bootstrap/54659, c++/57047, c++/57068, c++/57222,
	fortran/57142, libstdc++/57212, middle-end/56988, target/55033,
	target/57237, tree-optimization/57200, tree-optimization/57214
- fix up strlen pass (PR tree-optimization/57230)

* Tue May  7 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-4
- update from the 4.8 branch
  - PRs ada/56474, c++/50261, c++/56450, c++/56859, c++/56970, c++/57064,
	c++/57092, c++/57183, debug/57184, fortran/51825, fortran/52512,
	fortran/53685, fortran/56786, fortran/56814, fortran/56872,
	fortran/56968, fortran/57022, libfortran/51825, libfortran/52512,
	libfortran/56786, libstdc++/57010, middle-end/57103,
	rtl-optimization/56605, rtl-optimization/56847,
	rtl-optimization/57003, rtl-optimization/57130,
	rtl-optimization/57131, rtl-optimizations/57046, sanitizer/56990,
	target/44578, target/55445, target/56797, target/56866, target/57018,
	target/57091, target/57097, target/57098, target/57106, target/57108,
	target/57150, tree-optimization/57051, tree-optimization/57066,
	tree-optimization/57083, tree-optimization/57104,
	tree-optimization/57149, tree-optimization/57185
  - fix gcj with -fsection-anchors (#952673, PR libgcj/57074)
- enable libitm on s390{,x}
- error when linking with both -fsanitize=address and -fsanitize=thread
  (#957778)

* Fri Apr 19 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-3
- update from the 4.8 branch
  - PRs c++/56388, fortran/56816, fortran/56994, rtl-optimization/56992,
	target/56890, target/56903, target/56948, tree-optimization/56962,
	tree-optimization/56984
- fix up LRA caused miscompilation of xulrunner on i?86
  (#949553, PR rtl-optimization/56999)
- reassoc fix for -Ofast -frounding-math (PR tree-optimization/57000)

* Fri Apr 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-2
- update from the 4.8 branch
  - PRs c++/35722, c++/45282, c++/52014, c++/52374, c++/52748, c++/54277,
	c++/54359, c++/54764, c++/55532, c++/55951, c++/55972, c++/56039,
	c++/56447, c++/56582, c++/56646, c++/56692, c++/56699, c++/56722,
	c++/56728, c++/56749, c++/56772, c++/56774, c++/56793, c++/56794,
	c++/56821, c++/56895, c++/56913, debug/56819, fortran/54932,
	fortran/56696, fortran/56735, fortran/56737, fortran/56782,
	libstdc++/55977, libstdc++/55979, libstdc++/56002, libstdc++/56678,
	libstdc++/56834, lto/56777, middle-end/56694, middle-end/56768,
	middle-end/56883, other/55274, rtl-optimization/48182,
	rtl-optimization/56745, sanitizer/55702, target/54805, target/55487,
	target/56560, target/56720, target/56771, tree-optimization/48184,
	tree-optimization/48186, tree-optimization/48762,
	tree-optimization/56407, tree-optimization/56501,
	tree-optimization/56817, tree-optimization/56837,
	tree-optimization/56899, tree-optimization/56918,
	tree-optimization/56920

* Fri Mar 22 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-1
- update from the 4.8 branch
  - GCC 4.8.0 release
  - PRs c++/56607, other/43620
  - fix length in .debug_aranges in some cases
- improve debug info for optimized away global vars (PR debug/56608)
- don't warn about signed 1-bit enum bitfields containing values 0 and -1
  or just -1 (PR c/56566)

* Wed Mar 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.18
- update from the 4.8 branch
  - PRs libstdc++/56468, target/56640, tree-optimization/56635,
	tree-optimization/56661
- package libasan_preinit.o

* Sat Mar 16 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.17
- update from trunk and the 4.8 branch
  - PRs ada/52123, c++/51412, c++/51494, c++/51884, c++/52183, c++/56222,
	c++/56346, c++/56565, c++/56567, c++/56611, c++/56614, debug/56307,
	fortran/56575, fortran/56615, libstdc++/56492, libstdc++/56609,
	libstdc++/56613, lto/56557, middle-end/56524, middle-end/56571,
	target/40797, target/49880, target/56470, target/56591, target/56619,
	testsuite/54119, tree-optimization/53265, tree-optimization/56478,
	tree-optimization/56570, tree-optimization/56608

* Thu Mar  7 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.16
- updated from trunk
  - PRs bootstrap/56509, c++/54383, c++/55135, c++/56464, c++/56530,
	c++/56534, c++/56543, debug/55364, debug/56510, libquadmath/55473,
	lto/50293, lto/56515, middle-end/50494, middle-end/56294,
	middle-end/56525, middle-end/56526, middle-end/56548,
	rtl-optimization/56484, rtl-optimization/56494, target/56529,
	tree-optimization/56270, tree-optimization/56521,
	tree-optimization/56539, tree-optimization/56559
  - include arm-cores.def in gcc-python-plugin on arm (#910926)
- include vxworks-dummy.h in gcc-python-plugin where needed (PR plugins/45078)

* Mon Mar  4 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.15
- updated from trunk
  - PRs c++/10291, c++/40405, c++/52688, c++/55632, c++/55813, c++/56243,
	c++/56358, c++/56359, c++/56377, c++/56395, c++/56403, c++/56419,
	c++/56438, c++/56481, fortran/54730, fortran/56385, fortran/56416,
	fortran/56477, fortran/56491, libfortran/30162, libstdc++/56011,
	libstdc++/56012, middle-end/45472, middle-end/56077,
	middle-end/56108, middle-end/56420, middle-end/56461,
	rtl-optimization/50339, rtl-optimization/56466, sanitizer/56393,
	sanitizer/56454, target/48901, target/52500, target/52501,
	target/52550, target/54639, target/54640, target/54662, target/56444,
	target/56445, target/56455, testsuite/52641, tree-optimization/55481,
	tree-optimization/56175, tree-optimization/56294,
	tree-optimization/56310, tree-optimization/56415,
	tree-optimization/56426, tree-optimization/56443,
	tree-optimization/56448
- fnsplit fix (PR tree-optimization/56424)

* Wed Feb 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.14
- updated from trunk
  - PRs asan/56330, c++/51242, c++/54276, c++/56373, libquadmath/56379,
	middle-end/55889, middle-end/56349, pch/54117,
	rtl-optimization/56348, target/52555, target/54685, target/56214,
	target/56347, tree-optimization/55334, tree-optimization/56321,
	tree-optimization/56350, tree-optimization/56366,
	tree-optimization/56381, tree-optimization/56384,
	tree-optimization/56396, tree-optimization/56398
- add BuildRequires: /usr/bin/pod2man to fix man pages generation
- don't ICE on bogus inline asm in kernel (#912857, PR inline-asm/56405)
- fix up info page building with texinfo 5.0 (PR bootstrap/56258)
- devirtualization ICE fix (PR tree-optimization/56265)

* Fri Feb 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.13
- updated from trunk
  - PRs bootstrap/56327, c++/52026, c++/54922, c++/55003, c++/55220,
	c++/55223, c++/55232, c++/55582, c++/55670, c++/55680, c++/56323,
	c++/56343, fortran/53818, fortran/56224, fortran/56318,
	libstdc++/56111, lto/50494, target/55431, target/55941,
	testsuite/56138
- asan fixes (PR sanitizer/56330)
- asan speedup - use 0x7fff8000 shadow offset instead of 1LL << 44 on
  x86_64

* Wed Feb 13 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.12
- updated from trunk
  - PRs c++/55710, c++/55879, c++/55993, c++/56135, c++/56155, c++/56285,
	c++/56291, c/44938, fortran/46952, fortran/56204, inline-asm/56148,
	libitm/55693, lto/56295, lto/56297, middle-end/56288,
	sanitizer/56128, target/52122, testsuite/56082
  - fix IRA bug that caused reload ICE on ARM (#910153, target/56184)
  - attempt harder to fold "n" constrainted asm input operands in C++
    with -O0 (#910421, c++/56302)

* Mon Feb 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.11
- updated from trunk
  - PRs c++/56238, c++/56247, c++/56268, fortran/55362, libstdc++/56267,
	libstdc++/56278, libstdc++/56282, rtl-optimization/56246,
	rtl-optimization/56275, target/56043, tree-optimization/56264,
	tree-optimization/56273
- improve expansion of mem1 op= mem2 (PR rtl-optimization/56151)

* Fri Feb  8 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.10
- updated from trunk
  - PRs bootstrap/56227, c++/56235, c++/56237, c++/56239, c++/56241,
	debug/53363, fortran/54339, fortran/55789, libstdc++/56193,
	libstdc++/56216, lto/56231, middle-end/56181,
	rtl-optimization/56195, rtl-optimization/56225, target/50678,
	target/54009, target/54131, tree-optimization/56250
  - fix Ada frontend miscompilation with profiledbootstrap (#906516,
    PR rtl-optimization/56178)
- restore parsing of ppc inline asm dialects (#909298, PR target/56256)
- fix up libiberty old regex (PR other/56245)
- fix IRA -O0 -g code debug regression (PR debug/53948)

* Wed Feb  6 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.9
- updated from trunk
  - PRs c++/54122, c++/56177, c++/56208, debug/54793, fortran/47517,
	fortran/50627, fortran/54195, fortran/56008, fortran/56054,
	libstdc++/56202, lto/56168, middle-end/56113, middle-end/56167,
	middle-end/56217, rtl-optimization/56131, sanitizer/55617,
	target/52123, target/54601, target/55146, target/56186,
	tree-optimization/53185, tree-optimization/53342,
	tree-optimization/54386, tree-optimization/55789,
	tree-optimization/56188
  - fix up stdarg pass (PR tree-optimization/56205, #906367)
  - remove unused thread_local bitfield (#907882)
- fix cselim pass on calls that might free memory (PR tree-optimization/52448)
- fix libgfortran internal_pack (PR fortran/55978)
- fix up .debug_loc for first function in CU, if it contains empty ranges
  at the beginning of the function (PR debug/56154, #904252)
- fix ppc64 indirect calls (PR target/56228, #908388)

* Thu Jan 31 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.8
- updated from trunk
  - PRs c++/56162, debug/54410, debug/54508, debug/55059, fortran/54107,
	fortran/56138, libgomp/55561, libstdc++/54314, lto/56147,
	middle-end/53073, other/53413, other/54620, rtl-optimization/56144,
	sanitizer/55374, target/39064, target/56121, tree-optimization/55270,
	tree-optimization/56064, tree-optimization/56113,
	tree-optimization/56150, tree-optimization/56157

* Tue Jan 29 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.7
- updated from trunk
  - PRs c++/56095, c++/56104, c/56078, fortran/53537, fortran/55984,
	fortran/56047, inline-asm/55934, libstdc++/56085, libstdc++/56112,
	other/54814, other/56076, rtl-optimization/56117, target/54663,
	target/56114, testsuite/56053, tree-optimization/55927,
	tree-optimization/56034, tree-optimization/56035,
	tree-optimization/56094, tree-optimization/56098,
	tree-optimization/56125

* Thu Jan 24 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.6
- updated from trunk
  - PRs c++/53609, c++/55944, c++/56067, c++/56071, fortran/56081,
	libgomp/51376, libgomp/56073, libquadmath/56072, middle-end/56074,
	sanitizer/55989, target/49069, target/54222, target/55686,
	target/56028
- update TeX related BuildRequires (#891460)

* Tue Jan 22 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.5
- updated from trunk
  - PRs c++/56059, fortran/55919, rtl-optimization/56023,
	tree-optimization/56051
- fix up cloog dlopen patches for upgrade to cloog-0.18.0
- fix Fortran OpenMP OOP ICE (PR fortran/56052)

* Mon Jan 21 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.4
- updated from trunk
  - PRs ada/864, bootstrap/55792, bootstrap/55961, c++/52343, c++/55663,
	c++/55753, c++/55801, c++/55878, c++/55893, c/48418, debug/49888,
	debug/53235, debug/53671, debug/54114, debug/54402, debug/55579,
	debug/56006, driver/55470, driver/55884, fortran/42769, fortran/45836,
	fortran/45900, fortran/47203, fortran/52865, fortran/53876,
	fortran/54286, fortran/54678, fortran/54990, fortran/54992,
	fortran/55072, fortran/55341, fortran/55618, fortran/55758,
	fortran/55763, fortran/55806, fortran/55852, fortran/55868,
	fortran/55935, fortran/55983, libmudflap/53359, libstdc++/51007,
	libstdc++/55043, libstdc++/55233, libstdc++/55594, libstdc++/55728,
	libstdc++/55847, libstdc++/55861, libstdc++/55908, lto/45375,
	middle-end/55114, middle-end/55851, middle-end/55882,
	middle-end/55890, middle-end/56015, other/55973, other/55982,
	rtl-optimization/52573, rtl-optimization/53827,
	rtl-optimization/55153, rtl-optimization/55547,
	rtl-optimization/55672, rtl-optimization/55829,
	rtl-optimization/55833, rtl-optimization/55845,
	rtl-optimization/56005, sanitizer/55488, sanitizer/55679,
	sanitizer/55844, target/42661, target/43961, target/54461,
	target/54908, target/55301, target/55433, target/55565,
	target/55718, target/55719, target/55876, target/55897,
	target/55940, target/55948, target/55974, target/55981,
	target/56058, testsuite/54622, testsuite/55994,
	tree-optimization/44061, tree-optimization/48189,
	tree-optimization/48766, tree-optimization/52631,
	tree-optimization/53465, tree-optimization/54120,
	tree-optimization/54767, tree-optimization/55273,
	tree-optimization/55569, tree-optimization/55823,
	tree-optimization/55862, tree-optimization/55875,
	tree-optimization/55888, tree-optimization/55920,
	tree-optimization/55921, tree-optimization/55955,
	tree-optimization/55964, tree-optimization/55995,
	tree-optimization/56029, tree-optimization/55264
- fix up multiversioning (PR c++/55742)
- fix up ICE with target attribute (PR middle-end/56022)
- update isl to 0.11.1 and cloog to 0.18.0

* Fri Nov  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-8
- update from the 4.7 branch
  - PRs fortran/54917, libstdc++/28811, libstdc++/54482, libstdc++/55028,
	libstdc++/55215, middle-end/55219, target/55204,
	tree-optimization/54986
- further debug info quality improvements
- fix reassociation (PR c++/55137)
- fix range test optimization with -fwrapv (PR tree-optimization/55236)
- add BuildRequires hostname (#875001)
- __cxa_vec_new[23] overflow checking (#875009)

* Mon Nov  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-7
- update from the 4.7 branch
  - PRs c++/54984, c++/54988, debug/54828, libstdc++/55047, libstdc++/55123,
	libstdc++/55169, middle-end/54945, rtl-optimization/53701,
	rtl-optimization/54870, target/53975, target/54892, target/55019,
	target/55175, tree-optimization/53708, tree-optimization/54146,
	tree-optimization/54877, tree-optimization/54902,
	tree-optimization/54920, tree-optimization/54985
- backported s390{,x} zEC12 enablement (#805114)
- backport of selected debug info quality improvements
  - PRs debug/54402, debug/54693, debug/54953, debug/54970, debug/54971
- optimize away overflow checking for new char[n]; and similar cases
  where n is multiplied by 1

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> 4.7.2-6
- Provides: bundled(libiberty)

* Mon Oct 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-5
- update from the 4.7 branch
  - PRs fortran/54784, libfortran/54736, libstdc++/54861

* Tue Oct  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-4
- update from the 4.7 branch
  - PRs c++/54777, c++/54858, debug/53135, target/54741, target/54785,
	target/54854
- backport of selected debug info quality improvements (#851467)
  - PRs debug/48866, debug/52983, debug/53740, debug/53923, debug/54519,
	debug/54551

* Mon Oct  1 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-3
- update from the 4.7 branch
  - PRs target/54083, target/54703, target/54746, testsuite/54007
- backport operator new[] overflow checking (#850911, PR c++/19351)

* Fri Sep 21 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-2
- update from the 4.7 branch
  - PRs c/54103, c/54552, libstdc++/54102, middle-end/54638, other/43620

* Thu Sep 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-1
- update from the 4.7 branch
  - GCC 4.7.2 release
  - PRs c++/53661, lto/54312, tree-optimization/54563

* Thu Sep 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-8
- update from the 4.7 branch
  - PRs c++/53836, c++/53839, c++/54086, c++/54197, c++/54253, c++/54341,
	c++/54506, c++/54511, c/54363, c/54428, c/54559, debug/54534,
	driver/54335, fortran/53306, fortran/54208, fortran/54225,
	fortran/54435, fortran/54443, fortran/54556, gcov-profile/54487,
	libstdc++/54172, libstdc++/54185, libstdc++/54297, libstdc++/54351,
	libstdc++/54376, libstdc++/54388, lto/53572, middle-end/53667,
	middle-end/53992, middle-end/54146, middle-end/54486,
	middle-end/54515, rtl-optimization/54088, rtl-optimization/54369,
	rtl-optimization/54455, target/45070, target/46254, target/54212,
	target/54220, target/54252, target/54436, target/54461,
	target/54476, target/54536, tree-opt/54494,
	tree-optimization/53922, tree-optimization/54498
- fix up _mm_f{,n}m{add,sub}_s{s,d} fma intrinsics (PR target/54564)

* Mon Aug 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7
- update from the 4.7 branch
  - PR rtl-optimization/53942
- backport -mrdseed, -mprfchw and -madx support

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-6
- update from the 4.7 branch
  - PRs libstdc++/54036, libstdc++/54075, rtl-optimization/54157,
	target/33135, target/52530

* Fri Jul 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-5
- update from the 4.7 branch
  - PRs c++/54026, middle-end/54017, rtl-optimization/52250, target/53877,
	target/54029
  - fix endless hang of C++ compiler (#841814, PR c++/54038)

* Wed Jul 18 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-4
- update from the 4.7 branch
  - PRs c++/53549, c++/53989, c++/53995, libstdc++/53978

* Mon Jul 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-3
- update from the 4.7 branch
  - C++11 ABI change - std::list and std::pair in C++11 ABI compatible again
    with C++03, but ABI incompatible with C++11 in GCC 4.7.[01]
  - PRs bootstrap/52947, c++/53733, c++/53816, c++/53821, c++/53826,
	c++/53882, c++/53953, fortran/53732, libstdc++/49561,
	libstdc++/53578, libstdc++/53657, libstdc++/53830, libstdc++/53872,
	middle-end/38474, middle-end/50708, middle-end/52621,
	middle-end/52786, middle-end/53433, rtl-optimization/53908,
	target/53110, target/53811, target/53853, target/53961,
	testsuite/20771, tree-optimization/53693
- backport -mrtm and -mhle support (PRs target/53194, target/53201,
  target/53315)
- fix up ppc32 *movdi_internal32 pattern (#837630)
- apply ld.so arm hfp patch on all arm arches
- enable go support on arm

* Fri Jul 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-2
- change ld.so pathname for arm hfp for F18+

* Fri Jun 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-1
- update from the 4.7 branch
  - GCC 4.7.1 release
  - PRs ada/53592, c++/51214, c++/52637, c++/52841, c++/52988, c++/53202,
	c++/53305, c++/53498, c++/53524, c++/53594, c++/53599, c++/53602,
	c++/53616, c++/53651, c++/53752, debug/53682, fortran/50619,
	fortran/53597, fortran/53685, fortran/53691, gcov-profile/53744,
	libgomp/52993, libstdc++/53270, libstdc++/53678, middle-end/53470,
	middle-end/53580, middle-end/53790, preprocessor/37215,
	rtl-optimization/53589, rtl-optimization/53700, target/52908,
	target/53559, target/53595, target/53621, target/53759,
	tree-optimization/52558

* Mon Jun  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-7
- update from the 4.7 branch
  - PRs ada/53517, c++/52725, c++/52905, c++/52973, c++/53137, c++/53220,
	c++/53356, c++/53484, c++/53491, c++/53500, c++/53503,
	fortran/53521, libstdc++/52007, middle-end/47530, middle-end/48124,
	middle-end/48493, middle-end/52080, middle-end/52097,
	middle-end/52979, middle-end/53008, middle-end/53471,
	middle-end/53501, rtl-optimization/52528, rtl-optimization/53519,
	target/46261, target/52642, target/52667, tree-optimization/53438,
	tree-optimization/53505, tree-optimization/53516,
	tree-optimization/53550

* Fri May 25 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-6
- update from the 4.7 branch
  - PRs ada/52362, ada/52494, bootstrap/53183, c++/53209, c++/53301,
	c/53418, debug/52727, fortran/53310, fortran/53389, libstdc++/52700,
	middle-end/51071, middle-end/52584, middle-end/53460,
	rtl-optimization/52804, target/46098, target/53256, target/53272,
	target/53358, target/53385, target/53416, target/53435, target/53448,
	tree-optimization/53364, tree-optimization/53366,
	tree-optimization/53408, tree-optimization/53409,
	tree-optimization/53410, tree-optimization/53436,
	tree-optimization/53465

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5
- update from the 4.7 branch
  - PRs fortran/53111, fortran/53255, target/48496, target/52999,
	target/53228, tree-optimization/52633, tree-optimization/52870,
	tree-optimization/53195, tree-optimization/53239

* Fri May  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-4
- update from the 4.7 branch
  - PRs c++/53186, fortran/52864, libstdc++/53193, lto/52605,
	target/52684, target/53199, tree-optimization/53144
  - fix up gcc-ar, gcc-nm and gcc-ranlib (#818311, PR plugins/53126)

* Wed May  2 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-3
- update from the 4.7 branch
  - PRs bootstrap/52840, c++/38543, c++/50303, c++/50830, c++/53003,
	c/51527, c/52880, c/53060, fortran/53148, libstdc++/52689,
	libstdc++/52839, libstdc++/53027, libstdc++/53067, libstdc++/53115,
	middle-end/52939, middle-end/52999, middle-end/53084,
	middle-end/53136, rtl-optimization/53160, target/52932,
	target/53020, target/53033, target/53065, target/53120,
	target/53138, testsuite/52641, testsuite/53046,
	tree-optimization/53085, tree-optimization/53163,
	tree-optimizations/52891
- fix ARM SELECT_CC_MODE ICE (#817086, PR target/53187)
- fix predictive commoning debug info ICE (PR debug/53174)

* Mon Apr 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-2
- update from the 4.7 branch
  - PRs c++/52292, c++/52380, c++/52465, c++/52487, c++/52596, c++/52671,
	c++/52672, c++/52685, c++/52718, c++/52743, c++/52746, c++/52759,
	c++/52796, c++/52824, c++/52906, c/52682, c/52862, fortran/52452,
	fortran/52668, fortran/52893, libgfortran/52758, libitm/52854,
	libstdc++/52433, libstdc++/52476, libstdc++/52540, libstdc++/52591,
	libstdc++/52699, libstdc++/52799, libstdc++/52822, libstdc++/52924,
	libstdc++/52942, middle-end/51893, middle-end/52493,
	middle-end/52547, middle-end/52580, middle-end/52640,
	middle-end/52691, middle-end/52693, middle-end/52720,
	middle-end/52750, middle-end/52894, other/52545,
	rtl-optimization/52543, target/48596, target/48806, target/50310,
	target/52461, target/52484, target/52488, target/52496, target/52499,
	target/52505, target/52506, target/52507, target/52508, target/52610,
	target/52692, target/52698, target/52717, target/52736, target/52737,
	target/52775, tree-optimization/52406, tree-optimization/52678,
	tree-optimization/52701, tree-optimization/52754,
	tree-optimization/52835, tree-optimization/52943,
	tree-optimization/52969
- avoid duplicate pointers in C++ debug info due to injected class name
  (PR debug/45088)
- libjava locale fixes (#712013)

* Thu Mar 22 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-1
- update from the 4.7 branch
  - GCC 25th Anniversary 4.7.0 release
  - fix up new auto mangling

* Thu Mar 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.20
- update from the 4.7 branch
  - PRs fortran/52469, libitm/52526, libstdc++/52456, target/52450
  - fix __builtin_ir{ound,int}{,f,l} expansion (#803689, PR middle-end/52592)
  - fix up devirtualization (#802731, PR c++/52582)
- fix up user defined literal operator"" lookup (PR c++/52521)
- avoid false positive -Wunused-but-set-* warnings with __builtin_shuffle
  (PR c/52577)

* Thu Mar  8 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.19
- update from trunk and the 4.7 branch
  - PRs libstdc++/51785, middle-end/52419, middle-end/52443,
	middle-end/52463, rtl-optimization/52417, target/49939,
	target/51417, target/52408, target/52437, target/52481,
	testsuite/52297, tree-opt/52242, tree-optimization/52424,
	tree-optimization/52429, tree-optimization/52445
  - fix up mangling of operator"" (PR c++/52521)
- decrease size of .debug_ranges by ~ 20% (PR debug/51902)
- add support for demangling operator""
- package %{_prefix}/bin/gcc-{ar,nm,ranlib} binaries for LTO

* Tue Mar  6 2012 Jakub Jelinek <jakub@redhat.com> 4.6.3-2
- backport PLUGIN_FINISH_DECL event support
- adjust 22_locale/num_put/put/char/9780-2.cc testcase for recent
  locale data changes in glibc

* Tue Mar  6 2012 Jakub Jelinek <jakub@redhat.com> 4.6.3-1
- update from the 4.6 branch
  - GCC 4.6.3 release
  - PRs ada/46192, boehm-gc/48514, boehm-gc/52179, bootstrap/49907,
	bootstrap/50888, bootstrap/51686, bootstrap/51969, c++/50608,
	c++/50870, c++/50901, c++/51150, c++/51161, c++/51248, c++/51265,
	c++/51331, c++/51344, c++/51406, c++/51416, c++/51669, c++/51854,
	c++/51868, c++/52247, c/51339, c/51360, c/52181, c/52290, debug/48190,
	debug/49951, debug/51410, debug/51517, debug/51695, debug/51950,
	debug/52260, driver/48306, fortran/47545, fortran/49050,
	fortran/50408, fortran/50684, fortran/50923, fortran/51075,
	fortran/51218, fortran/51310, fortran/51338, fortran/51435,
	fortran/51448, fortran/51502, fortran/51550, fortran/51800,
	fortran/51904, fortran/51913, fortran/51948, fortran/51966,
	fortran/52012, fortran/52022, fortran/52093, fortran/52151,
	fortran/52335, fortran/52386, libjava/48512, libmudflap/40778,
	libstdc++/50862, libstdc++/50880, libstdc++/51083, libstdc++/51133,
	libstdc++/51142, libstdc++/51540, libstdc++/51626, libstdc++/51711,
	libstdc++/51795, libstdc++/52300, libstdc++/52309, libstdc++/52317,
	lto/41159, middle-end/44777, middle-end/45678, middle-end/48071,
	middle-end/48660, middle-end/50074, middle-end/51077,
	middle-end/51323, middle-end/51510, middle-end/51768,
	middle-end/51994, middle-end/52074, middle-end/52140,
	middle-end/52230, rtl-opt/37451, rtl-opt/37782,
	rtl-optimization/38644, rtl-optimization/47918,
	rtl-optimization/48721, rtl-optimization/49720,
	rtl-optimization/50396, rtl-optimization/51187,
	rtl-optimization/51374, rtl-optimization/51469,
	rtl-optimization/51767, rtl-optimization/51821,
	rtl-optimization/52060, rtl-optimization/52139, target/30282,
	target/40068, target/45233, target/48108, target/48743,
	target/49641, target/49992, target/50313, target/50493,
	target/50678, target/50691, target/50875, target/50906,
	target/50945, target/50979, target/51002, target/51106,
	target/51287, target/51345, target/51393, target/51408,
	target/51623, target/51643, target/51756, target/51835,
	target/51921, target/51934, target/52006, target/52107,
	target/52129, target/52199, target/52205, target/52238,
	target/52294, target/52330, target/52408, target/52425,
	testsuite/51511, testsuite/52296, tree-optimization/46886,
	tree-optimization/49536, tree-optimization/49642,
	tree-optimization/50031, tree-optimization/50078,
	tree-optimization/50569, tree-optimization/50622,
	tree-optimization/50969, tree-optimization/51042,
	tree-optimization/51070, tree-optimization/51118,
	tree-optimization/51315, tree-optimization/51466,
	tree-optimization/51485, tree-optimization/51583,
	tree-optimization/51624, tree-optimization/51759,
	tree-optimization/52286
- don't look for lto plugin/lto-wrapper if -E/-S/-c or in cpp (#787345)
- debuginfo related backports from trunk (PRs pch/51722, debug/52165,
  debug/52132)
- fix up ccp from optimizing away non-pure/const builtin passthrough calls
  with constant first argument (PR tree-optimization/51683)

* Wed Feb 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18
- update from trunk
  - PRs boehm-gc/48299, bootstrap/52397, bootstrap/52414, fortran/52386,
	libstdc++/52191, lto/52400, middle-end/51752, target/49448,
	target/51534, target/52148, target/52407, tree-optimization/52395,
	tree-optimization/52402, tree-optimization/53207
  - fix bootstrap on ppc*/arm/s390*

* Mon Feb 27 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.17
- update from trunk
  - PRs boehm-gc/52179, libffi/52223, libstdc++/52188, middle-end/52355,
	middle-end/52361, target/49263, target/49461, target/50580,
	target/52352, target/52375, target/52390, testsuite/52201,
	tree-optimization/52376

* Fri Feb 24 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.16
- update from trunk
  - fix vtable for std::num_get<char, std::istreambuf_iterator<char,
    std::char_traits<char> > > and vtable for std::num_get<wchar_t,
    std::istreambuf_iterator<wchar_t, std::char_traits<wchar_t> > >
    ABI breakage
  - PR bootstrap/52287

* Thu Feb 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.15
- update from trunk
  - PRs c/52290, fortran/52335, go/52349, libstdc++/50349, lto/50616,
	middle-end/52329, rtl-optimization/50063, target/18145, target/52330,
	tree-optimization/52019
- disable go on arm again, still not ready there

* Tue Feb 21 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.14
- update from trunk
  - PRs c++/51415, c++/52126, c++/52248, c++/52312, fortran/52295,
	libstdc++/47058, libstdc++/52189, libstdc++/52241, libstdc++/52300,
	libstdc++/52309, libstdc++/52317, middle-end/52141, middle-end/52314,
	rtl-optimization/52208, target/50166, target/51753, target/52137,
	target/52238, target/52294, testsuite/52229, translation/52232,
	translation/52234, translation/52245, translation/52246,
	translation/52262, translation/52273, tree-optimization/52285,
	tree-optimization/52286, tree-optimization/52298,
	tree-optimization/52318, tree-optimization/52324

* Thu Feb 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.13
- update from trunk
  - PRs boehm-gc/48514, bootstrap/52172, c++/39055, c++/51910, c++/52215,
	c/52181, c/52190, debug/52165, debug/52260, driver/48524,
	fortran/32380, fortran/52151, go/48411, go/51874, libffi/52221,
	libitm/52042, libitm/52220, libstdc++/51368, lto/52178,
	middle-end/48600, middle-end/51867, middle-end/51929,
	middle-end/52140, middle-end/52142, middle-end/52177,
	middle-end/52209, middle-end/52214, middle-end/52230,
	rtl-optimization/52175, target/51921, target/52146, target/52199,
	target/52205, target/52261, testsuite/50076, translation/52193,
	translation/52211, translation/52264, tree-optimization/50031,
	tree-optimization/50561, tree-optimization/52210,
	tree-optimization/52244, tree-optimization/52255
  - fix asm goto handling in templates (#790221, PR c++/52247)
- reenable go on ppc/ppc64/s390/s390x/arm

* Wed Feb  8 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.12
- update from trunk
  - PRs c++/52035, fortran/51514, gcov-profile/52150, libstdc++/51296,
	libstdc++/51906, middle-end/24306, middle-end/51994,
	middle-end/52074, rtl-optimization/52139, rtl-optimization/52170,
	target/40068, target/52152, target/52154, target/52155,
	tree-optimization/46886
  - fix up build on ppc*
  - don't look for lto plugin/lto-wrapper if -E/-S/-c or in cpp
- move liblto_plugin.so* back into gcc subpackage

* Mon Feb  6 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.11
- update from trunk
  - PRs bootstrap/52039, bootstrap/52041, bootstrap/52058, c++/48680,
	c++/51327, c++/51370, c++/51852, c++/52043, c++/52088, c/52118,
	debug/52001, debug/52027, debug/52048, fortran/32373, fortran/41587,
	fortran/41600, fortran/46356, fortran/48705, fortran/48847,
	fortran/51754, fortran/51808, fortran/51870, fortran/51943,
	fortran/51946, fortran/51953, fortran/51958, fortran/51970,
	fortran/51972, fortran/51977, fortran/52012, fortran/52013,
	fortran/52016, fortran/52022, fortran/52024, fortran/52029,
	fortran/52038, fortran/52093, fortran/52102, go/47656, go/48501,
	libitm/51822, libjava/48512, libstdc++/49445, libstdc++/51649,
	libstdc++/51795, libstdc++/51798, libstdc++/51811, libstdc++/51956,
	libstdc++/52068, libstdc++/52104, libstdc++/52119, libstdc++/52128,
	middle-end/43967, middle-end/47982, middle-end/48071,
	middle-end/51389, middle-end/51959, middle-end/51998,
	middle-end/52047, rtl-optimization/49800, rtl-optimization/51374,
	rtl-optimization/51978, rtl-optimization/52092,
	rtl-optimization/52095, rtl-optimization/52113, target/51500,
	target/51835, target/51871, target/51920, target/51974, target/52079,
	target/52107, target/52125, target/52129, testsuite/51875,
	testsuite/52011, tree-optimization/48794, tree-optimization/50444,
	tree-optimization/50955, tree-optimization/50969,
	tree-optimization/51528, tree-optimization/51990,
	tree-optimization/52020, tree-optimization/52028,
	tree-optimization/52045, tree-optimization/52046,
	tree-optimization/52073, tree-optimization/52091,
	tree-optimization/52115
  - fix i?86 mem += reg; mem cmp 0 8-bit peephole2 (#786570, PR target/52086)
  - fix fortran ICE on elemental call (#785433, PR fortran/52059)
- fix up /lib/cpp symlink for UsrMove (#787460)
- move LTO plugin into cpp subpackage (#787345)
- fix debug ICE with i387 reg-stack (#787518, PR debug/52132)
- fix ARM combine bug (PR rtl-optimization/52060)
- fix a DWARF4 .debug_types DIE cloning bug (PR debug/51950)

* Sat Feb  4 2012 Cristian Gafton <gafton@amazon.com> - 4.6.2-1%{?dist}
- update spec to create an alternate compile to the main system gcc

* Thu Jan 26 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.10
- update from trunk
  - PRs bootstrap/51985, c++/51223, c++/51812, c++/51917, c++/51928,
	c++/51930, c++/51973, c++/51992, driver/47249, fortran/51966,
	fortran/51995, libstdc++/49829, lto/51698, middle-end/45678,
	middle-end/51986, rtl-optimization/48308, rtl-optimization/48374
  - fix data-ref handling of non-volatile inline asms (#784242,
    PR tree-optimization/51987)
- fix ARM ICE with invalid peephole (#784748, PR target/52006)

* Mon Jan 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.9
- update from trunk
  - PRs ada/46192, c++/51344, c++/51398, c++/51402, c++/51832, c++/51919,
	c++/51922, debug/45682, fortran/50556, fortran/51056, fortran/51904,
	fortran/51913, fortran/51948, libgcj/23182, libgfortran/51899,
	libitm/51830, libstdc++/50982, lto/51916, middle-end/45416,
	rtl-optimization/40761, rtl-optimization/51924, target/47096,
	target/49868, target/50313, target/50887, target/51106, target/51819,
	target/51900, target/51915, target/51931, target/51934,
	testsuite/51941, tree-optimization/51895, tree-optimization/51903,
	tree-optimization/51914, tree-optimization/51949
  - fix REE pass (#783481, PR rtl-optimization/51933)
  - further overload fixes with using decls (#783586, PR c++/51925)
- fix ICE during expansion with BLKmode MEM_REF (#782868, PR middle-end/51895)
- fix ppc64 profiledbootstrap (PR target/51957)
- revert broken stack layout change (PR tree-optimization/46590)
- fix ARM ICE on neon insn splitting (PR target/51968)

* Thu Jan 19 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.8
- update from trunk
  - PRs bootstrap/50237, c++/51225, c++/51889, fortran/48426, fortran/51634,
	go/50656, libmudflap/40778, libstdc++/51845, libstdc++/51866,
	lto/51280, middle-end/51192, rtl-optimization/48496,
	rtl-optimization/51505, tree-optimization/37997,
	tree-optimization/46590
- fix a reload bug on s390 (#773565, PR rtl-optimization/51856)

* Tue Jan 17 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.7
- update from trunk
  - PRs bootstrap/51860, c++/14179, c++/20681, c++/50012, c++/51403,
	c++/51620, c++/51633, c++/51714, c++/51777, c++/51813, c++/51827,
	c++/51854, c++/51868, c/12245, fortran/36755, fortran/48351,
	fortran/51800, fortran/51809, fortran/51816, fortran/51842,
	fortran/51869, libitm/51173, libitm/51855, middle-end/51782,
	middle-end/8081, other/51165, rtl-optimization/51821, target/47852,
	target/50925, target/51756, tree-optimization/51865
  - fix up ppc64 bootstrap with -mminimal-toc (#773040, PR bootstrap/51872)
  - fix up -ftree-tail-merge (#782231, PR tree-optimization/51877)
- package up arm and sparc specific headers (#781765)
- enable libitm and disable go on ppc/ppc64
- fix up big-endian libstdc++ miscompilation (PR middle-end/50325)
- fix up arm neon vectorization ICEs (PR target/51876)

* Thu Jan 12 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.6
- update from trunk
  - PRs ada/41929, bootstrap/51705, bootstrap/51796, c++/47450,
	c++/48051, c++/50855, c++/51322, c++/51433, c++/51565,
	c++/51613, c++/51614, c++/51818, c++/6057, debug/51471,
	fortran/51057, fortran/51578, fortran/51616, fortran/51652,
	fortran/51758, fortran/51791, fortran/51792, gcov-profile/50127,
	gcov-profile/51715, gcov-profile/51717, libstdc++/51673,
	middle-end/51516, middle-end/51806, preprocessor/33919,
	preprocessor/51776, rtl-optimization/51271, target/47333,
	rarget/49868, testsuite/51655, tree-optimization/49642,
	tree-optimization/50913, tree-optimization/51600,
	tree-optimization/51680, tree-optimization/51694,
	tree-optimization/51759, tree-optimization/51775,
	tree-optimization/51799, tree-optimization/51801

* Fri Jan  6 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.5
- update from trunk
  - PRs c++/51541, fortran/48946, libstdc++/51504, lto/51774,
	rtl-optimization/51771, target/51681, tree-optimization/51315
- disable go on s390{,x}
- disable profiledbootstrap on arm and sparc* for now

* Thu Jan  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.4
- update from trunk
  - PRs bootstrap/51072, bootstrap/51648, debug/51746, debug/51762,
	lto/41576, lto/50490, middle-end/44777, middle-end/49710,
	middle-end/51472, middle-end/51761, middle-end/51764,
	middle-end/51768, other/51171, rtl-optimization/51767,
	tree-optimization/51624, tree-optimization/51760
- disable go on arm (#771482)
- enable profiledbootstrap

* Wed Jan  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.3
- update from trunk
  - PRs bootstrap/51006, bootstrap/51734, c++/29273, c++/51064, c++/51738,
	debug/51695, fortran/49693, fortran/50981, middle-end/51696,
	middle-end/51750, other/51163, other/51164, tree-optimization/49651
- fix up libitm.so.1

* Tue Jan  3 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.2
- update from trunk
  - PRs bootstrap/51686, bootstrap/51725, c++/15867, c++/16603, c++/20140,
	c++/23211, c++/51316, c++/51379, c++/51397, c++/51462, c++/51507,
	c++/51547, c++/51666, c++/51669, c++/51675, c++/51723, debug/51650,
	driver/48306, fortran/46262, fortran/46328, fortran/51052,
	fortran/51502, fortran/51529, fortran/51682, libfortran/51646,
	libgcj/49193, libstdc++/48362, libstdc++/49204, libstdc++/51608,
	libstdc++/51701, libstdc++/51711, lto/51650, middle-end/48641,
	middle-end/51200, middle-end/51212, middle-end/51252,
	middle-end/51730, other/51679, pch/51722, rtl-optimization/50396,
	rtl-optimization/51069, rtl-optimization/51667, target/27468,
	target/47643, target/51345, target/51552, target/51623, target/51643,
	target/51729, testsuite/50722, testsuite/51645, testsuite/51702,
	tree-optimization/43491, tree-optimization/51070,
	tree-optimization/51269, tree-optimization/51683,
	tree-optimization/51684, tree-optimization/51692,
	tree-optimization/51704, tree-optimization/51719

* Wed Dec 21 2011 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.1
- new package

* Thu Oct 27 2011 Jakub Jelinek <jakub@redhat.com> 4.6.2-1
- update from the 4.6 branch
  - GCC 4.6.2 release
  - PRs c++/44473, c++/49216, c++/49855, c++/49896, c++/50531, c++/50611,
	c++/50618, c++/50787, c++/50793, c/50565, debug/50816, fortran/47023,
	fortran/48706, fortran/50016, fortran/50273, fortran/50570,
	fortran/50585, fortran/50625, fortran/50659, fortran/50718,
	libobjc/49883, libobjc/50002, libstdc++/48698, middle-end/49801,
	middle-end/50326, middle-end/50386, obj-c++/48275, objc-++/48275,
	target/49049, target/49824, target/49965, target/49967, target/50106,
	target/50350, target/50652, target/50737, target/50788, target/50820,
	tree-optimization/49279, tree-optimization/50189,
	tree-optimization/50700, tree-optimization/50712,
	tree-optimization/50723
- add armv7hl configury options (#746843)
- add `gcc -print-file-name=rpmver` file with gcc NVRA for plugins
  (#744922)
- fix build against current glibc, ctype.h changes broke libjava compilation

* Sun Oct  2 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-10
- update from the 4.6 branch
  - PRs c++/20039, c++/40831, c++/42844, c++/46105, c++/48320, c++/50424,
	c++/50442, c++/50491, c++/50508, inline-asm/50571, libstdc++/49559,
	libstdc++/50509, libstdc++/50510, libstdc++/50529, middle-end/49886,
	target/50091, target/50341, target/50464, testsuite/50487,
	tree-optimization/49518, tree-optimization/49628,
	tree-optimization/49911, tree-optimization/50162,
	tree-optimization/50412, tree-optimization/50413,
	tree-optimization/50472
- recognize IVs with REFERENCE_TYPE in simple_iv similarly to
  IVs with POINTER_TYPE (#528578)
- return larger types for odd-sized precision in Fortran type_for_size
  langhook if possible

* Thu Sep  8 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-9
- update from the 4.6 branch
  - PRs c++/49267, c++/50089, c++/50157, c++/50207, c++/50220, c++/50224,
	c++/50234, c++/50255, c++/50309, c/50179, fortran/50163,
	libffi/49594, libfortran/50192, libstdc++/50268, middle-end/50116,
	middle-end/50266, target/50090, target/50202, target/50289,
	target/50310, tree-optimization/50178
- debug info related backports from the trunk
  - PRs debug/50191, debug/50215
- fix call site debug info on big endian targets (PR debug/50299)
- put libgcc.a into libgcc_s.so linker script also on arm (#733549)
- use %%{?fedora} instead of %%{fedora}, handle 0%%{?rhel} >= 7 like
  0%%{?fedora} >= 16

* Wed Aug 24 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-8
- update from the 4.6 branch
  - PRs c++/46862, c++/48993, c++/49669, c++/49921, c++/49988, c++/50024,
	c++/50054, c++/50086, fortran/49792, fortran/50050, fortran/50109,
	fortran/50129, fortran/50130, middle-end/49923, target/50001,
	target/50092, tree-optimization/48739
- build EH_SPEC_BLOCK with the same location as current function
  to help gcov (#732802, PR c++/50055)
- support used attribute on template class methods and static data
  members for forced instantiation (#722587)
- fix up location copying in the vectorizer (PR tree-optimization/50133)
- unshare CALL_INSN_FUNCTION_USAGE (PR middle-end/48722)
- fix up gthr*.h for -E -C (#713800)

* Thu Aug  4 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-7
- update from the 4.6 branch
  - PRs c++/43886, c++/49593, c++/49803, fortran/49885,
	tree-optimization/49948
- add self_spec support to specs
- add COPYING.RUNTIME to gcc and libgcc docs (#727809)
- SPARC entry_value fixes (PRs target/48220, debug/49815)
- fix up c-family headers in gcc-plugin-devel (#728011, PRs plugins/45348,
  plugins/46577, plugins/48425)

* Tue Aug  2 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-6
- update from the 4.6 branch
  - PRs c++/49260, c++/49924, libstdc++/49925, target/47908, target/49920
  - fix libquadmath on i686 (#726909)
- OpenMP 3.1 support (PR fortran/42041, PR fortran/46752)
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
- make -grecord-gcc-switches the default
%endif

* Sun Jul 31 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-5
- update from the 4.6 branch
  - PRs debug/49871, fortran/48876, fortran/49791, middle-end/49897,
	middle-end/49898, rtl-optimization/49799, target/47364
- don't attempt to size optimize -gdwarf-2 DW_AT_data_member_location
  from DW_OP_plus_uconst form

* Wed Jul 27 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-4
- update from the 4.6 branch
  - PRs ada/49819, c++/49785, debug/47393, fortran/49648, fortran/49708,
	middle-end/49675, middle-end/49732, target/39386, target/49600,
	target/49723, target/49746, testsuite/49753, tree-opt/49671,
	tree-optimization/45819, tree-optimization/49309,
	tree-optimization/49725, tree-optimization/49768
- require gmp-devel, mpfr-devel and libmpc-devel in gcc-plugin-devel
  (#725569)
- backport -grecord-gcc-switches (#507759, PR other/32998)
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
- more compact debug macro info for -g3 - .debug_macro section
- improve call site debug info for some floating point parameters
  passed on the stack (PR debug/49846)
%endif
- fix -mcmodel=large call constraints (PR target/49866, #725516)

* Fri Jul 15 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-3
- update from the 4.6 branch
  - PRs ada/46350, ada/48711, c++/49672, fortran/48926, fortran/49562,
	fortran/49690, fortran/49698, target/39633, target/46779,
	target/49487, target/49541, target/49621, tree-opt/49309,
	tree-optimization/49094, tree-optimization/49651
- backport -march=bdver2 and -mtune=bdver2 support
%if 0%{?fedora} < 16 || 0%{?rhel} >= 7
- use ENTRY_VALUE RTLs internally to improve generated debug info,
  just make sure to remove it from possible options before emitting
  var-tracking notes
%endif

* Fri Jul  8 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-2
- update from the 4.6 branch
  - PRs ada/49511, bootstrap/23656, bootstrap/49247, c++/48157, c/48825,
	c++/49418, c++/49440, c++/49528, c++/49598, c/49644, debug/49262,
	debug/49522, fortran/49466, fortran/49479, fortran/49623,
	libffi/46660, libfortran/49296, middle-end/49640, other/47733,
	regression/47836, rtl-optimization/49014, rtl-optimization/49472,
	rtl-optimization/49619, target/34734, target/47997, target/48273,
	target/49089, target/49335, target/49660, testsuite/49643,
	tree-optimization/38752, tree-optimization/49516,
	tree-optimization/49539, tree-optimization/49572,
	tree-optimization/49615, tree-optimization/49618
  - decrease compiler memory and time requirements on Fortran DATA
    with many times repeated initializers (#716721, PR fortran/49540)
- backport some debuginfo improvements and fixes
  - PRs debug/49364, debug/49602
  - fix typed DWARF stack ICE (#717240, PR49567)
- backport __builtin_assume_aligned support (#713586)
- backport further C++ FE improvements for heavy overloading use
  (#651098, PR c++/48481)

* Mon Jun 27 2011 Jakub Jelinek <jakub@redhat.com> 4.6.1-1
- update from the 4.6 branch
  - GCC 4.6.1 release
  - PRs c++/33840, c++/49117, c++/49134, c++/49229, c++/49251, c++/49264,
	c++/49276, c++/49290, c++/49298, c++/49369, c++/49482, c++/49507,
	debug/47590, debug/48459, fortran/47601, fortran/48699,
	fortran/49074, fortran/49103, fortran/49112, fortran/49268,
	fortran/49324, fortran/49417, gcov-profile/49299, middle-end/49191,
	rtl-optimization/48542, rtl-optimization/49235, target/44618,
	target/48454, target/49186, target/49238, target/49307, target/49411,
	target/49461, testsuite/49432, tree-optimization/48613,
	tree-optimization/48702, tree-optimization/49038,
	tree-optimization/49115, tree-optimization/49243,
	tree-optimization/49419
  - fix GCSE (#712480, PR rtl-optimization/49390)
- use rm -f and mv -f in split-debuginfo.sh (#716664)
- backport some debuginfo improvements and bugfixes
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
  - improve debug info for IPA-SRA through DW_OP_GNU_parameter_ref
    (PR debug/47858)
  - emit DW_OP_GNU_convert <0> as convert to untyped
%endif
  - emit .debug_loc empty ranges for parameters that are
    modified even before first insn in a function (PR debug/49382)
  - fix debug ICE on s390x (PR debug/49544)
  - VTA ICE fix (PR middle-end/49308)
- balance work in #pragma omp for schedule(static) better (PR libgomp/49490)

* Fri Jun  3 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-10
- update from the 4.6 branch
  - PRs fortran/45786, fortran/49265, middle-end/48953, middle-end/48985,
	tree-optimization/49093
- backport some debuginfo improvements
  - PRs debug/47919, debug/47994, debug/49250
- decrease C++ FE memory usage on code with heavy overloading
  (#651098, PR c++/48481)

* Mon May 30 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-9
- update from the 4.6 branch
  - PRs c++/44311, c++/44994, c++/45080, c++/45401, c++/45418, c++/45698,
	c++/46005, c++/46245, c++/46696, c++/47049, c++/47184, c++/47277,
	c++/48284, c++/48292, c++/48424, c++/48935, c++/49156, c++/49165,
	c++/49176, c++/49223, fortran/48955, libobjc/48177, libstdc++/49141,
	target/43700, target/43995, target/44643, target/45263,
	tree-optimization/44897, tree-optimization/49161,
	tree-optimization/49217, tree-optimization/49218
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
- default to -gdwarf-4 -fno-debug-types-section instead of -gdwarf-3
- backport DW_OP_GNU_entry_value support
  (PRs rtl-optimization/48826, debug/48902, bootstrap/48148,
   debug/48203, bootstrap/48168, debug/48023, debug/48178,
   debug/48163, debug/48160, bootstrap/48153, middle-end/48152,
   bootstrap/48148, debug/45882)
- backport DW_OP_GNU_{{const,regval,deref}_type,convert,reinterpret}
  support (PRs debug/48928, debug/48853)
%endif
- split off debuginfo for libgcc_s, libstdc++ and libgomp into
  gcc-base-debuginfo subpackage (#706973)
- run ldconfig in libgcc %%postun, drop libcc_post_upgrade,
  instead write the script in <lua> (#705832)

* Wed May 25 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-8
- update from the 4.6 branch
  - PRs bootstrap/49086, c++/47263, c++/47336, c++/47544, c++/48522,
	c++/48617, c++/48647, c++/48736, c++/48745, c++/48780, c++/48859,
	c++/48869, c++/48873, c++/48884, c++/48945, c++/48948, c++/49042,
	c++/49043, c++/49066, c++/49082, c++/49105, c++/49136, c/49120,
	debug/48159, debug/49032, fortran/48889, libstdc++/49058, lto/48207,
	lto/48703, lto/49123, middle-end/48973, middle-end/49029,
	preprocessor/48677, target/48986, target/49002, target/49104,
	target/49128, target/49133, tree-optimization/48172,
	tree-optimization/48794, tree-optimization/48822,
	tree-optimization/48975, tree-optimization/49000,
	tree-optimization/49018, tree-optimization/49039,
	tree-optimization/49073, tree-optimization/49079
  - ppc V2DImode ABI fix (#705764, PR target/48857)
  - fix ppc var-tracking ICE (#703888, PR debug/48967)

* Mon May  9 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-7
- update from the 4.6 branch
  - PRs ada/48844, c++/40975, c++/48089, c++/48446, c++/48656, c++/48749,
	c++/48838, c++/48909, c++/48911, fortran/48112, fortran/48279,
	fortran/48462, fortran/48720, fortran/48746, fortran/48788,
	fortran/48800, fortran/48810, fortran/48894, libgfortran/48030,
	libstdc++/48750, libstdc++/48760, lto/48846, middle-end/48597,
	preprocessor/48192, target/48226, target/48252, target/48262,
	target/48774, target/48900, tree-optimization/48809
- fix ICE with references in templates (PR c++/48574)
- disable tail call optimization if tail recursion needs accumulators
  (PR PR tree-optimization/48837)

* Thu Apr 28 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-6
- update from the 4.6 branch
  - PRs c++/42687, c++/46304, c++/48046, c++/48657, c++/48707, c++/48726,
	c/48685, c/48716, c/48742, debug/48768, fortran/47976,
	fortran/48588, libstdc++/48521, lto/48148, lto/48492,
	middle-end/48695, other/48748, preprocessor/48740, target/48288,
	target/48708, target/48723, tree-optimization/48611,
	tree-optimization/48717, tree-optimization/48731,
	tree-optimization/48734

* Tue Apr 19 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-5
- update from the 4.6 branch
  - PRs c++/48537, c++/48632, fortran/48360, fortran/48456,
	libfortran/47571, libstdc++/48476, libstdc++/48631,
	libstdc++/48635, lto/48538, middle-end/46364, middle-end/48661,
	preprocessor/48248, target/48366, target/48605, target/48614,
	target/48678, testsuite/48675, tree-optimization/48616
  - fix calling functor or non-pointer-to-member through
    overloaded pointer-to-member operator (#695567, PR c++/48594)

* Wed Apr 13 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-4
- update from the 4.6 branch
  - PRs c++/48450, c++/48452, c++/48468, c++/48500, c++/48523, c++/48528,
	c++/48534, c++/48570, c++/48574, c/48517, libstdc++/48465,
	libstdc++/48541, libstdc++/48566, target/47829, target/48090,
	testsuite/48506, tree-optimization/48195, tree-optimization/48377
  - fix combiner with -g (#695019, PR rtl-optimization/48549)
  - fix OpenMP atomic __float128 handling on i?86 (#696129,
    PR middle-end/48591)

* Fri Apr  8 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-3
- update from the 4.6 branch
  - PRs bootstrap/48431, c++/48280, debug/48343, debug/48466, fortran/48117,
	fortran/48291, libstdc++/48398, middle-end/48335,
	rtl-optimization/48143, rtl-optimization/48144, target/16292,
	target/48142
  - don't ICE because of empty partitions during LTO (#688767, PR lto/48246)
- don't emit DW_AT_*_pc for CUs without any code

* Thu Mar 31 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-2
- update from the 4.6 branch
  - PRs c++/47504, c++/47570, c++/47999, c++/48166, c++/48212, c++/48265,
	c++/48281, c++/48289, c++/48296, c++/48313, c++/48319, c++/48369,
	debug/48041, debug/48253, preprocessor/48248, target/48349
- add -fno-debug-types-section switch
- don't emit .debug_abbrev section if it is empty and unused

* Tue Mar 29 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-1
- update from the 4.6 branch
  - GCC 4.6.0 release
  - PRs c/42544, c/48197, debug/48204, middle-end/48031,
	middle-end/48134, middle-end/48269, other/48179, other/48221,
	other/48234, rtl-optimization/48156, target/47553,
	target/48237, testsuite/48251, tree-optimization/48228
  - improve RTL DSE speed with large number of stores (#684900,
    PR rtl-optimization/48141)
- add gnative2ascii binary and man page to libgcj

* Mon Mar 21 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-0.15
- update from the 4.6 branch
  - PRs bootstrap/45381, bootstrap/48135
- fix s390 ICE during address delegitimization (PR target/48213, #689266)

* Fri Mar 18 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-0.14
- update from the 4.6 branch
  - PRs bootstrap/48161, c++/48113, c++/48115, c++/48132, debug/47510,
	debug/48176, libstdc++/48123, middle-end/47405, middle-end/48165,
	target/46778, target/46788, target/48171
- update libstdc++ pretty printers from trunk

* Tue Mar 15 2011 Jakub Jelinek <jakub@redhat.com> 4.6.0-0.13
- update from trunk and the 4.6 branch
  - PRs bootstrap/48000, bootstrap/48102, c++/44629, c++/45651, c++/46220,
	c++/46803, c++/47125, c++/47144, c++/47198, c++/47488, c++/47705,
	c++/47808, c++/47957, c++/47971, c++/48003, c++/48008, c++/48015,
	c++/48029, c++/48035, c++/48069, c/47786, debug/47881, debug/48043,
	fortran/47552, fortran/47850, fortran/48054, fortran/48059,
	libfortran/48066, libgfortran/48047, libstdc++/48038, libstdc++/48114,
	lto/47497, lto/48073, lto/48086, middle-end/47968, middle-end/47975,
	middle-end/48044, middle-end/48098, rtl-optimization/47866,
	rtl-optimization/47899, target/45413, target/47719, target/47862,
	target/47986, target/48032, target/48053, testsuite/47954,
	tree-optimization/47127, tree-optimization/47278,
	tree-optimization/47714, tree-optimization/47967,
	tree-optimization/48022, tree-optimization/48063,
	tree-optimization/48067
  - fix var-tracking ICE on s390x (#682410, PR debug/47991)
