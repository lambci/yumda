%global snap 20121213

Summary:	The NetBSD Editline library
Name:		libedit
Version:	3.0
Release: 12.%{snap}cvs%{?dist}.0.2
License:	BSD
Group:		System Environment/Libraries
URL:		http://www.thrysoee.dk/editline/
Source0:	http://www.thrysoee.dk/editline/%{name}-%{snap}-%{version}.tar.gz

BuildRequires:	ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD Editline library.
It provides generic line editing, history, and tokenization functions, similar
to those found in GNU Readline.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	ncurses-devel

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n %{name}-%{snap}-%{version}

# Suppress rpmlint error.
iconv -f ISO8859-1 -t UTF-8 -o ChangeLog.utf-8 ChangeLog
touch -r ChangeLog ChangeLog.utf-8
mv -f ChangeLog.utf-8 ChangeLog

%build
%configure --disable-static --enable-widec

# Fix unused direct shared library dependencies.
sed -i "s/lcurses/ltinfo/" src/Makefile

make %{?_smp_mflags}

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog COPYING THANKS
%{_libdir}/%{name}.so.*

%files devel
%doc examples/fileman.c examples/tc1.c examples/wtc1.c
%doc %{_mandir}/man3/*
%doc %{_mandir}/man5/editrc.5*
%{_includedir}/histedit.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%dir %{_includedir}/editline
%{_includedir}/editline/readline.h

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.0-12.20121213cvs
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.0-11.20121213cvs
- Mass rebuild 2013-12-27

* Wed Feb 20 2013 Kamil Dudka <kdudka@redhat.com> - 3.0-10.20121213cvs
- Update to 20121213-3.0 (#912957)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-9.20120601cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 3.0-8.20110802cvs
- fix specfile issues reported by the fedora-review script

* Wed Jul 18 2012 Kamil Dudka <kdudka@redhat.com> 3.0-7.20120601cvs
- Update to 3.0 (20120601 snap)
- fix crash of el_insertstr() on incomplete multi-byte sequence (#840598)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-6.20110802cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Kamil Dudka <kdudka@redhat.com> - 3.0-5.20110802cvs
- fix code defects found by Coverity

* Wed Nov  9 2011 Adam Williamson <awilliam@redhat.com> 3.0-4.20110802cvs
- rebuild to keep it 'newer' than the f15 and f16 builds

* Fri Aug 26 2011 Kamil Dudka <kdudka@redhat.com> 3.0-3.20110802cvs
- Update to 3.0 (20110802 snap), fixes #732989

* Thu Mar 24 2011 Jerry James <loganjerry@gmail.com> - 3.0-3.20110227cvs
- Update to 3.0 (20110227 snap)
- Drop upstreamed -sigwinch patch
- Preserve ChangeLog timestamp when converting to UTF-8
- Fix "unused direct shared library dependency" warning from rpmlint
- Don't BR gawk; it is on the exceptions list

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3.20100424cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Jerry James <loganjerry@gmail.com> - 3.0-2.20100424cvs
- Update to 3.0 (20100424 snap)
- Enable wide-character (Unicode) support

* Tue Mar 30 2010 Kamil Dudka <kdudka@redhat.com> 3.0-2.20090923cvs
- eliminated compile-time warnings
- fix to not break the read loop on SIGWINCH, patch contributed
  by Edward Sheldrake (#575383)

* Tue Nov 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-1.20090923cvs
- Update to 3.0 (20090923 snap)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-4.20080712cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3.20080712cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.11-2.20080712cvs
- Add ncurses-devel requires to -devel subpackage (BZ#481252)

* Sun Jul 28 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.11-1.20080712cvs
- Version bump to 20080712-2.11.

* Sat Feb 16 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.10-4.20070831cvs
- Rebuilding with gcc-4.3 in Rawhide.

* Sun Nov 04 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.10-3.20070831cvs
- Removed 'Requires: ncurses-devel'.

* Sat Nov 03 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.10-2.20070831cvs
- Changed character encoding of ChangeLog from ISO8859-1 to UTF-8.

* Sun Sep 03 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.10-1.20070831cvs
- Initial build. Imported SPEC from Rawhide.
