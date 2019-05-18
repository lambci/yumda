%define _trivial .0
%define _buildid .1

Summary: Library for error values used by GnuPG components
Name: libgpg-error
Version: 1.12
Release: 3%{?dist}.0.3
URL: ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Source0: ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2.sig
Group: System Environment/Libraries
License: LGPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gawk, gettext, autoconf, automake, gettext-devel, libtool
%if 0%{?fedora} > 13
BuildRequires: gettext-autopoint
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Patch1000: amzn2-inhibit-linemarkers-that-confuse-errno-parser.patch

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

%prep
%setup -q
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g;s|@GPG_ERROR_CONFIG_HOST@|none|g' src/gpg-error-config.in

# We need a version of libtool that won't decide to add an rpath of /usr/lib64
# even when we ask it not to.
autoreconf -f -i

%patch1000 -p1

%build
%configure --disable-static --disable-rpath --disable-languages
make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%find_lang %{name}

# Relocate the shared libraries to /%{_lib}.
mkdir -p $RPM_BUILD_ROOT/%{_lib}
for shlib in $RPM_BUILD_ROOT/%{_libdir}/*.so* ; do
	if test -L "$shlib" ; then
		rm "$shlib"
	else
		mv "$shlib" $RPM_BUILD_ROOT/%{_lib}/
	fi
done
# Figure out where /%{_lib} is relative to %{_libdir}.
touch $RPM_BUILD_ROOT/root_marker
relroot=..
while ! test -f $RPM_BUILD_ROOT/%{_libdir}/$relroot/root_marker ; do
	relroot=$relroot/..
done
# Overwrite development symlinks.
pushd $RPM_BUILD_ROOT/%{_libdir}
for shlib in $relroot/%{_lib}/lib*.so.* ; do
	shlib=`echo "$shlib" | sed -e 's,//,/,g'`
	target=`basename "$shlib" | sed -e 's,\.so.*,,g'`.so
	ln -sf $shlib $target
done
popd
# Add the soname symlink.
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_lib}/
rm -f $RPM_BUILD_ROOT/root_marker

%check
make check

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING COPYING.LIB AUTHORS README NEWS ChangeLog
%{_bindir}/gpg-error
/%{_lib}/libgpg-error.so.0*

%files devel
%defattr(-,root,root)
%{_bindir}/gpg-error-config
%{_libdir}/libgpg-error.so
%{_includedir}/gpg-error.h
%{_datadir}/aclocal/gpg-error.m4

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.12-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.12-2
- Mass rebuild 2013-12-27

* Fri Aug 23 2013 Tomáš Mráz <tmraz@redhat.com> 1.12-1
- new upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Tomáš Mráz <tmraz@redhat.com> 1.11-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Tomáš Mráz <tmraz@redhat.com> 1.10-1
- new upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 23 2010 Rex Dieter <rdieter@fedoraproject.org> 1.9-1
- libgpg-error-1.9

* Thu Feb 25 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-3
- turn off common lisp bindings the right way
- drop finger output
- recode the changelog into UTF-8 if it isn't UTF-8 (rpmlint)

* Mon Jan 11 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-2
- fix use of macro in changelog (rpmlint)
- build with --disable-rpath (rpmlint)
- build with %%{?_smp_mflags}

* Thu Oct 15 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-1
- long-overdue update to 1.7
- add a disttag

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6-2
- Autorebuild for GCC 4.3

* Fri Dec  7 2007 Nalin Dahyabhai <nalin@redhat.com>
- remove the generic install docs (#226021)

* Fri Dec  7 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.6-1
- update to 1.6
- add suggested summary, buildrequires, and modify install call as suggested
  by package review (#226021)

* Mon Oct 15 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-6
- use ldconfig to make the soname symlink so that it gets packaged (#331241)

* Wed Aug 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-5
- add missing gawk buildrequirement

* Thu Aug 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-4
- clarify license

* Mon Jul 30 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-3
- disable static libraries (part of #249815)

* Fri Jul 27 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-2
- move libgpg-error shared library to /%%{_lib} (#249816)

* Thu Jul 19 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-1
- update to 1.5

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Bill Nottngham <notting@redhat.com> - 1.4-1
- update to 1.4
- don't ship lisp bindings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3-3.1
- rebuild

* Mon Jun  5 2006 Nalin Dahyabhai <nalin@redhat.com> 1.3-3
- give gpg-error-config libdir=@exec_prefix@/lib instead of @libdir@, so that
  it agrees on 32- and 64-bit arches (it suppresses the -L argument if @libdir@
  is /usr/lib, so this should be cleaner than adding a non-standard .pc file
  which upstream developers might inadvertently think they can depend to be on
  every system which provides this library)

* Mon May 15 2006 Karsten Hopp <karsten@redhat.de> 1.3-2
- switch to pkgconfig so that gpg-error-config can be the same on 
  32bit and 64bit archs

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.3-1
- update to version 1.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karsten Hopp <karsten@redhat.de> 1.1-1
- update

* Wed Mar  2 2005 Bill Nottingham <notting@redhat.com> - 1.0-2
- we can rebuild it. we have the technology.

* Tue Aug 31 2004 Bill Nottingham <notting@redhat.com> - 1.0-1
- update to 1.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> - 0.7-1
- adapt upstream specfile
