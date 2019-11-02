Name:           arduino-builder
Version:        1.3.25
Release:        1%{?dist}
Summary:        A command line tool for compiling Arduino sketches
License:        GPLv2+
URL:            http://www.arduino.cc
Source0:        https://github.com/arduino/arduino-builder/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1:         fix-paths-to-ctags-avrdude.patch
#Patch2:         make-tools-flag-optional.patch

Requires:       arduino-ctags

ExclusiveArch:  %{go_arches}

BuildRequires:  gcc
BuildRequires:  golang >= 1.4.3
BuildRequires:  git

BuildRequires:  golang(github.com/go-errors/errors)

# Needed for unit tests
BuildRequires:  golang(github.com/stretchr/testify)
# These are not available, check will not be enabled
#BuildRequires:  golang(github.com/jstemmer/go-junit-report)
#BuildRequires:  golang(golang.org/x/codereview/patch)
#BuildRequires:  golang(golang.org/x/tools/cmd/vet)


%description
This tool is able to parse Arduino Hardware specifications, properly run
gcc and produce compiled sketches.
An Arduino sketch differs from a standard C program in that it misses a
main (provided by the Arduino core), function prototypes are not mandatory,
and libraries inclusion is automagic (you just have to #include them).
This tool generates function prototypes and gathers library paths,
providing gcc with all the needed -I params.

%prep
%setup -q
%patch1 -p1
# %%patch2 -p1

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build
ln -s $(pwd)/src ./_build/

export GOPATH=$(pwd)/_build:%{gopath}

# Fix missing build-id
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
pushd src/arduino.cc/arduino-builder
gobuild
popd

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 ./src/arduino.cc/arduino-builder/arduino-builder %{buildroot}%{_bindir}/arduino-builder

install -d %{buildroot}%{_datadir}/arduino/hardware
install -p src/arduino.cc/builder/hardware/*.txt %{buildroot}%{_datadir}/arduino/hardware


# Check needs golang.org/x/ libraries that are not available
#%%check
#export GOPATH=$(pwd)/_build:%%{gopath}
#go test -v ./src/arduino.cc/builder/test/...


%files
%license LICENSE.txt
%doc CONTRIBUTING.md README.md
%{_bindir}/arduino-builder
%{_datadir}/arduino/hardware

%changelog
* Tue Aug 15 2017 Tom Callaway <spot@fedoraproject.org> - 1.3.25-1
- update to 1.3.25 for Arduino IDE 1.8.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Gianluca Sforna <giallu@gmail.com> 1.3.9-1
- update to 1.3.9 for Arduino IDE 1.6.7
- rebase patch

* Fri Jul 21 2017 Gianluca Sforna <giallu@gmail.com> 1.0.5-6
- revert binaries move, /usr/bin looks like the correct location

* Fri Apr  7 2017 Kir Kolyshkin <kolyshkin@gmail.com> 1.0.5-5
- require and use arduino-ctags instead of usual ctags
- use /usr/bin as path for ctags and avrdude
- make -tools CLI option non-required (i.e. optional)

* Sun Feb 12 2017 Gianluca Sforna <giallu@gmail.com> 1.0.5-4
- fix binary location

* Wed Feb  8 2017 Gianluca Sforna <giallu@gmail.com> 1.0.5-3
- package missing files

* Fri Nov  4 2016 Gianluca Sforna <giallu@gmail.com> 1.0.5-2
- use proper dependencies

* Fri Nov  4 2016 Gianluca Sforna <giallu@gmail.com> 1.0.5-1
- initial package
