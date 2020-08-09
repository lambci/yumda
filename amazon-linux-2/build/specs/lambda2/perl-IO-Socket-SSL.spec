Name:           perl-IO-Socket-SSL
Version:        1.94
Release: 7%{?dist}.0.1
Summary:        Perl library for transparent SSL
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/IO-Socket-SSL/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-%{version}.tar.gz
# Correct error reporting, fixed in 1.953, CPAN RT#87052
Patch0:         IO-Socket-SSL-1.94-1.953-RT-87052-fix-in-Utils.pm.patch
# Respect OpenSSL default ciphers and protocol versions BZ#1127322
Patch1:         IO-Socket-SSL-1.94-Respect-OpenSSL-default-ciphers-and-protocol-versions.patch
# Fix typo in Utils.pm BZ#1097710
Patch2:         IO-Socket-SSL-1.94-Fix-typo-key-free.patch
# Add support for ECDH key exchange, in upstream 1.955, bug #1316377
Patch3:         IO-Socket-SSL-1.94-Added-support-for-ECDH-key-exchange-with-key-SSL_ecd.patch
# Add support for handshake protocol TLSv11, TLSv12, bug #1335035,
# in upstream 1.955
Patch4:         IO-Socket-SSL-1.94-support-for-handshake-protocol-TLSv11-TLSv12.patch
# The new syntax for the protocols is TLSv1_1 instead of TLSv11, bug #1335035,
# in upstream 1.966
Patch5:         IO-Socket-SSL-1.94-The-new-syntax-for-the-protocols-is-TLSv1_1-instead-.patch
# Default to system wide CA certificate store, bug #1402588, in upstream 1.968
Patch6:         IO-Socket-SSL-1.94-Default-SSL_ca_file-to-system-wide-store.patch
BuildArch:      noarch
BuildRequires:  openssl >= 0.9.8
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.46
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(IO::Socket::INET)
#BuildRequires: perl(IO::Socket::INET6) ????
BuildRequires:  perl(IO::Socket::IP) >= 0.20
# Mozilla::CA not used at tests
BuildRequires:  perl(Net::LibIDN)
BuildRequires:  perl(Net::SSLeay) >= 1.46
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket) >= 1.9
BuildRequires:  perl(Socket6)
BuildRequires:  perl(strict)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  procps
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(IO::Socket::IP) >= 0.20
Requires:       perl(Socket) >= 1.95
Requires:       perl(Mozilla::CA)
Requires:       perl(Net::LibIDN)
Requires:       perl-Net-SSLeay >= 1.55-5
Requires:       openssl >= 0.9.8

Prefix: %{_prefix}

%description
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

%prep
%setup -q -n IO-Socket-SSL-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}

%files
%license README
%{perl_vendorlib}/IO/

%exclude %{_mandir}

%changelog
* Sun Aug 9 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Aug 30 2017 Petr Pisar <ppisar@redhat.com> - 1.94-7
- Default to system wide CA certificate store (bug #1402588)

* Thu Oct 06 2016 Petr Pisar <ppisar@redhat.com> - 1.94-6
- Add support for TLSv1.1, TLSv1.2 (bug #1335035)

* Thu Mar 10 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.94-5
- Add support for ECDH key exchange (bug #1316377)

* Fri Mar 04 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.94-4
- Respect OpenSSL default ciphers and protocol versions (bug #1127322)
- Fix typo in Utils.pm (bug #1097710)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.94-3
- Mass rebuild 2013-12-27

* Wed Aug 07 2013 Petr Šabata <contyk@redhat.com> - 1.94-2.1
- Extend the dependency list and remove not needed conditionals
- Modernize the spec

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.94-2
- Correct error reporting (CPAN RT#87052)

* Sat Jun  1 2013 Paul Howarth <paul@city-fan.org> - 1.94-1
- Update to 1.94
  - Makefile.PL reported wrong version of openssl if Net::SSLeay was not
    installed, instead of reporting a missing dependency of Net::SSLeay

* Fri May 31 2013 Paul Howarth <paul@city-fan.org> - 1.93-1
- Update to 1.93
  - Need at least OpenSSL version 0.9.8 now, since last 0.9.7 was released 6
    years ago; remove code to work around older releases
  - Changed AUTHOR in Makefile.PL from array back to string, because the array
    feature is not available in MakeMaker shipped with 5.8.9 (CPAN RT#85739)
- Set openssl version requirement to 0.9.8
- Drop ExtUtils::MakeMaker version requirement back to 6.46

* Thu May 30 2013 Paul Howarth <paul@city-fan.org> - 1.92-1
- Update to 1.92
  - Intercept: use sha1-fingerprint of original cert for id into cache unless
    otherwise given
  - Fix pod error in IO::Socket::SSL::Utils (CPAN RT#85733)

* Thu May 30 2013 Paul Howarth <paul@city-fan.org> - 1.91-1
- Update to 1.91
  - Added IO::Socket::SSL::Utils for easier manipulation of certificates and
    keys
  - Moved SSL interception into IO::Socket::SSL::Intercept and simplified it
    using IO::Socket::SSL::Utils
  - Enhance meta information in Makefile.PL
- Bump openssl version requirement to 0.9.8a
- Need at least version 6.58 of ExtUtils::MakeMaker (CPAN RT#85739)

* Wed May 29 2013 Paul Howarth <paul@city-fan.org> - 1.90-1
- Update to 1.90
  - Support more digests, especially SHA-2 (CPAN RT#85290)
  - Added support for easy SSL interception (man in the middle) based on ideas
    found in mojo-mitm proxy
  - Make 1.46 the minimal required version for Net::SSLeay, because it
    introduced lots of useful functions
- BR:/R: openssl ≥ 0.9.7e for P_ASN1_TIME_(get,set)_isotime in Net::SSLeay

* Tue May 14 2013 Paul Howarth <paul@city-fan.org> - 1.89-1
- Update to 1.89
  - If IO::Socket::IP is used it should be at least version 0.20; otherwise we
    get problems with HTTP::Daemon::SSL and maybe others (CPAN RT#81932)
  - Spelling corrections

* Thu May  2 2013 Paul Howarth <paul@city-fan.org> - 1.88-1
- Update to 1.88
  - Consider a value of '' the same as undef for SSL_ca_(path|file), SSL_key*
    and SSL_cert* - some apps like Net::LDAP use it that way

* Wed Apr 24 2013 Paul Howarth <paul@city-fan.org> - 1.87-1
- Update to 1.87
  - Complain if given SSL_(key|cert|ca)_(file|path) do not exist or if they are
    not readable (CPAN RT#84829)
  - Fix use of SSL_key|SSL_file objects instead of files, broken with 1.83

* Wed Apr 17 2013 Paul Howarth <paul@city-fan.org> - 1.86-1
- Update to 1.86
  - Don't warn about SSL_verify_mode when re-using an existing SSL context
    (CPAN RT#84686)

* Mon Apr 15 2013 Paul Howarth <paul@city-fan.org> - 1.85-1
- Update to 1.85
  - Probe for available modules with local __DIE__ and __WARN__handlers
    (CPAN RT#84574)
  - Fix warning, when IO::Socket::IP is installed and inet6 support gets
    explicitly requested (CPAN RT#84619)

* Sat Feb 16 2013 Paul Howarth <paul@city-fan.org> - 1.84-1
- Update to 1.84
  - Disabled client side SNI for openssl version < 1.0.0 because of
    CPAN RT#83289
  - Added functions can_client_sni, can_server_sni and can_npn to check
    availability of SNI and NPN features
  - Added more documentation for SNI and NPN

* Thu Feb 14 2013 Paul Howarth <paul@city-fan.org> - 1.83-2
- Update to 1.831
  - Separated documentation of non-blocking I/O from error handling
  - Changed and documented behavior of readline to return the read data on
    EAGAIN/EWOULDBLOCK in case of non-blocking socket
    (see https://github.com/noxxi/p5-io-socket-ssl/issues/1)
- Bumped release rather than version number to preserve likely upgrade path
  and avoid need for epoch or version number ugliness; may revisit this in
  light of upstream's future version numbering decisions

* Mon Feb  4 2013 Paul Howarth <paul@city-fan.org> - 1.83-1
- Update to 1.83
  - Server Name Indication (SNI) support on the server side (CPAN RT#82761)
  - Reworked part of the documentation, like providing better examples

* Mon Jan 28 2013 Paul Howarth <paul@city-fan.org> - 1.82-1
- Update to 1.82
  - sub error sets $SSL_ERROR etc. only if there really is an error; otherwise
    it will keep the latest error, which allows IO::Socket::SSL->new to report
    the correct problem, even if the problem is deeper in the code (like in
    connect)
  - Correct spelling (CPAN RT#82790)

* Thu Dec  6 2012 Paul Howarth <paul@city-fan.org> - 1.81-1
- Update to 1.81
  - Deprecated set_ctx_defaults; new name is set_defaults (the old name is
    still available)
  - Changed handling of default path for SSL_(ca|cert|key)* keys: if one of
    these keys is user defined, don't add defaults for the others, i.e.
    don't mix user settings and defaults
  - Cleaner handling of module defaults vs. global settings vs. socket
    specific settings; global and socket specific settings are both provided
    by the user, while module defaults are not
  - Make IO::Socket::INET6 and IO::Socket::IP specific tests both run, even
    if both modules are installed, by faking a failed load of the other module
- BR: perl(IO::Socket::INET6) and perl(Socket6) unconditionally

* Fri Nov 30 2012 Paul Howarth <paul@city-fan.org> - 1.80-1
- Update to 1.80
  - Removed some warnings in test (missing SSL_verify_mode => 0), which caused
    tests to hang on Windows (CPAN RT#81493)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 1.79-1
- Update to 1.79
  - Use getnameinfo instead of unpack_sockaddr_in6 to get PeerAddr and PeerPort
    from sockaddr in _update_peer, because this provides scope too
  - Work around systems that don't define AF_INET6 (CPAN RT#81216)
  - Prepare transition to a more secure default for SSL_verify_mode; the use of
    the current default SSL_VERIFY_NONE will cause a big warning for clients,
    unless SSL_verify_mode was explicitly set inside the application to this
    insecure value (in the near future the default will be SSL_VERIFY_PEER, and
    thus causing verification failures in unchanged applications)

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 1.77-2
- Added some missing build dependencies

* Fri Oct  5 2012 Paul Howarth <paul@city-fan.org> - 1.77-1
- Update to 1.77
  - support _update_peer for IPv6 too (CPAN RT#79916)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.76-2
- Perl 5.16 rebuild

* Mon Jun 18 2012 Paul Howarth <paul@city-fan.org> - 1.76-1
- Update to 1.76
  - add support for IO::Socket::IP, which supports inet6 and inet4
    (CPAN RT#75218)
  - fix documentation errors (CPAN RT#77690)
  - made it possible to explicitly disable TLSv11 and TLSv12 in SSL_version
  - use inet_pton from either Socket.pm 1.95 or Socket6.pm
- Use IO::Socket::IP for IPv6 support where available, else IO::Socket::INET6
- Add runtime dependency for appropriate IPv6 support module so that we can
  ensure that we run at runtime what we tested with at build time

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.74-2
- Perl 5.16 rebuild

* Mon May 14 2012 Paul Howarth <paul@city-fan.org> - 1.74-1
- Update to 1.74
  - accept a version of SSLv2/3 as SSLv23, because older documentation could
    be interpreted like this

* Fri May 11 2012 Paul Howarth <paul@city-fan.org> - 1.73-1
- Update to 1.73
  - set DEFAULT_CIPHER_LIST to ALL:!LOW instead of HIGH:!LOW
  - make test t/dhe.t hopefully work with more versions of openssl

* Wed May  9 2012 Paul Howarth <paul@city-fan.org> - 1.71-1
- Update to 1.71
  - 1.70 done right: don't disable SSLv2 ciphers; SSLv2 support is better
    disabled by the default SSL_version of 'SSLv23:!SSLv2'

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 1.70-1
- Update to 1.70
  - make it possible to disable protocols using SSL_version, and make
    SSL_version default to 'SSLv23:!SSLv2'

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 1.69-1
- Update to 1.69 (changes for CPAN RT#76929)
  - if no explicit cipher list is given, default to ALL:!LOW instead of the
    openssl default, which usually includes weak ciphers like DES
  - new config key SSL_honor_cipher_order and document how to use it to fight
    BEAST attack
  - fix behavior for empty cipher list (use default)
  - re-added workaround in t/dhe.t

* Mon Apr 16 2012 Paul Howarth <paul@city-fan.org> - 1.66-1
- Update to 1.66
  - make it thread safer (CPAN RT#76538)

* Mon Apr 16 2012 Paul Howarth <paul@city-fan.org> - 1.65-1
- Update to 1.65
  - added NPN (Next Protocol Negotiation) support (CPAN RT#76223)

* Sat Apr  7 2012 Paul Howarth <paul@city-fan.org> - 1.64-1
- Update to 1.64
  - ignore die from within eval to make tests more stable on Win32
    (CPAN RT#76147)
  - clarify some behavior regarding hostname verification
- Drop patch for t/dhe.t, no longer needed

* Wed Mar 28 2012 Paul Howarth <paul@city-fan.org> - 1.62-1
- Update to 1.62
  - small fix to last version

* Tue Mar 27 2012 Paul Howarth <paul@city-fan.org> - 1.61-1
- Update to 1.61
  - call CTX_set_session_id_context so that server's session caching works with
    client certificates too (CPAN RT#76053)

* Tue Mar 20 2012 Paul Howarth <paul@city-fan.org> - 1.60-1
- Update to 1.60
  - don't make blocking readline if socket was set nonblocking, but return as
    soon no more data are available (CPAN RT#75910)
  - fix BUG section about threading so that it shows package as thread safe
    as long as Net::SSLeay ≥ 1.43 is used (CPAN RT#75749)
- BR: perl(constant), perl(Exporter) and perl(IO::Socket)

* Thu Mar  8 2012 Paul Howarth <paul@city-fan.org> - 1.59-1
- Update to 1.59
  - if SSLv2 is not supported by Net::SSLeay set SSL_ERROR with useful message
    when attempting to use it
  - modify constant declarations so that 5.6.1 should work again
- Drop %%defattr, redundant since rpm 4.4

* Mon Feb 27 2012 Paul Howarth <paul@city-fan.org> - 1.58-1
- Update to 1.58
  - fix t/dhe.t for openssl 1.0.1 beta by forcing TLSv1, so that it does not
    complain about the too small RSA key, which it should not use anyway; this
    workaround is not applied for older openssl versions, where it would cause
    failures (CPAN RT#75165)
- Add patch to fiddle the openssl version number in the t/dhe.t workaround
  because the OPENSSL_VERSION_NUMBER cannot be trusted in Fedora
- One buildreq per line for readability
- Drop redundant buildreq perl(Test::Simple)
- Always run full test suite

* Wed Feb 22 2012 Paul Howarth <paul@city-fan.org> - 1.56-1
- Update to 1.56
  - add automatic or explicit (via SSL_hostname) SNI support, needed for
    multiple SSL hostnames with the same IP (currently only supported for the
    client)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- No need to delete empty directories from buildroot

* Mon Feb 20 2012 Paul Howarth <paul@city-fan.org> - 1.55-1
- Update to 1.55
  - work around IO::Socket's work around for systems returning EISCONN etc. on
    connect retry for non-blocking sockets by clearing $! if SUPER::connect
    returned true (CPAN RT#75101)

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 1.54-1
- Update to 1.54
  - return 0 instead of undef in SSL_verify_callback to fix uninitialized
    warnings (CPAN RT#73629)

* Mon Dec 12 2011 Paul Howarth <paul@city-fan.org> - 1.53-1
- Update to 1.53
  - kill child in t/memleak_bad_handshake.t if test fails (CPAN RT#73146)

* Wed Dec  7 2011 Paul Howarth <paul@city-fan.org> - 1.52-1
- Update to 1.52
  - fix for t/nonblock.t hangs on AIX (CPAN RT#72305)
  - disable t/memleak_bad_handshake.t on AIX, because it might hang
    (CPAN RT#72170)
  - fix syntax error in t/memleak_bad_handshake.t

* Fri Oct 28 2011 Paul Howarth <paul@city-fan.org> - 1.49-1
- Update to 1.49
  - another regression for readline fix: this time it failed to return lines
    at EOF that don't end with newline - extended t/readline.t to catch this
    case and the fix for 1.48

* Wed Oct 26 2011 Paul Howarth <paul@city-fan.org> - 1.48-1
- Update to 1.48
  - further fix for readline fix in 1.45: if the pending data were false (like
    '0'), it failed to read the rest of the line (CPAN RT#71953)

* Fri Oct 21 2011 Paul Howarth <paul@city-fan.org> - 1.47-1
- Update to 1.47
  - fix for 1.46 - check for mswin32 needs to be /i

* Tue Oct 18 2011 Paul Howarth <paul@city-fan.org> - 1.46-1
- Update to 1.46
  - skip signals test on Windows

* Thu Oct 13 2011 Paul Howarth <paul@city-fan.org> - 1.45-1
- Update to 1.45
  - fix readline to continue when getting interrupt waiting for more data
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.44-2
- Perl mass rebuild

* Fri May 27 2011 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - fix invalid call to inet_pton in verify_hostname_of_cert when identity
    should be verified as ipv6 address because it contains a colon

* Wed May 11 2011 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  - add SSL_create_ctx_callback to have a way to adjust context on creation
    (CPAN RT#67799)
  - describe problem of fake memory leak because of big session cache and how
    to fix it (CPAN RT#68073)
  - fix t/nonblock.t
  - stability improvements for t/inet6.t

* Tue May 10 2011 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - fix issue in stop_SSL where it did not issue a shutdown of the SSL
    connection if it first received the shutdown from the other side
  - try to make t/nonblock.t more reliable, at least report the real cause of
    SSL connection errors
- No longer need to re-code docs to UTF-8

* Mon May  2 2011 Paul Howarth <paul@city-fan.org> - 1.40-1
- Update to 1.40
  - fix in example/async_https_server
  - get IDN support from URI (CPAN RT#67676)
- Nobody else likes macros for commands

* Thu Mar  3 2011 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  - fixed documentation of http verification: wildcards in cn is allowed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - fixed wildcards_in_cn setting for http, wrongly set in 1.34 to 1 instead of
    anywhere (CPAN RT#64864)

* Fri Dec 10 2010 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  - don't complain about invalid certificate locations if user explicitly set
    SSL_ca_path and SSL_ca_file to undef: assume that user knows what they are
    doing and will work around the problems themselves (CPAN RT#63741)

* Thu Dec  9 2010 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
  - update documentation for SSL_verify_callback based on CPAN RT#63743 and
    CPAN RT#63740

* Mon Dec  6 2010 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35 (addresses CVE-2010-4334)
  - if verify_mode is not VERIFY_NONE and the ca_file/ca_path cannot be
    verified as valid, it will no longer fall back to VERIFY_NONE but throw an
    error (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=606058)

* Tue Nov  2 2010 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - schema http for certificate verification changed to wildcards_in_cn=1
  - if upgrading socket from inet to ssl fails due to handshake problems, the
    socket gets downgraded back again but is still open (CPAN RT#61466)
  - deprecate kill_socket: just use close()

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.33-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Paul Howarth <paul@city-fan.org> - 1.33-1
- Update to 1.33
  - attempt to make t/memleak_bad_handshake.t more stable
  - fix hostname checking: only check an IP against subjectAltName GEN_IPADD

* Tue Feb 23 2010 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32 (die in Makefile.PL if Scalar::Util has no dualvar support)
- Use %%{_fixperms} macro instead of our own %%{__chmod} incantation

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.31-2
- Rebuild against perl 5.10.1

* Sun Sep 27 2009 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31 (see Changes for details)

* Thu Aug 20 2009 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30 (fix memleak when SSL handshake failed)
- Add buildreq procps needed for memleak test

* Mon Jul 27 2009 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - various regex fixes for i18n and service names
  - fix warnings from perl -w (CPAN RT#48131)
  - improve handling of errors from Net::ssl_write_all

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul  4 2009 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26 (verify_hostname_of_cert matched only the prefix for the
  hostname when no wildcard was given, e.g. www.example.org matched against a
  certificate with name www.exam in it [#509819])

* Fri Jul  3 2009 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25 (fix t/nonblock.t for OS X 10.5 - CPAN RT#47240)

* Thu Apr  2 2009 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24 (add verify hostname scheme ftp, same as http)

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23 (complain when no certificates are provided)

* Sat Jan 24 2009 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to latest upstream version: 1.22

* Thu Jan 22 2009 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to latest upstream version: 1.20

* Tue Nov 18 2008 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to latest upstream version: 1.18
- BR: perl(IO::Socket::INET6) for extra test coverage

* Mon Oct 13 2008 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to latest upstream version: 1.17

* Mon Sep 22 2008 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to latest upstream version: 1.16

* Sat Aug 30 2008 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to latest upstream version: 1.15
- Add buildreq and req for perl(Net::LibIDN) to avoid croaking when trying to
  verify an international name against a certificate

* Wed Jul 16 2008 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to latest upstream version: 1.14
- BuildRequire perl(Net::SSLeay) >= 1.21

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-4
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-3
- Rebuild for new perl

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.12-2
- Cosmetic spec changes suiting new maintainer's preferences

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.12-1
- Update to latest upstream version: 1.12
- Fix license tag
- Add BuildRequires for ExtUtils::MakeMaker and Test::Simple
- Fix package review issues:
- Source URL
- Resolves: bz#226264

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-1.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.02-1
- Upgrade to latest CPAN version: 1.02

* Mon Sep 18 2006 Warren Togami <wtogami@redhat.com> - 1.01-1
- 1.01 bug fixes (#206782)

* Sun Aug 13 2006 Warren Togami <wtogami@redhat.com> - 0.998-1
- 0.998 with more important fixes

* Tue Aug 01 2006 Warren Togami <wtogami@redhat.com> - 0.994-1
- 0.994 important bugfixes (#200860)

* Tue Jul 18 2006 Warren Togami <wtogami@redhat.com> - 0.991-1
- 0.991

* Wed Jul 12 2006 Warren Togami <wtogami@redhat.com> - 0.97-3
- Import into FC6

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-2
- Rebuild for FC5 (perl 5.8.8).
- Rebuild switch: "--with sessiontests".

* Mon Jul 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.97-1
- 0.97.
- Convert docs to UTF-8, drop some unuseful ones.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.96-4
- Rebuilt

* Tue Oct 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-3
- Disable session test suite even if Net::SSLeay >= 1.26 is available.

* Wed Jul  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.2
- Bring up to date with current fedora.us Perl spec template.
- Include examples in docs.

* Sat May  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- Update to 0.96.
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).

* Fri Oct 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.95-0.fdr.1
- First build.
