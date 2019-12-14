%define _buildid .22

%global gcc_name 48
%global gcc_version 4.8.5

Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc
Version: %{gcc_version}
Release: 1%{?_buildid}%{?dist}

Requires: gcc%{gcc_name} >= %{gcc_version}
Requires(post): /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives

Obsoletes: gcc-objc = 4.6.2
Obsoletes: gcc-objc = 4.6.3
Obsoletes: gcc-objc++ = 4.6.2
Obsoletes: gcc-objc++ = 4.6.3
Obsoletes: libobjc = 4.6.2
Obsoletes: libobjc = 4.6.3

Obsoletes: gcc-go = 4.6.2
Obsoletes: gcc-go = 4.6.3
Obsoletes: libgo-devel = 4.6.2
Obsoletes: libgo-devel = 4.6.3
Obsoletes: libgo-static = 4.6.2
Obsoletes: libgo-static = 4.6.3

License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages

URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# libtool has hardcoded gcc versioned paths in its binaries
Conflicts: libtool < 2.2.10-%{gcc_version}

Prefix: %{_prefix}

%description
The gcc package contains the GNU Compiler Collection.
You'll need this package in order to compile C code.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++%{gcc_name} >= %{gcc_version}
Requires: gcc%{gcc_name}-c++ >= %{gcc_version}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
# libtool has hardcoded gcc versioned paths in its binaries
Conflicts: libtool < 2.2.10-%{gcc_version}
Prefix: %{_prefix}
%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{gcc_name}-devel >= %{gcc_version}
Requires: libstdc++%{gcc_name} >= %{gcc_version}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
Prefix: %{_prefix}
%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Requires: libstdc++%{gcc_name}-static >= %{gcc_version}
Prefix: %{_prefix}
%description -n libstdc++-static
Static libraries for the GNU standard C++ library. 

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: gcc%{gcc_name}-gfortran >= %{gcc_version}
Prefix: %{_prefix}
%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: cpp%{gcc_name} >= %{gcc_version}
Prefix: %{_prefix}
%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically by the C compiler to
transform your program before actual compilation. It is called a macro
processor because it allows you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the inclusion of
header files (files of declarations that can be substituted into your
program); macro expansion (you can define macros, and the C preprocessor will
replace the macros with their definitions throughout the program); conditional
compilation (using special preprocessing directives, you can include or
exclude parts of the program according to various conditions); and line
control (if you use a program to combine or rearrange source files into an
intermediate file which is then compiled, you can use line control to inform
the compiler about where each source line originated).

You should install this package if you are a C programmer and you use macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}
Requires: gcc%{gcc_name}-gnat >= %{gcc_version}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
Obsoletes: libgnat-devel
Obsoletes: libgnat-static
Prefix: %{_prefix}
%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Requires: libgnat%{gcc_name} >= %{gcc_version}
Prefix: %{_prefix}
%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%prep
exit 0

%build
exit 0

%install
rm -fr %{buildroot}
exit 0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%files -n cpp
%defattr(-,root,root,-)

%files c++
%defattr(-,root,root,-)

%files gfortran
%defattr(-,root,root,-)

%files gnat
%defattr(-,root,root,-)

%files -n libgnat
%defattr(-,root,root,-)

%changelog
* Sat Dec 14 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Sep 4 2017 Cristian Gafton <gafton@amazon.com>
- sync changes with subpackage updates for main compiler packages

* Thu Apr 27 2017 Cristian Gafton <gafton@amazon.com>
- Allow loseoser version matches for a particular compiler family

* Thu Aug 6 2015 Rodrigo Novo <rodarvus@amazon.com>
- Update required gcc version to 4.8.3

* Mon Mar 24 2014 cyler <cyler@amazon.com>
- Remove invalid reference to gcc 4.4

* Sat Mar 22 2014 cyler <cyler@amazon.com>
- Obsolete libobjc and libgo-*

* Thu Mar 20 2014 cyler <cyler@amazon.com>
- Obsolete shipped gcc-go virtual packages

* Wed Mar 19 2014 Cristian Gafton <gafton@amazon.com>
- conditionalize gccgo packages with bcond
- conditionalize objc packages with bcond
- Revert "Remove objc from metapackage to match gcc48"

* Tue Mar 18 2014 cyler <cyler@amazon.com>
- Obsolete gcc-objc/gcc-objc++ metapackages

* Wed Mar 12 2014 Tom Kirchner <tjk@amazon.com>
- Remove objc from metapackage to match gcc48

* Fri Mar 7 2014 Cristian Gafton <gafton@amazon.com>
- switch default compiler version to GCC 4.8

* Mon Mar 18 2013 Cristian Gafton <gafton@amazon.com>
- update for minor rev of gcc to 4.6.3

* Thu Sep 27 2012 Cristian Gafton <gafton@amazon.com>
- up revision
- remove noarch metapackage for libstdc++

* Wed Sep 26 2012 Cristian Gafton <gafton@amazon.com>
- remove meta package for libgcc

* Mon Sep 17 2012 Cristian Gafton <gafton@amazon.com>
- adjust for libgo package changes
- add handling for gcc-go and libgo

* Tue Sep 11 2012 Cristian Gafton <gafton@amazon.com>
- fix deps for libstdc++-static
- fix gnat requires

* Mon Sep 10 2012 Cristian Gafton <gafton@amazon.com> - 4.6.2-1
- create meta package

* Mon Sep 10 2012 Cristian Gafton <gafton@amazon.com>
- add conflict for older libtool packages
- create meta package for gcc suite
- setup complete for package gcc
