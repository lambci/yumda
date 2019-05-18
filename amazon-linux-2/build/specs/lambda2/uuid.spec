# %define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
# %global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

# # Private libraries are not be exposed globally by RPM
# %global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$

#fix multilib - add wrapper and suffix to original files
# %if %{_lib} == lib64
%global mlsuffix 64
# %else
# %global mlsuffix 32
# %endif

Name:           uuid
Version:        1.6.2
Release: 26%{?dist}.0.1
Summary:        Universally Unique Identifier library
License:        MIT
Group:          System Environment/Libraries
URL:            http://www.ossp.org/pkg/lib/uuid/
Source0:        ftp://ftp.ossp.org/pkg/lib/uuid/uuid-%{version}.tar.gz
Source1:        uuid-config-wrapper
Patch0:         uuid-1.6.1-ossp.patch
Patch1:         uuid-1.6.1-mkdir.patch
Patch2:         uuid-1.6.2-php54.patch

# rhbz#829532
Patch3:         uuid-1.6.2-hwaddr.patch

# do not strip binaries
Patch4:         uuid-1.6.2-nostrip.patch
Patch5: uuid-1.6.2-manfix.patch
Patch6: uuid-1.6.2-multilibfix.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libtool

Obsoletes:      %{name}-pgsql < 1.6.2-24

Prefix: %{_prefix}

%description
OSSP uuid is a ISO-C:1999 application programming interface (API)
and corresponding command line interface (CLI) for the generation
of DCE 1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally
Unique Identifier (UUID). It supports DCE 1.1 variant UUIDs of version
1 (time and node based), version 3 (name based, MD5), version 4
(random number based) and version 5 (name based, SHA-1). Additional
API bindings are provided for the languages ISO-C++:1998, Perl:5 and
PHP:4/5. Optional backward compatibility exists for the ISO-C DCE-1.1
and Perl Data::UUID APIs.

%package c++
Summary:        C++ support for Universally Unique Identifier library
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description c++
C++ libraries for OSSP uuid.

%package dce
Summary:        DCE support for Universally Unique Identifier library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description dce
DCE OSSP uuid library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .php54
%patch3 -p1 -b .hwaddr
%patch4 -p1 -b .nostrip
%patch5 -p1 -b .manfix
%patch6 -p1 -b .multilibfix

%build
# Build the library.
export LIB_NAME=libossp-uuid.la
export DCE_NAME=libossp-uuid_dce.la
export CXX_NAME=libossp-uuid++.la
export PHP_NAME=$(pwd)/php/modules/ossp-uuid.so
export PGSQL_NAME=$(pwd)/pgsql/libossp-uuid.so
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%configure \
    --disable-static \
    --without-perl \
    --without-php \
    --with-dce \
    --with-cxx \
    --without-pgsql

make LIBTOOL=/usr/bin/libtool CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so.*.*.*

%files
%defattr(-,root,root,-)
%license README
%{_bindir}/uuid
%{_libdir}/libossp-uuid.so.*

%files c++
%defattr(-,root,root,-)
%{_libdir}/libossp-uuid++.so.*

%files dce
%defattr(-,root,root,-)
%{_libdir}/libossp-uuid_dce.so.*

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_bindir}/%{name}-config*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.6.2-26
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.6.2-25
- Mass rebuild 2013-12-27

* Fri Nov 01 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-24
- revert perl changes from last change

* Wed Oct 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-23
- drop uuid-pgsql subpackage, it is outdated and does not work, use 
  uuid-ossp module from postgresql-contrib instead

* Mon Sep 02 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-21
- rebuild after php abi change

* Wed Jul 31 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-20
- drop last man page change, that option is just for compatibility
- fix NAME section of man pages to be whatis friendly

* Mon Jun 03 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-19
- fix multilib issue

* Thu May 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-18
- describe -r in man page

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.6.2-17
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-15
- make uuid-php compatible with php 5.4 (#873594)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.6.2-13
- Perl 5.16 rebuild

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-12
- enforce usage of our c(xx)flags

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-11
- fix debuginfo

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-10
- fix generation of MAC address based uuids (#829532), 
  patch by Philip Prindeville

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.6.2-9
- Perl 5.16 rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.6.2-8
- build against php 5.4, with patch
- add filter_provides to avoid private-shared-object-provides shout.so
- add minimal %%check for php extension

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.2-6
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 1.6.2-5
- fix php_zend_api check

* Thu Mar 03 2011 Karsten Hopp <karsten@redhat.com> 1.6.2-4
- fix build

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.2-2
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-1
- updated to 1.6.2
- uuid-config man page moved to sub-package containing uuid-config (#562838)

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 1.6.1-10
- silence rpmlint by using $(pwd) instead of shell variable RPM_SOURCE_DIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.6.1-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.6.1-7
- rebuild for new PHP 5.3.0 ABI (20090626)
- add PHP ABI check
- use php_extdir
- add php configuration file (/etc/php.d/uuid.ini)

* Thu May  7 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-6
- Using plain old "Requires: pkgconfig" instead -- see my post to
  fedora-devel-list made today.

* Mon May  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-5
- Replace expensive %%{_libdir}/pkgconfig dependency in uuid-devel
  with pkgconfig%%{_isa} for Fedora >= 11 (#484849).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-3
- Rebuild for new perl

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-2
- forgot to cvs add patch

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-1
- 1.6.1

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-4
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6.0-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.6.0-2
- Rebuild for selinux ppc32 issue.

* Tue Jul 24 2007 Steven Pritchard <steve@kspei.com> 1.6.0-1
- Update to 1.6.0.
- BR Test::More.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.5.1-3
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.5.1-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 1.5.1-1
- Update to 1.5.1.

* Sat Jul 29 2006 Steven Pritchard <steve@kspei.com> 1.5.0-1
- Update to 1.5.0.
- Rename libuuid* to libossp-uuid*, uuid.3 to ossp-uuid.3, and uuid.pc
  to ossp-uuid.pc to avoid conflicts with e2fsprogs-devel (#198520).
- Clean out the pgsql directory.  (Some cruft shipped with this release.)

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1.4.2-4
- Remove static php module.

* Tue May 23 2006 Steven Pritchard <steve@kspei.com> 1.4.2-3
- Force use of system libtool.
- Make libs executable.

* Tue May 23 2006 Steven Pritchard <steve@kspei.com> 1.4.2-2
- License is MIT(-ish).

* Fri May 19 2006 Steven Pritchard <steve@kspei.com> 1.4.2-1
- Initial packaging attempt.
