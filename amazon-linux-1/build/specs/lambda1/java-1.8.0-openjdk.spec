%define _buildid .48

# The -g flag says to use strip -g instead of full strip on DSOs or EXEs.
# This fixes detailed NMT and other tools which need minimal debug info.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1520879
%global _find_debuginfo_opts -g

# Fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349.
# See also https://bugzilla.redhat.com/show_bug.cgi?id=1590796
# as to why some libraries *cannot* be excluded. In particular,
# these are:
# libjsig.so, libjava.so, libjawt.so, libjvm.so and libverify.so
%global _privatelibs libatk-wrapper[.]so.*|libattach[.]so.*|libawt_headless[.]so.*|libawt[.]so.*|libawt_xawt[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libhprof[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas_unix[.]so.*|libjava_crw_demo[.]so.*|libjavajpeg[.]so.*|libjdwp[.]so.*|libjli[.]so.*|libjsdt[.]so.*|libjsoundalsa[.]so.*|libjsound[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libnpt[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsplashscreen[.]so.*|libsunec[.]so.*|libunpack[.]so.*|libzip[.]so.*|lib[.]so\\(SUNWprivate_.*

%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

# New Version-String scheme-style defines
%global majorver 8

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

# Standard JPackage naming and versioning defines.
%global origin          openjdk
%global origin_nice     OpenJDK
%global top_level_dir_name   %{origin}
# note, following three variables are sedded from update_sources if used correctly. Hardcode them rather there.
%global shenandoah_project	aarch64-port
%global shenandoah_repo		jdk8u-shenandoah
%global shenandoah_revision    	aarch64-shenandoah-jdk8u232-b09
# Define old aarch64/jdk8u tree variables for compatibility
%global project         %{shenandoah_project}
%global repo            %{shenandoah_repo}
%global revision        %{shenandoah_revision}

# e.g. aarch64-shenandoah-jdk8u212-b04-shenandoah-merge-2019-04-30 -> aarch64-shenandoah-jdk8u212-b04
%global version_tag     %(VERSION=%{revision}; echo ${VERSION%%-shenandoah-merge*})
# eg # jdk8u60-b27 -> jdk8u60 or # aarch64-jdk8u60-b27 -> aarch64-jdk8u60  (dont forget spec escape % by %%)
%global whole_update    %(VERSION=%{version_tag}; echo ${VERSION%%-*})
# eg  jdk8u60 -> 60 or aarch64-jdk8u60 -> 60
%global updatever       %(VERSION=%{whole_update}; echo ${VERSION##*u})
# eg jdk8u60-b27 -> b27
%global buildver        %(VERSION=%{version_tag}; echo ${VERSION##*-})
%global rpmrelease      0
# Define milestone (EA for pre-releases, GA ("fcs") for releases)
# Release will be (where N is usually a number starting at 1):
# - 0.N%%{?extraver}%%{?dist} for EA releases,
# - N%%{?extraver}{?dist} for GA releases
%global is_ga           1
%if %{is_ga}
%global milestone          fcs
%global milestone_version  %{nil}
%global extraver %{nil}
%global eaprefix %{nil}
%else
%global milestone          ea
%global milestone_version  "-ea"
%global extraver .%{milestone}
%global eaprefix 0.
%endif
# The priority must be < 17000 on amzn to keep java-1.7.0-openjdk the default
%global priority        18000

%global javaver         1.%{majorver}.0

# parametrized macros are order-sensitive
%global compatiblename  %{name}
%global fullversion     %{compatiblename}-%{version}-%{release}
# images stub
%global jdkimage       j2sdk-image
# output dir stub
%global buildoutputdir %{top_level_dir_name}/build/jdk8.build
#main id and dir of this jdk
%global uniquesuffix        %{fullversion}.%{_arch}

# Standard JPackage directories and symbolic links.
%global sdklnk_noarch java-%{javaver}-%{origin}
%global jrelnk_noarch jre-%{javaver}-%{origin}

%global sdkdir        %{uniquesuffix}
%global sdklnk        %{sdklnk_noarch}.%{_arch}
%global jrelnk        %{jrelnk_noarch}.%{_arch}

%global jredir        %{sdkdir}/jre
%global sdkbindir     %{_jvmdir}/%{sdklnk}/bin
%global jrebindir     %{_jvmdir}/%{jrelnk}/bin
%global jvmjardir     %{_jvmjardir}/%{uniquesuffix}

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/

# Prevent brp-java-repack-jars from being run
%global __jar_repack 0

# Java 8 uses bundled lcms libraries. We don't want to provide
# any of those libraries, as they could be chosen to satisfy
# requirements in other packages.
%global __provides_exclude ^liblcms\\.so

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{updatever}.%{buildver}
Release: %{?eaprefix}%{rpmrelease}%{?extraver}%{?_buildid}%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons
# and this change was brought into RHEL-4. java-1.5.0-ibm packages
# also included the epoch in their virtual provides. This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0". In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0. So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages. Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".

Epoch:   1
Summary: %{origin_nice} Runtime Environment %{majorver}
Group:   Development/Languages

# HotSpot code is licensed under GPLv2
# JDK library code is licensed under GPLv2 with the Classpath exception
# The Apache license is used in code taken from Apache projects (primarily JAXP & JAXWS)
# DOM levels 2 & 3 and the XML digital signature schemas are licensed under the W3C Software License
# The JSR166 concurrency code is in the public domain
# The BSD and MIT licenses are used for a number of third-party libraries (see THIRD_PARTY_README)
# The OpenJDK source tree includes the JPEG library (IJG), zlib & libpng (zlib), giflib and LCMS (MIT)
# The test code includes copies of NSS under the Mozilla Public License v2.0
# The PCSClite headers are under a BSD with advertising license
# The elliptic curve cryptography (ECC) source code is licensed under the LGPLv2.1 or any later version
License:  ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib
URL:      http://openjdk.java.net/

# Sources were downloaded using:
# yumdownloader java-1.8.0-openjdk-devel.x86_64
# And then queried using:
# rpm -qp --qf 'Name: %{name}\n[Requires: %{requires}\n][Conflicts: %{conflicts}\n][Obsoletes: %{obsoletes}\n][Provides: %{provides}\n]' *.rpm | uniq
Source0: %{name}-devel-%{version}-%{?eaprefix}%{rpmrelease}%{?extraver}%{?_buildid}.amzn1.%{_arch}.rpm

%description
The %{origin_nice} runtime environment.

%package devel
Summary: %{origin_nice} Development Environment %{majorver}
Group:   Development/Tools

BuildRequires: rpm
BuildRequires: cpio
BuildRequires: javapackages-tools

Requires:         %{name}%{?_isa} >= %{epoch}:%{javaver}
Requires(post):   /usr/sbin/alternatives

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java-sdk-%{javaver} = %{epoch}:%{version}
Provides: java-sdk-%{origin} = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel = %{epoch}:%{version}
Provides: java-%{javaver}-%{origin}-devel = %{epoch}:%{version}
Provides: java-devel-%{origin} = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{javaver}

Prefix: %{_prefix}

%description devel
The %{origin_nice} development tools %{majorver}.

%install
rm -rf %{buildroot} && mkdir -p %{buildroot}

pushd %{buildroot}
  rpm2cpio %{SOURCE0} | cpio -idm
popd

mv %{buildroot}/usr %{buildroot}%{_prefix}

mv %{buildroot}%{_prefix}/share/doc/*/* ./
for file in ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README; do chmod 644 $file; done

for dir in %{_jvmdir} %{_jvmjardir}; do
  pushd %{buildroot}$dir
    mv %{compatiblename}-%{version}-* %{sdkdir}
  popd
done

mkdir -p %{buildroot}%{_jvmdir}/%{jredir}

# Install extension symlinks.
pushd $RPM_BUILD_ROOT%{jvmjardir}
  RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
  ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
  ln -sf $RELATIVE/jce.jar jce-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
  ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
  ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
  ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
  ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
  for jar in *-%{version}.jar
  do
    if [ x%{version} != x%{javaver} ]
    then
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
    fi
    ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
  done
popd

pushd %{buildroot}%{_jvmdir}
  ln -sf %{jredir} %{jrelnk}
  ln -sf %{sdkdir} %{sdklnk}
  ln -sf %{sdkdir} java
  ln -sf %{jrelnk} %{jrelnk_noarch}
  ln -sf %{jrelnk} jre
  for X in %{origin} %{javaver}; do
    ln -sf %{jrelnk} jre-"$X"
    ln -sf %{sdklnk} java-"$X"
  done
popd

pushd %{buildroot}%{_jvmjardir}
  ln -sf %{sdkdir} %{jrelnk}
  ln -sf %{sdkdir} %{sdklnk}
  ln -sf %{sdkdir} java
  ln -sf %{jrelnk} %{jrelnk_noarch}
  ln -sf %{jrelnk} jre
  for X in %{origin} %{javaver}; do
    ln -sf %{jrelnk} jre-"$X"
    ln -sf %{sdklnk} java-"$X"
  done
popd

mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
  RELATIVE=$(%{abs2rel} %{jrebindir} %{_bindir})
  for file in java jjs keytool orbd pack200 rmid rmiregistry servertool tnameserv policytool unpack200; do
    ln -sf $RELATIVE/$file $file
  done

  RELATIVE=$(%{abs2rel} %{sdkbindir} %{_bindir})
  for file in $(ls %{buildroot}%{sdkbindir}); do
    ln -sf $RELATIVE/$file $file
  done
popd

%post devel
JVMDIR=$(echo %{_jvmdir} | sed "s_^%{_prefix}_${RPM_INSTALL_PREFIX}_")
cp -as /usr/lib/jvm/%{jrelnk}/* $JVMDIR/%{jredir}/
# XXX: unsure why this needs to be physically present, but it does...
cp --remove-destination /usr/lib/jvm/%{jrelnk}/lib/amd64/server/libjvm.so $JVMDIR/%{jredir}/lib/amd64/server/

%files devel
%defattr(-,root,root,-)
%license ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%{_jvmdir}/%{sdklnk}
%{_jvmdir}/%{sdklnk_noarch}
%{_jvmdir}/java
%{_jvmdir}/java-%{origin}
%{_jvmdir}/java-%{javaver}
%{_jvmjardir}/%{sdkdir}
%{_jvmjardir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk_noarch}
%{_jvmjardir}/java
%{_jvmjardir}/java-%{origin}
%{_jvmjardir}/java-%{javaver}
%{_bindir}/appletviewer
%{_bindir}/clhsdb
%{_bindir}/extcheck
%{_bindir}/hsdb
%{_bindir}/idlj
%{_bindir}/jar
%{_bindir}/jarsigner
%{_bindir}/java-rmi.cgi
%{_bindir}/javac
%{_bindir}/javadoc
%{_bindir}/javah
%{_bindir}/javap
%{_bindir}/jcmd
%{_bindir}/jconsole
%{_bindir}/jdb
%{_bindir}/jdeps
%{_bindir}/jhat
%{_bindir}/jinfo
%{_bindir}/jmap
%{_bindir}/jps
%{_bindir}/jrunscript
%{_bindir}/jsadebugd
%{_bindir}/jstack
%{_bindir}/jstat
%{_bindir}/jstatd
%{_bindir}/native2ascii
%{_bindir}/rmic
%{_bindir}/schemagen
%{_bindir}/serialver
%{_bindir}/wsgen
%{_bindir}/wsimport
%{_bindir}/xjc
%dir %{_jvmdir}/%{jredir}
%{_jvmdir}/%{jrelnk}
%{_jvmdir}/%{jrelnk_noarch}
%{_jvmdir}/jre
%{_jvmdir}/jre-%{origin}
%{_jvmdir}/jre-%{javaver}
%{_jvmjardir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk_noarch}
%{_jvmjardir}/jre
%{_jvmjardir}/jre-%{origin}
%{_jvmjardir}/jre-%{javaver}
%{_bindir}/java
%{_bindir}/jjs
%{_bindir}/keytool
%{_bindir}/orbd
%{_bindir}/pack200
%{_bindir}/rmid
%{_bindir}/rmiregistry
%{_bindir}/servertool
%{_bindir}/tnameserv
%{_bindir}/policytool
%{_bindir}/unpack200

%exclude %{_prefix}/share
%exclude %{_jvmdir}/%{sdkdir}/tapset

%changelog
* Fri Jan 10 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Thu Oct 17 2019 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.232.b09-0.el7_7

* Fri Oct 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b09-0
- Update to aarch64-shenandoah-jdk8u232-b09.
- Switch to GA mode for final release.
- Remove PR1834/RH1022017 which is now handled by JDK-8228825 upstream.
- Resolves: rhbz#1753423

* Tue Oct 01 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b08-0.0.ea
- Update to aarch64-shenandoah-jdk8u232-b08.
- Resolves: rhbz#1753423

* Tue Sep 17 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b05-0.1.ea
- Update to aarch64-shenandoah-jdk8u232-b05-shenandoah-merge-2019-09-09.
- Update version logic to handle -shenandoah* tag suffix.
- Resolves: rhbz#1753423

* Thu Sep 05 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b05-0.0.ea
- Update to aarch64-shenandoah-jdk8u232-b05.
- Drop upstreamed patch JDK-8141570/PR3548.
- Adjust context of JDK-8143245/PR3548 to apply against upstream JDK-8141570.
- Resolves: rhbz#1753423

* Wed Sep 4 2019 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.222.b10-1.el7_7

* Wed Aug 21 2019 kaos-source-imports <nobody@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.222.b03-1.el7

* Wed Aug 21 2019 Paul Ezvan <paulezva@amazon.com>
- Revert priority to 1800 to keep java-1.7.0-openjdk the default.

* Thu Aug 1 2019 kaos-source-imports <nobody@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.222.b10-0.el7_6

* Tue Jul 30 2019 Chuanhao jin <haroldji@amazon.com>
- Fix spec file build and install error after merge

* Fri Jul 26 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b01-0.0.ea
- Update to aarch64-shenandoah-jdk8u232-b01.
- Switch to EA mode.
- Drop JDK-8210761/RH1632174 as now upstream.
- Resolves: rhbz#1753423

* Thu Jul 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b10-1
- Update to aarch64-shenandoah-jdk8u222-b10.
- Resolves: rhbz#1724452

* Mon Jul 8 2019 kaos-source-imports <nobody@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b09-2
- Use normal_suffix for Javadoc zip filename to copy, as there is is no debug version.
- Resolves: rhbz#1724452

* Mon Jul 8 2019 kaos-source-imports <nobody@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.201.b09-2.el7_6

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b09-2
- Provide Javadoc debug subpackages for now, but populate them from the normal build.
- Resolves: rhbz#1724452

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b09-1
- Update to aarch64-shenandoah-jdk8u222-b09.
- Switch to GA mode for final release.
- Resolves: rhbz#1724452

* Tue Jul 02 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b08-0.1.ea
- Update to aarch64-shenandoah-jdk8u222-b08.
- Adjust PR3083/RH134640 to apply after JDK-8182999
- Resolves: rhbz#1724452

* Tue Jul 02 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.222.b07-0.3.ea
- Include 'ea' designator in Release when appropriate.
- Resolves: rhbz#1724452

* Wed Jun 26 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.222.b07-2
- Don't produce javadoc/javadoc-zip sub packages for the debug variant build.
- Don't perform a bootcycle build for the debug variant build.
- Resolves: rhbz#1724452

* Tue Jun 25 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b07-1
- Update to aarch64-shenandoah-jdk8u222-b07 and Shenandoah merge 2019-06-13.
- Resolves: rhbz#1724452

* Fri Jun 14 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b06-1
- Update to aarch64-shenandoah-jdk8u222-b06.
- Resolves: rhbz#1724452

* Thu Jun 06 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b05-1
- Update to aarch64-shenandoah-jdk8u222-b05.
- Resolves: rhbz#1724452

* Sat May 25 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b04-1
- Update to aarch64-shenandoah-jdk8u222-b04.
- Drop remaining JDK-8210425/RH1632174 patch now AArch64 part is upstream.
- Resolves: rhbz#1705328

* Wed May 22 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b03-1
- Handle milestone as variables so we can alter it easily and set the docs zip filename appropriately.
- Drop unused use_shenandoah_hotspot variable.
- Resolves: rhbz#1705328
- Update to aarch64-shenandoah-jdk8u222-b03.
- Set milestone to "ea" as this is not the final release.
- Drop 8210425 patches applied upstream. Still need to add AArch64 version in aarch64/shenandoah-jdk8u.
- Re-generate JDK-8141570 & JDK-8143245 patches due to 8210425 zeroshark.make changes.

* Mon May 13 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b02-1
- Update to aarch64-shenandoah-jdk8u222-b02.
- Drop 8064786/PR3599 & 8210416/RH1632174 as applied upstream (8064786 silently in 8176100).
- Resolves: rhbz#1705328

* Thu May 02 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b01-1
- Update to aarch64-shenandoah-jdk8u222-b01.
- Refactor PR2888 after inclusion of 8129988 upstream. Now includes PR3575.
- Drop 8171000, 8197546 & PR3634 as applied upstream.
- Adjust 8214206 fix for S390 as BinaryMagnitudeSeq moved to shenandoahNumberSeq.cpp
- Resolves: rhbz#1705328

* Thu Apr 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b04-1
- Update to aarch64-shenandoah-jdk8u212-b04.
- Resolves: rhbz#1693468

* Thu Apr 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b03-1
- Update to aarch64-shenandoah-jdk8u212-b03.
- Resolves: rhbz#1693468

* Wed Apr 10 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b02-2
- Rebase tarball so the AArch64 fix is included upstream
- Resolves: rhbz#1693468

* Wed Apr 10 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b02-1
- Add missing part of JDK-8213419 for AArch64 removing duplicate uabs definitions
- Yet another cast to resolve s390 ambiguity in call to log2_intptr
- Resolves: rhbz#1693468
- Another cast to resolve s390 ambiguity in call to log2_intptr

* Tue Apr 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b02-1
- Add cast to resolve s390 ambiguity in call to log2_intptr
- Resolves: rhbz#1693468
- Update to aarch64-shenandoah-jdk8u212-b02.
- Remove patches included upstream
  - JDK-8197429/PR3546/RH153662{2,3}
  - JDK-8184309/PR3596
  - JDK-8210647/RH1632174
  - JDK-8029661/PR3642/RH1477159
- Re-generate patches
  - JDK-8203030

* Sun Apr 07 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.202.b08-1
- Update to aarch64-shenandoah-jdk8u202-b08.
- Remove patches included upstream
  - JDK-8211387/PR3559
  - JDK-8207057/PR3613
  - JDK-8165852/PR3468
  - JDK-8073139/PR1758/RH1191652
  - JDK-8044235
  - JDK-8172850/RH1640127
  - JDK-8209639/RH1640127
  - JDK-8131048/PR3574/RH1498936
  - JDK-8164920/PR3574/RH1498936
- Re-generate patches
  - JDK-8210647/RH1632174
- Resolves: rhbz#1693468

* Thu Apr 04 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.201.b13-1
- Update to aarch64-shenandoah-jdk8u201-b13.
- Drop JDK-8160748 & JDK-8189170 AArch64 patches now applied upstream.
- Resolves: rhbz#1693468

* Tue Apr 02 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.201.b09-5
- Update patch for RH1566890.
  - Renamed rh1566890_speculative_store_bypass_so_added_more_per_task_speculation_control_CVE_2018_3639 to
    rh1566890-CVE_2018_3639-speculative_store_bypass.patch
  - Added dependent patch,
    rh1566890-CVE_2018_3639-speculative_store_bypass_toggle.patch
- Resolves: rhbz#1693468

* Sat Mar 30 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.201.b09-4
- Drop NSS runtime dependencies and patches to link against it.
- Resolves: rhbz#1656676

* Fri Mar 29 2019 Andrew John Hughes <gnu.andrew@redhat.com> - 1:1.8.0.201.b09-3
- Sync SystemTap & desktop files with upstream IcedTea release using new script
- Resolves: rhbz#1434241

* Fri Mar 29 2019 Jiri Vanek jvanek@redhat.com - 1:1.8.0.201.b09-3
- Change handling of SystemTap tarball, removing Java version
- Resolves: rhbz#1434241

* Tue Mar 5 2019 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.201.b09-0.el7_6

* Thu Feb 28 2019 Jiri Vanek jvanek@redhat.com - 1:1.8.0.201.b09-2
- Replaced pcsc-lite-devel (which is in optional channel) with pcsc-lite-libs.
- added rh1684077-openjdk_should_depend_on_pcsc-lite-libs_instead_of_pcsc-lite-devel.patch to make jdk work with pcsc

* Wed Jan 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.201.b09-1
- Update to aarch64-shenandoah-jdk8u201-b09.
- Resolves: rhbz#1661577

* Wed Jan 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.192.b12-1
- Add port of 8189170 to AArch64 which is missing from upstream 8u version.
- Resolves: rhbz#1661577
- Add 8160748 for AArch64 which is missing from upstream 8u version.
- Update to aarch64-shenandoah-jdk8u192-b12.
- Remove patches included upstream
  - JDK-8031668/PR2842
  - JDK-8148351/PR2842
  - JDK-6260348/PR3066
  - JDK-8061305/PR3335/RH1423421
  - JDK-8188030/PR3459/RH1484079
  - JDK-8205104/PR3539/RH1548475
  - JDK-8185723/PR3553
  - JDK-8186461/PR3557
  - JDK-8201509/PR3579
  - JDK-8075942/PR3602
  - JDK-8203182/PR3603
  - JDK-8206406/PR3610/RH1597825
  - JDK-8206425
  - JDK-8036003
  - JDK-8201495/PR2415
  - JDK-8150954/PR2866/RH1176206
- Re-generate patches (mostly due to upstream build changes)
  - JDK-8073139/PR1758/RH1191652
  - JDK-8143245/PR3548 (due to JDK-8202600)
  - JDK-8197429/PR3546/RH1536622 (due to JDK-8189170)
  - JDK-8199936/PR3533
  - JDK-8199936/PR3591
  - JDK-8207057/PR3613
  - JDK-8210761/RH1632174 (due to JDK-8207402)
  - PR3559 (due to JDK-8185723/JDK-8186461/JDK-8201509)
  - PR3593 (due to JDK-8081202)
  - RH1566890/CVE-2018-3639 (due to JDK-8189170)
  - RH1649664 (due to JDK-8196516)

* Mon Jan 14 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b14-2
- Add 8131048 & 8164920 (PR3574/RH1498936) to provide a CRC32 intrinsic for PPC64.
- Resolves: rhbz#1498936

* Thu Jan 10 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b14-1
- Update to aarch64-shenandoah-jdk8u191-b14.
- Adjust JDK-8073139/PR1758/RH1191652 to apply following 8155627 backport.
- Resolves: rhbz#1661577

* Wed Jan 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b13-1
- Update to aarch64-shenandoah-jdk8u191-b13.
- Update tarball generation script in preparation for PR3667/RH1656676 SunEC changes.
- Use remove-intree-libraries.sh to remove the remaining SunEC code for now.
- Resolves: rhbz#1661577

* Wed Dec 19 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-15
- Fix jdk8073139-pr1758-rh1191652-ppc64_le_says_its_arch_is_ppc64_not_ppc64le_jdk.patch paths to pass git apply
- Resolves: rhbz#1633817

* Tue Dec 04 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.191.b12-14
- Added %%global _find_debuginfo_opts -g
- Resolves: rhbz#1656996

* Tue Nov 27 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.191.b12-1.el7_6
- import source package EL7/java-1.8.0-openjdk-1.8.0.181-7.b13.el7

* Thu Nov 22 2018 Andrew John Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-13
- Add backport of JDK-8029661 which adds TLSv1.2 support to the PKCS11 provider.
- Resolves: rhbz#1477159

* Tue Nov 20 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-12
- Revise Shenandoah PR3634 patch following upstream discussion.
- Resolves: rhbz#1633817

* Tue Nov 20 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.191.b12-11
- Renamed all patches to new convention
-   bug1-bug2-..-bugN-XY-lowercase_comment_suffix_or_jdkpart.patch
- Resolves: rhbz#1633817

* Wed Nov 07 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.191.b12-10
- Headful Requires of cups, replaced by Requires of cups-libs in headless
- Resolves: rhbz#1598152

* Wed Nov 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-9
- Note why PR1834/RH1022017 is not suitable to go upstream in its current form.
- Resolves: rhbz#1633817

* Tue Nov 06 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-9
- Document patch sections.
- Resolves: rhbz#1633817
- Fix patch organisation in the spec file:
-   * Move ECC patches back to upstreamable section
-   * Move system cacerts patches to upstreamable section
-   * Merge "Local fixes" and "RPM fixes" which amount to the same thing
-   * Move system libpng & lcms patches back to 8u upstreamable section
-   * Make it clearer that "Non-OpenJDK fixes" is currently empty
- Bump release so y-stream is higher than z-stream.

* Mon Oct 29 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.191.b12-8
- added Patch583 jdk8172850-rh1640127-01-register_allocator_crash.patch
- added Patch584 jdk8209639-rh1640127-02-coalesce_attempted_spill_non_spillable.patch
- Resolves: rhbz#1633817

* Mon Oct 29 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.191.b12-7
- Add patch jdk8210425-rh1632174-03-compile_with_o2_and_ffp_contract_off_as_for_fdlibm_zero.patch:
  - Annother fix for optimization gaps (annocheck issues)
  - Zero 8u version fix was missing. Hence, only shows up on Zero arches.
- Resolves: rhbz#1633817

* Mon Oct 29 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.191.b12-6
- Add fixes for optimization gaps (annocheck issues):
  - 8210761: libjsig is being compiled without optimization
  - 8210647: libsaproc is being compiled without optimization
  - 8210416: [linux] Poor StrictMath performance due to non-optimized compilation
  - 8210425: [x86] sharedRuntimeTrig/sharedRuntimeTrans compiled without optimization
             8u upstream and aarch64/jdk8u upstream versions.
- Resolves: rhbz#1633817

* Mon Oct 29 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.191.b12-5
- Removed patch, rh1214835.patch, since it's invalid:
  See https://icedtea.classpath.org/bugzilla/show_bug.cgi?id=2304#c3
- Resolves: rhbz#1633817

* Mon Oct 29 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.191.b12-4
- Update(s) from upstreamed patches:
  - jdk8036003-add_with_native_debug_symbols_configure_flag.patch
  - jdk8150954-pr2866-rh1176206-screenshot_xcomposite_jdk.patch =>
    jdk8150954-pr2866-rh1176206-screenshot_xcomposite_jdk.patch
    Deleted rh1176206-root.patch as thats no longer needed with
    upstream 8150954.
  - 8207057-pr3613-hotspot-assembler-debuginfo.patch =>
    jdk8207057-pr3613-no_debug_info_for_assembler_files_hotspot.patch and
    jdk8207057-pr3613-no_debug_info_for_assembler_files_root.patch. From JDK 8u
    backport.
- Use --with-native-debug-symbols=internal which JDK-8036003 adds.
- Remove comment for make invocation since it's no longer valid.
  --with-native-debug-symbols=internal will do everything we need.
- Resolves: rhbz#1633817

* Tue Oct 23 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.191.b12-3
- cups moved to headful package
- enabled gtk2 in headful package (RH1598152)
- Resolves: rhbz#1633817

* Fri Oct 19 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.191.b12-0.el7_5

* Fri Oct 19 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.191.b12-2
- made rhpkg and srpm or rebuild working on fedora again
- cosmetic changes - using macros where possible
- fixed issues in desktop files (missing vendor, unexpandedmacros, missing information)
- README.src renamed to README.md
- Resolves: rhbz#1633817

* Tue Oct 09 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-1
- Update to aarch64-shenandoah-jdk8u191-b12.
- Resolves: rhbz#1633817

* Fri Oct 05 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b10-1
- Bump release to be greater than rhel-7.5.z
- Resolves: rhbz#1633817

* Tue Oct 02 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b10-0
- Update to aarch64-shenandoah-jdk8u191-b10.
- Drop 8146115/PR3508/RH1463098 applied upstream.
- Resolves: rhbz#1633817

* Mon Oct 01 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181.b16-0
- Add new Shenandoah patch PR3634 as upstream still fails on s390.
- Resolves: rhbz#1633822
- Update to aarch64-shenandoah-jdk8u181-b16.
- Drop PR3619 & PR3620 Shenandoah patches which should now be fixed upstream.

* Thu Aug 23 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181.b15-0
- Move to single OpenJDK tarball build, based on aarch64/shenandoah-jdk8u.
- Update to aarch64-shenandoah-jdk8u181-b15.
- Drop 8165489-pr3589.patch which was only applied to aarch64/jdk8u builds.
- Move buildver to where it should be in the OpenJDK version.
- Split ppc64 Shenandoah fix into separate patch file with its own bug ID (PR3620).
- Update pr3539-rh1548475.patch to apply after 8187045.
- Resolves: rhbz#1594249

* Sat Aug 11 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Remove unneeded functions from ppc shenandoahBarrierSet.
- Resolves: rhbz#1594249

* Wed Aug 8 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.181-3.b13.el7_5

* Wed Aug 08 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Add missing shenandoahBarrierSet implementation for ppc64{be,le}.
- Resolves: rhbz#1594249

* Tue Aug 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Fix wrong format specifiers in Shenandoah code.
- Resolves: rhbz#1594249
- Avoid changing variable types to fix size_t, at least for now.
- More size_t fixes for Shenandoah.

* Fri Aug 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Add additional s390 size_t case for Shenandoah.
- Resolves: rhbz#1594249
- Actually add the patch...
- Attempt to fix Shenandoah build issues on s390.

* Mon Jul 23 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Use the Shenandoah HotSpot on all architectures.
- Resolves: rhbz#1594249

* Mon Jul 16 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-7.b13
- Update to aarch64-jdk8u181-b13 and aarch64-shenandoah-jdk8u181-b13.
- Remove 8187577/PR3578 now applied upstream.
- Resolves: rhbz#1594249

* Mon Jul 16 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.181-7.b04
- Fix hook to show hs_err*.log files on failures.
- Resolves: rhbz#1594249
- Fix requires/provides filters for internal libs. See RHBZ#1590796

* Mon Jul 16 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-7.b04
- Update bug status and add missing bug IDs
- Resolves: rhbz#1594249

* Thu Jul 12 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-6.b04
- Add "8146115, PR3508, RH1463098: Improve docker container detection and resource configuration usage"
- Resolves: rhbz#1463098

* Wed Jul 11 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-5.b04
- Add "8206406, PR3610, RH1597825: StubCodeDesc constructor publishes partially-constructed objects on StubCodeDesc::_list"
- Resolves: rhbz#1597825

* Tue Jul 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-4.b04
- Mark bugs now backported to OpenJDK 8u upstream
- Resolves: rhbz#1594249
- Backport "8203182, PR3603: Release session if initialization of SunPKCS11 Signature fails"
- Resolves: rhbz#1568033
- Backport "8075942, PR3602: ArrayIndexOutOfBoundsException in sun.java2d.pisces.Dasher.goTo"
- Resolves: rhbz#1582032

* Wed Jun 27 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.181-3.b04
- Add hook to show hs_err*.log files on failures.
- Resolves: rhbz#1594249

* Wed Jun 27 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-3.b04
- Mark bugs that have been pushed to 8u upstream and are scheduled for a release.
- Resolves: rhbz#1594249

* Wed Jun 27 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-2.b04
- Update to aarch64-jdk8u181-b04 and aarch64-shenandoah-jdk8u181-b04.
- Resolves: rhbz#1594249

* Sun Jun 24 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-1.b03
- Update to aarch64-jdk8u181-b03 and aarch64-shenandoah-jdk8u181-b03.
- Remove AArch64 patch for PR3458/RH1540242 as applied upstream.
- Resolves: rhbz#1594249

* Thu Jun 21 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-11.b11
- Update Shenandoah tarball to fix TCK overflow failure.
- Resolves: rhbz#1573700

* Wed Jun 20 2018 Jiri Vanek <jvanek@redhat.com> - 11:1.8.0.172-10.b11
- jsa files changed to 444 to pass rpm verification
- Fix reg-ex for filtering private libraries' provides/requires.
- Resolves: rhbz#1573700

* Wed Jun 20 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-7.b11
- Add additional fix (PR3601) to fix -Wreturn-type failures introduced by 8061651
- Resolves: rhbz#1573700

* Tue Jun 19 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-7.b11
- Backport 8064786 (PR3601) to fix -Wreturn-type failure on debug builds.
- Resolves: rhbz#1573700

* Mon Jun 18 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-7.b11
- Bring in PR3519 from IcedTea 3.7.0 to fix remaining -Wreturn-type failure on AArch64.
- Resolves: rhbz#1573700

* Sat Jun 16 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-7.b11
- Sync with IcedTea 3.8.0 patches to use -Wreturn-type.
- Add backports of 8141570, 8143245, 8197981 & 8062808.
- Drop pr3458-rh1540242-zero.patch which is covered by 8143245.
- Resolves: rhbz#1573700

* Wed Jun 13 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-6.b11
- Remove build flags exemption for aarch64 now the platform is more mature and can bootstrap OpenJDK with these flags.
- Remove duplicate -fstack-protector-strong; it is provided by the RHEL cflags.
- Resolves: rhbz#1573700

* Mon Jun 11 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-5.b11
- Read jssecacerts file prior to trying either cacerts file (system or local) (PR3575)
- Resolves: rhbz#1567204
- Fix a number of bad bug identifiers (PR3546 should be PR3578, PR3456 should be PR3546)
- Resolves: rhbz#1573700

* Thu Jun 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-4.b11
- Update Shenandoah tarball to include 2018-05-15 merge.
- Split PR3458/RH1540242 fix into AArch64 & Zero sections, so former can be skipped on Shenandoah builds.
- Drop PR3573 patch applied upstream.
- Restrict 8187577 fix to non-Shenandoah builds, as it's included in the new tarball.
- Resolves: rhbz#1573700

* Thu Jun 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-3.b11
- Sync with IcedTea 3.8.0.
- Label architecture-specific fixes with architecture concerned
- x86: S8199936, PR3533: HotSpot generates code with unaligned stack, crashes on SSE operations (-mstackrealign workaround)
- PR3539, RH1548475: Pass EXTRA_LDFLAGS to HotSpot build
- 8171000, PR3542, RH1402819: Robot.createScreenCapture() crashes in wayland mode
- 8197546, PR3542, RH1402819: Fix for 8171000 breaks Solaris + Linux builds
- 8185723, PR3553: Zero: segfaults on Power PC 32-bit
- 8186461, PR3557: Zero's atomic_copy64() should use SPE instructions on linux-powerpcspe
- PR3559: Use ldrexd for atomic reads on ARMv7.
- 8187577, PR3578: JVM crash during gc doing concurrent marking
- 8201509, PR3579: Zero: S390 31bit atomic_copy64 inline assembler is wrong
- 8165489, PR3589: Missing G1 barrier in Unsafe_GetObjectVolatile
- PR3591: Fix for bug 3533 doesn't add -mstackrealign to JDK code
- 8184309, PR3596: Build warnings from GCC 7.1 on Fedora 26
- Resolves: rhbz#1573700

* Tue May 22 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.171-8.b10.el7_5

* Wed May 16 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.172-2.b11
- added and applied 1566890_embargoed20180521.patch
- Resolves: rhbz#1578558

* Wed May 09 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-1.b11
- Update to aarch64-jdk8u172-b11 and aarch64-shenandoah-jdk8u172-b11.
- Resolves: rhbz#1573700

* Thu May 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-9.b12
- Update to aarch64-jdk8u171-b12 and aarch64-shenandoah-jdk8u171-b12.
- Remove patch for 8200556/PR3566 as applied upstream.
- Resolves: rhbz#1573700

* Fri Apr 20 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.171-7.b10.el7

* Wed Apr 18 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-8.b10
- Bump release to 8 so it is again greater than the 7.5.z version.
- Resolves: rhbz#1559766

* Tue Apr 17 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.161-2.b14.el7

* Thu Apr 12 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-3.b10
- Fix jconsole.desktop.in subcategory, replacing "Monitor" with "Profiling" (PR3550)
- Resolves: rhbz#1559766

* Thu Apr 12 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-6.b10
- Fix invalid license 'LGPL+' (should be LGPLv2+ for ECC code) and add misisng ones
- Resolves: rhbz#1559766

* Thu Apr 12 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-5.b10
- Add fix for TCK crash on Shenandoah.
- Resolves: rhbz#1559766

* Mon Apr 02 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-4.b10
- Cleanup from previous commit.
- Remove unused upstream patch 8167200.hotspotAarch64.patch.
- Resolves: rhbz#1559766
- Resolves: rhbz#1536623

* Thu Mar 29 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.171-3.b10
- Backported from fedora: aarch64BuildFailure.patch, rhbz_1536622-JDK8197429-jdk8.patch, rhbz_1540242.patch
- Resolves: rhbz#1559766

* Mon Mar 26 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-1.b10
- Bump release for RHEL 7.6 now branch is available.
- Resolves: rhbz#1538772
- Resolves: rhbz#1559766

* Sat Mar 24 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-0.b10
- Update to aarch64-jdk8u171-b10 and aarch64-shenandoah-jdk8u171-b10.
- Resolves: rhbz#1559766

* Wed Mar 21 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.162-0.b12
- Update to aarch64-jdk8u162-b12 and aarch64-shenandoah-jdk8u162-b12.
- Remove upstreamed patches for 8181055/PR3394/RH1448880,
-  8181419/PR3413/RH1463144, 8145913/PR3466/RH1498309,
-  8168318/PR3466/RH1498320, 8170328/PR3466/RR1498321 and
-  8181810/PR3466/RH1498319.
- Resolves: rhbz#1559766

* Thu Feb 1 2018 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.161-0.b14.el7_4

* Fri Jan 12 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.161-2.b14
- Rebuild to fix temporary loss of RELRO on ppc64 and ppc64le
- Resolves: rhbz#1528233

* Wed Jan 10 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.161-1.b14
- Update to b14 with updated Zero fix for 8174962 (S8194828)
- Resolves: rhbz#1528233

* Tue Jan 09 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.161-1.b13
- Update to b13 including Zero fix for 8174962 (S8194739) and restoring tzdata2017c update
- Resolves: rhbz#1528233

* Mon Jan 08 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.161-1.b12
- Replace tarballs with version including AArch64 fix for 8174962 (S8194686)
- Resolves: rhbz#1528233

* Tue Jan 02 2018 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.161-1.b12
- Update to aarch64-jdk8u161-b12 and aarch64-shenandoah-jdk8u161-b12 (mbalao)
- Drop upstreamed patches for 8075484 (RH1490713), 8153711 (RH1284948),
  8162384 (RH1358661), 8164293 (RH1459641), 8173941, 8175813 (RH1448880),
  8175887 and 8180048 (RH1449870).(mbalao)
- drop more of usptreamed patches 565,566,567,568
  ( 8184673-pr3475-rh1487266.patch  8191840-pr3503-rh1512647.patch  8191137-pr3503-rh1512647.patch 8190258-pr3499-tzdata2017c.patch)
- Resolves: rhbz#1528233

* Wed Dec 20 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.151-5.b12.el7_4

* Wed Dec 20 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.152-1.b16
- Backport 8191137 and add updates to the translations (8191840 in OpenJDK 7)
- Resolves: rhbz#1512647
- Update to tzdata2017c (8190258/PR3499) to resolve TCK failure due to mismatch with system version.
- Resolves: rhbz#1508017
- Update to aarch64-jdk8u152-b16 and aarch64-shenandoah-jdk8u152-b16.
- Update 8145913/PR3466/RH1498309 patch following upstream addition of 8152172 (AES for PPC)
- Add new file cmsalpha.c to %%{name}-remove-intree-libraries.sh
- Remove upstreamed patches for 8153711/PR3313/RH1284948, 8162384/PR3122/RH1358661, 8173941/PR3226,
-    8175813/PR3394/RH1448880, 8175887/PR3415, 8146086/PR3439/RH1478402, 8180048/PR3411/RH1449870 and
-    8164293/PR3412/RH1459641

* Wed Nov 15 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-5.b13
- Update to aarch64-jdk8u151-b13 and aarch64-shenandoah-jdk8u151-b13.
- Drop upstreamed patch for 8075484.
- Resolves: rhbz#1508017

* Mon Oct 30 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-4.b12
- Bump release number so it remains higher than z-stream.
- Resolves: rhbz#1459641

* Thu Oct 26 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-3.b12
- Add backport of 8184673/PR3475/RH1487266 patch.
- Resolves: rhbz#1487266
- Backport "8180048: Interned string and symbol table leak memory during parallel unlinking"
- Resolves: rhbz#1490260
- Add backport of 8146086/PR3439/RH1478402 JAXWS fix.
- Resolves: rhbz#1478402
- Switch bootstrap back to java-1.7.0-openjdk on all architectures, depending on RH1482244 fix
- Resolves: rhbz#1499207

* Sat Oct 21 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.151-1.b12.el7_4

* Wed Oct 18 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.151-2.b12
- repack policies adapted to new counts and paths
- note that also c-j-c is needed to make this apply in next update
- Resolves: rhbz#1499207

* Wed Oct 18 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Update location of policy JAR files following 8157561.
- 8188030 is not yet upstream, so it should be listed under upstreamable fixes.
- 8181055, 8181419, 8145913, 8168318, 8170328 & 8181810 all now in 8u162.
- Resolves: rhbz#1499207
- Correct fix to RH1191652 root patch so existing COMMON_CCXXFLAGS_JDK is not lost.

* Tue Oct 17 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.151-1.b01
- Moving patch 560 out of ppc fixes
- Resolves: rhbz#1499207

* Tue Oct 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Update SystemTap tapsets to version in IcedTea 3.6.0pre02 to fix RH1492139.
- Resolves: rhbz#1499207
- Fix premature shutdown of NSS in SunEC provider.
- Add 8075484/PR3473/RH1490713 which is listed as being in 8u151 but not supplied by Oracle.
- Update to aarch64-jdk8u151-b12 and aarch64-shenandoah-jdk8u151-b12.
- Update location of OpenJDK zlib system library source code in remove-intree-libraries.sh
- Drop upstreamed patches for 8179084 and RH1367357 (part of 8183028).
- Update RH1191652 (root) and PR2842 to accomodate 8151841 (GCC 6 support).
- Update PR2964/RH1337583 to accomodate 8171319 (keytool warning output)
- Update RH1163501 to accomodate 8181048 (crypto refactoring)

* Mon Oct 16 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Reverted completely unnecessary patch addition which broke the RPM build.
- Resolves: rhbz#1484079

* Wed Oct 11 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.144-2.b01
- smuggled patch540, bug1484079.patch
- Resolves: rhbz#1484079

* Wed Oct 11 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Switch AArch64 to using java-1.8.0-openjdk to bootstrap until RH1482244 is fixed in bootstrap
- Resolves: rhbz#1499207
- Switch to IBM-supplied Montgomery backport and add remaining ppc64 fixes & CFF fix
- Resolves: rhbz#1498309
- Resolves: rhbz#1498319
- Resolves: rhbz#1498320
- Resolves: rhbz#1498321
- Resolves: rhbz#1484079

* Tue Oct 10 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Backport Montgomery multiply intrinsic and dependencies for ppc64
- Resolves: rhbz#1498309

* Wed Sep 6 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.144-0.b01.el7_4

* Tue Aug 15 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-1.b01
- Update to aarch64-jdk8u144-b01 and aarch64-shenandoah-jdk8u144-b01.
- Exclude 8175887 from Shenandoah builds as it has been included in that repo.
- Resolves: rhbz#1477855

* Mon Aug 14 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-3.b16
- Added 8164293-pr3412-rh1459641.patch backport from 8u development tree
- Resolves: rhbz#1459641

* Wed Aug 2 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.141-2.b16.el7_4
- import source package EL7/java-1.8.0-openjdk-1.8.0.131-11.b12.el7

* Tue Jul 25 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.141-1.b16.el7_3

* Fri Jul 14 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-2.b16
- Update to aarch64-jdk8u141-b16 and aarch64-shenandoah-jdk8u141-b16.
- Revert change to remove-intree-libraries.sh following backout of 8173207
- Resolves: rhbz#1466509

* Wed Jul 05 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-1.b15
- Actually add sources for previous commit.
- Resolves: rhbz#1466509
- Update to aarch64-jdk8u141-b15 and aarch64-shenandoah-jdk8u141-b15.
- Update location of OpenJDK system library source code in remove-intree-libraries.sh
- Drop upstreamed patches for 6515172, 8144566, 8155049, 8165231, 8174164, 8174729 and 8175097.
- Update PR1983, PR2899 and PR2934 (SunEC + system NSS) to accomodate 8175110.

* Wed Jul 05 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-12.b12
- Add backports from 8u152 (8179084/RH1455694, 8181419/RH1463144, 8175887) ahead of July CPU.
- Resolves: rhbz#1466509

* Tue Jun 13 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.131-11.b12
- make to use latest c-j-c and so fix persisting issues with java.security and other configfiles
- 1183793 is missing blocker
- Resolves: rhbz#1448880

* Wed May 31 2017 Zhengyu Gu <zgu@redhat.com> - 1:1.8.0.131-10.b12
- Added 8181055-pr3394-rh1448880.patch to fix a corner case of previous change
- Resolves: rhbz#1448880

* Fri May 26 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.131-3.b12.el7_3

* Fri May 19 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-9.b12
- Move 8175813/PR3394/RH1448880 to correct section and document.
- Resolves: rhbz#1448880

* Fri May 19 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.131-9.b12
- Added and applied patch550 8175813-rh1448880.patch
- Resolves: rhbz#1448880

* Fri May 12 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-8.b12
- Restore cacerts symlink as some broken apps hardcode the path (see RH1448802)
- Resolves: rhbz#1319875

* Mon May 01 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-7.b12
- Fix misspelt accessibility Provides
- Resolves: rhbz#1438514

* Thu Apr 27 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-6.b12
- Update to aarch64-jdk8u131-b12 and aarch64-shenandoah-jdk8u131-b12 for AArch64 8168699 fix
- Resolves: rhbz#1443417

* Fri Apr 21 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.131-2.b11.el7_3

* Fri Apr 21 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.131-5.b11
- Minor tweaks
- Resolves: rhbz#1438514

* Tue Apr 18 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-4.b11
- Rename SystemTap tapset tarball to avoid conflicts with previous version.
- Resolves: rhbz#1438514

* Fri Apr 14 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-3.b11
- Bump release to make sure y-stream takes priority over z-stream.
- Resolves: rhbz#1438514

* Thu Apr 13 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-2.b11
- Update tapset tarball to include the better error handling in PR3348
- http://icedtea.classpath.org/hg/icedtea8/rev/14fc67a5d5a3
- Resolves: rhbz#1438514

* Thu Apr 13 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.131-1.b11
- Update to aarch64-jdk8u131-b11 and aarch64-shenandoah-jdk8u131-b11.
- Drop upstreamed patches for 8147910, 8161993, 8170888 and 8173783.
- Update generate_source_tarball.sh to remove patch remnants.
- Cleanup Shenandoah tarball referencing and document how to create it.
- Add MD5 checksum for the new java.security file (MD5 disabled for JAR signing)
- Resolves: rhbz#1438751

* Fri Apr 07 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-10.b14
- Add backports from 8u131 and 8u152 ahead of April CPU.
- Apply backports before local RPM fixes so they will be the same as when applied upstream
- Adjust RH1022017 following application of 8173783
- Resolves: rhbz#1438751
- Move unprocessed nss.cfg to nss.cfg.in and add missing substitution to create nss.cfg for install
- Resolves: rhbz#1429774

* Mon Mar 20 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-9.b14
- Actually fix SystemTap source tarball name to match new one
- Resolves: rhbz#1373848

* Sat Mar 18 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-9.b14
- Introduce stapinstall variable to set SystemTap arch directory correctly (e.g. arm64 on aarch64)
- Update jstack tapset to handle AArch64
- Resolves: rhbz#1373848

* Mon Mar 13 2017 jvanek <jvanek@redhat.com> - 1:1.8.0.121-8.b14
- self-sependencies restricted by isa
- Resolves: rhbz#1388520

* Wed Mar 08 2017 jvanek <jvanek@redhat.com> - 1:1.8.0.121-7.b14
- updated to aarch64-shenandoah-jdk8u121-b14-shenandoah-merge-2017-03-08 (from aarch64-port/jdk8u-shenandoah) of hotspot
- used aarch64-port-jdk8u-shenandoah-aarch64-shenandoah-jdk8u121-b14-shenandoah-merge-2017-03-09.tar.xz as new sources for hotspot
- Resolves: rhbz#1400306

* Fri Mar 03 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-6.b14
- Restore .gitignore lines removed by "Fedora sync"
- Resolves: rhbz#1400306
- Patch OpenJDK to check the system cacerts database directly
- Remove unneeded symlink to the system cacerts database
- Drop outdated openssl dependency from when the RPM built the cacerts database
- Resolves: rhbz#1319875
- Regenerate tarball with correct version of PR2126 patch.
- Update generate_source_tarball.sh script to download correct version.
- Properly document recently added patches.

* Tue Feb 28 2017 jvanek <jvanek@redhat.com> - 1:1.8.0.121-5.b14
- shenandoah enabled on aarch64
- Resolves: rhbz#1400306

* Tue Feb 28 2017 jvanek <jvanek@redhat.com> - 1:1.8.0.121-4.b14
- added shenandoah hotspot
- sync with fedora
- Resolves: rhbz#1400306
- Resolves: rhbz#1390708
- Resolves: rhbz#1388520
- Resolves: rhbz#1403992

* Mon Feb 20 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-3.b13
- Backport "8170888: [linux] Experimental support for cgroup memory limits in container (ie Docker) environments"
- Resolves: rhbz#1390708

* Fri Feb 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-2.b13
- Backport "S8153711: [REDO] JDWP: Memory Leak: GlobalRefs never deleted when processing invokeMethod command"
- Resolves: rhbz#1284948

* Thu Jan 26 2017 Frederick Lefebvre <fredlef@amazon.com>
- Merge of EL7 upstream
- Update to EL7 upstream
- Update from EL7 upstream

* Sat Jan 21 2017 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.121-0.b13.el7_3

* Mon Jan 16 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-1.b13
- Update to aarch64-jdk8u121-b13.
- Add MD5 checksum for the new java.security file (EC < 224, DSA < 1024 restricted)
- Update PR1834/RH1022017 fix to reduce curves reported by SSL to apply against u121.
- Resolves: rhbz#1410612

* Mon Jan 16 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.112-1.b16
- Fix accidental change of line in updated size_t patch.
- Resolves: rhbz#1391132

* Sun Jan 15 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.112-1.b16
- Update to aarch64-jdk8u112-b16.
- Drop upstreamed patches for 8044762, 8049226, 8154210, 8158260 and 8160122.
- Re-generate size_t and key size (RH1163501) patches against u112.
- Resolves: rhbz#1391132

* Thu Jan 12 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-5.b18
- Use java-1.7.0-openjdk to bootstrap on RHEL to allow us to use main build target
- Resolves: rhbz#1391132

* Mon Jan 09 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-4.b18
- Replace our correct version of 8159244 with the amendment to the 8u version from 8160122.
- Resolves: rhbz#1391132
- Update to aarch64-jdk8u111-b18, synced with upstream u111, S8170873 and new AArch64 fixes

* Mon Nov 07 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-3.b15
- Add MD5 checksum from RHEL 7.2 security update so the 7.3 one overwrites it.
- Resolves: rhbz#1391132

* Fri Nov 4 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.111-2.b15.el7_3

* Thu Nov 3 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.102-4.b14.el7

* Thu Oct 20 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.111-1.b15.el7_2

* Mon Oct 10 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-2.b15
- Turn debug builds on for all JIT architectures. Always AssumeMP on RHEL.
- Resolves: rhbz#1382736

* Fri Oct 07 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-1.b15
- Update to aarch64-jdk8u111-b15, with AArch64 fix for S8160591.
- Resolves: rhbz#1382736

* Fri Oct 07 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-0.b14
- Update to aarch64-jdk8u111-b14.
- Add latest md5sum for java.security file due to jar signing property addition.
- Drop S8157306 and the CORBA typo fix, both of which appear upstream in u111.
- Add LCMS 2 patch to fix Red Hat security issue RH1367357 in the local OpenJDK copy.
- Resolves: rhbz#1350037

* Wed Oct 5 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.102-5.b14
- debug subpackages allowed on aarch64 and ppc64le
- Resolves: rhbz#1375224

* Thu Sep 15 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.102-1.b14.el7_2

* Wed Sep 14 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.102-4.b14
- Runtime native library requirements need to match the architecture of the JDK
- Resolves: rhbz#1375224

* Mon Sep 05 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.102-3.b14
- Rebuild java-1.8.0-openjdk for GCC aarch64 stack epilogue code generation fix (RH1372750)
- Resolves: rhbz#1359857

* Wed Aug 31 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.102-2.b14
- declared check_sum_presented_in_spec and used in prep and check
- it is checking that latest packed java.security is mentioned in listing
- Resolves: rhbz#1295754

* Mon Aug 29 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.102-2.b14
- @prefix@ in tapsetfiles substitued by prefix as necessary to work with systemtap3 (rhbz1371005)
- Resolves: rhbz#1295754

* Thu Aug 25 2016 jvanek <jvanek@redhat.com> - 1:1.8.0.102-1.b14
- jjs provides moved to headless
- Resolves: rhbz#1312019

* Mon Aug 08 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.102-0.b14
- Update to aarch64-jdk8u102-b14.
- Drop 8140620, 8148752 and 6961123, all of which appear upstream in u102.
- Move 8159244 to 8u111 section as it only appears to be in unpublished u102 b31.
- Move 8158260 to 8u112 section following its backport to 8u.
- Resolves: rhbz#1359857

* Wed Aug 03 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-9.b15
- Update to aarch64-jdk8u101-b15.
- Rebase SystemTap tarball on IcedTea 3.1.0 versions so as to avoid patching.
- Drop additional hunk for 8147771 which is now applied upstream.
- Resolves: rhbz#1359857

* Mon Aug 01 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-8.b13
- Replace patch for S8162384 with upstream version. Document correctly along with SystemTap RH1204159 patch.
- Resolves: rhbz#1358661
- Replace patch for S8157306 with upstream version, documented & applied on all archs with conditional in patch
- Resolves: rhbz#1360863

* Thu Jul 28 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.101-7.b13
- added patch532 hotspot-1358661.patch - to fix performance of bimorphic inlining may be bypassed by type speculation
- rhbz1358661
- added patch301 bz1204159_java8.patch - to fix systemtap on multiple jdks
- rhbz1204159
- added patch531 hotspot-8157306.changeset - to fix rare NPE injavac on aarch64
- rhbz1360863
- added all virtual provides of java-devel
- Resolves: rhbz#1216018

* Wed Jul 20 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.101-3.b13.el7_2

* Tue Jul 12 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.101-5.b13
- added Provides: /usr/bin/jjs
- Resolves: rhbz#1312019

* Mon Jul 11 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-4.b13
- Replace bad 8159244 patch from upstream 8u with fresh backport from OpenJDK 9.
- Resolves: rhbz#1335322

* Sun Jul 10 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-3.b13
- Add missing hunk from 8147771, missed due to inclusion of unneeded 8138811
- Resolves: rhbz#1350037

* Mon Jul 04 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-2.b13
- Add workaround for a typo in the CORBA security fix, 8079718
- Resolves: rhbz#1350037
- Fix regression in SSL debug output when no ECC provider is available.
- Resolves: rhbz#1346460

* Fri Jul 01 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-1.b13
- Update to u101b13.
- Document REPOS option in generate_source_tarball.sh
- Drop a leading zero from the priority as the update version is now three digits
- Resolves: rhbz#1350037

* Fri Jul 01 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.92-9.b14
- Add additional fixes (S6260348, S8159244) for u92 update.
- Add bug ID to Javadoc patch.
- Resolves: rhbz#1335322

* Fri Jun 24 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.91-1.b14.el7_2

* Tue Jun 21 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.92-7.b14
- family restricted by arch
- Resolves: rhbz#1296442
- Resolves: rhbz#1296414

* Mon Jun 20 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.92-6.b14
- Update ppc64le fix with upstream version, S8158260.
- Resolves: rhbz#1341258

* Tue Jun 07 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.92-5.b14
- added --family option with chkconfig version full dependence
- added nss restricting requires
- added zipped javadoc subpackage
- extracted lua scripts
- Resolves: rhbz#1296442
- Resolves: rhbz#1296414

* Tue Jun 07 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.92-4.b14
- added requires for copy-jdk-configs, to help with https://projects.engineering.redhat.com/browse/RCM-3654
- Resolves: rhbz#1296442

* Thu Jun 02 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.92-3.b14
- Forwardport SSL fix to only report curves supported by NSS.
- Resolves: rhbz#1245810
- Add fix for ppc64le crash due to illegal instruction.
- Resolves: rhbz#1341258

* Wed Jun 01 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.92-2.b14
- Add fix for PKCS#10 output regression, adding -systemlineendings option.
- Move S8150954/RH1176206/PR2866 fix to correct section, as not in 9 yet.
- Resolves: rhbz#1337583

* Thu May 26 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.92-1.b14
- Update to u92b14.
- Remove upstreamed patches for AArch64 byte behaviour and template issue.
- Remove upstreamed patches for Zero build failures 8087120 & 8143855.
- Replace 8132051 Zero fix with version upstreamed as 8154210 in 8u112.
- Add upstreamed patch 6961123 from u102 to fix application name in GNOME Shell.
- Add upstreamed patches 8044762 & 8049226 from u112 to fix JDI issues.
- Regenerate java-1.8.0-openjdk-rh1191652-root.patch against u92
- Resolves: rhbz#1335322

* Fri May 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-3.b14
- Add backport for S8148752.
- Resolves: rhbz#1330188

* Fri Apr 22 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-2.b14
- Add fix for PR2934 / RH1329342
- Re-enable ECDSA test which now passes.
- Resolves: rhbz#1245810

* Wed Apr 20 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.91-0.b14.el7_2

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Roll back release number as release 1 never succeeded, even with tests disabled.
- Resolves: rhbz#1325423
- Add additional fix to Zero patch to properly handle result on 64-bit big-endian
- Revert debugging options (aarch64 back to JIT, product build, no -Wno-error)
- Enable full bootstrap on all architectures to check we are good to go.
- Turn tests back on or build will not fail.
- Temporarily remove power64 from JIT arches to see if endian issue appears on Zero.
- Turn off Java-based checks in a vain attempt to get a complete build.
- Turn off -Werror so s390 can build in slowdebug mode.
- Add fix for formatting issue found by previous s390 build.
- Revert settings to production defaults so we can at least get a build.
- Switch to a slowdebug build to try and unearth remaining issue on s390x.

* Mon Apr 11 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Disable ECDSA test for now until failure on RHEL 7 is fixed.
- Resolves: rhbz#1325423
- Add 8132051 port to Zero.
- Turn on bootstrap build for all to ensure we are now good to go.
- Add 8132051 port to AArch64.
- Enable a full bootstrap on JIT archs. Full build held back by Zero archs anyway.

* Sun Apr 10 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Use basename of test file to avoid misinterpretation of full path as a package
- Resolves: rhbz#1325423
- Update to u91b14.

* Thu Mar 31 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-3.b03
- Fix typo in test invocation.
- Resolves: rhbz#1245810
- Add ECDSA test to ensure ECC is working.

* Wed Mar 30 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-2.b03
- Avoid WithSeed versions of NSS functions as they do not fully process the seed
- List current java.security md5sum so that java.security is replaced and ECC gets enabled.
- Resolves: rhbz#1245810

* Fri Mar 25 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.77-0.b03.el7_2

* Wed Mar 23 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-1.b03
- Bump release so 7.3 stays greater than 7.2.z
- Resolves: rhbz#1320665

* Wed Mar 23 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-0.b03
- Update to u77b03.
- Resolves: rhbz#1320665

* Thu Mar 03 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-13.b16
- When using a compositing WM, the overlay window should be used, not the root window.
- Resolves: rhbz#1176206

* Mon Feb 29 2016 Omair Majid <omajid@redhat.com> - 1:1.8.0.72-12.b15
- Use a simple backport for PR2462/8074839.
- Don't backport the crc check for pack.gz. It's not tested well upstream.
- Resolves: rhbz#1307108

* Mon Feb 29 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-5.b16
- Fix regression introduced on s390 by large code cache change.
- Resolves: rhbz#1307108
- Update to u72b16.
- Drop 8147805 and jvm.cfg fix which are applied upstream.

* Wed Feb 24 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-4.b15
- Add patches to allow the SunEC provider to be built with the system NSS install.
- Re-generate source tarball so it includes ecc_impl.h.
- Adjust tarball generation script to allow ecc_impl.h to be included.
- Bring over NSS changes from java-1.7.0-openjdk spec file (NSS_CFLAGS/NSS_LIBS)
- Remove patch which disables the SunEC provider as it is now usable.
- Correct spelling mistakes in tarball generation script.
- Resolves: rhbz#1245810
- Move completely unrelated AArch64 gcc 6 patch into separate file.
- Resolves: rhbz#1300630

* Tue Feb 23 2016 jvanek <jvanek@redhat.com> - 1:1.8.0.72-3.b15
- returning accidentlay removed hunk from renamed and so wrongly merged remove_aarch64_jvm.cfg_divergence.patch
- Resolves: rhbz#1300630

* Mon Feb 22 2016 jvanek <jvanek@redhat.com> - 1:1.8.0.72-2.b15
- sync from fedora
- Resolves: rhbz#1300630

* Fri Feb 19 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-1.b15
- Actually add the patch...
- Resolves: rhbz#1300630
- Add backport of 8147805: aarch64: C1 segmentation fault due to inline Unsafe.getAndSetObject

* Thu Feb 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Remove unnecessary AArch64 port divergence on parsing jvm.cfg, broken by 9399aa7ef558
- Resolves: rhbz#1307108
- Only use z format specifier on s390, not s390x.

* Wed Feb 17 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Remove fragment of s390 size_t patch that unnecessarily removes a cast, breaking ppc64le.
- Remove aarch64-specific suffix as update/build version are now the same as for other archs.
- Resolves: rhbz#1307108
- Replace s390 Java options patch with general version from IcedTea.
- Apply s390 patches unconditionally to avoid arch-specific patch failures.

* Tue Feb 16 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Update to u72b15.
- Drop 8146566 which is applied upstream.
- Resolves: rhbz#1307108

* Tue Feb 09 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-6.b15
- Define EXTRA_CPP_FLAGS again, after it was removed in the fix for 1146897.
- Resolves: rhbz#1146897

* Fri Feb 05 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-5.b15
- Backport S8148351: Only display resolved symlink for compiler, do not change path
- Resolves: rhbz#1256464

* Thu Feb 04 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-4.b15
- Resetting bootstrap after successful build.
- Resolves: rhbz#1146897

* Wed Feb 03 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-4.b15
- Remove -fno-tree-vectorize now a GCC is available with this bug fixed.
- Add build requirement on a GCC with working tree vectorization.
- Enable bootstrap temporarily to ensure the JDK is functional.
- Resolves: rhbz#1146897

* Thu Jan 21 2016 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.71-2.b15.el7_2

* Fri Jan 15 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-3.b15
- Add md5sum for previous java.security file so it gets updated.
- Resolves: rhbz#1295754

* Thu Jan 14 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-2.b15
- Restore upstream version of system LCMS patch removed by 'sync with Fedora'
- Add patch to turn off strict overflow on IndicRearrangementProcessor{,2}.cpp
- Resolves: rhbz#1295754

* Wed Jan 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- Change correct specifier in src/share/vm/gc_implementation/g1/g1StringDedupTable.cpp
- Resolves: rhbz#1295754
- Change correct specifier in src/share/vm/memory/blockOffsetTable.cpp
- Make bootstrap build optional and turn it off by default.
- Fix remaining warnings in s390 fix and re-enable -Werror
- Add additional fixes for s390 warnings in arguments.cpp
- Temporarily turn off -Werror on s390 to make progress
- Actually apply the S390 fix...
- Turn off additional CFLAGS/LDFLAGS on AArch64 as bootstrapping failed.
- Add patch for size_t formatting on s390 as size_t != intptr_t there.

* Tue Jan 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- October 2015 security update to u71b15.
- Improve verbosity and helpfulness of tarball generation script.
- Remove RH1290936 workaround as RHEL does not have the hardened flags nor ARM32.
- Update patch documentation using version originally written for Fedora.
- Drop prelink requirement as we no longer use execstack.
- Drop ifdefbugfix patch as this is fixed upstream.
- Temporarily enable a full bootcycle to ensure flag changes don't break anything.
- Resolves: rhbz#1295754

* Tue Jan 12 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.65-4.b17
- moved to integration forest
- sync with fedora (all but extracted luas and family)
- Resolves: rhbz#1295754

* Fri Nov 20 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.65-3.b17.el7

* Thu Oct 22 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.65-2.b17.el7_1

* Mon Oct 19 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.65-3.b17
- bumped release X.el7_1 is obviously > X.el7 :-/
- Resolves: rhbz#1257657

* Fri Oct 16 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.65-1.b17
- moved to bundled lcms
- Resolves: rhbz#1257657

* Thu Oct 15 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.65-0.b17
- October 2015 security update to u65b17.
- Add script for generating OpenJDK tarballs from a local Mercurial tree.
- Update RH1191652 patch to build against current AArch64 tree.
- Use appropriate source ID to avoid unpacking both tarballs on AArch64.
- Add MD5 checksums for java.security from 8u51 and 8u60 RPMs.
- Resolves: rhbz#1257657

* Wed Oct 14 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.60-6.b27
- removed link to soundfont. Unused in rhel7 and will be fixed upstream
- Resolves: rhbz#1257653

* Wed Sep 16 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.60-2.b27.el7_1

* Fri Sep 04 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.60-4.b27
- priority aligned to 7digits (sync with 6.8)
- Resolves: rhbz#1255350

* Fri Aug 28 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.60-2.b27
- updated to u60
- Resolves: rhbz#1255350

* Thu Jul 16 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.51-1.b16.el7_1

* Thu Jul 16 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.51-2.b16
- doubled slash in md5sum test in post
- Resolves: rhbz#1235163

* Fri Jul 03 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.51-1.b16
- Re-introduce handling of java.security updates, with new md5sum of Jan 2015 version.
- Resolves: rhbz#1235163

* Thu Jul 02 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.51-0.b16
- July 2015 security update to u51b16.
- Add script for generating OpenJDK tarballs from a local Mercurial tree.
- Add %%{name} prefix to patches to avoid conflicts with OpenJDK 7 versions.
- Add patches for RH issues fixed in IcedTea 2.x and/or the upcoming u60.
- Use 'openjdk' as directory prefix to allow patch interchange with IcedTea.
- Re-generate EC disablement patch following CPU DH changes.
- Resolves: rhbz#1235163

* Wed May 13 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.45-37.b13
- added build requires on tzdata
- Resolves: rhbz#1212571

* Wed May 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.45-36.b13
- Correctly fix system timezone data issue by depending on correct tzdata version.
- Remove reference to tz.properties which is no longer used.
- Resolves: rhbz#1212571

* Wed Apr 29 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.45-35.b13
- Make use of system timezone data for OpenJDK 8.
- moved to boot build by openjdk8
- priority set  gcj < lengthOffFour < otherJdks (RH1175457)
- misusing already fixed bug
- Resolves: rhbz#1189530

* Wed Apr 29 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.45-34.b13
- Omit jsa files from power64 file list as well, as they are never generated
- Resolves: rhbz#1202726

* Mon Apr 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.45-33.b13
- -Xshare:dump is not implemented for the PPC JIT port (both ppc64be & le)
- Resolves: rhbz#1202726

* Mon Apr 20 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.45-32.b13
- Use the template interpreter on ppc64le
- Resolves: rhbz#1213042

* Thu Apr 16 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.45-30.b13.el7_1

* Fri Apr 10 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.45-31.b13
- repacked sources
- Resolves: RHBZ#1209077

* Thu Apr 09 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.45-30.b13
- do not obsolete openjdk7
- Resolves: rhbz#1210006

* Tue Apr 07 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.45-28.b13
- Fix filenames broken by sync
- Resolves: rhbz#1209077

* Tue Apr 07 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.45-27.b13
- updated to security u45
- minor sync with 7.2
 - generate_source_tarball.sh
 - adapted java-1.8.0-openjdk-s390-java-opts.patch and java-1.8.0-openjdk-size_t.patch
 - reworked (synced) zero patches (removed 103,11 added 204, 400-403)
 - family of 5XX patches renamed to 6XX
 - added upstreamed patch 501 and 505
 - included removeSunEcProvider-RH1154143.patch
- returned java (jre only) provides
- repacked policies (source20)
- removed duplicated NVR provides
- added automated test for priority (length7)
- Resolves: RHBZ#1209077

* Wed Apr 1 2015 Sean Kelly <seankell@amazon.com>
- Use consistent alternatives path earlier java packages.

* Fri Mar 27 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.31-7.b13.el7_1

* Mon Mar 23 2015 Ethan Faust <efaust@amazon.com>
- use system-wide tzdata

* Wed Mar 18 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-7.b13
- Set archinstall to ppc64le on that platform.
- Resolves: rhbz#1194378

* Tue Mar 17 2015 Ben Cressey <bcressey@amazon.com>
- do not remove SunEC provider

* Fri Mar 13 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- import source package EL7/java-1.8.0-openjdk-1.8.0.31-2.b13.el7

* Wed Mar 11 2015 Amazon Linux AMI <amazon-linux-ami@amazon.com>
- setup complete for package java-1.8.0-openjdk

* Wed Mar 04 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-6.b13
- Adjust ppc64le HotSpot patch for OpenJDK 8.
- Enable AArch64 configure/JDK patch on all archs to minimise patching issues.
- Adjust ppc64le patches to apply after the enableAArch64 patch.
- Add %%{name} prefix to patches to avoid conflicts with OpenJDK 7 versions.
- Resolves: rhbz#1194378

* Tue Mar 03 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-5.b13
- Provide AArch64 version of RH1191652 HotSpot patch.
- Resolves: rhbz#1194378

* Wed Feb 18 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Actually add test case Java file.
- Resolves: rhbz#1194378
- Override ppc64le as ppc64 only in hotspot-spec.gmk so as not to disrupt JDK build.
- Add property test case from java-1.7.0-openjdk build.
- Set OPENJDK_TARGET_CPU_LEGACY to ppc64 so as not to mess up HotSpot build.
- Add -DABI_ELFv2 to CFLAGS on ppc64le to match OpenJDK 7.
- Print contents of hotspot-spec.gmk
- Fix path to spec.gmk.

* Tue Feb 17 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Print contents of spec.gmk to see what is being passed to the HotSpot build.
- Resolves: rhbz#1194378
- Remove patch to generated-configure.sh as RPM re-generates it.
- Fix configure script to use ppc64le, not ppc64.
- Add ppc64le support to LIBJSOUND_CFLAGS.
- Add a jvm.cfg for ppc64le
- Report ppc64le as the architecture on ppc64le, not ppc64.

* Tue Jan 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-3.b13
- Depend on java-1.7.0-openjdk to build instead.
- Resolves: rhbz#1194378

* Wed Jan 21 2015 hpetty <hpetty@amazon.com>
- import source package F21/java-1.8.0-openjdk-1.8.0.31-2.b13.fc21
- import source package F21/java-1.8.0-openjdk-1.8.0.25-5.b18.fc21
- import source package F21/java-1.8.0-openjdk-1.8.0.25-4.b18.fc21
- import source package F21/java-1.8.0-openjdk-1.8.0.25-2.b18.fc21

* Fri Jan 16 2015 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.31-2.b13
- Replace unmodified java.security file via headless post scriptlet.
- Resolves: RHBZ#1180301

* Fri Jan 09 2015 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.31-1.b13
- Update to January CPU patch update.
- Resolves: RHBZ#1180301

* Wed Dec 17 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.25-5.b17
- epoch synced to 1
- Resolves: rhbz#1125260

* Fri Oct 24 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.25-4.b17
- updated aarch64 sources
- all ppcs excluded from classes dump(1156151)
- Resolves: rhbz#1125260

* Fri Oct 24 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.25-3.b17
- added patch12,removeSunEcProvider-RH1154143
- xdump excluded from ppc64le (rh1156151)
- Add check for src.zip completeness. See RH1130490 (by sgehwolf@redhat.com)
- Resolves: rhbz#1125260

* Wed Oct 22 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.25-3.b17
- Do not provide JPackage java-* provides. (see RH1155783)
- Resolves: rhbz#1155786

* Mon Oct 20 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.25-2.b17
- ec/impl removed from source tarball
- Resolves: rhbz#1125260

* Thu Oct 16 2014 Lee Trager <ltrager@amazon.com>
- import source package F21/java-1.8.0-openjdk-1.8.0.25-0.b18.fc21

* Mon Oct 06 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.25-1.b17
- Update to October CPU patch update.

* Thu Sep 25 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.20-11.b26
- Fix rpmlint warnings about vectoriesed ppcs
- Resolves: rhbz#1125260

* Thu Sep 25 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.20-10.b26
- Remove LIBDIR and funny definition of _libdir.
- Fix rpmlint warnings about macros in comments.
- Resolves: rhbz#1125260

* Mon Sep 22 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.20-10.b26
- BR changed to java-1.8.0-openjdk in order to verify build by itself.
- Resolves: rhbz#1125260

* Mon Sep 22 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.20-9.b26
- Add hotspot compiler flag -fno-tree-vectorize which fixes the segfault in
  the bytecode verifier on ppc/ppc64.
- Resolves: rhbz#1125260

* Fri Sep 19 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.20-8.b26
- Add patches for PPC zero build.
- Fixes stack overflow problem. See RHBZ#1015432.
- Fixes missing memory barrier in Atomic::xchg*
- Fixes missing PPC32/PPC64 defines for Zero builds on power.
- Resolves: rhbz#1125260

* Wed Sep 17 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.20-7.b26
- Remove ppc/64 patches.
- Build with java-1.7.0-openjdk.
- Resolves: rhbz#1125260

* Wed Sep 10 2014 Lee Trager <ltrager@amazon.com>
- Flip bootstrap bit
- Build for Amazon Linux

* Wed Sep 10 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.20-6.b26
- Revert to building against java-1.8.0-openjdk
- Resolves: rhbz#1125260

* Wed Sep 10 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.20-5.b26
- Update aarch64 hotspot to latest upstream version
- Depend on java-1.7.0-openjdk to work around self-building issues
- Resolves: rhbz#1125260

* Mon Sep 08 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.20-4.b26
- forcing build by itself (jdk8 by jdk8)
- Resolves: rhbz#1125260

* Fri Sep 5 2014 Lee Trager <ltrager@amazon.com>
- import source package F21/java-1.8.0-openjdk-1.8.0.20-4.b26.fc21
- setup complete for package java-1.8.0-openjdk

* Fri Sep 05 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.20-3.b26
- Update aarch64 hotspot to latest version
- Resolves: rhbz#1125260

* Fri Sep 05 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.20-2.b26
- Enable jit for all ppc64 variants
- Resolves: rhbz#1125260

* Fri Sep 05 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.20-2.b26
- moving all ppc64 to jit arches
- using cpp interpreter for ppc64le
- removing requirement on datadir/javazi-1.8/tzdb.dat
- Resolves: rhbz#1125260

* Fri Sep 05 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.20-1.b26
- Switch back to 8u20
- Build using java-1.7.0-openjdk
- Resolves: rhbz#1125260

* Thu Sep 04 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.40-5.b26
- Update aarch64 hotspot to jdk7u40-b02 to match the rest of the JDK
- Do not obsolete java-1.7.0-openjdk
- Resolves: rhbz#1125260

* Wed Sep 03 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.20-4.b26
- forcing build by itself (jdk8 by jdk8)
- Resolves: rhbz#1125260

* Wed Sep 03 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.20-3.b26
- fixed RH1136544, orriginal issue, state of pc64le jit remians mistery
- Resolves: rhbz#1125260

* Thu Aug 28 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.40-1.b02
- adapted aarch64 patch
- removed upstreamed patch  0001-PPC64LE-arch-support-in-openjdk-1.8.patch
- added patch666 stackoverflow-ppc32_64-20140828.patch
- commented out patch2 1015432.patch (does nearly the same as new patch666)
- Resolves: rhbz#1125260

* Wed Aug 27 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.40-1.b02
- updated to u40-b02
- adapted aarch64 patches

* Wed Aug 27 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.40-1.b01
- updated to u40-b01
- adapted  rh1648242-accessible_toolkit_crash_do_not_break_jvm.patch
- adapted  jdk8042159-allow_using_system_installed_lcms2.patch
- removed patch8 set-active-window.patch
- removed patch9 javadoc-error-jdk-8029145.patch
- removed patch10 javadoc-error-jdk-8037484.patch
- removed patch99 applet-hole.patch - itw 1.5.1 is able to ive without it

* Tue Aug 19 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-19.b12
- fixed desktop icons
- Icon set to java-1.8.0
- Development removed from policy tool

* Mon Aug 18 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-18.b12
- fixed jstack

* Mon Aug 18 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-17.b12
- added build requires and requires for headles  _datadir/javazi-1.8/tzdb.dat
- restriction of tzdata provider, so we will be aware of another possible failure

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-15.b12
- fixed provides/obsolates

* Tue Aug 12 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-14.b12
- forced to build in fully versioned dir

* Tue Aug 12 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-13.b12
- fixing tapset to support multipleinstalls
- added more config/norepalce
- policitool moved to jre

* Tue Aug 12 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-12.b12
- bumped release to build by previous release.
- forcing rebuild by jdk8
- uncommenting forgotten comment on tzdb link

* Tue Aug 12 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-11.b12
- backporting old fixes:
- get rid of jre-abrt, uniquesuffix, parallel install, jsa files,
  config(norepalce) bug, -fstack-protector-strong, OrderWithRequires,
  nss config, multilib arches, provides/requires excludes
- some additional cosmetic changes

* Tue Jul 22 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.11-8.b12
- Modify aarch64-specific jvm.cfg to list server vm first

* Mon Jul 21 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-7.b12
- removed legacy aarch64 switches
 - --with-jvm-variants=client and  --disable-precompiled-headers

* Tue Jul 15 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-6.b12
- added patch patch9999 enableArm64.patch to enable new hotspot

* Tue Jul 15 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-5.b12
- Attempt to update aarch64 *jdk* to u11b12, by resticting aarch64 sources to hotpot only

* Tue Jul 15 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.11-1.b12
- updated to security u11b12

* Tue Jun 24 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-13.b13
- Obsolete java-1.7.0-openjdk

* Wed Jun 18 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-12.b13
- Use system tzdata from tzdata-java

* Thu Jun 12 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-11.b13
- Add patch from IcedTea to handle -j and -I correctly

* Wed Jun 11 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-11.b13
- Backport javadoc fixes from upstream
- Related: rhbz#1107273

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.0.5-10.b13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-9.b13
- Build with OpenJDK 8

* Wed May 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-8.b13
- Backport fix for JDK-8012224

* Wed May 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-7.b13
- Require fontconfig and minimal fonts (xorg-x11-fonts-Type1) explicitly
- Resolves rhbz#1101394

* Fri May 23 2014 Dan Horák <dan[at]danny.cz> - 1:1.8.0.5-6.b13
- Enable build on s390/s390x

* Tue May 20 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-5.b13
- Only check for debug symbols in libjvm if it exists.

* Fri May 16 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-4.b13
- Include all sources in src.zip

* Mon Apr 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-4.b13
- Check for debug symbols in libjvm.so

* Thu Apr 24 2014 Brent Baude <baude@us.ibm.com> - 1:1.8.0.5-3.b13
- Add ppc64le support, bz# 1088344

* Wed Apr 23 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-2.b13
- Build with -fno-devirtualize
- Don't strip debuginfo from files

* Wed Apr 16 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-1.b13
- Instrument build with various sanitizers.

* Tue Apr 15 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.5-1.b13
- Update to the latest security release: OpenJDK8 u5 b13

* Fri Mar 28 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-2.b132
- Include version information in desktop files
- Move desktop files from tarball to top level source

* Tue Mar 25 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-1.0.b132
- Switch from java8- style provides to java- style
- Bump priority to reflect java version

* Fri Mar 21 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.35.b132
- Disable doclint for compatiblity
- Patch contributed by Andrew John Hughes

* Tue Mar 11 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.34.b132
- Include jdeps and jjs for aarch64. These are present in b128.

* Mon Mar 10 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.33.b132
- Update aarch64 tarball to the latest upstream release

* Fri Mar 07 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.32.b132
- Fix `java -version` output

* Fri Mar 07 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.31.b132
- updated to rc4 aarch64 tarball
- outdated removed: patch2031 system-lcmsAARCH64.patch patch2011 system-libjpeg-aarch64.patch
  patch2021 system-libpng-aarch64.patch

* Thu Mar 06 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.30.b132
- Update to b132

* Thu Mar 06 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.29.b129
- Fix typo in STRIP_POLICY

* Mon Mar 03 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.28.b129
- Remove redundant debuginfo files
- Generate complete debug information for libjvm

* Tue Feb 25 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.27.b129
- Fix non-headless libraries

* Tue Feb 25 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.26.b129
- Fix incorrect Requires

* Thu Feb 13 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.26.b129
- Add -headless subpackage based on java-1.7.0-openjdk
- Add abrt connector support
- Add -accessibility subpackage
- Update to b129.

* Fri Feb 07 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.25.b126
- Update to candidate Reference Implementation release.

* Fri Jan 31 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.24.b123
- Forward port more patches from java-1.7.0-openjdk

* Mon Jan 20 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.23.b123
- Update to jdk8-b123

* Thu Nov 14 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.22.b115
- Update to jdk8-b115

* Wed Oct 30 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.21.b106
- added jre/lib/security/blacklisted.certs for aarch64
- updated to preview_rc2 aarch64 tarball

* Sun Oct 06 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.20.b106
- Fix paths in tapsets to work on non-x86_64
- Use system libjpeg

* Thu Sep 05 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.19.b106
- Fix with_systemtap conditionals

* Thu Sep 05 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.18.b106
- Update to jdk8-b106

* Tue Aug 13 2013 Deepak Bhole <dbhole@redhat.com> - 1:1.8.0.0-0.17.b89x
- Updated aarch64 to latest head
- Dropped upstreamed patches

* Wed Aug 07 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.16.b89x
- The zero fix only applies on b89 tarball

* Tue Aug 06 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.16.b89x
- Add patch to fix zero on 32-bit build

* Mon Aug 05 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.16.b89x
- Added additional build fixes for aarch64

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.0.0-0.16.b89x
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Deepak Bhole <dbhole@redhat.com> - 1:1.8.0.0-0.15.b89
- Added a missing includes patch (#302/%%{name}-arm64-missing-includes.patch)
- Added --disable-precompiled-headers for arm64 build

* Mon Jul 29 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.14.b89
- added patch 301 - removeMswitchesFromx11.patch

* Fri Jul 26 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.13.b89
- added new aarch64 tarball

* Thu Jul 25 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.12.b89
- ifarchaarch64 then --with-jvm-variants=client

* Tue Jul 23 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.11.b89
- prelink dependence excluded also for aaech64
- arm64 added to jitarches
- added source100 config.guess to repalce the outdated one in-tree
- added source101 config.sub  to repalce the outdated one in-tree
- added patch2011 system-libjpegAARCH64.patch (as aarch64-port is little bit diferent)
- added patch2031 system-lcmsAARCH64.patch (as aarch64-port is little bit diferent)
- added gcc-c++ build depndece so builddep will  result to better situation

* Tue Jul 23 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.10.b89
- moved to latest working osurces

* Tue Jul 23 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.10.b89
- Moved  to hg clone for generating sources.

* Sun Jul 21 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.0-0.9.b89
- added aarch 64 tarball, proposed usage of clone instead of tarballs

* Mon Jul 15 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.9.b89
- Switch to xz for compression
- Fixes RHBZ#979823
- Priority should be 0 until openjdk8 is released by upstream
- Fixes RHBZ#964409

* Mon Jun 3 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.8.b89
- Fix incorrect permissions on ct.sym

* Mon May 20 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.7.b89
- Fix incorrect permissions on jars

* Fri May 10 2013 Adam Williamson <awilliam@redhat.com>
- update scriptlets to follow current guidelines for updating icon cache

* Tue Apr 30 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.5.b87
- Update to b87
- Remove all rhino support; use nashorn instead
- Remove upstreamed/unapplied patches

* Tue Apr 23 2013 Karsten Hopp <karsten@redhat.com> 1:1.8.0.0-0.4.b79
- update java-1.8.0-openjdk-ppc-zero-hotspot patch
- use power64 macro

* Thu Mar 28 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.3.b79
- Add build fix for zero
- Drop gstabs fixes; enable full debug info instead

* Wed Mar 13 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.2.b79
- Fix alternatives priority

* Tue Mar 12 2013 Omair Majid <omajid@redhat.com> 1:1.8.0.0-0.1.b79.f19
- Update to jdk8-b79
- Initial version for Fedora 19

* Tue Sep 04 2012 Andrew John Hughes <gnu.andrew@redhat.com> - 1:1.8.0.0-b53.1
- Initial build from java-1.7.0-openjdk RPM
