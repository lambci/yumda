%define _buildid .10

Summary: A file compression and packaging utility compatible with PKZIP
Name: zip
Version: 3.0
Release: 1%{?_buildid}%{?dist}
License: BSD
Group: Applications/Archiving
Source: http://downloads.sourceforge.net/infozip/zip30.tar.gz
URL: http://www.info-zip.org/Zip.html
# This patch will probably be merged to zip 3.1
# http://www.info-zip.org/board/board.pl?m-1249408491/
Patch1: zip-3.0-exec-shield.patch
# Not upstreamed.
Patch2: zip-3.0-currdir.patch
# Not upstreamed.
Patch3: zip-3.0-time.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Prefix: %{_prefix}

%description
The zip program is a compression and file packaging utility.  Zip is
analogous to a combination of the UNIX tar and compress commands and
is compatible with PKZIP (a compression and file packaging utility for
MS-DOS systems).

Install the zip package if you need to compress files using the zip
program.

%prep
%setup -q -n zip30
%patch1 -p1 -b .exec-shield
%patch2 -p1 -b .currdir
%patch3 -p1 -b .time

%build
make -f unix/Makefile prefix=%{_prefix} "CFLAGS_NOOPT=-I. -DUNIX $RPM_OPT_FLAGS" generic_gcc  %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir} 

make -f unix/Makefile prefix=$RPM_BUILD_ROOT%{_prefix} \
        MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/zipnote
%{_bindir}/zipsplit
%{_bindir}/zip
%{_bindir}/zipcloak

%exclude %{_mandir}

%changelog
* Tue Oct 29 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Fri Jul 9 2010 22:56:14 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/zip-3.0-1.el6

* Fri Jul 9 2010 22:56:13 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/zip-2.31-9.el6

* Fri May 7 2010 03:44:41 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/zip-2.31-2.el5

* Fri May 7 2010 03:44:40 UTC Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/zip-2.31-1.2.2

* Fri May 7 2010 00:18:30 UTC Cristian Gafton <gafton@amazon.com>
- added submodule prep for package zip
