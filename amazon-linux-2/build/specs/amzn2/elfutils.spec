Name: elfutils
Summary: A collection of utilities and DSOs to handle ELF files and DWARF data
Version: 0.176
%global baserelease 2
URL: http://elfutils.org/
%global source_url ftp://sourceware.org/pub/elfutils/%{version}/
License: GPLv3+ and (GPLv2+ or LGPLv3+)
Group: Development/Tools

Release: %{baserelease}%{?dist}

%global provide_yama_scope	0

%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
%global provide_yama_scope	1
%endif

%global depsuffix %{?_isa}%{!?_isa:-%{_arch}}

Source: %{?source_url}%{name}-%{version}.tar.bz2

# Patches
Patch1: elfutils-0.176-xlate-note.patch

Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}

BuildRequires: gettext
BuildRequires: bison >= 1.875
BuildRequires: flex >= 2.5.4a
BuildRequires: bzip2
BuildRequires: gcc >= 4.4
# For libstdc++ demangle support
BuildRequires: libstdc++-devel

BuildRequires: zlib-devel >= 1.2.2.3
BuildRequires: bzip2-devel
BuildRequires: xz-devel

%global _gnu %{nil}
%global _program_prefix eu-

# The lib[64]/elfutils directory contains the private ebl backend
# libraries. They must not be exposed as global provides. We don't
# need to filter the requires since they are only loaded with dlopen.
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global __provides_exclude ^libebl_.*\\.so.*$
%endif

%description
Elfutils is a collection of utilities, including stack (to show
backtraces), nm (for listing symbols from object files), size
(for listing the section sizes of an object or archive file),
strip (for discarding symbols), readelf (to see the raw ELF file
structures), elflint (to check for well-formed ELF files) and
elfcompress (to compress or decompress ELF sections).


%package libs
Summary: Libraries to handle compiled objects
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libs%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
%if %{provide_yama_scope}
Requires: default-yama-scope
%endif

%description libs
The elfutils-libs package contains libraries which implement DWARF, ELF,
and machine-specific ELF handling.  These libraries are used by the programs
in the elfutils package.  The elfutils-devel package enables building
other programs using these libraries.

%package devel
Summary: Development libraries to handle compiled objects
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libebl provides some
higher-level ELF access functionality.  libdw provides access to
the DWARF debugging information.  libasm provides a programmable
assembler interface.

%package devel-static
Summary: Static archives to handle compiled objects
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-devel-static%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-devel%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}

%description devel-static
The elfutils-devel-static package contains the static archives
with the code to handle compiled objects.

%package libelf
Summary: Library to read and write ELF files
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libelf%{depsuffix} = %{version}-%{release}
%endif
Obsoletes: libelf <= 0.8.2-2

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package libelf-devel
Summary: Development support for libelf
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
Obsoletes: libelf-devel <= 0.8.2-2

%description libelf-devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%package libelf-devel-static
Summary: Static archive of libelf
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}

%description libelf-devel-static
The elfutils-libelf-static package contains the static archive
for libelf.

%if %{provide_yama_scope}
%package default-yama-scope
Summary: Default yama attach scope sysctl setting
Group: Development/Tools
License: GPLv2+ or LGPLv3+
Provides: default-yama-scope
BuildArch: noarch
# For the sysctl_apply macro
%{?systemd_requires}
BuildRequires: systemd >= 215

%description default-yama-scope
Yama sysctl setting to enable default attach scope settings
enabling programs to use ptrace attach, access to
/proc/PID/{mem,personality,stack,syscall}, and the syscalls
process_vm_readv and process_vm_writev which are used for
interprocess services, communication and introspection
(like synchronisation, signaling, debugging, tracing and
profiling) of processes.
%endif

%prep
%setup -q

# Apply patches
%patch1 -p1 -b .xlate-note

# In case the above patches added any new test scripts, make sure they
# are executable.
find . -name \*.sh ! -perm -0100 -print | xargs chmod +x

%ifarch %{arm}
echo -e '"dwarf: arm needs debuginfo installed for all libraries"\nexit 77' > tests/run-backtrace
%endif

%build
# Remove -Wall from default flags.  The makefiles enable enough warnings
# themselves, and they use -Werror.  Appending -Wall defeats the cases where
# the makefiles disable some specific warnings for specific code.
# But add -Wformat explicitly for use with -Werror=format-security which
# doesn't work without -Wformat (enabled by -Wall).
RPM_OPT_FLAGS="${RPM_OPT_FLAGS/-Wall/}"
RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -Wformat"

trap 'cat config.log' EXIT
%configure CFLAGS="$RPM_OPT_FLAGS -fexceptions"
trap '' EXIT
make -s %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make -s install DESTDIR=${RPM_BUILD_ROOT}

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/elfutils/lib*.so*

%find_lang %{name}

%if %{provide_yama_scope}
install -Dm0644 config/10-default-yama-scope.conf ${RPM_BUILD_ROOT}%{_sysctldir}/10-default-yama-scope.conf
%endif

%check
# Record some build root versions in build.log
uname -r; rpm -q glibc

make -s %{?_smp_mflags} check || (cat tests/test-suite.log; false)

%clean
rm -rf ${RPM_BUILD_ROOT}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post libelf -p /sbin/ldconfig

%postun libelf -p /sbin/ldconfig

%if %{provide_yama_scope}
%post default-yama-scope
# Due to circular dependencies might not be installed yet, so double check.
# (systemd -> elfutils-libs -> default-yama-scope -> systemd)
if [ -x /usr/lib/systemd/systemd-sysctl ] ; then
%sysctl_apply 10-default-yama-scope.conf
fi
%endif

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING-GPLV2 COPYING-LGPLV3
%doc README TODO CONTRIBUTING
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfcmp
%{_bindir}/eu-elflint
%{_bindir}/eu-findtextrel
%{_bindir}/eu-nm
%{_bindir}/eu-objdump
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-stack
%{_bindir}/eu-strings
%{_bindir}/eu-strip
%{_bindir}/eu-unstrip
%{_bindir}/eu-make-debug-archive
%{_bindir}/eu-elfcompress

%files libs
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libasm-%{version}.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/known-dwarf.h
%{_includedir}/elfutils/libasm.h
%{_includedir}/elfutils/libebl.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/libdwelf.h
%{_includedir}/elfutils/version.h
%{_libdir}/libebl.a
%{_libdir}/libasm.so
%{_libdir}/libdw.so
%{_libdir}/pkgconfig/libdw.pc

%files devel-static
%defattr(-,root,root)
%{_libdir}/libasm.a
%{_libdir}/libdw.a

%files -f %{name}.lang libelf
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf.so.*

%files libelf-devel
%defattr(-,root,root)
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%{_libdir}/libelf.so
%{_libdir}/pkgconfig/libelf.pc

%files libelf-devel-static
%defattr(-,root,root)
%{_libdir}/libelf.a

%if %{provide_yama_scope}
%files default-yama-scope
%defattr(-,root,root)
%config(noreplace) %{_sysctldir}/10-default-yama-scope.conf
%endif

%changelog
* Wed May  1 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.176-2
- Add elfutils-0.176-xlate-note.patch (#1704754)

* Wed Mar  6 2019 Mark Wielaard <mjw@redhat.com> - 0.176-1
- New upstream release (#1676504)
  CVE-2019-7146, CVE-2019-7148, CVE-2019-7149, CVE-2019-7150,
  CVE-2019-7664, CVE-2019-7665, CVE-2018-16062, CVE-2018-16402,
  CVE-2018-16403, CVE-2018-18310, CVE-2018-18521, CVE-2018-18520.

* Wed Jun 20 2018 Mark Wielaard <mjw@redhat.com> - 0.172-2
- Add elfutils-0.172-robustify.patch. (#1593328)

* Mon Jun 11 2018 Mark Wielaard <mjw@redhat.com> - 0.172-1
- New upstream release.
  - No functional changes compared to 0.171.
  - Various bug fixes in libdw and eu-readelf dealing with bad DWARF5
    data. Thanks to running the afl fuzzer on eu-readelf and various
    testcases.
  - eu-readelf -N is ~15% faster.

* Tue Jun 05 2018 Mark Wielaard <mjw@redhat.com> - 0.171-1
- New upstream release.
  - DWARF5 and split dwarf, including GNU DebugFission, support.
  - readelf: Handle all new DWARF5 sections.
    --debug-dump=info+ will show split unit DIEs when found.
    --dwarf-skeleton can be used when inspecting a .dwo file.
    Recognizes GNU locviews with --debug-dump=loc.
  - libdw: New functions dwarf_die_addr_die, dwarf_get_units,
    dwarf_getabbrevattr_data and dwarf_cu_info.
    libdw will now try to resolve the alt file on first use
    when not set yet with dwarf_set_alt.
    dwarf_aggregate_size() now works with multi-dimensional arrays.
  - libdwfl: Use process_vm_readv when available instead of ptrace.
  - backends: Add a RISC-V backend.

* Wed Dec 20 2017 Mark Wielaard <mjw@redhat.com> - 0.170-4
- Add elfutils-0.170-dwarf_aggregate_size.patch (#1527966).

* Wed Nov  8 2017 Mark Wielaard <mjw@redhat.com> - 0.170-3
- Rely on systemd_requires for sysctl_apply default-yama-scope (#1509861).

* Thu Nov  2 2017 Mark Wielaard <mjw@redhat.com> - 0.170-2
- Rebuild because of binutils bug (#1508966)

* Mon Oct 16 2017 Mark Wielaard <mjw@redhat.com> - 0.170-1
- New upstream release. Remove upstreamed patches.
- Sync provide_yama_scope with fedora.
- Add elfutils-0.170-x86_64-backtrace-test-override.patch.

* Tue May 30 2017 Mark Wielaard <mjw@redhat.com> - 0.168-8
- Fix ppc64 fallback unwinder (#1454754)

* Thu May 25 2017 Mark Wielaard <mjw@redhat.com> - 0.168-7
- Enable default-yama-scope (#1455514)

* Mon May 22 2017 Mark Wielaard <mjw@redhat.com> - 0.168-6
- Add ppc64 fallback unwinder (#1454754)

* Wed Mar  1 2017 Mark Wielaard <mjw@redhat.com> - 0.168-5
- Rebase to fedora elfutils 0.168 (#1371517, #1400302)

* Thu Apr 14 2016 Mark Wielaard <mjw@redhat.com> - 0.166-2
- Rebase to fedora elfutils 0.166 (#1296313, #1304873)

* Mon Sep 14 2015 Mark Wielaard <mjw@redhat.com> - 0.163-3
- Add elfutils-0.163-readelf-n-undefined-shift.patch (#1262839)

* Tue Aug 11 2015 Mark Wielaard <mjw@redhat.com> - 0.163-2
- Add elfutils-0.163-elflint-bad-nobits.patch (#1251698)

* Fri Jun 19 2015 Mark Wielaard <mjw@redhat.com> - 0.163-1
- Update to 0.163

* Thu Jun 11 2015 Mark Wielaard <mjw@redhat.com> - 0.162-1
- Update to 0.162 (#1224169, #1223462, #1207799)
- Include elfutils/known-dwarf.h
- Drop BuildRequires glibc-headers

* Wed Aug 27 2014 Mark Wielaard <mjw@redhat.com> - 0.160-1
- Update to 0.160.

* Tue Mar 11 2014 Mark Wielaard <mjw@redhat.com> - 0.158-3
- Add elfutils-0.158-mod-e_type.patch.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.158-2
- Mass rebuild 2014-01-24

* Tue Jan  7 2014 Petr Machata <pmachata@redhat.com> - 0.158-1
- Update to 0.158.  Add eu-stack.

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.157-3
- Mass rebuild 2013-12-27

* Wed Oct  9 2013 Mark Wielaard <mjw@redhat.com> 0.157-2
- Show tests/test-suite.log in build.log when make check fails.

* Mon Sep 30 2013 Mark Wielaard <mjw@redhat.com> 0.157-1
- Update to 0.157.
- Remove elfutils-0.156-abi_cfi-ppc-s390-arm.patch.
- Remove elfutils-0.156-et_dyn-kernels.patch.

* Fri Sep 06 2013 Mark Wielaard <mjw@redhat.com> 0.156-5
- Add elfutils-0.156-abi_cfi-ppc-s390-arm.patch.
  Sets up initial CFI return register, CFA location expression and
  register rules for PPC, S390 and ARM (dwarf_cfi_addrframe support).

* Mon Aug 26 2013 Mark Wielaard <mjw@redhat.com> 0.156-4
- Add elfutils-0.156-et_dyn-kernels.patch.
  Fixes an issue on ppc64 with systemtap kernel address placement.

* Thu Aug  8 2013 Mark Wielaard <mjw@redhat.com> 0.156-3
- Make check can now also be ran in parallel.

* Thu Jul 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> 0.156-2
- Update the %%configure command for compatibility with fc20 Koji.

* Thu Jul 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> 0.156-1
- Update to 0.156.
  - #890447 - Add __bss_start and __TMC_END__ to elflint.
  - #909481 - Only try opening files with installed compression libraries.
  - #914908 - Add __bss_start__ to elflint.
  - #853757 - Updated Polish translation.
  - #985438 - Incorrect prototype of __libdwfl_find_elf_build_id.
  - Drop upstreamed elfutils-0.155-binutils-pr-ld-13621.patch.
  - Drop upstreamed elfutils-0.155-mem-align.patch.
  - Drop upstreamed elfutils-0.155-sizeof-pointer-memaccess.patch.

* Tue Jul 02 2013 Karsten Hopp <karsten@redhat.com> 0.155-6
- bump release and rebuild to fix dependencies on PPC

* Sun Feb 24 2013 Mark Wielaard <mjw@redhat.com> - 0.155-5
- Add ARM variant to elfutils-0.155-binutils-pr-ld-13621.patch rhbz#914908.
- rhel >= 5 has xz-devel

* Fri Feb 22 2013 Mark Wielaard <mjw@redhat.com> - 0.155-4
- Replace elfutils-0.155-binutils-pr-ld-13621.patch with upstream fix.

* Thu Jan 24 2013 Mark Wielaard <mjw@redhat.com> - 0.155-3
- Backport sizeof-pointer-memaccess upstream fixes.

* Thu Jan 10 2013 Mark Wielaard <mjw@redhat.com> - 0.155-2
- #891553 - unaligned memory access issues.

* Mon Aug 27 2012 Mark Wielaard <mjw@redhat.com> - 0.155-1
- Update to 0.155.
  - #844270 - eu-nm invalid %N$ use detected.
  - #847454 - Ukrainian translation update.
  - Removed local ar 64-bit symbol patch, dwz support patch and xlatetom fix.

* Tue Aug 14 2012 Petr Machata <pmachata@redhat.com> - 0.154-4
- Add support for archives with 64-bit symbol tables (#843019)

* Wed Aug 01 2012 Mark Wielaard <mjw@redhat.com> 0.154-3
- Add dwz support

* Wed Jul 18 2012 Mark Wielaard <mjw@redhat.com> 0.154-2
- Add upstream xlatetom fix (#835877)

* Mon Jul 02 2012 Karsten Hopp <karsten@redhat.com> 0.154-1.1
- disable unstrip-n check for now (835877)

* Fri Jun 22 2012 Mark Wielaard <mjw@redhat.com> - 0.154-1
- Update to 0.154
  - elflint doesn't recognize SHF_INFO_LINK on relocation sections (#807823)
  - Update license to GPLv3+ and (GPLv2+ or LGPLv3+)
  - Remove elfutils-0.153-dwfl_segment_report_module.patch
- Add elfutils-0.154-binutils-pr-ld-13621.patch

* Mon Apr 02 2012 Mark Wielaard <mark@klomp.org> - 0.153-2
- Fix for eu-unstrip emits garbage for librt.so.1 (#805447)

* Thu Feb 23 2012 Mark Wielaard <mjw@redhat.com> - 0.153-1
- Update to 0.153
  - New --disable-werror for portability.
  - Support for .zdebug sections (#679777)
  - type_units and DW_AT_GNU_odr_signature support (#679815)
  - low level support DW_OP_GNU_entry_value and DW_TAG_GNU_call_site (#688090)
  - FTBFS on rawhide with gcc 4.7 (#783506)
    - Remove gcc-4.7 patch

* Fri Jan 20 2012 Mark Wielaard <mjw@redhat.com> - 0.152-3
- Fixes for gcc-4.7 based on upstream commit 32899a (#783506).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.152-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 15 2011 Roland McGrath <roland@redhat.com> - 0.152-1
- Update to 0.152
  - Various build and warning nits fixed for newest GCC and Autoconf.
  - libdwfl: Yet another prelink-related fix for another regression. (#674465)
  - eu-elfcmp: New flag --ignore-build-id to ignore differing build ID bits.
  - eu-elfcmp: New flag -l/--verbose to print all differences.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.151-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Roland McGrath <roland@redhat.com> - 0.151-1
- Update to 0.151
  - libdwfl: Fix for more prelink cases with separate debug file.
  - eu-strip: New flag --strip-sections to remove section headers entirely.

* Thu Dec  2 2010 Roland McGrath <roland@redhat.com> - 0.150-2
- libdwfl: Remove bogus assert. (#658268)

* Tue Nov 23 2010 Roland McGrath <roland@redhat.com> - 0.150-1
- Update to 0.150
  - libdw: Fix for handling huge .debug_aranges section. (#638432)
  - libdwfl: Fix for handling prelinked DSO with separate debug file. (#652857)
  - findtextrel: Fix diagnostics to work with usual section ordering.

* Wed Sep 29 2010 jkeating - 0.149-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Roland McGrath <roland@redhat.com> - 0.149-1
- Update to 0.149
  - libdw: Decode new DW_OP_GNU_implicit_pointer operation;
           new function dwarf_getlocation_implicit_pointer.
  - libdwfl: New function dwfl_dwarf_line.
  - eu-addr2line: New flag -F/--flags to print more DWARF line info details.
  - eu-readelf: better .debug_loc processing (#627729)
  - eu-strings: Fix non-mmap file reading. (#609468)
  - eu-strip: -g recognizes .gdb_index as a debugging section. (#631997)

* Mon Jun 28 2010 Roland McGrath <roland@redhat.com> - 0.148-1
- Update to 0.148
  - libdw: Accept DWARF 4 format: new functions dwarf_next_unit,
           dwarf_offdie_types.
           New functions dwarf_lineisa, dwarf_linediscriminator,
           dwarf_lineop_index.
  - libdwfl: Fixes in core-file handling, support cores from PIEs. (#588818)
             When working from build IDs, don't open a named file
             that mismatches.
  - readelf: Handle DWARF 4 formats.

* Mon May  3 2010 Roland McGrath <roland@redhat.com> - 0.147-1
- Update to 0.147

* Wed Apr 21 2010 Roland McGrath <roland@redhat.com> - 0.146-1
- Update to 0.146
  - libdwfl: New function dwfl_core_file_report.
  - libelf: Fix handling of phdrs in truncated file. (#577310)
  - libdwfl: Fix infinite loop handling clobbered link_map. (#576379)
- Package translations.

* Tue Feb 23 2010 Roland McGrath <roland@redhat.com> - 0.145-1
- Update to 0.145
  - Fix build with --disable-dependency-tracking. (#564646)
  - Fix build with most recent glibc headers.
  - libdw: Fix CFI decoding. (#563528)
  - libdwfl: Fix address bias returned by CFI accessors. (#563528)
             Fix core file module layout identification. (#559836)
  - readelf: Fix CFI decoding.

* Fri Jan 15 2010 Roland McGrath <roland@redhat.com> - 0.144-2
- Fix sloppy #include's breaking build with F-13 glibc.

* Thu Jan 14 2010 Roland McGrath <roland@redhat.com> - 0.144-1
- Update to 0.144
  - libdw: New function dwarf_aggregate_size for computing (constant) type
           sizes, including array_type cases with nontrivial calculation.
  - readelf: Don't give errors for missing info under -a.
             Handle Linux "VMCOREINFO" notes under -n.
- Resolves: RHBZ #527004, RHBZ #530704, RHBZ #550858

* Mon Sep 21 2009 Roland McGrath <roland@redhat.com> - 0.143-1
- Update to 0.143
  - libdw: Various convenience functions for individual attributes now use
           dwarf_attr_integrate to look up indirect inherited attributes.
           Location expression handling now supports DW_OP_implicit_value.
  - libdwfl: Support automatic decompression of files in XZ format,
             and of Linux kernel images made with bzip2 or LZMA
             (as well as gzip).

* Tue Jul 28 2009 Roland McGrath <roland@redhat.com> - 0.142-1
- Update to 0.142
  - libelf: Bug fix in filling gaps between sections. (#512840)
  - libelf: Add elf_getshdrnum alias for elf_getshnum and elf_getshdrstrndx
            alias for elf_getshstrndx and deprecate original names.
  - libebl, elflint: Add support for STB_GNU_UNIQUE. (#511436)
  - readelf: Add -N option, speeds up DWARF printing
             without address->name lookups. (#505347)
  - libdw: Add support for decoding DWARF CFI into location description form.
           Handle some new DWARF 3 expression operations previously omitted.
           Basic handling of some new encodings slated for DWARF 4.

* Thu Apr 23 2009 Roland McGrath <roland@redhat.com> - 0.141-1
- Update to 0.141
  - libebl: sparc backend fixes (#490585)
            some more arm backend support
  - libdwfl: fix dwfl_module_build_id for prelinked DSO case (#489439)
             fixes in core file support (#494858)
             dwfl_module_getsym interface improved for non-address symbols
  - eu-strip: fix infinite loop on strange inputs with -f
  - eu-addr2line: take -j/--section=NAME option for binutils compatibility
                  (same effect as '(NAME)0x123' syntax already supported)
- Resolves: RHBZ #495213, RHBZ #465872, RHBZ #470055, RHBZ #484623

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.140-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Roland McGrath <roland@redhat.com> - 0.140-1
- Update to 0.140
  - libelf: Fix regression in creation of section header. (#484946)

* Fri Jan 23 2009 Roland McGrath <roland@redhat.com> - 0.139-1
- Update to 0.139
  - libcpu: Add Intel SSE4 disassembler support
  - readelf: Implement call frame information and exception handling dumping.
             Add -e option.  Enable it implicitly for -a.
  - elflint: Check PT_GNU_EH_FRAME program header entry.
  - libdwfl: Support automatic gzip/bzip2 decompression of ELF files. (#472136)

* Thu Jan  1 2009 Roland McGrath <roland@redhat.com> - 0.138-2
- Fix libelf regression.

* Wed Dec 31 2008 Roland McGrath <roland@redhat.com> - 0.138-1
- Update to 0.138
  - Install <elfutils/version.h> header file for applications to use in
    source version compatibility checks.
  - libebl: backend fixes for i386 TLS relocs; backend support for NT_386_IOPERM
  - libcpu: disassembler fixes (#469739)
  - libdwfl: bug fixes (#465878)
  - libelf: bug fixes
  - eu-nm: bug fixes for handling corrupt input files (#476136)

* Wed Oct  1 2008 Roland McGrath <roland@redhat.com> - 0.137-3
- fix libdwfl regression (#462689)

* Thu Aug 28 2008 Roland McGrath <roland@redhat.com> - 0.137-2
- Update to 0.137
  - libdwfl: bug fixes; new segment interfaces;
             all the libdwfl-based tools now support --core=COREFILE option
- Resolves: RHBZ #325021, RHBZ #447416

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.135-2
- fix conditional comparison

* Mon May 12 2008 Roland McGrath <roland@redhat.com> - 0.135-1
- Update to 0.135
  - libdwfl: bug fixes
  - eu-strip: changed handling of ET_REL files wrt symbol tables and relocs

* Wed Apr  9 2008 Roland McGrath <roland@redhat.com> - 0.134-1
- Update to 0.134
  - elflint: backend improvements for sparc, alpha (#204170)
  - libdwfl, libelf: bug fixes (#439344, #438867, #438263, #438190)
- Remove Conflicts: libelf-devel from elfutils-libelf-devel. (#435742)

* Sun Mar  2 2008 Roland McGrath <roland@redhat.com> - 0.133-2
- Update to 0.133
  - readelf, elflint, libebl: SHT_GNU_ATTRIBUTE section handling (readelf -A)
  - readelf: core note handling for NT_386_TLS, NT_PPC_SPE, Alpha NT_AUXV
  - libdwfl: bug fixes and optimization in relocation handling
  - elfcmp: bug fix for non-allocated section handling
  - ld: implement newer features of binutils linker.
- Install eu-objdump and libasm, now has limited disassembler support.

* Mon Jan 21 2008 Roland McGrath <roland@redhat.com> - 0.132-3
- Update to 0.132
  - libelf: Use loff_t instead of off64_t in libelf.h header. (#377241)
  - eu-readelf: Fix handling of ET_REL files in archives.
  - libcpu: Implement x86 and x86-64 disassembler.
  - libasm: Add interface for disassembler.
  - all programs: add debugging of branch prediction.
  - libelf: new function elf_scnshndx.

* Sun Nov 11 2007 Roland McGrath <roland@redhat.com> - 0.131-1
- Update to 0.131
  - libdw: DW_FORM_ref_addr support; dwarf_formref entry point now deprecated;
           bug fixes for oddly-formatted DWARF
  - libdwfl: bug fixes in offline archive support, symbol table handling;
             apply partial relocations for dwfl_module_address_section on ET_REL
  - libebl: powerpc backend support for Altivec registers

* Wed Oct 17 2007 Roland McGrath <roland@redhat.com> - 0.130-3
- Fix ET_REL support.
- Fix odd indentation in eu-readelf -x output.

* Tue Oct 16 2007 Roland McGrath <roland@redhat.com> - 0.130-1
- Update to 0.130
  - eu-readelf -p option can take an argument like -x for one section
  - eu-readelf --archive-index (or -c)
  - eu-readelf -n improved output for core dumps
  - eu-readelf: handle SHT_NOTE sections without requiring phdrs (#249467)
  - eu-elflint: ditto
  - eu-elflint: stricter checks on debug sections
  - eu-unstrip: new options, --list (or -n), --relocate (or -R)
  - libelf: new function elf_getdata_rawchunk, replaces gelf_rawchunk;
            new functions gelf_getnote, gelf_getauxv, gelf_update_auxv
  - libebl: backend improvements (#324031)
  - libdwfl: build_id support, new functions for it
  - libdwfl: dwfl_module_addrsym fixes (#268761, #268981)
  - libdwfl offline archive support, new script eu-make-debug-archive

* Mon Aug 20 2007 Roland McGrath <roland@redhat.com> - 0.129-2
- Fix false-positive eu-elflint failure on ppc -mbss-plt binaries.

* Tue Aug 14 2007 Roland McGrath <roland@redhat.com> - 0.129-1
- Update to 0.129
  - readelf: new options --hex-dump (or -x), --strings (or -p) (#250973)
  - addr2line: new option --symbols (or -S)
  - libdw: dwarf_getscopes fixes (#230235)
  - libdwfl: dwfl_module_addrsym fixes (#249490)

* Fri Jun  8 2007 Roland McGrath <roland@redhat.com> - 0.128-2
- Update to 0.128
  - new program: unstrip
  - elfcmp: new option --hash-inexact
- Replace Conflicts: with Provides/Requires using -arch

* Wed Apr 18 2007 Roland McGrath <roland@redhat.com> - 0.127-1
- Update to 0.127
  - libdw: new function dwarf_getsrcdirs
  - libdwfl: new functions dwfl_module_addrsym, dwfl_report_begin_add,
             dwfl_module_address_section

* Mon Feb  5 2007 Roland McGrath <roland@redhat.com> - 0.126-1
- Update to 0.126
  - New program eu-ar.
  - libdw: fix missing dwarf_getelf (#227206)
  - libdwfl: dwfl_module_addrname for st_size=0 symbols (#227167, #227231)

* Wed Jan 10 2007 Roland McGrath <roland@redhat.com> - 0.125-3
- Fix overeager warn_unused_result build failures.

* Wed Jan 10 2007 Roland McGrath <roland@redhat.com> - 0.125-1
- Update to 0.125
  - elflint: Compare DT_GNU_HASH tests.
  - move archives into -static RPMs
  - libelf, elflint: better support for core file handling
  - Really fix libdwfl sorting of modules with 64-bit addresses (#220817).
- Resolves: RHBZ #220817, RHBZ #213792

* Tue Oct 10 2006 Roland McGrath <roland@redhat.com> - 0.124-1
- eu-strip -f: copy symtab into debuginfo file when relocs use it (#203000)
- Update to 0.124
  - libebl: fix ia64 reloc support (#206981)
  - libebl: sparc backend support for return value location
  - libebl, libdwfl: backend register name support extended with more info
  - libelf, libdw: bug fixes for unaligned accesses on machines that care
  - readelf, elflint: trivial bugs fixed

* Mon Aug 14 2006 Roland McGrath <roland@redhat.com> 0.123-1
- Update to 0.123
  - libebl: Backend build fixes, thanks to Stepan Kasal.
  - libebl: ia64 backend support for register names, return value location
  - libdwfl: Handle truncated linux kernel module section names.
  - libdwfl: Look for linux kernel vmlinux files with .debug suffix.
  - elflint: Fix checks to permit --hash-style=gnu format.

* Mon Jul 17 2006 Roland McGrath <roland@redhat.com> - 0.122-4
- Fix warnings in elflint compilation.

* Wed Jul 12 2006 Roland McGrath <roland@redhat.com> - 0.122-3
- Update to 0.122
  - Fix libdwfl sorting of modules with 64-bit addresses (#198225).
  - libebl: add function to test for relative relocation
  - elflint: fix and extend DT_RELCOUNT/DT_RELACOUNT checks
  - elflint, readelf: add support for DT_GNU_HASH
  - libelf: add elf_gnu_hash
  - elflint, readelf: add support for 64-bit SysV-style hash tables
  - libdwfl: new functions dwfl_module_getsymtab, dwfl_module_getsym.

* Thu Jun 15 2006 Roland McGrath <roland@redhat.com> - 0.121-1
- Update to 0.121
  - libelf: bug fixes for rewriting existing files when using mmap (#187618).
  - make all installed headers usable in C++ code (#193153).
  - eu-readelf: better output format.
  - eu-elflint: fix tests of dynamic section content.
  - libdw, libdwfl: handle files without aranges info.

* Thu May 25 2006 Jeremy Katz <katzj@redhat.com> - 0.120-3
- rebuild to pick up -devel deps

* Tue Apr  4 2006 Roland McGrath <roland@redhat.com> - 0.120-2
- Update to 0.120
  - License changed to GPL, with some exceptions for using
    the libelf, libebl, libdw, and libdwfl library interfaces.
    Red Hat elfutils is an included package of the Open Invention Network.
  - dwarf.h updated for DWARF 3.0 final specification.
  - libelf: Fix corruption in ELF_C_RDWR uses (#187618).
  - libdwfl: New function dwfl_version; fixes for offline.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.119-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.119-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Roland McGrath <roland@redhat.com> - 0.119-1
- update to 0.119

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 27 2005 Roland McGrath <roland@redhat.com> - 0.118-1
- update to 0.118
  - elflint: more tests.
  - libdwfl: New function dwfl_module_register_names.
  - libebl: New backend hook for register names.
- Make sure -fexceptions is always in CFLAGS.

* Tue Nov 22 2005 Roland McGrath <roland@redhat.com> - 0.117-2
- update to 0.117
  - libdwfl: New function dwfl_module_return_value_location (#166118)
  - libebl: Backend improvements for several CPUs

* Mon Oct 31 2005 Roland McGrath <roland@redhat.com> - 0.116-1
- update to 0.116
  - libdw fixes, API changes and additions
  - libdwfl fixes (#169672)
  - eu-strip/libelf fix to preserve setuid/setgid permission bits (#167745)

* Fri Sep  9 2005 Roland McGrath <roland@redhat.com> - 0.115-3
- Update requires/conflicts for better biarch update behavior.

* Mon Sep  5 2005 Roland McGrath <roland@redhat.com> - 0.115-2
- update to 0.115
  - New program eu-strings.
  - libdw: New function dwarf_getscopes_die.
  - libelf: speed-ups of non-mmap reading.
  - Implement --enable-gcov option for configure.

* Wed Aug 24 2005 Roland McGrath <roland@redhat.com> - 0.114-1
- update to 0.114
  - new program eu-ranlib
  - libdw: new calls for inlines
  - libdwfl: new calls for offline modules

* Sat Aug 13 2005 Roland McGrath <roland@redhat.com> - 0.113-2
- update to 0.113
  - elflint: relax a bit.  Allow version definitions for defined symbols
    against DSO versions also for symbols in nobits sections.
    Allow .rodata section to have STRINGS and MERGE flag set.
  - strip: add some more compatibility with binutils.
  - libdwfl: bug fixes.
- Separate libdw et al into elfutils-libs subpackage.

* Sat Aug  6 2005 Roland McGrath <roland@redhat.com> - 0.112-1
- update to 0.112
  - elfcmp: some more relaxation.
  - elflint: many more tests, especially regarding to symbol versioning.
  - libelf: Add elfXX_offscn and gelf_offscn.
  - libasm: asm_begin interface changes.
  - libebl: Add three new interfaces to directly access machine, class,
    and data encoding information.

* Fri Jul 29 2005 Roland McGrath <roland@redhat.com> - 0.111-2
- update portability patch

* Thu Jul 28 2005 Roland McGrath <roland@redhat.com> - 0.111-1
- update to 0.111
  - libdwfl library now merged into libdw

* Sun Jul 24 2005 Roland McGrath <roland@redhat.com> - 0.110-1
- update to 0.110

* Fri Jul 22 2005 Roland McGrath <roland@redhat.com> - 0.109-2
- update to 0.109
  - verify that libebl modules are from the same build
  - new eu-elflint checks on copy relocations
  - new program eu-elfcmp
  - new experimental libdwfl library

* Thu Jun  9 2005 Roland McGrath <roland@redhat.com> - 0.108-5
- robustification of eu-strip and eu-readelf

* Wed May 25 2005 Roland McGrath <roland@redhat.com> - 0.108-3
- more robustification

* Mon May 16 2005 Roland McGrath <roland@redhat.com> - 0.108-2
- robustification

* Mon May  9 2005 Roland McGrath <roland@redhat.com> - 0.108-1
- update to 0.108
  - merge strip fixes
  - sort records in dwarf_getsrclines, fix dwarf_getsrc_die searching
  - update elf.h from glibc

* Sun May  8 2005 Roland McGrath <roland@redhat.com> - 0.107-2
- fix strip -f byte-swapping bug

* Sun May  8 2005 Roland McGrath <roland@redhat.com> - 0.107-1
- update to 0.107
  - readelf: improve DWARF output format
  - elflint: -d option to support checking separate debuginfo files
  - strip: fix ET_REL debuginfo files (#156341)

* Mon Apr  4 2005 Roland McGrath <roland@redhat.com> - 0.106-3
- fix some bugs in new code, reenable make check

* Mon Apr  4 2005 Roland McGrath <roland@redhat.com> - 0.106-2
- disable make check for most arches, for now

* Mon Apr  4 2005 Roland McGrath <roland@redhat.com> - 0.106-1
- update to 0.106

* Mon Mar 28 2005 Roland McGrath <roland@redhat.com> - 0.104-2
- update to 0.104

* Wed Mar 23 2005 Jakub Jelinek <jakub@redhat.com> 0.103-2
- update to 0.103

* Wed Feb 16 2005 Jakub Jelinek <jakub@redhat.com> 0.101-2
- update to 0.101.
- use %%configure macro to get CFLAGS etc. right

* Sat Feb  5 2005 Jeff Johnson <jbj@redhat.com> 0.99-2
- upgrade to 0.99.

* Sun Sep 26 2004 Jeff Johnson <jbj@redhat.com> 0.97-3
- upgrade to 0.97.

* Tue Aug 17 2004 Jakub Jelinek <jakub@redhat.com> 0.95-5
- upgrade to 0.96.

* Mon Jul  5 2004 Jakub Jelinek <jakub@redhat.com> 0.95-4
- rebuilt with GCC 3.4.x, workaround VLA + alloca mixing
  warning

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr  2 2004 Jeff Johnson <jbj@redhat.com> 0.95-2
- upgrade to 0.95.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 0.94-1
- upgrade to 0.94

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 0.93-1
- upgrade to 0.93

* Thu Jan  8 2004 Jakub Jelinek <jakub@redhat.com> 0.92-1
- full version
- macroized spec file for GPL or OSL builds
- include only libelf under GPL plus wrapper scripts

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 0.91-2
- macroized spec file for GPL or OSL builds

* Wed Jan  7 2004 Ulrich Drepper <drepper@redhat.com>
- split elfutils-devel into two packages.

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 0.91-1
- include only libelf under GPL plus wrapper scripts

* Tue Dec 23 2003 Jeff Johnson <jbj@redhat.com> 0.89-3
- readelf, not readline, in %%description (#111214).

* Fri Sep 26 2003 Bill Nottingham <notting@redhat.com> 0.89-1
- update to 0.89 (fix eu-strip)

* Tue Sep 23 2003 Jakub Jelinek <jakub@redhat.com> 0.86-3
- update to 0.86 (fix eu-strip on s390x/alpha)
- libebl is an archive now; remove references to DSO

* Mon Jul 14 2003 Jeff Johnson <jbj@redhat.com> 0.84-3
- upgrade to 0.84 (readelf/elflint improvements, rawhide bugs fixed).

* Fri Jul 11 2003 Jeff Johnson <jbj@redhat.com> 0.83-3
- upgrade to 0.83 (fix invalid ELf handle on *.so strip, more).

* Wed Jul  9 2003 Jeff Johnson <jbj@redhat.com> 0.82-3
- upgrade to 0.82 (strip tests fixed on big-endian).

* Tue Jul  8 2003 Jeff Johnson <jbj@redhat.com> 0.81-3
- upgrade to 0.81 (strip excludes unused symtable entries, test borked).

* Thu Jun 26 2003 Jeff Johnson <jbj@redhat.com> 0.80-3
- upgrade to 0.80 (debugedit changes for kernel in progress).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Jeff Johnson <jbj@redhat.com> 0.79-2
- upgrade to 0.79 (correct formats for size_t, more of libdw "works").

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> 0.78-2
- upgrade to 0.78 (libdwarf bugfix, libdw additions).

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Jeff Johnson <jbj@redhat.com> 0.76-2
- use the correct way of identifying the section via the sh_info link.

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 0.75-2
- update to 0.75 (eu-strip -g fix)

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 0.74-2
- update to 0.74 (fix for writing with some non-dirty sections)

* Thu Feb  6 2003 Jeff Johnson <jbj@redhat.com> 0.73-3
- another -0.73 update (with sparc fixes).
- do "make check" in %%check, not %%install, section.

* Mon Jan 27 2003 Jeff Johnson <jbj@redhat.com> 0.73-2
- update to 0.73 (with s390 fixes).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Jakub Jelinek <jakub@redhat.com> 0.72-4
- fix arguments to gelf_getsymshndx and elf_getshstrndx
- fix other warnings
- reenable checks on s390x

* Sat Jan 11 2003 Karsten Hopp <karsten@redhat.de> 0.72-3
- temporarily disable checks on s390x, until someone has
  time to look at it

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 0.72-2
- update to 0.72

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> 0.71-2
- update to 0.71

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.69-4
- update to 0.69.
- add "make check" and segfault avoidance patch.
- elfutils-libelf needs to run ldconfig.

* Tue Dec 10 2002 Jeff Johnson <jbj@redhat.com> 0.68-2
- update to 0.68.

* Fri Dec  6 2002 Jeff Johnson <jbj@redhat.com> 0.67-2
- update to 0.67.

* Tue Dec  3 2002 Jeff Johnson <jbj@redhat.com> 0.65-2
- update to 0.65.

* Mon Dec  2 2002 Jeff Johnson <jbj@redhat.com> 0.64-2
- update to 0.64.

* Sun Dec 1 2002 Ulrich Drepper <drepper@redhat.com> 0.64
- split packages further into elfutils-libelf

* Sat Nov 30 2002 Jeff Johnson <jbj@redhat.com> 0.63-2
- update to 0.63.

* Fri Nov 29 2002 Ulrich Drepper <drepper@redhat.com> 0.62
- Adjust for dropping libtool

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 0.59-2
- update to 0.59

* Thu Nov 14 2002 Jeff Johnson <jbj@redhat.com> 0.56-2
- update to 0.56

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 0.54-2
- update to 0.54

* Sun Oct 27 2002 Jeff Johnson <jbj@redhat.com> 0.53-2
- update to 0.53
- drop x86_64 hack, ICE fixed in gcc-3.2-11.

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> 0.52-3
- get beehive to punch a rhpkg generated package.

* Wed Oct 23 2002 Jeff Johnson <jbj@redhat.com> 0.52-2
- build in 8.0.1.
- x86_64: avoid gcc-3.2 ICE on x86_64 for now.

* Tue Oct 22 2002 Ulrich Drepper <drepper@redhat.com> 0.52
- Add libelf-devel to conflicts for elfutils-devel

* Mon Oct 21 2002 Ulrich Drepper <drepper@redhat.com> 0.50
- Split into runtime and devel package

* Fri Oct 18 2002 Ulrich Drepper <drepper@redhat.com> 0.49
- integrate into official sources

* Wed Oct 16 2002 Jeff Johnson <jbj@redhat.com> 0.46-1
- Swaddle.
