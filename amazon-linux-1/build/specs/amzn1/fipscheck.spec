%define _buildid .13

Summary:	A library for integrity verification of FIPS validated modules
Name:		fipscheck
Version:	1.3.1
Release: 3%{?_buildid}%{?dist}
License:	BSD
Group:		System Environment/Libraries
# This is a Red Hat maintained package which is specific to
# our distribution.
URL:            http://fedorahosted.org/fipscheck/
Source0:        http://fedorahosted.org/releases/f/i/%{name}/%{name}-%{version}.tar.bz2

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: 	openssl-devel >= 0.9.8j

%description
FIPSCheck is a library for integrity verification of FIPS validated
modules. The package also provides helper binaries for creation and
verification of the HMAC-SHA256 checksum files.

%package lib
Summary:        Library files for %{name}
Group:          System Environment/Libraries

Requires:       %{_bindir}/fipscheck
Obsoletes:      %{name} < 1.2.0-1
Conflicts:      %{name} < 1.2.0-1

%description lib
This package contains the FIPSCheck library.

%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries

Requires:       %{name}-lib = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags}

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    $RPM_BUILD_ROOT%{_bindir}/fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/fipscheck $RPM_BUILD_ROOT%{_libdir}/libfipscheck.so.1.1.0 \
    ln -s libfipscheck.so.1.1.0.hmac $RPM_BUILD_ROOT%{_libdir}/fipscheck/libfipscheck.so.1.hmac \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

mkdir -p $RPM_BUILD_ROOT%{_libdir}/fipscheck

%clean
rm -rf $RPM_BUILD_ROOT

%post lib -p /sbin/ldconfig


%postun lib -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS
%{_bindir}/fipscheck
%{_bindir}/fipshmac
%{_libdir}/fipscheck/fipscheck.hmac
%{_mandir}/man8/*

%files lib
%defattr(-,root,root,-)
%{_libdir}/libfipscheck.so.*
%dir %{_libdir}/fipscheck
%{_libdir}/fipscheck/libfipscheck.so.*.hmac

%files devel
%defattr(-,root,root,-)
%{_includedir}/fipscheck.h
%{_libdir}/libfipscheck.so
%{_mandir}/man3/*

%changelog
* Wed Oct 30 2013 Lee Trager <ltrager@amazon.com>
- import source package F19/fipscheck-1.3.1-3.fc19

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 7 2012 Lee Trager <ltrager@amazon.com>
- import source package F17/fipscheck-1.3.0-3.fc17

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Tomas Mraz - 1.3.1-1
- manual pages added by Paul Wouters

* Thu Dec 8 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/fipscheck-1.2.0-7.el6

* Sat May 21 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/fipscheck-1.2.0-5.el6

* Mon Dec 20 2010 Ben Howard <behoward@amazon.com>
- Incrementing the version to allow for build

* Tue Sep  7 2010 Tomas Mraz - 1.3.0-1
- look up the hmac files in the _libdir/fipscheck first

* Tue Jul 13 2010 Cristian Gafton <gafton@amazon.com>
- rebuild

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/fipscheck-1.2.0-4.1.el6

* Fri May 7 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/fipscheck-1.2.0-1.el5
- import source package RHEL5/fipscheck-1.0.3-1.el5
- added submodule prep for package fipscheck

* Tue May 26 2009 Tomas Mraz - 1.2.0-1
- add lib subpackage to avoid multilib on the base package
- add ability to compute hmacs on multiple files at once
- improved debugging with FIPSCHECK_DEBUG

* Thu Mar 19 2009 Tomas Mraz - 1.1.1-1
- move binaries and libraries to /usr

* Wed Mar 18 2009 Tomas Mraz - 1.1.0-1
- hmac check itself as required by FIPS

* Mon Feb  9 2009 Tomas Mraz - 1.0.4-1
- add some docs to the README, require current openssl in Fedora

* Fri Oct 24 2008 Tomas Mraz - 1.0.3-1
- use OpenSSL in FIPS mode to do the HMAC checksum instead of NSS

* Tue Sep  9 2008 Tomas Mraz - 1.0.2-1
- fix test for prelink

* Mon Sep  8 2008 Tomas Mraz - 1.0.1-1
- put binaries in /bin and libraries in /lib as fipscheck
  will be used by modules in /lib

* Mon Sep  8 2008 Tomas Mraz - 1.0.0-2
- minor fixes for package review

* Wed Sep  3 2008 Tomas Mraz - 1.0.0-1
- Initial spec file
