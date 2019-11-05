Name: libtevent
Version: 0.9.36
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: The tevent library
License: LGPLv3+
URL: http://tevent.samba.org/
Source: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: libtalloc-devel >= 2.1.1
BuildRequires: python-devel
BuildRequires: pytalloc-devel >= 2.1.1
BuildRequires: doxygen
BuildRequires: docbook-style-xsl
BuildRequires: libxslt

Provides: bundled(libreplace)

# Patches

Prefix: %{_prefix}

%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%prep
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build, where "Level"
# is the patch prefix option (e.g. -p1)
# Taken from specfile for python-simplejson
UpdateTimestamps() {
  Level=$1
  PatchFile=$2

  # Locate the affected files:
  for f in $(diffstat $Level -l $PatchFile); do
    # Set the files to have the same timestamp as that of the patch:
    touch -r $PatchFile $f
  done
}

%setup -q -n tevent-%{version}

for p in %patches ; do
    %__patch -p3 -i $p
    UpdateTimestamps -p3 $p
done 

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtevent.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libtevent.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_prefix}/lib64/python*

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Apr 10 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.36
- Resolves: #1558494 - Rebase tevent to the latest available upstream release

* Thu Nov 16 2017 Jakub Hrozek <jhrozek@redhat.com> - 0.9.34-1
- Resolves: #1512414 - tevent can cause a Samba file corruption bug under
                       heavy threaded load

* Sun Oct 15 2017 Jakub Hrozek <jhrozek@redhat.com> - 0.9.33-1
- Resolves: #1470054 - Rebase libtevent to enable samba rebase to version
                       4.7.x

* Tue Feb 14 2017 Jakub Hrozek <jhrozek@redhat.com> - 0.9.31-1
- Resolves: #1393812 - Rebase libtevent in RHEL-7.4 to version 4.6.x

* Thu Jun  9 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.28-1
- Resolves: #1320247 - Rebase libtevent to version 0.9.28

* Mon Apr  4 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.26-2
- Resolves: #1309439 - libtevent leaks memory during signal handling

* Fri Apr  1 2016 Jakub Hrozek <jhrozek@redhat.com> - 0.9.26-1
- Rebase libtevent to 0.9.26
- Related: rhbz#1322691

* Sun Jun 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 0.9.25-1
- Resolves: rhbz#1226049 - Rebase libtevent to at least 0.9.22 in RHEL-7.2

* Wed Jun  3 2015 Jakub Hrozek <jhrozek@redhat.com> - 0.9.24-1
- Resolves: rhbz#1226049 - Rebase libtevent to at least 0.9.22 in RHEL-7.2

* Mon Nov 24 2014 Jakub Hrozek <jhrozek@redhat.com> - 0.9.21-3
- BuildRequire the minimal applicable libtalloc version
- Resolves: rhbz#1133919 - Rebase libtevent to version 0.9.21 or newer

* Mon Nov 24 2014 Jakub Hrozek <jhrozek@redhat.com> - 0.9.21-2
- Allow building with RHEL-7.0 libtalloc
- Resolves: rhbz#1133919 - Rebase libtevent to version 0.9.21 or newer

* Thu Sep 04 2014 Jakub Hrozek <jhrozek@redhat.com> - 0.9.21-1
- Resolves: rhbz#1133919 - Rebase libtevent to version 0.9.21 or newer
- removes upstreamed patches

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.18-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.18-5
- Mass rebuild 2013-12-27

* Thu Aug 08 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.18-4
- Resolves: rhbz#994015 - tevent_loop_wait() never finishes

* Mon Jul 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.9.18-3
- Make the dependency requirements arch-specific
- Remove ancient, unused patches
- Remove python variables that are not needed on modern systems

* Wed Jun 19 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.18-2
- Apply a patch from upstream to fix tevent_poll's additional_flags
  on 32bit architectures
- Resolves: rhbz#975490

* Mon Mar 18 2013 Jakub Hrozek <jhrozek@redhat.com> - 0.9.18-1
- New upstream release 0.9.18

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-3
- Dropping the workaround dropped even the doxygen command itself..

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-2
- Drop the workaround for building man pages, it has already been
  included upstream

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-1
- New upstream release 0.9.17

* Fri Aug 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.9.16-3
- Own the individual manual pages, not the top-level directory

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.16-1
- New upstream release 0.9.16
- Adds tevent_*_trace_*() and tevent_context_init_ops()
- Move tevent.py to the arch-specific directory

* Fri Feb 10 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.15-1
- New upstream release 0.9.15
- Properly re-sets the nested.level flag in the ev.ctx when reinitializing
  after a fork()
- Allow tevent_signal events to be freed during their handler

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-4
- Include missing patch file

* Tue Dec 06 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-4
- Build pytevent properly

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-3
- Add patch to ignore --disable-silent-rules
- Include API documentation

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-2
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120

* Wed Nov 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.14-1
- New upstream release
- Required for building more recent versions of samba4

* Tue Aug  2 2011 Simo Sorce <ssorce@redhat.com> - 0.9.13-1
- New upstream release

* Tue Mar 15 2011 Simo Sorce <ssorce@redhat.com> - 0.9.11-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.10-3
- Add missing Buildrequires for pytalloc-devel

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.10-2
- Let rpmbuild strip binaries, make build more verbose.
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.10-1
- New upstream release
- Convert to new WAF build-system

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7.1
- Bump revision to chain-build libtevent, samba4 and sssd

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7
- Drop ABI compatibility patch (no longer needed)

* Wed Sep 23 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-5
- Add patch to fix a segfault case

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-2
- Fix abi compatibility with 0.9.3

* Sat Sep 8 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-1
- First independent release for tevent 0.9.8
