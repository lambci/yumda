# Shared haskell libraries are supported for x86* archs
# (disabled for other archs in ghc-rpm-macros)

# To bootstrap build a new version of ghc, uncomment the following:
#%%global ghc_bootstrapping 1
#%%global without_testsuite 1
### either:
#%%{?ghc_bootstrap}
### or for shared libs:
#%%{?ghc_test}
### uncomment to generate haddocks for bootstrap
#%%undefine without_haddock

%global space %(echo -n ' ')
%global BSDHaskellReport BSD%{space}and%{space}HaskellReport

Name: ghc
# part of haskell-platform
# ghc must be rebuilt after a version bump to avoid ABI change problems
Version: 7.6.3
# Since library subpackages are versioned:
# - release can only be reset if *all* library versions get bumped simultaneously
#   (sometimes after a major release)
# - minor release numbers for a branch should be incremented monotonically
Release: 26.4%{?dist}
Summary: Glasgow Haskell Compiler

License: %BSDHaskellReport
URL: http://haskell.org/ghc/
Source0: http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
%if %{undefined without_testsuite}
Source2: http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-testsuite.tar.bz2
%endif
Source3: ghc-doc-index.cron
Source4: ghc-doc-index
# absolute haddock path (was for html/libraries -> libraries)
Patch1:  ghc-gen_contents_index-haddock-path.patch
# fedora does not allow copy libraries
Patch4:  ghc-use-system-libffi.patch
# fix dynamic linking of executables using Template Haskell
Patch9:  Cabal-fix-dynamic-exec-for-TH.patch
# add libffi include dir to ghc wrapper for archs using gcc/llc
Patch10: ghc-wrapper-libffi-include.patch
# disable building HS*.o libs for ghci
Patch12: ghc-7.4.2-Cabal-disable-ghci-libs.patch
# fix compilation with llvm-3.3
Patch13: ghc-llvmCodeGen-empty-array.patch
# stop warnings about unsupported version of llvm
Patch14: ghc-7.6.3-LlvmCodeGen-llvm-version-warning.patch
# fix hang on ppc64 and s390x (upstream in 7.8)
Patch15: ghc-64bit-bigendian-rts-hang-989593.patch
# unversion library html docdirs
Patch16: ghc-cabal-unversion-docdir.patch
# fix libffi segfaults on 32bit (upstream in 7.8)
Patch17: ghc-7.6.3-rts-Adjustor-32bit-segfault.patch
# add .note.GNU-stack to assembly output to avoid execstack (#973512)
# (disabled for now since it changes libghc ABI and fix only works for i686)
#Patch18: ghc-7.6-driver-Disable-executable-stack-for-the-linker-note.patch
# changes for ppc64le committed upstream for 7.8.3
# (https://ghc.haskell.org/trac/ghc/ticket/8965)
Patch19: ghc-ppc64el.patch
# warning "_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE"
Patch20: ghc-glibc-2.20_BSD_SOURCE.patch
# Debian patch
Patch21: ghc-arm64.patch
Patch22: ghc-7.6.3-armv7-VFPv3D16--NEON.patch

%global Cabal_ver 1.16.0
%global array_ver 0.4.0.1
%global base_ver 4.6.0.1
%global bin_package_db_ver 0.0.0.0
%global binary_ver 0.5.1.1
%global bytestring_ver 0.10.0.2
%global containers_ver 0.5.0.0
%global deepseq_ver 1.3.0.1
%global directory_ver 1.2.0.1
%global filepath_ver 1.3.0.1
%global ghc_prim_ver 0.3.0.0
%global haskell2010_ver 1.1.1.0
%global haskell98_ver 2.0.0.2
%global hoopl_ver 3.9.0.0
%global hpc_ver 0.6.0.0
%global integer_gmp_ver 0.5.0.0
%global old_locale_ver 1.0.0.5
%global old_time_ver 1.1.0.1
%global pretty_ver 1.1.1.0
%global process_ver 1.1.0.2
%global template_haskell_ver 2.8.0.0
%global time_ver 1.4.0.1
%global unix_ver 2.6.0.1

# fedora ghc has been bootstrapped on
# %{ix86} x86_64 ppc alpha sparcv9 ppc64 armv7hl armv5tel s390 s390x
# see ghc_arches defined in /etc/rpm/macros.ghc-srpm by redhat-rpm-macros
ExcludeArch: sparc64
Obsoletes: ghc-dph-base < 0.5, ghc-dph-base-devel < 0.5, ghc-dph-base-prof < 0.5
Obsoletes: ghc-dph-par < 0.5, ghc-dph-par-devel < 0.5, ghc-dph-par-prof < 0.5
Obsoletes: ghc-dph-prim-interface < 0.5, ghc-dph-prim-interface-devel < 0.5, ghc-dph-interface-prim-prof < 0.5
Obsoletes: ghc-dph-prim-par < 0.5, ghc-dph-prim-par-devel < 0.5, ghc-dph-prim-par-prof < 0.5
Obsoletes: ghc-dph-prim-seq < 0.5, ghc-dph-prim-seq-devel < 0.5, ghc-dph-prim-seq-prof < 0.5
Obsoletes: ghc-dph-seq < 0.5, ghc-dph-seq-devel < 0.5, ghc-dph-seq-prof < 0.5
Obsoletes: ghc-feldspar-language < 0.4, ghc-feldspar-language-devel < 0.4, ghc-feldspar-language-prof < 0.4
%if %{undefined ghc_bootstrapping}
BuildRequires: ghc-compiler = %{version}
%endif
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
BuildRequires: ghc-rpm-macros-extra
%else
BuildRequires: ghc-rpm-macros
%endif
BuildRequires: ghc-bytestring-devel
BuildRequires: ghc-containers-devel
BuildRequires: ghc-directory-devel
BuildRequires: ghc-haskell98-devel
BuildRequires: ghc-pretty-devel
BuildRequires: ghc-process-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
# for internal terminfo
BuildRequires: ncurses-devel
# for manpage and docs
BuildRequires: libxslt, docbook-style-xsl
%if %{undefined without_testsuite}
BuildRequires: python
%endif
%ifarch armv7hl armv5tel
BuildRequires: llvm34
%endif
%ifarch ppc64le aarch64
# for patch19 and patch21
BuildRequires: autoconf
%endif
%ifarch armv7hl
# patch22
BuildRequires: autoconf, automake
%endif
Requires: ghc-compiler = %{version}-%{release}
%if %{undefined without_haddock}
Requires: ghc-doc-index = %{version}-%{release}
%endif
Requires: ghc-libraries = %{version}-%{release}
Requires: ghc-ghc-devel = %{version}-%{release}

%description
GHC is a state-of-the-art, open source, compiler and interactive environment
for the functional language Haskell. Highlights:

- GHC supports the entire Haskell 2010 language plus various extensions.
- GHC has particularly good support for concurrency and parallelism,
  including support for Software Transactional Memory (STM).
- GHC generates fast code, particularly for concurrent programs
  (check the results on the "Computer Language Benchmarks Game").
- GHC works on several platforms including Windows, Mac, Linux,
  most varieties of Unix, and several different processor architectures.
- GHC has extensive optimisation capabilities,
  including inter-module optimisation.
- GHC compiles Haskell code either directly to native code or using LLVM
  as a back-end. GHC can also generate C code as an intermediate target for
  porting to new platforms. The interactive environment compiles Haskell to
  bytecode, and supports execution of mixed bytecode/compiled programs.
- Profiling is supported, both by time/allocation and heap profiling.
- GHC comes with core libraries, and thousands more are available on Hackage.

%package compiler
Summary: GHC compiler and utilities
License: BSD
Requires: gcc%{?_isa}
Requires: ghc-base-devel%{?_isa}
# for alternatives
Requires(post): chkconfig
Requires(postun): chkconfig
# added in f14
Obsoletes: ghc-doc < 6.12.3-4
%ifarch armv7hl armv5tel
Requires: llvm34
%endif

%description compiler
The package contains the GHC compiler, tools and utilities.

The ghc libraries are provided by ghc-libraries.
To install all of ghc (including the ghc library),
install the main ghc package.

%if %{undefined without_haddock}
%package doc-index
Summary: GHC library development documentation indexing
License: BSD
Requires: ghc-compiler = %{version}-%{release}
Requires: crontabs

%description doc-index
The package provides a cronjob for re-indexing installed library development
documention.
%endif

%global ghc_version_override %{version}

# EL7 rpm supports fileattrs ghc.attr
%if 0%{?rhel} && 0%{?rhel} < 7
# needs ghc_version_override for bootstrapping
%global _use_internal_dependency_generator 0
%global __find_provides %{_rpmconfigdir}/ghc-deps.sh --provides %{buildroot}%{ghclibdir}
%global __find_requires %{_rpmconfigdir}/ghc-deps.sh --requires %{buildroot}%{ghclibdir}
%endif

%global ghc_pkg_c_deps ghc-compiler = %{ghc_version_override}-%{release}

%if %{defined ghclibdir}
%ghc_lib_subpackage Cabal %{Cabal_ver}
%ghc_lib_subpackage -l %BSDHaskellReport array %{array_ver}
%ghc_lib_subpackage -l %BSDHaskellReport -c gmp-devel%{?_isa},libffi-devel%{?_isa} base %{base_ver}
%ghc_lib_subpackage binary %{binary_ver}
%ghc_lib_subpackage bytestring %{bytestring_ver}
%ghc_lib_subpackage -l %BSDHaskellReport containers %{containers_ver}
%ghc_lib_subpackage -l %BSDHaskellReport deepseq %{deepseq_ver}
%ghc_lib_subpackage -l %BSDHaskellReport directory %{directory_ver}
%ghc_lib_subpackage filepath %{filepath_ver}
%define ghc_pkg_obsoletes ghc-bin-package-db-devel < 0.0.0.0-12
# in ghc not ghc-libraries:
%ghc_lib_subpackage -x ghc %{ghc_version_override}
%undefine ghc_pkg_obsoletes
%ghc_lib_subpackage -l HaskellReport haskell2010 %{haskell2010_ver}
%ghc_lib_subpackage -l HaskellReport haskell98 %{haskell98_ver}
%ghc_lib_subpackage hoopl %{hoopl_ver}
%ghc_lib_subpackage hpc %{hpc_ver}
%ghc_lib_subpackage -l %BSDHaskellReport old-locale %{old_locale_ver}
%ghc_lib_subpackage -l %BSDHaskellReport old-time %{old_time_ver}
%ghc_lib_subpackage pretty %{pretty_ver}
%define ghc_pkg_obsoletes ghc-process-leksah-devel < 1.0.1.4-14
%ghc_lib_subpackage -l %BSDHaskellReport process %{process_ver}
%undefine ghc_pkg_obsoletes
%ghc_lib_subpackage template-haskell %{template_haskell_ver}
%ghc_lib_subpackage time %{time_ver}
%ghc_lib_subpackage unix %{unix_ver}
%endif

%global version %{ghc_version_override}

%package libraries
Summary: GHC development libraries meta package
License: %BSDHaskellReport
Requires: ghc-compiler = %{version}-%{release}
Obsoletes: ghc-devel < %{version}-%{release}
Provides: ghc-devel = %{version}-%{release}
Obsoletes: ghc-prof < %{version}-%{release}
Provides: ghc-prof = %{version}-%{release}
# since f15
Obsoletes: ghc-libs < 7.0.1-3
%{?ghc_packages_list:Requires: %(echo %{ghc_packages_list} | sed -e "s/\([^ ]*\)-\([^ ]*\)/ghc-\1-devel = \2-%{release},/g")}

%description libraries
This is a meta-package for all the development library packages in GHC
except the ghc library, which is installed by the toplevel ghc metapackage.


%prep
%setup -q -n %{name}-%{version} %{!?without_testsuite:-b2}

# gen_contents_index: use absolute path for haddock
%patch1 -p1 -b .orig

# make sure we don't use these
rm -r ghc-tarballs/{mingw*,perl}
# use system libffi
%patch4 -p1 -b .libffi
rm -r ghc-tarballs/libffi
mkdir -p rts/dist/build
ln -s $(pkg-config --variable=includedir libffi)/*.h rts/dist/build

%patch9 -p1 -b .orig

%ifnarch %{ix86} x86_64
%patch10 -p1 -b .10-ffi
%endif

%patch12 -p1 -b .orig

%patch13 -p1 -b .orig

%ifarch armv7hl armv5tel
%patch14 -p1 -b .orig
%endif

%ifarch ppc64 s390x
%patch15 -p1 -b .orig
%endif

%if 0%{?fedora} >= 21
%patch16 -p1 -b .orig
%endif

%patch17 -p0 -b .orig

#%%patch18 -p1 -b .orig

%ifarch ppc64le
%patch19 -p1 -b .orig
%endif

%patch20 -p1 -b .orig

%ifarch aarch64
%patch21 -p1 -b .orig
%endif

%ifarch armv7hl
%patch22 -p1 -b .orig
%endif


%global gen_contents_index gen_contents_index.orig
%if %{undefined without_haddock}
if [ ! -f "libraries/%{gen_contents_index}" ]; then
  echo "Missing libraries/%{gen_contents_index}, needed at end of %%install!"
  exit 1
fi
%endif


%build
# http://hackage.haskell.org/trac/ghc/wiki/Platforms
# cf https://github.com/gentoo-haskell/gentoo-haskell/tree/master/dev-lang/ghc
cat > mk/build.mk << EOF
%if %{undefined ghc_bootstrapping}
%ifnarch armv7hl armv5tel
BuildFlavour = perf
%else
BuildFlavour = perf-llvm
%endif
%else
%ifnarch armv7hl armv5tel
BuildFlavour = quick-llvm
%else
BuildFlavour = quick
%endif
%endif
GhcLibWays = v %{!?ghc_without_shared:dyn} %{!?without_prof:p}
%if %{defined without_haddock}
HADDOCK_DOCS = NO
%endif
%if %{defined without_manual}
BUILD_DOCBOOK_HTML = NO
%endif
## for verbose build output
#GhcStage1HcOpts=-v4
## enable RTS debugging:
## (http://ghc.haskell.org/trac/ghc/wiki/Debugging/RuntimeSystem)
#EXTRA_HC_OPTS=-debug
EOF

# note %%configure induces cross-build due to different target/host/build platform names
# --with-gcc=%{_bindir}/gcc is to avoid ccache hardcoding problem when bootstrapping 
%ifarch ppc64le aarch64 armv7hl
for i in $(find . -name config.guess -o -name config.sub) ; do
    [ -f /usr/lib/rpm/redhat/$(basename $i) ] && %{__rm} -f $i && %{__cp} -fv /usr/lib/rpm/redhat/$(basename $i) $i
done
autoreconf
%endif
export CFLAGS="${CFLAGS:-%optflags}"
export LDFLAGS="${LDFLAGS:-%__global_ldflags}"
./configure --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} \
  --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} \
  --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} \
  --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} \
  --with-gcc=%{_bindir}/gcc \
%ifarch armv7hl armv5tel
  --with-llc=%{_bindir}/llc-3.4 --with-opt=%{_bindir}/opt-3.4 \
%endif
%{nil}

# utf8 is needed when building with verbose output
LANG=en_US.utf8 make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install

for i in %{ghc_packages_list}; do
name=$(echo $i | sed -e "s/\(.*\)-.*/\1/")
ver=$(echo $i | sed -e "s/.*-\(.*\)/\1/")
%ghc_gen_filelists $name $ver
echo "%doc libraries/$name/LICENSE" >> ghc-$name.files
done

# ghc-base should own ghclibdir
echo "%dir %{ghclibdir}" >> ghc-base.files

%ghc_gen_filelists bin-package-db %{bin_package_db_ver}
%ghc_gen_filelists ghc %{ghc_version_override}
%ghc_gen_filelists ghc-prim %{ghc_prim_ver}
%ghc_gen_filelists integer-gmp %{integer_gmp_ver}

%define merge_filelist()\
cat ghc-%1.files >> ghc-%2.files\
cat ghc-%1-devel.files >> ghc-%2-devel.files\
cp -p libraries/%1/LICENSE libraries/LICENSE.%1\
echo "%doc libraries/LICENSE.%1" >> ghc-%2.files

%merge_filelist integer-gmp base
%merge_filelist ghc-prim base
%merge_filelist bin-package-db ghc

# add rts libs
%if %{undefined ghc_without_shared}
ls %{buildroot}%{ghclibdir}/libHS*.so >> ghc-base.files
sed -i -e "s|^%{buildroot}||g" ghc-base.files
%endif
ls -d %{buildroot}%{ghclibdir}/libHS*.a  %{buildroot}%{ghclibdir}/package.conf.d/builtin_*.conf %{buildroot}%{ghclibdir}/include >> ghc-base-devel.files
sed -i -e "s|^%{buildroot}||g" ghc-base-devel.files

# these are handled as alternatives
for i in hsc2hs runhaskell; do
  if [ -x %{buildroot}%{_bindir}/$i-ghc ]; then
    rm %{buildroot}%{_bindir}/$i
  else
    mv %{buildroot}%{_bindir}/$i{,-ghc}
  fi
  touch %{buildroot}%{_bindir}/$i
done

%ghc_strip_dynlinked

%if %{undefined without_haddock}
mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly
install -p --mode=0755 %SOURCE3 %{buildroot}%{_sysconfdir}/cron.hourly/ghc-doc-index
mkdir -p %{buildroot}%{_localstatedir}/lib/ghc
install -p --mode=0755 %SOURCE4 %{buildroot}%{_bindir}/ghc-doc-index

# generate initial lib doc index
cd libraries
sh %{gen_contents_index} --intree --verbose
cd ..
%endif


%check
# stolen from ghc6/debian/rules:
GHC=inplace/bin/ghc-stage2
# Do some very simple tests that the compiler actually works
rm -rf testghc
mkdir testghc
echo 'main = putStrLn "Foo"' > testghc/foo.hs
$GHC testghc/foo.hs -o testghc/foo
[ "$(testghc/foo)" = "Foo" ]
# doesn't seem to work inplace:
#[ "$(inplace/bin/runghc testghc/foo.hs)" = "Foo" ]
rm testghc/*
echo 'main = putStrLn "Foo"' > testghc/foo.hs
$GHC testghc/foo.hs -o testghc/foo -O2
[ "$(testghc/foo)" = "Foo" ]
rm testghc/*
%if %{undefined ghc_without_shared}
echo 'main = putStrLn "Foo"' > testghc/foo.hs
$GHC testghc/foo.hs -o testghc/foo -dynamic
[ "$(testghc/foo)" = "Foo" ]
rm testghc/*
%endif
%if %{undefined without_testsuite}
make test
%endif


%post compiler
# Alas, GHC, Hugs, and nhc all come with different set of tools in
# addition to a runFOO:
#
#   * GHC:  hsc2hs
#   * Hugs: hsc2hs, cpphs
#   * nhc:  cpphs
#
# Therefore it is currently not possible to use --slave below to form
# link groups under a single name 'runhaskell'. Either these tools
# should be disentangled from the Haskell implementations, or all
# implementations should have the same set of tools. *sigh*

update-alternatives --install %{_bindir}/runhaskell runhaskell \
  %{_bindir}/runghc 500
update-alternatives --install %{_bindir}/hsc2hs hsc2hs \
  %{_bindir}/hsc2hs-ghc 500

%preun compiler
if [ "$1" = 0 ]; then
  update-alternatives --remove runhaskell %{_bindir}/runghc
  update-alternatives --remove hsc2hs     %{_bindir}/hsc2hs-ghc
fi


%files

%files compiler
%doc ANNOUNCE HACKING LICENSE README
%{_bindir}/ghc
%{_bindir}/ghc-%{version}
%{_bindir}/ghc-pkg
%{_bindir}/ghc-pkg-%{version}
%{_bindir}/ghci
%{_bindir}/ghci-%{version}
%{_bindir}/hp2ps
%{_bindir}/hpc
%ghost %{_bindir}/hsc2hs
%{_bindir}/hsc2hs-ghc
%{_bindir}/runghc*
%ghost %{_bindir}/runhaskell
%{_bindir}/runhaskell-ghc
%{ghclibdir}/ghc
%{ghclibdir}/ghc-pkg
# unknown ("unregisterized") archs
%ifnarch ppc64 s390 s390x ppc64le aarch64
%{ghclibdir}/ghc-split
%endif
%{ghclibdir}/ghc-usage.txt
%{ghclibdir}/ghci-usage.txt
%{ghclibdir}/hsc2hs
%dir %{ghclibdir}/package.conf.d
%ghost %{ghclibdir}/package.conf.d/package.cache
%{ghclibdir}/runghc
%{ghclibdir}/settings
%{ghclibdir}/template-hsc.h
%{ghclibdir}/unlit
%{_mandir}/man1/ghc.*
%dir %{_docdir}/ghc
%dir %{ghcdocbasedir}
%if %{undefined without_haddock}
%{_bindir}/ghc-doc-index
%{_bindir}/haddock
%{_bindir}/haddock-ghc-%{version}
%{ghclibdir}/haddock
%{ghclibdir}/html
%{ghclibdir}/latex
%if %{undefined without_manual}
## needs pandoc
#%{ghcdocbasedir}/Cabal
%{ghcdocbasedir}/haddock
%{ghcdocbasedir}/users_guide
%endif
%dir %{ghcdocbasedir}/libraries
%{ghcdocbasedir}/libraries/frames.html
%{ghcdocbasedir}/libraries/gen_contents_index
%{ghcdocbasedir}/libraries/hslogo-16.png
%{ghcdocbasedir}/libraries/ocean.css
%{ghcdocbasedir}/libraries/prologue.txt
%{ghcdocbasedir}/libraries/synopsis.png
%{ghcdocbasedir}/index.html
%ghost %{ghcdocbasedir}/libraries/doc-index*.html
%ghost %{ghcdocbasedir}/libraries/haddock-util.js
%ghost %{ghcdocbasedir}/libraries/index*.html
%ghost %{ghcdocbasedir}/libraries/minus.gif
%ghost %{ghcdocbasedir}/libraries/plus.gif
%{_localstatedir}/lib/ghc
%endif

%if %{undefined without_haddock}
%files doc-index
%config(noreplace) %{_sysconfdir}/cron.hourly/ghc-doc-index
%endif

%files libraries


%changelog
* Thu Jun  9 2016 Jens Petersen <petersen@redhat.com> - 7.6.3-26.4
- rebase 7.6.3-18.3 to F21 7.6.3-26.3 to allow building for aarch64/ppc64le
  (#1200404)
- use rpm fileattrs also for EPEL7

* Wed Dec 24 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-26.3
- remove the build hack to switch from llvm to llvm34 (#1161049)

* Mon Dec 22 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-26.2
- use llvm34 instead of llvm-3.5 for arm (#1161049)

* Tue Nov 18 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-26.1
- use rpm internal dependency generator with ghc.attr on F21+
- fix bash-ism in ghc-doc-index (#1146733)
- do "quick" build when bootstrapping
- setup LDFLAGS

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-25
- configure ARM with VFPv3D16 and without NEON (#995419)
- only apply the Cabal unversion docdir patch to F21 and later
- hide llvm version warning on ARM now up to 3.4

* Fri Jun  6 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-24
- add aarch64 with Debian patch by Karel Gardas and Colin Watson
- patch Stg.h to define _DEFAULT_SOURCE instead of _BSD_SOURCE to quieten
  glibc 2.20 warnings (see #1067110)

* Fri May 30 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-23
- bump release

* Fri May 30 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-22
- add ppc64le support patch from Debian by Colin Watson
  (thanks to Jaromir Capik for Fedora ppc64le bootstrap)

-- 7.6.3-19
- generate and ship library doc index for ghc bundled libraries

* Wed Jan 29 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-18.3
- fix segfault on i686 when using ffi double-mapping for selinux (#907515)
  see http://hackage.haskell.org/trac/ghc/ticket/7629
  (thanks Garrett Mitchener for patch committed upstream)

* Wed Oct 30 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-18.2
- enable debuginfo for C code bits (#989593)
- back to production build

* Tue Oct 29 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-18.1
- fix rts hang on 64bit bigendian archs (patch by Gustavo Luiz Duarte, #989593)
- build with utf8 encoding (needed for verbose ghc output
  and makes better sense anyway)
- bootstrap build

* Sat Jul 27 2013 Jóhann B. Guðmundsson <johannbg@fedoraproject.org> - 7.6.3-18
- ghc-doc-index requires crontabs and mark cron file config noreplace
  (http://fedoraproject.org/wiki/Packaging:CronFiles)

* Wed Jul 24 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-17
- silence warnings about unsupported llvm version (> 3.1) on ARM

* Thu Jul 11 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-16
- revert the executable stack patch since it didn't fully fix the problem
  and yet changed the ghc library hash

* Wed Jul 10 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-15
- turn off executable stack flag in executables (#973512)
  (thanks Edward Zhang for upstream patch and Dhiru Kholia for report)

* Tue Jun 25 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-14
- fix compilation with llvm-3.3 (#977652)
  see http://hackage.haskell.org/trac/ghc/ticket/7996

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-13
- production perf -O2 build
- see release notes:
  http://www.haskell.org/ghc/docs/7.6.3/html/users_guide/release-7-6-1.html
  http://www.haskell.org/ghc/docs/7.6.3/html/users_guide/release-7-6-2.html
  http://www.haskell.org/ghc/docs/7.6.3/html/users_guide/release-7-6-3.html

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-12
- bootstrap 7.6.3
- all library versions bumped except pretty
- ghc-7.4-add-support-for-ARM-hard-float-ABI-fixes-5914.patch, and
  ghc-7.4-silence-gen_contents_index.patch are no longer needed
- build with ghc-rpm-macros-extra
- no longer filter type-level package from haddock index
- process obsoletes process-leksah
- do production build with BuildFlavour perf (#880135)

* Tue Feb  5 2013 Jens Petersen <petersen@redhat.com> - 7.4.2-11
- ghclibdir should be owned at runtime by ghc-base instead of ghc-compiler
  (thanks Michael Scherer, #907671)

* Thu Jan 17 2013 Jens Petersen <petersen@redhat.com> - 7.4.2-10
- rebuild for F19 libffi soname bump

* Wed Nov 21 2012 Jens Petersen <petersen@redhat.com> - 7.4.2-9
- fix permissions of ghc-doc-index and only run when root
- ghc-doc-index cronjob no longer looks at /etc/sysconfig/ghc-doc-index

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 7.4.2-8
- production 7.4.2 build
  http://www.haskell.org/ghc/docs/7.4.2/html/users_guide/release-7-4-2.html

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 7.4.2-7
- 7.4.2 bootstrap
- update base and unix library versions
- ARM StgCRun patches not longer needed
- use Karel Gardas' ARM hardfloat patch committed upstream
- use _smp_mflags again
- disable Cabal building ghci lib files
- silence the doc re-indexing script and move the doc indexing cronjob
  to a new ghc-doc-index subpackage (#870694)
- do not disable hscolour in build.mk
- drop the explicit hscolour BR
- without_hscolour should now be set by ghc-rpm-macros for bootstrapping

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-5
- use ghc_lib_subpackage instead of ghc_binlib_package (ghc-rpm-macros 0.91)

* Wed May  2 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-4
- add ghc-wrapper-libffi-include.patch to workaround "missing libffi.h"
  for prof compiling on secondary archs

* Sat Apr 28 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-3
- build with llvm-3.0 on ARM
- remove ARM from unregisterised_archs
- add 4 Debian ARM patches for armel and armhf (Iain Lane)

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-2
- full build

* Wed Feb 15 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-1
- update to new 7.4.1 major release
  http://www.haskell.org/ghc/docs/7.4.1/html/users_guide/release-7-4-1.html
- all library versions bumped
- binary package replaces ghc-binary
- random library dropped
- new hoopl library
- deepseq is now included in ghc
- Cabal --enable-executable-dynamic patch is upstream
- add Cabal-fix-dynamic-exec-for-TH.patch
- sparc linking fix is upstream
- use Debian's system-libffi patch by Joachim Breitner
- setup ghc-deps.sh after ghc_version_override for bootstrapping
- drop ppc64 config, pthread and mmap patches
- do not set GhcUnregisterised explicitly
- add s390 and s390x to unregisterised_archs
- Cabal manual needs pandoc

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 7.0.4-42
- move ghc-ghc-devel from ghc-libraries to the ghc metapackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.4-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-40
- do alternatives handling correctly (reported by Giam Teck Choon, #753661)
  see https://fedoraproject.org/wiki/Packaging:Alternatives

* Sat Nov 12 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-39
- move ghc-doc and ghc-libs obsoletes
- add HaskellReport license also to the base and libraries subpackages

* Thu Nov 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-38
- the post and postun scripts are now for the compiler subpackage

* Wed Nov  2 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-37
- rename ghc-devel metapackage to ghc-libraries
- require ghc-rpm-macros-0.14

* Tue Nov  1 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-36
- move compiler and tools to ghc-compiler
- the ghc base package is now a metapackage that installs all of ghc,
  ie ghc-compiler and ghc-devel (#750317)
- drop ghc-doc provides

* Fri Oct 28 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-35.1
- rebuild against new gmp

* Fri Oct 28 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-35
- add HaskellReport license tag to some of the library subpackages
  which contain some code from the Haskell Reports

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.0.4-34.1
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-34
- setup ghc-deps.sh after ghc_version_override for bootstrapping

* Tue Oct 18 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-33
- add armv5tel (ported by Henrik Nordström)
- also use ghc-deps.sh when bootstrapping (ghc-rpm-macros-0.13.13)

* Mon Oct 17 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-32
- remove libffi_archs: not allowed to bundle libffi on any arch
- include the ghc (ghci) library in ghc-devel (Narasim)

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 7.0.4-31.1
- rebuild with new gmp

* Fri Sep 30 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-31
- build with ghc-rpm-macros >= 0.13.11 to fix provides and obsoletes versions
  in library devel subpackages

* Thu Sep 29 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-30
- no need to specify -lffi in build.mk (Henrik Nordström)

* Wed Sep 28 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-29
- port to armv7hl by Henrik Nordström (#741725)

* Wed Sep 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-28
- setup ghc-deps.sh when not bootstrapping!

* Wed Sep 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-27
- setup dependency generation with ghc-deps.sh since it was moved to
  ghc_lib_install in ghc-rpm-macros

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-26
- BR same ghc version unless ghc_bootstrapping defined
- add libffi_archs
- drop the quick build profile
- put dyn before p in GhcLibWays
- explain new bootstrapping mode using ghc_bootstrap (ghc-rpm-macros-0.13.5)

* Thu Jun 16 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-25
- update to 7.0.4 bugfix release
  http://haskell.org/ghc/docs/7.0.4/html/users_guide/release-7-0-4.html
- strip static again (upstream #5004 fixed)
- Cabal updated to 1.10.2.0
- re-enable testsuite
- update summary and description

* Tue Jun 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-24
- finally change from ExclusiveArch to ExcludeArch to target more archs

* Sat May 21 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-23
- obsolete dph libraries and feldspar-language

* Mon May 16 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-22
- merge prof subpackages into the devel subpackages with ghc-rpm-macros-0.13

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-21
- configure with /usr/bin/gcc to help bootstrapping to new archs
  (otherwise ccache tends to get hardcoded as gcc, which not in koji)
- posttrans scriplet for ghc_pkg_recache is redundant

* Mon May  9 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-20
- make devel and prof meta packages require libs with release
- make ghc-*-devel subpackages require ghc with release

* Wed May 04 2011 Jiri Skala <jskala@redhat.com> - 7.0.2-19.1
- fixes path to gcc on ppc64 arch

* Tue Apr 26 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-19
- add upstream ghc-powerpc-linker-mmap.patch for ppc64 (Jiri Skala)

* Thu Apr 21 2011 Jiri Skala <jskala@redhat.com> - 7.0.2-18
- bootstrap to ppc64

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-17
- rebuild against ghc-rpm-macros-0.11.14 to provide ghc-*-doc

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-16
- provides ghc-doc again: it is still a buildrequires for libraries
- ghc-prof now requires ghc-devel
- ghc-devel now requires ghc explicitly

* Wed Mar 30 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-15
- do not strip static libs since it breaks ghci-7.0.2 loading libHSghc.a
  (see http://hackage.haskell.org/trac/ghc/ticket/5004)
- no longer provide ghc-doc
- no longer obsolete old haddock

* Tue Mar 29 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-14
- fix back missing LICENSE files in library subpackages
- drop ghc_reindex_haddock from install script

* Thu Mar 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-13
- rebuild against 7.0.2

* Wed Mar  9 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-12
- update to 7.0.2 release
- move bin-package-db into ghc-ghc
- disable broken testsuite

* Wed Feb 23 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 7.0.1-11
- enable build on sparcv9
- add ghc-fix-linking-on-sparc.patch to fix ld being called
  at the same time with --relax and -r. The two options conflict
  on sparc.
- bump BuildRequires on ghc-rpm-macros to >= 0.11.10 that guarantees
  a correct build on secondary architectures.

* Sun Feb 13 2011 Jens Petersen <petersen@redhat.com>
- without_shared renamed to ghc_without_shared

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-10
- rebuild

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-9
- fix without_shared build (thanks Adrian Reber)
- disable system libffi for secondary archs
- temporarily disable ghc-*-devel BRs for ppc

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-7
- include LICENSE files in the shared lib subpackages

* Sat Jan 22 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-6
- patch Cabal to add configure option --enable-executable-dynamic
- exclude huge ghc API library from devel and prof metapackages

* Thu Jan 13 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-5
- fix no doc and no manual builds

* Thu Jan 13 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-4
- add BRs for various subpackaged ghc libraries needed to build ghc
- condition rts .so libraries for non-shared builds

* Thu Dec 30 2010 Jens Petersen <petersen@redhat.com> - 7.0.1-3
- subpackage all the libraries with ghc-rpm-macros-0.11.1
- put rts, integer-gmp and ghc-prim in base, and ghc-binary in bin-package-db
- drop the libs mega-subpackage
- prof now a meta-package for backward compatibility
- add devel meta-subpackage to easily install all ghc libraries
- store doc cronjob package cache file under /var (#664850)
- drop old extralibs bcond
- no longer need to define or clean buildroot
- ghc base package now requires ghc-base-devel
- drop ghc-time obsoletes

* Wed Nov 24 2010 Jens Petersen <petersen@redhat.com> - 7.0.1-2
- require libffi-devel

* Tue Nov 16 2010 Jens Petersen <petersen@redhat.com> - 7.0.1-1
- update to 7.0.1 release
- turn on system libffi now

* Mon Nov  8 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-9
- disable the libffi changes for now since they break libHSffi*.so

* Thu Nov  4 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-8
- add a cronjob for doc indexing
- disable gen_contents_index when not run with --batch for cron
- use system libffi with ghc-use-system-libffi.patch from debian
- add bcond for system libffi

* Thu Nov  4 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-7
- skip huge type-level docs from haddock re-indexing (#649228)

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-6
- move gtk2hs obsoletes to ghc-glib and ghc-gtk
- drop happy buildrequires
- smp build with max 4 cpus

* Fri Jul 30 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-5
- obsolete old gtk2hs packages for smooth upgrades

* Thu Jul 15 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-4
- merge ghc-doc into base package
- obsolete ghc-time and ghc-ghc-doc (ghc-rpm-macros-0.8.0)
- note that ghc-6.12.3 is part of haskell-platform-2010.2.0.0

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-3
- drop the broken summary and description args to the ghc-ghc package
  and use ghc-rpm-macros-0.6.1

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-2
- strip all dynlinked files not just shared objects (ghc-rpm-macros-0.5.9)

* Mon Jun 14 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-1
- 6.12.3 release:
  http://darcs.haskell.org/download/docs/6.12.3/html/users_guide/release-6-12-3.html
- build with hscolour
- use ghc-rpm-macro-0.5.8 for ghc_strip_shared macro

* Fri May 28 2010 Jens Petersen <petersen@redhat.com> - 6.12.2.20100521-1
- 6.12.3 rc1
- ghost package.cache
- drop ghc-utf8-string obsoletes since it is no longer provided
- run testsuite fast
- fix description and summary of ghc internal library (John Obbele)

* Fri Apr 23 2010 Jens Petersen <petersen@redhat.com> - 6.12.2-1
- update to 6.12.2
- add testsuite with bcond, run it in check section, and BR python

* Mon Apr 12 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-6
- ghc-6.12.1 is part of haskell-platform-2010.1.0.0
- drop old ghc682, ghc681, haddock09 obsoletes
- drop haddock_version and no longer provide haddock explicitly
- update ghc-rpm-macros BR to 0.5.6 for ghc_pkg_recache

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-5
- drop ghc-6.12.1-no-filter-libs.patch and extras packages again
- filter ghc-ghc-prof files from ghc-prof
- ghc-mtl package was added to fedora

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-4
- ghc-rpm-macros-0.5.4 fixes wrong version requires between lib subpackages

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-3
- ghc-rpm-macros-0.5.2 fixes broken pkg_name requires for lib subpackages

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-2
- include haskeline, mtl, and terminfo for now with
  ghc-6.12.1-no-filter-libs.patch
- use ghc_binlibpackage, grep -v and ghc_gen_filelists to generate
  the library subpackages (ghc-rpm-macros-0.5.1)
- always set GhcLibWays (Lorenzo Villani)
- use ghcdocbasedir to revert html doc path to upstream's html/ for consistency

* Wed Dec 16 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-1
- pre became 6.12.1 final
- exclude ghc .conf file from package.conf.d in base package
- use ghc_reindex_haddock
- add scripts for ghc-ghc-devel and ghc-ghc-doc
- add doc bcond
- add ghc-6.12.1-gen_contents_index-haddock-path.patch to adjust haddock path
  since we removed html/ from libraries path
- require ghc-rpm-macros-0.3.1 and use ghc_version_override

* Sat Dec 12 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-0.2
- remove redundant mingw and perl from ghc-tarballs/
- fix exclusion of ghc internals lib from base packages with -mindepth
- rename the final file lists to PKGNAME.files for clarity

* Fri Dec 11 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-0.1
- update to ghc-6.12.1-pre
- separate bcond options into enabled and disabled for clarity
- only enable shared for intel x86 archs (Lorenzo Villani)
- add quick build profile (Lorenzo Villani)
- remove package_debugging hack (use "make install-short")
- drop sed BR (Lorenzo Villani)
- put all build.mk config into one cat block (Lorenzo Villani)
- export CFLAGS to configure (Lorenzo Villani)
- add dynamic linking test to check section (thanks Lorenzo Villani)
- remove old ghc66 obsoletes
- subpackage huge ghc internals library (thanks Lorenzo Villani)
  - BR ghc-rpm-macros >= 0.3.0
- move html docs to docdir/ghc from html subdir (Lorenzo Villani)
- disable smp build for now: broken for 8 cpus at least

* Wed Nov 18 2009 Jens Petersen <petersen@redhat.com> - 6.12.0.20091121-1
- update to 6.12.1 rc2
- build shared libs, yay! and package in standalone libs subpackage
- add bcond for manual and extralibs
- reenable ppc secondary arch
- don't provide ghc-haddock-*
- remove obsolete post requires policycoreutils
- add vanilla v to GhcLibWays when building without prof
- handle without hscolour
- can't smp make currently
- lots of filelist fixes for handling shared libs
- run ghc-pkg recache posttrans
- no need to install gen_contents_index by hand
- manpage is back

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-8
- comprehensive attempts at packaging fixes

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-7
- fix package.conf stuff

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-6
- give up trying to install man pages

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-5
- try to install man pages

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-3
- fix %check

* Sun Oct 11 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-2
- disable ppc for now (seems unsupported)
- buildreq ncurses-devel

* Sun Oct 11 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-1
- Update to 6.12 RC 1

* Thu Oct  1 2009 Jens Petersen <petersen@redhat.com>
- selinux file context no longer needed in post script
- (for ghc-6.12-shared) drop ld.so.conf.d files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.10.4-1
- update to 6.10.4

* Sat May 30 2009 Jens Petersen <petersen@redhat.com> - 6.10.3-3
- add haddock_version and use it to obsolete haddock and ghc-haddock-*

* Fri May 22 2009 Jens Petersen <petersen@redhat.com> - 6.10.3-2
- update haddock provides and obsoletes
- drop ghc-mk-pkg-install-inplace.patch: no longer needed with new 6.11 buildsys
- add bcond for extralibs
- rename doc bcond to manual

* Wed May 13 2009 Jens Petersen <petersen@redhat.com> - 6.10.3-1
- update to 6.10.3
- haskline replaces editline, so it is no longer needed to build
- macros.ghc moved to ghc-rpm-macros package
- fix handling of hscolor files in filelist generation

* Tue Apr 28 2009 Jens Petersen <petersen@redhat.com> - 6.10.2-4
- add experimental bcond hscolour
- add experimental support for building shared libraries (for ghc-6.11)
  - add libs subpackage for shared libraries
  - create a ld.conf.d file for libghc*.so
  - BR libffi-devel
- drop redundant setting of GhcLibWays in build.mk for no prof
- drop redundant setting of HADDOCK_DOCS
- simplify filelist names
- add a check section based on tests from debian's package
- be more careful about doc files in filelist

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 6.10.2-3
- define ghc_version in macros.ghc in place of ghcrequires
- drop ghc-requires script for now

* Sun Apr 19 2009 Jens Petersen <petersen@redhat.com> - 6.10.2-2
- add ghc-requires rpm script to generate ghc version dependencies
  (thanks to Till Maas)
- update macros.ghc:
  - add %%ghcrequires to call above script
  - pkg_libdir and pkg_docdir obsoleted in packages and replaced
    by ghcpkgdir and ghcdocdir inside macros.ghc
  - make filelist also for docs

* Wed Apr 08 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.10.2-1
- Update to 6.10.2

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-13
- ok let's stick with ExclusiveArch for brevity

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-12
- drop ghc_archs since it breaks koji
- fix missing -devel in ghc_gen_filelists
- change from ExclusiveArch to ExcludeArch ppc64 since alpha was bootstrapped
  by oliver

* Wed Feb 25 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-11
- use %%ix86 for change from i386 to i586 in rawhide
- add ghc_archs macro in macros.ghc for other packages
- obsolete haddock09
- use %%global instead of %%define
- use bcond for doc and prof
- rename ghc_gen_filelists lib filelist to -devel.files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-9
- require and buildrequire libedit-devel > 2.11-2
- protect ghc_register_pkg and ghc_unregister_pkg

* Fri Jan 23 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-8
- fix to libedit means can drop ncurses-devel BR workaround (#481252)

* Mon Jan 19 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-7
- buildrequire ncurses-devel to fix build of missing editline package needed
  for ghci line-editing (#478466)
- move spec templates to cabal2spec package for easy updating
- provide correct haddock version

* Mon Dec  1 2008 Jens Petersen <petersen@redhat.com> - 6.10.1-6
- update macros.ghc to latest proposed revised packaging guidelines:
  - use runghc
  - drop trivial cabal_build and cabal_haddock macros
  - ghc_register_pkg and ghc_unregister_pkg replace ghc_preinst_script,
    ghc_postinst_script, ghc_preun_script, and ghc_postun_script
- library templates prof subpackage requires main library again
- make cabal2spec work on .cabal files too, and
  read and check name and version directly from .cabal file
- ghc-prof does not need to own libraries dirs owned by main package

* Tue Nov 25 2008 Jens Petersen <petersen@redhat.com> - 6.10.1-5
- add cabal2spec and template files for easy cabal hackage packaging
- simplify script macros: make ghc_preinst_script and ghc_postun_script no-ops
  and ghc_preun_script only unregister for uninstall

* Tue Nov 11 2008 Jens Petersen <petersen@redhat.com> - 6.10.1-4
- fix broken urls to haddock docs created by gen_contents_index script
- avoid haddock errors when upgrading by making doc post script posttrans

* Wed Nov 05 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.1-3
- libraries/prologue.txt should not have been ghosted

* Tue Nov 04 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.1-2
- Fix a minor packaging glitch

* Tue Nov 04 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.1-1
- Update to 6.10.1

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-9
- remove redundant --haddockdir from cabal_configure
- actually ghc-pkg no longer seems to create package.conf.old backups
- include LICENSE in doc

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-8
- need to create ghost package.conf.old for ghc-6.10

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-7
- use gen_contents_index to re-index haddock
- add %%pkg_docdir to cabal_configure
- requires(post) ghc for haddock for doc
- improve doc file lists
- no longer need to create ghost package.conf.old
- remove or rename alternatives files more consistently

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-6
- Update macros to install html and haddock bits in the right places

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-5
- Don't use a macro to update the docs for the main doc package

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-4
- Add ghc_haddock_reindex macro
- Generate haddock index after installing ghc-doc package

* Mon Oct 13 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-3
- provide haddock = 2.2.2
- add selinux file context for unconfined_execmem following darcs package
- post requires policycoreutils

* Sun Oct 12 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-2.fc10
- Use libedit in preference to readline, for BSD license consistency
- With haddock bundled now, obsolete standalone versions (but not haddock09)
- Drop obsolete freeglut-devel, openal-devel, and haddock09 dependencies

* Sun Oct 12 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-1.fc10
- Update to 6.10.1 release candidate 1

* Wed Oct  1 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20080921-1.fc10
- Drop unneeded haddock patch
- Rename hsc2hs to hsc2hs-ghc so the alternatives symlink to it will work

* Wed Sep 24 2008 Jens Petersen <petersen@redhat.com> - 6.8.3-5
- bring back including haddock-generated lib docs, now under docdir/ghc
- fix macros.ghc filepath (#460304)
- spec file cleanups:
- fix the source urls back
- drop requires chkconfig
- do not override __spec_install_post
- setup docs building in build.mk
- no longer need to remove network/include/Typeable.h
- install binaries under libdir not libexec
- remove hsc2hs and runhaskell binaries since they are alternatives

* Wed Sep 17 2008 Jens Petersen <petersen@redhat.com> - 6.8.3-4
- add macros.ghc for new Haskell Packaging Guidelines (#460304)

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.3-3
- Add symlinks from _libdir, where ghc looks, to _libexecdir
- Patch libraries/gen_contents_index to use haddock-0.9

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.3-2
- Remove unnecessary dependency on alex

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.3-1
- Upgrade to 6.8.3
- Drop the ghc682-style naming scheme, obsolete those packages
- Manually strip binaries

* Tue Apr  8 2008 Jens Petersen <petersen@redhat.com> - 6.8.2-10
- another rebuild attempt

* Thu Feb 14 2008 Jens Petersen <petersen@redhat.com> - 6.8.2-9
- remove unrecognized --docdir and --htmldir from configure
- drop old buildrequires on libX11-devel and libXt-devel
- rebuild with gcc43

* Sun Jan 06 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.2-7
- More attempts to fix docdir

* Sun Jan 06 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.2-6
- Fix docdir

* Wed Dec 12 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.2-1
- Update to 6.8.2

* Fri Nov 23 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.1-2
- Exclude alpha

* Thu Nov  8 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.1-2
- Drop bit-rotted attempts at making package relocatable

* Sun Nov  4 2007 Michel Salim <michel.sylvan@gmail.com> - 6.8.1-1
- Update to 6.8.1

* Sat Sep 29 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.0.20070928-2
- add happy to BuildRequires

* Sat Sep 29 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.0.20070928-1
- prepare for GHC 6.8.1 by building a release candidate snapshot

* Thu May 10 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.6.1-3
- install man page for ghc

* Thu May 10 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.6.1-2
- exclude ppc64 for now, due to lack of time to bootstrap

* Wed May  9 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.6.1-1
- update to 6.6.1 release

* Mon Jan 22 2007 Jens Petersen <petersen@redhat.com> - 6.6-2
- remove truncated duplicate Typeable.h header in network package
  (Bryan O'Sullivan, #222865)

* Fri Nov  3 2006 Jens Petersen <petersen@redhat.com> - 6.6-1
- update to 6.6 release
- buildrequire haddock >= 0.8
- fix summary of ghcver package (Michel Salim, #209574)

* Thu Sep 28 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-4
- turn on docs generation again

* Mon Sep 25 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-3.fc6
- ghost package.conf.old (Gérard Milmeister)
- set unconfined_execmem_exec_t context on executables with ghc rts (#195821)
- turn off building docs until haddock is back

* Sat Apr 29 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-2.fc6
- buildrequire libXt-devel so that the X11 package and deps get built
  (Garrett Mitchener, #190201)

* Thu Apr 20 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-1.fc6
- update to 6.4.2 release

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 6.4.1-3.fc5
- buildrequire libX11-devel instead of xorg-x11-devel (Kevin Fenzi, #181024)
- make ghc-doc require ghc (Michel Salim, #180449)

* Tue Oct 11 2005 Jens Petersen <petersen@redhat.com> - 6.4.1-2.fc5
- turn on build_doc since haddock is now in Extras
- no longer specify ghc version to build with (Ville Skyttä, #170176)

* Tue Sep 20 2005 Jens Petersen <petersen@redhat.com> - 6.4.1-1.fc5
- 6.4.1 release
  - the following patches are now upstream: ghc-6.4-powerpc.patch,
    rts-GCCompact.h-x86_64.patch, ghc-6.4-dsforeign-x86_64-1097471.patch,
    ghc-6.4-rts-adjustor-x86_64-1097471.patch
  - builds with gcc4 so drop %%_with_gcc32
  - x86_64 build restrictions (no ghci and split objects) no longer apply

* Tue May 31 2005 Jens Petersen <petersen@redhat.com>
- add %%dist to release

* Thu May 12 2005 Jens Petersen <petersen@redhat.com> - 6.4-8
- initial import into Fedora Extras

* Thu May 12 2005 Jens Petersen <petersen@haskell.org>
- add build_prof and build_doc switches for -doc and -prof subpackages
- add _with_gcc32 switch since ghc-6.4 doesn't build with gcc-4.0

* Wed May 11 2005 Jens Petersen <petersen@haskell.org> - 6.4-7
- make package relocatable (ghc#1084122)
  - add post install scripts to replace prefix in driver scripts
- buildrequire libxslt and docbook-style-xsl instead of docbook-utils and flex

* Fri May  6 2005 Jens Petersen <petersen@haskell.org> - 6.4-6
- add ghc-6.4-dsforeign-x86_64-1097471.patch and
  ghc-6.4-rts-adjustor-x86_64-1097471.patch from trunk to hopefully fix
  ffi support on x86_64 (Simon Marlow, ghc#1097471)
- use XMLDocWays instead of SGMLDocWays to build documentation fully

* Mon May  2 2005 Jens Petersen <petersen@haskell.org> - 6.4-5
- add rts-GCCompact.h-x86_64.patch to fix GC issue on x86_64 (Simon Marlow)

* Thu Mar 17 2005 Jens Petersen <petersen@haskell.org> - 6.4-4
- add ghc-6.4-powerpc.patch (Ryan Lortie)
- disable building interpreter rather than install and delete on x86_64

* Wed Mar 16 2005 Jens Petersen <petersen@haskell.org> - 6.4-3
- make ghc require ghcver of same ver-rel
- on x86_64 remove ghci for now since it doesn't work and all .o files

* Tue Mar 15 2005 Jens Petersen <petersen@haskell.org> - 6.4-2
- ghc requires ghcver (Amanda Clare)

* Sat Mar 12 2005 Jens Petersen <petersen@haskell.org> - 6.4-1
- 6.4 release
  - x86_64 build no longer unregisterised
- use sed instead of perl to tidy filelists
- buildrequire ghc64 instead of ghc-6.4
- no epoch for ghc64-prof's ghc64 requirement
- install docs directly in docdir

* Fri Jan 21 2005 Jens Petersen <petersen@haskell.org> - 6.2.2-2
- add x86_64 port
  - build unregistered and without splitobjs
  - specify libdir to configure and install
- rename ghc-prof to ghcXYZ-prof, which obsoletes ghc-prof

* Mon Dec  6 2004 Jens Petersen <petersen@haskell.org> - 6.2.2-1
- move ghc requires to ghcXYZ

* Wed Nov 24 2004 Jens Petersen <petersen@haskell.org> - 6.2.2-0.fdr.1
- ghc622
  - provide ghc = %%version
- require gcc, gmp-devel and readline-devel

* Fri Oct 15 2004 Gerard Milmeister <gemi@bluewin.ch> - 6.2.2-0.fdr.1
- New Version 6.2.2

* Mon Mar 22 2004 Gerard Milmeister <gemi@bluewin.ch> - 6.2.1-0.fdr.1
- New Version 6.2.1

* Tue Dec 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.2-0.fdr.1
- New Version 6.2

* Tue Dec 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.0.1-0.fdr.3
- A few minor specfile tweaks

* Mon Dec 15 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.0.1-0.fdr.2
- Different file list generation

* Mon Oct 20 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.0.1-0.fdr.1
- First Fedora release
- Added generated html docs, so that haddock is not needed

* Wed Sep 26 2001 Manuel Chakravarty
- small changes for 5.04

* Wed Sep 26 2001 Manuel Chakravarty
- split documentation off into a separate package
- adapt to new docbook setup in RH7.1

* Mon Apr 16 2001 Manuel Chakravarty
- revised for 5.00
- also runs autoconf automagically if no ./configure found

* Thu Jun 22 2000 Sven Panne
- removed explicit usage of hslibs/docs, it belongs to ghc/docs/set

* Sun Apr 23 2000 Manuel Chakravarty
- revised for ghc 4.07; added suggestions from Pixel <pixel@mandrakesoft.com>
- added profiling package

* Tue Dec 7 1999 Manuel Chakravarty
- version for use from CVS

* Thu Sep 16 1999 Manuel Chakravarty
- modified for GHC 4.04, patchlevel 1 (no more 62 tuple stuff); minimises use
  of patch files - instead emits a build.mk on-the-fly

* Sat Jul 31 1999 Manuel Chakravarty
- modified for GHC 4.04

* Wed Jun 30 1999 Manuel Chakravarty
- some more improvements from vbzoli

* Fri Feb 26 1999 Manuel Chakravarty
- modified for GHC 4.02

* Thu Dec 24 1998 Zoltan Vorosbaranyi
- added BuildRoot
- files located in /usr/local/bin, /usr/local/lib moved to /usr/bin, /usr/lib

* Tue Jul 28 1998 Manuel Chakravarty
- original version
