Name:           matio
Version:        1.5.3
Release:        1%{?dist}
Summary:        Library for reading/writing Matlab MAT files

Group:          System Environment/Libraries
License:        BSD
URL:            http://sourceforge.net/projects/matio
Source0:        http://downloads.sourceforge.net/matio/matio-%{version}.tar.gz

BuildRequires:  doxygen
#According to the README - zlib 1.2.2 is possible but require a patch
BuildRequires:  zlib-devel >= 1.2.3
BuildRequires:  hdf5-devel >= 1.8
# 1.5.3 was released without configure
BuildRequires:  libtool
Requires:       hdf5 = %{_hdf5_version}
     

%description
matio is an open-source library for reading/writing Matlab MAT files.  This
library is designed for use by programs/libraries that do not have access or
do not want to rely on Matlab's libmat shared library.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       hdf5-devel
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
sh ./autogen.sh
%configure \
  --enable-shared \
  --disable-static \
  --enable-mat73=yes \
  --enable-extended-sparse=yes

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}



%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

#Fix timestamp
touch -r $RPM_BUILD_ROOT%{_includedir}/matio_pubconf.h NEWS

rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir


%check
#Needed to avoid rpath
export LD_LIBRARY_PATH=%{_builddir}/%{?buildsubdir}/src/.libs/ ; make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING
%doc NEWS README.md
%{_bindir}/matdump
%{_libdir}/*.so.*

%files devel
%{_includedir}/matio*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/Mat_*.3.*


%changelog
* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.3-1
- Update to 1.5.3

* Sat Nov 07 2015 Christian Dersch <lupinix@fedoraproject.org> - 1.5.2-1.el7
- initial package for EPEL7

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-6
- Rebuild for hdf5 1.8.15

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-5
- Rebuild for hdf5 1.8.14

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-3
- Rebuild for hdf 1.8.13

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-1
- Update to 1.5.2

* Sat Sep 14 2013 Dan Horák <dan[at]danny.cz> - 1.5.1-4
- Rebuilt to resolve broken deps on s390(x)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.5.1-2
- Rebuild for hdf5 1.8.11

* Thu Mar 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-1
- Update to 1.5.1
- Spec file clean-up

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Dan Horák <dan[at]danny.cz> - 1.5.0-5
- fix build on big endian platforms

* Wed Dec 05 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5.0-4
- Rebuild for hdf5 1.8.10

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5.0-2
- Rebuild for hdf5 1.8.9
- Add Requires on specific version of hdf5 built with

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.5.0-1
- Update to 1.5.0
- Enable mat73 support
- License change from LGPLv2+ to BSD

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4
- Remove uneeded patches.

* Wed Sep 30 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.3.3-5
- Fix location of Fortran module.
- Add Requires: pkgconfig on -devel.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 kwizart < kwizart at gmail.com > - 1.3.3-3
- Remove the test subpackage 
- Enable make check
- Various typo and clean-up

* Wed Sep 24 2008 kwizart < kwizart at gmail.com > - 1.3.3-2
- Fix undefined-non-weak-symbol 
- Fix missing f90 files in the debuginfo package

* Wed Sep 24 2008 kwizart < kwizart at gmail.com > - 1.3.3-1
- Initial package for fedora


