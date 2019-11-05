%define _trivial .0
%define _buildid .1

Summary: Enhanced seccomp library
Name: libseccomp
Version: 2.3.1
Release: 3%{?dist}.0.3
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64 ppc ppc64 ppc64le s390 s390x
License: LGPLv2
Group: System Environment/Libraries
Source: https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/seccomp/libseccomp
%ifnarch s390
BuildRequires: valgrind
%endif

Prefix: %{_prefix}

%description
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%prep
%setup -q

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}/%{_libdir}"
mkdir -p "%{buildroot}/%{_includedir}"
mkdir -p "%{buildroot}/%{_mandir}"
make V=1 DESTDIR="%{buildroot}" install
rm -f "%{buildroot}/%{_libdir}/libseccomp.la"

%files
%license LICENSE
%{_libdir}/libseccomp.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_bindir}
%exclude %{_mandir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Feb 22 2017 Paul Moore <pmoore@redhat.com> - 2.3.1-3
- Added the ppc arch to the build

* Thu Apr 28 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-2
- Fix a typo with the ppc64le architecture

* Thu Apr 21 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-1
- Escape the macros in the changelog to make rpmlint and friends happy

* Wed Apr 20 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-0
- New upstream version

* Mon Jun 15 2015 Paul Moore <pmoore@redhat.com> - 2.2.1-1
- Removed '--disable-static' from the build to ensure that scmp_sys_resolver
  is self contained and resolve RPATH issues

* Wed May 13 2015 Paul Moore <pmoore@redhat.com> - 2.2.1-0
- New upstream version
- Added aarch64 support
- Move to an autotools based build system

* Thu Feb 27 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-2
- Build with CFLAGS="${optflags}" (RHBZ #1070774)
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.1-1
- Mass rebuild 2013-12-27

* Tue Nov  5 2013 Paul Moore <pmoore@redhat.com> - 2.1.1-0
- New upstream version
- Added a %%check procedure for self-test during build
* Tue Jun 11 2013 Paul Moore <pmoore@redhat.com> - 2.1.0-0
- New upstream version
- Added support for the ARM architecture
- Added the scmp_sys_resolver tool
* Mon Jan 28 2013 Paul Moore <pmoore@redhat.com> - 2.0.0-0
- New upstream version
* Tue Nov 13 2012 Paul Moore <pmoore@redhat.com> - 1.0.1-0
- New upstream version with several important fixes
* Tue Jul 31 2012 Paul Moore <pmoore@redhat.com> - 1.0.0-0
- New upstream version
- Remove verbose build patch as it is no longer needed
- Enable _smp_mflags during build stage
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Tue Jul 10 2012 Paul Moore <pmoore@redhat.com> - 0.1.0-1
- Limit package to x86/x86_64 platforms (RHBZ #837888)
* Tue Jun 12 2012 Paul Moore <pmoore@redhat.com> - 0.1.0-0
- Initial version

