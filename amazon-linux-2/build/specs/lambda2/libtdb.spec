Name: libtdb
Version: 1.3.15
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: The tdb library
License: LGPLv3+
URL: http://tdb.samba.org/
Source: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel

Provides: bundled(libreplace)

# Patches

%description
A library that implements a trivial database.

%package -n tdb-tools
Group: Development/Libraries
Summary: Developer tools for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%prep
%setup -q -n tdb-%{version}

for p in %patches ; do
    %__patch -p3 -i $p
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

rm -f $RPM_BUILD_ROOT%{_libdir}/libtdb.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libtdb.so.*

%files -n tdb-tools
%defattr(-,root,root,-)
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_prefix}/lib64/python*

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sun Oct 15 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.3.15-1
- Resolves: rhbz#1470049 - Rebase libtdb to enable samba rebase to
                           version 4.7.x

* Tue May  2 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.3.12-2
- Resolves: rhbz#1441231 - The tdb robust mutexes runtime check is not thread safe and ends in a deadlock

* Tue Feb 14 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.3.12-1
- Resolves: rhbz#1393812 - Rebase libtevent in RHEL-7.4 to version 4.6.x

* Fri Apr  1 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.3.8-1
- Rebase libtdb to 1.3.8
- Related: rhbz#1322691

* Wed Aug 19 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.6-2
- Resolves: rhbz#1241015 - tdb deadlocks if you acquire allrecord_lock
                           and start two traverses

* Sun Jun 14 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.6-1
- Resolves: rhbz#1226048 - Rebase libtdb to at least 1.3.4 in RHEL-7.2

* Wed Jun  3 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.3.5-1
- Resolves: rhbz#1226048 - Rebase libtdb to at least 1.3.4 in RHEL-7.2

* Thu Sep  4 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.3.0-1
- Resolves: rhbz#1133915 - Rebase libtdb to version 1.3.0 or newer

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.12-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.12-2
- Mass rebuild 2013-12-27

* Tue Jun 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.2.12-1
- New upstream release 1.2.12

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 01 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.2.11-1
- New upstream release 1.2.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.2.10-15
- New upstream release 1.2.10
- Remove upstreamed patches
- Provides functionality for the upcoming Samba 4 beta

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-13
- Add patch to ignore --disable-silent-rules
- Include README documentation

* Wed Nov 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-12
- Add explicit mention of the bundled libreplace
- https://fedorahosted.org/fpc/ticket/120


* Wed Nov 09 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-11
- Rebuild for F17 due to bz#744766

* Tue Apr  5 2011 Simo Sorce <ssorce@redhat.com> - 1.2.9-9
- Add patch to limit database expansion, was causing OOMs in SSSD in some
  extreme situations.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-8
- Actually fix the verbosity

* Fri Jan 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-7
- Let rpmbuild strip binaries, make build more verbose.
- Original patch by Ville SkyttÃ¤ <ville.skytta@iki.fi>

* Wed Jan 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-6
- Install python bindings into the correct location

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-5
- Run ldconfig on python-tdb

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-4
- Do not delete a necessary file during %%install

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-3
- Bump release to rebuild with the correct sources in place

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-2
- Bump build to rebuild with sources in place

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.2.9-1
- New upstream bugfix release
- Adds a new tdbrestore utility
- Convert to new WAF build-system
- Add python bindings in new python-tdb subpackage

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-3
- add missing build require

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-2
- Fix spec file
- Package manpages too

* Wed Feb 24 2010 Simo Sorce <ssorce@redhat.com> - 1.2.1-1
- New upstream bugfix release

* Tue Dec 15 2009 Simo Sorce <ssorce@redhat.com> - 1.2.0-1
- New upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Simo Sorce <ssorce@redhat.com> - 1.1.5-1
- Original tarballs had a screw-up, rebuild with new fixed tarballs from
  upstream.

* Tue Jun 16 2009 Simo Sorce <ssorce@redhat.com> - 1.1.5-0
- New upstream release

* Wed May 6 2009 Simo Sorce <ssorce@redhat.com> - 1.1.3-15
- First public independent release from upstream
