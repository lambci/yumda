# The testsuite is unsuitable for running on buildsystems
%global tests_enabled 0

Summary: System and process monitoring utilities
Name: procps-ng
Version: 3.3.10
Release: 26%{?dist}
License: GPL+ and GPLv2 and GPLv2+ and GPLv3+ and LGPLv2+
Group: Applications/System
URL: https://sourceforge.net/projects/procps-ng/

Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz

Patch0: procps-ng-3.3.10-pmap-skip-vmflags.patch
Patch1: procps-ng-3.3.10-free-uninitialized-errno.patch
Patch2: procps-ng-3.3.10-ps-thcount-format-option.patch
Patch3: procps-ng-3.3.10-vmstat-devlen.patch
Patch4: procps-ng-3.3.10-find_elf_note-memory-error-fix.patch
Patch5: procps-ng-3.3.10-ps-scattered-thread-cgroups.patch
Patch6: procps-ng-3.3.10-vmstat-long-device-name.patch
Patch7: procps-ng-3.3.10-ps-full-wchan-name.patch
Patch8: procps-ng-3.3.10-pmap-lines-twice.patch
Patch9: procps-ng-3.3.10-slabtop-use-val-float.patch
Patch10: procps-ng-3.3.10-sysctl-conf-manpage-predef-note.patch 
Patch11: procps-ng-3.3.10-top-instant-cpu-stats.patch
Patch12: procps-ng-3.3.10-sysctl-man-conf-override-hint.patch
Patch13: procps-ng-3.3.10-top-strange-mem-val-scaling.patch 
Patch14: procps-ng-3.3.10-sysctl-empty-value-allowed.patch
Patch15: procps-ng-3.3.10-top-locale-independent-float-delay.patch
Patch16: procps-ng-3.3.10-free-mem-petabytes-segfault.patch
Patch17: procps-ng-3.3.10-ps-new-option-loginid-luid.patch
Patch18: procps-ng-3.3.10-CVE-2018-1124.patch
Patch19: procps-ng-3.3.10-CVE-2018-1122.patch
Patch20: procps-ng-3.3.10-recognize_sched_deadline.patch
Patch21: procps-ng-3.3.10-free-counts-unreclaim-slabs-in-avail-mem.patch


BuildRequires: ncurses-devel
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: systemd-devel

%if %{tests_enabled}
BuildRequires: dejagnu
%endif

Provides: procps = %{version}-%{release}
Obsoletes: procps < 3.2.9-1

# usrmove hack - will be removed once initscripts are fixed
Provides: /sbin/sysctl
Provides: /bin/ps

Prefix: %{_prefix}

%description
The procps package contains a set of system utilities that provide
system information. Procps includes ps, free, skill, pkill, pgrep,
snice, tload, top, uptime, vmstat, w, watch and pwdx. The ps command
displays a snapshot of running processes. The top command provides
a repetitive update of the statuses of running processes. The free
command displays the amounts of free and used memory on your
system. The skill command sends a terminate command (or another
specified signal) to a specified set of processes. The snice
command is used to change the scheduling priority of specified
processes. The tload command prints a graph of the current system
load average to a specified tty. The uptime command displays the
current time, how long the system has been running, how many users
are logged on, and system load averages for the past one, five,
and fifteen minutes. The w command displays a list of the users
who are currently logged on and what they are running. The watch
program watches a running program. The vmstat command displays
virtual memory statistics about processes, memory, paging, block
I/O, traps, and CPU activity. The pwdx command reports the current
working directory of a process or processes.

%package i18n
Summary:  Internationalization pack for procps-ng
Group:    Applications/System
Requires: %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description i18n
Internationalization pack for procps-ng


%prep
%setup -q -n %{name}-%{version}

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


%build

autoreconf --verbose --force --install

%configure \
  --docdir=/unwanted \
  --disable-static \
  --enable-w-from \
  --disable-kill \
  --disable-rpath \
  --enable-watch8bit \
  --enable-skill \
  --enable-sigwinch \
  --enable-libselinux \
  --without-systemd \
  --disable-pidof \
  --disable-modern-top

make CFLAGS="%{optflags}"


%install
make DESTDIR=%{buildroot} install

# --bindir seems to be ignored
mv %{buildroot}%{_prefix}/usr/bin/* %{buildroot}%{_bindir}/

%files
%license COPYING COPYING.LIB

%{_libdir}/libprocps.so.*
%{_bindir}/*
%{_sbindir}/*

%exclude %{_libdir}/libprocps.la
%exclude /unwanted/*

%files i18n
%{_datadir}/locale/*

%exclude %{_libdir}/libprocps.so
%exclude %{_libdir}/pkgconfig/libprocps.pc
%exclude %{_includedir}
%exclude %{_mandir}

%changelog
* Thu Oct 31 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Apr 12 2019 Jan Rybar <jrybar@redhat.com> - 3.3.10-26
- free: unreclaimable slabs counted into free memory, used mem incorrect
- Resolves: rhbz#1699264

* Wed Mar 27 2019 Jan Rybar <jrybar@redhat.com> - 3.3.10-25
- ps: recognize SCHED_DEADLINE in CLS field, upstream backport
- Resolves: rhbz#1692843

* Tue Feb 26 2019 Jan Rybar <jrybar@redhat.com> - 3.3.10-24
- top: Do not default to the cwd in configs_read()
- Resolves: rhbz#1577023

* Tue May 15 2018 Kamil Dudka <kdudka@redhat.com> - 3.3.10-23
- check for truncation after calling snprintf()
- Related: CVE-2018-1124

* Fri May 11 2018 Kamil Dudka <kdudka@redhat.com> - 3.3.10-22
- fix integer overflows leading to heap overflow in file2strvec()
- Resolves: CVE-2018-1124

* Thu Apr 19 2018 Jan Rybar <jrybar@redhat.com> - 3.3.10-21
- ps: new format option LUID (LoginId)
- Resolves: rhbz#1518986

* Mon Jan 15 2018 Jan Rybar <jrybar@redhat.com> - 3.3.10-20
- free: segfault when system memory exceeds petabytes
- Resolves: rhbz#1263765

* Mon Jan 15 2018 Jan Rybar <jrybar@redhat.com> - 3.3.10-19
- top: locale independent float character in delay now accepted
- Resolves: rhbz#1182248

* Thu Jan 04 2018 Jan Rybar <jrybar@redhat.com> - 3.3.10-18
- sysctl: empty value is now accepted
- Resolves: rhbz#1507356

* Wed Sep 06 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-17
- top: strange unit scaling with high memory values
- Resolves: rhbz#1253851

* Wed May 31 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-16
- sysctl manpage: Added explanation of conf files precedence
- Resolves: rhbz#1456905

* Fri Apr 07 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-15
- top - real CPU statistics instead of since-boot are shown at start
- Resolves: rhbz#1182327

* Fri Apr 07 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-14
- sysctl.conf manpage: note about predefined values added
- Resolves: rhbz#1439837

* Mon Mar 13 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-13
- slabtop: incorrect computation of "used" value, use float to fix
- Resolves: rhbz#1329958

* Mon Feb 20 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-12
- pmap no longer shows each line twice with blank values on newer kernels
- Resolves: rhbz#1330417

* Tue Jan 31 2017 Jan Rybar <jrybar@redhat.com> - 3.3.10-11
- ps no longer removes 'do_' and 'sys_' from wchan data
- Resolves: rhbz#1373246

* Tue Jul 26 2016 Jan Rybar <jrybar@redhat.com> - 3.3.10-10
- Fixes sysinfo - devices with name longer than 20 chars are mistaken for partitions
- Resolves: rhbz#1169349

* Thu Jul 07 2016 Jan Rybar <jrybar@redhat.com> - 3.3.10-9
- Fixes showing same cgroups for threads under process by adding format option
- Resolves: rhbz#1284087

* Mon Jul 04 2016 Jan Rybar <jrybar@redhat.com> - 3.3.10-8
- Fixes obtaining environment variables in find_elf_note function
- Resolves: rhbz#1287752
 
* Thu Jun 09 2016 Jan Rybar <jrybar@redhat.com> - 3.3.10-7
- Fixing sysinfo - devices with length exceeding 15 chars are not displayed in vmstat -d
- Resolves: #1169349

* Mon Jun 06 2016 Jan Rybar <jrybar@redhat.com> - 3.3.10-6
- #1174311 - ps - thcount not recognized as a format option
- Resolves: #1174311

* Tue Dec 01 2015 Jaromir Capik <jcapik@redhat.com> - 3.3.10-5
- #1287038 - free - error while parsing arguments
- Resolves: #1287038

* Tue Nov 24 2015 Jaromir Capik <jcapik@redhat.com> - 3.3.10-4
- #1262864 - Correctly skip vmflags (and other keys starting with A-Z)
- Resolves: #1262864

* Mon Oct 06 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.10-3
- Disabling translated man pages due to conflicts with man-pages-*
- Removing /etc/sysctl.d (quietly stolen by systemd)
- Related: rhbz#1119263 rhbz#1119260 rhbz#1060715 rhbz#1113206
- Related: rhbz#1112734 rhbz#1078310 rhbz#1116309 rhbz#1070736

* Tue Sep 23 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.10-2
- Replacing RC tarball with final 3.3.10 release
- Related: rhbz#1119263 rhbz#1119260 rhbz#1060715 rhbz#1113206
- Related: rhbz#1112734 rhbz#1078310 rhbz#1116309 rhbz#1070736

* Tue Sep 09 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.10-1
- Upgrading to 3.3.10
- top.1: physical memory - has used / is using (#1119263)
- Include man pages for openproc, readproc and readproctab (#1119260)
- ps -p cycles over all PIDs instead of just one (#1060715)
- Remove explicit dependency on systemd-libs package (#1113206)
- Allow longer usernames to display in ps output (#1112734)
- w doesn't display FROM by default (#1078310)
- Return value of pgrep is incorrect (#1116309)
- Should shared memory be accounted in cached in free output? (#1070736)
- Resolves: rhbz#1119263 rhbz#1119260 rhbz#1060715 rhbz#1113206
- Resolves: rhbz#1112734 rhbz#1078310 rhbz#1116309 rhbz#1070736

* Thu Feb 27 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-6
- Subtracting Shmem from Cached (#1070736)
- Resolves: rhbz#1070736

* Thu Feb 06 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-5
- Support for timestamps & wide diskstat (#1053428, #1025833)
- Fixing fd leak in watch
- Fixing format-security build issues
- Skipping trailing zeros in read_unvectored (#1057600)
- Resolves: rhbz#1053428, Related: rhbz#1025833

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.3.9-4
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.9-3
- 'vmstat -w' was not wide enough (#1025833)
- Related: rhbz#1025833

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.3.9-2
- Mass rebuild 2013-12-27

* Tue Dec 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.9-1
- Update to 3.3.9
- Resolves: rhbz#1025833 rhbz#1025774 rhbz#1027109

* Mon Oct 21 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-15
- Fixing incorrect format specifier (introduced with namespaces)

* Tue Sep 17 2013 Aristeu Rozanski <aris@redhat.com> - 3.3.8-14
- Introduce namespaces support (#980516)

* Fri Aug 09 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-13
- Including forgotten man fixes (#948522)

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-12
- Fixing the license tag

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-11
- Support for libselinux (#975459)
- Support for systemd (#994457)
- Support for 'Shmem' in free (#993271)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-9
- RH man page scan (#948522)

* Tue Jul 02 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-8
- Extending the end-of-job patch disabling the screen content restoration

* Mon Jul 01 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-7
- Disabling screen content restoration when exiting 'top' (#977561)
- Enabling SIGWINCH flood prevention

* Wed Jun 26 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-6
- Avoiding "write error" messages when piping to grep (#976199)

* Wed Jun 26 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-5
- Disabling tests - unsuitable for running on buildsystems

* Mon Jun 17 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-4
- Enabling skill and snice (#974752)

* Wed Jun 12 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-3
- Adding major version in the libnuma soname

* Thu May 30 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-2
- watch: enabling UTF-8 (#965867)

* Wed May 29 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.8-1
- Update to 3.3.8

* Wed May 22 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-4
- top: inoculated against a window manager like 'screen' (#962022)

* Tue Apr 16 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-3
- Avoid segfaults when reading zero bytes - file2str (#951391)

* Mon Apr 15 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-2
- Moving libprocps.pc to the devel subpackage (#951726)

* Tue Mar 26 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.7-1
- Update to 3.3.7
- Reverting upstream commit for testsuite/unix.exp

* Tue Feb 05 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-4
- Fixing empty pmap output on ppc/s390 (#906457)

* Tue Jan 15 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-3
- Typo in the description, pdwx instead of pwdx (#891476)

* Tue Jan 08 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-2
- Rebuilding with tests disabled (koji issue #853084)

* Tue Jan 08 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.6-1
- Update to 3.3.6
- Changing URL/Source from gitorious to recently created sourceforge page
- Replacing autogen.sh with autoreconf

* Mon Jan 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Dec 11 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.4-2
- fixing the following regressions:
-   negative ETIME field in ps (#871819)
-   procps states a bug is hit when receiving a signal (#871824)
-   allow core file generation by ps command (#871825)

* Tue Dec 11 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Tue Sep 25 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-3.20120807git
- SELinux spelling fixes (#859900)

* Tue Aug 21 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-2.20120807git
- Tests enabled

* Tue Aug 07 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-1.20120807git
- Update to 3.3.3-20120807git

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-3
- Second usrmove hack - providing /bin/ps

* Tue Mar 06 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-2
- Fixing requires in the devel subpackage (missing %{?_isa} macro)
- License statement clarification (upstream patch referrenced in the spec header)

* Mon Feb 27 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-1
- Initial version
