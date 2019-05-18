Name:           nettle
Version:        2.7.1
Release: 8%{?dist}.0.2
Summary:        A low-level cryptographic library

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
Source0:	%{name}-%{version}-hobbled.tar.gz
#Source0:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz
Patch0:		nettle-2.7.1-remove-ecc-testsuite.patch
Patch1:		nettle-2.7.1-tmpalloc.patch
Patch2:		nettle-2.7.1-sha3-fix.patch
Patch3:		nettle-2.7.1-ecc-cve.patch
Patch4:		nettle-2.7.1-powm-sec.patch

BuildRequires:  gmp-devel m4 texinfo-tex texlive-dvips ghostscript
BuildRequires:  fipscheck
BuildRequires:	libtool, automake, autoconf, texinfo

Prefix: %{_prefix}

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%prep
%setup -q
# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure
sed 's/ecc-192.c//g' -i Makefile.in
sed 's/ecc-224.c//g' -i Makefile.in
%patch0 -p1
%patch1 -p1 -b .tmpalloc
%patch2 -p1 -b .sha3
%patch3 -p1 -b .ecc-cve
%patch4 -p1 -b .powm-sec

%build
%configure --enable-shared
make %{?_smp_mflags}

%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
	fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/libnettle.so.4.* \
	fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.2.* \
	file=`basename $RPM_BUILD_ROOT%{_libdir}/libnettle.so.4.*.hmac` && mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.libnettle.so.4.hmac \
	file=`basename $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.2.*.hmac` && mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.libhogweed.so.2.hmac \
%{nil}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libnettle.so.4.*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.2.*


%files
%license COPYING.LIB
%{_bindir}/nettle-lfib-stream
%{_bindir}/pkcs1-conv
%{_bindir}/sexp-conv
%{_bindir}/nettle-hash
%{_libdir}/libnettle.so.4
%{_libdir}/libnettle.so.4.*
%{_libdir}/libhogweed.so.2
%{_libdir}/libhogweed.so.2.*
%{_libdir}/.libhogweed.so.*.hmac
%{_libdir}/.libnettle.so.*.hmac


%exclude %{_infodir}
%exclude %{_includedir}
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Aug  8 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-8
- Use a cache-silent version of mpz_powm to prevent cache-timing
  attacks against RSA and DSA in shared VMs. (#1364897,CVE-2016-6489)

* Wed Mar  2 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-5
- Fixed SHA-3 implementation to conform to final standard (#1252936)
- Fixed CVE-2015-8803 CVE-2015-8804 CVE-2015-8805 which caused issues
  in secp256r1 and secp384r1 calculations (#1314374)

* Tue Jul 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-4
- Correct path of links (#1117782)

* Mon Jul 28 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-3
- Added fipshmac checksum (#1117782)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.7.1-2
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Tomáš Mráz <tmraz@redhat.com> - 2.7.1-1
- Updated to nettle 2.7.1

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.6-4
- Mass rebuild 2013-12-27

* Fri Dec 13 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.6-3
- Added patch nettle-tmpalloc.patch (#1033570)

* Wed Feb  6 2013 Tomáš Mráz <tmraz@redhat.com> - 2.6-2
- nettle includes use gmp.h

* Tue Feb  5 2013 Tomáš Mráz <tmraz@redhat.com> - 2.6-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 David Woodhouse <dwmw2@infradead.org> - 2.4-3
- Remove explicit buildroot handling and defattr.

* Wed Jul 04 2012 David Woodhouse <dwmw2@infradead.org> - 2.4-2
- Review feedback

* Mon Jun 18 2012 David Woodhouse <dwmw2@infradead.org> - 2.4-1
- Revive package (GnuTLS needs it), disable static, update to current release 2.4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 10 2008 Ian Weller <ianweller@gmail.com> 1.15-5
- Moved static lib to -static

* Mon Mar 24 2008 Ian Weller <ianweller@gmail.com> 1.15-4
- Added libraries and ldconfig

* Mon Feb 18 2008 Ian Weller <ianweller@gmail.com> 1.15-3
- Added provides -static to -devel

* Sun Feb 17 2008 Ian Weller <ianweller@gmail.com> 1.15-2
- Removed redundant requires
- Removed redundant documentation between packages
- Fixed license tag
- Fixed -devel description
- Added the static library back to -devel
- Added make clean

* Fri Feb 08 2008 Ian Weller <ianweller@gmail.com> 1.15-1
- First package build.
