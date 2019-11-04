Name:           libarchive
Version:        3.1.2
Release:        12%{?dist}
Summary:        A library for handling streaming archive formats

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.libarchive.org/
Source0:        http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: bison
BuildRequires: sharutils
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: lzo-devel
BuildRequires: e2fsprogs-devel
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: automake autoconf libtool


# CVE-2013-0211 libarchive: read buffer overflow on 64-bit systems
# https://bugzilla.redhat.com/show_bug.cgi?id=927105
Patch0: libarchive-3.1.3-CVE-2013-0211_read_buffer_overflow.patch

Patch1: libarchive-3.1.2-testsuite.patch

# A bunch of security patches from 2016 summer
Patch2: libarchive-3.1.2-rhbz-1347085.patch
Patch3: libarchive-3.1.2-rhbz-1347086.patch
Patch4: libarchive-3.1.2-CVE-2015-8916-CVE-2015-8917.patch
Patch5: libarchive-3.1.2-CVE-2015-8919.patch
Patch6: libarchive-3.1.2-CVE-2015-8920.patch
Patch7: libarchive-3.1.2-CVE-2015-8921.patch
Patch8: libarchive-3.1.2-CVE-2015-8922.patch
Patch9: libarchive-3.1.2-CVE-2015-8923.patch
Patch10: libarchive-3.1.2-CVE-2015-8924.patch
Patch11: libarchive-3.1.2-CVE-2015-8925.patch
Patch12: libarchive-3.1.2-CVE-2015-8926.patch
Patch13: libarchive-3.1.2-CVE-2015-8928.patch
Patch14: libarchive-3.1.2-CVE-2015-8930.patch
Patch15: libarchive-3.1.2-CVE-2015-8931.patch
Patch16: libarchive-3.1.2-CVE-2015-8932.patch
Patch17: libarchive-3.1.2-CVE-2015-8934.patch
Patch18: libarchive-3.1.2-CVE-2016-4300.patch
Patch19: libarchive-3.1.2-CVE-2016-4302.patch
Patch20: libarchive-3.1.2-CVE-2016-4809.patch
Patch21: libarchive-3.1.2-CVE-2016-5844.patch
Patch22: libarchive-3.1.2-CVE-2016-1541.patch
Patch23: libarchive-3.1.2-CVE-2016-5418.patch
Patch24: libarchive-3.1.2-CVE-2016-5418-variation.patch
Patch25: libarchive-3.1.2-CVE-2017-14503.patch
Patch26: libarchive-3.1.2-CVE-2019-1000019.patch
Patch27: libarchive-3.1.2-CVE-2019-1000020.patch
Patch28: libarchive-3.3.2-CVE-2018-1000878.patch
Patch29: libarchive-3.3.2-CVE-2018-1000877.patch

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n     bsdtar
Summary:        Manipulate tape archives
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description -n bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n     bsdcpio
Summary:        Copy files to and from archives
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description -n bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.

%global _hardened_build 1

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .CVE-2013-0211
# fix bugs in testsuite
# ~> upstream ~> 26629c191a & b539b2e597 & 9caa49246
%patch1 -p1 -b .fix-testsuite

%patch2 -p1 -b .rhbz-1347085
%patch3 -p1 -b .rhbz-1347086
%patch4 -p1 -b .CVE-2015-8916-CVE-2015-8917
%patch5 -p1 -b .CVE-2015-8919
%patch6 -p1 -b .CVE-2015-8920
%patch7 -p1 -b .CVE-2015-8921
%patch8 -p1 -b .CVE-2015-8922
%patch9 -p1 -b .CVE-2015-8923
%patch10 -p1 -b .CVE-2015-8924
%patch11 -p1 -b .CVE-2015-8925
%patch12 -p1 -b .CVE-2015-8926
%patch13 -p1 -b .CVE-2015-8928
%patch14 -p1 -b .CVE-2015-8930
%patch15 -p1 -b .CVE-2015-8931
%patch16 -p1 -b .CVE-2015-8932
%patch17 -p1 -b .CVE-2015-8934
%patch18 -p1 -b .CVE-2016-4300
%patch19 -p1 -b .CVE-2016-4302
%patch20 -p1 -b .CVE-2016-4809
%patch21 -p1 -b .CVE-2016-5844
%patch22 -p1 -b .CVE-2016-1541
%patch23 -p1 -b .CVE-2016-5418
%patch24 -p1 -b .CVE-2016-5418-var
%patch25 -p1 -b .CVE-2017-14503
%patch26 -p1 -b .CVE-2019-1000019
%patch27 -p1 -b .CVE-2019-1000020
%patch28 -p1 -b .CVE-2019-1000878
%patch29 -p1 -b .CVE-2019-1000877


%build
build/autogen.sh
%configure --disable-static --disable-rpath
# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

test -z "$V" && verbose_make="V=1"
make %{?_smp_mflags} $verbose_make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
run_testsuite()
{
    LD_LIBRARY_PATH=`pwd`/.libs make check -j1
    res=$?
    echo $res
    if [ $res -ne 0 ]; then
        # error happened - try to extract in koji as much info as possible
        cat test-suite.log
        echo "========================="
        err=`cat test-suite.log | grep "Details for failing tests" | cut -d: -f2`
        for i in $err; do
            find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
            echo "-------------------------"
            cat $i/*.log
        done
        return 1
    else
        find -name '*_test.log' -exec cat {} +
        return 0
    fi
}

# On a ppc/ppc64 is some race condition causing 'make check' fail on ppc
# when both 32 and 64 builds are done in parallel on the same machine in
# koji.  Try to run once again if failed.
%ifarch ppc
run_testsuite || run_testsuite
%else
run_testsuite
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_libdir}/libarchive.so.13*
%{_mandir}/*/cpio.*
%{_mandir}/*/mtree.*
%{_mandir}/*/tar.*

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*.h
%{_mandir}/*/archive*
%{_mandir}/*/libarchive*
%{_libdir}/libarchive.so
%{_libdir}/pkgconfig/libarchive.pc

%files -n bsdtar
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_bindir}/bsdtar
%{_mandir}/*/bsdtar*

%files -n bsdcpio
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_bindir}/bsdcpio
%{_mandir}/*/bsdcpio*


%changelog
* Tue Apr 30 2019 Ondrej Dubaj <odubaj@redhat.com> - 3.1.2-12
- fixed use after free in RAR decoder (#1700749)
- fixed double free in RAR decoder (#1700748)

* Fri Feb 22 2019 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-11
- fix out-of-bounds read within lha_read_data_none() (CVE-2017-14503)
- fix crash on crafted 7zip archives (CVE-2019-1000019)
- fix infinite loop in ISO9660 (CVE-2019-1000020)

* Fri Aug 12 2016 Petr Kubat <pkubat@redhat.com> - 3.1.2-10
- Fixes variation of CVE-2016-5418: Hard links could include ".." in their path.

* Thu Aug 11 2016 Petr Kubat <pkubat@redhat.com> - 3.1.2-9
- Fixes CVE-2016-5418: Archive Entry with type 1 (hardlink) causes file overwrite (#1365777)

* Fri Jul 08 2016 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-8
- a bunch of security fixes (rhbz#1353065)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.1.2-7
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1.2-6
- Mass rebuild 2013-12-27

* Mon Jul 22 2013 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-5
- try to workaround racy testsuite fail

* Sun Jun 30 2013 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-4
- enable testsuite in the %%check phase

* Mon Jun 24 2013 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-3
- bsdtar/bsdcpio should require versioned libarchive

* Wed Apr  3 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-2
- Remove libunistring-devel build require

* Thu Mar 28 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Fix CVE-2013-0211: read buffer overflow on 64-bit systems (#927105)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1
- NEWS seems to be valid UTF-8 nowadays

* Wed Oct 03 2012 Pavel Raiskup <praiskup@redhat.com> - 3.0.4-3
- better install manual pages for libarchive/bsdtar/bsdcpio (# ... )
- several fedora-review fixes ...:
- Source0 has moved to github.com
- remove trailing white spaces
- repair summary to better describe bsdtar/cpiotar utilities

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Wed Feb  1 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.0.3-2
- Enable bsdtar and bsdcpio in separate subpackages (#786400)

* Fri Jan 13 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.3.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.2.a
- track files/sonames closer, so abi bumps aren't a surprise
- tighten subpkg deps via %%_isa

* Mon Nov 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-0.1.a
- Update to 3.0.0a (alpha release)

* Mon Sep  5 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.8.5-1
- Update to 2.8.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.8.4-2
- Rebuild for new xz-libs

* Wed Jun 30 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.4-1
- Update to 2.8.4

* Fri Jun 25 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.3-2
- Fix ISO9660 reader data type mismatches (#597243)

* Tue Mar 16 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.3-1
- Update to 2.8.3

* Mon Mar  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.1-1
- Update to 2.8.1

* Fri Feb  5 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Wed Jan  6 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.7.902a-1
- Update to 2.7.902a

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.7.1-2
- rebuilt with new openssl

* Fri Aug  7 2009 Tomas Bzatek <tbzatek@redhat.com> 2.7.1-1
- Update to 2.7.1
- Drop deprecated lzma dependency, libxz handles both formats

* Mon Jul 27 2009 Tomas Bzatek <tbzatek@redhat.com> 2.7.0-3
- Enable XZ compression format

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Tomas Bzatek <tbzatek@redhat.com> 2.7.0-1
- Update to 2.7.0

* Fri Mar  6 2009 Tomas Bzatek <tbzatek@redhat.com> 2.6.2-1
- Update to 2.6.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tomas Bzatek <tbzatek@redhat.com> 2.6.1-1
- Update to 2.6.1

* Thu Jan  8 2009 Tomas Bzatek <tbzatek@redhat.com> 2.6.0-1
- Update to 2.6.0

* Mon Dec 15 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.904a-1
- Update to 2.5.904a

* Tue Dec  9 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.903a-2
- Add LZMA support

* Mon Dec  8 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.903a-1
- Update to 2.5.903a

* Tue Jul 22 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.5-1
- Update to 2.5.5

* Wed Apr  2 2008 Tomas Bzatek <tbzatek@redhat.com> 2.4.17-1
- Update to 2.4.17

* Wed Mar 19 2008 Tomas Bzatek <tbzatek@redhat.com> 2.4.14-1
- Initial packaging
