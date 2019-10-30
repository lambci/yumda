# This is stable release:
#%%global rcversion RC1
Name:       pcre2
Version:    10.21
Release:    %{?rcversion:0.}22%{?rcversion:.%rcversion}%{?dist}
%global     myversion %{version}%{?rcversion:-%rcversion}
Summary:    Perl-compatible regular expression library
Group:      System Environment/Libraries
# the library:                          BSD
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text and declares Public Domain
#                                       for testdata
#Not distributed in binary package
# autotools:                            GPLv3+ with exception
# install-sh:                           MIT
# testdata:                             Public Domain
License:    BSD
URL:        http://www.pcre.org/
Source:     ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Do no set RPATH if libdir is not /usr/lib
Patch0:     pcre2-10.10-Fix-multilib.patch
# Report unmatched closing parantheses properly, in upstream after 10.21
Patch1:     pcre2-10.21-Detect-unmatched-closing-parentheses-in-the-pre-scan.patch
# Fix pcre2test for expressions with a callout inside a look-behind assertion,
# upstream bug #1783, fixed in upstream after 10.21
Patch2:     pcre2-10.21-Fix-pcre2test-loop-when-a-callout-is-in-an-initial-l.patch
# Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
# parentheses), upstream bug #1791, fixed in upstream after 10.21
Patch3:     pcre2-10.21-Fix-workspace-overflow-for-deep-nested-parentheses-w.patch
# Fix a typo in pcre2_study(), fixed in upstream after 10.21
Patch4:     pcre2-10.21-Fix-typo-in-pcre2_study.patch
# Fix a race in JIT locking condition, fixed in upstream after 10.21
Patch5:     pcre2-10.21-A-racing-condition-is-fixed-in-JIT-reported-by-Mozil.patch
# Fix an ovector check in JIT test program, fixed in upstream after 10.21
Patch6:     pcre2-10.21-Fix-typo-in-test-program.patch
# Enable JIT in the pcre2grep tool, fixed in upstream after 10.21
Patch7:     pcre2-10.21-Make-pcre2grep-use-JIT-it-was-omitted-by-mistake.patch
# Fix repeated pcregrep output if -o with -M options were used and the match
# extended over a line boundary, upstream bug #1848, fixed in upstream after
# 10.21
Patch8:     pcre2-10.21-Fix-bad-interaction-between-o-and-M-in-pcre2grep.patch
# Documentation for Fix-bad-interaction-between-o-and-M-in-pcre2grep.patch,
# upstream bug #1848, fixed in upstream after 10.21
Patch9:     pcre2-10.21-Documentation-clarification.patch
# Fix matching characters above 255 when a negative character type was used
# without enabled UCP in a positive class, in upstream after 10.22,
# upstream bug #1866
Patch10:    pcre2-10.22-Fix-bug-that-caused-chars-255-not-to-be-matched-by-c.patch
# Fix displaying a callout position in pcretest output with an escape sequence
# greater than \x{ff}, in upstream after 10.22
Patch11:    pcre2-10.22-Fix-callout-display-bug-in-pcre2test.patch
# 1/2 Fix pcrepattern(3) documentation, un upstream after 10.22
Patch12:    pcre2-10.22-Fix-typos-in-documentation.patch
# 2/2 Fix pcrepattern(3) documentation, in upstream after 10.22
Patch13:    pcre2-10.22-Missed-typo-fixed.patch
# 1/2 Fix miscopmilation of conditionals when a group name start with "R",
# fixed in upstream after 10.22 by code refactoring, upstream bug #1873
Patch14:    pcre2-10.22-Fix-bad-conditional-recursion-test-bug-when-a-group-.patch
# 2/2 Tests for Fix-bad-conditional-recursion-test-bug-when-a-group-.patch,
# in upstream after 10.22, upstream bug #1873
Patch15:    pcre2-10.21-Add-test-for-bug-already-fixed-by-the-refactoring.patch
# Fix internal option documentation in pcre2pattern(3), in upstream after 10.22,
# upstream bug #1875
Patch16:    pcre2-10.22-Fix-documentation-error.patch
# Fix optimization bugs for patterns starting with lookaheads,
# in upstream after 10.22, upstream bug #1882
Patch17:    pcre2-10.21-Fix-optimization-bugs-when-pattern-starts-with-looka.patch
# Document assert capture limitation, in upstream after 10.22,
# upstream bug #1887
Patch18:     pcre2-10.22-Document-current-assert-capture-limitation.patch
# Fix faulty auto-anchoring patterns when .* is inside an assertion,
# in upstream after 10.22
Patch19:    pcre2-10.22-Fix-auto-anchor-bug-when-.-is-inside-an-assertion.patch
# Fix pcre2-config --libs-posix output, in upstream after 10.22,
# upstream bug #1924
Patch20:    pcre2-10.22-Correct-libpcre2posix-typos-should-be-libpcre2-posix.patch
# Fix a memory leak and a typo in a documentation, in upstream after 10.22,
# upstream bug #1973
Patch21:    pcre2-10.22-Fix-small-memory-leak-in-error-code-path.patch
# Fix a buffer overflow in partial match test for CRLF in an empty buffer,
# in upsteam after 10.22, upstream bug #1975
Patch22:    pcre2-10.21-Fix-buffer-overflow-in-partial-match-test-for-CRLF-i.patch
# Fix a crash in pcre2test when displaying a wide character with a set locate,
# in upstream after 10.22, upstream bug #1976
Patch23:    pcre2-10.22-Fix-crash-in-pcre2test-when-displaying-a-wide-charac.patch
# Fix a crash when doing an extended substitution for \p, \P, or \X,
# in upstream after 10.22, upstream bug #1977
Patch24:    pcre2-10.21-Fix-NULL-defer-in-extended-substition-for-p-P-or-X.patch
# Fix a crash in substitution if starting offest was specified beyond the
# subject end, in upstream after 10.22, upstream bug #1992
Patch25:    pcre2-10.21-Fix-OOB-error-in-substitute-with-start-offset-longer.patch
# Fix compiling a class with UCP and without UTF, in upstream after 10.22
Patch26:    pcre2-10.22-Fix-class-bug-when-UCP-but-not-UTF-was-set-and-all-w.patch
# Fix an out-of-bound read in pcre2test tool within POSIX mode,
# in upstream after 10.22, upstream bug #2008
Patch27:    pcre2-10.21-Fix-pcre2test-mishandling-end-before-start-return-wi.patch
# Fix pcre2grep multi-line matching --only-matching option,
# in upstream 10.23, upstream bug #1848
Patch28:    pcre2-10.21-Fix-previously-broken-fix-for-pcre2grep-with-Mo-matc.patch
# New libtool to get rid of RPATH and to use distribution autotools
# Handle memmory allocation failures in pcre2test tool, in upstream after 10.23
Patch29:    pcre2-10.21-Check-malloc-returns-in-pcre2test.patch
# Fix CVE-2017-7186 (a crash when finding a Unicode property for a character
# with a code point greater than 0x10ffff in UTF-32 library while UTF mode is
# disabled), upstream bug #2052, in upstream after 10.23
Patch30:    pcre2-10.21-Fix-32-bit-non-UTF-property-test-crash.patch
# Fix a pcre2test bug for global match with zero terminated subject,
# upstream bug #2063, in upstream after 10.23
Patch31:    pcre2-10.21-Fix-pcre2test-bug-for-global-match-with-zero-termina.patch
# Close serialization file in pcre2test after any error, upstream bug #2074,
# in upstream after 10.23
Patch32:    pcre2-10.23-Close-serialization-file-in-pcre2test-after-any-erro.patch
# Fix a potential NULL dereference in pcre2_callout_enumerate() if called with
# a NULL pattern pointer when Unicode support is available, upstream bug #2076,
# in upstream after 10.23
Patch33:    pcre2-10.23-Fix-NULL-deference-if-pcre2_callout_enumerate-is-cal.patch
# Fix DFA match for a possessively repeated character class, upstream bug #2086,
# in upstream after 10.23
Patch34:    pcre2-10.21-Fix-misbehaving-DFA-match-for-possessively-repeated-.patch
# Use a memory allocator from the pattern if no context is supplied to
# pcre2_match(), in upsream after 10.23
Patch35:    pcre2-10.23-Fix-bug-introduced-at-10.21-use-memory-allocator-fro.patch
# Fix CVE-2017-7186 in JIT mode (a crash when finding a Unicode property for
# a character with a code point greater than 0x10ffff in UTF-32 library while
# UTF mode is disabled), bug #1434504, upstream bug #2052,
# in upstream after 10.23
Patch36:    pcre2-10.23-Fix-character-type-detection-when-32-bit-and-UCP-are.patch
# Fix an incorrect cast in UTF validation, upstream bug #2090,
# in upstream after 10.23
Patch37:    pcre2-10.23-Correct-an-incorrect-cast.patch
# Fix DFA matching a lookbehind assertion that has a zero-length branch,
# PCRE2 oss-fuzz issue 1859, in upstream after 10.23
Patch38:    pcre2-10.21-Fix-lookbehind-with-zero-length-branch-in-DFA-matchi.patch
# Fix returned offsets from regexec() when REG_STARTEND is used with starting offset
# greater than zero, upstream bug #2128, in upstream after 10.23
Patch39:    pcre2-10.21-Fix-matching-offsets-from-regexec-in-the-POSIX-wrapp.patch
# 1/2 Fix 32-bit error buffer size bug in pcre2test, CVE-2017-8786, bug #1500719,
# upstream bug #2079, in upstream after 10.23
Patch40:    pcre2-10.21-Fix-32-bit-error-buffer-size-bug-in-pcre2test-Bugzil.patch
# 2/2 Fix 32-bit error buffer size bug in pcre2test, CVE-2017-8786, bug #1500719,
# upstream bug #2079, in upstream after 10.23
Patch41:    pcre2-10.23-Previous-patch-was-not-quite-complete.patch
# 1/2 Accept files names longer than 128 bytes in recursive mode of pcre2grep,
# upstream bug #2177, in upstream after 10.30
Patch42:    pcre2-10.23-Fix-pcre2grep-recursive-file-name-length-issue.patch
# 2/2 Accept files names longer than 128 bytes in recursive mode of pcre2grep,
# upstream bug #2177, in upstream after 10.30
Patch43:    pcre2-10.30-Fix-memory-leak-issue-introduced-in-last-bug-fix-in-.patch
# Fix a subject buffer overread in JIT when UTF is disabled and \X or \R has
# a greater than 1 fixed quantifier, upstream bug #2320, in upstream after
# 10.32
Patch44:    pcre2-10.32-Fix-subject-buffer-overread-in-JIT.-Found-by-Yunho-K.patch
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
wrappers.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
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
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
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
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --disable-pcre2test-libedit \
    --enable-pcre2test-libreadline \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
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

%files
%{_libdir}/*.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS README

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc HACKING ./src/pcre2demo.c

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
* Tue Sep 18 2018 Petr Pisar <ppisar@redhat.com> - 10.21-22
- Fix a subject buffer overread in JIT when UTF is disabled and \X or \R has
  a greater than 1 fixed quantifier (upstream bug #2320)

* Thu Nov 02 2017 Petr Pisar <ppisar@redhat.com> - 10.21-21
- Accept files names longer than 128 bytes in recursive mode of pcre2grep
  (upstream bug #2177)

* Wed Nov 01 2017 Petr Pisar <ppisar@redhat.com> - 10.21-20
- Fix CVE-2017-8786 (32-bit error buffer size bug in pcre2test) (bug #1500719)

* Fri Jun 16 2017 Petr Pisar <ppisar@redhat.com> - 10.21-19
- Fix DFA matching a lookbehind assertion that has a zero-length branch
  (PCRE2 oss-fuzz issue 1859)
- Fix returned offsets from regexec() when REG_STARTEND is used with starting offset
  greater than zero (upstream bug #2128)

* Tue Apr 18 2017 Petr Pisar <ppisar@redhat.com> - 10.21-18
- Fix CVE-2017-7186 in JIT mode (a crash when finding a Unicode property for
  a character with a code point greater than 0x10ffff in UTF-32 library while
  UTF mode is disabled) (bug #1434504)
- Fix an incorrect cast in UTF validation (upstream bug #2090)

* Mon Mar 27 2017 Petr Pisar <ppisar@redhat.com> - 10.21-17
- Fix DFA match for a possessively repeated character class (upstream bug #2086)
- Use a memory allocator from the pattern if no context is supplied to
  pcre2_match()

* Wed Mar 22 2017 Petr Pisar <ppisar@redhat.com> - 10.21-16
- Close serialization file in pcre2test after any error (upstream bug #2074)
- Fix a potential NULL dereference in pcre2_callout_enumerate() if called with
  a NULL pattern pointer when Unicode support is available (upstream bug #2076)

* Mon Mar 20 2017 Petr Pisar <ppisar@redhat.com> - 10.21-15
- Fix a pcre2test bug for global match with zero terminated subject
  (upstream bug #2063)

* Mon Feb 27 2017 Petr Pisar <ppisar@redhat.com> - 10.21-14
- Handle memmory allocation failures in pcre2test tool
- Fix CVE-2017-7186 (a crash when finding a Unicode property for a character
  with a code point greater than 0x10ffff in UTF-32 library while UTF mode is
  disabled) (upstream bug #2052)

* Tue Feb 14 2017 Petr Pisar <ppisar@redhat.com> - 10.21-13
- Fix pcre2grep multi-line matching --only-matching option (upstream bug #1848)

* Tue Jan 03 2017 Petr Pisar <ppisar@redhat.com> - 10.21-12
- Fix compiling a class with UCP and without UTF
- Fix an out-of-bound read in pcre2test tool within POSIX mode
  (upstream bug #2008)

* Fri Dec 16 2016 Petr Pisar <ppisar@redhat.com> - 10.21-11
- Fix a crash when doing an extended substitution for \p, \P, or \X
  (upstream bug #1977)
- Fix a crash in substitution if starting offest was specified beyond the
  subject end (upstream bug #1992)

* Fri Dec 09 2016 Petr Pisar <ppisar@redhat.com> - 10.21-10
- Fix pcre2-config --libs-posix output (upstream bug #1924)
- Fix a memory leak and a typo in a documentation (upstream bug #1973)
- Fix a buffer overflow in partial match test for CRLF in an empty buffer
  (upstream bug #1975)
- Fix a crash in pcre2test when displaying a wide character with a set locate
  (upstream bug #1976)

* Tue Nov 08 2016 Petr Pisar <ppisar@redhat.com> - 10.21-9
- Fix faulty auto-anchoring patterns when .* is inside an assertion

* Mon Oct 24 2016 Petr Pisar <ppisar@redhat.com> - 10.21-8
- Disable the JIT on riscv64.
- Document assert capture limitation (upstream bug #1887)

* Wed Oct 19 2016 Petr Pisar <ppisar@redhat.com> - 10.21-7
- Fix displaying a callout position in pcretest output with an escape sequence
  greater than \x{ff}
- Fix pcrepattern(3) documentation
- Fix miscopmilation of conditionals when a group name start with "R"
  (upstream bug #1873)
- Fix internal option documentation in pcre2pattern(3) (upstream bug #1875)
- Fix optimization bugs for patterns starting with lookaheads
  (upstream bug #1882)

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 10.21-6
- Fix matching characters above 255 when a negative character type was used
  without enabled UCP in a positive class (upstream bug #1866)

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 10.21-5
- Fix repeated pcregrep output if -o with -M options were used and the match
  extended over a line boundary (upstream bug #1848)

* Fri Jun 10 2016 Petr Pisar <ppisar@redhat.com> - 10.21-4
- Fix a race in JIT locking condition
- Fix an ovector check in JIT test program
- Enable JIT in the pcre2grep tool

* Mon Feb 29 2016 Petr Pisar <ppisar@redhat.com> - 10.21-3
- Fix a typo in pcre2_study()

* Thu Feb 11 2016 Petr Pisar <ppisar@redhat.com> - 10.21-2
- Report unmatched closing parantheses properly
- Fix pcre2test for expressions with a callout inside a look-behind assertion
  (upstream bug #1783)
- Fix CVE-2016-3191 (workspace overflow for (*ACCEPT) with deeply nested
  parentheses) (upstream bug #1791)

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 10.21-1
- 10.21 bump

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

