%define datrie_version 0.2.3

Summary:  Thai language support routines
Name: libthai
Version: 0.1.14
Release: 9%{?dist}.0.2
License: LGPLv2+
Group: System Environment/Libraries
Source: ftp://linux.thai.net/pub/thailinux/software/libthai/libthai-%{version}.tar.gz
Source1: ftp://linux.thai.net/pub/thailinux/software/libthai/libdatrie-%{datrie_version}.tar.gz
Patch: libthai-libdatrie-static-build.patch
Patch1: libthai-0.1.9-doxygen-segfault.patch
Patch2: libthai-0.1.9-multilib.patch
URL: http://linux.thai.net
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig
BuildRequires: doxygen
# we edit the Makefile.am's
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool

%description
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their applications.
It includes important Thai-specific functions e.g. word breaking, input and
output methods as well as basic character and string supports.

%package devel
Summary:  Thai language support routines
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libthai-devel package includes the header files and developer docs 
for the libthai package.

Install libthai-devel if you want to develop programs which will use
libthai.

%prep
%setup -q -n %{name}-%{version} -a 1
mv libdatrie-%{datrie_version} libdatrie
%patch -p1 -b .static-build
%patch1 -p1 -b .doxygen-segfault
%patch2 -p1 -b .multilib

%build

# libthai depends on this library called libdatrie.  libdatrie is a
# data-structure implementaiton that the author of libthai ripped out of it.
# However, since libthai is the only user of that code, there's no reason to
# 1) package it separately, 2) use it as a shared library.
# So, we compile it as a libtool convenience library and include in libthai.so,
# and use symbol hiding to hide them (and other internal symbols).
#
# The patch takes care of making datrie into a convenience lib and making sure
# libthai will include it (and hide its symbols), and the exports make sure
# libthai finds the uninstalled libdatrie.  We need to call automake, since
# the patch modifies a few Makefile.am's.

{
  pushd libdatrie
  mkdir m4
  autoreconf -i -f
  %configure
  make
  popd
}

export DATRIE_CFLAGS="-I$PWD/libdatrie"
export DATRIE_LIBS="$PWD/libdatrie/datrie/libdatrie.la"
export PATH="$PWD/libdatrie/tools:$PATH"

autoreconf -i -f

%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# move installed doc files back to build directory to package them
# in the right place
mkdir installed-docs
mv $RPM_BUILD_ROOT%{_docdir}/libthai/* installed-docs
rmdir $RPM_BUILD_ROOT%{_docdir}/libthai

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README AUTHORS COPYING ChangeLog TODO
%{_libdir}/lib*.so.*
%{_datadir}/libthai

%files devel
%defattr(-, root, root)
%doc installed-docs/*
%{_includedir}/thai
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.1.14-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.1.14-8
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Behdad Esfahbod <behdad@redhat.com> - 0.1.14-3
- Update to 0.1.14

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.12-1
- Update to 0.1.12

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.9-7
- Fix the build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.9-5
- fix license tag

* Mon Mar 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.9-4
- Attempt to fix multilib conflict

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.9-3
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.9-2
- Add libthai-0.1.9-doxygen-segfault.patch to workaround doxygen segfault

* Tue Aug 28 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.9-1
- Update to 0.1.9
- Adjust patch

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.1.7-6
- Rebuild for build ID

* Tue Jan 22 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-5
- Export _th_*_tbl symbols too.  They are accessed by some of the macros.

* Tue Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-4
- Patch libthai.pc.in to not require datrie.

* Tue Jan 16 2007 Matthias Clasen <mclasen@redhat.com> 0.1.7-3
- Miscellaneous fixes
 
* Tue Jan 16 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-2
- Apply comments from Matthias Clasen (#222611) 
- devel summary improvement
- devel require pkgconfig
- configure --disable-static
- Add comments about the voodoo
- Install docs in the right place

* Sun Jan 14 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-1
- Initial package based on package by Supphachoke Suntiwichaya
  and Kamthorn Krairaksa for the OLPC.
