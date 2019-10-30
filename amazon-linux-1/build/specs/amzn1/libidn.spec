%define _buildid .8

Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.18
Release: 2%{?_buildid}%{?dist}
URL: http://www.gnu.org/software/libidn/
License: LGPLv2+ and GPLv3+ and GFDL
Source0: http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig, gettext
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(postun): /sbin/ldconfig
Requires(pre): /sbin/ldconfig

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package devel
Summary: Development files for the libidn library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.

%prep
%setup -q

# Name directory sections consistently in the info file, #209491
sed -i '/^INFO-DIR-SECTION/{s/GNU Libraries/Libraries/;s/GNU utilities/Utilities/;}' doc/libidn.info

iconv -f ISO-8859-1 -t UTF-8 doc/libidn.info > iconv.tmp
mv iconv.tmp doc/libidn.info

%build
%configure --disable-csharp --disable-static --libdir=/%{_lib}
make %{?_smp_mflags}

%check
make %{?_smp_mflags} -C tests check

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT pkgconfigdir=%{_libdir}/pkgconfig

# provide more examples
make %{?_smp_mflags} -C examples distclean

# clean up docs
find doc -name "Makefile*" | xargs rm
rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir

# Make multilib safe:
sed -i '/gnu compiler/d' $RPM_BUILD_ROOT%{_includedir}/idn-int.h

rm -f $RPM_BUILD_ROOT/%{_lib}/*.la \
      $RPM_BUILD_ROOT%{_datadir}/info/*.png

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libidn.so $RPM_BUILD_ROOT%{_libdir}

lib=`echo $RPM_BUILD_ROOT/%{_lib}/libidn.so.*.*`
ln -sf ../../%{_lib}/`basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/libidn.so

# Fix the .pc file to reference the directory which contains the .so
sed -i 's,^libdir=.*$,libdir=%{_libdir},' \
    $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libidn.pc

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS NEWS FAQ README THANKS COPYING*
%{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_datadir}/emacs/site-lisp
/%{_lib}/libidn.so.*
%{_infodir}/%{name}.info.gz

%files devel
%defattr(0644,root,root,755)
%doc doc/libidn.html examples
%{_libdir}/libidn.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Fri Jul 9 2010 22:19:40 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libidn-1.18-2.el6

* Fri Jul 9 2010 22:19:39 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/libidn-1.9-5.1

* Fri May 7 2010 01:54:18 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/libidn-0.6.5-1.1

* Fri May 7 2010 00:14:26 UTC Cristian Gafton <gafton@amazon.com>
- added submodule prep for package libidn
