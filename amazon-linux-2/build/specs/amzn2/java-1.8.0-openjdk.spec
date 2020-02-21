%define _trivial .0
%define _buildid .1

# The -g flag says to use strip -g instead of full strip on DSOs or EXEs.
# This fixes detailed NMT and other tools which need minimal debug info.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1520879
%global _find_debuginfo_opts -g

# note: parametrized macros are order-sensitive (unlike not-parametrized) even with normal macros
# also necessary when passing it as parameter to other macros. If not macro, then it is considered a switch
%global debug_suffix_unquoted -debug
# quoted one for shell operations
%global debug_suffix "%{debug_suffix_unquoted}"
%global normal_suffix ""

# if you want only debug build but providing java build only normal build but set normalbuild_parameter
%global debugbuild_parameter  slowdebug
%global normalbuild_parameter release
%global debug_warning This package has full debug on. Install only in need and remove asap.
%global debug_on with full debug on
%global for_debug for packages with debug on

# by default we build normal build always.
%global include_normal_build 1
%if %{include_normal_build}
%global build_loop1 %{normal_suffix}
%else
%global build_loop1 %{nil}
%endif

%global aarch64         aarch64 arm64 armv8
# we need to distinguish between big and little endian PPC64
%global ppc64le         ppc64le
%global ppc64be         ppc64 ppc64p7
%global multilib_arches %{power64} sparc64 x86_64
%global jit_arches      %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64}

# By default, we build a debug build during main build on JIT architectures
%ifarch %{jit_arches}
%global include_debug_build 1
%else
%global include_debug_build 0
%endif

%if %{include_debug_build}
%global build_loop2 %{debug_suffix}
%else
%global build_loop2 %{nil}
%endif

# if you disable both builds, then the build fails
# Note that the debug build requires the normal build for docs
%global build_loop  %{build_loop1} %{build_loop2}
# note: that order: normal_suffix debug_suffix, in case of both enabled
# is expected in one single case at the end of the build
%global rev_build_loop  %{build_loop2} %{build_loop1}

%ifarch %{jit_arches}
%global bootstrap_build 1
%else
%global bootstrap_build 1
%endif

%if %{bootstrap_build}
%global release_targets bootcycle-images zip-docs
%else
%global release_targets images zip-docs
%endif
# No docs nor bootcycle for debug builds
%global debug_targets images

# Filter out flags from the optflags macro that cause problems with the OpenJDK build
# We filter out -Wall which will otherwise cause HotSpot to produce hundreds of thousands of warnings (100+mb logs)
# We filter out -O flags so that the optimization of HotSpot is not lowered from O3 to O2
# We replace it with -Wformat (required by -Werror=format-security) and -Wno-cpp to avoid FORTIFY_SOURCE warnings
# We filter out -fexceptions as the HotSpot build explicitly does -fno-exceptions and it's otherwise the default for C++
%global ourflags %(echo %optflags | sed -e 's|-Wall|-Wformat -Wno-cpp|' | sed -r -e 's|-O[0-9]*||')
%global ourcppflags %(echo %ourflags | sed -e 's|-fexceptions||')
%global ourldflags %{__global_ldflags}

# With disabled nss is NSS deactivated, so NSS_LIBDIR can contain the wrong path
# the initialization must be here. Later the pkg-config have buggy behavior
# looks like openjdk RPM specific bug
# Always set this so the nss.cfg file is not broken
%global NSS_LIBDIR %(pkg-config --variable=libdir nss)
%global NSS_LIBS %(pkg-config --libs nss)
%global NSS_CFLAGS %(pkg-config --cflags nss-softokn)
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332456
%global NSSSOFTOKN_BUILDTIME_NUMBER %(pkg-config --modversion nss-softokn || : )
%global NSS_BUILDTIME_NUMBER %(pkg-config --modversion nss || : )
# this is workaround for processing of requires during srpm creation
%global NSSSOFTOKN_BUILDTIME_VERSION %(if [ "x%{NSSSOFTOKN_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSSSOFTOKN_BUILDTIME_NUMBER}" ;fi)
%global NSS_BUILDTIME_VERSION %(if [ "x%{NSS_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSS_BUILDTIME_NUMBER}" ;fi)


# Fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349.
# See also https://bugzilla.redhat.com/show_bug.cgi?id=1590796
# as to why some libraries *cannot* be excluded. In particular,
# these are:
# libjsig.so, libjava.so, libjawt.so, libjvm.so and libverify.so
%global _privatelibs libatk-wrapper[.]so.*|libattach[.]so.*|libawt_headless[.]so.*|libawt[.]so.*|libawt_xawt[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libhprof[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas_unix[.]so.*|libjava_crw_demo[.]so.*|libjavajpeg[.]so.*|libjdwp[.]so.*|libjli[.]so.*|libjsdt[.]so.*|libjsoundalsa[.]so.*|libjsound[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libnpt[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsplashscreen[.]so.*|libsunec[.]so.*|libunpack[.]so.*|libzip[.]so.*|lib[.]so\\(SUNWprivate_.*

%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

# In some cases, the arch used by the JDK does
# not match _arch.
# Also, in some cases, the machine name used by SystemTap
# does not match that given by _build_cpu
%ifarch x86_64
%global archinstall amd64
%global stapinstall x86_64
%endif
%ifarch ppc
%global archinstall ppc
%global stapinstall powerpc
%endif
%ifarch %{ppc64be}
%global archinstall ppc64
%global stapinstall powerpc
%endif
%ifarch %{ppc64le}
%global archinstall ppc64le
%global stapinstall powerpc
%endif
%ifarch %{ix86}
%global archinstall i386
%global stapinstall i386
%endif
%ifarch ia64
%global archinstall ia64
%global stapinstall ia64
%endif
%ifarch s390
%global archinstall s390
%global stapinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%global stapinstall s390
%endif
%ifarch %{arm}
%global archinstall arm
%global stapinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%global stapinstall arm64
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%global stapinstall %{_build_cpu}
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%global stapinstall %{_build_cpu}
%endif
%ifnarch %{jit_arches}
%global archinstall %{_arch}
%endif

%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

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
%global shenandoah_revision    	aarch64-shenandoah-jdk8u242-b08
# Define old aarch64/jdk8u tree variables for compatibility
%global project         %{shenandoah_project}
%global repo            %{shenandoah_repo}
%global revision        %{shenandoah_revision}
# Define IcedTea version used for SystemTap tapsets and desktop files
%global icedteaver      3.11.0

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
# priority must be 7 digits in total. The expression is workarounding tip
%global priority        %(TIP=1800%{updatever};  echo ${TIP/tip/999})

%global javaver         1.%{majorver}.0

# parametrized macros are order-sensitive
%global compatiblename  %{name}
%global fullversion     %{compatiblename}-%{version}-%{release}
# images stub
%global jdkimage       j2sdk-image
# output dir stub
%global buildoutputdir() %{expand:%{top_level_dir_name}/build/jdk8.build%1}
#we can copy the javadoc to not arched dir, or make it not noarch
%global uniquejavadocdir()    %{expand:%{fullversion}%1}
#main id and dir of this jdk
%global uniquesuffix()        %{expand:%{fullversion}.%{_arch}%1}

# Standard JPackage directories and symbolic links.
%global sdkdir()        %{expand:%{uniquesuffix %%1}}
%global jrelnk()        %{expand:jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}%1}

%global jredir()        %{expand:%{sdkdir %%1}/jre}
%global sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir %%1}/bin}
%global jrebindir()     %{expand:%{_jvmdir}/%{jredir %%1}/bin}
%global jvmjardir()     %{expand:%{_jvmjardir}/%{uniquesuffix %%1}}

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific sub-dir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinguish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{stapinstall}
%endif

# not-duplicated scriptlets for normal/debug packages
%global update_desktop_icons /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%global post_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0
}


%global post_headless() %{expand:
%ifarch %{jit_arches}
# MetaspaceShared::generate_vtable_methods not implemented for PPC JIT
%ifnarch %{power64}
#see https://bugzilla.redhat.com/show_bug.cgi?id=513605
%{jrebindir %%1}/java -Xshare:dump >/dev/null 2>/dev/null
%endif
%endif

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
alternatives \\
  --install %{_bindir}/java java %{jrebindir %%1}/java $PRIORITY  --family %{name}.%{_arch} \\
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jredir %%1} \\
  --slave %{_jvmjardir}/jre jre_exports %{_jvmjardir}/%{jrelnk %%1} \\
  --slave %{_bindir}/jjs jjs %{jrebindir %%1}/jjs \\
  --slave %{_bindir}/keytool keytool %{jrebindir %%1}/keytool \\
  --slave %{_bindir}/orbd orbd %{jrebindir %%1}/orbd \\
  --slave %{_bindir}/pack200 pack200 %{jrebindir %%1}/pack200 \\
  --slave %{_bindir}/rmid rmid %{jrebindir %%1}/rmid \\
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir %%1}/rmiregistry \\
  --slave %{_bindir}/servertool servertool %{jrebindir %%1}/servertool \\
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir %%1}/tnameserv \\
  --slave %{_bindir}/policytool policytool %{jrebindir %%1}/policytool \\
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir %%1}/unpack200 \\
  --slave %{_mandir}/man1/java.1$ext java.1$ext \\
  %{_mandir}/man1/java-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jjs.1$ext jjs.1$ext \\
  %{_mandir}/man1/jjs-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \\
  %{_mandir}/man1/keytool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \\
  %{_mandir}/man1/orbd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \\
  %{_mandir}/man1/pack200-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \\
  %{_mandir}/man1/rmid-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \\
  %{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \\
  %{_mandir}/man1/servertool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \\
  %{_mandir}/man1/tnameserv-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \\
  %{_mandir}/man1/policytool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \\
  %{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1$ext

for X in %{origin} %{javaver} ; do
  alternatives \\
    --install %{_jvmdir}/jre-"$X" \\
    jre_"$X" %{_jvmdir}/%{jredir %%1} $PRIORITY --family %{name}.%{_arch} \\
    --slave %{_jvmjardir}/jre-"$X" \\
    jre_"$X"_exports %{_jvmdir}/%{jredir %%1}
done

update-alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk %%1} $PRIORITY  --family %{name}.%{_arch} \\
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_%{origin}_exports      %{jvmjardir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

# see pretrans where this file is declared
# also see that pretrans is only for non-debug
if [ ! "%1" == %{debug_suffix} ]; then
  if [ -f %{_libexecdir}/copy_jdk_configs_fixFiles.sh ] ; then
    sh  %{_libexecdir}/copy_jdk_configs_fixFiles.sh %{rpm_state_dir}/%{name}.%{_arch}  %{_jvmdir}/%{sdkdir %%1}
  fi
fi

exit 0
}

%global postun_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}


%global postun_headless() %{expand:
  alternatives --remove java %{jrebindir %%1}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jredir %%1}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jredir %%1}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk %%1}
}

%global posttrans_script() %{expand:
%{update_desktop_icons}
}

%global post_devel() %{expand:

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
alternatives \\
  --install %{_bindir}/javac javac %{sdkbindir %%1}/javac $PRIORITY  --family %{name}.%{_arch} \\
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir %%1} \\
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdkdir %%1} \\
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir %%1}/appletviewer \\
  --slave %{_bindir}/extcheck extcheck %{sdkbindir %%1}/extcheck \\
  --slave %{_bindir}/idlj idlj %{sdkbindir %%1}/idlj \\
  --slave %{_bindir}/jar jar %{sdkbindir %%1}/jar \\
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir %%1}/jarsigner \\
  --slave %{_bindir}/javadoc javadoc %{sdkbindir %%1}/javadoc \\
  --slave %{_bindir}/javah javah %{sdkbindir %%1}/javah \\
  --slave %{_bindir}/javap javap %{sdkbindir %%1}/javap \\
  --slave %{_bindir}/jcmd jcmd %{sdkbindir %%1}/jcmd \\
  --slave %{_bindir}/jconsole jconsole %{sdkbindir %%1}/jconsole \\
  --slave %{_bindir}/jdb jdb %{sdkbindir %%1}/jdb \\
  --slave %{_bindir}/jdeps jdeps %{sdkbindir %%1}/jdeps \\
  --slave %{_bindir}/jhat jhat %{sdkbindir %%1}/jhat \\
  --slave %{_bindir}/jinfo jinfo %{sdkbindir %%1}/jinfo \\
  --slave %{_bindir}/jmap jmap %{sdkbindir %%1}/jmap \\
  --slave %{_bindir}/jps jps %{sdkbindir %%1}/jps \\
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir %%1}/jrunscript \\
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir %%1}/jsadebugd \\
  --slave %{_bindir}/jstack jstack %{sdkbindir %%1}/jstack \\
  --slave %{_bindir}/jstat jstat %{sdkbindir %%1}/jstat \\
  --slave %{_bindir}/jstatd jstatd %{sdkbindir %%1}/jstatd \\
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir %%1}/native2ascii \\
  --slave %{_bindir}/rmic rmic %{sdkbindir %%1}/rmic \\
  --slave %{_bindir}/schemagen schemagen %{sdkbindir %%1}/schemagen \\
  --slave %{_bindir}/serialver serialver %{sdkbindir %%1}/serialver \\
  --slave %{_bindir}/wsgen wsgen %{sdkbindir %%1}/wsgen \\
  --slave %{_bindir}/wsimport wsimport %{sdkbindir %%1}/wsimport \\
  --slave %{_bindir}/xjc xjc %{sdkbindir %%1}/xjc \\
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \\
  %{_mandir}/man1/appletviewer-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \\
  %{_mandir}/man1/extcheck-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/idlj.1$ext idlj.1$ext \\
  %{_mandir}/man1/idlj-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \\
  %{_mandir}/man1/jar-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \\
  %{_mandir}/man1/jarsigner-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \\
  %{_mandir}/man1/javac-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \\
  %{_mandir}/man1/javadoc-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \\
  %{_mandir}/man1/javah-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \\
  %{_mandir}/man1/javap-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jcmd.1$ext jcmd.1$ext \\
  %{_mandir}/man1/jcmd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \\
  %{_mandir}/man1/jconsole-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \\
  %{_mandir}/man1/jdb-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jdeps.1$ext jdeps.1$ext \\
  %{_mandir}/man1/jdeps-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \\
  %{_mandir}/man1/jhat-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \\
  %{_mandir}/man1/jinfo-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \\
  %{_mandir}/man1/jmap-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \\
  %{_mandir}/man1/jps-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \\
  %{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \\
  %{_mandir}/man1/jsadebugd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \\
  %{_mandir}/man1/jstack-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \\
  %{_mandir}/man1/jstat-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \\
  %{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \\
  %{_mandir}/man1/native2ascii-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \\
  %{_mandir}/man1/rmic-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \\
  %{_mandir}/man1/schemagen-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \\
  %{_mandir}/man1/serialver-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \\
  %{_mandir}/man1/wsgen-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \\
  %{_mandir}/man1/wsimport-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \\
  %{_mandir}/man1/xjc-%{uniquesuffix %%1}.1$ext

for X in %{origin} %{javaver} ; do
  alternatives \\
    --install %{_jvmdir}/java-"$X" \\
    java_sdk_"$X" %{_jvmdir}/%{sdkdir %%1} $PRIORITY  --family %{name}.%{_arch} \\
    --slave %{_jvmjardir}/java-"$X" \\
    java_sdk_"$X"_exports %{_jvmjardir}/%{sdkdir %%1}
done

update-alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir %%1} $PRIORITY  --family %{name}.%{_arch} \\
--slave %{_jvmjardir}/java-%{javaver}-%{origin}       java_sdk_%{javaver}_%{origin}_exports      %{_jvmjardir}/%{sdkdir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0
}

%global postun_devel() %{expand:
  alternatives --remove javac %{sdkbindir %%1}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}

%global posttrans_devel() %{expand:
%{update_desktop_icons}
}

%global post_javadoc() %{expand:

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

alternatives \\
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir %%1}/api \\
  $PRIORITY  --family %{name}
exit 0
}

%global postun_javadoc() %{expand:
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir %%1}/api
exit 0
}

%global post_javadoc_zip() %{expand:

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

alternatives \\
  --install %{_javadocdir}/java-zip javadoczip %{_javadocdir}/%{uniquejavadocdir %%1}.zip \\
  $PRIORITY  --family %{name}
exit 0
}

%global postun_javadoc_zip() %{expand:
  alternatives --remove javadoczip %{_javadocdir}/%{uniquejavadocdir %%1}.zip
exit 0
}

%global files_jre() %{expand:
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}-%{origin}.png
%{_datadir}/applications/*policytool%1.desktop
}


%global files_jre_headless() %{expand:
%defattr(-,root,root,-)
%doc %{buildoutputdir %%1}/images/%{jdkimage}/jre/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir %%1}/images/%{jdkimage}/jre/LICENSE
%doc %{buildoutputdir %%1}/images/%{jdkimage}/jre/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir %%1}
%{_jvmdir}/%{jrelnk %%1}
%{_jvmjardir}/%{jrelnk %%1}
%{_jvmprivdir}/*
%{jvmjardir %%1}
%dir %{_jvmdir}/%{jredir %%1}/lib/security
%{_jvmdir}/%{jredir %%1}/lib/security/cacerts
%dir %{_jvmdir}/%{jredir %%1}/lib/security/policy/unlimited/
%dir %{_jvmdir}/%{jredir %%1}/lib/security/policy/limited/
%dir %{_jvmdir}/%{jredir %%1}/lib/security/policy/
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/policy/unlimited/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/policy/unlimited/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/policy/limited/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/policy/limited/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/blacklisted.certs
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/logging.properties
%{_mandir}/man1/java-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jjs-%{uniquesuffix %%1}.1*
%{_mandir}/man1/keytool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/orbd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/pack200-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmid-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1*
%{_mandir}/man1/servertool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/tnameserv-%{uniquesuffix %%1}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1*
%{_mandir}/man1/policytool-%{uniquesuffix %%1}.1*
%config(noreplace) %{_jvmdir}/%{jredir %%1}/lib/security/nss.cfg
%ifarch %{jit_arches}
%ifnarch %{power64}
%attr(444, root, root) %ghost %{_jvmdir}/%{jredir %%1}/lib/%{archinstall}/server/classes.jsa
%attr(444, root, root) %ghost %{_jvmdir}/%{jredir %%1}/lib/%{archinstall}/client/classes.jsa
%endif
%endif
%{_jvmdir}/%{jredir %%1}/lib/%{archinstall}/server/
%{_jvmdir}/%{jredir %%1}/lib/%{archinstall}/client/
}

%global files_devel() %{expand:
%defattr(-,root,root,-)
%doc %{buildoutputdir %%1}/images/%{jdkimage}/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir %%1}/images/%{jdkimage}/LICENSE
%doc %{buildoutputdir %%1}/images/%{jdkimage}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir %%1}/bin
%dir %{_jvmdir}/%{sdkdir %%1}/include
%dir %{_jvmdir}/%{sdkdir %%1}/lib
%{_jvmdir}/%{sdkdir %%1}/bin/*
%{_jvmdir}/%{sdkdir %%1}/include/*
%{_jvmdir}/%{sdkdir %%1}/lib/*
%{_jvmjardir}/%{sdkdir %%1}
%{_datadir}/applications/*jconsole%1.desktop
%{_mandir}/man1/appletviewer-%{uniquesuffix %%1}.1*
%{_mandir}/man1/extcheck-%{uniquesuffix %%1}.1*
%{_mandir}/man1/idlj-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jar-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javac-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javah-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javap-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jdb-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jdeps-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jhat-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jmap-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jps-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jsadebugd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstack-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstat-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/native2ascii-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmic-%{uniquesuffix %%1}.1*
%{_mandir}/man1/schemagen-%{uniquesuffix %%1}.1*
%{_mandir}/man1/serialver-%{uniquesuffix %%1}.1*
%{_mandir}/man1/wsgen-%{uniquesuffix %%1}.1*
%{_mandir}/man1/wsimport-%{uniquesuffix %%1}.1*
%{_mandir}/man1/xjc-%{uniquesuffix %%1}.1*
%if %{with_systemtap}
%dir %{tapsetroot}
%dir %{tapsetdir}
%{tapsetdir}/*%{version}-%{release}.%{_arch}%1.stp
%dir %{_jvmdir}/%{sdkdir %%1}/tapset
%{_jvmdir}/%{sdkdir %%1}/tapset/*.stp
%endif
}

%global files_demo() %{expand:
%defattr(-,root,root,-)
%doc %{buildoutputdir %%1}/images/%{jdkimage}/jre/LICENSE
}

%global files_src() %{expand:
%defattr(-,root,root,-)
%doc README.md
%{_jvmdir}/%{sdkdir %%1}/src.zip
}

%global files_javadoc() %{expand:
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir %%1}
%doc %{buildoutputdir %%1}/images/%{jdkimage}/jre/LICENSE
}

%global files_javadoc_zip() %{expand:
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir %%1}.zip
%doc %{buildoutputdir %%1}/images/%{jdkimage}/jre/LICENSE
}

%global files_accessibility() %{expand:
%{_jvmdir}/%{jredir %%1}/lib/%{archinstall}/libatk-wrapper.so
%{_jvmdir}/%{jredir %%1}/lib/ext/java-atk-wrapper.jar
%{_jvmdir}/%{jredir %%1}/lib/accessibility.properties
}

# not-duplicated requires/provides/obsolate for normal/debug packages
%global java_rpo() %{expand:
Requires: fontconfig%{?_isa}
Requires: xorg-x11-fonts-Type1
# Require libXcomposite explicitly since it's only dynamically loaded
# at runtime. Fixes screenshot issues. See JDK-8150954.
Requires: libXcomposite%{?_isa}
# Requires rest of java
Requires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
# for java-X-openjdk package's desktop binding
Requires: gtk2%{?_isa}

Provides: java-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}

# Standard JPackage base provides.
Provides: jre = %{javaver}%1
Provides: jre-%{origin}%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-%{origin}%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}%1 = %{epoch}:%{version}-%{release}
Provides: java-%{origin}%1 = %{epoch}:%{version}-%{release}
Provides: java%1 = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: java-fonts%1 = %{epoch}:%{version}

#Obsoletes: java-1.7.0-openjdk%1
Obsoletes: java-1.5.0-gcj%1
Obsoletes: sinjdoc
}

%global java_headless_rpo() %{expand:
# Require /etc/pki/java/cacerts
Requires: ca-certificates
# Require jpackage-utils for ownership of /usr/lib/jvm/
Requires: jpackage-utils
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java >= 2015d
# libsctp.so.1 is being `dlopen`ed on demand
Requires: lksctp-tools%{?_isa}
# tool to copy jdk's configs - should be Recommends only, but then only dnf/yum enforce it,
# not rpm transaction and so no configs are persisted when pure rpm -u is run. It may be
# considered as regression
Requires: copy-jdk-configs >= 3.3
OrderWithRequires: copy-jdk-configs
# Post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7
# for optional support of kernel stream control, card reader and printing bindings
Requires: lksctp-tools%{?_isa}, pcsc-lite-libs%{?_isa}, cups-libs%{?_isa}

# Standard JPackage base provides
Provides: jre-headless%1 = %{epoch}:%{javaver}
Provides: jre-%{javaver}-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-headless%%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless%1 = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
Provides: java-headless%1 = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi%1 = %{epoch}:%{version}
Provides: jndi-ldap%1 = %{epoch}:%{version}
Provides: jndi-cos%1 = %{epoch}:%{version}
Provides: jndi-rmi%1 = %{epoch}:%{version}
Provides: jndi-dns%1 = %{epoch}:%{version}
Provides: jaas%1 = %{epoch}:%{version}
Provides: jsse%1 = %{epoch}:%{version}
Provides: jce%1 = %{epoch}:%{version}
Provides: jdbc-stdext%1 = 4.1
Provides: java-sasl%1 = %{epoch}:%{version}

# https://bugzilla.redhat.com/show_bug.cgi?id=1312019
Provides: /usr/bin/jjs

#Obsoletes: java-1.7.0-openjdk-headless%1
}

%global java_devel_rpo() %{expand:
# Require base package
Requires:         %{name}%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin}%1 = %{epoch}:%{version}
Provides: java-sdk-%{javaver}%1 = %{epoch}:%{version}
Provides: java-sdk-%{origin}%1 = %{epoch}:%{version}
Provides: java-sdk%1 = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel%1 = %{epoch}:%{version}
Provides: java-%{javaver}-%{origin}-devel%1 = %{epoch}:%{version}
Provides: java-devel-%{origin}%1 = %{epoch}:%{version}
Provides: java-devel%1 = %{epoch}:%{javaver}

#Obsoletes: java-1.7.0-openjdk-devel%1
#Obsoletes: java-1.5.0-gcj-devel%1
}


%global java_demo_rpo() %{expand:
Requires: %{name}%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}

Provides: java-demo%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-demo%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-demo%1 = %{epoch}:%{version}-%{release}

#Obsoletes: java-1.7.0-openjdk-demo%1
}

%global java_javadoc_rpo() %{expand:
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall javadoc alternative
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# Standard JPackage javadoc provides.
Provides: java-javadoc%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-javadoc%1 = %{epoch}:%{version}-%{release}

#Obsoletes: java-1.7.0-openjdk-javadoc%1

}

%global java_src_rpo() %{expand:
Requires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}

# Standard JPackage javadoc provides
Provides: java-src%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-src%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-src%1 = %{epoch}:%{version}-%{release}
#Obsoletes: java-1.7.0-openjdk-src%1
}

%global java_accessibility_rpo() %{expand:
Requires: java-atk-wrapper%{?_isa}
Requires: %{name}%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}

Provides: java-accessibility = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-accessibility = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-accessibility = %{epoch}:%{version}-%{release}

#Obsoletes: java-1.7.0-openjdk-accessibility%1
}

# Prevent brp-java-repack-jars from being run
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{updatever}.%{buildver}
Release: %{?eaprefix}%{rpmrelease}%{?extraver}%{?dist}%{?_trivial}%{?_buildid}
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

# Shenandoah HotSpot
# aarch64-port/jdk8u-shenandoah contains an integration forest of
# OpenJDK 8u, the aarch64 port and Shenandoah
# To regenerate, use:
# VERSION=%%{shenandoah_revision}
# FILE_NAME_ROOT=%%{shenandoah_project}-%%{shenandoah_repo}-${VERSION}
# REPO_ROOT=<path to checked-out repository> generate_source_tarball.sh
# where the source is obtained from http://hg.openjdk.java.net/%%{project}/%%{repo}
Source0: %{shenandoah_project}-%{shenandoah_repo}-%{shenandoah_revision}.tar.xz

# Custom README for -src subpackage
Source2:  README.md

# Use 'icedtea_sync.sh' to update the following
# They are based on code contained in the IcedTea project (3.x).

# Systemtap tapsets. Zipped up to keep it small.
Source8: tapsets-icedtea-%{icedteaver}.tar.xz

# Desktop files. Adapted from IcedTea
Source9: jconsole.desktop.in
Source10: policytool.desktop.in

# nss configuration file
Source11: nss.cfg.in

# Removed libraries that we link instead
Source12: %{name}-remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

# Ensure ECDSA is working
Source14: TestECDSA.java

Source20: repackReproduciblePolycies.sh

# New versions of config files with aarch64 support. This is not upstream yet.
Source100: config.guess
Source101: config.sub

############################################
#
# RPM/distribution specific patches
#
# This section includes patches specific to
# Fedora/RHEL which can not be upstreamed
# either in their current form or at all.
############################################

# Accessibility patches
# Ignore AWTError when assistive technologies are loaded 
Patch1:   rh1648242-accessible_toolkit_crash_do_not_break_jvm.patch
# Restrict access to java-atk-wrapper classes
Patch3:   rh1648644-java_access_bridge_privileged_security.patch
# Turn on AssumeMP by default on RHEL systems
Patch534: rh1648246-always_instruct_vm_to_assume_multiple_processors_are_available.patch

#############################################
#
# Upstreamable patches
#
# This section includes patches which need to
# be reviewed & pushed to the current development
# tree of OpenJDK.
#############################################
# PR2737: Allow multiple initialization of PKCS11 libraries
Patch5: pr2737-allow_multiple_pkcs11_library_initialisation_to_be_a_non_critical_error.patch
# PR2095, RH1163501: 2048-bit DH upper bound too small for Fedora infrastructure (sync with IcedTea 2.x)
Patch504: rh1163501-increase_2048_bit_dh_upper_bound_fedora_infrastructure_in_dhparametergenerator.patch
# Turn off strict overflow on IndicRearrangementProcessor{,2}.cpp following 8140543: Arrange font actions
Patch512: rh1649664-awt2dlibraries_compiled_with_no_strict_overflow.patch
# RH1337583, PR2974: PKCS#10 certificate requests now use CRLF line endings rather than system line endings
Patch523: pr2974-rh1337583-add_systemlineendings_option_to_keytool_and_use_line_separator_instead_of_crlf_in_pkcs10.patch
# PR3083, RH1346460: Regression in SSL debug output without an ECC provider
Patch528: pr3083-rh1346460-for_ssl_debug_return_null_instead_of_exception_when_theres_no_ecc_provider.patch
# PR3601: Fix additional -Wreturn-type issues introduced by 8061651
Patch530: pr3601-fix_additional_Wreturn_type_issues_introduced_by_8061651_for_prims_jvm_cpp.patch
# PR2888: OpenJDK should check for system cacerts database (e.g. /etc/pki/java/cacerts)
# PR3575, RH1567204: System cacerts database handling should not affect jssecacerts
Patch539: pr2888-openjdk_should_check_for_system_cacerts_database_eg_etc_pki_java_cacerts.patch
# RH1566890: CVE-2018-3639
Patch529: rh1566890-CVE_2018_3639-speculative_store_bypass.patch
Patch531: rh1566890-CVE_2018_3639-speculative_store_bypass_toggle.patch
# JDK-8009550, RH910107: PlatformPCSC should load versioned so
Patch541: rh1684077-openjdk_should_depend_on_pcsc-lite-libs_instead_of_pcsc-lite-devel.patch

#############################################
#
# Arch-specific upstreamable patches
#
# This section includes patches which need to
# be reviewed & pushed upstream and are specific
# to certain architectures. This usually means the
# current OpenJDK development branch, but may also
# include other trees e.g. for the AArch64 port for
# OpenJDK 8u.
#############################################
# s390: PR3593: Use "%z" for size_t on s390 as size_t != intptr_t
Patch103: pr3593-s390_use_z_format_specifier_for_size_t_arguments_as_size_t_not_equals_to_int.patch
# x86: S8199936, PR3533: HotSpot generates code with unaligned stack, crashes on SSE operations (-mstackrealign workaround)
Patch105: jdk8199936-pr3533-enable_mstackrealign_on_x86_linux_as_well_as_x86_mac_os_x.patch
# AArch64: PR3519: Fix further functions with a missing return value (AArch64)
Patch106: pr3519-fix_further_functions_with_a_missing_return_value.patch
# S390 ambiguous log2_intptr calls
Patch107: s390-8214206_fix.patch

#############################################
#
# Patches which need backporting to 8u
#
# This section includes patches which have
# been pushed upstream to the latest OpenJDK
# development tree, but need to be backported
# to OpenJDK 8u.
#############################################
# S8074839, PR2462: Resolve disabled warnings for libunpack and the unpack200 binary
# This fixes printf warnings that lead to build failure with -Werror=format-security from optflags
Patch502: pr2462-resolve_disabled_warnings_for_libunpack_and_the_unpack200_binary.patch
# S8154313: Generated javadoc scattered all over the place
Patch400: jdk8154313-generated_javadoc_scattered_all_over_the_place.patch
# PR3591: Fix for bug 3533 doesn't add -mstackrealign to JDK code
Patch571: jdk8199936-pr3591-enable_mstackrealign_on_x86_linux_as_well_as_x86_mac_os_x_jdk.patch
# 8143245, PR3548: Zero build requires disabled warnings
Patch574: jdk8143245-pr3548-zero_build_requires_disabled_warnings.patch
# 8197981, PR3548: Missing return statement in __sync_val_compare_and_swap_8
Patch575: jdk8197981-pr3548-missing_return_statement_in_sync_val_compare_and_swap_8.patch
# 8062808, PR3548: Turn on the -Wreturn-type warning
Patch577: jdk8062808-pr3548-turn_on_the_wreturn_type_warning.patch
# s390: JDK-8203030, Type fixing for s390
Patch102: jdk8203030-zero_s390_31_bit_size_t_type_conflicts_in_shared_code.patch
# 8035341: Allow using a system installed libpng
Patch202: jdk8035341-allow_using_system_installed_libpng.patch
# 8042159: Allow using a system-installed lcms2
Patch203: jdk8042159-allow_using_system_installed_lcms2.patch

#############################################
#
# Patches appearing in 8u222
#
# This section includes patches which are present
# in the listed OpenJDK 8u release and should be
# able to be removed once that release is out
# and used by this RPM.
#############################################

#############################################
#
# Patches ineligible for 8u
#
# This section includes patches which are present
# upstream, but ineligible for upstream 8u backport.
#############################################
# 8043805: Allow using a system-installed libjpeg
Patch201: jdk8043805-allow_using_system_installed_libjpeg.patch

#############################################
#
# Shenandoah fixes
#
# This section includes patches which are
# specific to the Shenandoah garbage collector
# and should be upstreamed to the appropriate
# trees.
#############################################

#############################################
#
# Non-OpenJDK fixes
#
# This section includes patches to code other
# that from OpenJDK.
#############################################

# Section currently empty

# Amazon-specific patches
Patch1000: 0001-Prevent-NULL-arguments-to-strcmp.patch

#############################################
#
# Dependencies
#
#############################################
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: binutils
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
# elfutils only are OK for build without AOT
BuildRequires: elfutils-devel
BuildRequires: fontconfig
BuildRequires: freetype-devel
BuildRequires: giflib-devel
BuildRequires: gcc-c++
BuildRequires: gdb
BuildRequires: gtk2-devel
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxslt
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
# Requirements for setting up the nss.cfg
BuildRequires: nss-devel
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: zip
BuildRequires: unzip
# Use OpenJDK 7 where available (on RHEL) to avoid
# having to use the rhel-7.x-java-unsafe-candidate hack
%if ! 0%{?fedora} && 0%{?rhel} <= 7
# Require a boot JDK which doesn't fail due to RH1482244
BuildRequires: java-1.7.0-openjdk-devel >= 1.7.0.151-2.6.11.3
%else
BuildRequires: java-1.8.0-openjdk-devel
%endif
# Zero-assembler build requirement
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif
BuildRequires: tzdata-java >= 2015d
# Earlier versions have a bug in tree vectorization on PPC
BuildRequires: gcc >= 4.8.3-8

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

# this is always built, also during debug-only build
# when it is built in debug-only this package is just placeholder
%{java_rpo %{nil}}

%description
The %{origin_nice} runtime environment.

%if %{include_debug_build}
%package debug
Summary: %{origin_nice} Runtime Environment %{majorver} %{debug_on}
Group:   Development/Languages

%{java_rpo -- %{debug_suffix_unquoted}}
%description debug
The %{origin_nice} runtime environment.
%{debug_warning}
%endif

%if %{include_normal_build}
%package headless
Summary: %{origin_nice} Headless Runtime Environment %{majorver}
Group:   Development/Languages

%{java_headless_rpo %{nil}}

%description headless
The %{origin_nice} runtime environment %{majorver} without audio and video support.
%endif

%if %{include_debug_build}
%package headless-debug
Summary: %{origin_nice} Runtime Environment %{debug_on}
Group:   Development/Languages

%{java_headless_rpo -- %{debug_suffix_unquoted}}

%description headless-debug
The %{origin_nice} runtime environment %{majorver} without audio and video support.
%{debug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: %{origin_nice} Development Environment %{majorver}
Group:   Development/Tools

%{java_devel_rpo %{nil}}

%description devel
The %{origin_nice} development tools %{majorver}.
%endif

%if %{include_debug_build}
%package devel-debug
Summary: %{origin_nice} Development Environment %{majorver} %{debug_on}
Group:   Development/Tools

%{java_devel_rpo -- %{debug_suffix_unquoted}}

%description devel-debug
The %{origin_nice} development tools %{majorver}.
%{debug_warning}
%endif

%if %{include_normal_build}
%package demo
Summary: %{origin_nice} Demos %{majorver}
Group:   Development/Languages

%{java_demo_rpo %{nil}}

%description demo
The %{origin_nice} demos %{majorver}.
%endif

%if %{include_debug_build}
%package demo-debug
Summary: %{origin_nice} Demos %{majorver} %{debug_on}
Group:   Development/Languages

%{java_demo_rpo -- %{debug_suffix_unquoted}}

%description demo-debug
The %{origin_nice} demos %{majorver}.
%{debug_warning}
%endif

%if %{include_normal_build}
%package src
Summary: %{origin_nice} Source Bundle %{majorver}
Group:   Development/Languages

%{java_src_rpo %{nil}}

%description src
The java-%{origin}-src sub-package contains the complete %{origin_nice} %{majorver}
class library source code for use by IDE indexers and debuggers.
%endif

%if %{include_debug_build}
%package src-debug
Summary: %{origin_nice} Source Bundle %{majorver} %{for_debug}
Group:   Development/Languages

%{java_src_rpo -- %{debug_suffix_unquoted}}

%description src-debug
The java-%{origin}-src-slowdebug sub-package contains the complete %{origin_nice} %{majorver}
 class library source code for use by IDE indexers and debuggers. Debugging %{for_debug}.
%endif

%if %{include_normal_build}
%package javadoc
Summary: %{origin_nice} %{majorver} API documentation
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

%{java_javadoc_rpo %{nil}}

%description javadoc
The %{origin_nice} %{majorver} API documentation.
%endif

%if %{include_normal_build}
%package javadoc-zip
Summary: %{origin_nice} %{majorver} API documentation compressed in a single archive
Group:   Documentation
Requires: javapackages-tools
BuildArch: noarch

%{java_javadoc_rpo %{nil}}

%description javadoc-zip
The %{origin_nice} %{majorver} API documentation compressed in a single archive.
%endif

%if %{include_debug_build}
%package javadoc-debug
Summary: %{origin_nice} %{majorver} API documentation %{for_debug}
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

%{java_javadoc_rpo -- %{debug_suffix_unquoted}}

%description javadoc-debug
The %{origin_nice} %{majorver} API documentation %{for_debug}.
%endif

%if %{include_debug_build}
%package javadoc-zip-debug
Summary: %{origin_nice} %{majorver} API documentation compressed in a single archive %{for_debug}
Group:   Documentation
Requires: javapackages-tools
BuildArch: noarch

%{java_javadoc_rpo -- %{debug_suffix_unquoted}}

%description javadoc-zip-debug
The %{origin_nice} %{majorver} API documentation compressed in a single archive %{for_debug}.
%endif

%if %{include_normal_build}
%package accessibility
Summary: OpenJDK accessibility connector

%{java_accessibility_rpo %{nil}}

%description accessibility
Enables accessibility support in %{origin_nice} %{majorver} by using java-atk-wrapper. This allows
compatible at-spi2 based accessibility programs to work for AWT and Swing-based
programs.

Please note, the java-atk-wrapper is still in beta, and %{origin_nice} %{majorver} itself is still
being tuned to be working with accessibility features. There are known issues
with accessibility on, so please do not install this package unless you really
need to.
%endif

%if %{include_debug_build}
%package accessibility-debug
Summary: %{origin_nice} %{majorver} accessibility connector %{for_debug}

%{java_accessibility_rpo -- %{debug_suffix_unquoted}}

%description accessibility-debug
See normal java-%{version}-openjdk-accessibility description.
%endif

%prep
if [ %{include_normal_build} -eq 0 -o  %{include_normal_build} -eq 1 ] ; then
  echo "include_normal_build is %{include_normal_build}"
else
  echo "include_normal_build is %{include_normal_build}, thats invalid. Use 1 for yes or 0 for no"
  exit 11
fi
if [ %{include_debug_build} -eq 0 -o  %{include_debug_build} -eq 1 ] ; then
  echo "include_debug_build is %{include_debug_build}"
else
  echo "include_debug_build is %{include_debug_build}, thats invalid. Use 1 for yes or 0 for no"
  exit 12
fi
if [ %{include_debug_build} -eq 0 -a  %{include_normal_build} -eq 0 ] ; then
  echo "You have disabled both include_debug_build and include_normal_build. That is a no go."
  exit 13
fi
if [ %{include_normal_build} -eq 0 ] ; then
  echo "You have disabled the normal build, but this is required to provide docs for the debug build."
  exit 14
fi

echo "Update version: %{updatever}"
echo "Build number: %{buildver}"
echo "Milestone: %{milestone}"
%setup -q -c -n %{uniquesuffix ""} -T -a 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 7 ] ; then
 echo "priority must be 7 digits in total, violated"
 exit 14
fi
# For old patches
ln -s %{top_level_dir_name} jdk8

cp %{SOURCE2} .

# replace outdated configure guess script
#
# the configure macro will do this too, but it also passes a few flags not
# supported by openjdk configure script
cp %{SOURCE100} %{top_level_dir_name}/common/autoconf/build-aux/
cp %{SOURCE101} %{top_level_dir_name}/common/autoconf/build-aux/

# OpenJDK patches

# Remove libraries that are linked
sh %{SOURCE12}

# System library fixes
%patch201
%patch202
%patch203

%patch1
%patch3
%patch5

# s390 build fixes
%patch102
%patch103
%patch107

# AArch64 fixes
%patch106

# x86 fixes
%patch105

# Upstreamable fixes
%patch502
%patch504
%patch512
%patch400
%patch523
%patch528
%patch530
%patch529
%patch531
%patch571
%patch574
%patch575
%patch577
%patch541

# RPM-only fixes
%patch539

# RHEL-only patches
%if ! 0%{?fedora} && 0%{?rhel} <= 7
%patch534
%endif

# Shenandoah patches

# Amazon-specific patches
%patch1000

# Extract systemtap tapsets
%if %{with_systemtap}
tar --strip-components=1 -x -I xz -f %{SOURCE8}
%if %{include_debug_build}
cp -r tapset tapset%{debug_suffix}
%endif


for suffix in %{build_loop} ; do
  for file in "tapset"$suffix/*.in; do
    OUTPUT_FILE=`echo $file | sed -e "s:\.stp\.in$:-%{version}-%{release}.%{_arch}.stp:g"`
    sed -e "s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir $suffix}/jre/lib/%{archinstall}/server/libjvm.so:g" $file > $file.1
# TODO find out which architectures other than i686 have a client vm
%ifarch %{ix86}
    sed -e "s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir $suffix}/jre/lib/%{archinstall}/client/libjvm.so:g" $file.1 > $OUTPUT_FILE
%else
    sed -e "/@ABS_CLIENT_LIBJVM_SO@/d" $file.1 > $OUTPUT_FILE
%endif
    sed -i -e "s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir $suffix}:g" $OUTPUT_FILE
    sed -i -e "s:@INSTALL_ARCH_DIR@:%{archinstall}:g" $OUTPUT_FILE
    sed -i -e "s:@prefix@:%{_jvmdir}/%{sdkdir $suffix}/:g" $OUTPUT_FILE
  done
done
# systemtap tapsets ends
%endif

# Prepare desktop files
# The _X_ syntax indicates variables that are replaced by make upstream
# The @X@ syntax indicates variables that are replaced by configure upstream
for suffix in %{build_loop} ; do
for file in %{SOURCE9} %{SOURCE10} ; do
    FILE=`basename $file | sed -e s:\.in$::g`
    EXT="${FILE##*.}"
    NAME="${FILE%.*}"
    OUTPUT_FILE=$NAME$suffix.$EXT
    sed    -e  "s:_BINDIR_:%{sdkbindir -- $suffix}:g" $file > $OUTPUT_FILE
    sed -i -e  "s:_JREBINDIR_:%{jrebindir -- $suffix}:g" $OUTPUT_FILE
    sed -i -e  "s:@target_cpu@:%{_arch}:g" $OUTPUT_FILE
    sed -i -e  "s:@OPENJDK_VER@:%{version}-%{release}$suffix:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VER@:%{javaver}:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VENDOR@:%{origin}:g" $OUTPUT_FILE
done
done

# Setup nss.cfg
sed -e "s:@NSS_LIBDIR@:%{NSS_LIBDIR}:g" %{SOURCE11} > nss.cfg


%build
# How many CPU's do we have?
export NUM_PROC=%(/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :)
export NUM_PROC=${NUM_PROC:-1}
%if 0%{?_smp_ncpus_max}
# Honor %%_smp_ncpus_max
[ ${NUM_PROC} -gt %{?_smp_ncpus_max} ] && export NUM_PROC=%{?_smp_ncpus_max}
%endif

%ifarch s390x sparc64 alpha %{power64} %{aarch64}
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

# We use ourcppflags because the OpenJDK build seems to
# pass EXTRA_CFLAGS to the HotSpot C++ compiler...
# Explicitly set the C++ standard as the default has changed on GCC >= 6
EXTRA_CFLAGS="%ourcppflags -Wno-error -fno-delete-null-pointer-checks -fno-lifetime-dse -Wno-deprecated-declarations"
EXTRA_CPP_FLAGS="%ourcppflags -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse -Wno-deprecated-declarations"
%ifarch %{power64} ppc
# fix rpmlint warnings
EXTRA_CFLAGS="$EXTRA_CFLAGS -fno-strict-aliasing"
%endif
export EXTRA_CFLAGS

(cd %{top_level_dir_name}/common/autoconf
 bash ./autogen.sh
)

for suffix in %{build_loop} ; do
if [ "$suffix" = "%{debug_suffix}" ] ; then
debugbuild=%{debugbuild_parameter}
else
debugbuild=%{normalbuild_parameter}
fi

# Variable used in hs_err hook on build failures
top_dir_abs_path=$(pwd)/%{top_level_dir_name}

mkdir -p %{buildoutputdir $suffix}
pushd %{buildoutputdir $suffix}

bash ../../configure \
%ifnarch %{jit_arches}
    --with-jvm-variants=zero \
%endif
    --with-native-debug-symbols=internal \
    --with-milestone=%{milestone} \
    --with-update-version=%{updatever} \
    --with-build-number=%{buildver} \
    --with-boot-jdk=/usr/lib/jvm/java-openjdk \
    --with-debug-level=$debugbuild \
    --enable-unlimited-crypto \
    --with-zlib=system \
    --with-libjpeg=system \
    --with-giflib=system \
    --with-libpng=system \
    --with-lcms=bundled \
    --with-stdc++lib=dynamic \
    --with-extra-cxxflags="$EXTRA_CPP_FLAGS" \
    --with-extra-cflags="$EXTRA_CFLAGS" \
    --with-extra-ldflags="%{ourldflags}" \
    --with-num-cores="$NUM_PROC"

cat spec.gmk
cat hotspot-spec.gmk

# Debug builds don't need same targets as release for
# build speed-up
maketargets="%{release_targets}"
if echo $debugbuild | grep -q "debug" ; then
  maketargets="%{debug_targets}"
fi
make \
    JAVAC_FLAGS=-g \
    LOG=trace \
    $maketargets || ( pwd; find $top_dir_abs_path -name "hs_err_pid*.log" | xargs cat && false )

# the build (erroneously) removes read permissions from some jars
# this is a regression in OpenJDK 7 (our compiler):
# http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
find images/%{jdkimage} -iname '*.jar' -exec chmod ugo+r {} \;
chmod ugo+r images/%{jdkimage}/lib/ct.sym

# remove redundant *diz and *debuginfo files
find images/%{jdkimage} -iname '*.diz' -exec rm {} \;
find images/%{jdkimage} -iname '*.debuginfo' -exec rm {} \;

# Build screws up permissions on binaries
# https://bugs.openjdk.java.net/browse/JDK-8173610
find images/%{jdkimage} -iname '*.so' -exec chmod +x {} \;
find images/%{jdkimage}/bin/ -exec chmod +x {} \;

popd >& /dev/null

# Install nss.cfg right away as we will be using the JRE above
export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{jdkimage}

# Install nss.cfg right away as we will be using the JRE above
install -m 644 nss.cfg $JAVA_HOME/jre/lib/security/

# Use system-wide tzdata
rm $JAVA_HOME/jre/lib/tzdb.dat
ln -s %{_datadir}/javazi-1.8/tzdb.dat $JAVA_HOME/jre/lib/tzdb.dat

# build cycles
done

%check

# We test debug first as it will give better diagnostics on a crash
for suffix in %{rev_build_loop} ; do

export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{jdkimage}

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java TestCryptoLevel

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

# Check debug symbols are present and can identify code
find "$JAVA_HOME" -iname '*.so' -print0 | while read -d $'\0' lib
do
  if [ -f "$lib" ] ; then
    echo "Testing $lib for debug symbols"
    # All these tests rely on RPM failing the build if the exit code of any set
    # of piped commands is non-zero.

    # Test for .debug_* sections in the shared object. This is the main test
    # Stripped objects will not contain these
    eu-readelf -S "$lib" | grep "] .debug_"
    test $(eu-readelf -S "$lib" | grep -E "\]\ .debug_(info|abbrev)" | wc --lines) == 2

    # Test FILE symbols. These will most likely be removed by anything that
    # manipulates symbol tables because it's generally useless. So a nice test
    # that nothing has messed with symbols
    old_IFS="$IFS"
    IFS=$'\n'
    for line in $(eu-readelf -s "$lib" | grep "00000000      0 FILE    LOCAL  DEFAULT")
    do
     # We expect to see .cpp files, except for architectures like aarch64 and
     # s390 where we expect .o and .oS files
      echo "$line" | grep -E "ABS ((.*/)?[-_a-zA-Z0-9]+\.(c|cc|cpp|cxx|o|oS))?$"
    done
    IFS="$old_IFS"

    # If this is the JVM, look for javaCalls.(cpp|o) in FILEs, for extra sanity checking
    if [ "`basename $lib`" = "libjvm.so" ]; then
      eu-readelf -s "$lib" | \
        grep -E "00000000      0 FILE    LOCAL  DEFAULT      ABS javaCalls.(cpp|o)$"
    fi

    # Test that there are no .gnu_debuglink sections pointing to another
    # debuginfo file. There shouldn't be any debuginfo files, so the link makes
    # no sense either
    eu-readelf -S "$lib" | grep 'gnu'
    if eu-readelf -S "$lib" | grep '] .gnu_debuglink' | grep PROGBITS; then
      echo "bad .gnu_debuglink section."
      eu-readelf -x .gnu_debuglink "$lib"
      false
    fi
  fi
done

# Make sure gdb can do a backtrace based on line numbers on libjvm.so
# javaCalls.cpp:58 should map to:
# http://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/file/ff3b27e6bcc2/src/share/vm/runtime/javaCalls.cpp#l58 
# Using line number 1 might cause build problems. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1539664
# https://bugzilla.redhat.com/show_bug.cgi?id=1538767
gdb -q "$JAVA_HOME/bin/java" <<EOF | tee gdb.out
handle SIGSEGV pass nostop noprint
handle SIGILL pass nostop noprint
set breakpoint pending on
break javaCalls.cpp:1
commands 1
backtrace
quit
end
run -version
EOF
grep 'JavaCallWrapper::JavaCallWrapper' gdb.out

# Check src.zip has all sources. See RHBZ#1130490
jar -tf $JAVA_HOME/src.zip | grep 'sun.misc.Unsafe'

# Check class files include useful debugging information
$JAVA_HOME/bin/javap -l java.lang.Object | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.lang.Object | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.lang.Object | grep LocalVariableTable

# Check generated class files include useful debugging information
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LocalVariableTable

# build cycles check
done

%install
STRIP_KEEP_SYMTAB=libjvm*

for suffix in %{build_loop} ; do

# Install the jdk
pushd %{buildoutputdir $suffix}/images/%{jdkimage}

# Install jsa directories so we can owe them
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix}/lib/%{archinstall}/server/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix}/lib/%{archinstall}/client/

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}
  cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix}

%if %{with_systemtap}
  # Install systemtap support files
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset
  # note, that uniquesuffix  is in BUILD dir in this case
  cp -a $RPM_BUILD_DIR/%{uniquesuffix ""}/tapset$suffix/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset/
  pushd  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset/
   tapsetFiles=`ls *.stp`
  popd
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir $suffix}/tapset %{tapsetdir})
    for name in $tapsetFiles ; do
      targetName=`echo $name | sed "s/.stp/$suffix.stp/"`
      ln -sf $RELATIVE/$name $targetName
    done
  popd
%endif

  # Remove empty cacerts database
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix}/lib/security/cacerts
  # Install cacerts symlink needed by some apps which hardcode the path
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir $suffix}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir $suffix}
  pushd $RPM_BUILD_ROOT%{jvmjardir $suffix}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir $suffix}/lib %{jvmjardir $suffix})
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

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{uniquesuffix $suffix}/jce/vanilla

  # Install versioned symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir $suffix} %{jrelnk $suffix}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir $suffix} %{jrelnk $suffix}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{uniquesuffix $suffix}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}
  mkdir -p sample/rmi
  if [ ! -e sample/rmi/java-rmi.cgi ] ; then 
    # hack to allow --short-circuit on install
    mv bin/java-rmi.cgi sample/rmi
  fi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}

popd
 
# Install Javadoc documentation
# Always take docs from normal build to avoid building them twice
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir $normal_suffix}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}
cp -a %{buildoutputdir $normal_suffix}/bundles/jdk-%{javaver}_%{updatever}%{milestone_version}${normal_suffix}-%{buildver}-docs.zip  $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}.zip

# Install icons and menu entries
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    %{top_level_dir_name}/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}-%{origin}.png
done

# Install desktop files
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole$suffix policytool$suffix ; do
    desktop-file-install --vendor=%{uniquesuffix $suffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files-headless"$suffix"
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir $suffix} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  > %{name}.files.all"$suffix"
#split %%{name}.files to %%{name}.files-headless and %%{name}.files
#see https://bugzilla.redhat.com/show_bug.cgi?id=875408
NOT_HEADLESS=\
"%{_jvmdir}/%{uniquesuffix $suffix}/jre/lib/%{archinstall}/libjsoundalsa.so
%{_jvmdir}/%{uniquesuffix $suffix}/jre/lib/%{archinstall}/libpulse-java.so
%{_jvmdir}/%{uniquesuffix $suffix}/jre/lib/%{archinstall}/libsplashscreen.so
%{_jvmdir}/%{uniquesuffix $suffix}/jre/lib/%{archinstall}/libawt_xawt.so
%{_jvmdir}/%{uniquesuffix $suffix}/jre/lib/%{archinstall}/libjawt.so
%{_jvmdir}/%{uniquesuffix $suffix}/jre/bin/policytool"
#filter  %%{name}.files from  %%{name}.files.all to %%{name}.files-headless
ALL=`cat %{name}.files.all"$suffix"`
for file in $ALL ; do 
  INLCUDE="NO" ; 
  for blacklist in $NOT_HEADLESS ; do
#we can not match normally, because rpmbuild will evaluate !0 result as script failure
    q=`expr match "$file" "$blacklist"` || :
    l=`expr length  "$blacklist"` || :
    if [ $q -eq $l  ]; then 
      INLCUDE="YES" ; 
    fi;
done
if [ "x$INLCUDE" = "xNO"  ]; then 
    echo "$file" >> %{name}.files-headless"$suffix"
else
    echo "$file" >> %{name}.files"$suffix"
fi
done
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files"$suffix"

# FIXME: remove SONAME entries from demo DSOs. See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files"$suffix"
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files"$suffix"

# Create links which leads to separately installed java-atk-bridge and allow configuration
# links points to java-atk-wrapper - an dependence
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir $suffix}/lib/%{archinstall}
    ln -s %{_libdir}/java-atk-wrapper/libatk-wrapper.so.0 libatk-wrapper.so
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir $suffix}/lib/ext
     ln -s %{_libdir}/java-atk-wrapper/java-atk-wrapper.jar  java-atk-wrapper.jar
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir $suffix}/lib/
    echo "#Config file to  enable java-atk-wrapper" > accessibility.properties
    echo "" >> accessibility.properties
    echo "assistive_technologies=org.GNOME.Accessibility.AtkWrapper" >> accessibility.properties
    echo "" >> accessibility.properties
  popd

bash %{SOURCE20} $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir $suffix} %{javaver}
# https://bugzilla.redhat.com/show_bug.cgi?id=1183793
touch -t 201401010000 $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir $suffix}/lib/security/java.security

# stabilize permissions
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -name "*.so" -exec chmod 755 {} \; ; 
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -type d -exec chmod 755 {} \; ; 
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -name "ASSEMBLY_EXCEPTION" -exec chmod 644 {} \; ; 
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -name "LICENSE" -exec chmod 644 {} \; ; 
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -name "THIRD_PARTY_README" -exec chmod 644 {} \; ; 

# end, dual install
done

%if %{include_normal_build}
# intentionally only for non-debug
%pretrans headless -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1290388 for pretrans over pre
-- if copy-jdk-configs is in transaction, it installs in pretrans to temp
-- if copy_jdk_configs is in temp, then it means that copy-jdk-configs is in transaction  and so is
-- preferred over one in %%{_libexecdir}. If it is not in transaction, then depends
-- whether copy-jdk-configs is installed or not. If so, then configs are copied
-- (copy_jdk_configs from %%{_libexecdir} used) or not copied at all
local posix = require "posix"
local debug = false

SOURCE1 = "%{rpm_state_dir}/copy_jdk_configs.lua"
SOURCE2 = "%{_libexecdir}/copy_jdk_configs.lua"

local stat1 = posix.stat(SOURCE1, "type");
local stat2 = posix.stat(SOURCE2, "type");

  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE1 .." exists - copy-jdk-configs in transaction, using this one.")
  end;
  package.path = package.path .. ";" .. SOURCE1
else
  if (stat2 ~= nil) then
  if (debug) then
    print(SOURCE2 .." exists - copy-jdk-configs already installed and NOT in transaction. Using.")
  end;
  package.path = package.path .. ";" .. SOURCE2
  else
    if (debug) then
      print(SOURCE1 .." does NOT exists")
      print(SOURCE2 .." does NOT exists")
      print("No config files will be copied")
    end
  return
  end
end
-- run content of included file with fake args
arg = {"--currentjvm", "%{uniquesuffix %{nil}}", "--jvmdir", "%{_jvmdir %{nil}}", "--origname", "%{name}", "--origjavaver", "%{javaver}", "--arch", "%{_arch}", "--temp", "%{rpm_state_dir}/%{name}.%{_arch}"}
require "copy_jdk_configs.lua"

%post
%{post_script %{nil}}

%post headless
%{post_headless %{nil}}

%postun
%{postun_script %{nil}}

%postun headless
%{postun_headless %{nil}}

%posttrans
%{posttrans_script %{nil}}

%post devel
%{post_devel %{nil}}

%postun devel
%{postun_devel %{nil}}

%posttrans  devel
%{posttrans_devel %{nil}}

%post javadoc
%{post_javadoc %{nil}}

%postun javadoc
%{postun_javadoc %{nil}}

%post javadoc-zip
%{post_javadoc_zip %{nil}}

%postun javadoc-zip
%{postun_javadoc_zip %{nil}}
%endif

%if %{include_debug_build}
%post debug
%{post_script -- %{debug_suffix_unquoted}}

%post headless-debug
%{post_headless -- %{debug_suffix_unquoted}}

%postun debug
%{postun_script -- %{debug_suffix_unquoted}}

%postun headless-debug
%{postun_headless -- %{debug_suffix_unquoted}}

%posttrans debug
%{posttrans_script -- %{debug_suffix_unquoted}}

%post devel-debug
%{post_devel -- %{debug_suffix_unquoted}}

%postun devel-debug
%{postun_devel -- %{debug_suffix_unquoted}}

%posttrans  devel-debug
%{posttrans_devel -- %{debug_suffix_unquoted}}

%post javadoc-debug
%{post_javadoc -- %{debug_suffix_unquoted}}

%postun javadoc-debug
%{postun_javadoc -- %{debug_suffix_unquoted}}

%post javadoc-zip-debug
%{post_javadoc_zip -- %{debug_suffix_unquoted}}

%postun javadoc-zip-debug
%{postun_javadoc_zip -- %{debug_suffix_unquoted}}

%endif

%if %{include_normal_build}
%files -f %{name}.files
# main package builds always
%{files_jre %{nil}}
%else
%files
# placeholder
%endif


%if %{include_normal_build}
%files headless  -f %{name}.files-headless
# important note, see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
# all config/noreplace files (and more) have to be declared in pretrans. See pretrans
%{files_jre_headless %{nil}}

%files devel
%{files_devel %{nil}}

%files demo -f %{name}-demo.files
%{files_demo %{nil}}

%files src
%{files_src %{nil}}

%files javadoc
%{files_javadoc %{nil}}

# this puts huge file to /usr/share
# unluckily ti is really a documentation file
# and unluckily it really is architecture-dependent, as eg. aot and grail are now x86_64 only
# same for debug variant
%files javadoc-zip
%{files_javadoc_zip %{nil}}

%files accessibility
%{files_accessibility %{nil}}
%endif

%if %{include_debug_build}
%files debug -f %{name}.files-debug
%{files_jre -- %{debug_suffix_unquoted}}

%files headless-debug  -f %{name}.files-headless-debug
%{files_jre_headless -- %{debug_suffix_unquoted}}

%files devel-debug
%{files_devel -- %{debug_suffix_unquoted}}

%files demo-debug -f %{name}-demo.files-debug
%{files_demo -- %{debug_suffix_unquoted}}

%files src-debug
%{files_src -- %{debug_suffix_unquoted}}

%files javadoc-debug
%{files_javadoc -- %{debug_suffix_unquoted}}

%files javadoc-zip-debug
%{files_javadoc_zip -- %{debug_suffix_unquoted}}

%files accessibility-debug
%{files_accessibility -- %{debug_suffix_unquoted}}
%endif

%changelog
* Wed Jan 15 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b08-0
- Update to aarch64-shenandoah-jdk8u242-b08.
- Remove local copies of JDK-8031111 & JDK-8132111 as replaced by upstream versions.
- Resolves: rhbz#1785753

* Wed Jan 15 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b07-1
- Add backports of JDK-8031111 & JDK-8132111 to fix TCK issue.
- Resolves: rhbz#1785753

* Mon Jan 13 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b07-0
- Update to aarch64-shenandoah-jdk8u242-b07.
- Switch to GA mode for final release.
- Remove Shenandoah S390 patch which is now included upstream as JDK-8236829.
- Resolves: rhbz#1785753

* Tue Jan 07 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b06-0.0.ea
- Update to aarch64-shenandoah-jdk8u242-b06 (EA)
- Resolves: rhbz#1785753

* Sun Jan 05 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b05-0.1.ea
- Update to aarch64-shenandoah-jdk8u242-b05.
- Attempt to fix Shenandoah formatting failures on S390, introduced by JDK-8232102.
- Revise b05 snapshot to include JDK-8236178.
- Add additional Shenandoah formatting fixes revealed by successful -Wno-error=format run
- Resolves: rhbz#1785753

* Thu Jan 02 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b02-0.0.ea
- Update to aarch64-shenandoah-jdk8u242-b02.
- Resolves: rhbz#1785753

* Thu Jan 02 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b01-0.1.ea
- Revert SSBD removal for now, until appropriate messaging has been decided.
- Resolves: rhbz#1785753

* Thu Dec 26 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.242.b01-0.0.ea
- Update to aarch64-shenandoah-jdk8u242-b01.
- Switch to EA mode.
- Resolves: rhbz#1785753

* Tue Dec 24 2019 Andrew John Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b09-1
- Remove CVE-2018-3639 mitigation due to performance regression and
    OpenJDK position on speculative execution vulnerabilities.
    https://mail.openjdk.java.net/pipermail/vuln-announce/2019-July/000002.html
- Resolves: rhbz#1785753

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

* Fri Jul 26 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.232.b01-0.0.ea
- Update to aarch64-shenandoah-jdk8u232-b01.
- Switch to EA mode.
- Drop JDK-8210761/RH1632174 as now upstream.
- Resolves: rhbz#1753423

* Thu Jul 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b10-1
- Update to aarch64-shenandoah-jdk8u222-b10.
- Resolves: rhbz#1724452

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b09-2
- Use normal_suffix for Javadoc zip filename to copy, as there is is no debug version.
- Resolves: rhbz#1724452

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

* Wed May 22 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.222.b03-1
- Update to aarch64-shenandoah-jdk8u222-b03.
- Set milestone to "ea" as this is not the final release.
- Drop 8210425 patches applied upstream. Still need to add AArch64 version in aarch64/shenandoah-jdk8u.
- Re-generate JDK-8141570 & JDK-8143245 patches due to 8210425 zeroshark.make changes.
- Resolves: rhbz#1705328

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

* Wed Apr 10 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b02-1
- Another cast to resolve s390 ambiguity in call to log2_intptr
- Resolves: rhbz#1693468

* Tue Apr 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b02-1
- Add cast to resolve s390 ambiguity in call to log2_intptr
- Resolves: rhbz#1693468

* Tue Apr 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.212.b02-1
- Update to aarch64-shenandoah-jdk8u212-b02.
- Remove patches included upstream
  - JDK-8197429/PR3546/RH153662{2,3}
  - JDK-8184309/PR3596
  - JDK-8210647/RH1632174
  - JDK-8029661/PR3642/RH1477159
- Re-generate patches
  - JDK-8203030
- Resolves: rhbz#1693468

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

* Thu Feb 28 2019 Jiri Vanek jvanek@redhat.com - 1:1.8.0.201.b09-2
- Replaced pcsc-lite-devel (which is in optional channel) with pcsc-lite-libs.
- added rh1684077-openjdk_should_depend_on_pcsc-lite-libs_instead_of_pcsc-lite-devel.patch to make jdk work with pcsc

* Wed Jan 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.201.b09-1
- Update to aarch64-shenandoah-jdk8u201-b09.
- Resolves: rhbz#1661577

* Wed Jan 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.192.b12-1
- Add port of 8189170 to AArch64 which is missing from upstream 8u version.
- Resolves: rhbz#1661577

* Wed Jan 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.192.b12-1
- Add 8160748 for AArch64 which is missing from upstream 8u version.
- Resolves: rhbz#1661577

* Wed Jan 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.192.b12-1
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
- Resolves: rhbz#1661577

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

* Tue Nov 06 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-9
- Fix patch organisation in the spec file:
-   * Move ECC patches back to upstreamable section
-   * Move system cacerts patches to upstreamable section
-   * Merge "Local fixes" and "RPM fixes" which amount to the same thing
-   * Move system libpng & lcms patches back to 8u upstreamable section
-   * Make it clearer that "Non-OpenJDK fixes" is currently empty
- Resolves: rhbz#1633817

* Tue Nov 06 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.191.b12-9
- Bump release so y-stream is higher than z-stream.
- Resolves: rhbz#1633817

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

* Mon Oct 01 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181.b16-0
- Update to aarch64-shenandoah-jdk8u181-b16.
- Drop PR3619 & PR3620 Shenandoah patches which should now be fixed upstream.
- Resolves: rhbz#1633822

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

* Wed Aug 08 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Add missing shenandoahBarrierSet implementation for ppc64{be,le}.
- Resolves: rhbz#1594249

* Tue Aug 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Fix wrong format specifiers in Shenandoah code.
- Resolves: rhbz#1594249

* Tue Aug 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Avoid changing variable types to fix size_t, at least for now.
- Resolves: rhbz#1594249

* Tue Aug 07 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- More size_t fixes for Shenandoah.
- Resolves: rhbz#1594249

* Fri Aug 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Add additional s390 size_t case for Shenandoah.
- Resolves: rhbz#1594249

* Fri Aug 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Actually add the patch...
- Resolves: rhbz#1594249

* Fri Aug 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-8.b13
- Attempt to fix Shenandoah build issues on s390.
- Resolves: rhbz#1594249

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

* Mon Jul 16 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.8.0.181-7.b04
- Fix requires/provides filters for internal libs. See RHBZ#1590796
- Resolves: rhbz#1594249

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

* Tue Jul 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-4.b04
- Backport "8203182, PR3603: Release session if initialization of SunPKCS11 Signature fails"
- Resolves: rhbz#1568033

* Tue Jul 03 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.181-4.b04
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

* Mon Jun 11 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.172-5.b11
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

* Wed Apr 18 2018 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.171-8.b10
- Bump release to 8 so it is again greater than the 7.5.z version.
- Resolves: rhbz#1559766

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

* Wed Dec 20 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.152-1.b16
- Backport 8191137 and add updates to the translations (8191840 in OpenJDK 7)
- Resolves: rhbz#1512647

* Wed Dec 20 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.152-1.b16
- Update to tzdata2017c (8190258/PR3499) to resolve TCK failure due to mismatch with system version.
- Resolves: rhbz#1508017

* Wed Dec 20 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.152-1.b16
- Update to aarch64-jdk8u152-b16 and aarch64-shenandoah-jdk8u152-b16.
- Update 8145913/PR3466/RH1498309 patch following upstream addition of 8152172 (AES for PPC)
- Add new file cmsalpha.c to %%{name}-remove-intree-libraries.sh
- Remove upstreamed patches for 8153711/PR3313/RH1284948, 8162384/PR3122/RH1358661, 8173941/PR3226,
-    8175813/PR3394/RH1448880, 8175887/PR3415, 8146086/PR3439/RH1478402, 8180048/PR3411/RH1449870 and
-    8164293/PR3412/RH1459641
- Resolves: rhbz#1508017

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

* Thu Oct 26 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-3.b12
- Backport "8180048: Interned string and symbol table leak memory during parallel unlinking"
- Resolves: rhbz#1490260

* Thu Oct 26 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-3.b12
- Add backport of 8146086/PR3439/RH1478402 JAXWS fix.
- Resolves: rhbz#1478402

* Thu Oct 26 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-3.b12
- Switch bootstrap back to java-1.7.0-openjdk on all architectures, depending on RH1482244 fix
- Resolves: rhbz#1499207

* Wed Oct 18 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.151-2.b12
- repack policies adapted to new counts and paths
- note that also c-j-c is needed to make this apply in next update
- Resolves: rhbz#1499207

* Wed Oct 18 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Update location of policy JAR files following 8157561.

* Wed Oct 18 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- 8188030 is not yet upstream, so it should be listed under upstreamable fixes.
- 8181055, 8181419, 8145913, 8168318, 8170328 & 8181810 all now in 8u162.
- Resolves: rhbz#1499207

* Wed Oct 18 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Correct fix to RH1191652 root patch so existing COMMON_CCXXFLAGS_JDK is not lost.
- Resolves: rhbz#1499207

* Tue Oct 17 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.151-1.b01
- Moving patch 560 out of ppc fixes
- Resolves: rhbz#1499207

* Tue Oct 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Update SystemTap tapsets to version in IcedTea 3.6.0pre02 to fix RH1492139.
- Resolves: rhbz#1499207

* Tue Oct 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Fix premature shutdown of NSS in SunEC provider.
- Resolves: rhbz#1499207

* Tue Oct 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Add 8075484/PR3473/RH1490713 which is listed as being in 8u151 but not supplied by Oracle.
- Resolves: rhbz#1499207

* Tue Oct 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.151-1.b12
- Update to aarch64-jdk8u151-b12 and aarch64-shenandoah-jdk8u151-b12.
- Update location of OpenJDK zlib system library source code in remove-intree-libraries.sh
- Drop upstreamed patches for 8179084 and RH1367357 (part of 8183028).
- Update RH1191652 (root) and PR2842 to accomodate 8151841 (GCC 6 support).
- Update PR2964/RH1337583 to accomodate 8171319 (keytool warning output)
- Update RH1163501 to accomodate 8181048 (crypto refactoring)
- Resolves: rhbz#1499207

* Mon Oct 16 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Reverted completely unnecessary patch addition which broke the RPM build.
- Resolves: rhbz#1484079

* Wed Oct 11 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.144-2.b01
- smuggled patch540, bug1484079.patch
- Resolves: rhbz#1484079

* Wed Oct 11 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Switch AArch64 to using java-1.8.0-openjdk to bootstrap until RH1482244 is fixed in bootstrap
- Resolves: rhbz#1499207

* Wed Oct 11 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Switch to IBM-supplied Montgomery backport and add remaining ppc64 fixes & CFF fix
- Resolves: rhbz#1498309
- Resolves: rhbz#1498319
- Resolves: rhbz#1498320
- Resolves: rhbz#1498321
- Resolves: rhbz#1484079

* Tue Oct 10 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-2.b01
- Backport Montgomery multiply intrinsic and dependencies for ppc64
- Resolves: rhbz#1498309

* Tue Aug 15 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.144-1.b01
- Update to aarch64-jdk8u144-b01 and aarch64-shenandoah-jdk8u144-b01.
- Exclude 8175887 from Shenandoah builds as it has been included in that repo.
- Resolves: rhbz#1477855

* Mon Aug 14 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-3.b16
- Added 8164293-pr3412-rh1459641.patch backport from 8u development tree
- Resolves: rhbz#1459641

* Fri Jul 14 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-2.b16
- Update to aarch64-jdk8u141-b16 and aarch64-shenandoah-jdk8u141-b16.
- Revert change to remove-intree-libraries.sh following backout of 8173207
- Resolves: rhbz#1466509

* Wed Jul 05 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-1.b15
- Actually add sources for previous commit.
- Resolves: rhbz#1466509

* Wed Jul 05 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.141-1.b15
- Update to aarch64-jdk8u141-b15 and aarch64-shenandoah-jdk8u141-b15.
- Update location of OpenJDK system library source code in remove-intree-libraries.sh
- Drop upstreamed patches for 6515172, 8144566, 8155049, 8165231, 8174164, 8174729 and 8175097.
- Update PR1983, PR2899 and PR2934 (SunEC + system NSS) to accomodate 8175110.
- Resolves: rhbz#1466509

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

* Fri Apr 07 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-10.b14
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

* Fri Mar 03 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-6.b14
- Patch OpenJDK to check the system cacerts database directly
- Remove unneeded symlink to the system cacerts database
- Drop outdated openssl dependency from when the RPM built the cacerts database
- Resolves: rhbz#1319875

* Fri Mar 03 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-6.b14
- Regenerate tarball with correct version of PR2126 patch.
- Update generate_source_tarball.sh script to download correct version.
- Resolves: rhbz#1400306

* Fri Mar 03 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.121-6.b14
- Properly document recently added patches.
- Resolves: rhbz#1400306

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

* Mon Jan 09 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-4.b18
- Update to aarch64-jdk8u111-b18, synced with upstream u111, S8170873 and new AArch64 fixes
- Resolves: rhbz#1391132

* Mon Nov 07 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.111-3.b15
- Add MD5 checksum from RHEL 7.2 security update so the 7.3 one overwrites it.
- Resolves: rhbz#1391132

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

* Wed Oct 5 2016  Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.102-5.b14
- debug subpackages allowed on aarch64 and ppc64le
- Resolves: rhbz#1375224

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

* Mon Aug 01 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-8.b13
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

* Mon Jul 04 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.101-2.b13
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

* Thu Jun 02 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.92-3.b14
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

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Roll back release number as release 1 never succeeded, even with tests disabled.
- Resolves: rhbz#1325423

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Add additional fix to Zero patch to properly handle result on 64-bit big-endian
- Revert debugging options (aarch64 back to JIT, product build, no -Wno-error)
- Enable full bootstrap on all architectures to check we are good to go.
- Resolves: rhbz#1325423

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Turn tests back on or build will not fail.
- Resolves: rhbz#1325423

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Temporarily remove power64 from JIT arches to see if endian issue appears on Zero.
- Resolves: rhbz#1325423

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Turn off Java-based checks in a vain attempt to get a complete build.
- Resolves: rhbz#1325423

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Turn off -Werror so s390 can build in slowdebug mode.
- Add fix for formatting issue found by previous s390 build.
- Resolves: rhbz#1325423

* Tue Apr 12 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Revert settings to production defaults so we can at least get a build.
- Switch to a slowdebug build to try and unearth remaining issue on s390x.
- Resolves: rhbz#1325423

* Mon Apr 11 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Disable ECDSA test for now until failure on RHEL 7 is fixed.
- Resolves: rhbz#1325423

* Mon Apr 11 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Add 8132051 port to Zero.
- Turn on bootstrap build for all to ensure we are now good to go.
- Resolves: rhbz#1325423

* Mon Apr 11 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Add 8132051 port to AArch64.
- Resolves: rhbz#1325423

* Mon Apr 11 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Enable a full bootstrap on JIT archs. Full build held back by Zero archs anyway.
- Resolves: rhbz#1325423

* Sun Apr 10 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Use basename of test file to avoid misinterpretation of full path as a package
- Resolves: rhbz#1325423

* Sun Apr 10 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.91-1.b14
- Update to u91b14.
- Resolves: rhbz#1325423

* Thu Mar 31 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-3.b03
- Fix typo in test invocation.
- Resolves: rhbz#1245810

* Thu Mar 31 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-3.b03
- Add ECDSA test to ensure ECC is working.
- Resolves: rhbz#1245810

* Wed Mar 30 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.77-2.b03
- Avoid WithSeed versions of NSS functions as they do not fully process the seed
- List current java.security md5sum so that java.security is replaced and ECC gets enabled.
- Resolves: rhbz#1245810

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

* Mon Feb 29 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-5.b16
- Update to u72b16.
- Drop 8147805 and jvm.cfg fix which are applied upstream.
- Resolves: rhbz#1307108

* Wed Feb 24 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-4.b15
- Add patches to allow the SunEC provider to be built with the system NSS install.
- Re-generate source tarball so it includes ecc_impl.h.
- Adjust tarball generation script to allow ecc_impl.h to be included.
- Bring over NSS changes from java-1.7.0-openjdk spec file (NSS_CFLAGS/NSS_LIBS)
- Remove patch which disables the SunEC provider as it is now usable.
- Correct spelling mistakes in tarball generation script.
- Resolves: rhbz#1245810

* Wed Feb 24 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-4.b15
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

* Fri Feb 19 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-1.b15
- Add backport of 8147805: aarch64: C1 segmentation fault due to inline Unsafe.getAndSetObject
- Resolves: rhbz#1300630

* Thu Feb 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Remove unnecessary AArch64 port divergence on parsing jvm.cfg, broken by 9399aa7ef558
- Resolves: rhbz#1307108

* Thu Feb 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Only use z format specifier on s390, not s390x.
- Resolves: rhbz#1307108

* Wed Feb 17 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Remove fragment of s390 size_t patch that unnecessarily removes a cast, breaking ppc64le.
- Remove aarch64-specific suffix as update/build version are now the same as for other archs.
- Resolves: rhbz#1307108

* Wed Feb 17 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.72-0.b15
- Replace s390 Java options patch with general version from IcedTea.
- Apply s390 patches unconditionally to avoid arch-specific patch failures.
- Resolves: rhbz#1307108

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

* Wed Jan 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- Change correct specifier in src/share/vm/memory/blockOffsetTable.cpp
- Resolves: rhbz#1295754

* Wed Jan 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- Make bootstrap build optional and turn it off by default.
- Fix remaining warnings in s390 fix and re-enable -Werror
- Resolves: rhbz#1295754

* Wed Jan 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- Add additional fixes for s390 warnings in arguments.cpp
- Temporarily turn off -Werror on s390 to make progress
- Resolves: rhbz#1295754

* Wed Jan 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- Actually apply the S390 fix...
- Resolves: rhbz#1295754

* Wed Jan 13 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.71-1.b15
- Turn off additional CFLAGS/LDFLAGS on AArch64 as bootstrapping failed.
- Add patch for size_t formatting on s390 as size_t != intptr_t there.
- Resolves: rhbz#1295754

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

* Fri Sep 04 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.60-4.b27
- priority aligned to 7digits (sync with 6.8)
- Resolves: rhbz#1255350

* Fri Aug 28 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.8.0.60-2.b27
- updated to u60
- Resolves: rhbz#1255350

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

* Wed Mar 18 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-7.b13
- Set archinstall to ppc64le on that platform.
- Resolves: rhbz#1194378

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

* Wed Feb 18 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Override ppc64le as ppc64 only in hotspot-spec.gmk so as not to disrupt JDK build.
- Add property test case from java-1.7.0-openjdk build.
- Resolves: rhbz#1194378

* Wed Feb 18 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Set OPENJDK_TARGET_CPU_LEGACY to ppc64 so as not to mess up HotSpot build.
- Add -DABI_ELFv2 to CFLAGS on ppc64le to match OpenJDK 7.
- Print contents of hotspot-spec.gmk
- Resolves: rhbz#1194378

* Wed Feb 18 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Fix path to spec.gmk.
- Resolves: rhbz#1194378

* Tue Feb 17 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Print contents of spec.gmk to see what is being passed to the HotSpot build.
- Resolves: rhbz#1194378

* Tue Feb 17 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Remove patch to generated-configure.sh as RPM re-generates it.
- Resolves: rhbz#1194378

* Tue Feb 17 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Fix configure script to use ppc64le, not ppc64.
- Add ppc64le support to LIBJSOUND_CFLAGS.
- Add a jvm.cfg for ppc64le
- Resolves: rhbz#1194378

* Tue Feb 17 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-4.b13
- Report ppc64le as the architecture on ppc64le, not ppc64.
- Resolves: rhbz#1194378

* Tue Jan 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.8.0.31-3.b13
- Depend on java-1.7.0-openjdk to build instead.
- Resolves: rhbz#1194378

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

* Thu Feb 13 2014 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.26.b129
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

* Mon Jul 15 2013 Omair Majid <omajid@redhat.com> - 1:1.8.0.0-0.9.b89
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
