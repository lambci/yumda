
Name:    gpgme
Summary: GnuPG Made Easy - high level crypto API
Version: 1.3.2
Release: 5%{?dist}.0.2

License: LGPLv2+
Group:   Applications/System
URL:     http://www.gnupg.org/related_software/gpgme/
Source0: ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2.sig
Source2: gpgme-multilib.h
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: gpgme-1.3.2-config_extras.patch

# fix ImplicitDSOLinking in tests/, upstreamable
Patch2:  gpgme-1.3.2-ImplicitDSOLinking.patch

# add -D_FILE_OFFSET_BITS... to gpgme-config, upstreamable
Patch3:  gpgme-1.3.2-largefile.patch

BuildRequires: gawk
BuildRequires: gnupg2
BuildRequires: gnupg2-smime
BuildRequires: libgpg-error-devel
BuildRequires: pth-devel
BuildRequires: libassuan2-devel

%define _with_gpg --with-gpg=%{_bindir}/gpg2
Requires: gnupg2

# On the following architectures workaround multiarch conflict of -devel packages:
%define multilib_arches %{ix86} x86_64 ia64 ppc ppc64 s390 s390x %{sparc}

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.  It provides a high-level crypto API for
encryption, decryption, signing, signature verification and key
management.

%package devel
Summary:  Development headers and libraries for %{name}
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libgpg-error-devel%{?_isa}
# http://bugzilla.redhat.com/676954
# TODO: see if -lassuan can be added to config_extras patch too -- Rex
#Requires: libassuan2-devel
# /usr/share/aclocal ownership
#Requires: automake
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
%description devel
%{summary}


%prep
%setup -q

%patch1 -p1 -b .config_extras
%patch2 -p1 -b .ImplicitDSOLinking
%patch3 -p1 -b .largefile

## HACK ALERT
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' src/gpgme-config.in

%build
%configure \
  --disable-static \
  --without-g13 \
  %{?_with_gpg}

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/common-lisp/source/gpgme/

# Hack to resolve multiarch conflict (#341351)
%ifarch %{multilib_arches}
mv $RPM_BUILD_ROOT%{_bindir}/gpgme-config{,.%{_target_cpu}}
cat > gpgme-config-multilib.sh <<__END__
#!/bin/sh
exec %{_bindir}/gpgme-config.\$(arch) \$@
__END__
install -D -p gpgme-config-multilib.sh $RPM_BUILD_ROOT%{_bindir}/gpgme-config
mv $RPM_BUILD_ROOT%{_includedir}/gpgme.h \
   $RPM_BUILD_ROOT%{_includedir}/gpgme-%{__isa_bits}.h
install -m644 -p -D %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/gpgme.h
%endif


%check 
make -C tests check 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* ChangeLog NEWS README* THANKS TODO VERSION
%{_libdir}/libgpgme.so.11*
%{_libdir}/libgpgme-pthread.so.11*

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ $1 -eq 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :
fi

%files devel
%defattr(-,root,root,-)
%{_bindir}/gpgme-config
%ifarch %{multilib_arches}
%{_bindir}/gpgme-config.%{_target_cpu}
%{_includedir}/gpgme-%{__isa_bits}.h
%endif
%{_includedir}/gpgme.h
%{_libdir}/libgpgme*.so
%{_datadir}/aclocal/gpgme.m4
%{_infodir}/gpgme.info*


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.3.2-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.2-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.3.2-2
- minor spec cleanup

* Wed Sep 26 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.2-1
- new upstream version
- re-enable gpg tests (original patch by John Morris <john@zultron.com>)
- quiet configure warning 'could not find g13'
- there is no libgpgme-pth anymore

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 22 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.0-8
- -devel: make Requires: libgpg-error-devel arch'd
- ensure gpgme-config wrapper is executable

* Sun Apr 22 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.0-7
- gpgme.h: fatal error: gpgme-i386.h: No such file or directory compilation terminated (#815116)

* Wed Feb 15 2012 Simon Lukasik <slukasik@redhat.com> - 1.3.0-6
- Resolve multilib conflict of gpgme-config (#341351)
- Resolve multilib conflict of gpgme.h (#341351)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 17 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.3.0-4
- gpgme-config: remove libassuan-related flags as threatened (#676954) 
\
* Sun Feb 13 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.3.0-3
- -devel: fix typo (broken dep)

* Sat Feb 12 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.3.0-2
- BR: libassuan2-devel
- gpgme-config outputs -lassuan (#676954)

* Fri Feb 11 2011 Tomas Mraz <tmraz@redhat.com> - 1.3.0-1
- new upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 18 2010 Tomas Mraz <tmraz@redhat.com> - 1.2.0-3
- fix the condition for adding the -D_FILE_OFFSET_BITS...

* Wed Aug 11 2010 Tomas Mraz <tmraz@redhat.com> - 1.2.0-2
- add -D_FILE_OFFSET_BITS... to gpgme-config as appropriate (#621698)

* Fri Jul 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2.0-1
- gpgme-1.2.0 (#610984)

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.8-4
- FTBFS gpgme-1.1.8-3.fc13: ImplicitDSOLinking (#564605)

* Thu Nov 19 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.8-3
- Add buildrequires gnupg2-smime for the gpgsm

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.8-1
- gpgme-1.1.8
- -devel: s/postun/preun/ info scriptlet

* Wed Mar 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.7-3
- track shlib sonames closer, to highlight future abi/soname changes
- _with_gpg macro, to potentially conditionalize gnupg vs gnupg2 defaults
  for various os/releases (ie, fedora vs rhel)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 18 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.7-1
- gpgme-1.1.7

* Sun Feb 17 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.6-3
- --with-gpg=%%_bindir/gpg2 (#432445)
- drop Requires: gnupg (#432445)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.1.6-2 
- respin (gcc43)

* Fri Jan 04 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.6-1
- gpgme-1.1.6
- multiarch conflicts in gpgme (#341351)

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.5-4
- BR: gawk

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.5-3
- respin (BuildID)

* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.5-2
- License: LGPLv2+

* Mon Jul 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.5-1
- gpgme-1.1.5

* Mon Mar 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.4-1
- gpgme-1.1.4

* Sat Feb 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.3-1
- gpgme-1.1.3

* Tue Oct 03 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- respin

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.2-6
- fix gpgme-config --thread=pthread --cflags

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.2-5
- fc6 respin

* Mon Mar 6 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.2-4
- add back support for gpgme-config --thread=pthread

* Mon Mar 6 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.2-2
- drop extraneous libs from gpgme-config

* Fri Mar 3 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1.2-1
- 1.1.2
- drop upstreamed gpgme-1.1.0-tests.patch

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Wed Nov 30 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.0-3
- (re)build against (newer) libksba/gnupg2

* Thu Oct 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.0-2
- 1.1.0

* Mon Aug  8 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.3-1
- 1.0.3
- --disable-static

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.2-3
- rebuilt

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.0.2-2
- Fix FC4 build.

* Tue Feb  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:1.0.2-1
- LGPL used here, and made summary more explicit.
- Remove dirmngr dependency (gpgsm interfaces with it).
- Obsolete cryptplug as gpgme >= 0.4.5 provides what we used cryptplug for.

* Thu Jan 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:1.0.2-0.fdr.1
- 1.0.2

* Thu Oct 21 2004 Rex Dieter <rexdieter at sf.net> 0:1.0.0-0.fdr.1
- 1.0.0
- Requires: dirmngr

* Tue Oct 19 2004 Rex Dieter <rexdieter at sf.net> 0:0.4.7-0.fdr.1
- 0.4.7

* Sun May  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.3-0.fdr.3
- Require %%{_bindir}/gpgsm instead of newpg.
- Cosmetic spec file improvements.

* Thu Oct 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.3-0.fdr.2
- Update description.

* Tue Oct  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.3-0.fdr.1
- Update to 0.4.3.

* Fri Aug 15 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.2-0.fdr.1
- Update to 0.4.2.
- make check in the %%check section.

* Thu Jul 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.1
- Update to 0.4.1.
- Make -devel cooperate with --excludedocs.

* Sat Apr 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.0-0.fdr.2
- BuildRequire pth-devel, fix missing epoch in -devel Requires (#169).
- Save .spec in UTF-8.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.0-0.fdr.1
- Update to current Fedora guidelines.
- Exclude %%{_libdir}/*.la.

* Tue Feb 12 2003 Warren Togami <warren@togami.com> 0.4.0-1.fedora.3
- info/dir temporary workaround

* Sat Feb  8 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.4.0-1.fedora.1
- First Fedora release.
