# This is stable release:
#%%global rcversion RC1
Name:       pcre2
Version:    10.23
Release: %{?rcversion:0.}2%{?rcversion:.%rcversion}%{?dist}.0.2
%global     myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
Group:      System Environment/Libraries
# the library:                          BSD
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text and declares Public Domain
#                                       for testdata
#Not distributed in binary package
# aclocal.m4:                           FSFULLR and GPLv2+ with exception
# ar-lib:                               GPLv2+ with exception
# autotools:                            GPLv3+ with exception
# compile:                              GPLv2+ with exception
# config.sub:                           GPLv3+ with exception
# depcomp:                              GPLv2+ with exception
# install-sh:                           MIT
# ltmain.sh:                            GPLv2+ with exception and GPLv3+ with
#                                       exception and GPLv3+
# m4/ax_pthread.m4:                     GPLv3+ with exception
# m4/libtool.m4:                        FSFULLR and GPLv2+ with exception
# m4/ltoptions.m4:                      FSFULLR
# m4/ltsugar.m4:                        FSFULLR
# m4/ltversion.m4:                      FSFULLR
# m4/lt~obsolete.m4:                    FSFULLR
# m4/pcre2_visibility.m4:               FSFULLR
# missing:                              GPLv2+ with exception
# test-driver:                          GPLv2+ with exception
# testdata:                             Public Domain
License:    BSD
URL:        http://www.pcre.org/
Source:     ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre2-10.10-Fix-multilib.patch
# Handle memmory allocation failures in pcre2test tool, in upstream after 10.23
Patch1:     pcre2-10.23-Check-malloc-returns-in-pcre2test.patch
# Fix a compiler warning, proposed to upstream but not portable before ISO C99
# Fix a crash when finding a Unicode property for a character with a code
# point greater than 0x10ffff in UTF-32 library while UTF mode is disabled,
# upstream bug #2052, in upstream after 10.23
Patch2:     pcre2-10.23-Fix-32-bit-non-UTF-property-test-crash.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  readline-devel

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings. Install %{name}-utf16 or %{name}-utf32 packages for the other ones.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.

%package utf16
Summary:    UTF-16 variant of PCRE2
Group:      Development/Libraries
Conflicts:  %{name}%{?_isa} < 10.21-4

%description utf16
This is PCRE2 library working on UTF-16 strings.

%package utf32
Summary:    UTF-32 variant of PCRE2
Group:      Development/Libraries
Conflicts:  %{name}%{?_isa} < 10.21-4

%description utf32
This is PCRE2 library working on UTF-32 strings.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf16%{?_isa} = %{version}-%{release}
Requires:   %{name}-utf32%{?_isa} = %{version}-%{release}
Requires:   gcc

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%package static
Summary:    Static library for %{name}
Group:      Development/Libraries
Requires:   %{name}-devel%{_isa} = %{version}-%{release}

%description static
Library for static linking for %{name}.

%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
License:    BSD and GPLv3+
Group:      Development/Tools
Requires:   %{name}%{_isa} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.

%prep
%setup -q -n %{name}-%{myversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1
# Because of multilib patch
libtoolize --copy --force
autoreconf -vif

%build
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --disable-jit \
    --disable-pcre2grep-jit \
%else
    --enable-jit \
    --enable-pcre2grep-jit \
%endif
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-pcre2grep-callout \
    --enable-pcre2grep-jit \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
    --enable-pcre2test-libreadline \
    --disable-rebuild-chartables \
    --enable-shared \
    --enable-stack-for-recursion \
    --enable-static \
    --enable-unicode \
    --disable-valgrind
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre2

%check
make %{?_smp_mflags} check VERBOSE=yes

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post utf16 -p /sbin/ldconfig
%postun utf16 -p /sbin/ldconfig

%post utf32 -p /sbin/ldconfig
%postun utf32 -p /sbin/ldconfig

%files
%{_libdir}/libpcre2-8.so.*
%{_libdir}/libpcre2-posix.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS

%files utf16
%{_libdir}/libpcre2-16.so.*
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS

%files utf32
%{_libdir}/libpcre2-32.so.*
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c

%files static
%{_libdir}/*.a
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE

%files tools
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*

%changelog
* Mon Feb 27 2017 Petr Pisar <ppisar@redhat.com> - 10.23-2
- Handle memmory allocation failures in pcre2test tool
- Fix a crash when finding a Unicode property for a character with a code
  point greater than 0x10ffff in UTF-32 library while UTF mode is disabled
  (upstream bug #2052)

* Tue Feb 14 2017 Petr Pisar <ppisar@redhat.com> - 10.23-1
- 10.23 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.23-0.1.RC1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Petr Pisar <ppisar@redhat.com> - 10.23-0.1.RC1
- 10.23-RC1 bump

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 10.22-10.1
- Rebuild for readline 7.x

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 10.22-10
- Fix an out-of-bound read in pcre2test tool within POSIX mode
  (upstream bug #2008)

* Tue Jan 03 2017 Petr Pisar <ppisar@redhat.com> - 10.22-9
- Fix compiling a class with UCP and without UTF

* Fri Dec 16 2016 Petr Pisar <ppisar@redhat.com> - 10.22-8
- Fix a crash when doing an extended substitution for \p, \P, or \X
  (upstream bug #1977)
- Fix a crash in substitution if starting offest was specified beyond the
  subject end (upstream bug #1992)

* Fri Dec 09 2016 Petr Pisar <ppisar@redhat.com> - 10.22-7
- Fix pcre2-config --libs-posix output (upstream bug #1924)
- Fix a memory leak and a typo in a documentation (upstream bug #1973)
- Fix a buffer overflow in partial match test for CRLF in an empty buffer
  (upstream bug #1975)
- Fix a crash in pcre2test when displaying a wide character with a set locate
  (upstream bug #1976)

* Tue Nov 08 2016 Petr Pisar <ppisar@redhat.com> - 10.22-6
- Fix faulty auto-anchoring patterns when .* is inside an assertion

* Mon Oct 24 2016 Petr Pisar <ppisar@redhat.com> - 10.22-5
- Document assert capture limitation (upstream bug #1887)
- Ignore offset modifier in pcre2test in POSIX mode (upstream bug #1898)

* Wed Oct 19 2016 Richard W.M. Jones <@redhat.com> - 10.22-4
- Disable the JIT on riscv64.

* Wed Oct 19 2016 Petr Pisar <ppisar@redhat.com> - 10.22-3
- Fix displaying a callout position in pcretest output with an escape sequence
  greater than \x{ff}
- Fix pcrepattern(3) documentation
- Fix miscopmilation of conditionals when a group name start with "R"
  (upstream bug #1873)
- Fix internal option documentation in pcre2pattern(3) (upstream bug #1875)
- Fix optimization bugs for patterns starting with lookaheads
  (upstream bug #1882)

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 10.22-2
- Fix matching characters above 255 when a negative character type was used
  without enabled UCP in a positive class (upstream bug #1866)

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 10.22-1
- 10.22 bump

* Thu Jun 30 2016 Petr Pisar <ppisar@redhat.com> - 10.22-0.1.RC1
- 10.22-RC1 bump
- libpcre2-posix library changed ABI
- Fix register overwite in JIT when SSE2 acceleration is enabled
- Correct pcre2unicode(3) documentation

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 10.21-6
- Fix repeated pcregrep output if -o with -M options were used and the match
  extended over a line boundary (upstream bug #1848)

* Fri Jun 03 2016 Petr Pisar <ppisar@redhat.com> - 10.21-5
- Fix a race in JIT locking condition
- Fix an ovector check in JIT test program
- Enable JIT in the pcre2grep tool

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 10.21-4
- Ship README in devel as it covers API and build, not general info
- Move UTF-16 and UTF-32 libraries into pcre-ut16 and pcre-32 subpackages

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 10.21-3
- Fix a typo in pcre2_study()

* Thu Feb 11 2016 Petr Pisar <ppisar@redhat.com> - 10.21-2
- Report unmatched closing parantheses properly
- Fix pcre2test for expressions with a callout inside a look-behind assertion
  (upstream bug #1783)
- Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
  parentheses) (upstream bug #1791)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.21-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 10.21-1
- 10.21 bump

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 10.21-0.2.RC1
- Adapt a test to French locale on RHEL

* Tue Jan 05 2016 Petr Pisar <ppisar@redhat.com> - 10.21-0.1.RC1
- 10.21-RC1 bump

* Mon Oct 26 2015 Petr Pisar <ppisar@redhat.com> - 10.20-3
- Fix compiling patterns with PCRE2_NO_AUTO_CAPTURE (upstream bug #1704)

* Mon Oct 12 2015 Petr Pisar <ppisar@redhat.com> - 10.20-2
- Fix compiling classes with a negative escape and a property escape
  (upstream bug #1697)
- Fix integer overflow for patterns whose minimum matching length is large
  (upstream bug #1699)

* Fri Jul 03 2015 Petr Pisar <ppisar@redhat.com> - 10.20-1
- 10.20 bump

* Fri Jun 19 2015 Petr Pisar <ppisar@redhat.com> - 10.20-0.1.RC1
- 10.20-RC1 bump
- Replace dependency on glibc-headers with gcc (bug #1230479)
- Preserve soname

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.10-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 10.10-3
- fixed Release field

* Fri May 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 10.10-2.1
- Backport fix for AArch64

* Tue May 05 2015 Petr Pisar <ppisar@redhat.com> - 10.10-2
- Package pcre2demo.c as a documentation for pcre2-devel

* Fri Mar 13 2015 Petr Pisar <ppisar@redhat.com> - 10.10-1
- PCRE2 library packaged

