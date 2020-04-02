Name:		   libtirpc
Version:		0.2.4
Release:		0.16%{?dist}
Summary:		Transport Independent RPC Library
Group:		  	System Environment/Libraries
License:		SISSL and BSD
URL:  			http://git.linux-nfs.org/?p=steved/libtirpc.git;a=summary

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	http://downloads.sourceforge.net/libtirpc/libtirpc-%{version}.tar.bz2

BuildRequires:		automake, autoconf, libtool, pkgconfig
BuildRequires:		krb5-devel

#
# RHEL7.1
#
Patch001: libtirpc-0.2.4-svc-buffer-overflow.patch
Patch002: libtirpc-0.2.4-nonblocking-mode.patch

#
# RHEL7.2
#
Patch003: libtirpc-0.2.4-mem-leak.patch

#
# RHEL7.3
#
Patch004: libtirpc-0.2.4-debug.patch
Patch005: libtirpc-0.2.4-svc_vc_create-memleak.patch
Patch006: libtirpc-0.2.4-svc-gss-memleaks.patch
Patch007: libtirpc-0.2.4-clnt-mthr-create.patch

#
# RHEL7.4
#
Patch008: libtirpc-0.2.4-makefd_xprt-fd.patch
Patch009: libtirpc-0.2.4-CVE-2017-8779.patch

Prefix: %{_prefix}

#
# RHEL7.6
#
Patch010: libtirpc-0.2.4-xdrstdio.patch
Patch011: libtirpc-0.2.4-covscan.patch

#
# RHEL7.7
#
Patch012: libtirpc-0.2.4-badfree.patch
Patch013: libtirpc-0.2.4-eof.patch

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of 
Open Network Computing (ONC), and is derived directly from the 
Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V 
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface 
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported 
by almost 70 vendors on all major operating systems.  TS-RPC source code 
(RPCSRC 4.0) remains available from several internet sites.

%prep
%setup -q
# 1102765 - rpcbind segfaults in svc_vc_recv
%patch001 -p1
# 1162714 - Non blocking mode for writes is broken
%patch002 -p1
# 1236187 - Memory Leak in libtirpc 
%patch003 -p1
# 1273159 - Backport libtirpc's new debugging interface from upstream 
%patch004 -p1
# 1276685 - memory leak in svc_vc_create
%patch005 -p1
# 1282488 - Address memory leaks in server-side GSS authenticator
%patch006 -p1
# 1342545 - Threads specifically interacting with libtirpc library...
%patch007 -p1
# 1410617 - makefd_xprt: remove obsolete check for fd number 
%patch008 -p1
#  CVE-2017-8779 libtirpc: libtirpc, libntirpc: Memory leak....
%patch009 -p1
# 1261738 - xdrstdio_create buffers do not output encoded values on ppc
%patch010 -p1
# 1627856 - Backport important issues found by covscan in...
%patch011 -p1
# 1631609 - BAD_FREE: "free" frees incorrect pointer "tmp" found by covscan
%patch012 -p1
# 1331554 - rpcbind closes connection when rpc fragment sent...
%patch013 -p1

# Remove .orig files
find . -name "*.orig" | xargs rm -f

%build
sh autogen.sh
autoreconf -fisv
%configure
make all

%install
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
make install DESTDIR=%{buildroot} \
	libdir=%{_libdir} pkgconfigdir=%{_libdir}/pkgconfig
# Don't package .a or .la files
rm -f %{buildroot}%{_libdir}/*.{a,la}


%files
%defattr(-,root,root)
%{_libdir}/libtirpc.so.*
%config(noreplace)%{_sysconfdir}/netconfig

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_mandir}

%changelog
* Thu Apr 2 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Dec 17 2018 Steve Dickson <steved@redhat.com> 0.2.4-0.16
- getnetconfig.c: fix a BAD_FREE (CWE-763) (bz 1631609)
- Fix EOF detection on non-blocking socket (bz 1331554)

* Wed Sep 19 2018 Steve Dickson <steved@redhat.com> 0.2.4-0.15
- Fixed typo in spec file (bz 1627856)

* Fri Sep 14 2018 Steve Dickson <steved@redhat.com> 0.2.4-0.14
- Removed a false positive from the covscan (bz 1627856)

* Tue Sep 11 2018 Steve Dickson <steved@redhat.com> 0.2.4-0.13
- Fix issues found from covscan (bz 1627856)

* Fri Jul 20 2018 Steve Dickson <steved@redhat.com> 0.2.4-0.12
- xdrstdio_create buffers do not output encoded values on ppc (bz 1261738)

* Tue Jul 10 2018 Steve Dickson <steved@redhat.com> 0.2.4-0.11
- Updated the URL (bz 1583922)

* Wed May 17 2017 Steve Dickson <steved@redhat.com> 0.2.4-0.10
- Fix for CVE-2017-8779 (bz 1449463)

* Sat Feb 25 2017 Steve Dickson <steved@redhat.com> 0.2.4-0.9
-  makefd_xprt: remove obsolete check for fd number (bz 1410617)

* Mon Jun  6 2016 Steve Dickson <steved@redhat.com> 0.2.4-0.8
- handle concurrent connect calls in clnt_vc_create() (bz 1342545)

* Fri Apr  8 2016 Steve Dickson <steved@redhat.com> 0.2.4-0.7
- Backported upstream debugging (bz 1273159)
- Fixed memory leak in svc_vc_create (bz 1276685)
- Fixed memory leaks in server-side GSS authenticator (bz 1282488)

* Mon Jun 29 2015 Steve Dickson <steved@redhat.com> 0.2.4-0.6
- Fixed a couple memory leaks (bz 1236187)

* Sat Nov 15 2014 Steve Dickson <steved@redhat.com> 0.2.4-0.5
- Fixed the non-blocking mode (bz 1162714)

* Wed Sep 17 2014 Steve Dickson <steved@redhat.com> 0.2.4-0.4
- Avoid buffer overruns svcauth_gss_validate() (bz 1102765)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.2.4-0.3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.2.4-0.2
- Mass rebuild 2013-12-27

* Fri Dec 13 2013 Steve Dickson <steved@redhat.com> 0.2.4-0.1
- Update to latest upstream release: 0.2.4 (bz 1040593)

* Wed Dec 11 2013 Steve Dickson <steved@redhat.com> 0.2.4-0
- Update to latest upstream release: 0.2.4 (bz 1038736)

* Tue Nov 26 2013 Steve Dickson <steved@redhat.com> 0.2.3-4
- Update to latest RC release: libtirpc-0-2-4-rc3 (bz 1034434)

* Tue Jul  2 2013 Steve Dickson <steved@redhat.com> 0.2.3-3
- Update to latest RC release: libtirpc-0-2-4-rc2 (bz 959469)

* Mon Apr 22 2013 Steve Dickson <steved@redhat.com> 0.2.3-2
- Update to latest RC release: libtirpc-0-2-4-rc1 (bz 948378)

* Thu Apr 11 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-1
- Removed libgssglue dependency (patch from master)

* Wed Feb 13 2013 Steve Dickson <steved@redhat.com> 0.2.3-0
- Updated to latest upstream release: 0.2.3

* Tue Nov 13 2012 Steve Dickson <steved@redhat.com> 0.2.1-43
- Updated to latest upstream RC release: 0.2.3-rc4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Steve Dickson <steved@redhat.com> 0.2.1-4.1
- Updated to latest upstream RC release: libtirpc-0.2.3-rc3

* Mon Mar 19 2012 Steve Dickson <steved@redhat.com> 0.2.1-3.1
- Fixed the install path in doc/Makefile.am

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Steve Dickson <steved@redhat.com> 0.2.1-1.1
- Fixed segfault in SVCAUTH_WRAP call (bz 722594)

* Tue Jun 21 2011 Steve Dickson  <steved@redhat.com> 0.2.1-1
- Updated to latest upstream version: 0.2.3-rc1

* Mon May  2 2011 Steve Dickson  <steved@redhat.com> 0.2.1-0
- Updated to latest upstream version: 0.2.2

* Tue Apr 12 2011 Karsten Hopp <karsten@redhat.com> 0.2.1-7.1
- replace Requires(devel) with a simple Requires as the new rpm
  aborts otherwise with "Bad Requireflags: qualifiers: Requires(devel)"

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Steve Dickson  <steved@redhat.com> 0.2.1-6
- Moved the libraries from /usr/lib to /lib 

* Mon Aug 30 2010 Steve Dickson  <steved@redhat.com> 0.2.1-5
- Relicense these SISSL files to 3 clause BSD
- Fixed last remaining BSD license issues

* Fri Jul 16 2010 Steve Dickson  <steved@redhat.com> 0.2.1-4
- Add back SISSL license attribution

* Fri Jul 09 2010 Mike McGrath <mmcgrath@redhat.com> 0.2.1-3.1
- Rebuild to fix broken man dep s/man/man-db/

* Tue May 18 2010 Steve Dickson  <steved@redhat.com> 0.2.1-3
- Updated to latest RC release: libtirpc-0-2-2-rc2 [bz 519430]

* Mon Mar 22 2010 Steve Dickson  <steved@redhat.com> 0.2.1-2
- Updated to latest RC release: libtirpc-0-2-2-rc1

* Mon Nov 30 2009 Steve Dickson  <steved@redhat.com> 0.2.1-1
- Updated to latest upstream version: 0.2.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Steve Dickson  <steved@redhat.com> 0.2.0-3
- Updated to latest upstream tag: 0-2-1-rc3
    Fixed the --disable-gss options
    Fixed a number of warnings
    Change how architectures are define in xdr_float.c

* Mon Jun 29 2009 Steve Dickson  <steved@redhat.com> 0.2.0-2
- Updated to latest upstream tag: 0-2-1-rc2
    rpcb_clnt: RPC_PROGNOTREGISTERED is a permanent error
    clnt_dg: Fix infinite loop when datagram call times ou
    Updated .gitignore file
    Replace the hard coded path name with the top_srcdir macrc
    Added 'doc' to the SUBDIRS list so make install work correctly.

* Fri May 29 2009 Steve Dickson  <steved@redhat.com> 0.2.0-1
- Updated to latest upstream version: 0.2.0

* Tue May 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.11-3
- Replace the Sun RPC license with the BSD license, with the explicit permission of Sun Microsystems

* Mon Apr 20 2009 Steve Dickson  <steved@redhat.com> 0.1.11-2
- Updated to libtirpc-0.1.12-rc1

* Mon Apr 20 2009 Steve Dickson  <steved@redhat.com> 0.1.11-1
- Updated to the latest release: 0.1.11 

* Fri Mar 13 2009 Steve Dickson  <steved@redhat.com> 0.1.10-6
- libtirpc: set r_netid and r_owner in __rpcb_findaddr_timed
- libtirpc: be sure to free cl_netid and cl_tp
- libtirpc: must free saved wire verifier when destroying context

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Steve Dickson  <steved@redhat.com> 0.1.10-4
- Converted all uids and uids to type uid_t and gid_t (sf 2446314)

* Wed Jan 28 2009 Steve Dickson  <steved@redhat.com> 0.1.10-3
- backwards compatibility: fix order of fields in TI-RPC's 
  svc_req (bz 481388)
- Removed a number warnings.

* Thu Jan 22 2009 Steve Dickson  <steved@redhat.com> 0.1.10-2
- Header file fixes for C++

* Thu Nov 20 2008 Steve Dickson  <steved@redhat.com> 0.1.10-1
- Updated to latest upstream version: 0.1.10

* Tue Oct 28 2008 Steve Dickson  <steved@redhat.com> 0.1.9-7
- Fixed some incorrect function declarations (bz468815)

* Mon Oct 27 2008 Steve Dickson  <steved@redhat.com> 0.1.9-6
- Fix bad assumption taddr2uaddr processing that 
  caused a segfault (bz468014)

* Tue Sep 16 2008 Steve Dickson <steved@redhat.com> 0.1.9-5
- Fix for taddr2addr conversion bug of local addresses
- Fixed some of warnings in: src/auth_time.c, src/clnt_dg.c and
  src/clnt_raw.c
- Added some #ifdef NOTUSED around some code in src/rpbc_clnt.c
  that was not being used...

* Thu Sep  4 2008 Steve Dickson <steved@redhat.com> 0.1.9-4
- Always make IPv6 sockets V6ONLY
- Fix incorrect sizeof() in __rpc_getbroadifs

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.9-3
- fix license tag

* Tue Jul 8 2008 Steve Dickson  <steved@redhat.com> 0.1.9-1
- Update to latest upstream version 0.1.9

* Fri Jun 27 2008 Steve Dickson  <steved@redhat.com> 0.1.8-2
- Added super-H(sh3,4) architecture support (bz 446559)

* Tue Jun 10 2008 Steve Dickson  <steved@redhat.com> 0.1.8-1
- Update to latest upstream version 0.1.8

* Wed Mar 12 2008 Steve Dickson  <steved@redhat.com> 0.1.7-18
- Install man pages in the 3t section

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.7-17
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Steve Dickson  <steved@redhat.com> 0.1.7-16
- Added patch that creates a libtirpc.pc used by the
  pkg-config command.

* Thu Jan 24 2008 Steve Dickson  <steved@redhat.com> 0.1.7-15
- Protect from buffer overflow in the GSS code. (bz 362121)

* Mon Dec 17 2007 Steve Dickson  <steved@redhat.com> 0.1.7-14
- Fixed typo in /etc/netconfig file (bz 414471)

* Thu Oct 25 2007 Steve Dickson  <steved@redhat.com> 0.1.7-13
- Added a check for the ARM arch (bz 351071)

* Wed Oct 17 2007 Steve Dickson  <steved@redhat.com> 0.1.7-12
- Switch the libgssapi dependency to libgssglue

* Mon Oct 15 2007 Steve Dickson  <steved@redhat.com> 0.1.7-11
- Made tcp6/udp6 network ids no longer visible in the netconfig
  file since the ipv6 code is not fully baked yet in rpcbind. (bz 249121)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.1.7-10
- Rebuild for selinux ppc32 issue.

* Mon Jul 30 2007 <steved@redhat.com> 0.1.7-9
- Fixed mutex lock problem in clnt_raw_create()
- Ignore the return value of snprintf() and use strlen() instead
  to bump the pointer in clnt_sperror()
- A couple ntohs() were needed in bindresvport_sa()
- Added IP_RECVERR processing with to clnt_dg_call() so
  application will see errors instead of timing out
- Make sure remote address (xp_rtaddr) is populated
  with the correct type of address.
- Change the order of network ids in /etc/netconfg
  putting ipv4 ids before ipv6.
- Bumped up Release from 8 to 9.

* Mon Jul  9 2007 <steved@redhat.com> 0.1.7-7
- Fixed infinite loop in svc_run() (bz 246677)

* Thu Apr 26 2007 <steved@redhat.com> 0.1.7-6
- Fixed potential buffer overflow in xdr_strings
- Added a optimization to bindresvport that allows more
  ports to be tried.

* Mon Mar 26 2007 Steve Dickson <steved@redhat.com> 0.1.7-5
- Fixed Unowned Directory RPM problem (bz 233873)

* Mon Aug 28 2006 Steve Dickson <steved@redhat.com> 0.1.7-4
- Fixed undefined symbol (bz 204296)

* Mon Aug 14 2006 Steve Dickson <steved@redhat.com> 0.1.7-3
- Added in svc_auth_none needed by the GSSAPI code.
- Added compile define for ppc64 archs

* Fri Aug 11 2006 Steve Dickson <steved@redhat.com> 0.1.7-2
- Uncommented tcp6 and udp6 in the default /etc/netconfig file.
- Added hooks to used the libgssapi library.

* Fri Aug  4 2006 Steve Dickson <steved@redhat.com> 0.1.7-1
- Initial commit
