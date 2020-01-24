Name:           eccodes
Version:        2.14.1
Release:        1%{?dist}
Summary:        WMO data format decoding and encoding

# force the shared libraries to have these so versions
%global so_version       0.1
%global so_version_f90   0.1
%global datapack_date    20181010

# latest rawhide grib_api version is 1.27.0-5
# but this version number is to be updated as soon as we know
# what the final release of grib_api by upstream will be.
# latest upstream grib_api release is 1.28.0 (05-Dec-2018)
# see https://confluence.ecmwf.int/display/GRIB/Home
%global final_grib_api_version 1.28.1-1%{?dist}

%ifarch i686 ppc64 s390x armv7hl
  %global obsolete_grib_api 0
%else
  %global obsolete_grib_api 1
%endif

# license remarks:
# Most of eccodes is licensed ASL 2.0 but a special case must be noted.
# These 2 files:
#     src/grib_yacc.c
#     src/grib_yacc.h
# contain a special exception clause that allows them to be
# relicensed if they are included in a larger project

License:        ASL 2.0

URL:            https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home
Source0:        https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-%{version}-Source.tar.gz
# note: this data package is unversioned upstream but still it is updated
# now and then so rename the datapack using the download date
# to make it versioned in fedora
Source1:        http://download.ecmwf.org/test-data/eccodes/eccodes_test_data.tar.gz#/eccodes_test_data_%{datapack_date}.tar.gz
# Support 32-bit
# https://software.ecmwf.int/issues/browse/SUP-1813
# (unfortunately this issue is not public)
Patch1:         eccodes-32bit.patch
# Add soversion to the shared libraries, since upstream refuses to do so
# https://software.ecmwf.int/issues/browse/SUP-1809
Patch2:         eccodes-soversion.patch

# note that the requests to make the other issues public are filed here:
# https://software.ecmwf.int/issues/browse/SUP-2073
# (and again, unfortunately this issue is not public)

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  /usr/bin/git
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  netcdf-devel
BuildRequires:  openjpeg2-devel

# For tests
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Test::More)

# the data is needed by the library and all tools provided in the main package
# the other way around, the data package could be installed without
# installing the base package. It will probably be pretty useless,
# unless a user wishes to read and study all these grib and bufr
# file format definitions.
Requires: %{name}-data = %{version}-%{release}

# NOTE: upstream writes:
# """
# For GRIB encoding and decoding, the GRIB-API functionality is provided
# fully in ecCodes with only minor interface and behaviour changes.
# Interfaces for C, Fortran 90 and Python are all maintained as in GRIB-API.
# However, the GRIB-API Fortran 77 interface is no longer available.
# """
# Therefore, since the library name and pkg-config file content changes
# and fortran77 support was removed, this replacement package cannot be
# considered compatible enough and no Provides can be defined.
#
# Furthermore, upstream writes:
# "Please note that GRIB-API support is being discontinued at the end of 2018."
# So the old grib_api will need to be obsoleted.

%if 0%{obsolete_grib_api}
# as stated in the note above, setting provides seems not correct here
# Provides:       grib_api = %%{final_grib_api_version}
Obsoletes:      grib_api < %{final_grib_api_version}
%endif

# as explained in bugzilla #1562066
ExcludeArch: i686
# as explained in bugzilla #1562071
#  note: this is no longer part of fc30/rawhide
#  but the exclude is still needed for EPEL-7
ExcludeArch: ppc64
# as explained in bugzilla #1562076
ExcludeArch: s390x
# as explained in bugzilla #1562084
ExcludeArch: armv7hl

%if 0%{?rhel} >= 7
# as explained in bugzilla #1629377
ExcludeArch: aarch64
%endif

Prefix: %{_prefix}

%description
ecCodes is a package developed by ECMWF which provides an application
programming interface and a set of tools for decoding and encoding messages
in the following formats:

 *  WMO FM-92 GRIB edition 1 and edition 2
 *  WMO FM-94 BUFR edition 3 and edition 4 
 *  WMO GTS abbreviated header (only decoding).

A useful set of command line tools provide quick access to the messages. C,
and Fortran 90 interfaces provide access to the main ecCodes functionality.

ecCodes is an evolution of GRIB-API.  It is designed to provide the user with
a simple set of functions to access data from several formats with a key/value
approach.

For GRIB encoding and decoding, the GRIB-API functionality is provided fully
in ecCodes with only minor interface and behaviour changes. Interfaces for C,
and Fortran 90 are all maintained as in GRIB-API.  However, the
GRIB-API Fortran 77 interface is no longer available.

In addition, a new set of functions with the prefix "codes_" is provided to
operate on all the supported message formats. These functions have the same
interface and behaviour as the "grib_" functions. 

A selection of GRIB-API tools has been included in ecCodes (ecCodes GRIB
tools), while new tools are available for the BUFR (ecCodes BUFR tools) and
GTS formats. The new tools have been developed to be as similar as possible
to the existing GRIB-API tools maintaining, where possible, the same options
and behaviour. A significant difference compared with GRIB-API tools is that
bufr_dump produces output in JSON format suitable for many web based
applications.

#####################################################
%package data
Summary:    Data needed by the eccodes library and tools
BuildArch:  noarch
Prefix: %{_prefix}

%description data
This package provides all tables and definitions needed
to encode and decode grib and bufr files, and includes
both the official WMO tables and a number of often used
local definitions by ECMWF and other meteorological centers.

#####################################################
%prep
%autosetup -n %{name}-%{version}-Source -p1

# unpack the test data below build
mkdir build
cd build
tar xf %SOURCE1

# remove executable permissions from c files
cd ..
chmod 644 tigge/*.c
chmod 644 tools/*.c

# remove executable permissions from the authors and license file
chmod 644 AUTHORS LICENSE

%build
cd build

#-- The following features are disabled by default and not switched on:
#
# * AEC , support for Adaptive Entropy Coding
# * MEMFS , Memory based access to definitions/samples
# * MEMORY_MANAGEMENT , enable memory management
# * ALIGN_MEMORY , enable memory alignment
# * GRIB_TIMER , enable timer
# * ECCODES_THREADS , enable POSIX threads
#
#-- The following features are disabled by default and switched on:
# * PNG , support for PNG decoding/encoding
# * ECCODES_OMP_THREADS , enable OMP threads
# * EXTRA_TESTS , enable extended regression testing
#
#-- The following features are set to AUTO by default and
#   explicitely switched on to ensure they don't vanish unnoticed
#   in case of dependency problems during the build:
# * ENABLE_JPG
# ^ ENABLE_FORTRAN
# * ENABLE_NETCDF
#   NetCDF is only needed to create the grib_to_netcdf convert tool
#
# * ENABLE_PYTHON has value AUTO as default, so if python2 is available
#   during a package build it will build an interface for it.
#   To make sure it does not do so,  explicitely switch it off.
#   Python3 support has been moved to an additional project now,
#   so python handling has been removed completely from this spec file.
#
#-- Also add an explicit option to not use rpath
#
# Note: -DINSTALL_LIB_DIR=%%{_lib} is needed because otherwise
#        the library so files get installed in /usr/lib in stead
#        of /usr/lib64 on x86_64.

%cmake3 -DINSTALL_LIB_DIR=%{_lib} \
        -DENABLE_ECCODES_OMP_THREADS=ON \
        -DENABLE_EXTRA_TESTS=ON \
        -DENABLE_JPG=ON \
        -DENABLE_PNG=ON \
        -DENABLE_FORTRAN=ON \
        -DENABLE_NETCDF=ON \
        -DCMAKE_SKIP_INSTALL_RPATH=TRUE \
        -DECCODES_SOVERSION=%{so_version} \
        -DECCODES_SOVERSION_F90=%{so_version_f90} \
        -DENABLE_PYTHON=OFF \
        ..

%make_build

# copy some include files to the build dir
# that are otherwise not found when creating the debugsource subpackage
cd ..
cp fortran/eccodes_constants.h build/fortran/
cp fortran/grib_api_constants.h build/fortran/

%install
%make_install -C build

# remove a script that does not belong in the doc section
# and triggers an rpmlint error
rm %{buildroot}%{_datadir}/%{name}/definitions/installDefinitions.sh
# by the way, is there a way in the files section to include a directory
# but exclude a given file in it? I could not find such a trick.

%files
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so.*

%files data
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/definitions/
%{_datadir}/%{name}/samples/
%{_datadir}/%{name}/ifs_samples/

%exclude %{_includedir}/*
%exclude %{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/*.so
%exclude %{_libdir}/cmake


%changelog
* Fri Jan 24 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sun Oct 27 2019 Jos de Kloe <josdekloe@gmail.com> - 2.14.1-1
- Upgrade to upstream version 2.14.1

* Sat Nov 24 2018 Jos de Kloe <josdekloe@gmail.com> - 2.9.2-1
- Upgrade to upstream version 2.9.2

* Sun Oct 7 2018 Jos de Kloe <josdekloe@gmail.com> - 2.9.0-1
- Upgrade to upstream version 2.9.0

* Sat Sep 15 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-4
- add Excludearch for aarch64 on epel7

* Sat Sep 15 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-3
- Explicitely disable python in cmake call and use ctest3 rather than ctest
  to ensure the build runs on EPEL-7 as well

* Thu Sep 13 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-2
- Remove python2 sub-package as per Mass Python 2 Package Removal for f30

* Sun Sep 9 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.2-1
- Upgrade to version 2.8.2

* Fri Aug 17 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.0-3
- rebuild with patch provided by Matthew Krupcale for f28

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 5 2018 Jos de Kloe <josdekloe@gmail.com> - 2.8.0-1
- Upgrade to version 2.8.0

* Tue May 08 2018 Jos de Kloe <josdekloe@gmail.com> - 2.7.3-1
- Upgrade to version 2.7.3
- adjust latest grib_api version to 1.26.1-1

* Thu Mar 29 2018 Jos de Kloe <josdekloe@gmail.com> - 2.7.0-2
- added ExcludeArch statements for the failing architectures

* Thu Mar 22 2018 Jos de Kloe <josdekloe@gmail.com> - 2.7.0-1
- Upgrade to version 2.7.0
- Fix rpath and some permission issues
- Remove Provides, add post/postun sections, add LD_LIBRARY_PATH
- Fix failing tests in check section
- Implement so version because upstream refuses to do so
- Add fix for test failure 184 and ldconfig_scriptlets
  and move unversioned so file to devel package
  as suggested by Robert-André Mauchin
- Add a documentation and a data sub-package
- Change the license and add a note explaining why this was done

* Fri Mar 24 2017 Orion Poplawski <orion@cora.nwra.com> - 2.2.0-1
- Initial Fedora package
