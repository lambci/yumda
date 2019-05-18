Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.28
Release: 4%{?dist}.0.2
URL: http://www.gnu.org/software/libidn/
License: LGPLv2+ and GPLv3+ and GFDL
Source0: http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
Group: System Environment/Libraries
BuildRequires: pkgconfig, gettext
%ifarch ppc64le
# libtool automatic fixing tool will touch things
BuildRequires: autoconf
%endif
Requires(post): /sbin/install-info /sbin/ldconfig
Requires(preun): /sbin/install-info
Requires(postun): /sbin/ldconfig
# gnulib is a copylib, bundling is allowed
Provides: bundled(gnulib)

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package devel
Summary: Development files for the libidn library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.

%package -n emacs-%{name}
Summary: GNU Emacs libidn support files
License: GPLv3+
BuildRequires: emacs
Requires: %{name} = %{version}-%{release}
Requires: emacs(bin) >= %{_emacs_version}
BuildArch: noarch

%description -n emacs-%{name}
This package includes libidn support files for GNU Emacs.

%prep
%setup -q

# Name directory sections consistently in the info file, #209491
sed -i '/^INFO-DIR-SECTION/{s/GNU Libraries/Libraries/;s/GNU utilities/Utilities/;}' doc/libidn.info

iconv -f ISO-8859-1 -t UTF-8 doc/libidn.info > iconv.tmp
mv iconv.tmp doc/libidn.info

%build
%configure --disable-csharp --disable-static --with-lispdir=%{_emacs_sitelispdir}/%{name}

# remove RPATH hardcoding
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%ifarch ppc64le
# ppc64le libtool fixing tool might have tweaked libtool.m4.
# Touch these files so aclocal-1.14 is not needed.
touch aclocal.m4 Makefile.in configure
%endif

make %{?_smp_mflags} V=1

%check
# without RPATH this needs to be set to test the compiled library
export LD_LIBRARY_PATH=$(pwd)/lib/.libs
make %{?_smp_mflags} -C tests check VALGRIND=env

%install
make install DESTDIR=$RPM_BUILD_ROOT pkgconfigdir=%{_libdir}/pkgconfig

# provide more examples
make %{?_smp_mflags} -C examples distclean

# clean up docs
find doc -name "Makefile*" | xargs rm
rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir

# Make multilib safe:
sed -i '/gnu compiler/d' $RPM_BUILD_ROOT%{_includedir}/idn-int.h

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la \
      $RPM_BUILD_ROOT%{_datadir}/info/*.png

%{_emacs_bytecompile} $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{name}/*.el

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS NEWS FAQ README THANKS COPYING*
%{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_libdir}/libidn.so.*
%{_infodir}/%{name}.info.gz

%files devel
%doc doc/libidn.html examples
%{_libdir}/libidn.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files -n emacs-%{name}
%{_emacs_sitelispdir}/%{name}

%changelog
* Fri Aug 22 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.28-4
- fix building on ppc64le (#1125577)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.28-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.28-2
- Mass rebuild 2013-12-27

* Thu Jul 18 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.28-1
- update to 1.28
- remove RPATH hardcoding
- move library to /usr

* Fri Jun 07 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.27-1
- update to 1.27
- make devel dependency arch-specific
- remove obsolete macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.26-1
- update to 1.26

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Joe Orton <jorton@redhat.com> - 1.25-2
- update to 1.25

* Tue May 15 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.24-2
- provide bundled(gnulib) (#821768)

* Sun Jan 15 2012 Robert Scheck <robert@fedoraproject.org> - 1.24-1
- Update to 1.24 (#781379)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.23-1
- update to 1.23

* Tue May 31 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.22-3
- Split emacs-libidn subpackage to avoid *.elc arch conflicts (#709136).

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.22-2
- Byte compile Emacs lisp files, require emacs-filesystem for dir ownership.

* Thu May 05 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.22-1
- update to 1.22

* Tue Apr 26 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.21-1
- update to 1.21

* Thu Mar 03 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.20-1
- update to 1.20
- fix requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 24 2010 Joe Orton <jorton@redhat.com> - 1.19-1
- update to 1.19 (#595086)

* Tue Mar 30 2010 Joe Orton <jorton@redhat.com> - 1.18-2
- add GFDL to License

* Mon Mar 29 2010 Joe Orton <jorton@redhat.com> - 1.18-1
- update to 1.18
- fix Source0 to reference gnu.org repository

* Fri Jan 29 2010 Joe Orton <jorton@redhat.com> - 1.16-1
- update to 1.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Joe Orton <jorton@redhat.com> 1.9-4
- update to 1.9 (#302111)
- update License to reflect GPLv3+ binaries, LGPLv2+ library

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Kedar Sovani <kedars@marvell.com> 0.6.14-9
- fix the problem with #include_next

* Tue Jun 10 2008 Joe Orton <jorton@redhat.com> 0.6.14-8
- fix build with latest autoconf (#449440)

* Mon Mar 31 2008 Joe Orton <jorton@redhat.com> 0.6.14-7
- fix libidn.pc for correct libdir (#439549)

* Fri Mar  7 2008 Joe Orton <jorton@redhat.com> 0.6.14-6
- drop libidn.a
- move shared library to /lib{,64} (#283651)

* Thu Feb  7 2008 Joe Orton <jorton@redhat.com> 0.6.14-5
- fix DT_RPATH in /usr/bin/idn
- convert libidn.iconv to UTF-8 (Jon Ciesla, #226029)
- fix BuildRoot tag (Jon Ciesla, #226029)

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 0.6.14-4
- drop contrib directory from docs

* Mon Aug 20 2007 Joe Orton <jorton@redhat.com> 0.6.14-3
- fix License

* Mon Jun 18 2007 Joe Orton <jorton@redhat.com> 0.6.14-2
- update to 0.6.14

* Mon Jan 29 2007 Joe Orton <jorton@redhat.com> 0.6.9-2
- update to 0.6.9
- make install-info use failsafe (Ville Skyttä, #223707)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 0.6.8-4
- use non-GNU section in info directory (#209491)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 0.6.8-3
- update to 0.6.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.5-1.1
- rebuild

* Fri Jul  7 2006 Joe Orton <jorton@redhat.com> 0.6.5-1
- update to 0.6.5

* Fri Jul  7 2006 Joe Orton <jorton@redhat.com> 0.6.4-1
- update to 0.6.4

* Thu Jun  1 2006 Joe Orton <jorton@redhat.com> 0.6.3-1
- update to 0.6.3
- fix some places where gettext() was not getting used

* Thu Jun  1 2006 Joe Orton <jorton@redhat.com> 0.6.2-4
- remove the libidn.la (#172639)

* Thu May 11 2006 Joe Orton <jorton@redhat.com> 0.6.2-3
- make idn-int.h multilib-safe

* Wed Feb 22 2006 Joe Orton <jorton@redhat.com> 0.6.2-2
- disable C# support (#182393)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.2-1.1
- bump again for double-long bug on ppc(64)

* Mon Feb 06 2006 Florian La Roche <laroche@redhat.com>
- 0.6.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 0.6.0-1
- update to 0.6.0

* Mon Oct 24 2005 Joe Orton <jorton@redhat.com> 0.5.20-1
- update to 0.5.20

* Mon Sep 19 2005 Joe Orton <jorton@redhat.com> 0.5.19-1
- update to 0.5.19

* Fri May 27 2005 Joe Orton <jorton@redhat.com> 0.5.17-1
- update to 0.5.17

* Fri May  6 2005 Joe Orton <jorton@redhat.com> 0.5.16-1
- update to 0.5.16

* Thu May  5 2005 Joe Orton <jorton@redhat.com> 0.5.15-2
- constify data tables in pr29.c
- clean up pre/post/postun requires

* Sun Mar 20 2005 Joe Orton <jorton@redhat.com> 0.5.15-1
- update to 0.5.15

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 0.5.13-2
- rebuild

* Mon Jan 31 2005 Joe Orton <jorton@redhat.com> 0.5.13-1
- update to 0.5.13

* Sun Dec  5 2004 Joe Orton <jorton@redhat.com> 0.5.12-1
- update to 0.5.12

* Mon Nov 29 2004 Joe Orton <jorton@redhat.com> 0.5.11-1
- update to 0.5.11 (#141094)

* Tue Nov  9 2004 Joe Orton <jorton@redhat.com> 0.5.10-1
- update to 0.5.10
- buildroot cleanup fix (Robert Scheck)

* Mon Nov  8 2004 Joe Orton <jorton@redhat.com> 0.5.9-1
- update to 0.5.9 (#138296)

* Thu Oct  7 2004 Joe Orton <jorton@redhat.com> 0.5.6-1
- update to 0.5.6 (#134343)

* Thu Sep 30 2004 Miloslav Trmac <mitr@redhat.com> - 0.5.4-3
- Fix Group: (#134068)

* Tue Aug 31 2004 Joe Orton <jorton@redhat.com> 0.5.4-2
- move ldconfig from preun to postun (#131280)

* Sun Aug  8 2004 Joe Orton <jorton@redhat.com> 0.5.4-1
- update to 0.5.4 (#129341)

* Thu Jul 15 2004 Robert Scheck <redhat@linuxnetz.de> 0.5.2-1
- upgrade to 0.5.2, enabled i18n support and info files (#127906)

* Fri Jul  9 2004 Joe Orton <jorton@redhat.com> 0.5.1-1
- update to 0.5.1 (#127496)

* Mon Jun 28 2004 Joe Orton <jorton@redhat.com> 0.5.0-1
- update to 0.5.0 (#126836)

* Tue Jun 22 2004 Than Ngo <than@redhat.com> 0.4.9-2
- add prereq: /sbin/ldconfig
- move la file in main package

* Tue Jun 15 2004 Robert Scheck <redhat@linuxnetz.de> 0.4.9-1
- upgrade to 0.4.9 (#126353)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 29 2004 Joe Orton <jorton@redhat.com> 0.4.4-1
- update to 0.4.4; remove contrib from -devel docs

* Thu Apr 29 2004 Joe Orton <jorton@redhat.com> 0.4.3-1
- update to 0.4.3, remove -rpath patch

* Tue Jan 27 2004 Joe Orton <jorton@redhat.com> 0.3.7-1
- update to 0.3.7, simplify

* Wed Jan 07 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.3.6-1mdk
- 0.3.6

* Mon Dec 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.5-1mdk
- 0.3.5

* Sun Oct 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.3-2mdk
- drop the "soname fix" and use the correct way...

* Sat Oct 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.3-1mdk
- 0.3.3

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.3.2-1mdk
- initial cooker contrib
- used the package from PLD as a start point
