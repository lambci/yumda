%global perl_version    5.16.3
%global perl_epoch      4
%global perl_arch_stem -thread-multi
%global perl_archname %{_arch}-%{_os}%{perl_arch_stem}

%global multilib_64_archs aarch64 %{power64} s390x sparc64 x86_64
%global parallel_tests 1
%global tapsetdir   %{_datadir}/systemtap/tapset

%global dual_life 0
%global rebuild_from_scratch 0

# This overrides filters from build root (/etc/rpm/macros.perl)
# intentionally (unversioned perl(DB) is removed and versioned one is kept)
# Filter provides from *.pl files, bug #924938
# Filter *.so file from auto subdir only to keep providing libperl.so
%global __provides_exclude_from .*/auto/.*\\.so$|.*%{_docdir}|.*%{perl_archlib}/.*\\.pl$|.*%{perl_privlib}/.*\\.pl$
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)
# same as we provide in /etc/rpm/macros.perl
%global perl5_testdir   %{_libexecdir}/perl5-tests

# We can bootstrap without gdbm
%bcond_without gdbm
# We can skip %%check phase
%bcond_without test

Name:           perl
Version:        %{perl_version}
# release number must be even higher, because dual-lived modules will be broken otherwise
Release:        294%{?dist}
Epoch:          %{perl_epoch}
Summary:        Practical Extraction and Report Language
Group:          Development/Languages
# Modules Tie::File and Getopt::Long are licenced under "GPLv2+ or Artistic,"
# we have to reflect that in the sub-package containing them.
# under UCD are unicode tables
# Public domain: ext/SDBM_File/sdbm/*, ext/Compress-Raw-Bzip2/bzip2-src/dlltest.c 
# MIT: ext/MIME-Base64/Base64.xs 
# Copyright Only: for example ext/Text-Soundex/Soundex.xs 
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
Url:            http://www.perl.org/
Source0:        http://www.cpan.org/src/5.0/perl-%{perl_version}.tar.bz2
Source2:        perl-5.8.0-libnet.cfg
Source3:        macros.perl
#Systemtap tapset and example that make use of systemtap-sdt-devel
# build requirement. Written by lberk; Not yet upstream.
Source4:        perl.stp
Source5:        perl-example.stp

Patch0:         porting-podcheck-regen.patch
# Removes date check, Fedora/RHEL specific
Patch1:         perl-perlbug-tag.patch

# Fedora/RHEL only (64bit only)
Patch3:         perl-5.8.0-libdir64.patch

# Fedora/RHEL specific (use libresolv instead of libbind)
Patch4:         perl-5.10.0-libresolv.patch

# FIXME: May need the "Fedora" references removed before upstreaming
# patches ExtUtils-MakeMaker
Patch5:         perl-USE_MM_LD_RUN_PATH.patch

# Skip hostname tests, since hostname lookup isn't available in Fedora
# buildroots by design.
# patches Net::Config from libnet
Patch6:         perl-disable_test_hosts.patch

# The Fedora builders started randomly failing this futime test
# only on x86_64, so we just don't run it. Works fine on normal
# systems.
Patch7:         perl-5.10.0-x86_64-io-test-failure.patch

# switch off test, which is failing only on koji (fork)
Patch8:         perl-5.14.1-offtest.patch

# Fix find2perl to translate ? glob properly, rhbz#825701, RT#113054
Patch9:         perl-5.14.2-find2perl-transtate-question-mark-properly.patch

# Fix broken atof, rhbz#835452, RT#109318
Patch10:        perl-5.16.0-fix-broken-atof.patch

# Clear $@ before `do' I/O error, rhbz#834226, RT#113730
Patch13:        perl-5.16.1-RT-113730-should-be-cleared-on-do-IO-error.patch

# Do not truncate syscall() return value to 32 bits, rhbz#838551, RT#113980
Patch14:        perl-5.16.1-perl-113980-pp_syscall-I32-retval-truncates-the-retu.patch

# Override the Pod::Simple::parse_file, rhbz#826872, CPANRT#77530, in
# podlators-2.4.1
Patch15:        perl-5.14.2-Override-the-Pod-Simple-parse_file.patch

# Do not leak with attribute on my variable, rhbz#858966, RT#114764,
# fixed after 5.17.4
Patch16:        perl-5.16.1-perl-114764-Stop-my-vars-with-attrs-from-leaking.patch

# Allow operator after numeric keyword argument, rhbz#859328, RT#105924,
# fixed after 5.17.4
Patch17:        perl-5.16.1-perl-105924-require-1-2.patch

# Extend stack in File::Glob::glob, rhbz#859332, RT#114984, fixed after 5.17.4
Patch18:        perl-5.16.1-perl-114984-Glob.xs-Extend-stack-when-returning.patch

# Do not crash when vivifying $|, rhbz#865296, RT#115206
Patch19:        perl-5.16.1-perl-115206-Don-t-crash-when-vivifying.patch

# Fix CVE-2012-6329, rhbz#884354
Patch20:        perl-5.17.6-Fix-misparsing-of-maketext-strings.patch

# Add NAME heading into CPAN PODs, rhbz#908113, CPANRT#73396
Patch21:        perl-5.16.2-cpan-CPAN-add-NAME-headings-in-modules-with-POD.patch

# Fix leaking tied hashes, rhbz#859910, RT#107000, fixed after 5.17.4
Patch22:        perl-5.16.3-Don-t-leak-deleted-iterator-when-tying-hash.patch
Patch23:        perl-5.16.3-Free-iterator-when-freeing-tied-hash.patch
Patch24:        perl-5.16.3-Don-t-leak-if-hh-copying-dies.patch

# Fix dead lock in PerlIO after fork from thread, rhbz#947444, RT#106212
Patch25:        perl-5.17.9-106212-Add-PL_perlio_mutex-to-atfork_lock.patch

# Make regular expression engine safe in a signal handler, rhbz#849703,
# RT#114878, fixed after 5.17.11
Patch26:        perl-5.16.3-Remove-PERL_ASYNC_CHECK-from-Perl_leave_scope.patch

# Update h2ph(1) documentation, rhbz#948538, RT#117647
Patch27:        perl-5.19.0-Synchronize-h2ph-POD-text-with-usage-output.patch

# Update pod2html(1) documentation, rhbz#948538, RT#117623
Patch28:        perl-5.16.3-Synchronize-pod2html-usage-output-and-its-POD-text.patch

# Document Math::BigInt::CalcEmu requires Math::BigInt, rhbz#959096,
# CPAN RT#85015
Patch29:        perl-5.18.1-Document-Math-BigInt-CalcEmu-requires-Math-BigInt.patch 

# Use stronger algorithm needed for FIPS in t/op/crypt.t, bug #1084796,
# RT#121591
Patch30:        perl-5.18.2-t-op-crypt.t-Perform-SHA-256-algorithm-if-default-on.patch

# Make *DBM_File desctructors thread-safe, bug #1107542, RT#61912
Patch31:        perl-5.16.3-Destroy-GDBM-NDBM-ODBM-SDBM-_File-objects-only-from-.patch

# Use stronger algorithm needed for FIPS in t/op/taint.t, bug #1084796,
# RT#123338
Patch32:        perl-5.16.3-t-op-taint.t-Perform-SHA-256-algorithm-by-crypt-if-d.patch

# Remove CPU-speed-sensitive test in Benchmark test, bug #1238567,
# in upstream after 5.19.1
Patch33:        perl-5.16.3-Benchmark.t-remove-CPU-speed-sensitive-test.patch

# Make File::Glob work with threads again, bug #1223045
# RT#119897, in upstream after 5.19.5
Patch34:        perl-5.16.3-File-Glob-Dup-glob-state-in-CLONE.patch

# Fix CRLF conversion in ASCII FTP upload, bug #1263734, CPAN RT#41642
Patch35:        perl-5.16.3-Fix-incorrect-handling-of-CRLF-in-Net-FTP.patch

# Don't leak the temp utf8 copy of namepv, bug #1063330, CPAN RT#123786
Patch36:        perl-5.20.3-Don-t-leak-the-temp-utf8-copy-of-n.patch

# Fix duplicating PerlIO::encoding when spawning threads, bug #1344749,
# RT#31923, in upstream after 5.23.3
Patch37:        perl-5.16.3-Properly-duplicate-PerlIO-encoding-objects.patch

# Add SSL support to Net::SMTP, bug #1557574, CPAN RT#93823
Patch38:        perl-5.16.3-SSL-support-for-Net-SMTP.patch
Patch39:        perl-5.16.3-added-tests-for-Net-SMTP-SSL-save-arguments-in-Net-S.patch
Patch40:        perl-5.16.3-Fix-PAUSE-indexing-problem.patch
Patch41:        perl-5.16.3-use-SNI-for-SSL-support-in-SMTP.patch

# Do not overload ".." in Math::BigInt, bug #1497734, CPAN RT#80182,
# fixed in Math-BigInt-1.999718
Patch42:        perl-5.16.3-Fix-Math-BigInt-overload-warning.patch

# Fix an integer wrap when allocating memory for an environment variable,
# RT#133204, in upstream after 5.29.0 - CVE-2018-18311
Patch43:        perl-5.16.3-Perl_my_setenv-handle-integer-wrap.patch

# Amazon Patches
Patch100:       0001-gcc7-compat-fixes.patch

# Update some of the bundled modules
# see http://fedoraproject.org/wiki/Perl/perl.spec for instructions

BuildRequires:  groff, libdb-devel, tcsh, zlib-devel, bzip2-devel
BuildRequires:  systemtap-sdt-devel
%if %{with gdbm}
BuildRequires: gdbm-devel
%endif

# For tests
BuildRequires:  procps, rsyslog

# The long line of Perl provides.


# compat macro needed for rebuild
%global perl_compat perl(:MODULE_COMPAT_5.16.3)

# perl-interpreter denotes a package with the perl executable.
# Full EVR is for compatibility with systems that swapped perl and perl-core
# <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>.
Provides: perl-interpreter = %{perl_epoch}:%{perl_version}-%{release}

# Compat provides
Provides: %perl_compat
Provides: perl(:MODULE_COMPAT_5.16.2)
Provides: perl(:MODULE_COMPAT_5.16.1)
Provides: perl(:MODULE_COMPAT_5.16.0)

# Threading provides
Provides: perl(:WITH_ITHREADS)
Provides: perl(:WITH_THREADS)
# Largefile provides
Provides: perl(:WITH_LARGEFILES)
# PerlIO provides
Provides: perl(:WITH_PERLIO)
# File provides
Provides: perl(bytes_heavy.pl)
Provides: perl(dumpvar.pl)
Provides: perl(perl5db.pl)
Provides: perl(utf8_heavy.pl)

# suidperl isn't created by upstream since 5.12.0
Obsoletes: perl-suidperl <= 4:5.12.2

Requires: perl-libs = %{perl_epoch}:%{perl_version}-%{release}
# Time::HiRes needed by Net::Ping, bug #1122368
Requires: perl(Time::HiRes)

# We need this to break the dependency loop, and ensure that perl-libs 
# gets installed before perl.
Requires(post): perl-libs
# Same as perl-libs. We need macros in basic buildroot, where Perl is only
# because of git.
Requires(post): perl-macros


%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.  Perl is good at handling processes and files, and is especially
good at handling text.  Perl's hallmarks are practicality and efficiency.
While it is used to do a lot of different things, Perl's most common
applications are system administration utilities and web programming.  A large
proportion of the CGI scripts on the web are written in Perl.  You need the
perl package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your system to
handle Perl scripts.

%package libs
Summary:        The libraries for the perl runtime
Group:          Development/Languages
License:        GPL+ or Artistic
# Interpreter version to fulfil requires based on "require 5.006;"
Provides:       perl(:VERSION) = %{perl_version}
Requires:       %perl_compat

%description libs
The libraries for the perl runtime


%package devel
Summary:        Header #files for use in perl development
Group:          Development/Languages
License:        GPL+ or Artistic
# Require $Config{libs} providers, bug #905482
Requires:       libdb-devel
%if %{with gdbm}
Requires:       gdbm-devel
%endif
Requires:       glibc-devel
Requires:       systemtap-sdt-devel
Requires:       perl(ExtUtils::ParseXS)
Requires:       %perl_compat

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.


%package macros
Summary:        Macros for rpmbuild
Group:          Development/Languages
License:        GPL+ or Artistic
Requires:       %perl_compat

%description macros
Macros for rpmbuild are needed during build of srpm in koji. This
sub-package must be installed into buildroot, so it will be needed
by perl. Perl is needed because of git.


%package tests
Summary:        The Perl test suite
Group:          Development/Languages
License:        GPL+ or Artistic
# right?
AutoReqProv:    0
Requires:       %perl_compat
# FIXME - note this will need to change when doing the core/minimal swizzle
Requires:       perl-core

%description tests
This package contains the test suite included with Perl %{perl_version}.

Install this if you want to test your Perl installation (binary and core
modules).


%if %{dual_life} || %{rebuild_from_scratch}
%package Archive-Extract
Summary:        Generic archive extracting mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.58
Requires:       %perl_compat
BuildArch:      noarch

%description Archive-Extract
Archive::Extract is a generic archive extraction mechanism.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Archive-Tar
Summary:        A module for Perl manipulation of .tar files
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.82 
Requires:       %perl_compat
Requires:       perl(Compress::Zlib), perl(IO::Zlib)
BuildArch:      noarch

%description Archive-Tar
Archive::Tar provides an object oriented mechanism for handling tar files.  It
provides class methods for quick and easy files handling while also allowing
for the creation of tar file objects for custom manipulation.  If you have the
IO::Zlib module installed, Archive::Tar will also support compressed or
gzipped tar files.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package autodie
Summary:        Replace functions with ones that succeed or die
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.10
Requires:       %perl_compat
BuildArch:      noarch
Requires:       perl(B)
Requires:       perl(Fcntl)
Requires:       perl(overload)
Requires:       perl(POSIX)
Conflicts:      perl < 4:5.16.2-259

%description autodie
The "autodie" and "Fatal" pragma provides a convenient way to replace
functions that normally return false on failure with equivalents that throw an
exception on failure.

However "Fatal" has been obsoleted by the new autodie pragma. Please use
autodie in preference to "Fatal".
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package B-Lint
Summary:        Perl lint
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.14
Requires:       %perl_compat
Requires:       perl(constant)
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-251

%description B-Lint
The B::Lint module is equivalent to an extended version of the -w option of
perl. It is named after the program lint which carries out a similar process
for C programs.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Carp
Summary:        Alternative warn and die for modules
Epoch:          0
Version:        1.26
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
Provides:       perl(Carp::Heavy) = %{version}
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Carp\\)\\s*$

%description Carp
The Carp routines are useful in your own modules because they act like
die() or warn(), but with a message which is more likely to be useful to a
user of your module. In the case of cluck, confess, and longmess that
context is a summary of every call in the call-stack. For a shorter message
you can use carp or croak which report the error as being from where your
module was called. There is no guarantee that that is where the error was,
but it is a good educated guess.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CGI
Summary:        Handle Common Gateway Interface requests and responses
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.59
Requires:       %perl_compat
Provides:       perl(CGI) = %{version}
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(CGI\\)\\s*$
# Do not export private modules
%global __provides_exclude %{__provides_exclude}|^perl\\(Fh\\)\\s*$
%global __provides_exclude %{__provides_exclude}|^perl\\(MultipartBuffer\\)\\s*$
%global __provides_exclude %{__provides_exclude}|^perl\\(utf8\\)\\s*$

%description CGI
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string generation
and manipulation, and processing and preparing HTTP headers. Some HTML
generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes
with built-in support for mod_perl and mod_perl2 as well as FastCGI.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Compress-Raw-Bzip2
Summary:        Low-Level Interface to bzip2 compression library
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.048
Requires:       perl(Exporter), perl(File::Temp)

%description Compress-Raw-Bzip2
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.

%package Compress-Raw-Zlib
Summary:        Low-Level Interface to the zlib compression library
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.048
Requires:       %perl_compat

%description Compress-Raw-Zlib
This module provides a Perl interface to the zlib compression library.
It is used by IO::Compress::Zlib.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package constant
Summary:        Perl pragma to declare constants
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.23
Requires:       %perl_compat
Requires:       perl(Carp)
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-264

%description constant
This pragma allows you to declare constants at compile-time:

use constant PI => 4 * atan2(1, 1);

When you declare a constant such as "PI" using the method shown above,
each machine your script runs upon can have as many digits of accuracy
as it can use. Also, your program will be easier to read, more likely
to be maintained (and maintained correctly), and far less likely to
send a space probe to the wrong planet because nobody noticed the one
equation in which you wrote 3.14195.

When a constant is used in an expression, Perl replaces it with its
value at compile time, and may then optimize the expression further.
In particular, any code in an "if (CONSTANT)" block will be optimized
away if the constant is false.
%endif

%package CPAN
Summary:        Query, download and build perl modules from CPAN sites
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.9800
Requires:       perl(Data::Dumper)
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
# local::lib recommended by CPAN::FirstTime default choice, bug #1122368
Requires:       perl(local::lib)
Requires:       %perl_compat
Provides:       cpan = %{version}
BuildArch:      noarch

%description CPAN
Query, download and build perl modules from CPAN sites.

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Epoch:          0
Version:        2.120630
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
BuildArch:      noarch

%description CPAN-Meta
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-Requirements
Summary:        Set of version requirements for a CPAN dist
Epoch:          0
Version:        2.120.630
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
BuildArch:      noarch

%description CPAN-Meta-Requirements
A CPAN::Meta::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions.
It can be built up by adding more and more constraints, and it will reduce
them to the simplest representation.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-YAML
Version:        0.007
Epoch:          0
Summary:        Read and write a subset of YAML for CPAN Meta files
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %perl_compat

%description CPAN-Meta-YAML
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPANPLUS
Summary:        API & CLI access to the CPAN mirrors
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# real version 0.9121
Version:        0.91.21
# CPANPLUS encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Module::Pluggable) >= 2.4
Requires:       perl(Module::CoreList)
Requires:       %perl_compat
BuildArch:      noarch

%description CPANPLUS
The CPANPLUS library is an API to the CPAN mirrors and a collection of
interactive shells, commandline programs, etc, that use this API.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPANPLUS-Dist-Build
Summary:        Module::Build extension for CPANPLUS
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.62
Requires:       %perl_compat
# This is a plug-in for CPANPLUS, specify reverse dependency here
Requires:       perl(CPANPLUS)
BuildArch:      noarch

%description CPANPLUS-Dist-Build
CPANPLUS::Dist::Build is a distribution class for Module::Build related
modules. With this package, you can create, install and uninstall
Module::Build-based perl modules by calling CPANPLUS::Dist methods.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Data-Dumper
Summary:        Stringify perl data structures, suitable for printing and eval
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.135.06
Requires:       %perl_compat
Requires:       perl(Scalar::Util)
Requires:       perl(XSLoader)

%description Data-Dumper
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package DB_File
Summary:        Perl5 access to Berkeley DB version 1.x
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.826
Requires:       %perl_compat
Requires:       perl(Fcntl)
Requires:       perl(XSLoader)
Conflicts:      perl < 4:5.16.3-264

%description DB_File
DB_File is a module which allows Perl programs to make use of the facilities
provided by Berkeley DB version 1.x (if you have a newer version of DB, you
will be limited to functionality provided by interface of version 1.x). The
interface defined here mirrors the Berkeley DB interface closely.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest
Summary:        Modules that calculate message digests
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        1.17
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(MIME::Base64)

%description Digest
The Digest:: modules calculate digests, also called "fingerprints" or
"hashes", of some data, called a message. The digest is (usually)
some small/fixed size string. The actual size of the digest depend of
the algorithm used. The message is simply a sequence of arbitrary
bytes or bits.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-MD5
Summary:        Perl interface to the MD5 Algorithm
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        2.51
Requires:       %perl_compat
Requires:       perl(XSLoader)
# Recommended
Requires:       perl(Digest::base) >= 1.00

%description Digest-MD5
The Digest::MD5 module allows you to use the RSA Data Security Inc. MD5
Message Digest algorithm from within Perl programs. The algorithm takes as
input a message of arbitrary length and produces as output a 128-bit
"fingerprint" or "message digest" of the input.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-SHA
Summary:        Perl extension for SHA-1/224/256/384/512
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        5.71
Requires:       %perl_compat
# Recommended
Requires:       perl(Digest::base)
Requires:       perl(MIME::Base64)

%description Digest-SHA
Digest::SHA is a complete implementation of the NIST Secure Hash
Standard.  It gives Perl programmers a convenient way to calculate
SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 message digests.  The
module can handle all types of input, including partial-byte data.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Encode
Summary:        Character encodings in Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.44.01
Requires:       %perl_compat
Conflicts:      perl < 4:5.16.2-256

%description Encode
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

%package Encode-devel
Summary:        Character encodings in Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.44.01
Requires:       %perl_compat
Requires:       %{name}-Encode = %{epoch}:%{version}-%{release}
Requires:       perl-devel
BuildArch:      noarch

%description Encode-devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Env
Summary:        Perl module that imports environment variables as scalars or arrays
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.03
Requires:       %perl_compat
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-265

%description Env
Perl maintains environment variables in a special hash named %%ENV. For when
this access method is inconvenient, the Perl module Env allows environment
variables to be treated as scalar or array variables.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Exporter
Summary:        Implements default import method for modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        5.66
Requires:       %perl_compat
Requires:       perl(Carp) >= 1.05
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-265

%description Exporter
The Exporter module implements an import method which allows a module to
export functions and variables to its users' name spaces. Many modules use
Exporter rather than implementing their own import method because Exporter
provides a highly flexible interface, with an implementation optimized for
the common case.
%endif

%package ExtUtils-CBuilder
Summary:        Compile and link C code for Perl modules
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
# real version 0.280206 https://fedoraproject.org/wiki/Perl/Tips#Dot_approach
Version:        0.28.2.6
Requires:       perl-devel
Requires:       %perl_compat
BuildArch:      noarch

%description ExtUtils-CBuilder
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.


%package ExtUtils-Embed
Summary:        Utilities for embedding Perl in C/C++ applications
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.30
Requires:       perl-devel
Requires:       %perl_compat
BuildArch:      noarch

%description ExtUtils-Embed
Utilities for embedding Perl in C/C++ applications.


%package ExtUtils-Install
Summary:        Install files from here to there
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.58
Requires:       perl-devel
Requires:       %perl_compat
BuildArch:      noarch

%description ExtUtils-Install
Handles the installing and uninstalling of perl modules, scripts, man
pages, etc.

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-MakeMaker
Summary:        Create a module Makefile
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        6.63.2
Requires:       perl-devel
Requires:       %perl_compat
Requires:       perl(ExtUtils::Install)
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(Test::Harness)
# Optional run-time needed for generating documentation from POD:
Requires:       perl(Pod::Man)
BuildArch:      noarch

# Filter false DynaLoader provides. Versioned perl(DynaLoader) keeps
# unfiltered on perl package, no need to reinject it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader\\)\\s*$
%global __provides_exclude %__provides_exclude|^perl\\(ExtUtils::MakeMaker::_version\\)

%description ExtUtils-MakeMaker
Create a module Makefile.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Manifest
Summary:        Utilities to write and check a MANIFEST file
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.61
Requires:       perl-devel
Requires:       %perl_compat
Requires:       perl(File::Path)
BuildArch:      noarch

%description ExtUtils-Manifest
%{summary}.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-ParseXS
Summary:        Module and a script for converting Perl XS code into C code
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.16
Requires:       perl-devel
Requires:       %perl_compat
BuildArch:      noarch
Obsoletes:      perl-ExtUtils-Typemaps

%description ExtUtils-ParseXS
ExtUtils::ParseXS will compile XS code into C code by embedding the constructs
necessary to let C functions manipulate Perl values and creates the glue
necessary to let Perl access those functions.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package File-CheckTree
Summary:        Run many file-test checks on a tree
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        4.41
Requires:       %perl_compat
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-256

%description File-CheckTree
File::CheckTree::validate() routine takes a single multi-line string
consisting of directives, each containing a file name plus a file test to try
on it. (The file test may also be a "cd", causing subsequent relative file
names to be interpreted relative to that directory.) After the file test you
may put || die to make it a fatal error if the file test fails. The default is
|| warn.  The file test may optionally have a "!' prepended to test for the
opposite condition. If you do a cd and then list some relative file names, you
may want to indent them slightly for readability. If you supply your own die()
or warn() message, you can use $file to interpolate the file name.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Fetch
Summary:        Generic file fetching mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.32 
Requires:       perl(IPC::Cmd) >= 0.36
Requires:       perl(Module::Load::Conditional) >= 0.04
Requires:       perl(Params::Check) >= 0.07
Requires:       %perl_compat
BuildArch:      noarch

%description File-Fetch
File::Fetch is a generic file fetching mechanism.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Path
Summary:        Create or remove directory trees
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.08.01
Requires:       %perl_compat
Requires:       perl(Carp)
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-265

%description File-Path
This module provides a convenient way to create directories of arbitrary
depth and to delete an entire directory subtree from the file system.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Temp
Summary:        Return name and handle of a temporary file safely
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.22
Requires:       %perl_compat
BuildArch:      noarch
Requires:       perl(File::Path) >= 2.06
Requires:       perl(POSIX)
Conflicts:      perl < 4:5.16.2-265

%description File-Temp
File::Temp can be used to create and open temporary files in a safe way.
There is both a function interface and an object-oriented interface. The
File::Temp constructor or the tempfile() function can be used to return the
name and the open file handle of a temporary file. The tempdir() function
can be used to create a temporary directory.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
# FIXME Filter-Simple? version?
%package Filter
Summary:        Perl source filters
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.40
Requires:       %perl_compat

%description Filter
Source filters alter the program text of a module before Perl sees it, much as
a C preprocessor alters the source text of a C program before the compiler
sees it.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Getopt-Long
Summary:        Extended processing of command line options
Group:          Development/Libraries
License:        GPLv2+ or Artistic
Epoch:          0
Version:        2.38
Requires:       %perl_compat
Requires:       perl(overload)
Requires:       perl(Text::ParseWords)
# Recommended:
Requires:       perl(Pod::Usage) >= 1.14
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-268

%description Getopt-Long
The Getopt::Long module implements an extended getopt function called
GetOptions(). It parses the command line from @ARGV, recognizing and removing
specified options and their possible values.  It adheres to the POSIX syntax
for command line options, with GNU extensions. In general, this means that
options have long names instead of single letters, and are introduced with
a double dash "--". Support for bundling of command line options, as was the
case with the more traditional single-letter approach, is provided but not
enabled by default.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Compress
Summary:        IO::Compress wrapper for modules
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.048
Requires:       %perl_compat
Obsoletes:      perl-Compress-Zlib <= 2.020
Provides:       perl(IO::Uncompress::Bunzip2)
BuildArch:      noarch

%description IO-Compress
This module is the base class for all IO::Compress and IO::Uncompress modules.
This module is not intended for direct use in application code. Its sole
purpose is to to be sub-classed by IO::Compress modules.
%endif

%package IO-Zlib
Summary:        Perl IO:: style interface to Compress::Zlib
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.10
Requires:       perl(Compress::Zlib)
Requires:       %perl_compat
BuildArch:      noarch

%description IO-Zlib
This modules provides an IO:: style interface to the Compress::Zlib package.
The main advantage is that you can use an IO::Zlib object in much the same way
as an IO::File object so you can have common code that doesn't know which sort
of file it is using.


%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-Cmd
Summary:        Finding and running system commands made easy
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.76
Requires:       perl(ExtUtils::MakeMaker)
Requires:       %perl_compat
BuildArch:      noarch

%description IPC-Cmd
IPC::Cmd allows you to run commands, interactively if desired, in a platform
independent way, but have them still work.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package HTTP-Tiny
Summary:        A small, simple, correct HTTP/1.1 client
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.017
Requires:       perl(bytes)
Requires:       perl(Carp)
Requires:       perl(IO::Socket)
Requires:       perl(Time::Local)
BuildArch:      noarch

%description HTTP-Tiny
This is a very simple HTTP/1.1 client, designed primarily for doing simple GET 
requests without the overhead of a large framework like LWP::UserAgent.
It is more correct and more complete than HTTP::Lite. It supports proxies 
(currently only non-authenticating ones) and redirection. It also correctly 
resumes after EINTR.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package JSON-PP
Summary:        JSON::XS compatible pure-Perl module
Epoch:          0
# 2.27150 version is a typo but we cannot fix it because it would break
# monotony
Version:        2.27200
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %perl_compat 
Conflicts:      perl-JSON < 2.50

%description JSON-PP
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.
JSON::PP is a pure-Perl module and is compatible with JSON::XS.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Locale-Codes
Summary:        Distribution of modules to handle locale codes
Epoch:          0
Version:        3.21
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
Requires:       perl(constant)
Provides:       perl(Locale::Codes) = %{version}
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Locale::Codes\\)\\s*$

%description Locale-Codes
Locale-Codes is a distribution containing a set of modules. The modules
each deal with different types of codes which identify parts of the locale
including languages, countries, currency, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Locale-Maketext
Summary:        Framework for localization
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.22
Requires:       %perl_compat
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-268

%description Locale-Maketext
It is a common feature of applications (whether run directly, or via the Web)
for them to be "localized" -- i.e., for them to present an English interface
to an English-speaker, a German interface to a German-speaker, and so on for
all languages it's programmed with. Locale::Maketext is a framework for
software localization; it provides you with the tools for organizing and
accessing the bits of text and text-processing code that you need for
producing localized applications.
%endif

%package Locale-Maketext-Simple
Summary:        Simple interface to Locale::Maketext::Lexicon
Group:          Development/Libraries
License:        MIT
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.21
Requires:       %perl_compat
BuildArch:      noarch

%description Locale-Maketext-Simple
This module is a simple wrapper around Locale::Maketext::Lexicon, designed
to alleviate the need of creating Language Classes for module authors.


%if %{dual_life} || %{rebuild_from_scratch}
%package Log-Message
Summary:        Generic message storage mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.04
Requires:       %perl_compat
# Add a versioned provides, since we pull the unversioned one out.
Provides:       perl(Log::Message::Handlers) = %{version}
BuildArch:      noarch

%description Log-Message
Log::Message is a generic message storage mechanism. It allows you to store
messages on a stack -- either shared or private -- and assign meta-data to it.
Some meta-data will automatically be added for you, like a timestamp and a
stack trace, but some can be filled in by the user, like a tag by which to
identify it or group it, and a level at which to handle the message (for
example, log it, or die with it).
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Log-Message-Simple
Summary:        Simplified frontend to Log::Message
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.08
Requires:       %perl_compat
BuildArch:      noarch

%description Log-Message-Simple
This module provides standardized logging facilities using the
Log::Message module.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Build
Summary:        Perl module for building and installing Perl modules
Group:          Development/Libraries
License:        GPL+ or Artistic
# Check epoch with standalone package
Epoch:          2
# real version 0.39_01
Version:        0.39.01 
Requires:       perl(Archive::Tar) >= 1.08
Requires:       perl(CPAN::Meta) >= 2.110420
Requires:       perl(ExtUtils::CBuilder) >= 0.15
Requires:       perl(ExtUtils::ParseXS) >= 1.02
Requires:       perl-devel
Requires:       %perl_compat
# Optional run-time needed for generating documentation from POD:
Requires:       perl(Pod::Html)
Requires:       perl(Pod::Man)
Requires:       perl(Pod::Text)
BuildArch:      noarch

%description Module-Build
Module::Build is a system for building, testing, and installing Perl modules.
It is meant to be an alternative to ExtUtils::MakeMaker.  Developers may alter
the behavior of the module through subclassing in a much more straightforward
way than with MakeMaker. It also does not require a make on your system - most
of the Module::Build code is pure-perl and written in a very cross-platform
way. In fact, you don't even need a shell, so even platforms like MacOS
(traditional) can use it fairly easily. Its only prerequisites are modules that
are included with perl 5.6.0, and it works fine on perl 5.005 if you can
install a few additional modules.
%endif

%package Module-CoreList
Summary:        Perl core modules indexed by perl versions
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          1
Version:        2.76.02
Requires:       %perl_compat
Requires:       perl(version)
BuildArch:      noarch

%description Module-CoreList
Module::CoreList contains the hash of hashes %%Module::CoreList::version, this
is keyed on perl version as indicated in $].  The second level hash is module
=> version pairs.


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load
Summary:        Runtime require of both modules and files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.22
Requires:       %perl_compat
BuildArch:      noarch

%description Module-Load
Module::Load eliminates the need to know whether you are trying to require
either a file or a module.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load-Conditional
Summary:        Looking up module information / loading at runtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.46
Requires:       %perl_compat
BuildArch:      noarch

%description Module-Load-Conditional
Module::Load::Conditional provides simple ways to query and possibly load any
of the modules you have installed on your system during runtime.
%endif


%package Module-Loaded
Summary:        Mark modules as loaded or unloaded
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.08
Requires:       %perl_compat
BuildArch:      noarch

%description Module-Loaded
When testing applications, often you find yourself needing to provide
functionality in your test environment that would usually be provided by
external modules. Rather than munging the %%INC by hand to mark these external
modules as loaded, so they are not attempted to be loaded by perl, this module
offers you a very simple way to mark modules as loaded and/or unloaded.


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Metadata
Summary:        Gather package and POD information from perl module files
Epoch:          0
Version:        1.000009
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %perl_compat

%description Module-Metadata
Gather package and POD information from perl module files
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Pluggable
Summary:        Automatically give your module the ability to have plugins
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
# Keep two digit decimal part
Version:        4.00 
Requires:       %perl_compat
BuildArch:      noarch

%description Module-Pluggable
Provides a simple but, hopefully, extensible way of having 'plugins' for your
module.
%endif


%package Object-Accessor
Summary:        Perl module that allows per object accessors
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.42
Requires:       %perl_compat
BuildArch:      noarch

%description Object-Accessor
Object::Accessor provides an interface to create per object accessors (as
opposed to per Class accessors, as, for example, Class::Accessor provides).


%package Package-Constants
Summary:        List all constants declared in a package
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.02
Requires:       %perl_compat
BuildArch:      noarch

%description Package-Constants
Package::Constants lists all the constants defined in a certain package.  This
can be useful for, among others, setting up an autogenerated @EXPORT/@EXPORT_OK
for a Constants.pm file.

%if %{dual_life} || %{rebuild_from_scratch}
%package PathTools
Summary:        PathTools Perl module (Cwd, File::Spec)
Group:          Development/Libraries
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        3.39.2
Requires:       %perl_compat
Requires:       perl(Carp)

%description PathTools
PathTools Perl module (Cwd, File::Spec).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Params-Check
Summary:        Generic input parsing/checking mechanism
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.32
Requires:       %perl_compat
BuildArch:      noarch

%description Params-Check
Params::Check is a generic input parsing/checking mechanism.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Parse-CPAN-Meta
Summary:        Parse META.yml and other similar CPAN metadata files
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.4402
Requires:       %perl_compat
BuildArch:      noarch
Requires:       perl(CPAN::Meta::YAML) >= 0.002
Requires:       perl(JSON::PP) >= 2.27103
# FIXME it could be removed now?
Obsoletes:      perl-Parse-CPAN-Meta < 1.40

%description Parse-CPAN-Meta 
Parse::CPAN::Meta is a parser for META.yml files, based on the parser half of
YAML::Tiny.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Perl-OSType
Summary:        Map Perl operating system names to generic types
Version:        1.002
Epoch:          0
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
BuildArch:      noarch

%description Perl-OSType
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.
This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Checker
Summary:        Check POD documents for syntax errors
License:        GPL+ or Artistic
Group:          Development/Libraries
Requires:       %perl_compat
BuildArch:      noarch

%description Pod-Checker
Module and tools to verify POD documentation contents for compliance with the
Plain Old Documentation format specifications.
%endif

%package Pod-Escapes
Summary:        Perl module for resolving POD escape sequences
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.04
Requires:       %perl_compat
BuildArch:      noarch

%description Pod-Escapes
This module provides things that are useful in decoding Pod E<...> sequences.
Presumably, it should be used only by Pod parsers and/or formatters.

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-LaTeX
Summary:        Convert POD data to formatted LaTeX
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.60
Requires:       %perl_compat
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-248

%description Pod-LaTeX
Pod::LaTeX is a module to convert documentation in the POD format into
LaTeX. A pod2latex replacement command is provided.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Parser
Summary:        Basic perl modules for handling Plain Old Documentation (POD)
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.51
Requires:       %perl_compat
BuildArch:      noarch

%description Pod-Parser
This software distribution contains the packages for using Perl5 POD (Plain
Old Documentation). See the "perlpod" and "perlsyn" manual pages from your
Perl5 distribution for more information about POD.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Perldoc
Summary:        Look up Perl documentation in Pod format
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.17.00
# Pod::Perldoc::ToMan executes roff
Requires:       groff-base
Requires:       %perl_compat
BuildArch:      noarch

%description Pod-Perldoc
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Simple
Summary:        Framework for parsing POD documentation
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.20
Requires:       %perl_compat
BuildArch:      noarch

%description Pod-Simple
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Usage
Summary:        Print a usage message from embedded pod documentation
License:        GPL+ or Artistic
Group:          Development/Libraries
# Pod::Usage execute perldoc from perl-Pod-Perldoc by default
BuildRequires:  perl-Pod-Perldoc
Requires:       %perl_compat
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
Requires:       perl-Pod-Perldoc
Requires:       perl(Pod::Text)
BuildArch:      noarch

%description Pod-Usage
pod2usage will print a usage message for the invoking script (using its
embedded POD documentation) and then exit the script with the desired exit
status. The usage message printed may have any one of three levels of
"verboseness": If the verbose level is 0, then only a synopsis is printed.
If the verbose level is 1, then the synopsis is printed along with a
description (if present) of the command line options and arguments. If the
verbose level is 2, then the entire manual page is printed.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package podlators
Summary:        Format POD source into various output formats
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.4.0
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Pod::Simple) >= 3.06
Conflicts:      perl < 4:5.16.1-234

%description podlators
This package contains Pod::Man and Pod::Text modules which convert POD input
to *roff source output, suitable for man pages, or plain text.  It also
includes several sub-classes of Pod::Text for formatted output to terminals
with various capabilities.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Scalar-List-Utils
Summary:        A selection of general-utility scalar and list subroutines
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.25
Requires:       %perl_compat

%description Scalar-List-Utils
Scalar::Util and List::Util contain a selection of subroutines that people have
expressed would be nice to have in the perl core, but the usage would not
really be high enough to warrant the use of a keyword, and the size so small
such that being individual extensions would be wasteful.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Storable
Summary:        Persistence for Perl data structures
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.34
Requires:       %perl_compat
# Carp substitutes missing Log::Agent
Requires:       perl(Carp)
Requires:       perl(Config)
# Fcntl is optional, but locking is good
Requires:       perl(Fcntl)
Requires:       perl(IO::File)
Conflicts:      perl < 4:5.16.3-274

%description Storable
The Storable package brings persistence to your Perl data structures
containing scalar, array, hash or reference objects, i.e. anything that
can be conveniently stored to disk and retrieved at a later time.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Sys-Syslog
Summary:        Perl interface to the UNIX syslog(3) calls
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.29
Requires:       %perl_compat
Requires:       perl(XSLoader)
Conflicts:      perl < 4:5.16.3-269

%description Sys-Syslog
Sys::Syslog is an interface to the UNIX syslog(3) function. Call syslog() with
a string priority and a list of printf() arguments just like at syslog(3).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-UI
Summary:        Term::ReadLine UI made easy
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        0.30
Requires:       %perl_compat
Requires:       perl(Log::Message::Simple)
BuildArch:      noarch

%description Term-UI
Term::UI is a transparent way of eliminating the overhead of having to format
a question and then validate the reply, informing the user if the answer was not
proper and re-issuing the question.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Harness
Summary:        Run Perl standard test scripts with statistics
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        3.23
Requires:       %perl_compat
BuildArch:      noarch

%description Test-Harness
Run Perl standard test scripts with statistics.
Use TAP::Parser, Test::Harness package was whole rewritten.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Simple
Summary:        Basic utilities for writing tests
Group:          Development/Languages
License:        GPL+ or Artistic
Epoch:          0
Version:        0.98
Requires:       %perl_compat
Requires:       perl(Data::Dumper)
BuildArch:      noarch

%description Test-Simple
Basic utilities for writing tests.

%package Test-Simple-tests
Summary:        Test suite for package perl-Test-Simple
Group:          Development/Debug
License:        GPL+ or Artistic
Epoch:          0
Version:        0.98
Requires:       perl-Test-Simple = %{epoch}:%{version}-%{release}
Requires:       /usr/bin/prove
AutoReqProv:    0
BuildArch:      noarch

%description Test-Simple-tests
This package provides the test suite for package perl-Test-Simple.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-ParseWords
Summary:        Parse text into an array of tokens or array of arrays
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        3.27
Requires:       %perl_compat
Requires:       perl(Carp)
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-256

%description Text-ParseWords
Parse text into an array of tokens or array of arrays.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Soundex
Summary:        Implementation of the soundex algorithm
Group:          Development/Libraries
License:        Copyright only
Epoch:          0
# perl's 3.03_1 copy is identical to CPAN 3.03
Version:        3.03
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(Text::Unidecode)
Conflicts:      perl < 4:5.16.2-250

%description Text-Soundex
Soundex is a phonetic algorithm for indexing names by sound, as pronounced in
English. This module implements the original soundex algorithm developed by
Robert Russell and Margaret Odell, as well as a variation called "American
Soundex".
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Thread-Queue
Summary:        Thread-safe queues
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.12
Requires:       %perl_compat
Requires:       perl(Carp)
BuildArch:      noarch
Conflicts:      perl < 4:5.16.2-257

%description Thread-Queue
This module provides thread-safe FIFO queues that can be accessed safely by
any number of threads.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-HiRes
Summary:        High resolution alarm, sleep, gettimeofday, interval timers
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.9725
Requires:       %perl_compat
Requires:       perl(Carp)
Conflicts:      perl < 4:5.16.3-271

%description Time-HiRes
The Time::HiRes module implements a Perl interface to the usleep, nanosleep,
ualarm, gettimeofday, and setitimer/getitimer system calls, in other words,
high resolution time and timers.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-Local
Summary:        Efficiently compute time from local and GMT time
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.2000
Requires:       %perl_compat
BuildArch:      noarch
Conflicts:      perl < 4:5.16.3-262

%description Time-Local
This module provides functions that are the inverse of built-in perl functions
localtime() and gmtime(). They accept a date as a six-element array, and
return the corresponding time(2) value in seconds since the system epoch
(Midnight, January 1, 1970 GMT on Unix, for example). This value can be
positive or negative, though POSIX only requires support for positive values,
so dates before the system's epoch may not work on all operating systems.
%endif

%package Time-Piece
Summary:        Time objects from localtime and gmtime
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
# real 1.20_01
Version:        1.20.1
Requires:       %perl_compat

%description Time-Piece
The Time::Piece module replaces the standard localtime and gmtime functions
with implementations that return objects.  It does so in a backwards compatible
manner, so that using localtime or gmtime as documented in perlfunc still
behave as expected.

%if %{dual_life} || %{rebuild_from_scratch}
%package parent
Summary:        Establish an ISA relationship with base classes at compile time
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.225
Requires:       %perl_compat
BuildArch:      noarch

%description parent
parent allows you to both load one or more modules, while setting up
inheritance from those modules at the same time. Mostly similar in effect to:

    package Baz;

    BEGIN {
        require Foo;
        require Bar; 
        
        push @ISA, qw(Foo Bar); 
    }
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Socket
Summary:        C socket.h defines and structure manipulators
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        2.001
Requires:       %perl_compat

%description Socket
This module is just a translation of the C socket.h file.  Unlike the old
mechanism of requiring a translated socket.ph file, this uses the h2xs program
(see the Perl source distribution) and your native C compiler.  This means
that it has a far more likely chance of getting the numbers right.  This
includes all of the commonly used pound-defines like AF_INET, SOCK_STREAM, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package threads
Summary:        Perl interpreter-based threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.86
Requires:       perl = %{perl_epoch}:%{perl_version}

%description threads
Since Perl 5.8, thread programming has been available using a model called
interpreter threads  which provides a new Perl interpreter for each thread,
and, by default, results in no data or state information being shared between
threads.

(Prior to Perl 5.8, 5005threads was available through the Thread.pm API. This
threading model has been deprecated, and was removed as of Perl 5.10.0.)

As just mentioned, all variables are, by default, thread local. To use shared
variables, you need to also load threads::shared.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package threads-shared
Summary:        Perl extension for sharing data structures between threads
Group:          Development/Libraries
License:        GPL+ or Artistic
Epoch:          0
Version:        1.40
Requires:       %perl_compat

%description threads-shared
By default, variables are private to each thread, and each newly created thread
gets a private copy of each existing variable. This module allows you to share
variables across different threads (and pseudo-forks on Win32). It is used
together with the threads module.  This module supports the sharing of the
following data types only: scalars and scalar refs, arrays and array refs, and
hashes and hash refs.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package version
Summary:        Perl extension for Version Objects
Group:          Development/Libraries
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          3
Version:        0.99
Requires:       %perl_compat
BuildArch:      noarch

%description version
Perl extension for Version Objects
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Version-Requirements
Summary:        Set of version requirements for a CPAN dist
License:        GPL+ or Artistic
Group:          Development/Libraries
Version:        0.101022
Epoch:          0
Requires:       %perl_compat
BuildArch:      noarch

%description Version-Requirements
A Version::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions.
It can be built up by adding more and more constraints, and it will reduce
them to the simplest representation.
%endif

%package core
Summary:        Base perl metapackage
Group:          Development/Languages
# This rpm doesn't contain any copyrightable material.
# Nevertheless, it needs a License tag, so we'll use the generic
# "perl" license.
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
Requires:       %perl_compat
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-devel = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-macros

Requires:       perl-Archive-Extract, perl-Archive-Tar, perl-autodie
Requires:       perl-B-Lint, perl-Compress-Raw-Bzip2,
Requires:       perl-Carp, perl-Compress-Raw-Zlib, perl-CGI, perl-constant,
Requires:       perl-CPAN, perl-CPAN-Meta, perl-CPAN-Meta-Requirements,
Requires:       perl-CPAN-Meta-YAML, perl-CPANPLUS,
Requires:       perl-CPANPLUS-Dist-Build, perl-Encode
Requires:       perl-Data-Dumper, perl-DB_File, perl-Digest, perl-Digest-MD5,
Requires:       perl-Digest-SHA, perl-Env, perl-Exporter
Requires:       perl-ExtUtils-CBuilder, perl-ExtUtils-Embed,
Requires:       perl-ExtUtils-Install, perl-ExtUtils-MakeMaker
Requires:       perl-ExtUtils-Manifest
Requires:       perl-ExtUtils-ParseXS, perl-File-CheckTree, perl-File-Fetch
Requires:       perl-File-Path, perl-File-Temp, perl-Filter, perl-Getopt-Long
Requires:       perl-HTTP-Tiny
Requires:       perl-IO-Compress, perl-IO-Zlib, perl-IPC-Cmd, perl-JSON-PP
Requires:       perl-Locale-Codes, perl-Locale-Maketext,
Requires:       perl-Locale-Maketext-Simple
Requires:       perl-Log-Message, perl-Log-Message-Simple, perl-Module-Build
Requires:       perl-Module-CoreList, perl-Module-Load
Requires:       perl-Module-Load-Conditional, perl-Module-Loaded, perl-Module-Metadata
Requires:       perl-Module-Pluggable, perl-Object-Accessor, perl-Package-Constants, perl-PathTools
Requires:       perl-Params-Check, perl-Parse-CPAN-Meta, perl-Perl-OSType
Requires:       perl-Pod-Checker, perl-Pod-Escapes, perl-Pod-LaTeX
Requires:       perl-Pod-Parser, perl-Pod-Perldoc, perl-Pod-Usage
Requires:       perl-podlators, perl-Pod-Simple, perl-Scalar-List-Utils
Requires:       perl-Socket, perl-Storable, perl-Sys-Syslog,
Requires:       perl-Term-UI, perl-Test-Harness,
Requires:       perl-Test-Simple
Requires:       perl-Text-ParseWords, perl-Text-Soundex, perl-Thread-Queue
Requires:       perl-Time-HiRes
Requires:       perl-Time-Local, perl-Time-Piece, perl-Version-Requirements,
Requires:       perl-version, perl-threads, perl-threads-shared, perl-parent

%description core
A metapackage which requires all of the perl bits and modules in the upstream
tarball from perl.org.

%prep
%setup -q -n perl-%{perl_version}
%patch0 -p1
%patch1 -p1
%ifarch %{multilib_64_archs}
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
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

# Amazon Patches
%patch100 -p1

%if !%{defined perl_bootstrap}
# Local patch tracking
perl -x patchlevel.h \
    'Fedora Patch1: Removes date check, Fedora/RHEL specific' \
%ifarch %{multilib_64_archs} \
    'Fedora Patch3: support for libdir64' \
%endif \
    'Fedora Patch4: use libresolv instead of libbind' \
    'Fedora Patch5: USE_MM_LD_RUN_PATH' \
    'Fedora Patch6: Skip hostname tests, due to builders not being network capable' \
    'Fedora Patch7: Dont run one io test due to random builder failures' \
    'Fedora Patch9: Fix find2perl to translate ? glob properly (RT#113054)' \
    'Fedora Patch10: Fix broken atof (RT#109318)' \
    'Fedora Patch13: Clear $@ before "do" I/O error (RT#113730)' \
    'Fedora Patch14: Do not truncate syscall() return value to 32 bits (RT#113980)' \
    'Fedora Patch15: Override the Pod::Simple::parse_file (CPANRT#77530)' \
    'Fedora Patch16: Do not leak with attribute on my variable (RT#114764)' \
    'Fedora Patch17: Allow operator after numeric keyword argument (RT#105924)' \
    'Fedora Patch18: Extend stack in File::Glob::glob, (RT#114984)' \
    'Fedora Patch19: Do not crash when vivifying $|' \
    'Fedora Patch20: Fix misparsing of maketext strings (CVE-2012-6329)' \
    'Fedora Patch21: Add NAME headings to CPAN modules (CPANRT#73396)' \
    'Fedora Patch22: Fix leaking tied hashes (RT#107000) [1]' \
    'Fedora Patch23: Fix leaking tied hashes (RT#107000) [2]' \
    'Fedora Patch24: Fix leaking tied hashes (RT#107000) [3]' \
    'Fedora Patch25: Fix dead lock in PerlIO after fork from thread (RT#106212)' \
    'Fedora Patch26: Make regexp safe in a signal handler (RT#114878)' \
    'Fedora Patch27: Update h2ph(1) documentation (RT#117647)' \
    'Fedora Patch28: Update pod2html(1) documentation (RT#117623)' \
    'Fedora Patch29: Document Math::BigInt::CalcEmu requires Math::BigInt (CPAN RT#85015)' \
    'RHEL Patch30: Use stronger algorithm needed for FIPS in t/op/crypt.t (RT#121591)' \
    'RHEL Patch31: Make *DBM_File desctructors thread-safe (RT#61912)' \
    'RHEL Patch32: Use stronger algorithm needed for FIPS in t/op/taint.t (RT#123338)' \
    'RHEL Patch33: Remove CPU-speed-sensitive test in Benchmark test' \
    'RHEL Patch34: Make File::Glob work with threads again' \
    'RHEL Patch35: Fix CRLF conversion in ASCII FTP upload (CPAN RT#41642)' \
    'RHEL Patch36: Do not leak the temp utf8 copy of namepv (CPAN RT#123786)' \
    'RHEL Patch37: Fix duplicating PerlIO::encoding when spawning threads (RT#31923)' \
    'RHEL Patch38: Add SSL support to Net::SMTP (CPAN RT#93823) [1]' \
    'RHEL Patch39: Add SSL support to Net::SMTP (CPAN RT#93823) [2]' \
    'RHEL Patch40: Add SSL support to Net::SMTP (CPAN RT#93823) [3]' \
    'RHEL Patch41: Add SSL support to Net::SMTP (CPAN RT#93823) [4]' \
    'RHEL Patch42: Do not overload ".." in Math::BigInt (CPAN RT#80182)' \
    'RHEL Patch43: Fix CVE-2018-18311 Integer overflow leading to buffer overflow' \
    %{nil}
%endif

#copy the example script
cp -a %{SOURCE5} .

#
# Candidates for doc recoding (need case by case review):
# find . -name "*.pod" -o -name "README*" -o -name "*.pm" | xargs file -i | grep charset= | grep -v '\(us-ascii\|utf-8\)'
recode()
{
        iconv -f "${2:-iso-8859-1}" -t utf-8 < "$1" > "${1}_"
        touch -r "$1" "${1}_"
        mv -f "${1}_" "$1"
}
recode README.cn euc-cn
recode README.jp euc-jp
recode README.ko euc-kr
# TODO iconv fail on this one
##recode README.tw big5
recode pod/perlebcdic.pod
recode pod/perlhack.pod
recode pod/perlhist.pod
recode pod/perlthrtut.pod
recode AUTHORS

find . -name \*.orig -exec rm -fv {} \;

# Configure Compress::Zlib to use system zlib
sed -i 's|BUILD_ZLIB      = True|BUILD_ZLIB      = False|
    s|INCLUDE         = ./zlib-src|INCLUDE         = %{_includedir}|
    s|LIB             = ./zlib-src|LIB             = %{_libdir}|' \
    cpan/Compress-Raw-Zlib/config.in

# Ensure that we never accidentally bundle zlib or bzip2
rm -rf cpan/Compress-Raw-Zlib/zlib-src
rm -rf cpan/Compress-Raw-Bzip2/bzip2-src
sed -i '/\(bzip2\|zlib\)-src/d' MANIFEST

%if !%{with gdbm}
# Do not install anything requiring NDBM_File if NDBM is not available.
rm -rf 'cpan/Memoize/Memoize/NDBM_File.pm'
sed -i '\|cpan/Memoize/Memoize/NDBM_File.pm|d' MANIFEST
%endif

%build
echo "RPM Build arch: %{_arch}"

# use "lib", not %%{_lib}, for privlib, sitelib, and vendorlib
# To build production version, we would need -DDEBUGGING=-g

# Perl INC path (perl -V) in search order:
# - /usr/local/share/perl5            -- for CPAN     (site lib)
# - /usr/local/lib[64]/perl5          -- for CPAN     (site arch)
# - /usr/share/perl5/vendor_perl      -- 3rd party    (vendor lib)
# - /usr/lib[64]/perl5/vendor_perl    -- 3rd party    (vendor arch)
# - /usr/share/perl5                  -- Fedora       (priv lib)
# - /usr/lib[64]/perl5                -- Fedora       (arch lib)

%global privlib     %{_prefix}/share/perl5
%global archlib     %{_libdir}/perl5

%global perl_vendorlib  %{privlib}/vendor_perl
%global perl_vendorarch %{archlib}/vendor_perl

# For perl-5.14.2-large-repeat-heap-abuse.patch 
perl regen.pl -v

/bin/sh Configure -des -Doptimize="$RPM_OPT_FLAGS" \
        -Dccdlflags="-Wl,--enable-new-dtags" \
        -Dlddlflags="-shared $RPM_OPT_FLAGS $RPM_LD_FLAGS" \
        -DDEBUGGING=-g \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=root@localhost \
        -Dcc='%{__cc}' \
        -Dcf_by='Red Hat, Inc.' \
        -Dprefix=%{_prefix} \
        -Dvendorprefix=%{_prefix} \
        -Dsiteprefix=%{_prefix}/local \
        -Dsitelib="%{_prefix}/local/share/perl5" \
        -Dsitearch="%{_prefix}/local/%{_lib}/perl5" \
        -Dprivlib="%{privlib}" \
        -Dvendorlib="%{perl_vendorlib}" \
        -Darchlib="%{archlib}" \
        -Dvendorarch="%{perl_vendorarch}" \
        -Darchname=%{perl_archname} \
%ifarch %{multilib_64_archs}
        -Dlibpth="/usr/local/lib64 /lib64 %{_prefix}/lib64" \
%endif
%ifarch sparc sparcv9
        -Ud_longdbl \
%endif
        -Duseshrplib \
        -Dusethreads \
        -Duseithreads \
        -Dusedtrace='/usr/bin/dtrace' \
        -Duselargefiles \
        -Dd_semctl_semun \
        -Di_db \
%if %{with gdbm}
        -Ui_ndbm \
        -Di_gdbm \
%endif
        -Di_shadow \
        -Di_syslog \
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dpager='/usr/bin/less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{_bindir}' \
        -Dusesitecustomize

# -Duseshrplib creates libperl.so, -Ubincompat5005 help create DSO -> libperl.so

BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

%ifarch sparc64 %{arm}
make
%else
make %{?_smp_mflags}
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT

%global build_archlib $RPM_BUILD_ROOT%{archlib}
%global build_privlib $RPM_BUILD_ROOT%{privlib}
%global build_bindir  $RPM_BUILD_ROOT%{_bindir}
%global new_perl LD_PRELOAD="%{build_archlib}/CORE/libperl.so" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib}:%{build_privlib}" \\\
    %{build_bindir}/perl

install -p -m 755 utils/pl2pm %{build_bindir}/pl2pm

for i in asm/termios.h syscall.h syslimits.h syslog.h \
    sys/ioctl.h sys/socket.h sys/time.h wait.h
do
    %{new_perl} %{build_bindir}/h2ph -a -d %{build_archlib} $i || true
done

# vendor directories (in this case for third party rpms)
# perl doesn't create the auto subdirectory, but modules put things in it,
# so we need to own it.

mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}

#
# libnet configuration file
#
install -p -m 644 %{SOURCE2} %{build_privlib}/Net/libnet.cfg

#
# perl RPM macros
#
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm
install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/

#
# Core modules removal
#
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty | xargs rm -f 

chmod -R u+w $RPM_BUILD_ROOT/*

# miniperl? As an interpreter? How odd. Anyway, a symlink does it:
rm %{build_privlib}/ExtUtils/xsubpp
ln -s ../../../bin/xsubpp %{build_privlib}/ExtUtils/

# Don't need the .packlist
rm %{build_archlib}/.packlist

# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
# We cannot remove it in %%prep because dist/Cwd/t/Spec.t test needs it.
rm %{build_archlib}/File/Spec/VMS.pm
rm $RPM_BUILD_ROOT%{_mandir}/man3/File::Spec::VMS.3*

# Fix some manpages to be UTF-8
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
pushd $RPM_BUILD_ROOT%{_mandir}/man1/
  for i in perl588delta.1 perldelta.1 ; do
    iconv -f MS-ANSI -t UTF-8 $i --output new-$i
    rm $i
    mv new-$i $i
  done
popd

# for now, remove Bzip2:
# Why? Now is missing Bzip2 files and provides
##find $RPM_BUILD_ROOT -name Bzip2 | xargs rm -r
##find $RPM_BUILD_ROOT -name '*B*zip2*'| xargs rm

# tests -- FIXME need to validate that this all works as expected
mkdir -p %{buildroot}%{perl5_testdir}/perl-tests

# "core"
tar -cf - t/ | ( cd %{buildroot}%{perl5_testdir}/perl-tests && tar -xf - )

# "dual-lifed"
for dir in `find ext/ -type d -name t -maxdepth 2` ; do

    tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir}/perl-tests/t && tar -xf - )
done

# Selected "Dual-lifed cpan" packages
pushd cpan
for package in Test-Simple; do
    for dir in `find ${package} -type d -name t -maxdepth 2` ; do
        tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir} && tar -xf - )
    done
done
popd

# Systemtap tapset install
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{multilib_64_archs}
%global libperl_stp libperl%{perl_version}-64.stp
%else
%global libperl_stp libperl%{perl_version}-32.stp
%endif

sed \
  -e "s|LIBRARY_PATH|%{archlib}/CORE/libperl.so|" \
  %{SOURCE4} \
  > %{buildroot}%{tapsetdir}/%{libperl_stp}

# TODO: Canonicalize test files (rewrite intrerpreter path, fix permissions)
# XXX: We cannot rewrite ./perl before %%check phase. Otherwise the test
# would run against system perl at build-time.
# See __spec_check_pre global macro in macros.perl.
#T_FILES=`find %%{buildroot}%%{perl5_testdir} -type f -name '*.t'`
#%%fix_shbang_line $T_FILES
#%%{__chmod} +x $T_FILES
#%%{_fixperms} %%{buildroot}%%{perl5_testdir}
#
# lib/perl5db.t will fail if Term::ReadLine::Gnu is available
%check
%if %{with test}
%if %{parallel_tests}
    JOBS=$(printf '%%s' "%{?_smp_mflags}" | sed 's/.*-j\([0-9][0-9]*\).*/\1/')
    LC_ALL=C TEST_JOBS=$JOBS make test_harness
%else
    LC_ALL=C make test
%endif
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc Artistic AUTHORS Copying README Changes
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_bindir}/*
%{privlib}
%{archlib}/*
%{perl_vendorlib}


# libs
%exclude %{archlib}/CORE/libperl.so
%exclude %{perl_vendorarch}

# devel
%exclude %{_bindir}/h2xs
%exclude %{_mandir}/man1/h2xs*
%exclude %{_bindir}/libnetcfg
%exclude %{_mandir}/man1/libnetcfg*
%exclude %{_bindir}/perlivp
%exclude %{_mandir}/man1/perlivp*
%exclude %{archlib}/CORE/*.h
%exclude %{_mandir}/man1/perlxs*

# Archive-Extract
%exclude %{privlib}/Archive/Extract.pm
%exclude %{_mandir}/man3/Archive::Extract.3*

# Archive-Tar
%exclude %{_bindir}/ptar
%exclude %{_bindir}/ptardiff
%exclude %{_bindir}/ptargrep
%exclude %{privlib}/Archive/Tar/
%exclude %{privlib}/Archive/Tar.pm
%exclude %{_mandir}/man1/ptar.1*
%exclude %{_mandir}/man1/ptardiff.1*
%exclude %{_mandir}/man1/ptargrep.1*
%exclude %{_mandir}/man3/Archive::Tar*

# autodie
%exclude %{privlib}/autodie/
%exclude %{privlib}/autodie.pm
%exclude %{privlib}/Fatal.pm
%exclude %{_mandir}/man3/autodie.3*
%exclude %{_mandir}/man3/autodie::*
%exclude %{_mandir}/man3/Fatal.3*

# B-Lint
%exclude %{privlib}/B/Lint*
%exclude %{_mandir}/man3/B::Lint*

# Carp
%exclude %{privlib}/Carp
%exclude %{privlib}/Carp.*
%exclude %{_mandir}/man3/Carp.*

# CGI
%exclude %{privlib}/CGI/
%exclude %{privlib}/CGI.pm
%exclude %{_mandir}/man3/CGI.3*
%exclude %{_mandir}/man3/CGI::*.3*

# constant
%exclude %{privlib}/constant.pm
%exclude %{_mandir}/man3/constant.3*

# CPAN
%exclude %{_bindir}/cpan
%exclude %{privlib}/App/Cpan.pm
%exclude %{privlib}/CPAN/
%exclude %{privlib}/CPAN.pm
%exclude %{_mandir}/man1/cpan.1*
%exclude %{_mandir}/man3/App::Cpan.*
%exclude %{_mandir}/man3/CPAN.*
%exclude %{_mandir}/man3/CPAN:*

# CPAN-Meta
%exclude %{privlib}/CPAN/Meta.pm
%exclude %{privlib}/CPAN/Meta/Converter.pm
%exclude %{privlib}/CPAN/Meta/Feature.pm
%exclude %{privlib}/CPAN/Meta/History.pm
%exclude %{privlib}/CPAN/Meta/Prereqs.pm
%exclude %{privlib}/CPAN/Meta/Spec.pm
%exclude %{privlib}/CPAN/Meta/Validator.pm
%exclude %{_mandir}/man3/CPAN::Meta*

# CPAN-Meta-Requirements
%exclude %{privlib}/CPAN/Meta/Requirements.pm
%exclude %{_mandir}/man3/CPAN::Meta::Requirements.3*

# CPAN-Meta-YAML
%exclude %{privlib}/CPAN/Meta/YAML.pm
%exclude %{_mandir}/man3/CPAN::Meta::YAML*

# Parse-CPAN-Meta
%exclude %dir %{privlib}/Parse/
%exclude %dir %{privlib}/Parse/CPAN/
%exclude %{privlib}/Parse/CPAN/Meta.pm
%exclude %{_mandir}/man3/Parse::CPAN::Meta.3*

# CPANPLUS
# CPANPLUS-Dist-Build
%exclude %{_bindir}/cpan2dist
%exclude %{_bindir}/cpanp
%exclude %{_bindir}/cpanp-run-perl
%exclude %{privlib}/CPANPLUS/
%exclude %{privlib}/CPANPLUS.pm
%exclude %{_mandir}/man1/cpan2dist.1*
%exclude %{_mandir}/man1/cpanp.1*
%exclude %{_mandir}/man3/CPANPLUS*

# Compress-Raw-Bzip2
%exclude %dir %{archlib}/Compress
%exclude %{archlib}/Compress/Raw/Bzip2.pm
%exclude %{_mandir}/man3/Compress::Raw::Bzip2*

# Compress-Raw-Zlib
%exclude %{archlib}/Compress/Raw/
%exclude %{archlib}/auto/Compress
%exclude %{archlib}/auto/Compress/Raw/
%exclude %{archlib}/auto/Compress/Raw/Zlib/
%exclude %{_mandir}/man3/Compress::Raw::Zlib*

# Data-Dumper
%exclude %dir %{archlib}/auto/Data
%exclude %dir %{archlib}/auto/Data/Dumper
%exclude %{archlib}/auto/Data/Dumper/Dumper.so
%exclude %dir %{archlib}/Data
%exclude %{archlib}/Data/Dumper.pm
%exclude %{_mandir}/man3/Data::Dumper.3*

# DB_File
%exclude %{archlib}/DB_File.pm
%exclude %dir %{archlib}/auto/DB_File
%exclude %{archlib}/auto/DB_File/DB_File.so
%exclude %{_mandir}/man3/DB_File*

# Digest
%exclude %{privlib}/Digest.pm
%exclude %dir %{privlib}/Digest
%exclude %{privlib}/Digest/base.pm
%exclude %{privlib}/Digest/file.pm
%exclude %{_mandir}/man3/Digest.3*
%exclude %{_mandir}/man3/Digest::base.3*
%exclude %{_mandir}/man3/Digest::file.3*

# Digest-MD5
%exclude %{archlib}/Digest/MD5.pm
%exclude %{archlib}/auto/Digest/MD5/
%exclude %{_mandir}/man3/Digest::MD5.3*

# Digest-SHA
%exclude %{_bindir}/shasum
%exclude %{archlib}/Digest/SHA.pm
%exclude %{archlib}/auto/Digest/SHA/
%exclude %{_mandir}/man1/shasum.1*
%exclude %{_mandir}/man3/Digest::SHA.3*

# Encode
%exclude %{_bindir}/piconv
%exclude %{archlib}/encoding.pm
%exclude %{archlib}/Encode*
%exclude %{archlib}/auto/Encode*
%exclude %{_mandir}/man1/piconv.1*
%exclude %{_mandir}/man3/encoding.3*
%exclude %{_mandir}/man3/Encode*.3*

# Encode-devel
%exclude %{_bindir}/enc2xs
%exclude %{privlib}/Encode/*.e2x
%exclude %{privlib}/Encode/encode.h
%exclude %{_mandir}/man1/enc2xs.1*

# Env
%exclude %{privlib}/Env.pm
%exclude %{_mandir}/man3/Env.3*

# Exporter
%exclude %{privlib}/Exporter*
%exclude %{_mandir}/man3/Exporter*

# ExtUtils-CBuilder
%exclude %{privlib}/ExtUtils/CBuilder/
%exclude %{privlib}/ExtUtils/CBuilder.pm
%exclude %{_mandir}/man3/ExtUtils::CBuilder*

# ExtUtils-Embed
%exclude %{privlib}/ExtUtils/Embed.pm
%exclude %{_mandir}/man3/ExtUtils::Embed*

# ExtUtils-Install
%exclude %{privlib}/ExtUtils/Install.pm
%exclude %{privlib}/ExtUtils/Installed.pm
%exclude %{privlib}/ExtUtils/Packlist.pm
%exclude %{_mandir}/man3/ExtUtils::Install.3*
%exclude %{_mandir}/man3/ExtUtils::Installed.3*
%exclude %{_mandir}/man3/ExtUtils::Packlist.3*

# ExtUtils-Manifest
%exclude %{privlib}/ExtUtils/Manifest.pm
%exclude %{privlib}/ExtUtils/MANIFEST.SKIP
%exclude %{_mandir}/man3/ExtUtils::Manifest.3*

# ExtUtils-MakeMaker
%exclude %{_bindir}/instmodsh
%exclude %{privlib}/ExtUtils/Command/
%exclude %{privlib}/ExtUtils/Liblist/
%exclude %{privlib}/ExtUtils/Liblist.pm
%exclude %{privlib}/ExtUtils/MakeMaker/
%exclude %{privlib}/ExtUtils/MakeMaker.pm
%exclude %{privlib}/ExtUtils/MM*.pm
%exclude %{privlib}/ExtUtils/MY.pm
%exclude %{privlib}/ExtUtils/Mkbootstrap.pm
%exclude %{privlib}/ExtUtils/Mksymlists.pm
%exclude %{privlib}/ExtUtils/testlib.pm
%exclude %{_mandir}/man1/instmodsh.1*
%exclude %{_mandir}/man3/ExtUtils::Command::MM*
%exclude %{_mandir}/man3/ExtUtils::Liblist.3*
%exclude %{_mandir}/man3/ExtUtils::MM*
%exclude %{_mandir}/man3/ExtUtils::MY.3*
%exclude %{_mandir}/man3/ExtUtils::MakeMaker*
%exclude %{_mandir}/man3/ExtUtils::Mkbootstrap.3*
%exclude %{_mandir}/man3/ExtUtils::Mksymlists.3*
%exclude %{_mandir}/man3/ExtUtils::testlib.3*

# ExtUtils-ParseXS
%exclude %dir %{privlib}/ExtUtils/ParseXS/
%exclude %dir %{privlib}/ExtUtils/Typemaps/
%exclude %{privlib}/ExtUtils/ParseXS.pm
%exclude %{privlib}/ExtUtils/ParseXS.pod
%exclude %{privlib}/ExtUtils/ParseXS/Constants.pm
%exclude %{privlib}/ExtUtils/ParseXS/CountLines.pm
%exclude %{privlib}/ExtUtils/ParseXS/Utilities.pm
%exclude %{privlib}/ExtUtils/Typemaps.pm
%exclude %{privlib}/ExtUtils/Typemaps/Cmd.pm
%exclude %{privlib}/ExtUtils/Typemaps/InputMap.pm
%exclude %{privlib}/ExtUtils/Typemaps/OutputMap.pm
%exclude %{privlib}/ExtUtils/Typemaps/Type.pm
%exclude %{privlib}/ExtUtils/xsubpp
%exclude %{_bindir}/xsubpp
%exclude %{_mandir}/man1/xsubpp*
%exclude %{_mandir}/man3/ExtUtils::ParseXS.3*
%exclude %{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
%exclude %{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
%exclude %{_mandir}/man3/ExtUtils::Typemaps::Type.3*

# File-CheckTree
%exclude %{privlib}/File/CheckTree.pm
%exclude %{_mandir}/man3/File::CheckTree.3*

# File-Fetch
%exclude %{privlib}/File/Fetch.pm
%exclude %{_mandir}/man3/File::Fetch.3*

# File-Path
%exclude %{privlib}/File/Path.pm
%exclude %{_mandir}/man3/File::Path.3*

# File-Temp
%exclude %{privlib}/File/Temp.pm
%exclude %{_mandir}/man3/File::Temp.3*

# Filter
%exclude %{archlib}/auto/Filter/Util
%exclude %{archlib}/Filter/Util
%exclude %{privlib}/pod/perlfilter.pod
%exclude %{_mandir}/man1/perlfilter.*
%exclude %{_mandir}/man3/Filter::Util::*

# Getopt-Long
%exclude %{privlib}/Getopt/Long.pm
%exclude %{_mandir}/man3/Getopt::Long.3*

# IO-Compress
%exclude %{_bindir}/zipdetails
%exclude %{privlib}/IO/Compress/FAQ.pod
%exclude %{_mandir}/man1/zipdetails.*
%exclude %{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
%exclude %{privlib}/Compress/Zlib.pm
%exclude %{_mandir}/man3/Compress::Zlib*
# IO-Compress-Base
%exclude %{privlib}/File/GlobMapper.pm
%exclude %{privlib}/IO/Compress/Base/
%exclude %{privlib}/IO/Compress/Base.pm
%exclude %{privlib}/IO/Uncompress/AnyUncompress.pm
%exclude %{privlib}/IO/Uncompress/Base.pm
%exclude %{_mandir}/man3/File::GlobMapper.*
%exclude %{_mandir}/man3/IO::Compress::Base.*
%exclude %{_mandir}/man3/IO::Uncompress::AnyUncompress.*
%exclude %{_mandir}/man3/IO::Uncompress::Base.*
# IO-Compress-Zlib
%exclude %{privlib}/IO/Compress/Adapter/
%exclude %{privlib}/IO/Compress/Deflate.pm
%exclude %{privlib}/IO/Compress/Gzip/
%exclude %{privlib}/IO/Compress/Gzip.pm
%exclude %{privlib}/IO/Compress/RawDeflate.pm
%exclude %{privlib}/IO/Compress/Bzip2.pm
%exclude %{privlib}/IO/Compress/Zip/
%exclude %{privlib}/IO/Compress/Zip.pm
%exclude %{privlib}/IO/Compress/Zlib/
%exclude %{privlib}/IO/Uncompress/Adapter/
%exclude %{privlib}/IO/Uncompress/AnyInflate.pm
%exclude %{privlib}/IO/Uncompress/Bunzip2.pm
%exclude %{privlib}/IO/Uncompress/Gunzip.pm
%exclude %{privlib}/IO/Uncompress/Inflate.pm
%exclude %{privlib}/IO/Uncompress/RawInflate.pm
%exclude %{privlib}/IO/Uncompress/Unzip.pm
%exclude %{_mandir}/man3/IO::Compress::Deflate*
%exclude %{_mandir}/man3/IO::Compress::Bzip2*
%exclude %{_mandir}/man3/IO::Compress::Gzip*
%exclude %{_mandir}/man3/IO::Compress::RawDeflate*
%exclude %{_mandir}/man3/IO::Compress::Zip*
%exclude %{_mandir}/man3/IO::Uncompress::AnyInflate*
%exclude %{_mandir}/man3/IO::Uncompress::Bunzip2*
%exclude %{_mandir}/man3/IO::Uncompress::Gunzip*
%exclude %{_mandir}/man3/IO::Uncompress::Inflate*
%exclude %{_mandir}/man3/IO::Uncompress::RawInflate*
%exclude %{_mandir}/man3/IO::Uncompress::Unzip*

# IO-Zlib
%exclude %{privlib}/IO/Zlib.pm
%exclude %{_mandir}/man3/IO::Zlib.*

# HTTP-Tiny
%exclude %{privlib}/HTTP/Tiny.pm
%exclude %{_mandir}/man3/HTTP::Tiny*

# IPC-Cmd
%exclude %{privlib}/IPC/Cmd.pm
%exclude %{_mandir}/man3/IPC::Cmd.3*

# JSON-PP
%exclude %{_bindir}/json_pp
%exclude %{privlib}/JSON/PP
%exclude %{privlib}/JSON/PP.pm
%exclude %{_mandir}/man1/json_pp.1*
%exclude %{_mandir}/man3/JSON::PP.3*
%exclude %{_mandir}/man3/JSON::PP::Boolean.3pm*

# Locale-Codes
%exclude %{privlib}/Locale/Codes
%exclude %{privlib}/Locale/Codes.*
%exclude %{privlib}/Locale/Country.*
%exclude %{privlib}/Locale/Currency.*
%exclude %{privlib}/Locale/Language.*
%exclude %{privlib}/Locale/Script.*
%exclude %{_mandir}/man3/Locale::Codes::*
%exclude %{_mandir}/man3/Locale::Codes.*
%exclude %{_mandir}/man3/Locale::Country.*
%exclude %{_mandir}/man3/Locale::Currency.*
%exclude %{_mandir}/man3/Locale::Language.*
%exclude %{_mandir}/man3/Locale::Script.*

# Locale-Maketext
%exclude %dir %{privlib}/Locale/Maketext
%exclude %{privlib}/Locale/Maketext.*
%exclude %{privlib}/Locale/Maketext/Cookbook.*
%exclude %{privlib}/Locale/Maketext/Guts.*
%exclude %{privlib}/Locale/Maketext/GutsLoader.*
%exclude %{privlib}/Locale/Maketext/TPJ13.*
%exclude %{_mandir}/man3/Locale::Maketext.*
%exclude %{_mandir}/man3/Locale::Maketext::Cookbook.*
%exclude %{_mandir}/man3/Locale::Maketext::Guts.*
%exclude %{_mandir}/man3/Locale::Maketext::GutsLoader.*
%exclude %{_mandir}/man3/Locale::Maketext::TPJ13.*

# Locale-Maketext-Simple
%exclude %{privlib}/Locale/Maketext/Simple.pm
%exclude %{_mandir}/man3/Locale::Maketext::Simple.*

# Log-Message
%exclude %{privlib}/Log/Message.pm
%exclude %{privlib}/Log/Message/Config.pm
%exclude %{privlib}/Log/Message/Handlers.pm
%exclude %{privlib}/Log/Message/Item.pm
%exclude %{_mandir}/man3/Log::Message.3*
%exclude %{_mandir}/man3/Log::Message::Config.3*
%exclude %{_mandir}/man3/Log::Message::Handlers.3*
%exclude %{_mandir}/man3/Log::Message::Item.3*

# Log-Message-Simple
%exclude %{privlib}/Log/Message/Simple.pm
%exclude %{_mandir}/man3/Log::Message::Simple.3*

# Module-Build
%exclude %{_bindir}/config_data
%exclude %{privlib}/inc/
%exclude %{privlib}/Module/Build/
%exclude %{privlib}/Module/Build.pm
%exclude %{_mandir}/man1/config_data.1*
%exclude %{_mandir}/man3/Module::Build*
%exclude %{_mandir}/man3/inc::latest.3*

# Module-CoreList
%exclude %{_bindir}/corelist
%exclude %{privlib}/Module/CoreList.pm
%exclude %{_mandir}/man1/corelist*
%exclude %{_mandir}/man3/Module::CoreList*

# Module-Load
%exclude %{privlib}/Module/Load.pm
%exclude %{_mandir}/man3/Module::Load.*

# Module-Load-Conditional
%exclude %{privlib}/Module/Load/
%exclude %{_mandir}/man3/Module::Load::Conditional*

# Module-Loaded
%exclude %{privlib}/Module/Loaded.pm
%exclude %{_mandir}/man3/Module::Loaded*

# Module-Metadata
%exclude %{privlib}/Module/Metadata.pm
%exclude %{_mandir}/man3/Module::Metadata.3pm*

# Module-Pluggable
%exclude %{privlib}/Devel/InnerPackage.pm
%exclude %{privlib}/Module/Pluggable/
%exclude %{privlib}/Module/Pluggable.pm
%exclude %{_mandir}/man3/Devel::InnerPackage*
%exclude %{_mandir}/man3/Module::Pluggable*

# Object-Accessor
%exclude %{privlib}/Object/
%exclude %{_mandir}/man3/Object::Accessor*

# Package-Constants
%exclude %{privlib}/Package/
%exclude %{_mandir}/man3/Package::Constants*

# PathTools
%exclude %{archlib}/Cwd.pm
%exclude %{archlib}/File/Spec*
%exclude %{archlib}/auto/Cwd/
%exclude %{_mandir}/man3/Cwd*
%exclude %{_mandir}/man3/File::Spec*

# Params-Check
%exclude %{privlib}/Params/
%exclude %{_mandir}/man3/Params::Check*

# Perl-OSType
%exclude %{privlib}/Perl/OSType.pm
%exclude %{_mandir}/man3/Perl::OSType.3pm*

# parent
%exclude %{privlib}/parent.pm
%exclude %{_mandir}/man3/parent.3*

# Pod-Checker
%exclude %{_bindir}/podchecker
%exclude %{privlib}/Pod/Checker.pm
%exclude %{_mandir}/man1/podchecker.*
%exclude %{_mandir}/man3/Pod::Checker.*

# Pod-Escapes
%exclude %{privlib}/Pod/Escapes.pm
%exclude %{_mandir}/man3/Pod::Escapes.*

# Pod-LaTeX
%exclude %{_bindir}/pod2latex
%exclude %{privlib}/Pod/LaTeX.pm
%exclude %{_mandir}/man1/pod2latex.1*
%exclude %{_mandir}/man3/Pod::LaTeX.*

# Pod-Parser
%exclude %{_bindir}/podselect
%exclude %{privlib}/Pod/Find.pm
%exclude %{privlib}/Pod/InputObjects.pm
%exclude %{privlib}/Pod/ParseUtils.pm
%exclude %{privlib}/Pod/Parser.pm
%exclude %{privlib}/Pod/PlainText.pm
%exclude %{privlib}/Pod/Select.pm
%exclude %{_mandir}/man1/podselect.1*
%exclude %{_mandir}/man3/Pod::Find.*
%exclude %{_mandir}/man3/Pod::InputObjects.*
%exclude %{_mandir}/man3/Pod::ParseUtils.*
%exclude %{_mandir}/man3/Pod::Parser.*
%exclude %{_mandir}/man3/Pod::PlainText.*
%exclude %{_mandir}/man3/Pod::Select.*

# Pod-Perldoc
%exclude %{_bindir}/perldoc
%exclude %{privlib}/pod/perldoc.pod
%exclude %{privlib}/Pod/Perldoc.pm
%exclude %{privlib}/Pod/Perldoc/
%exclude %{_mandir}/man1/perldoc.1*
%exclude %{_mandir}/man3/Pod::Perldoc*

# Pod-Usage
%exclude %{_bindir}/pod2usage
%exclude %{privlib}/Pod/Usage.pm
%exclude %{_mandir}/man1/pod2usage.*
%exclude %{_mandir}/man3/Pod::Usage.*

# podlators
%exclude %{_bindir}/pod2man
%exclude %{_bindir}/pod2text
%exclude %{privlib}/pod/perlpodstyle.pod
%exclude %{privlib}/Pod/Man.pm
%exclude %{privlib}/Pod/ParseLink.pm
%exclude %{privlib}/Pod/Text
%exclude %{privlib}/Pod/Text.pm
%exclude %{_mandir}/man1/pod2man.1*
%exclude %{_mandir}/man1/pod2text.1*
%exclude %{_mandir}/man1/perlpodstyle.1*
%exclude %{_mandir}/man3/Pod::Man*
%exclude %{_mandir}/man3/Pod::ParseLink*
%exclude %{_mandir}/man3/Pod::Text*

# Pod-Simple
%exclude %{privlib}/Pod/Simple/
%exclude %{privlib}/Pod/Simple.pm
%exclude %{privlib}/Pod/Simple.pod
%exclude %{_mandir}/man3/Pod::Simple*

# Scalar-List-Utils
%exclude %{archlib}/List/
%exclude %{archlib}/Scalar/
%exclude %{archlib}/auto/List/
%exclude %{_mandir}/man3/List::Util*
%exclude %{_mandir}/man3/Scalar::Util*

# Storable
%exclude %{archlib}/Storable.pm
%exclude %{archlib}/auto/Storable/
%exclude %{_mandir}/man3/Storable.*

# Sys-Syslog
%exclude %{archlib}/Sys/Syslog.pm
%exclude %{archlib}/auto/Sys/Syslog/
%exclude %{_mandir}/man3/Sys::Syslog.*

# Term-UI
%exclude %{privlib}/Term/UI.pm
%exclude %{privlib}/Term/UI/
%exclude %{_mandir}/man3/Term::UI*

# Test-Harness
%exclude %{_bindir}/prove
%exclude %{privlib}/App/Prove*
%exclude %{privlib}/TAP*
%exclude %{privlib}/Test/Harness*
%exclude %{_mandir}/man1/prove.1*
%exclude %{_mandir}/man3/App::Prove*
%exclude %{_mandir}/man3/TAP*
%exclude %{_mandir}/man3/Test::Harness*

# Test-Simple
%exclude %{privlib}/Test/More*
%exclude %{privlib}/Test/Builder*
%exclude %{privlib}/Test/Simple*
%exclude %{privlib}/Test/Tutorial*
%exclude %{_mandir}/man3/Test::More*
%exclude %{_mandir}/man3/Test::Builder*
%exclude %{_mandir}/man3/Test::Simple*
%exclude %{_mandir}/man3/Test::Tutorial*

# Text-ParseWords
%exclude %{privlib}/Text/ParseWords.pm
%exclude %{_mandir}/man3/Text::ParseWords.*

# Text-Soundex
%exclude %{archlib}/auto/Text/Soundex/
%exclude %{archlib}/Text/Soundex.pm
%exclude %{_mandir}/man3/Text::Soundex.*

# Thread-Queue
%exclude %{privlib}/Thread/Queue.pm
%exclude %{_mandir}/man3/Thread::Queue.*

# Time-HiRes
%exclude %{archlib}/Time/HiRes.pm
%exclude %{archlib}/auto/Time/HiRes/
%exclude %{_mandir}/man3/Time::HiRes.*

# Time-Local
%exclude %{privlib}/Time/Local.pm
%exclude %{_mandir}/man3/Time::Local.*

# Time-Piece
%exclude %{archlib}/Time/Piece.pm
%exclude %{archlib}/Time/Seconds.pm
%exclude %{archlib}/auto/Time/Piece/
%exclude %{_mandir}/man3/Time::Piece.3*
%exclude %{_mandir}/man3/Time::Seconds.3*

# Version-Requirements
%exclude %{privlib}/Version/Requirements.pm
%exclude %{_mandir}/man3/Version::Requirements*

# Socket
%exclude %dir %{archlib}/auto/Socket
%exclude %{archlib}/auto/Socket/Socket.*
%exclude %{archlib}/Socket.pm
%exclude %{_mandir}/man3/Socket.3*

# threads
%dir %exclude %{archlib}/auto/threads
%exclude %{archlib}/auto/threads/threads*
%exclude %{archlib}/threads.pm
%exclude %{_mandir}/man3/threads.3*

# threads-shared
%exclude %{archlib}/auto/threads/shared*
%exclude %dir %{archlib}/threads
%exclude %{archlib}/threads/shared*
%exclude %{_mandir}/man3/threads::shared*

# version
%exclude %{privlib}/version.pm
%exclude %{privlib}/version.pod
%exclude %{privlib}/version/
%exclude %{_mandir}/man3/version.3*
%exclude %{_mandir}/man3/version::Internals.3*

%files libs
%defattr(-,root,root)
%{archlib}/CORE/libperl.so
%dir %{archlib}
%dir %{perl_vendorarch}
%dir %{perl_vendorarch}/auto

%files devel
%{_bindir}/h2xs
%{_mandir}/man1/h2xs*
%{_bindir}/libnetcfg
%{_mandir}/man1/libnetcfg*
%{_bindir}/perlivp
%{_mandir}/man1/perlivp*
%{archlib}/CORE/*.h
%{_mandir}/man1/perlxs*
%{tapsetdir}/%{libperl_stp}
%doc perl-example.stp

%files macros
%attr(0644,root,root) %{_sysconfdir}/rpm/macros.perl

%files tests
%{perl5_testdir}/
%exclude %{perl5_testdir}/Test-Simple

%if %{dual_life} || %{rebuild_from_scratch}
%files Archive-Extract
%{privlib}/Archive/Extract.pm
%{_mandir}/man3/Archive::Extract.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Archive-Tar
%{_bindir}/ptar
%{_bindir}/ptardiff
%{_bindir}/ptargrep
%{privlib}/Archive/Tar/ 
%{privlib}/Archive/Tar.pm
%{_mandir}/man1/ptar.1*
%{_mandir}/man1/ptardiff.1*
%{_mandir}/man1/ptargrep.1*
%{_mandir}/man3/Archive::Tar* 
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files autodie
%{privlib}/autodie/
%{privlib}/autodie.pm
%{privlib}/Fatal.pm
%{_mandir}/man3/autodie.3*
%{_mandir}/man3/autodie::*
%{_mandir}/man3/Fatal.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files B-Lint
%{privlib}/B/Lint*
%{_mandir}/man3/B::Lint*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Carp
%{privlib}/Carp
%{privlib}/Carp.*
%{_mandir}/man3/Carp.*

%files CGI
%{privlib}/CGI/
%{privlib}/CGI.pm
%{_mandir}/man3/CGI.3*
%{_mandir}/man3/CGI::*.3*

%files Compress-Raw-Bzip2
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Bzip2.pm
%dir %{archlib}/auto/Compress/
%dir %{archlib}/auto/Compress/Raw/
%{archlib}/auto/Compress/Raw/Bzip2/
%{_mandir}/man3/Compress::Raw::Bzip2*

%files Compress-Raw-Zlib
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Zlib.pm
%dir %{archlib}/auto/Compress/
%dir %{archlib}/auto/Compress/Raw/
%{archlib}/auto/Compress/Raw/Zlib/
%{_mandir}/man3/Compress::Raw::Zlib*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files constant
%{privlib}/constant.pm
%{_mandir}/man3/constant.3*
%endif

%files CPAN
%{_bindir}/cpan
%{privlib}/App/Cpan.pm
%{privlib}/CPAN/
%{privlib}/CPAN.pm
%{_mandir}/man1/cpan.1*
%{_mandir}/man3/App::Cpan.*
%{_mandir}/man3/CPAN.*
%{_mandir}/man3/CPAN:*
%exclude %{privlib}/CPAN/Meta/
%exclude %{privlib}/CPAN/Meta.pm
%exclude %{_mandir}/man3/CPAN::Meta*

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta.pm
%{privlib}/CPAN/Meta/Converter.pm
%{privlib}/CPAN/Meta/Feature.pm
%{privlib}/CPAN/Meta/History.pm
%{privlib}/CPAN/Meta/Prereqs.pm
%{privlib}/CPAN/Meta/Spec.pm
%{privlib}/CPAN/Meta/Validator.pm
%{_mandir}/man3/CPAN::Meta*
%exclude %{_mandir}/man3/CPAN::Meta::YAML*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-Requirements
%{privlib}/CPAN/Meta/Requirements.pm
%{_mandir}/man3/CPAN::Meta::Requirements.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-YAML
%{privlib}/CPAN/Meta/YAML.pm
%{_mandir}/man3/CPAN::Meta::YAML*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPANPLUS
%{_bindir}/cpan2dist
%{_bindir}/cpanp
%{_bindir}/cpanp-run-perl
%{privlib}/CPANPLUS/
%{privlib}/CPANPLUS.pm
%exclude %{privlib}/CPANPLUS/Dist/Build/
%{_mandir}/man1/cpan2dist.1*
%{_mandir}/man1/cpanp.1*
%{_mandir}/man3/CPANPLUS*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPANPLUS-Dist-Build
%{privlib}/CPANPLUS/Dist/Build/
%{privlib}/CPANPLUS/Dist/Build.pm
%{_mandir}/man3/CPANPLUS::Dist::Build.3*
%{_mandir}/man3/CPANPLUS::Dist::Build::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Data-Dumper
%dir %{archlib}/auto/Data
%dir %{archlib}/auto/Data/Dumper
%{archlib}/auto/Data/Dumper/Dumper.so
%dir %{archlib}/Data
%{archlib}/Data/Dumper.pm
%{_mandir}/man3/Data::Dumper.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files DB_File
%{archlib}/DB_File.pm
%dir %{archlib}/auto/DB_File
%{archlib}/auto/DB_File/DB_File.so
%{_mandir}/man3/DB_File*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest
%{privlib}/Digest.pm
%dir %{privlib}/Digest
%{privlib}/Digest/base.pm
%{privlib}/Digest/file.pm
%{_mandir}/man3/Digest.3*
%{_mandir}/man3/Digest::base.3*
%{_mandir}/man3/Digest::file.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-MD5
%{archlib}/Digest/MD5.pm
%{archlib}/auto/Digest/MD5/
%{_mandir}/man3/Digest::MD5.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-SHA
%{_bindir}/shasum
%dir %{archlib}/Digest/
%{archlib}/Digest/SHA.pm
%{archlib}/auto/Digest/SHA/
%{_mandir}/man1/shasum.1*
%{_mandir}/man3/Digest::SHA.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Encode
%{_bindir}/piconv
%{archlib}/encoding.pm
%{archlib}/Encode*
%{archlib}/auto/Encode*
%{privlib}/Encode
%exclude %{privlib}/Encode/*.e2x
%exclude %{privlib}/Encode/encode.h
%{_mandir}/man1/piconv.1*
%{_mandir}/man3/encoding.3*
%{_mandir}/man3/Encode*.3*

%files Encode-devel
%{_bindir}/enc2xs
%{privlib}/Encode/*.e2x
%{privlib}/Encode/encode.h
%{_mandir}/man1/enc2xs.1*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Env
%{privlib}/Env.pm
%{_mandir}/man3/Env.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Exporter
%{privlib}/Exporter*
%{_mandir}/man3/Exporter*
%endif

%files ExtUtils-CBuilder
%{privlib}/ExtUtils/CBuilder/
%{privlib}/ExtUtils/CBuilder.pm
%{_mandir}/man3/ExtUtils::CBuilder*

%files ExtUtils-Embed
%{privlib}/ExtUtils/Embed.pm
%{_mandir}/man3/ExtUtils::Embed*

%files ExtUtils-Install
%{privlib}/ExtUtils/Install.pm
%{privlib}/ExtUtils/Installed.pm
%{privlib}/ExtUtils/Packlist.pm
%{_mandir}/man3/ExtUtils::Install.3*
%{_mandir}/man3/ExtUtils::Installed.3*
%{_mandir}/man3/ExtUtils::Packlist.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Manifest
%{privlib}/ExtUtils/Manifest.pm
%{privlib}/ExtUtils/MANIFEST.SKIP
%{_mandir}/man3/ExtUtils::Manifest.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-MakeMaker
%{_bindir}/instmodsh
%{privlib}/ExtUtils/Command/
%{privlib}/ExtUtils/Liblist/
%{privlib}/ExtUtils/Liblist.pm
%{privlib}/ExtUtils/MakeMaker/
%{privlib}/ExtUtils/MakeMaker.pm
%{privlib}/ExtUtils/MM*.pm
%{privlib}/ExtUtils/MY.pm
%{privlib}/ExtUtils/Mkbootstrap.pm
%{privlib}/ExtUtils/Mksymlists.pm
%{privlib}/ExtUtils/testlib.pm
%{_mandir}/man1/instmodsh.1*
%{_mandir}/man3/ExtUtils::Command::MM*
%{_mandir}/man3/ExtUtils::Liblist.3*
%{_mandir}/man3/ExtUtils::MM*
%{_mandir}/man3/ExtUtils::MY.3*
%{_mandir}/man3/ExtUtils::MakeMaker*
%{_mandir}/man3/ExtUtils::Mkbootstrap.3*
%{_mandir}/man3/ExtUtils::Mksymlists.3*
%{_mandir}/man3/ExtUtils::testlib.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-ParseXS
%dir %{privlib}/ExtUtils/ParseXS/
%dir %{privlib}/ExtUtils/Typemaps/
%{privlib}/ExtUtils/ParseXS.pm
%{privlib}/ExtUtils/ParseXS.pod
%{privlib}/ExtUtils/ParseXS/Constants.pm
%{privlib}/ExtUtils/ParseXS/CountLines.pm
%{privlib}/ExtUtils/ParseXS/Utilities.pm
%{privlib}/ExtUtils/Typemaps.pm
%{privlib}/ExtUtils/Typemaps/Cmd.pm
%{privlib}/ExtUtils/Typemaps/InputMap.pm
%{privlib}/ExtUtils/Typemaps/OutputMap.pm
%{privlib}/ExtUtils/Typemaps/Type.pm
%{privlib}/ExtUtils/xsubpp
%{_bindir}/xsubpp
%{_mandir}/man1/xsubpp*
%{_mandir}/man3/ExtUtils::ParseXS.3*
%{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
%{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
%{_mandir}/man3/ExtUtils::Typemaps.3*
%{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
%{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::Type.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-CheckTree
%{privlib}/File/CheckTree.pm
%{_mandir}/man3/File::CheckTree.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Fetch
%{privlib}/File/Fetch.pm
%{_mandir}/man3/File::Fetch.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Path
%{privlib}/File/Path.pm
%{_mandir}/man3/File::Path.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Temp
%{privlib}/File/Temp.pm
%{_mandir}/man3/File::Temp.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter
%{archlib}/auto/Filter/Util
%{archlib}/Filter/Util
%{privlib}/pod/perlfilter.pod
%{_mandir}/man1/perlfilter.*
%{_mandir}/man3/Filter::Util::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Getopt-Long
%{privlib}/Getopt/Long.pm
%{_mandir}/man3/Getopt::Long.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Compress
# IO-Compress
%{_bindir}/zipdetails
%{privlib}/IO/Compress/FAQ.pod
%{_mandir}/man1/zipdetails.*
%{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
%{privlib}/Compress/Zlib.pm
%{_mandir}/man3/Compress::Zlib*
#IO-Compress-Base
%{privlib}/File/GlobMapper.pm
%{privlib}/IO/Compress/Base/
%{privlib}/IO/Compress/Base.pm
%{privlib}/IO/Uncompress/AnyUncompress.pm
%{privlib}/IO/Uncompress/Base.pm
%{_mandir}/man3/File::GlobMapper.*
%{_mandir}/man3/IO::Compress::Base.*
%{_mandir}/man3/IO::Uncompress::AnyUncompress.*
%{_mandir}/man3/IO::Uncompress::Base.*

# IO-Compress-Zlib
%{privlib}/IO/Compress/Adapter/
%{privlib}/IO/Compress/Deflate.pm
%{privlib}/IO/Compress/Bzip2.pm
%{privlib}/IO/Compress/Gzip/
%{privlib}/IO/Compress/Gzip.pm
%{privlib}/IO/Compress/RawDeflate.pm
%{privlib}/IO/Compress/Zip/
%{privlib}/IO/Compress/Zip.pm
%{privlib}/IO/Compress/Zlib/
%{privlib}/IO/Uncompress/Adapter/
%{privlib}/IO/Uncompress/AnyInflate.pm
%{privlib}/IO/Uncompress/Bunzip2.pm
%{privlib}/IO/Uncompress/Gunzip.pm
%{privlib}/IO/Uncompress/Inflate.pm
%{privlib}/IO/Uncompress/RawInflate.pm
%{privlib}/IO/Uncompress/Unzip.pm
%{_mandir}/man3/IO::Compress::Deflate*
%{_mandir}/man3/IO::Compress::Gzip*
%{_mandir}/man3/IO::Compress::Bzip2*
%{_mandir}/man3/IO::Compress::RawDeflate*
%{_mandir}/man3/IO::Compress::Zip*
%{_mandir}/man3/IO::Uncompress::AnyInflate*
%{_mandir}/man3/IO::Uncompress::Bunzip2*
%{_mandir}/man3/IO::Uncompress::Gunzip*
%{_mandir}/man3/IO::Uncompress::Inflate*
%{_mandir}/man3/IO::Uncompress::RawInflate*
%{_mandir}/man3/IO::Uncompress::Unzip*
%endif

%files IO-Zlib
%{privlib}/IO/Zlib.pm
%{_mandir}/man3/IO::Zlib.*

%if %{dual_life} || %{rebuild_from_scratch}
%files HTTP-Tiny
%{privlib}/HTTP/Tiny.pm
%{_mandir}/man3/HTTP::Tiny*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-Cmd
%{privlib}/IPC/Cmd.pm
%{_mandir}/man3/IPC::Cmd.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files JSON-PP
%{_bindir}/json_pp
%{privlib}/JSON/PP
%{privlib}/JSON/PP.pm
%{_mandir}/man1/json_pp.1*
%{_mandir}/man3/JSON::PP.3*
%{_mandir}/man3/JSON::PP::Boolean.3pm*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Locale-Codes
%{privlib}/Locale/Codes
%{privlib}/Locale/Codes.*
%{privlib}/Locale/Country.*
%{privlib}/Locale/Currency.*
%{privlib}/Locale/Language.*
%{privlib}/Locale/Script.*
%{_mandir}/man3/Locale::Codes::*
%{_mandir}/man3/Locale::Codes.*
%{_mandir}/man3/Locale::Country.*
%{_mandir}/man3/Locale::Currency.*
%{_mandir}/man3/Locale::Language.*
%{_mandir}/man3/Locale::Script.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Locale-Maketext
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext.*
%{privlib}/Locale/Maketext/Cookbook.*
%{privlib}/Locale/Maketext/Guts.*
%{privlib}/Locale/Maketext/GutsLoader.*
%{privlib}/Locale/Maketext/TPJ13.*
%{_mandir}/man3/Locale::Maketext.*
%{_mandir}/man3/Locale::Maketext::Cookbook.*
%{_mandir}/man3/Locale::Maketext::Guts.*
%{_mandir}/man3/Locale::Maketext::GutsLoader.*
%{_mandir}/man3/Locale::Maketext::TPJ13.*
%endif

%files Locale-Maketext-Simple
%{privlib}/Locale/Maketext/Simple.pm
%{_mandir}/man3/Locale::Maketext::Simple.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Log-Message
%{privlib}/Log/Message.pm
%{privlib}/Log/Message/Config.pm
%{privlib}/Log/Message/Handlers.pm
%{privlib}/Log/Message/Item.pm
%{_mandir}/man3/Log::Message.3*
%{_mandir}/man3/Log::Message::Config.3*
%{_mandir}/man3/Log::Message::Handlers.3*
%{_mandir}/man3/Log::Message::Item.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Log-Message-Simple
%{privlib}/Log/Message/Simple.pm
%{_mandir}/man3/Log::Message::Simple.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Build
%{_bindir}/config_data
%{privlib}/inc/
%{privlib}/Module/Build/
%{privlib}/Module/Build.pm
%{_mandir}/man1/config_data.1*
%{_mandir}/man3/Module::Build*
%{_mandir}/man3/inc::latest.3*
%endif

%files Module-CoreList
%{_bindir}/corelist
%{privlib}/Module/CoreList.pm
%{_mandir}/man1/corelist*
%{_mandir}/man3/Module::CoreList*

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load
%{privlib}/Module/Load.pm
%{_mandir}/man3/Module::Load.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load-Conditional
%{privlib}/Module/Load/
%{_mandir}/man3/Module::Load::Conditional* 
%endif

%files Module-Loaded
%dir %{privlib}/Module/
%{privlib}/Module/Loaded.pm
%{_mandir}/man3/Module::Loaded*

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Metadata
%{privlib}/Module/Metadata.pm
%{_mandir}/man3/Module::Metadata.3pm*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Pluggable
%{privlib}/Devel/InnerPackage.pm
%{privlib}/Module/Pluggable/
%{privlib}/Module/Pluggable.pm
%{_mandir}/man3/Devel::InnerPackage*
%{_mandir}/man3/Module::Pluggable*
%endif

%files Object-Accessor
%{privlib}/Object/
%{_mandir}/man3/Object::Accessor*

%files Package-Constants
%{privlib}/Package/
%{_mandir}/man3/Package::Constants*

%if %{dual_life} || %{rebuild_from_scratch}
%files PathTools
%{archlib}/Cwd.pm
%{archlib}/File/Spec*
%{archlib}/auto/Cwd/
%{_mandir}/man3/Cwd*
%{_mandir}/man3/File::Spec*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Params-Check
%{privlib}/Params/
%{_mandir}/man3/Params::Check*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Parse-CPAN-Meta
%dir %{privlib}/Parse/
%dir %{privlib}/Parse/CPAN/
%{privlib}/Parse/CPAN/Meta.pm
%{_mandir}/man3/Parse::CPAN::Meta.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files parent
%{privlib}/parent.pm
%{_mandir}/man3/parent.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Perl-OSType
%{privlib}/Perl/OSType.pm
%{_mandir}/man3/Perl::OSType.3pm*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Checker
%{_bindir}/podchecker
%{privlib}/Pod/Checker.pm
%{_mandir}/man1/podchecker.*
%{_mandir}/man3/Pod::Checker.*
%endif

%files Pod-Escapes
%{privlib}/Pod/Escapes.pm
%{_mandir}/man3/Pod::Escapes.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-LaTeX
%{_bindir}/pod2latex
%{privlib}/Pod/LaTeX.pm
%{_mandir}/man1/pod2latex.1*
%{_mandir}/man3/Pod::LaTeX.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Parser
%{_bindir}/pod2usage
%{_bindir}/podchecker
%{_bindir}/podselect
%{privlib}/Pod/Checker.pm
%{privlib}/Pod/Find.pm
%{privlib}/Pod/InputObjects.pm
%{privlib}/Pod/ParseUtils.pm
%{privlib}/Pod/Parser.pm
%{privlib}/Pod/PlainText.pm
%{privlib}/Pod/Select.pm
%{privlib}/Pod/Usage.pm
%{_mandir}/man1/pod2usage.1*
%{_mandir}/man1/podchecker.1*
%{_mandir}/man1/podselect.1*
%{_mandir}/man3/Pod::Checker.*
%{_mandir}/man3/Pod::Find.*
%{_mandir}/man3/Pod::InputObjects.*
%{_mandir}/man3/Pod::ParseUtils.*
%{_mandir}/man3/Pod::Parser.*
%{_mandir}/man3/Pod::PlainText.*
%{_mandir}/man3/Pod::Select.*
%{_mandir}/man3/Pod::Usage.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Perldoc
%{_bindir}/perldoc
%{privlib}/pod/perldoc.pod
%{privlib}/Pod/Perldoc.pm
%{privlib}/Pod/Perldoc/
%{_mandir}/man1/perldoc.1*
%{_mandir}/man3/Pod::Perldoc*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Usage
%{_bindir}/pod2usage
%{privlib}/Pod/Usage.pm
%{_mandir}/man1/pod2usage.*
%{_mandir}/man3/Pod::Usage.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files podlators
%{_bindir}/pod2man
%{_bindir}/pod2text
%{privlib}/pod/perlpodstyle.pod
%{privlib}/Pod/Man.pm
%{privlib}/Pod/ParseLink.pm
%{privlib}/Pod/Text
%{privlib}/Pod/Text.pm
%{_mandir}/man1/pod2man.1*
%{_mandir}/man1/pod2text.1*
%{_mandir}/man1/perlpodstyle.1*
%{_mandir}/man3/Pod::Man*
%{_mandir}/man3/Pod::ParseLink*
%{_mandir}/man3/Pod::Text*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Simple
%{privlib}/Pod/Simple/ 
%{privlib}/Pod/Simple.pm
%{privlib}/Pod/Simple.pod
%{_mandir}/man3/Pod::Simple*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Scalar-List-Utils
%{archlib}/List/
%{archlib}/Scalar/
%{archlib}/auto/List/
%{_mandir}/man3/List::Util*
%{_mandir}/man3/Scalar::Util*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Sys-Syslog
%{archlib}/Sys/Syslog.pm
%{archlib}/auto/Sys/Syslog/
%{_mandir}/man3/Sys::Syslog.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Socket
%dir %{archlib}/auto/Socket
%{archlib}/auto/Socket/Socket.*
%{archlib}/Socket.pm
%{_mandir}/man3/Socket.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Storable
%{archlib}/Storable.pm
%{archlib}/auto/Storable/
%{_mandir}/man3/Storable.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-UI
%{privlib}/Term/UI/
%{privlib}/Term/UI.pm
%{_mandir}/man3/Term::UI*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Harness
%{_bindir}/prove
%{privlib}/App/Prove*
%{privlib}/TAP*
%{privlib}/Test/Harness*
%{_mandir}/man1/prove.1*
%{_mandir}/man3/App::Prove*
%{_mandir}/man3/TAP*
%{_mandir}/man3/Test::Harness*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Simple
%{privlib}/Test/More*
%{privlib}/Test/Builder*
%{privlib}/Test/Simple*
%{privlib}/Test/Tutorial*
%{_mandir}/man3/Test::More*
%{_mandir}/man3/Test::Builder*
%{_mandir}/man3/Test::Simple*
%{_mandir}/man3/Test::Tutorial*

%files Test-Simple-tests
%dir %{perl5_testdir}
%{perl5_testdir}/Test-Simple
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-ParseWords
%{privlib}/Text/ParseWords.pm
%{_mandir}/man3/Text::ParseWords.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Soundex
%{archlib}/auto/Text/Soundex/
%{archlib}/Text/Soundex.pm
%{_mandir}/man3/Text::Soundex.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Thread-Queue
%{privlib}/Thread/Queue.pm
%{_mandir}/man3/Thread::Queue.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-HiRes
%{archlib}/Time/HiRes.pm
%{archlib}/auto/Time/HiRes/
%{_mandir}/man3/Time::HiRes.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-Local
%{privlib}/Time/Local.pm
%{_mandir}/man3/Time::Local.*
%endif

%files Time-Piece
%{archlib}/Time/Piece.pm 
%{archlib}/Time/Seconds.pm
%{archlib}/auto/Time/Piece/        
%{_mandir}/man3/Time::Piece.3*
%{_mandir}/man3/Time::Seconds.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Version-Requirements
%{privlib}/Version/Requirements.pm
%{_mandir}/man3/Version::Requirements*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files threads
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/threads*
%{archlib}/threads.pm
%{_mandir}/man3/threads.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files threads-shared
%{archlib}/auto/threads/shared*
%dir %{archlib}/threads
%{archlib}/threads/shared*
%{_mandir}/man3/threads::shared*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files version
%{privlib}/version.pm
%{privlib}/version.pod
%{privlib}/version/
%{_mandir}/man3/version.3*
%{_mandir}/man3/version::Internals.3*
%endif

%files core
# Nothing. Nada. Zilch. Zarro. Uh uh. Nope. Sorry.

# Old changelog entries are preserved in CVS.
%changelog
* Mon Jan 07 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.3-294
- Fix CVE-2018-18311 Integer overflow leading to buffer overflow (bug #1661064)

* Wed Mar 21 2018 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-293
- Add SSL support to Net::SMTP (bug #1557574)
- Do not overload ".." in Math::BigInt (bug #1497734)
- Provide perl(:VERSION) and perl-interpreter RPM symbols (bug #1410347)

* Mon Feb 27 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.3-292
- Removed perl-Perl4-CoreLibs because it was added as separate package to
  RHEL (bug #1366724)

* Wed Aug 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.3-291
- Backported and sub-packaged libraries historically supplied with Perl 4
  into perl-Perl4-CoreLibs

* Tue Aug 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.3-290
- Removed deprecated files from provides (bug #1365991)

* Mon Jun 13 2016 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-289
- Fix duplicating PerlIO::encoding when spawning threads (bug #1344749)

* Wed Mar 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.3-288
- Fix CRLF conversion in ASCII FTP upload (bug #1263734)
- Don't leak the temp utf8 copy of namepv (bug #1063330)

* Wed Mar 02 2016 Petr Šabata <contyk@redhat.com> - 4:5.16.3-287
- Make File::Glob work with threads again (bug #1223045)

* Thu Jul 02 2015 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-286
- Remove CPU-speed-sensitive test in Benchmark test (bug #1238567)
- Rebuild with corrected binutils to fix systemtap support (bug #1238472)

* Mon Dec 01 2014 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-285
- Use stronger algorithm needed for FIPS in t/op/taint.t (bug #1084796)

* Fri Aug 08 2014 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-284
- Use a macro to cover all 64-bit PowerPC architectures (bug #1061792)
- Declare dependencies for cpan tool (bug #1122368)
- Use stronger algorithm needed for FIPS in t/op/crypt.t (bug #1084796)
- Make *DBM_File desctructors thread-safe (bug #1107542)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4:5.16.3-283
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4:5.16.3-282
- Mass rebuild 2013-12-27

* Mon Dec 02 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-281
- Document Math::BigInt::CalcEmu requires Math::BigInt (bug #959096)

* Wed Jun 26 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-280
- Edit local patch level before compilation

* Fri Jun 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-279
- Do not distribute File::Spec::VMS (bug #973713)
- Remove bundled CPANPLUS-Dist-Build (bug #973041)

* Wed Jun 12 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-278
- Update SystemTap scripts to recognize new phase__change marker and new probe
  arguments (bug #971094)
- Update h2ph(1) documentation (bug #948538)
- Update pod2html(1) documentation (bug #948538)
- Do not double-own archlib directory (bug #894195)

* Tue Jun 11 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-277
- Move CPANPLUS-Dist-Build files from perl-CPANPLUS
- Move CPAN-Meta-Requirements files from CPAN-Meta
- Add perl-Scalar-List-Utils to perl-core dependencies

* Thu Jun 06 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-276
- Require $Config{libs} providers (bug #905482)

* Thu May 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-275
- Correct typo in perl-Storable file list (bug #966865)
- Remove bundled Storable (bug #966865)

* Wed May 29 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-274
- Sub-package Storable (bug #966865)

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-273
- Use lib64 directories on aarch64 architecture (bug #961900)

* Fri May 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-272
- Make regular expression engine safe in a signal handler (bug #849703)
- Remove bundled ExtUtils-ParseXS, and Time-HiRes

* Fri Apr 26 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-271
- Sub-package Time-HiRes (bug #957048)
- Remove bundled Getopt-Long, Locale-Maketext, and Sys-Syslog

* Wed Apr 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-270
- Fix leaking tied hashes (bug #859910)
- Fix dead lock in PerlIO after fork from thread (bug #947444)
- Add proper conflicts to perl-Getopt-Long, perl-Locale-Maketext, and
  perl-Sys-Syslog

* Tue Apr 09 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-269
- Sub-package Sys-Syslog (bug #950057)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-268
- Sub-package Getopt-Long (bug #948855)
- Sub-package Locale-Maketext (bug #948974)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-267
- Remove bundled constant, DB_File, Digest-MD5, Env, Exporter, File-Path,
  File-Temp, Module-Load, Log-Message-Simple, Pod-Simple, Test-Harness,
  Text-ParseWords

* Mon Mar 25 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-266
- Filter provides from *.pl files (bug #924938)

* Fri Mar 22 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-265
- Conflict perl-autodie with older perl (bug #911226)
- Sub-package Env (bug #924619)
- Sub-package Exporter (bug #924645)
- Sub-package File-Path (bug #924782)
- Sub-package File-Temp (bug #924822)

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-264
- Sub-package constant (bug #924169)
- Sub-package DB_File (bug #924351)

* Tue Mar 19 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-263
- Correct perl-Digest-MD5 dependencies
- Remove bundled Archive-Extract, File-Fetch, HTTP-Tiny,
  Module-Load-Conditional, Time-Local

* Fri Mar 15 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-262
- Correct dependencies of perl-HTTP-Tiny
- Sub-package Time-Local (bug #922054)

* Thu Mar 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-261
- 5.16.3 bump (see <http://search.cpan.org/dist/perl-5.16.3/pod/perldelta.pod>
  for release notes)
- Remove bundled autodie, B-Lint, CPANPLUS, Encode, File-CheckTree, IPC-Cmd,
  Params-Check, Text-Soundex, Thread-Queue

* Tue Mar 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-260
- Fix CVE-2013-1667 (DoS in rehashing code) (bug #918008)

* Mon Feb 18 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-259
- Sub-package autodie (bug #911226)
- Add NAME headings to CPAN modules (bug #908113)

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-258
- Fix perl-Encode-devel dependency declaration

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-257
- Sub-package Thread-Queue (bug #911062)

* Wed Feb 13 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-256
- Sub-package File-CheckTree (bug #909144)
- Sub-package Text-ParseWords
- Sub-package Encode (bug #859149)

* Fri Feb 08 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-255
- Remove bundled Log-Message
- Remove bundled Term-UI

* Thu Feb 07 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-254
- Correct perl-podlators dependencies
- Obsolete perl-ExtUtils-Typemaps by perl-ExtUtils-ParseXS (bug #891952)

* Tue Feb 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-253
- Sub-package Pod-Checker and Pod-Usage (bugs #907546, #907550)

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-252
- Remove bundled PathTools

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-251
- Sub-package B-Lint (bug #906015)

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-250
- Sub-package Text-Soundex (bug #905889)
- Fix conflict declaration at perl-Pod-LaTeX (bug #904085)
- Remove bundled Module-Pluggable (bug #903624)

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-249
- Run-require POD convertors by Module-Build and ExtUtils-MakeMaker to
  generate documentation when building other packages

* Fri Jan 25 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-248
- Sub-package Pod-LaTeX (bug #904085)

* Wed Jan 16 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-247
- Remove bundled Pod-Parser

* Fri Jan 11 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-246
- Fix CVE-2012-6329 (misparsing of maketext strings) (bug #884354)

* Thu Jan 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-245
- Do not package App::Cpan(3pm) to perl-Test-Harness (bug #893768)

* Tue Dec 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-244
- Remove bundled Archive-Tar
- Remove bundled CPAN-Meta-YAML
- Remove bundled Module-Metadata

* Tue Dec 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-243
- Remove bundled Filter modules

* Mon Nov 05 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.2-242
- 5.16.2 bump (see
  http://search.cpan.org/dist/perl-5.16.1/pod/perldelta.pod for release
  notes)

* Wed Oct 31 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-241
- Remove bundled podlators (bug #856516)

* Wed Oct 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.1-240
- Do not crash when vivifying $| (bug #865296)

* Mon Sep 24 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-239
- Conflict perl-podlators with perl before sub-packaging (bug #856516)

* Fri Sep 21 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-238
- Do not leak with attribute on my variable (bug #858966)
- Allow operator after numeric keyword argument (bug #859328)
- Extend stack in File::Glob::glob (bug #859332)

* Thu Sep 20 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-237
- Put perl-podlators into perl-core list (bug #856516)

* Tue Sep 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-236
- Remove bundled perl-ExtUtils-Manifest
- perl-PathTools uses Carp

* Fri Sep 14 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-235
- Override the Pod::Simple::parse_file to set output to STDOUT by default
  (bug #826872)

* Wed Sep 12 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-234
- Sub-package perl-podlators (bug #856516)

* Tue Sep 11 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-233
- Do not access freed memory when cloning thread (bug #825749)
- Match non-breakable space with /[\h]/ in ASCII mode (bug #844919)
- Clear $@ before `do' I/O error (bug #834226)
- Do not truncate syscall() return value to 32 bits (bug #838551)

* Wed Sep 05 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-232
- Move App::Cpan from perl-Test-Harness to perl-CPAN (bug #854577)

* Fri Aug 24 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-231
- Remove perl-devel dependency from perl-Test-Harness and perl-Test-Simple

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-230
- define perl_compat by macro for rebuilds
- sub-packages depend on compat rather than on nvr

* Thu Aug  9 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-229
- apply conditionals for dual life patches

* Thu Aug 09 2012 Jitka Plesnikova <jplesnik@redhat.com> 4:5.16.1-228
- 5.16.1 bump (see
  http://search.cpan.org/dist/perl-5.16.1/pod/perldelta.pod for release
  notes)
- Fixed reopening by scalar handle (bug #834221)
- Fixed tr/// multiple transliteration (bug #831679)
- Fixed heap-overflow in gv_stashpv (bug #826516)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.16.0-227
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Paul Howarth <paul@city-fan.org> 4:5.16.0-226
- Move the rest of ExtUtils-ParseXS into its sub-package, so that the main
  perl package doesn't need to pull in perl-devel (bug #839953)

* Mon Jul 02 2012 Jitka Plesnikova <jplesnik@redhat.com> 4:5.16.0-225
- Fix broken atof (bug #835452)

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-224
- perl-Pod-Perldoc must require groff-base because Pod::Perldoc::ToMan executes
  roff

* Mon Jun 25 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-223
- Test::Build requires Data::Dumper
- Sub-package perl-Pod-Parser

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-222
- Remove MODULE_COMPAT_5.14.* Provides

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-221
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-220
- perl_bootstrap macro is distributed in perl-srpm-macros now

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-219
- Own zipdetails and IO::Compress::FAQ by perl-IO-Compress

* Fri Jun  1 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.0-218
- Fix find2perl to translate ? glob properly (bug #825701)

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-218
- Shorten perl-Module-Build version to 2 digits to follow upstream

* Fri May 25 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-217
- upload the stable 5.16.0

* Wed May 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-RC2-217
- clean patches, not needed with new version
- regen by podcheck list of failed pods. cn, jp, ko pods failed. I can't decide
  whether it's a real problem or false positives.

* Mon Apr 30 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-216
- Enable usesitecustomize

* Thu Apr 19 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-215
- Rebuild perl against Berkeley database version 5 (bug #768846)

* Fri Apr 13 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-214
- perl-Data-Dumper requires Scalar::Util (bug #811239)

* Tue Apr 10 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-213
- Sub-package Data::Dumper (bug #811239)

* Tue Feb 21 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-212
- Sub-package Filter (bug #790349)

* Mon Feb 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-211
- Fix searching for Unicode::Collate::Locale data (bug #756118)
- Run safe signal handlers before returning from sigsuspend() and pause()
  (bug #771228)
- Correct perl-Scalar-List-Utils files list
- Stop !$^V from leaking (bug #787613)

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 4:5.14.2-210
- Rebuild again now that perl dependency generator is fixed (#772632, #772699)

* Fri Jan 06 2012 Iain Arnell <iarnell@gmail.com> -4:5.14.2-209
- perl-ExtUtils-MakeMaker sub-package requires ExtUtils::Install

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> - 4:5.14.2-208
- Rebuild for gcc 4.7

* Tue Dec 20 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-207
- Fix interrupted reading. Thanks to Šimon Lukašík for reporting this issue
  and thanks to Marcela Mašláňová for finding fix. (bug #767931)

* Wed Dec 14 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-206
- Fix leak with non-matching named captures (bug #767597)

* Tue Nov 29 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-205
- Sub-package ExtUtils::Install
- Sub-package ExtUtils::Manifest
- Do not provide private perl(ExtUtils::MakeMaker::_version)

* Thu Nov 24 2011 Ville Skyttä <ville.skytta@iki.fi> - 4:5.14.2-204
- Add $RPM_LD_FLAGS to lddlflags.

* Wed Nov 23 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-203
- Sub-package Socket

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-202
- Sub-package Pod::Perldoc

* Fri Nov 18 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-201
- Increase epoch of perl-Module-CoreList to overcome version regression in
  upstream (bug #754641)

* Thu Nov  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.2-200
- perl(DBIx::Simple) is not needed in spec requirement in CPANPLUS. It's generated
  automatically.

* Wed Nov 02 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-199
- Provide perl(DB) by perl

* Mon Oct 24 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-198
- Do not warn about missing site directories (bug #732799)

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.2-197
- cleaned spec (thanks to Grigory Batalov)
-  Module-Metadata sub-package contained perl_privlib instead of privlib
-  %%files parent section was repeated twice

* Fri Oct 14 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-196
- Filter false perl(DynaLoader) provide from perl-ExtUtils-MakeMaker
  (bug #736714)
- Change Perl_repeatcpy() prototype to allow repeat count above 2^31
  (bug #720610)
- Do not own site directories located in /usr/local (bug #732799)

* Tue Oct 04 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-195
- Fix CVE-2011-3597 (code injection in Digest) (bug #743010)
- Sub-package Digest and thus Digest::MD5 module (bug #743247)

* Tue Oct 04 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.2-194
- add provide for perl(:MODULE_COMPAT_5.14.2)

* Mon Oct 03 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-193
- 5.14.2 bump (see
  https://metacpan.org/module/FLORA/perl-5.14.2/pod/perldelta.pod for release
  notes).
- Fixes panics when processing regular expression with \b class and /aa
  modifier (bug #731062)
- Fixes CVE-2011-2728 (File::Glob bsd_glob() crash with certain glob flags)
  (bug #742987)

* Mon Oct 03 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-192
- Enable GDBM support again to build against new gdbm 1.9.1

* Fri Sep 30 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-191
- Disable NDBM support temporarily too as it's provided by gdbm package

* Wed Sep 21 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-190
- Disable GDBM support temporarily to build new GDBM

* Thu Sep 15 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-189
- Correct perl-CGI list of Provides
- Make tests optional
- Correct perl-ExtUtils-ParseXS Provides
- Correct perl-Locale-Codes Provides
- Correct perl-Module-CoreList version
- Automate perl-Test-Simple-tests Requires version

* Tue Sep 13 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-188
- Make gdbm support optional to bootstrap with new gdbm
- Split Carp into standalone sub-package to dual-live with newer versions
  (bug #736768)

* Tue Aug 30 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-187
- Split Locale::Codes into standalone sub-package to dual-live with newer
  versions (bug #717863)

* Sun Aug 14 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-186
- perl needs to own vendorarch/auto directory

* Fri Aug 05 2011 Petr Sabata <contyk@redhat.com> - 4:5.14.1-185
- Move xsubpp to ExtUtils::ParseXS (#728393)

* Fri Jul 29 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-184
- fix Compress-Raw-Bzip2 pacakging
- ensure that we never bundle bzip2 or zlib

* Tue Jul 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-183
- remove from provides MODULE_COMPAT 5.12.*

* Fri Jul 22 2011 Paul Howarth <paul@city-fan.org> - 4:5.14.1-182
- Have perl-Module-Build explicitly require perl(CPAN::Meta) >= 2.110420,
  needed for creation of MYMETA files by Build.PL; the dual-life version of
  the package already has this dependency

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 4:5.14.1-181
- Temporarily provide 5.12.* MODULE_COMPAT

* Sat Jul 16 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-180
- fix escaping of the __provides_exclude_from macro

* Wed Jul 13 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-179
- Parse-CPAN-Meta explicitly requires CPAN::Meta::YAML and JSON::PP
- Exclude CPAN::Meta* from CPAN sub-package
- Don't try to normalize CPAN-Meta, JSON-PP, and Parse-CPAN-Meta versions;
  their dual-life packages aren't and have much higher numbers already

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-178
- update macros -> add %%perl_bootstrap 1 and example for readability
- add into Module::Build dependency on perl-devel (contains macros.perl)
- create new sub-package macros, because we need macros in minimal buildroot

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-175
- remove from macros BSD, because there exists BSD::Resources

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-174
- remove old MODULE_COMPATs

* Mon Jun 20 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-173
- move ptargrep to Archive-Tar sub-package
- fix version numbers in last two changelog entries

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 4:5.14.1-172
- add provide for perl(:MODULE_COMPAT_5.14.1)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-171
- update to 5.14.1 - no new modules, just serious bugfixes and doc
- switch off fork test, which is failing only on koji

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-170
- try to update to latest ExtUtils::MakeMaker, no luck -> rebuild with current 
  version, fix bug RT#67618 in modules

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-169
- filter even Mac:: requires, polish filter again for correct installation
- add sub-package Compress-Raw-Bzip2, solve Bzip2 conflicts after install
- and add IO::Uncompress::Bunzip2 correctly into IO-Compress

* Mon Jun 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-167
- Perl 5.14 mass rebuild, bump release, remove releases in subpackages

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-165
- Perl 5.14 mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-163
- Perl 5.14 mass rebuild

* Thu Jun  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-162
- add new sub-packages, remove BR in them

* Wed Jun  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-161
- arm can't do parallel builds
- add require EE::MM into IPC::Cmd 711486

* Mon May 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-161
- test build of released 5.14.0
- remove Class::ISA from sub-packages
- patches 8+ are part of new release
- remove vendorarch/auto/Compress/Zlib

* Wed Apr 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-160
- add provides UNIVERSAL and DB back into perl

* Thu Apr 07 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-159
- Remove rpath-make patch because we use --enable-new-dtags linker option

* Fri Apr  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-158
- 692900 - lc launders tainted flag, RT #87336

* Fri Apr  1 2011 Robin Lee <cheeselee@fedoraproject.org> - 4:5.12.3-157
- Cwd.so go to the PathTools sub-package

* Tue Mar 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-156
- sub-package Path-Tools

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 4:5.12.3-154
- sub-package Scalar-List-Utils

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.12.3-153
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-152
- Document ExtUtils::ParseXS upgrade in local patch tracking

* Wed Jan 26 2011 Tom Callaway <spot@fedoraproject.org> - 4:5.12.3-151
- update ExtUtils::ParseXS to 2.2206 (current) to fix Wx build

* Wed Jan 26 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-150
- Make %%global perl_default_filter lazy
- Do not hard-code tapsetdir path

* Tue Jan 25 2011 Lukas Berk <lberk@redhat.com> - 4:5.12.3-149
- added systemtap tapset to make use of systemtap-sdt-devel
- added an example systemtap script

* Mon Jan 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-148
- stable update 5.12.3
- add COMPAT

* Thu Dec  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-146
- 463773 revert change. txt files are needed for example by UCD::Unicode,
 PDF::API2,...

* Thu Dec  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-145
- required systemtap-sdt-devel on request in 661553

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-144
- create sub-package for CGI 3.49

* Tue Nov 09 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-143
- Sub-package perl-Class-ISA (bug #651317)

* Mon Nov 08 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-142
- Make perl(ExtUtils::ParseXS) version 4 digits long (bug #650882)

* Tue Oct 19 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-141
- 643447 fix redefinition of constant C in h2ph (visible in git send mail,
  XML::Twig test suite)
- remove ifdef for s390

* Thu Oct 07 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-140
- Package Test-Simple tests to dual-live with standalone package (bug #640752)
 
* Wed Oct  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-139
- remove removal of NDBM

* Tue Oct 05 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-138
- Consolidate Requires filtering
- Consolidate libperl.so* Provides

* Fri Oct  1 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-137
- filter useless requires, provide libperl.so

* Fri Oct 01 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-136
- Reformat perl-threads description
- Fix threads directories ownership

* Thu Sep 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-135
- sub-package threads

* Thu Sep 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-134
- add vendor path, clean paths in Configure in spec file
- create sub-package threads-shared

* Tue Sep  7 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-133
- Do not leak when destroying thread (RT #77352, RHBZ #630667)

* Tue Sep  7 2010 Petr Sabata <psabata@redhat.com> - 5:5.12.2-132
- Fixing release number for modules

* Tue Sep  7 2010 Petr Sabata <psabata@redhat.com> - 4:5.12.2-1
- Update to 5.12.2
- Removed one hardcoded occurence of perl version in build process
- Added correct path to dtrace binary
- BuildRequires: systemtap-sdt-devel

* Tue Sep  7 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-131
- run Configure with -Dusedtrace for systemtap support

* Wed Aug 18 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.1-130
- Run tests in parallel
- Add "-Wl,--enable-new-dtags" to linker to allow to override perl's rpath by
  LD_LIBRARY_PATH used in tests. Otherwise tested perl would link to old
  in-system libperl.so.
- Normalize spec file indentation

* Mon Jul 26 2010  Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-129
- 617956 move perlxs* docs files into perl-devel

* Thu Jul 15 2010  Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-128
- 614662 wrong perl-suidperl version in obsolete

* Sun Jul 11 2010 Dan Horák <dan[at]danny.cz> - 4:5.12.1-127
- add temporary compat provides needed on s390(x)

* Fri Jul 09 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.1-126
- Add Digest::SHA requirement to perl-CPAN and perl-CPANPLUS (bug #612563)

* Thu Jul  8 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-125
- 607505 add another dir into Module::Build (thanks to Paul Howarth)

* Mon Jun 28 2010 Ralf Corsépius <corsepiu@fedoraproject.org> -  4:5.12.1-124
- Address perl-Compress-Raw directory ownership (BZ 607881).

* Thu Jun 10 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-123
- remove patch with debugging symbols, which should be now ok without it
- update to 5.12.1
- MODULE_COMPAT

* Tue Apr 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-122
- packages in buildroot needs MODULE_COMPAT 5.10.1, add it back for rebuild

* Sun Apr 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-121
- rebuild with tests in test buildroot

* Fri Apr 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-120-test
- MODULE_COMPAT 5.12.0
- remove BR man
- clean configure
- fix provides/requires in IO-Compress

* Wed Apr 14 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-119.1
- rebuild 5.12.0 without MODULE_COMPAT

* Wed Apr 14 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-119
- initial 5.12.0 build

* Tue Apr  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-118
- 463773 remove useless txt files from installation
- 575842 remove PERL_USE_SAFE_PUTENV, use perl putenv

* Tue Mar 16 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-117
- package tests in their own subpackage

* Mon Mar 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-116
- add noarch into correct sub-packages
- move Provides/Obsoletes into correct modules from main perl

* Thu Mar 11 2010 Paul Howarth <paul@city-fan.org> - 4:5.10.1-115
- restore missing version macros for Compress::Raw::Zlib, IO::Compress::Base
  and IO::Compress::Zlib

* Thu Mar 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-114
- clean spec a little more
- rebuild with new gdbm

* Fri Mar  5 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-112
- fix license according to advice from legal
- clean unused patches

* Wed Feb 24 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-111
- update subpackage tests macros to handle packages with an epoch properly

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-110
- add initial EXPERIMENTAL tests subpackage rpm macros to macros.perl

* Tue Dec 22 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-109
- 547656 CVE-2009-3626 perl: regexp matcher crash on invalid UTF-8 characters  
- 549306 version::Internals should be packaged in perl-version subpackage
- Parse-CPAN-Meta updated and separate package is dead

* Mon Dec 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-107
- subpackage parent and Parse-CPAN-Meta; add them to core's dep list

* Fri Dec 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 4:5.10.1-106
- exclude "parent".

* Fri Dec 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 4:5.10.1-105
- exclude Parse-CPAN-Meta.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-104
- do not pack Bzip2 manpages either (#544582)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-103
- do not pack Bzip2 modules (#544582)
- hack: cheat about Compress::Raw::Zlib version (#544582)

* Thu Dec  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-102
- switch off check for ppc64 and s390x
- remove the hack for "make test," it is no longer needed

* Thu Dec  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-101
- be more careful with the libperl.so compatibility symlink (#543936)

* Wed Dec  2 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-100
- new upstream version
- release number must be high, because of stale version numbers of some
  of the subpackages
- drop upstreamed patches
- update the versions of bundled modules
- shorten the paths in @INC
- build without DEBUGGING
- implement compatibility measures for the above two changes, for a short
  transition period
- provide perl(:MODULE_COMPAT_5.10.0), for that transition period only

* Tue Dec  1 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-87
- fix patch-update-Compress-Raw-Zlib.patch (did not patch Zlib.pm)
- update Compress::Raw::Zlib to 2.023
- update IO::Compress::Base, and IO::Compress::Zlib to 2.015 (#542645)

* Mon Nov 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-86
- 542645 update IO-Compress-Base

* Tue Nov 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-85
- back out perl-5.10.0-spamassassin.patch (#528572)

* Thu Oct 01 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-84
- add /perl(UNIVERSAL)/d; /perl(DB)/d to perl_default_filter auto-provides
  filtering

* Thu Oct  1 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-83
- update Storable to 2.21

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-82
- update our Test-Simple update to 0.92 (patch by Iain Arnell), #519417
- update Module-Pluggable to 3.9

* Thu Aug 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-81
- fix macros.perl *sigh*

* Mon Aug 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-80
- Remove -DDEBUGGING=-g, we are not ready yet.

* Fri Aug 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-79
- add helper filtering macros to -devel, for perl-* package invocation
  (#502402)

* Fri Jul 31 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-78
- Add configure option -DDEBUGGING=-g (#156113)

* Tue Jul 28 2009 arcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-77
- 510127 spam assassin suffer from tainted bug

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-76
- 494773 much better swap logic to support reentrancy and fix assert failure (rt #60508)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.10.0-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-74
- fix generated .ph files so that they no longer cause warnings (#509676)
- remove PREREQ_FATAL from Makefile.PL's processed by miniperl
- update to latest Scalar-List-Utils (#507378)
- perl-skip-prereq.patch: skip more prereq declarations in Makefile.PL files

* Tue Jul  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-73
- re-enable tests

* Tue Jul  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-72
- move -DPERL_USE_SAFE_PUTENV to ccflags (#508496)

* Mon Jun  8 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-71
- #504386 update of Compress::Raw::Zlib 2.020

* Thu Jun  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-70
- update File::Spec (PathTools) to 3.30

* Wed Jun  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-69
- fix #221113, $! wrongly set when EOF is reached

* Fri Apr 10 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-68
- do not use quotes in patchlevel.h; it breaks installation from cpan (#495183)

* Tue Apr  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-67
- update CGI to 3.43, dropping upstreamed perl-CGI-escape.patch

* Tue Apr  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-66
- fix CGI::escape for all strings (#472571)
- perl-CGI-t-util-58.patch: Do not distort lib/CGI/t/util-58.t
  http://rt.perl.org/rt3/Ticket/Display.html?id=64502

* Fri Mar 27 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-65
- Move the gargantuan Changes* collection to -devel (#492605)

* Tue Mar 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-64
- update module autodie

* Mon Mar 23 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-63
- update Digest::SHA (fixes 489221)

* Wed Mar 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-62
- drop 26_fix_pod2man_upgrade (don't need it)
- fix typo in %%define ExtUtils_CBuilder_version

* Wed Mar 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-61
- apply Change 34507: Fix memory leak in single-char character class optimization
- Reorder @INC, based on b9ba2fadb18b54e35e5de54f945111a56cbcb249
- fix Archive::Extract to fix test failure caused by tar >= 1.21
- Merge useful Debian patches

* Tue Mar 10 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-60
- remove compatibility obsolete sitelib directories
- use a better BuildRoot
- drop a redundant mkdir in %%install
- call patchlevel.h only once; rm patchlevel.bak
- update modules Sys::Syslog, Module::Load::Conditional, Module::CoreList,
  Test::Harness, Test::Simple, CGI.pm (dropping the upstreamed patch),
  File::Path (that includes our perl-5.10.0-CVE-2008-2827.patch),
  constant, Pod::Simple, Archive::Tar, Archive::Extract, File::Fetch,
  File::Temp, IPC::Cmd, Time::HiRes, Module::Build, ExtUtils::CBuilder
- standardize the patches for updating embedded modules
- work around a bug in Module::Build tests bu setting TMPDIR to a directory
  inside the source tree

* Sun Mar 08 2009 Robert Scheck <robert@fedoraproject.org> - 4:5.10.0-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-58
- add /usr/lib/perl5/site_perl to otherlibs (bz 484053)

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 4:5.10.0-57
- build sparc64 without _smp_mflags

* Sat Feb 07 2009 Dennis Gilmore <dennis@ausil.us> - 4:5.10.0-56
- limit sparc builds to -j12

* Tue Feb  3 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-55
- update IPC::Cmd to v 0.42

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-54
- 455410 http://rt.perl.org/rt3/Public/Bug/Display.html?id=54934
  Attempt to free unreferenced scalar fiddling with the symbol table
  Keep the refcount of the globs generated by PerlIO::via balanced.

* Mon Dec 22 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-53
- add missing XHTML.pm into Pod::Simple

* Fri Dec 12 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-52
- 295021 CVE-2007-4829 perl-Archive-Tar directory traversal flaws
- add another source for binary files, which test untaring links

* Fri Nov 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-51
- to fix Fedora bz 473223, which is really perl bug #54186 (http://rt.perl.org/rt3//Public/Bug/Display.html?id=54186)
  we apply Changes 33640, 33881, 33896, 33897

* Mon Nov 24 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-50
- change summary according to RFC fix summary discussion at fedora-devel :)

* Thu Oct 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-49
- update File::Temp to 0.20

* Sun Oct 12 2008 Lubomir Rintel <lkundrak@v3.sk> - 4:5.10.0-48
- Include fix for rt#52740 to fix a crash when using Devel::Symdump and
  Compress::Zlib together

* Tue Oct 07 2008 Marcela Mašláňová <mmaslano@redhat.com> 4:5.10.0-47.fc10
- rt#33242, rhbz#459918. Segfault after reblessing objects in Storable.
- rhbz#465728 upgrade Simple::Pod to 3.07

* Wed Oct  1 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-46
- also preserve the timestamp of AUTHORS; move the fix to the recode
  function, which is where the stamps go wrong

* Wed Oct  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-45
- give Changes*.gz the same datetime to avoid multilib conflict

* Wed Sep 17 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-44.fc10
- remove Tar.pm from Archive-Extract
- fix version of Test::Simple in spec
- update Test::Simple
- update Archive::Tar to 1.38

* Tue Sep 16 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-43.fc10
- 462444 update Test::Simple to 0.80

* Thu Aug 14 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-42.fc10
- move libnet to the right directory, along Net/Config.pm

* Wed Aug 13 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-41.fc10
- do not create directory .../%%{version}/auto

* Tue Aug  5 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-40.fc10
- 457867 remove required IPC::Run from CPANPLUS - needed only by win32
- 457771 add path

* Fri Aug  1 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-39.fc10
- CGI.pm bug in exists() on tied param hash (#457085)
- move the enc2xs templates (../Encode/*.e2x) to -devel, (#456534)

* Mon Jul 21 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-38
- 455933 update to CGI-3.38
- fix fuzz problems (patch6)
- 217833 pos() function handle unicode characters correct

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-36
- rebuild for new db4 4.7

* Wed Jul  9 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-35
- remove db4 require, it is handled automatically

* Thu Jul  3 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-34
- 453646 use -DPERL_USE_SAFE_PUTENV. Without fail some modules f.e. readline.

* Tue Jul  1 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-33
- 451078 update Test::Harness to 3.12 for more testing. Removed verbose 
test, new Test::Harness has possibly verbose output, but updated package
has a lot of features f.e. TAP::Harness. Carefully watched all new bugs 
related to tests!

* Fri Jun 27 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-32
- bump the release number, so that it is not smaller than in F-9

* Tue Jun 24 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-28
- CVE-2008-2827 perl: insecure use of chmod in rmtree

* Wed Jun 11 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-27
- 447371 wrong access permission rt49003

* Tue Jun 10 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-26
- make config parameter list consistent for 32bit and 64bit platforms,
  add config option -Dinc_version_list=none (#448735)
- use perl_archname consistently
- cleanup of usage of *_lib macros in %%install

* Fri Jun  6 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-25
- 449577 rebuild for FTBFS

* Mon May 26 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-24
- 448392 upstream fix for assertion

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-23
- sparc64 breaks with the rpath hack patch applied

* Mon May 19 2008 Marcela Maslanova <mmaslano@redhat.com>
- 447142 upgrade CGI to 3.37 (this actually happened in -21 in rawhide.)

* Sat May 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-21
- sparc64 fails two tests under mysterious circumstances. we need to get the
  rest of the tree moving, so we temporarily disable the tests on that arch.

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-20
- create the vendor_perl/%%{perl_version}/%%{perl_archname}/auto directory 
  in %%{_libdir} so we own it properly

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-19
- fix CPANPLUS-Dist-Build Provides/Obsoletes (bz 437615)
- bump version on Module-CoreList subpackage

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-18
- forgot to create the auto directory for multilib vendor_perl dirs

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-17
- own multilib vendor_perl directories
- mark Module::CoreList patch in patchlevel.h

* Tue Mar 18 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-16
- 437817: RFE: Upgrade Module::CoreList to 2.14

* Wed Mar 12 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-15
- xsubpp now lives in perl-devel instead of perl.

* Sat Mar  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-14
- back out Archive::Extract patch, causing odd test failure

* Sat Mar  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-13
- add missing lzma test file

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-12
- conditionalize multilib patch report in patchlevel.h
- Update Archive::Extract to 0.26
- Update Module::Load::Conditional to 0.24

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-11
- only do it once, and do it for all our patches

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-10
- note 32891 in patchlevel.h

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-9
- get rid of bad conflicts on perl-File-Temp

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-8
- use /usr/local for sitelib/sitearch dirs
- patch 32891 for significant performance improvement

* Fri Feb 22 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-7
- Add perl-File-Temp provides/obsoletes/conflicts (#433836),
  reported by Bill McGonigle <bill@bfccomputing.com>
- escape the macros in Jan 30 entry

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4:5.10.0-6
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-5
- disable some futime tests in t/io/fs.t because they started failing on x86_64
  in the Fedora builders, and no one can figure out why. :/

* Wed Jan 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-4
- create %%{_prefix}/lib/perl5/vendor_perl/%%{perl_version}/auto and own it
  in base perl (resolves bugzilla 214580)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-3
- Update Sys::Syslog to 0.24, to fix test failures

* Wed Jan 9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-2
- add some BR for tests

* Tue Jan 8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-1
- 5.10.0 final
- clear out all the unnecessary patches (down to 8 patches!)
- get rid of super perl debugging mode
- add new subpackages

* Thu Nov 29 2007 Robin Norwood <rnorwood@redhat.com> - 4:5.10.0_RC2-0.1
- first attempt at building 5.10.0


