Name:    libatomic_ops
Summary: Atomic memory update operations
Version: 7.6.2
Release: 3%{?dist}.0.1

# libatomic_ops MIT, libatomic_ops_gpl GPLv2
License: GPLv2 and MIT
#URL:    http://www.hboehm.info/gc/
URL:     https://github.com/ivmai/libatomic_ops/
Source0: https://github.com/ivmai/libatomic_ops/releases/download/v%{version}/libatomic_ops-%{version}.tar.gz
# updated GPLv2 license text
Source1: http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

## upstream patches
# 7.4 branch

# master branch

## upstreamable patches
# https://bugzilla.redhat.com/show_bug.cgi?id=1096574
Patch500: gc_ppc64le_force_AO_load.patch

# re-autofoo for patch2 (and others)
BuildRequires: automake libtool

%description
Provides implementations for atomic memory update operations on a
number of architectures. This allows direct use of these in reasonably
portable code. Unlike earlier similar packages, this one explicitly
considers memory barrier semantics, and allows the construction of code
that involves minimum overhead across a variety of architectures.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Files for developing with %{name}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
Files for developing with %{name} and linking statically.


%prep
%autosetup -p1

# refresh stuff here to be rid of rpath
autoreconf -fi

install -m644 -p %{SOURCE1} ./COPYING


%build
%configure \
  --enable-shared \
  --disable-silent-rules

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

## unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la
# omit dup'd docs
rm -fv %{buildroot}%{_docdir}/libatomic_ops/{COPYING,README*,*.txt}


%check
## ignore failures on powerpc, atomic stack feature not working (#883748)
#ifarch ppc ppc64 ppc64le aarch64
#global arch_ignore ||:
#endif
make check %{?arch_ignore}

%ldconfig_scriptlets

%files
%license COPYING
%license doc/LICENSING.txt
%doc AUTHORS ChangeLog README.md
%{_libdir}/libatomic_ops.so.1*
%{_libdir}/libatomic_ops_gpl.so.1*

%files devel
%doc doc/README*
%{_includedir}/atomic_ops.h
%{_includedir}/atomic_ops_malloc.h
%{_includedir}/atomic_ops_stack.h
%{_includedir}/atomic_ops/
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%files static
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a


%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.6.2-2
- Switch to %%ldconfig_scriptlets

* Fri Dec 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.6.2-1
- libatomic_ops-7.6.2 (#1528830)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.4.6-1
- libatomic_ops-7.4.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.4.4-1
- libatomic_ops-7.4.4 (#1346524)

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-9
- make check fails on test_stack for ppc64le arch (#1096574), drop reference to 0032.patch

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.4.2-8
- pull in upstream (7.4 branch) fixes
- Add support for 64-bit MIPS (#1317509)
- use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 7.4.2-6
- Don't fail check on aarch64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-2
- link libatomic_ops_gpl against libatomic_ops for missing symbol(s)

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-1
- libatomic_opts-7.4.2
- new upstream/source URLs
- %%check: skip ppc64le too
- License: MIT and GPLv2
- update/longer %%description
- updated GPLv2 license text (with correct address)

* Wed Dec 04 2013 Rex Dieter <rdieter@fedoraproject.org>  7.4.0-1
- separate libatomic_ops lives again!

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-8.gc
- use gc tarball, tag gc release

* Thu Jul 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-7
- devel: Provides: %%name-static ...
- consolidate %%doc's
- %%files: track libs

* Wed May 20 2009 Dan Horak <dan[t]danny.cz> - 1.2-6
- added fix for s390

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Jon Stanley <jonstanley@gmail.com> - 1.2-4
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-3
- Autorebuild for GCC 4.3

* Tue May 29 2007 Pierre Ossman <drzeus@drzeus.cx> 1.2-2
- Added fix for PPC AO_load_acquire.

* Fri Nov 10 2006 Pierre Ossman <drzeus@drzeus.cx> 1.2-1
- Update to 1.2.

* Sat Sep  9 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-2
- Fix naming of package.
- General cleanup of spec file.

* Wed Aug 30 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-1
- Initial package for Fedora Extras.
