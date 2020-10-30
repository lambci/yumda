%define _trivial .0
%define _buildid .3

%global major_version 2
%global minor_version 6
%global teeny_version 6
%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_release %{ruby_version}

# Specify the named version. It has precedense to revision.
#%%global milestone rc2

# Keep the revision enabled for pre-releases from SVN.
#%%global revision 66252

%global ruby_archive %{name}-%{ruby_version}

# If revision and milestone are removed/commented out, the official release build is expected.
%if 0%{?milestone:1}%{?revision:1} != 0
%global development_release %{?milestone}%{?!milestone:%{?revision:r%{revision}}}
%global ruby_archive %{ruby_archive}-%{?milestone}%{?!milestone:%{?revision:r%{revision}}}
%endif


%global release 125
%{!?release_string:%global release_string %{?development_release:0.}%{release}%{?development_release:.%{development_release}}%{?dist}}

# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/rubygems

# Bundled libraries versions
%global rubygems_version 3.0.3
%global rubygems_molinillo_version 0.5.7

%global bundler_version 1.17.2
%global bundler_fileutils_version 1.1.0
%global bundler_molinillo_version 0.6.6
%global bundler_net_http_persistent_version 2.9.4
%global bundler_thor_version 0.20.0

%global bigdecimal_version 1.4.1
%global did_you_mean_version 1.3.0
%global io_console_version 0.4.7
%global irb_version 1.0.0
%global json_version 2.1.0
%global minitest_version 5.11.3
%global net_telnet_version 0.2.0
%global openssl_version 2.1.2
%global power_assert_version 1.1.3
%global psych_version 3.1.0
%global rake_version 12.3.3
%global rdoc_version 6.1.2
%global test_unit_version 3.2.9
%global xmlrpc_version 0.3.0

# Might not be needed in the future, if we are lucky enough.
# https://bugzilla.redhat.com/show_bug.cgi?id=888262
%global tapset_root %{_datadir}/systemtap
%global tapset_dir %{tapset_root}/tapset
%global tapset_libdir %(echo %{_libdir} | sed 's/64//')*

%global _normalized_cpu %(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/')

%if 0%{?fedora} >= 19
%bcond_without rubypick
%endif

%bcond_without cmake
%bcond_without git
%bcond_without gmp
%bcond_with hostname
%bcond_without systemtap

%if 0%{?fedora}
%bcond_without hardening_test
%endif

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: %{ruby_version}
Release: %{release_string}%{?_trivial}%{?_buildid}
# Public Domain for example for: include/ruby/st.h, strftime.c, missing/*, ...
# MIT and CCO: ccan/*
# zlib: ext/digest/md5/md5.*, ext/nkf/nkf-utf8/nkf.c
# UCD: some of enc/trans/**/*.src
License: (Ruby or BSD) and Public Domain and MIT and CC0 and zlib and UCD
URL: https://www.ruby-lang.org/
Source0: https://cache.ruby-lang.org/pub/%{name}/%{major_minor_version}/%{ruby_archive}.tar.xz
Source1: operating_system.rb
# TODO: Try to push SystemTap support upstream.
Source2: libruby.stp
Source3: ruby-exercise.stp
Source4: macros.ruby
Source5: macros.rubygems
Source6: abrt_prelude.rb
# RPM dependency generators.
Source8: rubygems.attr
Source9: rubygems.req
Source10: rubygems.prov
Source11: rubygems.con
# ABRT hoook test case.
Source13: test_abrt.rb
# SystemTap tests.
Source14: test_systemtap.rb

%if 0%{?amzn}
%{lua:

function source_macros(file)
  local macro = nil

  for line in io.lines(file) do
    if not macro and line:match("^%%") then
      macro = line:match("^%%(.*)$")
      line = nil
    end

    if macro then
      if line and macro:match("^.-%s*\\%s*$") then
        macro = macro .. '\n' .. line
      end

      if not macro:match("^.-%s*\\%s*$") then
        rpm.define(macro)
        macro = nil
      end
    end
  end
end

source_macros(rpm.expand("%{SOURCE4}"))
source_macros(rpm.expand("%{SOURCE5}"))

}
%else
# The load directive is supported since RPM 4.12, i.e. F21+. The build process
# fails on older Fedoras.
%{?load:%{SOURCE4}}
%{?load:%{SOURCE5}}
%endif

# Patchset resycned with ruby-2.6.6-125.fc31
# Fix ruby_version abuse.
# https://bugs.ruby-lang.org/issues/11002
Patch0: ruby-2.3.0-ruby_version.patch
# http://bugs.ruby-lang.org/issues/7807
Patch1: ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Allows to override libruby.so placement. Hopefully we will be able to return
# to plain --with-rubyarchprefix.
# http://bugs.ruby-lang.org/issues/8973
Patch2: ruby-2.1.0-Enable-configuration-of-archlibdir.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
Patch3: ruby-2.1.0-always-use-i386.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://bugs.ruby-lang.org/issues/5617
Patch4: ruby-2.1.0-custom-rubygems-location.patch
# Make mkmf verbose by default
Patch5: ruby-1.9.3-mkmf-verbose.patch
# Adds support for '--with-prelude' configuration option. This allows to built
# in support for ABRT.
# http://bugs.ruby-lang.org/issues/8566
Patch6: ruby-2.1.0-Allow-to-specify-additional-preludes-by-configuratio.patch
# Use miniruby to regenerate prelude.c.
# https://bugs.ruby-lang.org/issues/15306
Patch7: ruby-2.2.3-Generate-preludes-using-miniruby.patch
# Workaround "an invalid stdio handle" error on PPC, due to recently introduced
# hardening features of glibc (rhbz#1361037).
# https://bugs.ruby-lang.org/issues/12666
Patch9: ruby-2.3.1-Rely-on-ldd-to-detect-glibc.patch
# `gem build ../foo.gemspec` changes directory, which does not play well with
# gems unpacked by setup macro.
# https://github.com/rubygems/rubygems/issues/2587
Patch11: rubygems-3.0.3-Restore-gem-build-behavior-and-introdcue-the-C-flag-to-gem-build.patch
# This allows to loosen the RDoc dependency again.
# https://github.com/rubygems/rubygems/pull/2604
Patch12: rubygems-3.0.3-Avoid-rdoc-hook-when-its-failed-to-load-rdoc-library.patch

# Add support for .include directive used by OpenSSL config files.
# https://github.com/ruby/openssl/pull/216
Patch22: ruby-2.6.0-config-support-include-directive.patch

# Amazon Patches
Patch100: ruby-2.6.3-fix-gem_ext_cmake_builder-test.patch
# Enable arm64 optimizations that exist for power/x86
# https://github.com/ruby/ruby/pull/3393
Patch101: ruby-2.6.6-arm64-optimizations.patch

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ruby(rubygems) >= %{rubygems_version}
Requires: rubygem(bigdecimal) >= %{bigdecimal_version}
Requires: rubygem(did_you_mean) >= %{did_you_mean_version}
Requires: rubygem(openssl) >= %{openssl_version}


BuildRequires: autoconf
BuildRequires: gdbm-devel
%{?with_gmp:BuildRequires: gmp-devel}
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
# Needed to pass test_set_program_name(TestRubyOptions)
BuildRequires: procps
%{?with_systemtap:BuildRequires: %{_bindir}/dtrace}
# RubyGems test suite optional dependencies.
%{?with_git:BuildRequires: git}
%{?with_cmake:BuildRequires: %{_bindir}/cmake}
# Required to test hardening.
%{?with_hardening_test:BuildRequires: %{_bindir}/checksec}
%{?with_hostname:BuildRequires: %{_bindir}/hostname}
BuildRequires: multilib-rpm-config
BuildRequires: gcc
BuildRequires: zlib-devel

# This package provides %%{_bindir}/ruby-mri therefore it is marked by this
# virtual provide. It can be installed as dependency of rubypick.
Provides: ruby(runtime_executable) = %{ruby_release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package devel
Summary:    A Ruby development environment
Requires:   %{name}%{?_isa} = %{version}-%{release}
# This would not be needed if ~50 packages depending on -devel used
# --disable-gems
Requires:   rubygems

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package libs
Summary:    Libraries necessary to run Ruby
License:    Ruby or BSD
Provides:   ruby(release) = %{ruby_release}

# Virtual provides for CCAN copylibs.
# https://fedorahosted.org/fpc/ticket/364
Provides: bundled(ccan-build_assert)
Provides: bundled(ccan-check_type)
Provides: bundled(ccan-container_of)
Provides: bundled(ccan-list)

# Tcl/Tk support was removed from stdlib in Ruby 2.4, i.e. F27 timeframe
# so lets obsolete it. This is not the best place, but we don't have
# better, unless https://fedorahosted.org/fpc/ticket/645 provides some
# generic solution.
Obsoletes: ruby-tcltk < 2.4.0


%description libs
This package includes the libruby, necessary to run Ruby.


# TODO: Rename or not rename to ruby-rubygems?
%package -n rubygems
Summary:    The Ruby standard for packaging ruby libraries
Version:    %{rubygems_version}
License:    Ruby or MIT
Requires:   ruby(release)
Requires:   rubygem(openssl) >= %{openssl_version}
Requires:   rubygem(psych) >= %{psych_version}
Provides:   gem = %{version}-%{release}
Provides:   ruby(rubygems) = %{version}-%{release}
# https://github.com/rubygems/rubygems/pull/1189#issuecomment-121600910
Provides:   bundled(rubygem-molinillo) = %{rubygems_molinillo_version}
BuildArch:  noarch

%description -n rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.


%package -n rubygems-devel
Summary:    Macros and development tools for packaging RubyGems
Version:    %{rubygems_version}
License:    Ruby or MIT
Requires:   ruby(rubygems) = %{version}-%{release}
# Needed for RDoc documentation format generation.
Requires:   rubygem(json) >= %{json_version}
Requires:   rubygem(rdoc) >= %{rdoc_version}
BuildArch:  noarch

%description -n rubygems-devel
Macros and development tools for packaging RubyGems.


%package -n rubygem-rake
Summary:    Ruby based make-like utility
Version:    %{rake_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rake = %{version}-%{release}
Provides:   rubygem(rake) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.


%package -n rubygem-irb
Summary:    The Interactive Ruby
Version:    %{irb_version}
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   irb = %{version}-%{release}
Provides:   rubygem(irb) = %{version}-%{release}
# Obsoleted by Ruby 2.6 in F30 timeframe.
Provides:   ruby(irb) = %{ruby_version}-%{release}
Provides:   ruby-irb = %{ruby_version}-%{release}
Obsoletes:  ruby-irb < %{ruby_version}-%{release}
BuildArch:  noarch

%description -n rubygem-irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package -n rubygem-rdoc
Summary:    A tool to generate HTML and command-line documentation for Ruby projects
Version:    %{rdoc_version}
# SIL: lib/rdoc/generator/template/darkfish/css/fonts.css
License:    GPLv2 and Ruby and MIT and OFL
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Requires:   rubygem(irb) >= %{irb_version}
Requires:   rubygem(io-console) >= %{io_console_version}
Requires:   rubygem(json) >= %{json_version}
Provides:   rdoc = %{version}-%{release}
Provides:   ri = %{version}-%{release}
Provides:   rubygem(rdoc) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-rdoc
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.


%package doc
Summary:    Documentation for %{name}
Requires:   %{_bindir}/ri
BuildArch:  noarch

%description doc
This package contains documentation for %{name}.


%package -n rubygem-bigdecimal
Summary:    BigDecimal provides arbitrary-precision floating point decimal arithmetic
Version:    %{bigdecimal_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(bigdecimal) = %{version}-%{release}

%description -n rubygem-bigdecimal
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect–whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.


%package -n rubygem-did_you_mean
Summary:    "Did you mean?" experience in Ruby
Version:    %{did_you_mean_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(did_you_mean) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-did_you_mean
"did you mean?" experience in Ruby: the error message will tell you the right
one when you misspelled something.


%package -n rubygem-io-console
Summary:    IO/Console is a simple console utilizing library
Version:    %{io_console_version}
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(io-console) = %{version}-%{release}

%description -n rubygem-io-console
IO/Console provides very simple and portable access to console. It doesn't
provide higher layer features, such like curses and readline.


%package -n rubygem-json
Summary:    This is a JSON implementation as a Ruby extension in C
Version:    %{json_version}
# UCD: ext/json/generator/generator.c
License:    (Ruby or GPLv2) and UCD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(json) = %{version}-%{release}

%description -n rubygem-json
This is a implementation of the JSON specification according to RFC 4627.
You can think of it as a low fat alternative to XML, if you want to store
data to disk or transmit it over a network rather than use a verbose
markup language.


%package -n rubygem-minitest
Summary:    Minitest provides a complete suite of testing facilities
Version:    %{minitest_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(minitest) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.


%package -n rubygem-openssl
Summary:    OpenSSL provides SSL, TLS and general purpose cryptography
Version:    %{openssl_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(openssl) = %{version}-%{release}

%description -n rubygem-openssl
OpenSSL provides SSL, TLS and general purpose cryptography. It wraps the
OpenSSL library.


%package -n rubygem-power_assert
Summary:    Power Assert for Ruby
Version:    %{power_assert_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(power_assert) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-power_assert
Power Assert shows each value of variables and method calls in the expression.
It is useful for testing, providing which value wasn't correct when the
condition is not satisfied.


%package -n rubygem-psych
Summary:    A libyaml wrapper for Ruby
Version:    %{psych_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(psych) = %{version}-%{release}

%description -n rubygem-psych
Psych is a YAML parser and emitter. Psych leverages
libyaml[http://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting
capabilities. In addition to wrapping libyaml, Psych also knows how to
serialize and de-serialize most Ruby objects to and from the YAML format.


%package -n rubygem-net-telnet
Summary:    Provides telnet client functionality
Version:    %{net_telnet_version}
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(net-telnet) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-net-telnet
Provides telnet client functionality.

This class also has, through delegation, all the methods of a socket object
(by default, a TCPSocket, but can be set by the Proxy option to new()). This
provides methods such as close() to end the session and sysread() to read data
directly from the host, instead of via the waitfor() mechanism. Note that if
you do use sysread() directly when in telnet mode, you should probably pass
the output through preprocess() to extract telnet command sequences.


%package -n rubygem-test-unit
Summary:    An xUnit family unit testing framework for Ruby
Version:    %{test_unit_version}
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:    (Ruby or BSD) and (Ruby or BSD or Python) and (Ruby or BSD or LGPLv2+)
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Requires:   rubygem(power_assert)
Provides:   rubygem(test-unit) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-test-unit
Test::Unit (test-unit) is unit testing framework for Ruby, based on xUnit
principles. These were originally designed by Kent Beck, creator of extreme
programming software development methodology, for Smalltalk's SUnit. It allows
writing tests, checking results and automated testing in Ruby.


%package -n rubygem-xmlrpc
Summary:    XMLRPC is a lightweight protocol that enables remote procedure calls over HTTP
Version:    %{xmlrpc_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(xmlrpc) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-xmlrpc
XMLRPC is a lightweight protocol that enables remote procedure calls over
HTTP.


%package -n rubygem-bundler
Summary:    Library and utilities to manage a Ruby application's gem dependencies
Version:    %{bundler_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Requires:   rubygem(io-console)
Provides:   rubygem(bundler) = %{version}-%{release}
# The following bundled() Provides: are virtual
# https://fedoraproject.org/wiki/Bundled_Libraries
# https://github.com/bundler/bundler/issues/3647
Provides:   bundled(rubygem-fileutils) = %{bundler_fileutils_version}
Provides:   bundled(rubygem-molinillo) = %{bundler_molinillo_version}
Provides:   bundled(rubygem-net-http-persistent) = %{bundler_net_http_persistent_version}
Provides:   bundled(rubygem-thor) = %{bundler_thor_version}
# Streamline upgrade if an older version of rubygem-bundler-doc is present
Provides:   rubygem-bundler-doc
Obsoletes:  rubygem-bundler-doc <= %{bundler_version}
BuildArch:  noarch

%description -n rubygem-bundler
Bundler manages an application's dependencies through its entire life, across
many machines, systematically and repeatably.


%prep
%setup -q -n %{ruby_archive}

# Remove bundled libraries to be sure they are not used.
rm -rf ext/psych/yaml
rm -rf ext/fiddle/libffi*

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1

%patch22 -p1

# Amazon Patches
%patch100 -p1
%patch101 -p1

# Provide an example of usage of the tapset:
cp -a %{SOURCE3} .

# Make abrt_prelude.rb available for compilation process. The prelude must be
# available together with Ruby's source due to
# https://github.com/ruby/ruby/blob/trunk/tool/compile_prelude.rb#L26
cp -a %{SOURCE6} .

%build
autoconf

%configure \
        --with-rubylibprefix='%{ruby_libdir}' \
        --with-archlibdir='%{_libdir}' \
        --with-rubyarchprefix='%{ruby_libarchdir}' \
        --with-sitedir='%{ruby_sitelibdir}' \
        --with-sitearchdir='%{ruby_sitearchdir}' \
        --with-vendordir='%{ruby_vendorlibdir}' \
        --with-vendorarchdir='%{ruby_vendorarchdir}' \
        --with-rubyhdrdir='%{_includedir}' \
        --with-rubyarchhdrdir='%{_includedir}' \
        --with-sitearchhdrdir='$(sitehdrdir)/$(arch)' \
        --with-vendorarchhdrdir='$(vendorhdrdir)/$(arch)' \
        --with-rubygemsdir='%{rubygems_dir}' \
        --with-ruby-pc='%{name}.pc' \
        --with-compress-debug-sections=no \
        --disable-rpath \
        --enable-shared \
        --with-ruby-version='' \
        --enable-multiarch \
        --with-prelude=./abrt_prelude.rb \

# Q= makes the build output more verbose and allows to check Fedora
# compiler options.
make %{?_smp_mflags} COPY="cp -p" Q=

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Rename ruby/config.h to ruby/config-<arch>.h to avoid file conflicts on
# multilib systems and install config.h wrapper
%multilib_fix_c_header --file %{_includedir}/%{name}/config.h
# TODO: The correct patch should be %%{_includedir}/%%{name}/rb_mjit_min_header-%{ruby_version}.h
# https://bugs.ruby-lang.org/issues/15425
%multilib_fix_c_header --file %{_includedir}/rb_mjit_min_header-%{ruby_version}.h

# Rename the ruby executable. It is replaced by RubyPick.
%{?with_rubypick:mv %{buildroot}%{_bindir}/%{name}{,-mri}}

# Version is empty if --with-ruby-version is specified.
# http://bugs.ruby-lang.org/issues/7807
sed -i 's/Version: \${ruby_version}/Version: %{ruby_version}/' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Kill bundled certificates, as they should be part of ca-certificates.
for cert in \
  rubygems.global.ssl.fastly.net/DigiCertHighAssuranceEVRootCA.pem \
  rubygems.org/AddTrustExternalCARoot.pem \
  index.rubygems.org/GlobalSignRootCA.pem
do
  rm %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/$cert
  rm -r $(dirname %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/$cert)
  rm %{buildroot}%{ruby_libdir}/bundler/ssl_certs/$cert
  rm -r $(dirname %{buildroot}%{ruby_libdir}/bundler/ssl_certs/$cert)
done
# Ensure there is not forgotten any certificate.
test ! "$(ls -A  %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/ 2>/dev/null)"
test "$(ls -A  %{buildroot}%{ruby_libdir}/bundler/ssl_certs/ 2>/dev/null)" \
  = "certificate_manager.rb"

# Move macros file into proper place and replace the %%{name} macro, since it
# would be wrongly evaluated during build of other packages.
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
install -m 644 %{SOURCE5} %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems

# Install dependency generators.
mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 644 %{SOURCE8} %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 755 %{SOURCE9} %{buildroot}%{_rpmconfigdir}
install -m 755 %{SOURCE10} %{buildroot}%{_rpmconfigdir}
install -m 755 %{SOURCE11} %{buildroot}%{_rpmconfigdir}

# Install custom operating_system.rb.
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
cp %{SOURCE1} %{buildroot}%{rubygems_dir}/rubygems/defaults

# Move gems root into common direcotry, out of Ruby directory structure.
mv %{buildroot}%{ruby_libdir}/gems %{buildroot}%{gem_dir}

# Create folders for gem binary extensions.
# TODO: These folders should go into rubygem-filesystem but how to achieve it,
# since noarch package cannot provide arch dependent subpackages?
# http://rpm.org/ticket/78
mkdir -p %{buildroot}%{_exec_prefix}/lib{,64}/gems/%{name}

# Move bundled rubygems to %%gem_dir and %%gem_extdir_mri
# make symlinks for io-console and bigdecimal, which are considered to be part of stdlib by other Gems
mkdir -p %{buildroot}%{gem_dir}/gems/irb-%{irb_version}/lib
mv %{buildroot}%{ruby_libdir}/irb* %{buildroot}%{gem_dir}/gems/irb-%{irb_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/irb-%{irb_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/irb-%{irb_version}/lib/irb.rb %{buildroot}%{ruby_libdir}/irb.rb
# TODO: This should be possible to replaced by simple directory symlink
# after ~ F31 EOL (rhbz#1691039).
mkdir -p %{buildroot}%{ruby_libdir}/irb
pushd %{buildroot}%{gem_dir}/gems/irb-%{irb_version}/lib
find irb -type d -mindepth 1 -exec mkdir %{buildroot}%{ruby_libdir}/'{}' \;
find irb -type f -exec ln -s %{gem_dir}/gems/irb-%{irb_version}/lib/'{}' %{buildroot}%{ruby_libdir}/'{}' \;
popd

mkdir -p %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib
mv %{buildroot}%{ruby_libdir}/rdoc* %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/rdoc-%{rdoc_version}.gemspec %{buildroot}%{gem_dir}/specifications

mkdir -p %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal
mv %{buildroot}%{ruby_libdir}/bigdecimal %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mv %{buildroot}%{ruby_libarchdir}/bigdecimal.so %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}
mv %{buildroot}%{ruby_libarchdir}/bigdecimal/util.so %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal
mv %{buildroot}%{gem_dir}/specifications/default/bigdecimal-%{bigdecimal_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib/bigdecimal %{buildroot}%{ruby_libdir}/bigdecimal
ln -s %{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal.so %{buildroot}%{ruby_libarchdir}/bigdecimal.so
ln -s %{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal/util.so %{buildroot}%{ruby_libarchdir}/bigdecimal/util.so

# TODO: Put help files into proper location.
# https://bugs.ruby-lang.org/issues/15359
mkdir -p %{buildroot}%{gem_dir}/gems/bundler-%{bundler_version}/lib
mv %{buildroot}%{ruby_libdir}/bundler.rb %{buildroot}%{gem_dir}/gems/bundler-%{bundler_version}/lib
mv %{buildroot}%{ruby_libdir}/bundler %{buildroot}%{gem_dir}/gems/bundler-%{bundler_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/bundler-%{bundler_version}.gemspec %{buildroot}%{gem_dir}/specifications

mkdir -p %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/io-console-%{io_console_version}/io
mv %{buildroot}%{ruby_libdir}/io %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mv %{buildroot}%{ruby_libarchdir}/io/console.so %{buildroot}%{_libdir}/gems/%{name}/io-console-%{io_console_version}/io
mv %{buildroot}%{gem_dir}/specifications/default/io-console-%{io_console_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/io-console-%{io_console_version}/lib/io %{buildroot}%{ruby_libdir}/io
ln -s %{_libdir}/gems/%{name}/io-console-%{io_console_version}/io/console.so %{buildroot}%{ruby_libarchdir}/io/console.so

mkdir -p %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/json-%{json_version}
mv %{buildroot}%{ruby_libdir}/json* %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mv %{buildroot}%{ruby_libarchdir}/json/ %{buildroot}%{_libdir}/gems/%{name}/json-%{json_version}/
mv %{buildroot}%{gem_dir}/specifications/default/json-%{json_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/json-%{json_version}/lib/json.rb %{buildroot}%{ruby_libdir}/json.rb
ln -s %{gem_dir}/gems/json-%{json_version}/lib/json %{buildroot}%{ruby_libdir}/json
ln -s %{_libdir}/gems/%{name}/json-%{json_version}/json/ %{buildroot}%{ruby_libarchdir}/json

mkdir -p %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/openssl-%{openssl_version}
mv %{buildroot}%{ruby_libdir}/openssl* %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib
mv %{buildroot}%{ruby_libarchdir}/openssl.so %{buildroot}%{_libdir}/gems/%{name}/openssl-%{openssl_version}/
mv %{buildroot}%{gem_dir}/specifications/default/openssl-%{openssl_version}.gemspec %{buildroot}%{gem_dir}/specifications
# This used to be directory when OpenSSL was integral part of StdLib => Keep
# it as directory and link everything in it to prevent directory => symlink
# conversion RPM issues.
mkdir -p %{buildroot}%{ruby_libdir}/openssl
find %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl -maxdepth 1 -type f -exec \
  sh -c 'ln -s %{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl/`basename {}` %{buildroot}%{ruby_libdir}/openssl' \;
ln -s %{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl.rb %{buildroot}%{ruby_libdir}/openssl.rb
ln -s %{_libdir}/gems/%{name}/openssl-%{openssl_version}/openssl.so %{buildroot}%{ruby_libarchdir}/openssl.so

mkdir -p %{buildroot}%{gem_dir}/gems/psych-%{psych_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/psych-%{psych_version}
mv %{buildroot}%{ruby_libdir}/psych* %{buildroot}%{gem_dir}/gems/psych-%{psych_version}/lib
mv %{buildroot}%{ruby_libarchdir}/psych.so %{buildroot}%{_libdir}/gems/%{name}/psych-%{psych_version}/
mv %{buildroot}%{gem_dir}/specifications/default/psych-%{psych_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/psych-%{psych_version}/lib/psych %{buildroot}%{ruby_libdir}/psych
ln -s %{gem_dir}/gems/psych-%{psych_version}/lib/psych.rb %{buildroot}%{ruby_libdir}/psych.rb
ln -s %{_libdir}/gems/%{name}/psych-%{psych_version}/psych.so %{buildroot}%{ruby_libarchdir}/psych.so

# Move the binary extensions into proper place (if no gem has binary extension,
# the extensions directory might be empty).
find %{buildroot}%{gem_dir}/extensions/*-%{_target_os}/%{ruby_version}/* -maxdepth 0 \
  -exec mv '{}' %{buildroot}%{_libdir}/gems/%{name}/ \; \
  || echo "No gem binary extensions to move."

# Adjust the gemspec files so that the gems will load properly
sed -i '/^end$/ i\
  s.extensions = ["json/ext/parser.so", "json/ext/generator.so"]' %{buildroot}%{gem_dir}/specifications/json-%{json_version}.gemspec

# Move man pages into proper location
mv %{buildroot}%{gem_dir}/gems/rake-%{rake_version}/doc/rake.1 %{buildroot}%{_mandir}/man1

%if %{with systemtap}
# Install a tapset and fix up the path to the library.
mkdir -p %{buildroot}%{tapset_dir}
sed -e "s|@LIBRARY_PATH@|%{tapset_libdir}/libruby.so.%{major_minor_version}|" \
  %{SOURCE2} > %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp
# Escape '*/' in comment.
sed -i -r "s|( \*.*\*)\/(.*)|\1\\\/\2|" %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp
%endif

# Prepare -doc subpackage file lists.
find doc -maxdepth 1 -type f ! -name '.*' ! -name '*.ja*' > .ruby-doc.en
echo 'doc/images' >> .ruby-doc.en
echo 'doc/syntax' >> .ruby-doc.en

find doc -maxdepth 1 -type f -name '*.ja*' > .ruby-doc.ja
echo 'doc/irb' >> .ruby-doc.ja
echo 'doc/pty' >> .ruby-doc.ja

sed -i 's/^/%doc /' .ruby-doc.*
sed -i 's/^/%lang(ja) /' .ruby-doc.ja

# https://github.com/yuki24/did_you_mean/issues/122
rm -rf %{buildroot}%{gem_dir}/gems/did_you_mean-%{did_you_mean_version}/tmp/

# https://github.com/ruby/rake/issues/316
rm -f %{buildroot}%{gem_dir}/gems/rake-%{rake_version}/.gitignore

%check
%if 0%{?with_hardening_test}
# Check Ruby hardening.
checksec --file=libruby.so.%{ruby_version} | \
  grep "Full RELRO.*Canary found.*NX enabled.*DSO.*No RPATH.*No RUNPATH.*Yes.*\d*.*\d*.*libruby.so.%{ruby_version}"
%endif

# Check RubyGems version.
[ "`make runruby TESTRUN_SCRIPT='bin/gem -v' | tail -1`" == '%{rubygems_version}' ]

# Check Rubygems bundled dependencies versions.

# Molinillo.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Gem; module Resolver; end; end; \
  require 'rubygems/resolver/molinillo/lib/molinillo/gem_metadata'; \
  puts Gem::Resolver::Molinillo::VERSION\\\"\" | tail -1`" \
  == '%{rubygems_molinillo_version}' ]

# Check Bundler bundled dependencies versions.

# FileUtils.
# TODO: There is no version in bundled FileUtils yet.
#%%{global bundler_fileutils_version}

# Molinillo.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; end; \
  require 'bundler/vendor/molinillo/lib/molinillo/gem_metadata'; \
  puts Bundler::Molinillo::VERSION\\\"\" | tail -1`" \
  == '%{bundler_molinillo_version}' ]

# Net::HTTP::Persistent.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; module Persistent; module Net; module HTTP; \
  end; end; end; end; \
  require 'bundler/vendor/net-http-persistent/lib/net/http/persistent'; \
  puts Bundler::Persistent::Net::HTTP::Persistent::VERSION\\\"\" | tail -1`" \
  == '%{bundler_net_http_persistent_version}' ]

# Thor.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; end; \
  require 'bundler/vendor/thor/lib/thor/version'; \
  puts Bundler::Thor::VERSION\\\"\" | tail -1`" \
  == '%{bundler_thor_version}' ]


# test_debug(TestRubyOptions) fails due to LoadError reported in debug mode,
# when abrt.rb cannot be required (seems to be easier way then customizing
# the test suite).
touch abrt.rb

# Check if abrt hook is required (RubyGems are disabled by default when using
# runruby, so re-enable them).
make runruby TESTRUN_SCRIPT="--enable-gems %{SOURCE13}"

# Check if systemtap is supported.
%{?with_systemtap:make runruby TESTRUN_SCRIPT=%{SOURCE14}}

DISABLE_TESTS=""
MSPECOPTS=""

# Avoid `hostname' dependency.
%{!?with_hostname:MSPECOPTS="-P 'Socket.gethostname returns the host name'"}

# SIGSEV handler does not provide correct output on AArch64.
# https://bugs.ruby-lang.org/issues/13758
%ifarch aarch64
DISABLE_TESTS="$DISABLE_TESTS -n !/test_segv_\(setproctitle\|test\|loaded_features\)/"
%endif

# Disable failing TestResolvMDNS#test_mdns_each_address test,
# which fails on Koji.
# https://bugs.ruby-lang.org/issues/14175
sed -i '/def test_mdns_each_address$/,/^  end$/ s/^/#/' test/resolv/test_mdns.rb
# Disable Timeouting test_queue_with_trap
# https://github.com/ruby/ruby/pull/3101/
sed -i '/^  def test_queue_with_trap$/,/^  end$/ s/^/#/g' \
  test/ruby/test_thread_queue.rb
# Disable "File.utime allows Time instances in the far future to set
# mtime and atime".
# https://bugs.ruby-lang.org/issues/16410
MSPECOPTS="$MSPECOPTS -P 'File.utime allows Time instances in the far future to set mtime and atime'"

make check TESTS="-v $DISABLE_TESTS" MSPECOPT="-fs $MSPECOPTS"

%files
%license BSDL
%license COPYING
%lang(ja) %license COPYING.ja
%license GPL
%license LEGAL
%{_bindir}/erb
%{_bindir}/%{name}%{?with_rubypick:-mri}
%{_mandir}/man1/erb*
%{_mandir}/man1/ruby*

%files devel
%license BSDL
%license COPYING
%lang(ja) %license COPYING.ja
%license GPL
%license LEGAL

%{_rpmconfigdir}/macros.d/macros.ruby

%{_includedir}/*
%{_libdir}/libruby.so
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%license COPYING
%lang(ja) %license COPYING.ja
%license GPL
%license LEGAL
%doc README.md
%doc NEWS
# Exclude /usr/local directory since it is supposed to be managed by
# local system administrator.
%exclude %{ruby_sitelibdir}
%exclude %{ruby_sitearchdir}
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorarchdir}

# List all these files explicitly to prevent surprises
# Platform independent libraries.
%dir %{ruby_libdir}
%{ruby_libdir}/*.rb
%exclude %{ruby_libdir}/irb.rb
%exclude %{ruby_libdir}/json.rb
%exclude %{ruby_libdir}/openssl.rb
%exclude %{ruby_libdir}/psych.rb
%{ruby_libdir}/cgi
%{ruby_libdir}/csv
%{ruby_libdir}/digest
%{ruby_libdir}/drb
%{ruby_libdir}/e2mmap
%{ruby_libdir}/fiddle
%{ruby_libdir}/fileutils
%{ruby_libdir}/forwardable
%{ruby_libdir}/matrix
%{ruby_libdir}/net
%{ruby_libdir}/optparse
%{ruby_libdir}/racc
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper
%{ruby_libdir}/rss
%{ruby_libdir}/shell
%{ruby_libdir}/syslog
%{ruby_libdir}/thwait
%{ruby_libdir}/tracer
%{ruby_libdir}/unicode_normalize
%{ruby_libdir}/uri
%{ruby_libdir}/webrick
%{ruby_libdir}/yaml

# Platform specific libraries.
%{_libdir}/libruby.so.*
%dir %{ruby_libarchdir}
%dir %{ruby_libarchdir}/cgi
%{ruby_libarchdir}/cgi/escape.so
%{ruby_libarchdir}/continuation.so
%{ruby_libarchdir}/coverage.so
%{ruby_libarchdir}/date_core.so
%{ruby_libarchdir}/dbm.so
%dir %{ruby_libarchdir}/digest
%{ruby_libarchdir}/digest.so
%{ruby_libarchdir}/digest/bubblebabble.so
%{ruby_libarchdir}/digest/md5.so
%{ruby_libarchdir}/digest/rmd160.so
%{ruby_libarchdir}/digest/sha1.so
%{ruby_libarchdir}/digest/sha2.so
%dir %{ruby_libarchdir}/enc
%{ruby_libarchdir}/enc/big5.so
%{ruby_libarchdir}/enc/cp949.so
%{ruby_libarchdir}/enc/emacs_mule.so
%{ruby_libarchdir}/enc/encdb.so
%{ruby_libarchdir}/enc/euc_jp.so
%{ruby_libarchdir}/enc/euc_kr.so
%{ruby_libarchdir}/enc/euc_tw.so
%{ruby_libarchdir}/enc/gb18030.so
%{ruby_libarchdir}/enc/gb2312.so
%{ruby_libarchdir}/enc/gbk.so
%{ruby_libarchdir}/enc/iso_8859_1.so
%{ruby_libarchdir}/enc/iso_8859_10.so
%{ruby_libarchdir}/enc/iso_8859_11.so
%{ruby_libarchdir}/enc/iso_8859_13.so
%{ruby_libarchdir}/enc/iso_8859_14.so
%{ruby_libarchdir}/enc/iso_8859_15.so
%{ruby_libarchdir}/enc/iso_8859_16.so
%{ruby_libarchdir}/enc/iso_8859_2.so
%{ruby_libarchdir}/enc/iso_8859_3.so
%{ruby_libarchdir}/enc/iso_8859_4.so
%{ruby_libarchdir}/enc/iso_8859_5.so
%{ruby_libarchdir}/enc/iso_8859_6.so
%{ruby_libarchdir}/enc/iso_8859_7.so
%{ruby_libarchdir}/enc/iso_8859_8.so
%{ruby_libarchdir}/enc/iso_8859_9.so
%{ruby_libarchdir}/enc/koi8_r.so
%{ruby_libarchdir}/enc/koi8_u.so
%{ruby_libarchdir}/enc/shift_jis.so
%dir %{ruby_libarchdir}/enc/trans
%{ruby_libarchdir}/enc/trans/big5.so
%{ruby_libarchdir}/enc/trans/chinese.so
%{ruby_libarchdir}/enc/trans/ebcdic.so
%{ruby_libarchdir}/enc/trans/emoji.so
%{ruby_libarchdir}/enc/trans/emoji_iso2022_kddi.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_docomo.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_kddi.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_softbank.so
%{ruby_libarchdir}/enc/trans/escape.so
%{ruby_libarchdir}/enc/trans/gb18030.so
%{ruby_libarchdir}/enc/trans/gbk.so
%{ruby_libarchdir}/enc/trans/iso2022.so
%{ruby_libarchdir}/enc/trans/japanese.so
%{ruby_libarchdir}/enc/trans/japanese_euc.so
%{ruby_libarchdir}/enc/trans/japanese_sjis.so
%{ruby_libarchdir}/enc/trans/korean.so
%{ruby_libarchdir}/enc/trans/single_byte.so
%{ruby_libarchdir}/enc/trans/transdb.so
%{ruby_libarchdir}/enc/trans/utf8_mac.so
%{ruby_libarchdir}/enc/trans/utf_16_32.so
%{ruby_libarchdir}/enc/utf_16be.so
%{ruby_libarchdir}/enc/utf_16le.so
%{ruby_libarchdir}/enc/utf_32be.so
%{ruby_libarchdir}/enc/utf_32le.so
%{ruby_libarchdir}/enc/windows_1250.so
%{ruby_libarchdir}/enc/windows_1251.so
%{ruby_libarchdir}/enc/windows_1252.so
%{ruby_libarchdir}/enc/windows_1253.so
%{ruby_libarchdir}/enc/windows_1254.so
%{ruby_libarchdir}/enc/windows_1257.so
%{ruby_libarchdir}/enc/windows_31j.so
%{ruby_libarchdir}/etc.so
%{ruby_libarchdir}/fcntl.so
%{ruby_libarchdir}/fiber.so
%{ruby_libarchdir}/fiddle.so
%{ruby_libarchdir}/gdbm.so
%dir %{ruby_libarchdir}/io
%{ruby_libarchdir}/io/nonblock.so
%{ruby_libarchdir}/io/wait.so
%{ruby_libarchdir}/nkf.so
%{ruby_libarchdir}/objspace.so
%{ruby_libarchdir}/pathname.so
%{ruby_libarchdir}/pty.so
%dir %{ruby_libarchdir}/racc
%{ruby_libarchdir}/racc/cparse.so
%dir %{ruby_libarchdir}/rbconfig
%{ruby_libarchdir}/rbconfig.rb
%{ruby_libarchdir}/rbconfig/sizeof.so
%{ruby_libarchdir}/readline.so
%{ruby_libarchdir}/ripper.so
%{ruby_libarchdir}/sdbm.so
%{ruby_libarchdir}/socket.so
%{ruby_libarchdir}/stringio.so
%{ruby_libarchdir}/strscan.so
%{ruby_libarchdir}/syslog.so
%{ruby_libarchdir}/zlib.so

%{?with_systemtap:%{tapset_root}}

%files -n rubygems
%{_bindir}/gem
%dir %{rubygems_dir}
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb

# Explicitly include only RubyGems directory strucure to avoid accidentally
# packaged content.
%dir %{gem_dir}
%dir %{gem_dir}/build_info
%dir %{gem_dir}/cache
%dir %{gem_dir}/doc
%dir %{gem_dir}/extensions
%dir %{gem_dir}/gems
%dir %{gem_dir}/specifications
%dir %{gem_dir}/specifications/default
%dir %{_exec_prefix}/lib*/gems
%dir %{_exec_prefix}/lib*/gems/ruby

%exclude %{gem_dir}/cache/*

# TODO: Gemify these libraries
%{gem_dir}/specifications/default/cmath-1.0.0.gemspec
%{gem_dir}/specifications/default/csv-3.0.9.gemspec
%{gem_dir}/specifications/default/date-2.0.0.gemspec
%{gem_dir}/specifications/default/dbm-1.0.0.gemspec
%{gem_dir}/specifications/default/e2mmap-0.1.0.gemspec
%{gem_dir}/specifications/default/etc-1.0.1.gemspec
%{gem_dir}/specifications/default/fcntl-1.0.0.gemspec
%{gem_dir}/specifications/default/fiddle-1.0.0.gemspec
%{gem_dir}/specifications/default/fileutils-1.1.0.gemspec
%{gem_dir}/specifications/default/forwardable-1.2.0.gemspec
%{gem_dir}/specifications/default/gdbm-2.0.0.gemspec
%{gem_dir}/specifications/default/ipaddr-1.2.2.gemspec
%{gem_dir}/specifications/default/logger-1.3.0.gemspec
%{gem_dir}/specifications/default/matrix-0.1.0.gemspec
%{gem_dir}/specifications/default/mutex_m-0.1.0.gemspec
%{gem_dir}/specifications/default/ostruct-0.1.0.gemspec
%{gem_dir}/specifications/default/prime-0.1.0.gemspec
%{gem_dir}/specifications/default/rexml-3.1.9.gemspec
%{gem_dir}/specifications/default/rss-0.2.7.gemspec
%{gem_dir}/specifications/default/scanf-1.0.0.gemspec
%{gem_dir}/specifications/default/sdbm-1.0.0.gemspec
%{gem_dir}/specifications/default/shell-0.7.gemspec
%{gem_dir}/specifications/default/stringio-0.0.2.gemspec
%{gem_dir}/specifications/default/strscan-1.0.0.gemspec
%{gem_dir}/specifications/default/sync-0.5.0.gemspec
%{gem_dir}/specifications/default/thwait-0.1.0.gemspec
%{gem_dir}/specifications/default/tracer-0.1.0.gemspec
%{gem_dir}/specifications/default/webrick-1.4.2.gemspec
%{gem_dir}/specifications/default/zlib-1.0.0.gemspec

%files -n rubygems-devel
%{_rpmconfigdir}/macros.d/macros.rubygems
%{_rpmconfigdir}/fileattrs/rubygems.attr
%{_rpmconfigdir}/rubygems.req
%{_rpmconfigdir}/rubygems.prov
%{_rpmconfigdir}/rubygems.con

%files -n rubygem-rake
%{_bindir}/rake
%{gem_dir}/gems/rake-%{rake_version}
%{gem_dir}/specifications/rake-%{rake_version}.gemspec
%{_mandir}/man1/rake.1*

%files -n rubygem-irb
%{_bindir}/irb
%{ruby_libdir}/irb*
%{gem_dir}/gems/irb-%{irb_version}
%{gem_dir}/specifications/irb-%{irb_version}.gemspec
%{_mandir}/man1/irb.1*

%files -n rubygem-rdoc
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_dir}/gems/rdoc-%{rdoc_version}
%{gem_dir}/specifications/rdoc-%{rdoc_version}.gemspec
%{_mandir}/man1/ri*

%files doc -f .ruby-doc.en -f .ruby-doc.ja
%doc README.md
%doc ChangeLog
%{?with_systemtap:%doc ruby-exercise.stp}
%{_datadir}/ri

%files -n rubygem-bigdecimal
%{ruby_libdir}/bigdecimal
%{ruby_libarchdir}/bigdecimal*
%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}
%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}
%{gem_dir}/specifications/bigdecimal-%{bigdecimal_version}.gemspec

%files -n rubygem-did_you_mean
%{gem_dir}/gems/did_you_mean-%{did_you_mean_version}
%exclude %{gem_dir}/gems/did_you_mean-%{did_you_mean_version}/.*
%{gem_dir}/specifications/did_you_mean-%{did_you_mean_version}.gemspec

%files -n rubygem-io-console
%{ruby_libdir}/io
%{ruby_libarchdir}/io/console.so
%{_libdir}/gems/%{name}/io-console-%{io_console_version}
%{gem_dir}/gems/io-console-%{io_console_version}
%{gem_dir}/specifications/io-console-%{io_console_version}.gemspec

%files -n rubygem-json
%{ruby_libdir}/json*
%{ruby_libarchdir}/json*
%{_libdir}/gems/%{name}/json-%{json_version}
%{gem_dir}/gems/json-%{json_version}
%{gem_dir}/specifications/json-%{json_version}.gemspec

%files -n rubygem-minitest
%{gem_dir}/gems/minitest-%{minitest_version}
%exclude %{gem_dir}/gems/minitest-%{minitest_version}/.*
%{gem_dir}/specifications/minitest-%{minitest_version}.gemspec

%files -n rubygem-openssl
%{ruby_libdir}/openssl
%{ruby_libdir}/openssl.rb
%{ruby_libarchdir}/openssl.so
%{_libdir}/gems/%{name}/openssl-%{openssl_version}
%{gem_dir}/gems/openssl-%{openssl_version}
%{gem_dir}/specifications/openssl-%{openssl_version}.gemspec

%files -n rubygem-power_assert
%{gem_dir}/gems/power_assert-%{power_assert_version}
%exclude %{gem_dir}/gems/power_assert-%{power_assert_version}/.*
%{gem_dir}/specifications/power_assert-%{power_assert_version}.gemspec

%files -n rubygem-psych
%{ruby_libdir}/psych
%{ruby_libdir}/psych.rb
%{ruby_libarchdir}/psych.so
%{_libdir}/gems/%{name}/psych-%{psych_version}
%{gem_dir}/gems/psych-%{psych_version}
%{gem_dir}/specifications/psych-%{psych_version}.gemspec

%files -n rubygem-net-telnet
%{gem_dir}/gems/net-telnet-%{net_telnet_version}
%exclude %{gem_dir}/gems/net-telnet-%{net_telnet_version}/.*
%{gem_dir}/specifications/net-telnet-%{net_telnet_version}.gemspec

%files -n rubygem-test-unit
%{gem_dir}/gems/test-unit-%{test_unit_version}
%{gem_dir}/specifications/test-unit-%{test_unit_version}.gemspec

%files -n rubygem-xmlrpc
%license %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/LICENSE.txt
%dir %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}
%exclude %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/.*
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/Gemfile
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/Rakefile
%doc %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/README.md
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/bin
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/lib
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/xmlrpc.gemspec
%{gem_dir}/specifications/xmlrpc-%{xmlrpc_version}.gemspec

%files -n rubygem-bundler
%{_bindir}/bundle
%{_bindir}/bundler
%{gem_dir}/gems/bundler-%{bundler_version}
%{gem_dir}/specifications/bundler-%{bundler_version}.gemspec
%{_mandir}/man1/bundle*.1*
%{_mandir}/man5/gemfile.5*

%changelog
* Tue Sep 29 2020 Andrew Lau <andrelau@amazon.com> - 2.6.6-125.amzn2.0.3
- ARM64 optimizations provided by Ali Saidi <alisaidi@amazon.com>
  https://github.com/ruby/ruby/pull/3393

* Mon Sep 07 2020 Andrew Lau <andrelau@amazon.com> - 2.6.6-125.amzn2
- Rebuild for Amazon Linux 2 (Extras Library).
- Fixes: CVE-2012-6708 CVE-2015-9251 CVE-2019-15845 CVE-2019-16201
  CVE-2019-16254 CVE-2019-16255 CVE-2020-10663 CVE-2020-10933

* Thu May 07 2020 Pavel Valena <pvalena@redhat.com> - 2.6.6-125
- Upgrade to Ruby 2.6.6.
  Resolves: rhbz#1833293
  Resolves: rhbz#1827505

* Tue Oct 08 2019 Slava Kardakov <ojab@ojab.ru> - 2.6.5-124
- Update to Ruby 2.6.5.

* Fri Aug 30 2019 Pavel Valena <pvalena@redhat.com> - 2.6.4-123
- Update to Ruby 2.6.4.
- Fix checksec 2.0+ compatibility.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-122
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.3-121
- Properly support %%prerelease in %%gemspec_ macros.

* Thu Apr 25 2019 Pavel Valena <pvalena@redhat.com> - 2.6.3-120
- Update to Ruby 2.6.3.

* Thu Mar 28 2019 Arjen Heidinga <dexter@beetjevreemd.nl> - 2.6.2-119
- Add zlib-devel explicitly as BuildRequirement.

* Thu Mar 21 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.2-118
- Link IRB files instead of directories, which RPM cannot handle
  during updates (rhbz#1691039).

* Tue Mar 19 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.2-117
- Link IRB back to StdLib.

* Thu Mar 14 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.2-116
- Upgrade to Ruby 2.6.2.

* Tue Mar 05 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.1-115
- Fix ".include =" support in openssl.cnf (rhbz#1668916).

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.6.1-114
- Rebuild for readline 8.0

* Thu Feb 07 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.1-113
- Don't ship .stp files when SystemTap support is disabled.

* Thu Jan 31 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.1-112
- Upgrade to Ruby 2.6.1.

* Thu Jan 24 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.0-111
- Properly generate versioned ruby(rubygems) dependencies.
- Loosen RDoc dependency.

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 2.6.0-110
- Upgrade to Ruby 2.6.0.

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.5.3-104
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jan 11 2019 Jun Aruga <jaruga@redhat.com> - 2.5.3-103
- Refresh expired certificates to fix FTBFS.

* Tue Nov 13 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.3-102
- Fix Tokyo TZ tests.

* Fri Oct 19 2018 Jun Aruga <jaruga@redhat.com> - 2.5.3-101
- Update to Ruby 2.5.3.

* Mon Sep 03 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-100
- Properly harden package using -fstack-protector-strong.

* Wed Aug 29 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-99
- Additional OpenSSL 1.1.1 fixes.
- Add --with-cxxflags configuration for %%gem_install macro.

* Tue Aug 28 2018 Jun Aruga <jaruga@redhat.com> - 2.5.1-99
- Fix generated rdoc template issues.

* Mon Aug 13 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-98
- Properly execute entire test suite.

* Mon Aug 13 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-97
- Fix TLS 1.3 issues.

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 2.5.1-96
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.1-95
- Rebuild for new binutils

* Thu Jul 26 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-94
- Disable some test failing with OpenSSL 1.1.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-94
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Pavel Valena <pvalena@redhat.com> - 2.5.1-93
- Add macros to edit files lists in .gemspec
  (gemspec_add_file and gemspec_remove_file).

* Wed May 02 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-93
- Make %%gemspec_{add,remove}_dep modify .gemspec provided by %%setup macro.

* Tue Apr 10 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.1-92
- Conflict requirement needs to generate dependency.
- Stop using --with-setjmp-type=setjmp on aarch64 (rhbz#1545239).

* Thu Mar 29 2018 Pavel Valena <pvalena@redhat.com> - 2.5.1-92
- Update to Ruby 2.5.1.

* Mon Mar 05 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.0-91
- Don't force libraries used to build Ruby to its dependencies.
- Re-enable GMP dependency.

* Thu Mar 01 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.0-90
- Drop GMP dependency.

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 2.5.0-89
- Rebuild with new LDFLAGS from redhat-rpm-config
- Use --with-setjmp-type=setjmp on aarch64 to work around gcc issue (#1545239)

* Wed Feb 21 2018 Pavel Valena <pvalena@redhat.com> - 2.5.0-89
- Fix: Multiple vulnerabilities in RubyGems
  https://bugzilla.redhat.com/show_bug.cgi?id=1547431
  https://www.ruby-lang.org/en/news/2018/02/17/multiple-vulnerabilities-in-rubygems/

* Tue Feb 13 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.0-89
- Drop obsolete ldconfig scriptlets.
- Add GMP dependency.
- Use 'with' operator in RPM dependency generator.
- Add conflicts RPM generator.
- Fix thread_safe test suite segfaults.
- Fix invalid licenses.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-89
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.5.0-88
- Rebuilt for switch to libxcrypt

* Tue Jan 09 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.0-87
- Fix segfaults during generating of documentation.

* Tue Jan 02 2018 Vít Ondruch <vondruch@redhat.com> - 2.5.0-86
- Upgrade to Ruby 2.5.0.

* Fri Oct 27 2017 Jun Aruga <jaruga@redhat.com> - 2.4.2-86
- Add macro to remove rubypick dependency.
- Improve "with" conditional statement as inline.

* Thu Oct 19 2017 Jun Aruga <jaruga@redhat.com> - 2.4.2-85
- Add macros to remove systemtap, git and cmake dependencies.

* Mon Sep 18 2017 Pavel Valena <pvalena@redhat.com> - 2.4.2-84
- Update to Ruby 2.4.2.

* Fri Sep 08 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.1-84
- Drop ruby-devel dependency on rubypick, which is pulled in transtitively.

* Fri Aug 11 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.1-83
- Fix "IOError: stream closed" errors affecting Puma.
- Temporary disable checksec on PPC64LE (rhbz#1479302).

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-82
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-81
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.1-80
- OpenSSL 1.1.0f-3 disables some weak ciphers. Adjust the package to pass
  the tests suite.

* Mon Apr 03 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.1-79
- Update to Ruby 2.4.1.

* Thu Feb 23 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-78
- Fix OpenSSL symlinks.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-77
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-76
- Fix GCC 7.x compatibility (rhbz#1417590).
- Use standardized multilib solution (rhbz#1412274).

* Tue Jan 17 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-75
- Apply patch fixing rubygem-mongo build failures.

* Fri Jan 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.4.0-74
- Rebuild again for f26-ruby24 sidetag

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.0-73
- Rebuild for readline 7.x

* Wed Jan 11 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-72
- Link files into directory to avoid dir => symlink isues.

* Mon Jan 09 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-71
- Add rubygem-io-console dependency for rubygem-rdoc.

* Mon Jan 02 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-70
- Upgrade to Ruby 2.4.0.
- Move gemified xmlrpc into subpackage.
- Move gemified openssl into subpackage.
- Tk is removed from stdlib.
- Extend 'gem_' macros for pre-release version support.

* Tue Nov 22 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.3-61
- Update to Ruby 2.3.3.
- Exclude json.rb from ruby-libs (rhbz#1397370).

* Fri Nov 18 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.2-60
- Update to Ruby 2.3.2.

* Fri Oct 21 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.1-59
- Continue to use OpenSSL 1.0 for the moment.
- Add gemspec_add_dep and gemspec_remove_dep macros.
- Harden package.

* Wed Aug 10 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.1-58
- Workaround "an invalid stdio handle" error on PPC (rhbz#1361037).

* Tue Jul 12 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.1-57
- Make symlinks for json gem.

* Mon May 23 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.1-56
- Requires rubygem(json) for rubygem-rdoc (rhbz#1325022).

* Fri Apr 29 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.1-55
- Update to Ruby 2.3.1.

* Wed Feb  3 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.0-54
- Add rubypick and rubygems requires to ruby-devel to deal with BuildRequires

* Fri Jan 15 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-53
- Backport trunk@53455 to make ruby-qt build

* Wed Jan 06 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.0-52
- Explicitly require RDoc, since weak dependencies are ignored by default.

* Wed Jan 06 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.0-51
- Load RubyGems prior ABRT hook to properly rescue RubyGems exceptions.

* Mon Jan 04 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.0-50
- Upgrade to Ruby 2.3.0.
- Move gemified net-telnet into subpackage.
- Add did_you_mean subpackage.
- Add virtual provides for CCAN copylibs.
- Use weak dependencies.

* Tue Dec 22 2015 Pavel Valena <pvalena@redhat.com> - 2.3.0-0.7.preview2
- Add systemtap tests.

* Mon Dec 21 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.4-47
- Update to Ruby 2.2.4.

* Thu Dec 10 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.3-46
- Fix ABRT hook autoloading.

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 2.2.3-45
- Add support for MIPS architecture to config.h

* Tue Sep 01 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.3-44
- Update to Ruby 2.2.3.

* Tue Jun 23 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.2-43
- Fix for "dh key too small" error of OpenSSL 1.0.2+.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.2-41
- Fix the git BR following the git package split.

* Mon May 04 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.2-40
- Fix upgrade path (rubygem-io-console's version was recently bumped in F21
  and makes the higher release to win).

* Tue Apr 14 2015 Josef Stribny <jstribny@redhat.com> - 2.2.2-11
- Bump release because of gems

* Tue Apr 14 2015 Josef Stribny <jstribny@redhat.com> - 2.2.2-1
- Update to Ruby 2.2.2

* Fri Mar 20 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.1-10
- Fix libruby.so versions in SystemTap scripts (rhbz#1202232).

* Wed Mar 04 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.1-9
- Update to Ruby 2.2.1.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.2.0-8
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 05 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.0-7
- Fix directory ownership.

* Wed Feb 04 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.0-6
- Initialize all load paths in operating_system.rb.

* Tue Feb 03 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.0-5
- Make operating_system.rb more robust.
- Add RubyGems stub headers for bundled gems.

* Thu Jan 29 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.0-4
- Add missing rubygem-test-unit dependency on rubygem-power_assert.

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-3
- Bump release to avoid EVR issue on rubygem-test-unit

* Fri Jan 02 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.0-1
- Upgrade to Ruby 2.2.0.
- Explicitly list RubyGems directories to avoid accidentaly packaged content.
- Split test-unit and power_assert gems into separate sub-packages.
- Drop libdb dependency in favor of gdbm.

* Fri Dec 26 2014 Orion Poplwski <orion@cora.nwra.com> - 2.1.5-26
- Disbable sse2 on i668 (bug #1101811)

* Thu Nov 20 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.5-25
- Update to Ruby 2.1.5.

* Fri Oct 31 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.4-24
- Update to Ruby 2.1.4.
- Include only vendor directories, not their content (rhbz#1114071).
- Fix "invalid regex" warning for non-rubygem packages (rhbz#1154067).
- Use load macro introduced in RPM 4.12.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.2-23
- Fix FTBFS 
- Specify tcl/tk 8.6
- Add upstream patch to build with libffi 3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com>
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue May 20 2014 Josef Stribny <jstribny@redhat.com> - 2.1.2-21
- Update to Ruby 2.1.2

* Tue May 06 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.1-20
- Remove useless exclude (rhbz#1065897).
- Extract load macro into external file and include it.
- Kill bundled certificates.

* Wed Apr 23 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.1-19
- Correctly expand $(prefix) in some Makefiles, e.g. eruby.

* Tue Apr 08 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.1-18
- Update to Ruby 2.1.1.
- Revert regression of Hash#reject.

* Mon Mar 03 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.0-19
- Add RPM dependency generators for RubyGems.

* Mon Feb 10 2014 Josef Stribny <jstribny@redhat.com> - 2.1.0-19
- Don't link cert.pem explicitely

* Wed Jan 15 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.0-18
- Don't generate documentation on unexpected places.
- Detect if rubygems are running under rpmbuild and install gem binary
  extensions into appropriate place.
- Add support for ppc64le arch (rhbz#1053263).
- Re-enable some test cases, which are passing now with Kernel 3.12.8+.
- Backport fix for floating point issues on i686.

* Thu Jan 02 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.0-17
- Upgrade to Ruby 2.1.0.
- Move RPM macros into /usr/lib/rpm/macros.d directory.
- Allow MD5 in OpenSSL for tests.

* Tue Jul 30 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-15
- Move Psych symlinks to vendor dir, to prevent F18 -> F19 upgrade issues
  (rhbz#988490).

* Mon Jul 15 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-14
- Add forgotten psych.rb link into rubygem-psych to fix "private method `load'
  called for Psych:Moduler" error (rhbz#979133).

* Thu Jul 11 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-13
- Fixes multilib conlicts of .gemspec files.
- Make symlinks for psych gem to ruby stdlib dirs (rhbz#979133).
- Use system-wide cert.pem.

* Thu Jul 04 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-12
- Fix RubyGems search paths when building gems with native extension
  (rhbz#979133).

* Tue Jul 02 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-11
- Fix RubyGems version.

* Tue Jul 02 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-10
- Better support for build without configuration (rhbz#977941).

* Mon Jul 01 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.247-9
- Update to Ruby 2.0.0-p247 (rhbz#979605).
- Fix CVE-2013-4073.
- Fix for wrong makefiles created by mkmf (rhbz#921650).
- Add support for ABRT autoloading.

* Fri May 17 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.195-8
- Update to Ruby 2.0.0-p195 (rhbz#917374).
- Fix object taint bypassing in DL and Fiddle (CVE-2013-2065).
- Fix build against OpenSSL with enabled ECC curves.
- Add aarch64 support (rhbz#926463).

* Fri Apr 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-7
- Macro definition moved into macros.ruby and macros.rubygems files.
- Added filtering macros.
- Filter automatically generated provides of private libraries (rhbz#947408).

* Fri Mar 22 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-6
- Fix RbConfig::CONFIG['exec_prefix'] returns empty string (rhbz#924851).

* Thu Mar 21 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-5
- Make Ruby buildable without rubypick.
- Prevent random test failures.

* Fri Mar 08 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.0.0-4
- Don't mark rpm config file as %%config (fpc#259)

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-3
- Avoid "method redefined;" warnings due to modified operating_system.rb.
- Fix strange paths created during build of binary gems.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-2
- Prevent squash of %%gem_install with following line.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-1
- Update to Ruby 2.0.0-p0.
- Change %%{ruby_extdir} to %%{ruby_extdir_mri} in preparation for better
  JRuby support.

* Mon Feb 25 2013 Mamoru TASAKA <mtasaka@fedoraprojec.org> - 2.0.0.0-0.3.r39387
- Move test-unit.gemspec to -libs subpackage for now because rubygems
  2.0.0 does not create this

* Fri Feb 22 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-0.2.r39387
- Fix issues with wrong value of Rubygem's shebang introduced in r39267.

* Fri Feb 22 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0.0-0.1.r39387
- Upgrade to Ruby 2.0.0 (r39387).
- Introduce %%gem_install macro.
- Build against libdb instead of libdb4 (rhbz#894022).
- Move native extensions from exts to ruby directory.
- Enable most of the PPC test suite.
- Change ruby(abi) -> ruby(release).
- Rename ruby executable to ruby-mri, to be prepared for RubyPick.
- Add ruby(runtime_executable) virtual provide, which is later used
  by RubyPick.
- RDoc now depends on JSON.
- Try to make -doc subpackage noarch again, since the new RDoc should resolve
  the arch dependent issues (https://github.com/rdoc/rdoc/issues/71).
- Enable SystemTap support.
- Add TapSet for Ruby.
- Split Psych into rubygem-psych subpackage.

* Mon Feb 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.385-28
- Update to 1.9.3 p385

* Sat Jan 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.374-27
- Update to 1.9.3 p374
- Fix provided variables in pkgconfig (bug 789532:
  Vít Ondruch <vondruch@redhat.com>)

* Fri Jan 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.362-26
- Provide non-versioned pkgconfig file (bug 789532)
- Use db5 on F-19 (bug 894022)
 
* Wed Jan 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.362-25
- Backport fix for the upstream PR7629, save the proc made from the given block
  (bug 895173)

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.362-24
- Update to 1.9.3.362

* Mon Dec 03 2012 Jaromir Capik <jcapik@redhat.com> - 1.9.3.327-23
- Skipping test_parse.rb (fails on ARM at line 787)
- http://bugs.ruby-lang.org/issues/6899

* Sun Nov 11 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.327-23
- Skip test_str_crypt (on rawhide) for now (upstream bug 7312)

* Sat Nov 10 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.327-22
- Ignore some network related tests

* Sat Nov 10 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.327-21
- Update to 1.9.3.327
- Fix Hash-flooding DoS vulnerability on MurmurHash function
  (CVE-2012-5371)

* Sat Oct 13 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3.286-19
- Update to 1.9.3 p286
- Don't create files when NUL-containing path name is passed
  (bug 865940, CVE-2012-4522)

* Thu Oct 04 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.9.3.194-18
- Patch from trunk for CVE-2012-4464, CVE-2012-4466

* Thu Sep 06 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.194-17
- Split documentation into -doc subpackage (rhbz#854418).

* Tue Aug 14 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.194-16
- Revert the dependency of ruby-libs on rubygems (rhbz#845011, rhbz#847482).

* Wed Aug 01 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.194-15
- ruby-libs must require rubygems (rhbz#845011).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3.194-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.9.3.194-13
- Make the bigdecimal gem a runtime dependency of Ruby.

* Mon Jun 11 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.9.3.194-12
- Make symlinks for bigdecimal and io-console gems to ruby stdlib dirs (RHBZ 829209).

* Tue May 29 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.9.3.194-11
- Fix license to contain Public Domain.
- macros.ruby now contains unexpanded macros.

* Sun Apr 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.9.3.194-10.1
- Bump release

* Fri Apr 20 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.194-1
- Update to Ruby 1.9.3-p194.

* Mon Apr 09 2012 Karsten Hopp <karsten@redhat.com> 1.9.3.125-3
- disable check on ppc(64), RH bugzilla 803698

* Wed Feb 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.3.125-2
- Temporarily disable make check on ARM until it's fixed upstream. Tracked in RHBZ 789410

* Mon Feb 20 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.125-1
- Upgrade to Ruby 1.9.3-p125.

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraprpject.org> - 1.9.3.0-7
- Make mkmf.rb verbose by default

* Thu Jan 26 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-6
- Relax dependencies to allow external updates of bundled gems.

* Wed Jan 18 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-5
- Initial release of Ruby 1.9.3.
- Add rubygems dependency on io-console for user interactions.
- Gems license clarification.

* Tue Jan 17 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-4
- Bundled gems moved into dedicated directories and subpackages.
- Create and own RubyGems directories for binary extensions.
- Fix build with GCC 4.7.

* Mon Jan 16 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-3
- Fix RHEL build.
- Fixed directory ownership.
- Verose build output.

* Sun Jan 15 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-2
- Install RubyGems outside of Ruby directory structure.
- RubyGems has not its own -devel subpackage.
- Enhanced macros.ruby and macros.rubygems.
- All tests are green now (bkabrda).

* Sat Jan 14 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-1
- Initial package

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.7.357-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.7.357-1
- Update to 1.8.7p357
- Randomize hash on process startup (CVE-2011-4815, bug 750564)

* Fri Dec 23 2011 Dennis Gilmore <dennis@ausil.us> - 1.8.7.352-2
- dont normalise arm cpus to arm
- there is something weird about how ruby choses where to put bits

* Thu Nov 17 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.7.352-3
- F-17: kill gdbm support for now due to licensing compatibility issue

* Sat Oct  1 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.7.352-2
- F-17: rebuild against new gdbm

* Sat Jul 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.7.352-1
- Update to 1.8.7 p352
- CVE-2011-2686 is fixed in this version (bug 722415)
- Update ext/tk to the latest git
- Remove duplicate path entry (bug 718695)

* Thu Jul 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.7.334-4
- Once fix FTBFS (bug 716021)

* Mon Jul 11 2011 Dennis Gilmore <dennis@ausil.us> - 1.8.7.334-3
- normalise arm cpus to arm

* Mon May 30 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.7.334-2
- Own %%{_normalized_cpu}-%%{_target_os} directory (bug 708816)

* Sat Feb 19 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.7.334-1
- Update to 1.8.7 p334

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.7.330-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Dennis Gilmore <dennis@ausil.us> - 1.8.7.330-2
- nomalise the 32 bit sparc archs to sparc

* Sun Dec 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.7.330-1
- Update to 1.8.7 p330
- ext/tk updated to the newest header

* Thu Nov  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.7.302-2
- Avoid multilib conflict on -libs subpackage (bug 649174)

* Mon Aug 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.7.302-1
- Update to 1.8.7.302
- CVE-2010-0541 (bug 587731) is fixed in this version
- Update ext/tk to the latest head

* Mon Aug  2 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.7.299-5
- More cleanup of spec file, expecially for rpmlint issue
- build ri files in %%build

* Mon Jul 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.7.299-4
- Cleanup spec file
- Make -irb, -rdoc subpackage noarch
- Make dependencies between arch-dependent subpackages isa specific
- Improve sample documentation gathering

* Mon Jul 12 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.299-3
- updated packaged based on feedback (from mtasaka)
- added comments to all patches / sources
- obsoleted ruby-mode, as it's now provided by the emacs package itself
- readded missing documentation
- various small compatability/regression fixes

* Tue Jul 06 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.299-2
- readded bits to pull tk package from upstream source branch
- removed unecessary .tk.old dir
- renamed macros which may cause confusion, removed unused ones

* Thu Jun 24 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.299-1
- integrate more of jmeyering's and mtaska's feedback
- removed emacs bits that are now shipped with the emacs package
- various patch and spec cleanup
- rebased to ruby 1.8.7 patch 299, removed patches no longer needed:
   ruby-1.8.7-openssl-1.0.patch, ruby-1.8.7-rb_gc_guard_ptr-optimization.patch

* Wed Jun 23 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.249-5
- Various fixes

* Wed Jun 23 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.249-4
- Fixed incorrect paths in 1.8.7 rpm

* Tue Jun 22 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.249-3
- Integrated Jim Meyering's feedback and changes in to:
- remove trailing blanks
- placate rpmlint
- ruby_* definitions: do not use trailing slashes in directory names
- _normalized_cpu: simplify definition

* Mon Jun 21 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.249-2
- Integrate mtasaka's feedback and changes
- patch101 ruby_1_8_7-rb_gc_guard_ptr-optimization.patch

* Tue Jun 15 2010 Mohammed Morsi <mmorsi@redhat.com> - 1.8.7.249-1
- Initial Ruby 1.8.7 specfile

* Wed May 19 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.399-5
- Retry for bug 559158, Simplify the OpenSSL::Digest class
  pull more change commits from ruby_1_8 branch

* Mon May 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.399-4
- Patch36 (ruby-1.8.x-RHASH_SIZE-rb_hash_lookup-def.patch)
  also backport rb_hash_lookup definition (bug 592936)

* Thu May 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.399-3
- ruby-1.8.x-null-class-must-be-Qnil.patch (bug 530407)
- Recreate some patches using upstream svn when available, and
  add some comments for patches

* Tue May 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.399-2
- tcltk: Give up using potentially unmaintained ruby_1_8_6 branch
  and instead completely replace with ruby_1_8 branch head
  (at this time, using rev 27738)
  (seems to fix 560053, 590503)
- Fix Japanese encoding strings under ruby-tcltk/ext/tk/sample/

* Tue Apr 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.399-1
- Update to 1.8.6 p 399 (bug 579675)
- Patch to fix gc bug causing open4 crash (bug 580993)

* Fri Mar 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.388-9
- F-14: rebuild against new gdbm

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Once revert the previous change (patch34)

* Wed Jan 27 2010 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.8.6.388-8
- Backport openssl/digest functions providing digest and hexdigest functions
  directly in OpenSSL::Digest.methods
- Make sure that Red Hat people version their changelog entries
- This is actually release #1, but now needs to be release #7

* Mon Jan 18 2010 Akira TAGOH <tagoh@redhat.com> - 1.8.6.388-1
- Add conditional for RHEL.

* Wed Jan 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.383-6
- CVE-2009-4492 ruby WEBrick log escape sequence (bug 554485)

* Wed Dec  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.383-5
- Change mkmf.rb to use LIBRUBYARG_SHARED so that have_library() works
  without libruby-static.a (bug 428384)
- And move libruby-static.a to -static subpackage

* Thu Oct 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.383-4
- Use bison to regenerate parse.c to keep the original format of error
  messages (bug 530275 comment 4)

* Sun Oct 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.383-3
- Patch so that irb saves its history (bug 518584, ruby issue 1556)

* Sat Oct 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.383-2
- Update to 1.8.6 patchlevel 383 (bug 520063)

* Wed Oct 14 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.369-5
- Much better idea for Patch31 provided by Akira TAGOH <tagoh@redhat.com>

* Wed Oct 14 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.369-4
- Fix the search path of ri command for ri manuals installed with gem
  (bug 528787)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.6.369-3
- Rebuild against new openssl

* Thu Jul 23 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.369-2
- Make sure that readline.so is linked against readline 5 because
  Ruby is under GPLv2

* Sat Jun 20 2009  Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.8.6.369-1
- New patchlevel fixing CVE-2009-1904
- Fix directory on ARM (#506233, Kedar Sovani)

* Sun May 31 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.8.6.368-1
- New upstream release (p368)

* Sat Apr 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.287-8
- Merge Review fix (#226381)

* Wed Mar 18 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.8.6.287-7
- Fix regression in CVE-2008-3790 (#485383)

* Mon Mar 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.8.6.287-6
- Again use -O2 optimization level
- i586 should search i386-linux directory (on <= F-11)

* Thu Mar 05 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.8.6.287-5
- Rebuild for gcc4.4

* Fri Feb 27 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.8.6.287-3
- CVE-2008-5189: CGI header injection.

* Wed Oct  8 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.287-2
- CVE-2008-3790: DoS vulnerability in the REXML module.

* Sat Aug 23 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.287-1
- New upstream release.
- Security fixes.
  - CVE-2008-3655: Ruby does not properly restrict access to critical
                   variables and methods at various safe levels.
  - CVE-2008-3656: DoS vulnerability in WEBrick.
  - CVE-2008-3657: Lack of taintness check in dl.
  - CVE-2008-1447: DNS spoofing vulnerability in resolv.rb.
  - CVE-2008-3443: Memory allocation failure in Ruby regex engine.
- Remove the unnecessary backported patches.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.8.6.230-5
- rebuild against db4-4.7

* Tue Jul  1 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-4
- Backported from upstream SVN to fix a segfault issue with Array#fill.

* Mon Jun 30 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-3
- Backported from upstream SVN to fix a segfault issue. (#452825)
- Backported from upstream SVN to fix an integer overflow in rb_ary_fill.

* Wed Jun 25 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-2
- Fix a segfault issue. (#452810)

* Tue Jun 24 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.230-1
- New upstream release.
- Security fixes. (#452295)
  - CVE-2008-1891: WEBrick CGI source disclosure.
  - CVE-2008-2662: Integer overflow in rb_str_buf_append().
  - CVE-2008-2663: Integer overflow in rb_ary_store().
  - CVE-2008-2664: Unsafe use of alloca in rb_str_format().
  - CVE-2008-2725: Integer overflow in rb_ary_splice().
  - CVE-2008-2726: Integer overflow in rb_ary_splice().
- ruby-1.8.6.111-CVE-2007-5162.patch: removed.
- Build ruby-mode package for all archtectures.

* Tue Mar  4 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.114-1
- Security fix for CVE-2008-1145.
- Improve a spec file. (#226381)
  - Correct License tag.
  - Fix a timestamp issue.
  - Own a arch-specific directory.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.8.6.111-9
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-8
- Rebuild for gcc-4.3.

* Tue Jan 15 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-7
- Revert the change of libruby-static.a. (#428384)

* Fri Jan 11 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-6
- Fix an unnecessary replacement for shebang. (#426835)

* Fri Jan  4 2008 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-5
- Rebuild.

* Fri Dec 28 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-4
- Clean up again.

* Fri Dec 21 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-3
- Clean up the spec file.
- Remove ruby-man-1.4.6 stuff. this is entirely the out-dated document.
  this could be replaced by ri.
- Disable the static library building.

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.8.6.111-2
 - Rebuild for openssl bump

* Wed Oct 31 2007 Akira TAGOH <tagoh@redhat.com>
- Fix the dead link.

* Mon Oct 29 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.111-1
- New upstream release.
- ruby-1.8.6.111-CVE-2007-5162.patch: Update a bit with backporting the changes
   at trunk to enable the fix without any modifications on the users' scripts.
   Note that Net::HTTP#enable_post_connection_check isn't available anymore.
   If you want to disable this post-check, you should give OpenSSL::SSL::VERIFY_NONE
   to Net::HTTP#verify_mode= instead of.

* Mon Oct 15 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.110-2
- Enable pthread support for ppc too. (#201452)
- Fix unexpected dependencies appears in ruby-libs. (#253325)

* Wed Oct 10 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.110-1
- New upstream release.
  - ruby-r12567.patch: removed.
- ruby-1.8.6-CVE-2007-5162.patch: security fix for Net::HTTP that is
  insufficient verification of SSL certificate.

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.36-4
- Rebuild

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com>
- Update License tag.

* Mon Jun 25 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.36-3
- ruby-r12567.patch: backport patch from upstream svn to get rid of
  the unnecessary declarations. (#245446)

* Wed Jun 20 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6.36-2
- New upstream release.
  - Fix Etc::getgrgid to get the correct gid as requested. (#236647)

* Wed Mar 28 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6-2
- Fix search path breakage. (#234029)

* Thu Mar 15 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.6-1
- New upstream release.
- clean up a spec file.

* Tue Feb 13 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.5.12-2
- Rebuild

* Mon Feb  5 2007 Akira TAGOH <tagoh@redhat.com> - 1.8.5.12-1
- New upstream release.

* Mon Dec 11 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5.2-1
- security fix release.

* Fri Oct 27 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5-4
- security fix release.
- ruby-1.8.5-cgi-CVE-2006-5467.patch: fix a CGI multipart parsing bug that
  causes the denial of service. (#212396)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.8.5-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5-2
- fixed rbconfig.rb to refer to DESTDIR for sitearchdir. (#207311)

* Mon Aug 28 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.5-1
- New upstream release.
- removed the unnecessary patches:
  - ruby-1.8.4-no-eaccess.patch
  - ruby-1.8.4-64bit-pack.patch
  - ruby-1.8.4-fix-insecure-dir-operation.patch
  - ruby-1.8.4-fix-insecure-regexp-modification.patch
  - ruby-1.8.4-fix-alias-safe-level.patch
- build with --enable-pthread except on ppc.
- ruby-1.8.5-hash-memory-leak.patch: backported from CVS to fix a memory leak
  on Hash. [ruby-talk:211233]

* Mon Aug  7 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-12
- owns sitearchdir. (#201208)

* Thu Jul 20 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-11
- security fixes [CVE-2006-3694]
  - ruby-1.8.4-fix-insecure-dir-operation.patch:
  - ruby-1.8.4-fix-insecure-regexp-modification.patch: fixed the insecure
    operations in the certain safe-level restrictions. (#199538)
  - ruby-1.8.4-fix-alias-safe-level.patch: fixed to not bypass the certain
    safe-level restrictions. (#199543)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.8.4-10.fc6.1
- rebuild

* Mon Jun 19 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-10
- fixed the wrong file list again. moved tcltk library into ruby-tcltk.
  (#195872)

* Thu Jun  8 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-8
- ruby-deprecated-sitelib-search-path.patch: correct the order of search path.

* Wed Jun  7 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-7
- exclude ppc64 to make ruby-mode package. right now emacs.ppc64 isn't provided
  and buildsys became much stricter.
- ruby-deprecated-sitelib-search-path.patch: applied to add more search path
  for backward compatiblity.
- added byacc to BuildReq. (#194161)

* Wed May 17 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-6
- ruby-deprecated-search-path.patch: added the deprecated installation paths
  to the search path for the backward compatibility.
- added a Provides: ruby(abi) to ruby-libs.
- ruby-1.8.4-64bit-pack.patch: backport patch from upstream to fix unpack("l")
  not working on 64bit arch and integer overflow on template "w". (#189350)
- updated License tag to be more comfortable, and with a pointer to get more
  details, like Python package does. (#179933)
- clean up.

* Wed Apr 19 2006 Akira TAGOH <tagoh@redhat.com>
- ruby-rubyprefix.patch: moved all arch-independent modules under /usr/lib/ruby
  and keep arch-dependent modules under /usr/lib64/ruby for 64bit archs.
  so 'rubylibdir', 'sitelibdir' and 'sitedir' in Config::CONFIG points to
  the kind of /usr/lib/ruby now. (#184199)

* Mon Apr 17 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-4
- correct sitelibdir. (#184198)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.8.4-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.8.4-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-3
- ruby-1.8.4-no-eaccess.patch: backported from ruby CVS to avoid conflict
  between newer glibc. (#179835)

* Wed Jan  4 2006 Akira TAGOH <tagoh@redhat.com> - 1.8.4-2
- ruby-tcltk-multilib.patch: fixed a typo.

* Tue Dec 27 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-1
- New upstream release.
  - fixed a missing return statement. (#140833)
  - fixed an use of uninitialized variable. (#144890)

* Fri Dec 16 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.4.preview2
- updates to 1.8.4-preview2.
- renamed the packages to ruby-* (#175765)
  - irb  -> ruby-irb
  - rdoc -> ruby-rdoc
  - ri   -> ruby-ri
- added tcl-devel and tk-devel into BuildRequires.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.3.preview1
- rebuilt against the latest openssl.

* Tue Nov  1 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.2.preview1
- build-deps libX11-devel instead of xorg-x11-devel.

* Mon Oct 31 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.4-0.1.preview1
- New upstream release.
- ruby-1.8.2-strscan-memset.patch: removed because it's no longer needed.

* Tue Oct  4 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-4
- moved the documents from ruby-libs to ruby-docs, which contains the arch
  specific thing and to be multilib support. (#168826)

* Mon Oct  3 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-3
- fixed the wrong file list. the external library for tcl/tk was included
  in ruby-libs unexpectedly.

* Mon Sep 26 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-2
- ruby-multilib.patch: added another chunk for multilib. (#169127)

* Wed Sep 21 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.3-1
- New upstream release.
- Build-Requires xorg-x11-devel instead of XFree86-devel.
- ruby-multilib.patch: applied for only 64-bit archs.
- ruby-1.8.2-xmlrpc-CAN-2005-1992.patch: removed. it has already been in upstream.

* Tue Jun 21 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-9
- ruby-1.8.2-xmlrpc-CAN-2005-1992.patch: fixed the arbitrary command execution
  on XMLRPC server. (#161096)

* Thu Jun 16 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-8
- ruby-1.8.2-tcltk-multilib.patch: applied to get tcltklib.so built. (#160194)

* Thu Apr  7 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-7
- ruby-1.8.2-deadcode.patch: removed the dead code from the source. (#146108)
- make sure that all documentation files in ruby-docs are the world-
  readable. (#147279)

* Tue Mar 22 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-6
- ruby-1.8.2-strscan-memset.patch: fixed an wrong usage of memset(3).

* Tue Mar 15 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-5
- rebuilt

* Tue Jan 25 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-4
- fixed the wrong generation of file manifest. (#146055)
- spec file clean up.

* Mon Jan 24 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-3
- separated out to rdoc package.
- make the dependency of irb for rdoc. (#144708)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> - 1.8.2-2
- Rebuilt for new readline.

* Wed Jan  5 2005 Akira TAGOH <tagoh@redhat.com> - 1.8.2-1
- New upstream release.
- ruby-1.8.1-ia64-stack-limit.patch: removed - it's no longer needed.
- ruby-1.8.1-cgi_session_perms.patch: likewise.
- ruby-1.8.1-cgi-dos.patch: likewise.
- generated Ruby interactive documentation - senarated package.
  it's now provided as ri package. (#141806)

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 1.8.1-10
- rebuild against db-4.3.21.

* Wed Nov 10 2004 Akira TAGOH <tagoh@redhat.com> - 1.8.1-9
- ruby-1.8.1-cgi-dos.patch: security fix [CAN-2004-0983]
- ruby-1.8.1-cgi_session_perms.patch: security fix [CAN-2004-0755]

* Fri Oct 29 2004 Akira TAGOH <tagoh@redhat.com> - 1.8.1-8
- added openssl-devel and db4-devel into BuildRequires (#137479)

* Wed Oct  6 2004 Akira TAGOH <tagoh@redhat.com> - 1.8.1-7
- require emacs-common instead of emacs.

* Wed Jun 23 2004 Akira TAGOH <tagoh@redhat.com> 1.8.1-4
- updated the documentation.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 04 2004 Akira TAGOH <tagoh@redhat.com> 1.8.1-1
- New upstream release.
- don't use any optimization for ia64 to avoid the build failure.
- ruby-1.8.1-ia64-stack-limit.patch: applied to fix SystemStackError when the optimization is disabled.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 1.8.0-3
- rebuild against db-4.2.52.

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 1.8.0-2
- rebuild against db-4.2.42.

* Tue Aug  5 2003 Akira TAGOH <tagoh@redhat.com> 1.8.0-1
- New upstream release.

* Thu Jul 24 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-9.1
- rebuilt

* Thu Jul 24 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-9
- ruby-1.6.8-castnode.patch: handling the nodes with correct cast.
  use this patch now instead of ruby-1.6.8-fix-x86_64.patch.

* Fri Jul 04 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-8
- rebuilt

* Fri Jul 04 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-7
- fix the gcc warnings. (#82192)
- ruby-1.6.8-fix-x86_64.patch: correct a patch.
  NOTE: DON'T USE THIS PATCH FOR BIG ENDIAN ARCHITECTURE.
- ruby-1.6.7-long2int.patch: removed.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  7 2003 Jens Petersen <petersen@redhat.com> - 1.6.8-5
- rebuild against ucs4 tcltk

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-3
- ruby-1.6.8-multilib.patch: applied to fix the search path issue on x86_64

* Tue Jan 21 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-2
- ruby-1.6.8-require.patch: applied to fix the search bug in require.
- don't apply long2int patch to s390 and s390x. it doesn't work.

* Wed Jan 15 2003 Akira TAGOH <tagoh@redhat.com> 1.6.8-1
- New upstream release.
- removed some patches. it's no longer needed.
  - ruby-1.6.7-100.patch
  - ruby-1.6.7-101.patch
  - ruby-1.6.7-102.patch
  - ruby-1.6.7-103.patch
  - 801_extmk.rb-shellwords.patch
  - 801_mkmf.rb-shellwords.patch
  - 804_parse.y-new-bison.patch
  - 805_uri-bugfix.patch
  - ruby-1.6.6-900_XXX_strtod.patch
  - ruby-1.6.7-sux0rs.patch
  - ruby-1.6.7-libobj.patch

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 1.6.7-14
- rebuild to update tcltk deps

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 1.6.7-13
- Remove ExcludeArch: x86_64
- Fix x86_64 ruby with long2int.patch (ruby was assuming that sizeof(long)
  == sizeof(int). The patch does not fix the source of the problem, just
  makes it a non-issue.)
- _smp_mflags

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 1.6.7-12
- rebuild to fix broken tcltk deps

* Tue Oct 22 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-11
- use %%configure macro instead of configure script.
- use the latest config.{sub,guess}.
- get archname from rbconfig.rb for %%dir
- applied some patches from Debian:
  - 801_extmk.rb-shellwords.patch: use Shellwords
  - 801_mkmf.rb-shellwords.patch: mkmf.rb creates bad Makefile. the Makefile
    links libruby.a to the target.
  - 803_sample-fix-shbang.patch: all sample codes should be
    s|/usr/local/bin|/usr/bin|g
  - 804_parse.y-new-bison.patch: fix syntax warning.
  - 805_uri-bugfix.patch: uri.rb could not handle correctly broken mailto-uri.
- add ExcludeArch x86_64 temporarily to fix Bug#74581. Right now ruby can't be
  built on x86_64.

* Tue Aug 27 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-10
- moved sitedir to /usr/lib/ruby/site_ruby again according as our perl and
  python.
- ruby-1.6.7-resolv1.patch, ruby-1.6.7-resolv2.patch: applied to fix 'Too many
  open files - "/etc/resolv.conf"' issue. (Bug#64830)

* Thu Jul 18 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-9
- add the owned directory.

* Fri Jul 12 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-8
- fix typo.

* Thu Jul 04 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-7
- removed the ruby-mode-xemacs because it's merged to the xemacs sumo.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-5
- fix the stripped binary.
- use the appropriate macros.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-3
- ruby-1.6.7-libobj.patch: applied to fix autoconf2.53 error.

* Mon Mar 18 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-2
- ruby-man-1.4.6-jp.tar.bz2: removed.
- ruby-refm-rdp-1.4.7-ja-html.tar.bz2: uses it instead of.
- ruby-1.6.7-500-marshal-proc.patch, ruby-1.6.7-501-class-var.patch:
  removed.
- ruby-1.6.7-100.patch: applied a bug fix patch.
  (ruby-dev#16274: patch for 'wm state')
  (PR#206ja: SEGV handle EXIT)
- ruby-1.6.7-101.patch: applied a bug fix patch.
  (ruby-list#34313: singleton should not be Marshal.dump'ed)
  (ruby-dev#16411: block local var)
- ruby-1.6.7-102.patch: applied a bug fix patch.
  (handling multibyte chars is partially broken)
- ruby-1.6.7-103.patch: applied a bug fix patch.
  (ruby-dev#16462: preserve reference for GC, but link should be cut)

* Fri Mar  8 2002 Akira TAGOH <tagoh@redhat.com> 1.6.7-1
- New upstream release.
- ruby-1.6.6-100.patch, ruby-1.6.6-501-ruby-mode.patch:
  removed. these patches no longer should be needed.
- ruby-1.6.7-500-marshal-proc.patch: applied a fix patch.
  (ruby-dev#16178: Marshal::dump should call Proc#call.)
- ruby-1.6.7-501-class-var.patch: applied a fix patch.
  (ruby-talk#35157: class vars broken in 1.6.7)

* Wed Feb 27 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-5
- Disable alpha because nothing is xemacs for alpha now.

* Tue Feb  5 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-3
- Fixed the duplicate files.

* Tue Feb  5 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-2
- Fixed the missing %%defattr

* Fri Feb  1 2002 Akira TAGOH <tagoh@redhat.com> 1.6.6-1
- New upstream release.
- Applied bug fix patches:
  - ruby-1.6.6-501-ruby-mode.patch: ruby-talk#30479: disables font-lock
    coloring.
  - ruby-1.6.6-100.patch: ruby-talk#30203: Ruby 1.6.6 bug and fix
                          ruby-list#33047: regex bug
                          PR#230: problem with -d in 1.6.6
- Added ruby-mode and ruby-mode-xemacs packages.
- Ruby works fine for ia64. so re-enable to build with ia64.
  (probably it should be worked for alpha)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.6.4-2
- Remove Japanese description and summaries; they belong in specspo and
  break rpm
- Clean up specfile
- Mark language specific files (README.jp) as such
- bzip2 sources
- rename the libruby package to ruby-libs for consistency
- Exclude ia64 (doesn't build - the code doesn't seem to be 64-bit clean
  [has been excluded on alpha forever])

* Tue Jul 17 2001 Akira TAGOH <tagoh@redhat.com> 1.6.4-1
- rebuild for Red Hat 7.2

* Mon Jun 04 2001 akira yamada <akira@vinelinux.org>
- upgrade to nwe upstream version 1.6.4.

* Mon Apr 02 2001 akira yamada <akira@vinelinux.org>
- applied patch:
  - fixed method cache bug. etc. (Patch103, Patch104)

* Tue Mar 27 2001 akira yamada <akira@vinelinux.org>
- applied patch:
  - fixed marshal for bignum bug.
  - fixed scope of constant variables bug.

* Tue Mar 20 2001 akira yamada <akira@vinelinux.org>
- upgraded to new upstream version 1.6.3.

* Fri Feb 09 2001 akira yamada <akira@vinelinux.org>
- fixed bad group for libruby.
- Applied patch: upgraded to cvs version (2001-02-08):
  fixed minor bugs.

* Thu Jan 18 2001 akira yamada <akira@vinelinux.org>
- Applied patch: upgraded to cvs version (2001-01-15):
  fixed minor bugs(e.g. ruby makes extention librares too large...).

* Wed Jan 10 2001 akira yamada <akira@vinelinux.org>
- Applied patch: upgraded to cvs version (2001-01-09):
  fixed minor bugs.

* Sat Dec 30 2000 akira yamada <akira@vinelinux.org>
- Applied bug fix patch.

* Mon Dec 25 2000 akira yamada <akira@vinelinux.org>
- Updated to new upstream version 1.6.2.

* Fri Dec 22 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000122019.patch, added ruby_cvs.2000122215.patch
  (upgraded ruby to latest cvs version, 1.6.2-preview4).

* Wed Dec 20 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000121413.patch, added ruby_cvs.2000122019.patch
  (upgraded ruby to latest cvs version).
- new package: libruby

* Thu Dec 14 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000101901.patch, added ruby_cvs.2000121413.patch
  (upgraded ruby to latest cvs version).
- Removed ruby-dev.11262.patch, ruby-dev.11265.patch,
  and ruby-dev.11268.patch (included into above patch).

* Sun Nov 12 2000 MACHINO, Satoshi <machino@vinelinux.org> 1.6.1-0vl9
- build on gcc-2.95.3

* Thu Oct 19 2000 akira yamada <akira@vinelinux.org>
- Added ruby-dev.11268.patch.

* Thu Oct 19 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000101117.patch and added ruby_cvs.2000101901.patch
  (upgraded ruby to latest cvs version).
- Added ruby-dev.11262.patch.
- Added ruby-dev.11265.patch.

* Wed Oct 11 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000100313.patch and added ruby_cvs.2000101117.patch
  (upgraded ruby to latest cvs version).

* Mon Oct 09 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000100313.patch and added ruby_cvs.2000100313.patch
  (upgraded ruby to latest cvs version).

* Tue Oct 03 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000100218.patch and added ruby_cvs.2000100313.patch
  (upgraded ruby to latest cvs version).

* Mon Oct 02 2000 akira yamada <akira@vinelinux.org>
- Removed ruby_cvs.2000092718.patch and added ruby_cvs.2000100218.patch
  (upgraded ruby to latest cvs version).

* Wed Sep 27 2000 akira yamada <akira@vinelinux.org>
- Updated to upstream version 1.6.1.
- Removed ruby_cvs.2000082901.patch and added ruby_cvs.2000092718.patch
  (upgraded ruby to latest cvs version).

* Tue Aug 29 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.6.
- removed ruby-dev.10123.patch(included into ruby-1.4.6).
- Added ruby_cvs.2000082901.patch(upgraded ruby to latest cvs version).

* Tue Jun 27 2000 akira yamada <akira@redhat.com>
- Updated manuals to version 1.4.5.

* Sun Jun 25 2000 akira yamada <akira@redhat.com>
- Added ruby-dev.10123.patch.

* Sat Jun 24 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.5.
- Removed ruby_cvs.2000062401.patch(included into ruby-1.4.5).

* Thu Jun 22 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.4(06/22/2000 CVS).
- Removed ruby-dev.10054.patch(included into ruby_cvs.patch).

* Thu Jun 22 2000 akira yamada <akira@redhat.com>
- Renamed to ruby_cvs20000620.patch from ruby_cvs.patch.

* Tue Jun 20 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.4(06/20/2000 CVS).
- Removed ruby-list.23190.patch(included into ruby_cvs.patch).
- Added ruby-dev.10054.patch.

* Thu Jun 15 2000 akira yamada <akira@redhat.com>
- Updated to version 1.4.4(06/12/2000 CVS).
- Added manuals and FAQs.
- Split into ruby, ruby-devel, ruby-tcltk, ruby-docs, irb.

* Tue Jun 13 2000 Mitsuo Hamada <mhamada@redhat.com>
- Updated to version 1.4.4

* Wed Dec 08 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.3

* Mon Sep 20 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.2 (Sep 18)

* Fri Sep 17 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.2

* Tue Aug 17 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.4.0

* Fri Jul 23 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- 2nd release
- Updated to version 1.2.6(15 Jul 1999)
- striped %%{prefix}/bin/ruby

* Mon Jun 28 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.2.6(21 Jun 1999)

* Wed Apr 14 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.2.5

* Fri Apr 09 1999 Atsushi Yamagata <yamagata@plathome.co.jp>
- Updated to version 1.2.4

* Fri Dec 25 1998 Toru Hoshina <hoshina@best.com>
- Version up to 1.2 stable.

* Fri Nov 27 1998 Toru Hoshina <hoshina@best.com>
- Version up to 1.1c9.

* Thu Nov 19 1998 Toru Hoshina <hoshina@best.com>
- Version up to 1.1c8, however it appear short life :-P

* Fri Nov 13 1998 Toru Hoshina <hoshina@best.com>
- Version up.

* Tue Sep 22 1998 Toru Hoshina <hoshina@best.com>
- To make a libruby.so.

* Mon Sep 21 1998 Toru Hoshina <hoshina@best.com>
- Modified SPEC in order to install libruby.a so that it should be used by
  another ruby entention.
- 2nd release.

* Mon Mar 9 1998 Shoichi OZAWA <shoch@jsdi.or.jp>
- Added a powerPC arch part. Thanks, MURATA Nobuhiro <nob@makioka.y-min.or.jp>
