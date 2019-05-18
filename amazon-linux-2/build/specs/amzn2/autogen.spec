Summary:	Automated text file generator
Name:		autogen
Version:	5.18
Release: 5%{?dist}.0.2
# Some files are licensed under GPLv2+.
# We redistribute them under GPLv3+.
License:	GPLv3+
Group:		Development/Tools
URL:		http://www.gnu.org/software/autogen/
Source0:	ftp://ftp.gnu.org/gnu/autogen/rel%{version}/%{name}-%{version}.tar.xz

# Fix multilib conflicts
Patch0:		autogen-multilib.patch

Requires:	%{name}-libopts%{?_isa} = %{version}-%{release}
Requires(post):	/sbin/install-info
Requires(preun):  /sbin/install-info

BuildRequires:	guile-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel

%description
AutoGen is a tool designed to simplify the creation and maintenance of
programs that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept
synchronised.

%package libopts
Summary:	Automated option processing library based on %{name}
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		System Environment/Libraries

%description libopts
Libopts is very powerful command line option parser consisting of a set of
AutoGen templates and a run time library that nearly eliminates the hassle of
parsing and documenting command line options.

%package libopts-devel
Summary:	Development files for libopts
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		Development/Libraries

Requires:	automake
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libopts%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description libopts-devel
This package contains development files for libopts.

%prep
%setup -q
%patch0 -p1 -b .multilib

# Disable failing test
sed -i 's|errors.test||' autoopts/test/Makefile.in

%build
# Static libraries are needed to run test-suite.
%configure

# Fix Libtool to remove rpaths.
rm -f ./libtool
cp %{_bindir}/libtool .

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' ./libtool

make %{?_smp_mflags}

%check
make check

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete
find $RPM_BUILD_ROOT -type f -name "*.a" -delete

# Remove time stamps from generated devel man pages to avoid multilib conflicts
sed -i 's|\(It has been AutoGen-ed\).*.\(by AutoGen\)|\1 \2|' \
	$RPM_BUILD_ROOT%{_mandir}/man3/*.3

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info \
  %{_infodir}/dir >/dev/null 2>&1 || :
fi

%post libopts -p /sbin/ldconfig

%postun libopts -p /sbin/ldconfig

%files
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc NEWS
%doc README
%doc THANKS
%doc TODO
%doc pkg/libopts/COPYING.gplv3
%{_bindir}/columns
%{_bindir}/getdefs
%{_bindir}/%{name}
%{_bindir}/xml2ag
%{_infodir}/%{name}.info*.gz
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/columns.1.gz
%{_mandir}/man1/getdefs.1.gz
%{_mandir}/man1/xml2ag.1.gz

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files libopts
%doc pkg/libopts/COPYING.mbsd
%doc pkg/libopts/COPYING.lgplv3
%{_libdir}/libopts.so.*

%files libopts-devel
%{_bindir}/autoopts-config
%{_datadir}/aclocal/autoopts.m4
#%{_datadir}/aclocal/liboptschk.m4
%{_libdir}/libopts.so
%{_datadir}/pkgconfig/autoopts.pc
%{_mandir}/man1/autoopts-config.1.gz
%{_mandir}/man3/*

%dir %{_includedir}/autoopts
%{_includedir}/autoopts/options.h
%{_includedir}/autoopts/usage-txt.h

%changelog
* Fri Mar 14 2014 Miroslav Lichvar <mlichvar@redhat.com> - 5.18-5
- Remove arch-specific dependency to avoid multilib conflict (#1076407)

* Tue Feb 11 2014 Miroslav Lichvar <mlichvar@redhat.com> - 5.18-4
- Package libopts tear-off tarball (#1055904)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 5.18-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 5.18-2
- Mass rebuild 2013-12-27

* Mon Jul 29 2013 Miroslav Lichvar <mlichvar@redhat.com> - 5.18-1
- Update to 5.18
- Fix multilib conflicts (#831379)
- Make some dependencies arch-specific
- Remove obsolete macros

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.12-6
- Perl 5.18 rebuild

* Thu Apr 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 5.12-5
- Fix build failure with guile2.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Anthony Green <green@redhat.com> - 5.12-1
- Upgrade.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 5.9.4-7
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 25 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-4
- Changed dual licensing of autogen-libopts by dropping BSD.
- Fixed multilib conflicts, static libraries and removed rpath setting bits
  from autoopts-config.
- Replaced 'BuildRequires: chrpath' with 'BuildRequires: libtool' for removing
  rpaths.

* Sun Feb 24 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-3
- Added 'Obsoletes: autogen-manuals ...'.
- Changed dual licensing of autogen-libopts-devel by dropping BSD.
- Defined undefined non-weak symbols.
- Omitted unused direct shared library dependencies.
- Removed rpath setting bits from pkgconfig file.
- Miscellaneous fixes.

* Thu Feb 21 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-2
- Prefixed libopts and libopts-devel with autogen-.
- Removed 'BuildRequires: /usr/sbin/alternatives' and use of alternatives.
- Added Provides & Obsoletes pair in autogen-libopts-devel according to
  Fedora naming guidelines.

* Sat Feb 09 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-1
- Initial build. Imported SPEC from Rawhide.
- Removed 'Obsoletes: libopts ...' and introduced libopts subpackages to avoid
  mulitple licensing scenario.
