%bcond_without check

Summary: Enhanced seccomp library
Name: libseccomp
Version: 2.4.1
Release: 1%{?dist}
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64 mipsel mips64el ppc64 ppc64le s390 s390x
License: LGPLv2
Group: System Environment/Libraries
Source: https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/seccomp/libseccomp
%ifarch %{valgrind_arches}
# Versions prior to 3.13.0-4 do not work on ARM with newer glibc 2.25.0-6
# See https://bugzilla.redhat.com/show_bug.cgi?id=1466017
BuildRequires: valgrind >= 1:3.13.0-4
%endif

%description
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%package devel
Summary: Development files used to build applications with libseccomp support
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release} pkgconfig

%description devel
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%package static
Summary: Enhanced seccomp static library
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release} pkgconfig

%description static
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

%if %{with check}
%check
make V=1 check
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CREDITS
%doc README.md
%doc CHANGELOG
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_libdir}/libseccomp.so
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%files static
%{_libdir}/libseccomp.a

%changelog
* Fri May 31 2019 Marek Tamaskovic <mtamasko@redhat.com> - 2.4.1-1
- rebase to 2.4.1

* Fri May 10 2019 Daniel Kopecek <dkopecek@redhat.com> - 2.3.3-4
- spec: make the check phase conditional

* Fri Aug  3 2018 Florian Weimer <fweimer@redhat.com> - 2.3.3-3
- Honor %%{valgrind_arches}

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Paul Moore <pmoore@redhat.com> - 2.3.3-1
- New upstream version

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.3.2-3
- Re-enable valgrind-based tests on ARMv7

* Thu Jun 29 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.3.2-2
- Disable running valgrind-based tests on ARMv7 due to glibc/valgrind bug (RHBZ #1466017)

* Wed Mar 01 2017 Paul Moore <pmoore@redhat.com> -2.3.2-1
- New upstream version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 20 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-1
- Cleanup the changelog whitespace and escape the macros to make rpmlint happy

* Wed Apr 20 2016 Paul Moore <pmoore@redhat.com> - 2.3.1-0
- New upstream version

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.0-1
- No valgrind on s390

* Mon Feb 29 2016 Paul Moore <pmoore@redhat.com> - 2.3.0-0
- New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 08 2015 Paul Moore <pmoore@redhat.com> - 2.2.3-0
- New upstream version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Paul Moore <pmoore@redhat.com> - 2.2.1-0
- New upstream version

* Thu Feb 12 2015 Paul Moore <pmoore@redhat.com> - 2.2.0-0
- New upstream version
- Added aarch64 support
- Added a static build

* Thu Sep 18 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-6
- Fully builds on i686, x86_64, and armv7hl (RHBZ #1106071)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.1.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-2
- Build with CFLAGS="${optflags}"

* Mon Feb 17 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-1
- Removed the kernel dependency (RHBZ #1065572)

* Thu Oct 31 2013 Paul Moore <pmoore@redhat.com> - 2.1.1-0
- New upstream version
- Added a %%check procedure for self-test during build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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

