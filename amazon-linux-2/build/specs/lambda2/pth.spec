Summary:        The GNU Portable Threads library
Name:           pth
Version:        2.0.7
Release: 23%{?dist}.0.2
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.gnu.org/software/pth/
Source:         ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz.sig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Fedora customization, keep -g in the compiler options
Patch1:         pth-2.0.7-dont-remove-gcc-g.patch
# Fedora customization, fix arch-dependent conflicts in pth-config script
Patch2:         pth-2.0.7-config-script.patch
# Fedora customization, let build fail if running test_std fails
Patch3:         pth-2.0.7-test_std.patch
# bz 744740 / patch from Mikael Pettersson
Patch4: pth-2.0.7-linux3.patch

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications.
All threads run in the same address space of the server application,
but each thread has it's own individual program-counter, run-time
stack, signal mask and errno variable.

%package devel
Summary:        Development headers and libraries for GNU Pth
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.


%prep
%setup -q
%patch1 -p1 -b .dont-remove-gcc-g
%patch2 -p1 -b .config-script
%patch3 -p1 -b .test_std
%patch4 -p1 -b .no-linux3


%build
OUR_CFLAGS="${RPM_OPT_FLAGS} -D_FILE_OFFSET_BITS=64"

%ifarch %{arm}
OUR_CFLAGS=$(echo "${OUR_CFLAGS}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=0/g')
# guard
echo "${OUR_CFLAGS}" | grep FORTIFY_SOURCE=0
%endif

CFLAGS="${OUR_CFLAGS}"
%configure --disable-static ac_cv_func_sigstack='no'

# Work around multiarch conflicts in the pth-config script in order
# to complete patch2. Make the script choose between /usr/lib and
# /usr/lib64 at run-time.
if [ "%_libdir" == "/usr/lib64" ] ; then
    if grep -e '^pth_libdir="/usr/lib64"' pth-config ; then
        sed -i -e 's!^pth_libdir="/usr/lib64"!pth_libdir="/usr/lib"!' pth-config
    else
        echo "ERROR: Revisit the multiarch pth_libdir fixes for pth-config!"
        exit 1
    fi
fi
if [ -v OUR_CFLAGS ] && grep -e "${OUR_CFLAGS}" pth-config ; then
    # Remove our extra CFLAGS from the pth-config script, since they
    # don't belong in there.
    [ -n "${OUR_CFLAGS}" ] && sed -i -e "s!${OUR_CFLAGS}!!g" pth-config
else
    echo "ERROR: Revisit the multiarch CFLAGS fix for pth-config!"
    exit 1
fi

# this is necessary; without it make -j fails
make pth_p.h
make %{?_smp_mflags}


%check
make test
l=$($(pwd)/pth-config --libdir)
if [ "%{_libdir}" == "/usr/lib64" ]; then
    [ "$l" == "/usr/lib64" ]
fi


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ANNOUNCE AUTHORS COPYING ChangeLog HISTORY NEWS PORTING README
%doc SUPPORT TESTS THANKS USERS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/*/*
%{_datadir}/aclocal/*


%changelog
* Fri Aug 1 2014 Jeff Law <law@redhat.com>  - 2.0.7-23
- update pth-config for ppc64le

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.0.7-22
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.7-21
- Mass rebuild 2013-12-27

* Thu Nov 14 2013 Jeff Law <law@redhat.com>  - 2.0.7-20
- update pth-config for Aarch64

* Wed Feb 20 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-19
- Build with -D_FILE_OFFSET_BITS=64 to get stat64 in pth_high.c
- Guard the ARM CFLAGS sed substitution.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-16
- Apply Linux 3 configure check patch from Mikael Pettersson (#744740).

* Wed Jan  4 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-15
- rebuild for GCC 4.7 as requested

* Wed Nov 16 2011 Dan Horák <dan[at]danny.cz> - 2.0.7-14
- update pth-config for s390x and sparc64

* Mon Oct 31 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-13
- Let build fail if test_std fails.
- Fix previous commit, so pth-config CFLAGS check passes again.

* Mon Oct 31 2011 Chris Tyler <chris@tylers.info> - 2.0.7-12
- Removed FORTIFY_SOURCE for %%{arm} archs per Ajay Ramaswamy <ajayr@krithika.net>
- See https://bugzilla.redhat.com/show_bug.cgi?id=750243

* Fri Sep 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-11
- Use %%_isa in -devel package dependency.
- Use %%_libdir not %%ifarch in %%check section.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat May 31 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-7
- Drop "|| :" from check section. It failed to build for mdomsch
  in Rawhide today.

* Fri Feb 08 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-6
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Sun Oct 21 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-5
- Patch pth-config.
  This shall fix the multiarch conflict in pth-devel (#342961).
  It must not return -I/usr/include and -L/usr/{lib,lib64} either,
  since these are default search paths already.
- Replace the config.status CFLAGS sed expr with a patch.

* Tue Aug 21 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Thu Aug  2 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-2
- Clarify licence (LGPLv2+).

* Sat Nov 25 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7 (very minor maintenance updates only).

* Mon Aug 28 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.6-3
- rebuilt

* Mon May 22 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.6-2
- Insert -g into CFLAGS after configure script removes it.
- Disable configure check for obsolete sigstack(), which segfaults.

* Thu Feb 16 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6.

* Fri Oct  7 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5.
- Don't build static archive.

* Fri May 13 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.4-3
- rebuilt

* Thu Apr  7 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.4-2
- rebuilt

* Thu Feb 24 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0:2.0.4-1
- Update to 2.0.4.
- Remove ancient changelog entries which even pre-date Fedora.

* Tue Dec 14 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:2.0.3-1
- Update to 2.0.3, minor and common spec adjustments + LGPL, %%check,
  use URLs for official GNU companion sites.

* Thu Oct 07 2004 Adrian Reber <adrian@lisas.de> - 0:2.0.2-0.fdr.2
- iconv-ing spec to utf8

* Wed Oct 06 2004 Adrian Reber <adrian@lisas.de> - 0:2.0.2-0.fdr.1
- Update to 2.0.2 and current Fedora guidelines.
- added workaround for make -j problem

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0.0-0.fdr.1
- Update to 2.0.0 and current Fedora guidelines.
- Exclude %%{_libdir}/*.la

* Fri Feb  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.4.1-1.fedora.1
- First Fedora release, based on Ryan Weaver's work.
- Move (most of) docs to main package.

