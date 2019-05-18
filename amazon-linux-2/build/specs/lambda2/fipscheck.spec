Summary:	A library for integrity verification of FIPS validated modules
Name:		fipscheck
Version:	1.4.1
Release: 6%{?dist}.0.2
License:	BSD
Group:		System Environment/Libraries
# This is a Red Hat maintained package which is specific to
# our distribution.
URL:		http://fedorahosted.org/fipscheck/
Source0:	http://fedorahosted.org/releases/f/i/%{name}/%{name}-%{version}.tar.bz2
# Prelink blacklist
Source1:	fipscheck.conf

Patch1:		fipscheck-1.4.1-empty-hmac.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: 	openssl-devel >= 0.9.8j

Requires:      %{name}-lib%{?_isa} = %{version}-%{release}

Prefix: %{_prefix}

%description
FIPSCheck is a library for integrity verification of FIPS validated
modules. The package also provides helper binaries for creation and
verification of the HMAC-SHA256 checksum files.

%package lib
Summary:	Library files for %{name}
Group:		System Environment/Libraries

Requires:	%{_bindir}/fipscheck

Prefix: %{_prefix}

%description lib
This package contains the FIPSCheck library.

%prep
%setup -q
%patch1 -p1 -b .empty-hmac

%build
%configure --disable-static

make %{?_smp_mflags}

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    $RPM_BUILD_ROOT%{_bindir}/fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/fipscheck $RPM_BUILD_ROOT%{_libdir}/libfipscheck.so.1.2.1 \
    ln -s libfipscheck.so.1.2.1.hmac $RPM_BUILD_ROOT%{_libdir}/fipscheck/libfipscheck.so.1.hmac \
%{nil}

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/fipscheck

# Prelink blacklist
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d
install -m644 %{SOURCE1} \
	$RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/fipscheck.conf

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/fipscheck
%{_bindir}/fipshmac
%{_libdir}/fipscheck/fipscheck.hmac

%files lib
%defattr(-,root,root,-)
%{_libdir}/libfipscheck.so.*
%dir %{_libdir}/fipscheck
%{_libdir}/fipscheck/libfipscheck.so.*.hmac
%dir %{_sysconfdir}/prelink.conf.d
%{_sysconfdir}/prelink.conf.d/fipscheck.conf

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Feb 21 2017 Tomáš Mráz <tmraz@redhat.com> - 1.4.1-6
- handle empty hmac file as checksum mismatch

* Mon Feb 10 2014 Tomáš Mráz <tmraz@redhat.com> - 1.4.1-5
- fix the library path in prelink blacklist

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.4.1-4
- Mass rebuild 2014-01-24

* Mon Jan 13 2014 Tomáš Mráz <tmraz@redhat.com> - 1.4.1-3
- add versioned dependency to -lib on base package (#1010349)
- add prelink blacklist

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4.1-2
- Mass rebuild 2013-12-27

* Tue Sep 10 2013 Tomáš Mráz <tmraz@redhat.com> - 1.4.1-1
- fix inverted condition in FIPSCHECK_verify_ex()

* Fri Sep  6 2013 Tomáš Mráz <tmraz@redhat.com> - 1.4.0-1
- added new API calls to support setting hmac suffix

* Mon Apr 16 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.1-1
- manual pages added by Paul Wouters

* Tue Sep  7 2010 Tomas Mraz <tmraz@redhat.com> - 1.3.0-1
- look up the hmac files in the _libdir/fipscheck first

* Tue May 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.0-1
- add lib subpackage to avoid multilib on the base package
- add ability to compute hmacs on multiple files at once
- improved debugging with FIPSCHECK_DEBUG

* Thu Mar 19 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.1-1
- move binaries and libraries to /usr

* Wed Mar 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.0-1
- hmac check itself as required by FIPS

* Mon Feb  9 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.4-1
- add some docs to the README, require current openssl in Fedora

* Fri Oct 24 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.3-1
- use OpenSSL in FIPS mode to do the HMAC checksum instead of NSS

* Tue Sep  9 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.2-1
- fix test for prelink

* Mon Sep  8 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.1-1
- put binaries in /bin and libraries in /lib as fipscheck
  will be used by modules in /lib

* Mon Sep  8 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.0-2
- minor fixes for package review

* Wed Sep  3 2008 Tomas Mraz <tmraz@redhat.com> - 1.0.0-1
- Initial spec file
