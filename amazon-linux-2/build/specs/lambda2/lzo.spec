%define _trivial .0
%define _buildid .1

Name:           lzo
Version:        2.10
Release: 1%{?dist}
Summary:        Data compression library with very fast (de)compression
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/lzo/
Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel

Prefix: %{_prefix}

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package minilzo
Summary:        Mini version of lzo for apps which don't need the full version
Group:          System Environment/Libraries
Prefix: %{_prefix}

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.


%prep
%setup -q
# mark asm files as NOT needing execstack
for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
make %{?_smp_mflags} CFLAGS="%{optflags} -fno-strict-aliasing -std=gnu89"
# build minilzo too (bz 439979)
gcc %{optflags} -fno-strict-aliasing -std=gnu89 -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
install -m 755 libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/libminilzo.so

#Remove doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/lzo


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/liblzo2.so.*

%files minilzo
%defattr(-,root,root,-)
%license minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig


%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org> - 2.10-1
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Jul  2 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.06-8
- Built with -fno-strict-aliasing (rpmdiff)
  Related: CVE-2014-4607

* Mon Jun 30 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.06-7
- Fixed integer overflow in decompressor
  Resolves: CVE-2014-4607

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.06-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.06-5
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 14 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.06-1
- Upgrade to latest upstream
- Apply patch from Nicolas Chauvet

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May  1 2008 Lubomir Rintel <lkundrak@v3.sk> 2.03-1
- New upstream release
- Changed the license to GPLv2+

* Wed Apr  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-5
- Fix configure failure with -Werror-implicit-function-declaration in CFLAGS
- Add a minilzo subpackage which contains a shared version of minilzo, to be
  used by all applications which ship with their own copy of it (bz 439979)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.02-4
- Autorebuild for GCC 4.3

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-3
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-2
- FE6 Rebuild

* Wed Jul 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-1
- New upstream release 2.02, soname change!

* Mon Jul 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.08-7
- Taking over as maintainer since Anvil has other priorities
- Add a patch to fix asm detection on i386 (bug 145882, 145893). Thanks to
  Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe> for the initial patch.
- Removed unused build dependency on nasm
- Remove static lib
- Cleanup %%doc a bit

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.08-6.fc5
- Rebuild for new gcc

* Tue Jan 17 2006 Dams <anvil[AT]livna.org> - 1.08-5.fc5
- Bumped release for gcc 4.1 rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.08-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.08-0.fdr.2
- Typo un devel description
- Added post and postun scriptlets
- Added URL in Source0

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.
