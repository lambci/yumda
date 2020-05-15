%define buildid 139.254

# We have to override the new %%install behavior because, well... the kernel is special.
%global __spec_install_pre %%{___build_pre}

Summary: The Linux kernel

# Amazon: Enable module signing and disable efi
%global signmodules 1
%global usingefi 0

# Save original buildid for later if it's defined
%if 0%{?buildid:1}
%global orig_buildid %{buildid}
%undefine buildid
%endif

# Tentatively set this macro to override .amzn1
%global dist .amzn2

###################################################################
# Polite request for people who spin their own kernel rpms:
# please modify the "buildid" define in a way that identifies
# that the kernel isn't the stock distribution kernel, for example,
# by setting the define to ".local" or ".bz123456". This will be
# appended to the full kernel version.
#
# (Uncomment the '#' and both spaces below to set the buildid.)
#
# %% define buildid .local
###################################################################

# The buildid can also be specified on the rpmbuild command line
# by adding --define="buildid .whatever". If both the specfile and
# the environment define a buildid they will be concatenated together.
%if 0%{?orig_buildid:1}
%if 0%{?buildid:1}
%global srpm_buildid %{buildid}
%define buildid %{srpm_buildid}%{orig_buildid}
%else
%define buildid %{orig_buildid}
%endif
%endif

# what kernel is it we are building
%global kversion 4.14.177
%define rpmversion %{kversion}

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them.
#
# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# kernel-debug
%define with_debug     %{?_without_debug:     0} %{?!_without_debug:     0}
# kernel-doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       0}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
# perf
%define with_perf      %{?_without_perf:      0} %{?!_without_perf:      1}
# tools
%define with_tools     %{?_without_tools:     0} %{?!_without_tools:     1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# Want to build a the vsdo directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
# Use dracut instead of mkinitrd for initrd image generation
%define with_dracut       %{?_without_dracut:       0} %{?!_without_dracut:       1}
# Control whether we build the hmac for fips mode
%define with_fips      %{?_without_fips:       0} %{?!_without_fips:   1}

# Build the kernel-doc package, but don't fail the build if it botches.
# Here "true" means "continue" and "false" means "fail the build".
%define doc_build_fail true

# should we do C=1 builds with sparse
%define with_sparse	%{?_with_sparse:      1} %{?!_with_sparse:      0}

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 0

# do we want the oldconfig run over the config files (when regenerating
# configs this should be avoided in order to save duplicate work...)
%define with_oldconfig     %{?_without_oldconfig:      0} %{?!_without_oldconfig:      1}

# pkg_release is what we'll fill in for the rpm Release: field
%define pkg_release %{?buildid}%{?dist}

%define make_target bzImage

%define KVERREL %{rpmversion}-%{pkg_release}.%{_target_cpu}
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug

%define all_x86 i386 i686

%if %{with_vdso_install}
# These arches install vdso/ directories.
%define vdso_arches x86_64 aarch64
%endif

# Overrides for generic default options

# don't do debug builds on anything but i686 and x86_64
%ifnarch i686 x86_64 aarch64
%define with_debug 0
%endif

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%endif

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_tools 0
%define with_perf 0
%define signmodules 0
%define all_arch_configs kernel-%{version}-*.config
%endif

# Per-arch tweaks

%ifarch %{all_x86}
%define asmarch x86
%define hdrarch i386
%define all_arch_configs kernel-%{version}-i?86*.config
%define image_install_path boot
%define kernel_image arch/%{asmarch}/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define all_arch_configs kernel-%{version}-x86_64*.config
%define image_install_path boot
%define kernel_image arch/%{asmarch}/boot/bzImage
%endif

%ifarch aarch64
%define all_arch_configs kernel-%{version}-aarch64*.config
%define asmarch arm64
%define hdrarch arm64
%define image_install_path boot
%define make_target Image
%define kernel_image arch/%{asmarch}/boot/Image
%define with_perf 1
%endif

# amazon: don't use nonint config target - we want to know when our config files are
# not complete
%define oldconfig_target oldconfig

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We don't build a kernel on i386; we only do kernel-headers there
%define nobuildarches i386 i486 i586 i686 noarch

%ifarch %nobuildarches
%define with_up 0
%define with_debuginfo 0
%define with_perf 0
%define with_tools 0
%define _enable_debug_packages 0
%define signmodules 0
%endif

# Architectures we build tools/cpupower on
%define cpupowerarchs %{ix86} x86_64 aarch64
#define cpupowerarchs none

#
# Three sets of minimum package version requirements in the form of Conflicts:
# to versions below the minimum
#

#
# First the general kernel 2.6 required versions as per
# Documentation/Changes
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.2.5-7.fc17, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2, device-mapper-libs < 1.02.63-2, mdadm < 3.2.1-5

#
# Then a series of requirements that are distribution specific, either
# because we add patches for something, or the older versions have
# problems with the newer kernel or lack certain things that make
# integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0

# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  fileutils, module-init-tools, initscripts >= 8.11.1-1, grubby >= 7.0.15-2.5
%if %{with_dracut}
%define initrd_prereq  dracut >= 004-336.27, grubby >= 7.0.10-1
%else
%define initrd_prereq  mkinitrd >= 6.0.91
%endif
# XXX: fedora16 has a prereq grubby >= 8.3-1

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#	%%kernel_reqprovconf <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf \
Provides: kernel = %{rpmversion}-%{pkg_release}\
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:.%{1}}\
Provides: kernel-drm = 4.3.0\
Provides: kernel-drm-nouveau = 16\
Provides: kernel-modeset = 1\
Provides: kernel-uname-r = %{KVERREL}%{?1:.%{1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(post): %{_sbindir}/new-kernel-pkg\
Requires(preun): %{_sbindir}/new-kernel-pkg\
Conflicts: %{kernel_dot_org_conflicts}\
Conflicts: %{package_conflicts}\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}

Name: kernel%{?variant}
Group: System Environment/Kernel
License: GPLv2 and Redistributable, no modification permitted
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
ExclusiveArch: noarch i686 x86_64 aarch64
ExclusiveOS: Linux

%kernel_reqprovconf
%ifarch x86_64
Requires(pre): microcode_ctl >= 2:2.1-47.amzn2.0.4
%endif

%ifarch x86_64
Obsoletes: kernel-smp
%endif

%ifarch x86_64
Provides: kmod-lustre-client = 2.10.5
%endif


#
# List the packages used during the kernel build
#
BuildRequires: kmod >= 14, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildRequires: bzip2, findutils, gzip, m4, perl, make >= 3.78, diffutils, gawk
BuildRequires: gcc >= 7.2.1, hostname, openssl
# Required for kernel documentation build
%if %{with_doc}
BuildRequires: python-virtualenv, python-sphinx, ImageMagick-perl
%endif
#defines based on the compiler version we need to use
%global _gcc gcc
%global _gxx g++
%global _gccver %(eval %{_gcc} -dumpfullversion 2>/dev/null || :)
%if "%{_gccver}" > "7"
Provides: buildrequires(gcc) = %{_gccver}
%endif
BuildRequires: binutils >= 2.12
BuildRequires: system-rpm-config, gdb, bc
BuildRequires: net-tools
BuildRequires: xmlto, asciidoc
BuildRequires: openssl-devel
%if %{with_sparse}
BuildRequires: sparse >= 0.4.1
%endif
%if %{with_perf}
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison
BuildRequires: audit-libs-devel
BuildRequires: numactl-devel

%endif
%if %{with_tools}
BuildRequires: pciutils-devel gettext
%endif # tools
BuildConflicts: rhbuildsys(DiskFree) < 3000Mb

%define fancy_debuginfo 0
%if %{with_debuginfo}
%define fancy_debuginfo 1
%endif

%if %{fancy_debuginfo}
# Fancy new debuginfo generation introduced in Fedora 8.
BuildRequires: rpm-build >= 4.4.2.1-4
## The -r flag to find-debuginfo.sh invokes eu-strip --reloc-debug-sections
## which reduces the number of relocations in kernel module .ko.debug files and
## was introduced with rpm 4.9 and elfutils 0.153.
#BuildRequires: rpm-build >= 4.9.0-1, elfutils >= elfutils-0.153-1
#%define debuginfo_args --strict-build-id -r
%define debuginfo_args --strict-build-id
%endif

%if %{signmodules}
BuildRequires: pesign >= 0.10-4
%endif

%if %{with_fips}
BuildRequires: hmaccalc
%endif

Source0: linux-4.14.177.tar
Source1: linux-4.14.177-patches.tar

# this is for %{signmodules}
Source11: x509.genkey

Source15: kconfig.py
Source16: mod-extra.list
Source17: mod-extra.sh
Source18: mod-extra-sign.sh
%define modsign_cmd %{SOURCE18}

Source19: Makefile.config
Source20: config-x86_64
Source30: config-aarch64
Source50: split-man.pl
%define split_man_cmd %{SOURCE50}

# Sources for kernel-tools
Source2000: cpupower.init
Source2001: cpupower.config

# __PATCHFILE_TEMPLATE__
Patch0001: 0001-kbuild-AFTER_LINK.patch
Patch0002: 0002-scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
Patch0003: 0003-bump-the-default-TTL-to-255.patch
Patch0004: 0004-bump-default-tcp_wmem-from-16KB-to-20KB.patch
Patch0005: 0005-force-perf-to-use-usr-bin-python-instead-of-usr-bin-.patch
Patch0006: 0006-nvme-update-timeout-module-parameter-type.patch
Patch0007: 0007-not-for-upstream-testmgr-config-changes-to-enable-FI.patch
Patch0008: 0008-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
Patch0009: 0009-drivers-amazon-add-network-device-drivers-support.patch
Patch0010: 0010-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
Patch0011: 0011-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
Patch0012: 0012-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
Patch0013: 0013-xen-manage-introduce-helper-function-to-know-the-on-.patch
Patch0014: 0014-xenbus-add-freeze-thaw-restore-callbacks-support.patch
Patch0015: 0015-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
Patch0016: 0016-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
Patch0017: 0017-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch0018: 0018-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
Patch0019: 0019-xen-time-introduce-xen_-save-restore-_steal_clock.patch
Patch0020: 0020-x86-xen-save-and-restore-steal-clock.patch
Patch0021: 0021-xen-events-add-xen_shutdown_pirqs-helper-function.patch
Patch0022: 0022-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
Patch0023: 0023-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
Patch0024: 0024-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
Patch0025: 0025-xen-blkfront-resurrect-request-based-mode.patch
Patch0026: 0026-xen-blkfront-add-persistent_grants-parameter.patch
Patch0027: 0027-ACPI-SPCR-Make-SPCR-available-to-x86.patch
Patch0028: 0028-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
Patch0029: 0029-locking-paravirt-Use-new-static-key-for-controlling-.patch
Patch0030: 0030-KVM-Introduce-paravirtualization-hints-and-KVM_HINTS.patch
Patch0031: 0031-KVM-X86-Choose-qspinlock-when-dedicated-physical-CPU.patch
Patch0032: 0032-x86-paravirt-Set-up-the-virt_spin_lock_key-after-sta.patch
Patch0033: 0033-KVM-X86-Fix-setup-the-virt_spin_lock_key-before-stat.patch
Patch0034: 0034-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
Patch0035: 0035-x86-tsc-avoid-system-instability-in-hibernation.patch
Patch0036: 0036-blk-mq-simplify-queue-mapping-schedule-with-each-pos.patch
Patch0037: 0037-blk-wbt-Avoid-lock-contention-and-thundering-herd-is.patch
Patch0038: 0038-x86-MCE-AMD-Read-MCx_MISC-block-addresses-on-any-CPU.patch
Patch0039: 0039-x86-CPU-Rename-intel_cacheinfo.c-to-cacheinfo.c.patch
Patch0040: 0040-x86-CPU-AMD-Calculate-last-level-cache-ID-from-numbe.patch
Patch0041: 0041-x86-CPU-AMD-Fix-LLC-ID-bit-shift-calculation.patch
Patch0042: 0042-sched-topology-Introduce-NUMA-identity-node-sched-do.patch
Patch0043: 0043-x86-CPU-AMD-Derive-CPU-topology-from-CPUID-function-.patch
Patch0044: 0044-vmxnet3-increase-default-rx-ring-sizes.patch
Patch0045: 0045-block-xen-blkfront-consider-new-dom0-features-on-res.patch
Patch0046: 0046-ACPICA-Enable-sleep-button-on-ACPI-legacy-wake.patch
Patch0047: 0047-xen-restore-pirqs-on-resume-from-hibernation.patch
Patch0048: 0048-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
Patch0049: 0049-net-ena-Import-the-ENA-v2-driver-2.0.2g.patch
Patch0050: 0050-arm64-export-memblock_reserve-d-regions-via-proc-iom.patch
Patch0051: 0051-arm64-Fix-proc-iomem-for-reserved-but-not-memory-reg.patch
Patch0052: 0052-efi-arm64-Check-whether-x18-is-preserved-by-runtime-.patch
Patch0053: 0053-arm64-kexec-always-reset-to-EL2-if-present.patch
Patch0054: 0054-arm64-acpi-fix-alignment-fault-in-accessing-ACPI.patch
Patch0055: 0055-ACPICA-ACPI-6.2-Additional-PPTT-flags.patch
Patch0056: 0056-drivers-base-cacheinfo-move-cache_setup_of_node.patch
Patch0057: 0057-drivers-base-cacheinfo-setup-DT-cache-properties-ear.patch
Patch0058: 0058-cacheinfo-rename-of_node-to-fw_token.patch
Patch0059: 0059-arm64-acpi-Create-arch-specific-cpu-to-acpi-id-helpe.patch
Patch0060: 0060-ACPI-PPTT-Add-Processor-Properties-Topology-Table-pa.patch
Patch0061: 0061-ACPI-Enable-PPTT-support-on-ARM64.patch
Patch0062: 0062-drivers-base-cacheinfo-Add-support-for-ACPI-based-fi.patch
Patch0063: 0063-arm64-Add-support-for-ACPI-based-firmware-tables.patch
Patch0064: 0064-arm64-topology-rename-cluster_id.patch
Patch0065: 0065-arm64-topology-enable-ACPI-PPTT-based-CPU-topology.patch
Patch0066: 0066-ACPI-Add-PPTT-to-injectable-table-list.patch
Patch0067: 0067-arm64-topology-divorce-MC-scheduling-domain-from-cor.patch
Patch0068: 0068-ACPI-PPTT-use-ACPI-ID-whenever-ACPI_PPTT_ACPI_PROCES.patch
Patch0069: 0069-ACPI-PPTT-fix-build-when-CONFIG_ACPI_PPTT-is-not-ena.patch
Patch0070: 0070-ACPI-PPTT-Handle-architecturally-unknown-cache-types.patch
Patch0071: 0071-xen-netfront-call-netif_device_attach-on-resume.patch
Patch0072: 0072-xfs-refactor-superblock-verifiers.patch
Patch0073: 0073-libxfs-add-more-bounds-checking-to-sb-sanity-checks.patch
Patch0074: 0074-xfs-only-validate-summary-counts-on-primary-superblo.patch
Patch0075: 0075-xfs-iomap-define-and-use-the-IOMAP_F_DIRTY-flag-in-x.patch
Patch0076: 0076-iomap-add-a-swapfile-activation-function.patch
Patch0077: 0077-iomap-provide-more-useful-errors-for-invalid-swap-fi.patch
Patch0078: 0078-iomap-don-t-allow-holes-in-swapfiles.patch
Patch0079: 0079-iomap-inline-data-should-be-an-iomap-type-not-a-flag.patch
Patch0080: 0080-iomap-fsync-swap-files-before-iterating-mappings.patch
Patch0081: 0081-Import-lustre-client-2.10.5.patch
Patch0082: 0082-Config-glue-for-lustre-client.patch
Patch0083: 0083-net-allow-per-netns-sysctl_rmem-and-sysctl_wmem-for-.patch
Patch0084: 0084-tcp-Namespace-ify-sysctl_tcp_rmem-and-sysctl_tcp_wme.patch
Patch0085: 0085-Add-new-config-CONFIG_MICROVM-to-enable-microvm-opti.patch
Patch0086: 0086-x86-stacktrace-Do-not-unwind-after-user-regs.patch
Patch0087: 0087-x86-stacktrace-Remove-STACKTRACE_DUMP_ONCE.patch
Patch0088: 0088-x86-stacktrace-Clarify-the-reliable-success-paths.patch
Patch0089: 0089-x86-stacktrace-Do-not-fail-for-ORC-with-regs-on-stac.patch
Patch0090: 0090-x86-unwind-orc-Detect-the-end-of-the-stack.patch
Patch0091: 0091-x86-stacktrace-Enable-HAVE_RELIABLE_STACKTRACE-for-t.patch
Patch0092: 0092-lustre-fix-ACL-handling.patch
Patch0093: 0093-irqchip-gic-v2m-invoke-from-gic-v3-initialization-an.patch
Patch0094: 0094-PCI-al-Add-Amazon-Annapurna-Labs-PCIe-host-controlle.patch
Patch0095: 0095-arm64-acpi-pci-invoke-_DSM-whether-to-preserve-firmw.patch
Patch0096: 0096-NFS-Remove-redundant-semicolon.patch
Patch0097: 0097-Fix-microvm-config-dependency-in-Kconfig.patch
Patch0098: 0098-microvm-enable-debug-in-case-of-tcp-out-of-memory.patch
Patch0099: 0099-linux-ena-update-ENA-linux-driver-to-version-2.1.1.patch
Patch0100: 0100-PCI-Add-Amazon-s-Annapurna-Labs-vendor-ID.patch
Patch0101: 0101-PCI-Add-ACS-quirk-for-Amazon-Annapurna-Labs-root-por.patch
Patch0102: 0102-Partially-revert-cc946adcb9e983ad9fe56ebe35f1292e111.patch
Patch0103: 0103-livepatch-introduce-shadow-variable-API.patch
Patch0104: 0104-livepatch-__klp_shadow_get_or_alloc-is-local-to-shad.patch
Patch0105: 0105-livepatch-add-un-patch-callbacks.patch
Patch0106: 0106-livepatch-move-transition-complete-notice-into-klp_c.patch
Patch0107: 0107-livepatch-add-transition-notices.patch
Patch0108: 0108-livepatch-Correctly-call-klp_post_unpatch_callback-i.patch
Patch0109: 0109-livepatch-__klp_disable_patch-should-never-be-called.patch
Patch0110: 0110-livepatch-send-a-fake-signal-to-all-blocking-tasks.patch
Patch0111: 0111-livepatch-force-transition-to-finish.patch
Patch0112: 0112-livepatch-Remove-immediate-feature.patch
Patch0113: 0113-livepatch-add-locking-to-force-and-signal-functions.patch
Patch0114: 0114-livepatch-Initialize-shadow-variables-safely-by-a-cu.patch
Patch0115: 0115-livepatch-Allow-to-call-a-custom-callback-when-freei.patch
Patch0116: 0116-livepatch-Remove-reliable-stacktrace-check-in-klp_tr.patch
Patch0117: 0117-livepatch-Replace-synchronize_sched-with-synchronize.patch
Patch0118: 0118-livepatch-Change-unsigned-long-old_addr-void-old_fun.patch
Patch0119: 0119-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
Patch0120: 0120-block-add-io-timeout-to-sysfs.patch
Patch0121: 0121-block-don-t-show-io_timeout-if-driver-has-no-timeout.patch
Patch0122: 0122-Add-Amazon-EFA-driver-version-1.4.patch
Patch0123: 0123-percpu-refcount-Introduce-percpu_ref_resurrect.patch
Patch0124: 0124-block-Allow-unfreezing-of-a-queue-while-requests-are.patch
Patch0125: 0125-nvme-change-namespaces_mutext-to-namespaces_rwsem.patch
Patch0126: 0126-blk-mq-fix-hang-caused-by-freeze-unfreeze-sequence.patch
Patch0127: 0127-nvme-move-the-dying-queue-check-from-cancel-to-compl.patch
Patch0128: 0128-nvme-pci-Better-support-for-disabling-controller.patch
Patch0129: 0129-nvme-host-core-Allow-overriding-of-wait_ready-timeou.patch
Patch0130: 0130-nvme-host-pci-Fix-a-race-in-controller-removal.patch
Patch0131: 0131-nvme-pci-move-cq_vector-1-check-outside-of-q_lock.patch
Patch0132: 0132-irqchip-gic-v3-its-Pass-its_node-pointer-to-each-com.patch
Patch0133: 0133-irqchip-gic-v3-its-Only-emit-SYNC-if-targetting-a-va.patch
Patch0134: 0134-irqchip-gic-v3-its-Only-emit-VSYNC-if-targetting-a-v.patch
Patch0135: 0135-irqchip-gic-v3-its-Refactor-LPI-allocator.patch
Patch0136: 0136-irqchip-gic-v3-its-Use-full-range-of-LPIs.patch
Patch0137: 0137-irqchip-gic-v3-its-Move-minimum-LPI-requirements-to-.patch
Patch0138: 0138-irqchip-gic-v3-its-Drop-chunk-allocation-compatibili.patch
Patch0139: 0139-irqchip-gic-v3-Expose-GICD_TYPER-in-the-rdist-struct.patch
Patch0140: 0140-irqchip-gic-v3-its-Honor-hypervisor-enforced-LPI-ran.patch
Patch0141: 0141-irqchip-gic-v3-its-Reduce-minimum-LPI-allocation-to-.patch
Patch0142: 0142-irqchip-gic-v3-its-Cap-lpi_id_bits-to-reduce-memory-.patch
Patch0143: 0143-irqchip-gic-v3-its-Gracefully-fail-on-LPI-exhaustion.patch
Patch0144: 0144-irqchip-gic-v3-its-Fix-comparison-logic-in-lpi_range.patch
Patch0145: 0145-iommu-io-pgtable-arm-Convert-to-IOMMU-API-TLB-sync.patch
Patch0146: 0146-iommu-io-pgtable-arm-v7s-Convert-to-IOMMU-API-TLB-sy.patch
Patch0147: 0147-iommu-arm-smmu-v3-Implement-flush_iotlb_all-hook.patch
Patch0148: 0148-iommu-dma-Add-support-for-non-strict-mode.patch
Patch0149: 0149-iommu-Add-iommu.strict-command-line-option.patch
Patch0150: 0150-iommu-io-pgtable-arm-Add-support-for-non-strict-mode.patch
Patch0151: 0151-iommu-arm-smmu-v3-Add-support-for-non-strict-mode.patch
Patch0152: 0152-iommu-io-pgtable-arm-v7s-Add-support-for-non-strict-.patch
Patch0153: 0153-iommu-arm-smmu-Support-non-strict-mode.patch
Patch0154: 0154-iommu-use-config-option-to-specify-if-iommu-mode-sho.patch
Patch0155: 0155-locking-atomic-Add-atomic_cond_read_acquire.patch
Patch0156: 0156-locking-barriers-Introduce-smp_cond_load_relaxed-and.patch
Patch0157: 0157-locking-qspinlock-Use-atomic_cond_read_acquire.patch
Patch0158: 0158-locking-mcs-Use-smp_cond_load_acquire-in-MCS-spin-lo.patch
Patch0159: 0159-locking-qspinlock-Use-smp_cond_load_relaxed-to-wait-.patch
Patch0160: 0160-locking-qspinlock-Use-smp_store_release-in-queued_sp.patch
Patch0161: 0161-locking-qspinlock-Elide-back-to-back-RELEASE-operati.patch
Patch0162: 0162-locking-qspinlock-Use-try_cmpxchg-instead-of-cmpxchg.patch
Patch0163: 0163-MAINTAINERS-Add-myself-as-a-co-maintainer-for-the-lo.patch
Patch0164: 0164-arm64-barrier-Implement-smp_cond_load_relaxed.patch
Patch0165: 0165-arm64-locking-Replace-ticket-lock-implementation-wit.patch
Patch0166: 0166-arm64-kconfig-Ensure-spinlock-fastpaths-are-inlined-.patch
Patch0167: 0167-arm64-pull-in-upstream-erratum-workarounds.patch
Patch0168: 0168-arm64-Avoid-flush_icache_range-in-alternatives-patch.patch
Patch0169: 0169-update-ena-driver-to-version-2.1.3.patch
Patch0170: 0170-Revert-nvme-pci-Better-support-for-disabling-control.patch
Patch0171: 0171-nvme-pci-introduce-RECONNECTING-state-to-mark-initia.patch
Patch0172: 0172-nvme-allow-controller-RESETTING-to-RECONNECTING-tran.patch
Patch0173: 0173-nvme-rename-NVME_CTRL_RECONNECTING-state-to-NVME_CTR.patch
Patch0174: 0174-nvme-pci-Fix-timeouts-in-connecting-state.patch
Patch0175: 0175-nvme-pci-shutdown-on-timeout-during-deletion.patch
Patch0176: 0176-nvme-pci-Unblock-reset_work-on-IO-failure.patch
Patch0177: 0177-nvme-pci-Don-t-disable-on-timeout-in-reset-state.patch
Patch0178: 0178-nvme-pci-use-atomic-bitops-to-mark-a-queue-enabled.patch
Patch0179: 0179-arm64-fix-merge-error-in-errata-changes.patch
Patch0180: 0180-lustre-hold-lock-while-walking-changelog-dev-list.patch
Patch0181: 0181-Revert-Fix-the-locking-in-dcache_readdir-and-friends.patch
Patch0182: 0182-drivers-amazon-efa-update-to-1.5.0.patch
Patch0183: 0183-SMB3-Backup-intent-flag-missing-from-compounded-ops.patch
Patch0184: 0184-Add-support-for-setting-owner-info-dos-attributes-an.patch
Patch0185: 0185-update-ENA-linux-driver-to-version-2.2.1.patch
Patch0186: 0186-Revert-update-ENA-linux-driver-to-version-2.2.1.patch
Patch0187: 0187-kunit-test-add-KUnit-test-runner-core.patch
Patch0188: 0188-kunit-test-add-test-resource-management-API.patch
Patch0189: 0189-kunit-test-add-string_stream-a-std-stream-like-strin.patch
Patch0190: 0190-kunit-test-add-assertion-printing-library.patch
Patch0191: 0191-kunit-test-add-the-concept-of-expectations.patch
Patch0192: 0192-lib-enable-building-KUnit-in-lib.patch
Patch0193: 0193-kunit-test-add-initial-tests.patch
Patch0194: 0194-kunit-test-add-support-for-test-abort.patch
Patch0195: 0195-kunit-test-add-tests-for-kunit-test-abort.patch
Patch0196: 0196-kunit-test-add-the-concept-of-assertions.patch
Patch0197: 0197-kunit-test-add-tests-for-KUnit-managed-resources.patch
Patch0198: 0198-kunit-fix-failure-to-build-without-printk.patch
Patch0199: 0199-kunit-tool-add-Python-wrappers-for-running-KUnit-tes.patch
Patch0200: 0200-kunit-defconfig-add-defconfigs-for-building-KUnit-te.patch
Patch0201: 0201-kunit-Fix-build_dir-option.patch
Patch0202: 0202-Documentation-kunit-add-documentation-for-KUnit.patch
Patch0203: 0203-Documentation-kunit-Fix-verification-command.patch
Patch0204: 0204-lib-list-test-add-a-test-for-the-list-doubly-linked-.patch
Patch0205: 0205-cifs-Fix-slab-out-of-bounds-in-send_set_info-on-SMB2.patch
Patch0206: 0206-CIFS-don-t-log-STATUS_NOT_FOUND-errors-for-DFS.patch
Patch0207: 0207-Don-t-log-expected-error-on-DFS-referral-request.patch
Patch0208: 0208-Don-t-log-confusing-message-on-reconnect-by-default.patch
Patch0209: 0209-genirq-export-irq_get_percpu_devid_partition-to-modu.patch
Patch0210: 0210-perf-core-Export-AUX-buffer-helpers-to-modules.patch
Patch0211: 0211-perf-core-Add-PERF_AUX_FLAG_COLLISION-to-report-coll.patch
Patch0212: 0212-arm64-sysreg-Move-SPE-registers-and-PSB-into-common-.patch
Patch0213: 0213-arm64-head-Init-PMSCR_EL2.-PA-PCT-when-entered-at-EL.patch
Patch0214: 0214-dt-bindings-Document-devicetree-binding-for-ARM-SPE.patch
Patch0215: 0215-drivers-perf-Add-support-for-ARMv8.2-Statistical-Pro.patch
Patch0216: 0216-perf-tools-Add-ARM-Statistical-Profiling-Extensions-.patch
Patch0217: 0217-perf-arm-spe-Fix-uninitialized-record-error-variable.patch
Patch0218: 0218-ACPICA-ACPI-6.3-MADT-add-support-for-statistical-pro.patch
Patch0219: 0219-ACPICA-ACPI-6.3-PPTT-add-additional-fields-in-Proces.patch
Patch0220: 0220-ACPI-PPTT-Modify-node-flag-detection-to-find-last-ID.patch
Patch0221: 0221-ACPI-PPTT-Add-function-to-return-ACPI-6.3-Identical-.patch
Patch0222: 0222-arm_pmu-acpi-spe-Add-initial-MADT-SPE-probing.patch
Patch0223: 0223-perf-arm_spe-Enable-ACPI-Platform-automatic-module-l.patch
Patch0224: 0224-ena-update-to-2.2.3.patch
Patch0225: 0225-random-try-to-actively-add-entropy-rather-than-passi.patch
Patch0226: 0226-random-introduce-RANDOM_WAIT_JITTER-config-option.patch
Patch0227: 0227-lustre-update-to-AmazonFSxLustreClient-v2.10.8-1.patch
Patch0228: 0228-Revert-ena-update-to-2.2.3.patch
Patch0229: 0229-kernel-sched-fair.c-Fix-divide-by-zero.patch
Patch0230: 0230-efi-honour-memory-reservations-passed-via-a-linux-sp.patch
Patch0231: 0231-efi-arm-libstub-add-a-root-memreserve-config-table.patch
Patch0232: 0232-efi-add-API-to-reserve-memory-persistently-across-ke.patch
Patch0233: 0233-efi-Permit-calling-efi_mem_reserve_persistent-from-a.patch
Patch0234: 0234-efi-Prevent-GICv3-WARN-by-mapping-the-memreserve-tab.patch
Patch0235: 0235-efi-Permit-multiple-entries-in-persistent-memreserve.patch
Patch0236: 0236-efi-Reduce-the-amount-of-memblock-reservations-for-p.patch
Patch0237: 0237-efi-memreserve-deal-with-memreserve-entries-in-unmap.patch
Patch0238: 0238-efi-memreserve-Register-reservations-as-reserved-in-.patch
Patch0239: 0239-irqchip-gic-v3-Ensure-GICR_CTLR.EnableLPI-0-is-obser.patch
Patch0240: 0240-irqchip-gic-v3-its-Change-initialization-ordering-fo.patch
Patch0241: 0241-irqchip-gic-v3-its-Simplify-LPI_PENDBASE_SZ-usage.patch
Patch0242: 0242-irqchip-gic-v3-its-Split-property-table-clearing-fro.patch
Patch0243: 0243-irqchip-gic-v3-its-Move-pending-table-allocation-to-.patch
Patch0244: 0244-irqchip-gic-v3-its-Keep-track-of-property-table-s-PA.patch
Patch0245: 0245-irqchip-gic-v3-its-Allow-use-of-pre-programmed-LPI-t.patch
Patch0246: 0246-irqchip-gic-v3-its-Use-pre-programmed-redistributor-.patch
Patch0247: 0247-irqchip-gic-v3-its-Check-that-all-RDs-have-the-same-.patch
Patch0248: 0248-irqchip-gic-v3-its-Register-LPI-tables-with-EFI-conf.patch
Patch0249: 0249-irqchip-gic-v3-its-Allow-use-of-LPI-tables-in-reserv.patch
Patch0250: 0250-iommu-arm-smmu-v3-Prevent-any-devices-access-to-memo.patch
Patch0251: 0251-iommu-arm-smmu-v3-Abort-all-transactions-if-SMMU-is-.patch
Patch0252: 0252-iommu-arm-smmu-v3-Don-t-disable-SMMU-in-kdump-kernel.patch
Patch0253: 0253-netlabel-cope-with-NULL-catmap.patch

BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Group: Development/Debug
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

%if %{with_perf}
%package -n perf
Summary: Performance monitoring for the Linux kernel
Group: Development/System
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n perf-debuginfo
Summary: Debug information for package perf
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|.*%%{_libdir}/traceevent/plugins/.*|XXX' -o perf-debuginfo.list}

%package -n python-perf
Summary: Python bindings for apps which will manipulate perf events
Group: Development/Libraries
%description -n python-perf
The python-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%package -n python-perf-debuginfo
Summary: Debug information for package perf python bindings
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n python-perf-debuginfo
This package provides debug information for the perf python bindings.

%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{python_sitearch}/perf.so(\.debug)?|XXX' -o python-perf-debuginfo.list}

%endif #perf

%if %{with_tools}
%package tools
Summary: Assortment of tools for the Linux kernel
Group: Development/System
License: GPLv2
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16

%description tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package tools-devel
Summary: Assortment of tools for the Linux kernel
Group: Development/System
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
%ifarch %{cpupowerarchs}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
%endif # cpupower

%description tools-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package tools-debuginfo
Summary: Debug information for package kernel-tools
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description tools-debuginfo
This package provides debug information for package kernel-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|XXX' -o kernel-tools-debuginfo.list}
%endif

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#	%%kernel_debuginfo_package <subpackage>
#
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Group: Development/Debug\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
AutoReqProv: no\
%description -n %{name}%{?1:-%{1}}-debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '/.*/%%{KVERREL}%{?1:\.%{1}}/.*|/.*%%{KVERREL}%{?1:\.%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#	%%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: kernel%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel-devel = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{?1:.%{1}}\
AutoReqProv: no\
Requires(pre): %{_bindir}/find\
Requires(post): %{_sbindir}/hardlink\
Requires: perl\
Requires: elfutils-libelf-devel\
Requires: gcc >= 7.2.1\
%if  "%{_gccver}" > "7"\
Provides: buildrequires(gcc) = %{_gccver}\
%endif\
%description -n kernel%{?variant}%{?1:-%{1}}-devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package %1\
Summary: %{variant_summary}\
Group: System Environment/Kernel\
%kernel_reqprovconf\
%{expand:%%kernel_devel_package %1 %{!?-n:%1}%{?-n:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %1}\
%{nil}


# First the auxiliary packages of the main kernel package.
%kernel_devel_package
%kernel_debuginfo_package


# Now, each variant package.

%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description debug
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.


%prep
# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='patch -p1 -F1 -s'

ApplyNoCheckPatch()
{
  local patch=$1
  shift
  case "$patch" in
    *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
    *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
    *) $patch_command ${1+"$@"} < $patch ;;
  esac
}

ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  if ! grep -E "^Patch[0-9]+: $patch\$" %{_specdir}/${RPM_PACKAGE_NAME%%%%%{?variant}}.spec ; then
    if [ "${patch:0:8}" != "patch-3." ] ; then
      echo "ERROR: Patch  $patch  not listed as a source patch in specfile"
      exit 1
    fi
  fi 2>/dev/null
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# don't apply patch if it's empty
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}

# First we unpack the kernel tarball.
# If this isn't the first make prep, we use links to the existing clean tarball
# which speeds things up quite a bit.

# Update to latest upstream.
%define vanillaversion %{kversion}

# %%{vanillaversion} : the full version name, e.g. 2.6.35-rc6-git3
# %%{kversion}       : the base version, e.g. 2.6.34

# Use kernel-%%{kversion}%%{?dist} as the top-level directory name
# so we can prep different trees within a single git directory.

%setup -q -n kernel-%{kversion}%{?dist} -c
mv linux-%{vanillaversion} vanilla-%{vanillaversion}

%if "%{kversion}" != "%{vanillaversion}"
# Need to apply patches to the base vanilla version.
pushd vanilla-%{vanillaversion} && popd

%endif

# Now build the fedora kernel tree.
if [ -d linux-%{KVERREL} ]; then
  # Just in case we ctrl-c'd a prep already
  rm -rf deleteme.%{_target_cpu}
  # Move away the stale away, and delete in background.
  mv linux-%{KVERREL} deleteme.%{_target_cpu}
  rm -rf deleteme.%{_target_cpu} &
fi

cp -rl vanilla-%{vanillaversion} linux-%{KVERREL}

cd linux-%{KVERREL}
tar xf %{SOURCE1}

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/config-* .
cp %{SOURCE15} .

%ifnarch %nobuildarches
# Dynamically generate kernel .config files from config-* files
make -f %{SOURCE19} VERSION=%{version} config
%endif

# apply the patches we had included in the -patches tarball. We use the
# linux-KVER-patches.list hardcoded apply log filename
patch_list=linux-%{kversion}-patches.list
if [ ! -f ${patch_list} ] ; then
    echo "ERROR: patch file apply log is missing: ${patch_list} not found"
    exit -1
fi
for p in `cat $patch_list` ; do
  ApplyNoCheckPatch ${p}
done

# __APPLYFILE_TEMPLATE__
ApplyPatch 0001-kbuild-AFTER_LINK.patch
ApplyPatch 0002-scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
ApplyPatch 0003-bump-the-default-TTL-to-255.patch
ApplyPatch 0004-bump-default-tcp_wmem-from-16KB-to-20KB.patch
ApplyPatch 0005-force-perf-to-use-usr-bin-python-instead-of-usr-bin-.patch
ApplyPatch 0006-nvme-update-timeout-module-parameter-type.patch
ApplyPatch 0007-not-for-upstream-testmgr-config-changes-to-enable-FI.patch
ApplyPatch 0008-drivers-introduce-AMAZON_DRIVER_UPDATES.patch
ApplyPatch 0009-drivers-amazon-add-network-device-drivers-support.patch
ApplyPatch 0010-drivers-amazon-introduce-AMAZON_ENA_ETHERNET.patch
ApplyPatch 0011-Importing-Amazon-ENA-driver-1.5.0-into-amazon-4.14.y.patch
ApplyPatch 0012-xen-manage-keep-track-of-the-on-going-suspend-mode.patch
ApplyPatch 0013-xen-manage-introduce-helper-function-to-know-the-on-.patch
ApplyPatch 0014-xenbus-add-freeze-thaw-restore-callbacks-support.patch
ApplyPatch 0015-x86-xen-Introduce-new-function-to-map-HYPERVISOR_sha.patch
ApplyPatch 0016-x86-xen-add-system-core-suspend-and-resume-callbacks.patch
ApplyPatch 0017-xen-blkfront-add-callbacks-for-PM-suspend-and-hibern.patch
ApplyPatch 0018-xen-netfront-add-callbacks-for-PM-suspend-and-hibern.patch
ApplyPatch 0019-xen-time-introduce-xen_-save-restore-_steal_clock.patch
ApplyPatch 0020-x86-xen-save-and-restore-steal-clock.patch
ApplyPatch 0021-xen-events-add-xen_shutdown_pirqs-helper-function.patch
ApplyPatch 0022-x86-xen-close-event-channels-for-PIRQs-in-system-cor.patch
ApplyPatch 0023-PM-hibernate-update-the-resume-offset-on-SNAPSHOT_SE.patch
ApplyPatch 0024-Not-for-upstream-PM-hibernate-Speed-up-hibernation-b.patch
ApplyPatch 0025-xen-blkfront-resurrect-request-based-mode.patch
ApplyPatch 0026-xen-blkfront-add-persistent_grants-parameter.patch
ApplyPatch 0027-ACPI-SPCR-Make-SPCR-available-to-x86.patch
ApplyPatch 0028-Revert-xen-dont-fiddle-with-event-channel-masking-in.patch
ApplyPatch 0029-locking-paravirt-Use-new-static-key-for-controlling-.patch
ApplyPatch 0030-KVM-Introduce-paravirtualization-hints-and-KVM_HINTS.patch
ApplyPatch 0031-KVM-X86-Choose-qspinlock-when-dedicated-physical-CPU.patch
ApplyPatch 0032-x86-paravirt-Set-up-the-virt_spin_lock_key-after-sta.patch
ApplyPatch 0033-KVM-X86-Fix-setup-the-virt_spin_lock_key-before-stat.patch
ApplyPatch 0034-xen-blkfront-Fixed-blkfront_restore-to-remove-a-call.patch
ApplyPatch 0035-x86-tsc-avoid-system-instability-in-hibernation.patch
ApplyPatch 0036-blk-mq-simplify-queue-mapping-schedule-with-each-pos.patch
ApplyPatch 0037-blk-wbt-Avoid-lock-contention-and-thundering-herd-is.patch
ApplyPatch 0038-x86-MCE-AMD-Read-MCx_MISC-block-addresses-on-any-CPU.patch
ApplyPatch 0039-x86-CPU-Rename-intel_cacheinfo.c-to-cacheinfo.c.patch
ApplyPatch 0040-x86-CPU-AMD-Calculate-last-level-cache-ID-from-numbe.patch
ApplyPatch 0041-x86-CPU-AMD-Fix-LLC-ID-bit-shift-calculation.patch
ApplyPatch 0042-sched-topology-Introduce-NUMA-identity-node-sched-do.patch
ApplyPatch 0043-x86-CPU-AMD-Derive-CPU-topology-from-CPUID-function-.patch
ApplyPatch 0044-vmxnet3-increase-default-rx-ring-sizes.patch
ApplyPatch 0045-block-xen-blkfront-consider-new-dom0-features-on-res.patch
ApplyPatch 0046-ACPICA-Enable-sleep-button-on-ACPI-legacy-wake.patch
ApplyPatch 0047-xen-restore-pirqs-on-resume-from-hibernation.patch
ApplyPatch 0048-xen-Only-restore-the-ACPI-SCI-interrupt-in-xen_resto.patch
ApplyPatch 0049-net-ena-Import-the-ENA-v2-driver-2.0.2g.patch
ApplyPatch 0050-arm64-export-memblock_reserve-d-regions-via-proc-iom.patch
ApplyPatch 0051-arm64-Fix-proc-iomem-for-reserved-but-not-memory-reg.patch
ApplyPatch 0052-efi-arm64-Check-whether-x18-is-preserved-by-runtime-.patch
ApplyPatch 0053-arm64-kexec-always-reset-to-EL2-if-present.patch
ApplyPatch 0054-arm64-acpi-fix-alignment-fault-in-accessing-ACPI.patch
ApplyPatch 0055-ACPICA-ACPI-6.2-Additional-PPTT-flags.patch
ApplyPatch 0056-drivers-base-cacheinfo-move-cache_setup_of_node.patch
ApplyPatch 0057-drivers-base-cacheinfo-setup-DT-cache-properties-ear.patch
ApplyPatch 0058-cacheinfo-rename-of_node-to-fw_token.patch
ApplyPatch 0059-arm64-acpi-Create-arch-specific-cpu-to-acpi-id-helpe.patch
ApplyPatch 0060-ACPI-PPTT-Add-Processor-Properties-Topology-Table-pa.patch
ApplyPatch 0061-ACPI-Enable-PPTT-support-on-ARM64.patch
ApplyPatch 0062-drivers-base-cacheinfo-Add-support-for-ACPI-based-fi.patch
ApplyPatch 0063-arm64-Add-support-for-ACPI-based-firmware-tables.patch
ApplyPatch 0064-arm64-topology-rename-cluster_id.patch
ApplyPatch 0065-arm64-topology-enable-ACPI-PPTT-based-CPU-topology.patch
ApplyPatch 0066-ACPI-Add-PPTT-to-injectable-table-list.patch
ApplyPatch 0067-arm64-topology-divorce-MC-scheduling-domain-from-cor.patch
ApplyPatch 0068-ACPI-PPTT-use-ACPI-ID-whenever-ACPI_PPTT_ACPI_PROCES.patch
ApplyPatch 0069-ACPI-PPTT-fix-build-when-CONFIG_ACPI_PPTT-is-not-ena.patch
ApplyPatch 0070-ACPI-PPTT-Handle-architecturally-unknown-cache-types.patch
ApplyPatch 0071-xen-netfront-call-netif_device_attach-on-resume.patch
ApplyPatch 0072-xfs-refactor-superblock-verifiers.patch
ApplyPatch 0073-libxfs-add-more-bounds-checking-to-sb-sanity-checks.patch
ApplyPatch 0074-xfs-only-validate-summary-counts-on-primary-superblo.patch
ApplyPatch 0075-xfs-iomap-define-and-use-the-IOMAP_F_DIRTY-flag-in-x.patch
ApplyPatch 0076-iomap-add-a-swapfile-activation-function.patch
ApplyPatch 0077-iomap-provide-more-useful-errors-for-invalid-swap-fi.patch
ApplyPatch 0078-iomap-don-t-allow-holes-in-swapfiles.patch
ApplyPatch 0079-iomap-inline-data-should-be-an-iomap-type-not-a-flag.patch
ApplyPatch 0080-iomap-fsync-swap-files-before-iterating-mappings.patch
ApplyPatch 0081-Import-lustre-client-2.10.5.patch
ApplyPatch 0082-Config-glue-for-lustre-client.patch
ApplyPatch 0083-net-allow-per-netns-sysctl_rmem-and-sysctl_wmem-for-.patch
ApplyPatch 0084-tcp-Namespace-ify-sysctl_tcp_rmem-and-sysctl_tcp_wme.patch
ApplyPatch 0085-Add-new-config-CONFIG_MICROVM-to-enable-microvm-opti.patch
ApplyPatch 0086-x86-stacktrace-Do-not-unwind-after-user-regs.patch
ApplyPatch 0087-x86-stacktrace-Remove-STACKTRACE_DUMP_ONCE.patch
ApplyPatch 0088-x86-stacktrace-Clarify-the-reliable-success-paths.patch
ApplyPatch 0089-x86-stacktrace-Do-not-fail-for-ORC-with-regs-on-stac.patch
ApplyPatch 0090-x86-unwind-orc-Detect-the-end-of-the-stack.patch
ApplyPatch 0091-x86-stacktrace-Enable-HAVE_RELIABLE_STACKTRACE-for-t.patch
ApplyPatch 0092-lustre-fix-ACL-handling.patch
ApplyPatch 0093-irqchip-gic-v2m-invoke-from-gic-v3-initialization-an.patch
ApplyPatch 0094-PCI-al-Add-Amazon-Annapurna-Labs-PCIe-host-controlle.patch
ApplyPatch 0095-arm64-acpi-pci-invoke-_DSM-whether-to-preserve-firmw.patch
ApplyPatch 0096-NFS-Remove-redundant-semicolon.patch
ApplyPatch 0097-Fix-microvm-config-dependency-in-Kconfig.patch
ApplyPatch 0098-microvm-enable-debug-in-case-of-tcp-out-of-memory.patch
ApplyPatch 0099-linux-ena-update-ENA-linux-driver-to-version-2.1.1.patch
ApplyPatch 0100-PCI-Add-Amazon-s-Annapurna-Labs-vendor-ID.patch
ApplyPatch 0101-PCI-Add-ACS-quirk-for-Amazon-Annapurna-Labs-root-por.patch
ApplyPatch 0102-Partially-revert-cc946adcb9e983ad9fe56ebe35f1292e111.patch
ApplyPatch 0103-livepatch-introduce-shadow-variable-API.patch
ApplyPatch 0104-livepatch-__klp_shadow_get_or_alloc-is-local-to-shad.patch
ApplyPatch 0105-livepatch-add-un-patch-callbacks.patch
ApplyPatch 0106-livepatch-move-transition-complete-notice-into-klp_c.patch
ApplyPatch 0107-livepatch-add-transition-notices.patch
ApplyPatch 0108-livepatch-Correctly-call-klp_post_unpatch_callback-i.patch
ApplyPatch 0109-livepatch-__klp_disable_patch-should-never-be-called.patch
ApplyPatch 0110-livepatch-send-a-fake-signal-to-all-blocking-tasks.patch
ApplyPatch 0111-livepatch-force-transition-to-finish.patch
ApplyPatch 0112-livepatch-Remove-immediate-feature.patch
ApplyPatch 0113-livepatch-add-locking-to-force-and-signal-functions.patch
ApplyPatch 0114-livepatch-Initialize-shadow-variables-safely-by-a-cu.patch
ApplyPatch 0115-livepatch-Allow-to-call-a-custom-callback-when-freei.patch
ApplyPatch 0116-livepatch-Remove-reliable-stacktrace-check-in-klp_tr.patch
ApplyPatch 0117-livepatch-Replace-synchronize_sched-with-synchronize.patch
ApplyPatch 0118-livepatch-Change-unsigned-long-old_addr-void-old_fun.patch
ApplyPatch 0119-xen-Restore-xen-pirqs-on-resume-from-hibernation.patch
ApplyPatch 0120-block-add-io-timeout-to-sysfs.patch
ApplyPatch 0121-block-don-t-show-io_timeout-if-driver-has-no-timeout.patch
ApplyPatch 0122-Add-Amazon-EFA-driver-version-1.4.patch
ApplyPatch 0123-percpu-refcount-Introduce-percpu_ref_resurrect.patch
ApplyPatch 0124-block-Allow-unfreezing-of-a-queue-while-requests-are.patch
ApplyPatch 0125-nvme-change-namespaces_mutext-to-namespaces_rwsem.patch
ApplyPatch 0126-blk-mq-fix-hang-caused-by-freeze-unfreeze-sequence.patch
ApplyPatch 0127-nvme-move-the-dying-queue-check-from-cancel-to-compl.patch
ApplyPatch 0128-nvme-pci-Better-support-for-disabling-controller.patch
ApplyPatch 0129-nvme-host-core-Allow-overriding-of-wait_ready-timeou.patch
ApplyPatch 0130-nvme-host-pci-Fix-a-race-in-controller-removal.patch
ApplyPatch 0131-nvme-pci-move-cq_vector-1-check-outside-of-q_lock.patch
ApplyPatch 0132-irqchip-gic-v3-its-Pass-its_node-pointer-to-each-com.patch
ApplyPatch 0133-irqchip-gic-v3-its-Only-emit-SYNC-if-targetting-a-va.patch
ApplyPatch 0134-irqchip-gic-v3-its-Only-emit-VSYNC-if-targetting-a-v.patch
ApplyPatch 0135-irqchip-gic-v3-its-Refactor-LPI-allocator.patch
ApplyPatch 0136-irqchip-gic-v3-its-Use-full-range-of-LPIs.patch
ApplyPatch 0137-irqchip-gic-v3-its-Move-minimum-LPI-requirements-to-.patch
ApplyPatch 0138-irqchip-gic-v3-its-Drop-chunk-allocation-compatibili.patch
ApplyPatch 0139-irqchip-gic-v3-Expose-GICD_TYPER-in-the-rdist-struct.patch
ApplyPatch 0140-irqchip-gic-v3-its-Honor-hypervisor-enforced-LPI-ran.patch
ApplyPatch 0141-irqchip-gic-v3-its-Reduce-minimum-LPI-allocation-to-.patch
ApplyPatch 0142-irqchip-gic-v3-its-Cap-lpi_id_bits-to-reduce-memory-.patch
ApplyPatch 0143-irqchip-gic-v3-its-Gracefully-fail-on-LPI-exhaustion.patch
ApplyPatch 0144-irqchip-gic-v3-its-Fix-comparison-logic-in-lpi_range.patch
ApplyPatch 0145-iommu-io-pgtable-arm-Convert-to-IOMMU-API-TLB-sync.patch
ApplyPatch 0146-iommu-io-pgtable-arm-v7s-Convert-to-IOMMU-API-TLB-sy.patch
ApplyPatch 0147-iommu-arm-smmu-v3-Implement-flush_iotlb_all-hook.patch
ApplyPatch 0148-iommu-dma-Add-support-for-non-strict-mode.patch
ApplyPatch 0149-iommu-Add-iommu.strict-command-line-option.patch
ApplyPatch 0150-iommu-io-pgtable-arm-Add-support-for-non-strict-mode.patch
ApplyPatch 0151-iommu-arm-smmu-v3-Add-support-for-non-strict-mode.patch
ApplyPatch 0152-iommu-io-pgtable-arm-v7s-Add-support-for-non-strict-.patch
ApplyPatch 0153-iommu-arm-smmu-Support-non-strict-mode.patch
ApplyPatch 0154-iommu-use-config-option-to-specify-if-iommu-mode-sho.patch
ApplyPatch 0155-locking-atomic-Add-atomic_cond_read_acquire.patch
ApplyPatch 0156-locking-barriers-Introduce-smp_cond_load_relaxed-and.patch
ApplyPatch 0157-locking-qspinlock-Use-atomic_cond_read_acquire.patch
ApplyPatch 0158-locking-mcs-Use-smp_cond_load_acquire-in-MCS-spin-lo.patch
ApplyPatch 0159-locking-qspinlock-Use-smp_cond_load_relaxed-to-wait-.patch
ApplyPatch 0160-locking-qspinlock-Use-smp_store_release-in-queued_sp.patch
ApplyPatch 0161-locking-qspinlock-Elide-back-to-back-RELEASE-operati.patch
ApplyPatch 0162-locking-qspinlock-Use-try_cmpxchg-instead-of-cmpxchg.patch
ApplyPatch 0163-MAINTAINERS-Add-myself-as-a-co-maintainer-for-the-lo.patch
ApplyPatch 0164-arm64-barrier-Implement-smp_cond_load_relaxed.patch
ApplyPatch 0165-arm64-locking-Replace-ticket-lock-implementation-wit.patch
ApplyPatch 0166-arm64-kconfig-Ensure-spinlock-fastpaths-are-inlined-.patch
ApplyPatch 0167-arm64-pull-in-upstream-erratum-workarounds.patch
ApplyPatch 0168-arm64-Avoid-flush_icache_range-in-alternatives-patch.patch
ApplyPatch 0169-update-ena-driver-to-version-2.1.3.patch
ApplyPatch 0170-Revert-nvme-pci-Better-support-for-disabling-control.patch
ApplyPatch 0171-nvme-pci-introduce-RECONNECTING-state-to-mark-initia.patch
ApplyPatch 0172-nvme-allow-controller-RESETTING-to-RECONNECTING-tran.patch
ApplyPatch 0173-nvme-rename-NVME_CTRL_RECONNECTING-state-to-NVME_CTR.patch
ApplyPatch 0174-nvme-pci-Fix-timeouts-in-connecting-state.patch
ApplyPatch 0175-nvme-pci-shutdown-on-timeout-during-deletion.patch
ApplyPatch 0176-nvme-pci-Unblock-reset_work-on-IO-failure.patch
ApplyPatch 0177-nvme-pci-Don-t-disable-on-timeout-in-reset-state.patch
ApplyPatch 0178-nvme-pci-use-atomic-bitops-to-mark-a-queue-enabled.patch
ApplyPatch 0179-arm64-fix-merge-error-in-errata-changes.patch
ApplyPatch 0180-lustre-hold-lock-while-walking-changelog-dev-list.patch
ApplyPatch 0181-Revert-Fix-the-locking-in-dcache_readdir-and-friends.patch
ApplyPatch 0182-drivers-amazon-efa-update-to-1.5.0.patch
ApplyPatch 0183-SMB3-Backup-intent-flag-missing-from-compounded-ops.patch
ApplyPatch 0184-Add-support-for-setting-owner-info-dos-attributes-an.patch
ApplyPatch 0185-update-ENA-linux-driver-to-version-2.2.1.patch
ApplyPatch 0186-Revert-update-ENA-linux-driver-to-version-2.2.1.patch
ApplyPatch 0187-kunit-test-add-KUnit-test-runner-core.patch
ApplyPatch 0188-kunit-test-add-test-resource-management-API.patch
ApplyPatch 0189-kunit-test-add-string_stream-a-std-stream-like-strin.patch
ApplyPatch 0190-kunit-test-add-assertion-printing-library.patch
ApplyPatch 0191-kunit-test-add-the-concept-of-expectations.patch
ApplyPatch 0192-lib-enable-building-KUnit-in-lib.patch
ApplyPatch 0193-kunit-test-add-initial-tests.patch
ApplyPatch 0194-kunit-test-add-support-for-test-abort.patch
ApplyPatch 0195-kunit-test-add-tests-for-kunit-test-abort.patch
ApplyPatch 0196-kunit-test-add-the-concept-of-assertions.patch
ApplyPatch 0197-kunit-test-add-tests-for-KUnit-managed-resources.patch
ApplyPatch 0198-kunit-fix-failure-to-build-without-printk.patch
ApplyPatch 0199-kunit-tool-add-Python-wrappers-for-running-KUnit-tes.patch
ApplyPatch 0200-kunit-defconfig-add-defconfigs-for-building-KUnit-te.patch
ApplyPatch 0201-kunit-Fix-build_dir-option.patch
ApplyPatch 0202-Documentation-kunit-add-documentation-for-KUnit.patch
ApplyPatch 0203-Documentation-kunit-Fix-verification-command.patch
ApplyPatch 0204-lib-list-test-add-a-test-for-the-list-doubly-linked-.patch
ApplyPatch 0205-cifs-Fix-slab-out-of-bounds-in-send_set_info-on-SMB2.patch
ApplyPatch 0206-CIFS-don-t-log-STATUS_NOT_FOUND-errors-for-DFS.patch
ApplyPatch 0207-Don-t-log-expected-error-on-DFS-referral-request.patch
ApplyPatch 0208-Don-t-log-confusing-message-on-reconnect-by-default.patch
ApplyPatch 0209-genirq-export-irq_get_percpu_devid_partition-to-modu.patch
ApplyPatch 0210-perf-core-Export-AUX-buffer-helpers-to-modules.patch
ApplyPatch 0211-perf-core-Add-PERF_AUX_FLAG_COLLISION-to-report-coll.patch
ApplyPatch 0212-arm64-sysreg-Move-SPE-registers-and-PSB-into-common-.patch
ApplyPatch 0213-arm64-head-Init-PMSCR_EL2.-PA-PCT-when-entered-at-EL.patch
ApplyPatch 0214-dt-bindings-Document-devicetree-binding-for-ARM-SPE.patch
ApplyPatch 0215-drivers-perf-Add-support-for-ARMv8.2-Statistical-Pro.patch
ApplyPatch 0216-perf-tools-Add-ARM-Statistical-Profiling-Extensions-.patch
ApplyPatch 0217-perf-arm-spe-Fix-uninitialized-record-error-variable.patch
ApplyPatch 0218-ACPICA-ACPI-6.3-MADT-add-support-for-statistical-pro.patch
ApplyPatch 0219-ACPICA-ACPI-6.3-PPTT-add-additional-fields-in-Proces.patch
ApplyPatch 0220-ACPI-PPTT-Modify-node-flag-detection-to-find-last-ID.patch
ApplyPatch 0221-ACPI-PPTT-Add-function-to-return-ACPI-6.3-Identical-.patch
ApplyPatch 0222-arm_pmu-acpi-spe-Add-initial-MADT-SPE-probing.patch
ApplyPatch 0223-perf-arm_spe-Enable-ACPI-Platform-automatic-module-l.patch
ApplyPatch 0224-ena-update-to-2.2.3.patch
ApplyPatch 0225-random-try-to-actively-add-entropy-rather-than-passi.patch
ApplyPatch 0226-random-introduce-RANDOM_WAIT_JITTER-config-option.patch
ApplyPatch 0227-lustre-update-to-AmazonFSxLustreClient-v2.10.8-1.patch
ApplyPatch 0228-Revert-ena-update-to-2.2.3.patch
ApplyPatch 0229-kernel-sched-fair.c-Fix-divide-by-zero.patch
ApplyPatch 0230-efi-honour-memory-reservations-passed-via-a-linux-sp.patch
ApplyPatch 0231-efi-arm-libstub-add-a-root-memreserve-config-table.patch
ApplyPatch 0232-efi-add-API-to-reserve-memory-persistently-across-ke.patch
ApplyPatch 0233-efi-Permit-calling-efi_mem_reserve_persistent-from-a.patch
ApplyPatch 0234-efi-Prevent-GICv3-WARN-by-mapping-the-memreserve-tab.patch
ApplyPatch 0235-efi-Permit-multiple-entries-in-persistent-memreserve.patch
ApplyPatch 0236-efi-Reduce-the-amount-of-memblock-reservations-for-p.patch
ApplyPatch 0237-efi-memreserve-deal-with-memreserve-entries-in-unmap.patch
ApplyPatch 0238-efi-memreserve-Register-reservations-as-reserved-in-.patch
ApplyPatch 0239-irqchip-gic-v3-Ensure-GICR_CTLR.EnableLPI-0-is-obser.patch
ApplyPatch 0240-irqchip-gic-v3-its-Change-initialization-ordering-fo.patch
ApplyPatch 0241-irqchip-gic-v3-its-Simplify-LPI_PENDBASE_SZ-usage.patch
ApplyPatch 0242-irqchip-gic-v3-its-Split-property-table-clearing-fro.patch
ApplyPatch 0243-irqchip-gic-v3-its-Move-pending-table-allocation-to-.patch
ApplyPatch 0244-irqchip-gic-v3-its-Keep-track-of-property-table-s-PA.patch
ApplyPatch 0245-irqchip-gic-v3-its-Allow-use-of-pre-programmed-LPI-t.patch
ApplyPatch 0246-irqchip-gic-v3-its-Use-pre-programmed-redistributor-.patch
ApplyPatch 0247-irqchip-gic-v3-its-Check-that-all-RDs-have-the-same-.patch
ApplyPatch 0248-irqchip-gic-v3-its-Register-LPI-tables-with-EFI-conf.patch
ApplyPatch 0249-irqchip-gic-v3-its-Allow-use-of-LPI-tables-in-reserv.patch
ApplyPatch 0250-iommu-arm-smmu-v3-Prevent-any-devices-access-to-memo.patch
ApplyPatch 0251-iommu-arm-smmu-v3-Abort-all-transactions-if-SMMU-is-.patch
ApplyPatch 0252-iommu-arm-smmu-v3-Don-t-disable-SMMU-in-kdump-kernel.patch
ApplyPatch 0253-netlabel-cope-with-NULL-catmap.patch

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl

touch .scmversion

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

mkdir configs

# Remove configs not for the buildarch
for cfg in kernel-%{version}-*.config; do
  if [ `echo %{all_arch_configs} | grep -c $cfg` -eq 0 ]; then
    rm -f $cfg
  fi
done

%if !%{debugbuildsenabled}
rm -f kernel-%{version}-*debug.config
%endif

# now run oldconfig over all the config files
for i in *.config
do
  mv $i .config
  Arch=`head -1 .config | cut -b 3-`
%if %{with_oldconfig}
  make ARCH=$Arch %{oldconfig_target}
%endif
  echo "# $Arch" > configs/$i
  cat .config >> configs/$i
done
# end of kernel config
%endif

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null

cd ..

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

%if %{with_debuginfo}
# This override tweaks the kernel makefiles so that we run debugedit on an
# object before embedding it.  When we later run find-debuginfo.sh, it will
# run debugedit again.  The edits it does change the build ID bits embedded
# in the stripped object, but repeating debugedit is a no-op.  We do it
# beforehand to get the proper final build ID bits into the embedded image.
# This affects the vDSO images in vmlinux, and the vmlinux image in bzImage.
export AFTER_LINK=\
'sh -xc "/usr/lib/rpm/debugedit -b $$RPM_BUILD_DIR -d /usr/src/debug \
    				-i $@ > $@.id"'
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

export CC=%{?_gcc}%{?!_gcc:gcc}
export HOSTCC=%{?_gcc}%{?!_gcc:gcc}
export HOSTCXX=%{?_gxx}%{?!_gxx:g++}

%global make_defines CC=gcc HOSTCC=gcc HOSTCXX=g++

export KBUILD_BUILD_HOST=$(hostname --short)

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$3
    Flav=${Flavour:+.${Flavour}}
    InstallName=${4:-vmlinuz}

    # Pick the right config file for the kernel we're building
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flav}

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flav}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}${Flav}/" Makefile

    # and now to start the build process

    make -s mrproper
    cp configs/$Config .config

%if %{signmodules}
    cp %{SOURCE11} .
%endif

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    make -s ARCH=$Arch %{oldconfig_target} %{?make_defines} > /dev/null
    make -s ARCH=$Arch V=1 %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?make_defines}
    make -s ARCH=$Arch V=1 %{?_smp_mflags} modules %{?sparse_mflags} %{?make_defines} || exit 1

    # Start installing the results
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer

%if %{with_dracut}
    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20
%else
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initrd-$KernelVer.img bs=1M count=5
%endif

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
    fi
    %if %{signmodules}
        %if %{usingefi}
        # Sign the image if we're using EFI
        %pesign -s -i $KernelImage -o vmlinuz.signed
        if [ ! -s vmlinuz.signed ]; then
            echo "pesigning failed"
            exit 1
        fi
        mv vmlinuz.signed $KernelImage
        %endif
    %endif
    $CopyKernel $KernelImage \
    		$RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer

%if %{with_fips}
    #hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," >  $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac
%endif
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    # Override $(mod-fw) because we don't want it to install any firmware
    # we'll get it from the linux-firmware package and we don't want conflicts
    make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=

%ifarch %{vdso_arches}
    make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
    if grep '^CONFIG_XEN=y$' .config >/dev/null ; then
        echo > ldconfig-kernel.conf "\
# This directive teaches ldconfig to search in nosegneg subdirectories
# and cache the DSOs there with extra bit 0 set in their hwcap match
# fields.  In Xen guest kernels, the vDSO tells the dynamic linker to
# search in nosegneg subdirectories and to match this extra hwcap bit
# in the ld.so.cache file.
hwcap 1 nosegneg"
    fi
    if [ ! -s ldconfig-kernel.conf ]; then
      echo > ldconfig-kernel.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-kernel.conf \
        $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
%endif

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    gzip -c9 Module.symvers >  $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -f tools/objtool/objtool ]; then
      cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include

    # newer kernels relocate these from under include/linux to
    # include/generated.... Maintain compatibility with old(er) code looking
    # for former files in the formerly valid location
    pushd  $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux
    test -s utsrelease.h        || ln -sf ../generated/utsrelease.h .
    test -s autoconf.h          || ln -sf ../generated/autoconf.h .
    popd
    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux/autoconf.h
    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp -a $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
%if %{fancy_debuginfo}
    if test -s vmlinux.id; then
      cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id
    else
      echo >&2 "*** ERROR *** no vmlinux build ID! ***"
      exit 1
    fi
%endif # fancy_debuginfo
    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif #debuginfo

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
      LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
    }

    collect_modules_list networking \
                        'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
                        'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size'
    collect_modules_list drm \
                        'drm_open|drm_init'
    collect_modules_list modesetting \
                        'drm_crtc_init'

    # detect missing or incorrect license tags
    rm -f modinfo
    while read i
    do
      echo -n "${i#$RPM_BUILD_ROOT/lib/modules/$KernelVer/} " >> modinfo
      %{_sbindir}/modinfo -l $i >> modinfo
    done < modnames

    grep -E -v \
    	  'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' \
	  modinfo && exit 1

    rm -f modinfo modnames

    # Call the modules-extra script to move things around
    %{SOURCE17} $RPM_BUILD_ROOT/lib/modules/$KernelVer %{SOURCE16}

%if %{signmodules}
    # Save off the .tmp_versions/ directory.  We'll use it in the
    # __debug_install_post macro below to sign the right things
    # Also save the signing keys so we actually sign the modules with the
    # right key.
    cp -r .tmp_versions .tmp_versions.sign${Flavour:+.${Flavour}}
    cp certs/signing_key.pem signing_key.pem.sign${Flavour:+.${Flavour}}
    cp certs/signing_key.x509 signing_key.x509.sign${Flavour:+.${Flavour}}
%endif

    # remove files that will be auto generated by depmod at rpm -i time
    for i in alias alias.bin builtin.bin ccwmap dep dep.bin ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols symbols.bin usbmap devname softdep
    do
      rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$i
    done

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -exec rm -f {} \;
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}

%if %{with_debug}
BuildKernel %make_target %kernel_image debug
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image
%endif

# perf
%global perf_make \
  make %{?_smp_mflags} -C tools/perf -s V=1 EXTRA_CFLAGS="-Wno-error=array-bounds" HAVE_CPLUS_DEMANGLE=1 NO_LIBUNWIND=1 NO_GTK2=1 NO_LIBNUMA=1 NO_STRLCPY=1 prefix=%{_prefix} lib=%{_lib} PYTHON=%{__python}
%if %{with_perf}
%{perf_make} all
%{perf_make} man || %{doc_build_fail}
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif # ix86
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif # x86_64
%ifarch %{ix86} x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   make
   popd
   pushd tools/power/x86/turbostat
   make
   popd
%endif #turbostat/x86_energy_perf_policy
%endif # cpupowerarchs
%endif # tools

%if %{with_doc}
#
# Make the HTML documents.
# Newer kernel versions use ReST markups for documentation which
# needs to be built using Sphinx. Sphinx toolchain is fragile and any
# upgrade to its toolchain or dependent python package can cause
# documentation build to fail. To avoid this problem, documentation
# build uses one particular version of Sphinx. To build document,
# we create a virtual environment and install the required version
# of Sphinx inside it.
# Refer to $SRC/Documentation/sphinx/requirements.txt for more
# information related to package and version dependency.
#
virtualenv doc_build_env
source ./doc_build_env/bin/activate
pip install -r Documentation/sphinx/requirements.txt
make htmldocs || %{doc_build_fail}
deactivate
rm -rf doc_build_env

# Build man pages for the kernel API (section 9)
scripts/kernel-doc -man $(find . -name '*.[ch]') | %{split_man_cmd} Documentation/output/man
pushd Documentation/output/man
gzip *.9
popd

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w

# switch absolute symlinks to relative ones
find . -lname "$(pwd)*" -exec sh -c 'ln -snvf $(python -c "from os.path import *; print relpath(\"$(readlink {})\",dirname(\"{}\"))") {}' \;
%endif # with_doc

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke mod-sign.sh command to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.
%define __modsign_install_post \
  if [ "%{signmodules}" == "1" ]; then \
    if [ "%{with_debug}" != "0" ]; \
    then \
      Arch=`head -1 configs/kernel-%{rpmversion}-%{_target_cpu}-debug.config | cut -b 3-` \
      rm -rf .tmp_versions \
      mv .tmp_versions.sign.debug .tmp_versions \
      mv signing_key.pem.sign.debug signing_key.pem \
      mv signing_key.x509.sign.debug signing_key.x509 \
      make -s ARCH=$Arch V=1 INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_sign KERNELRELEASE=%{KVERREL}.debug \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}.debug/extra/ \
    else \
      Arch=`head -1 configs/kernel-%{rpmversion}-%{_target_cpu}.config | cut -b 3-` \
      rm -rf .tmp_versions \
      mv signing_key.pem.sign signing_key.pem \
      mv signing_key.x509.sign signing_key.x509 \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/ \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/extra/ \
    fi \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}
%if %{fancy_debuginfo}
%define __debug_install_post \
  /usr/lib/rpm/find-debuginfo.sh %{debuginfo_args} %{_builddir}/%{?buildsubdir}\
%{nil}
%endif # fancy_debuginfo

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%defattr(-,root,root)
%endif # noarch

%endif # debuginfo

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{rpmversion}
man9dir=$RPM_BUILD_ROOT%{_datadir}/man/man9

# copy the source over
mkdir -p $docdir
tar -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir

# Install man pages for the kernel API.
mkdir -p $man9dir
pushd Documentation/output/man
find -type f -name '*.9.gz' -print0 |
xargs -0 --no-run-if-empty %{__install} -m 444 -t $man9dir $m
popd
ls $man9dir | grep -q '' || > $man9dir/BROKEN
%endif # with_doc

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
make -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do headers_check but don't die if it fails.
make -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check \
     > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   # exit 1
fi

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
     	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

# glibc provides scsi headers for itself, for now
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
rm -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h
%endif

%if %{with_perf}
# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install
# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext
# perf man pages (note: implicit rpm magic compresses them later)
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man || %{doc_build_fail}
# clean up files we don't use
rm -f $RPM_BUILD_ROOT/etc/bash_completion.d/perf
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
make -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_initddir} %{buildroot}%{_sysconfdir}/sysconfig
#install -m644 %{SOURCE2000} %{buildroot}%{_initddir}/cpupower
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%endif # cpupowerarchs
# just in case so the files list won't croak
touch ../cpupower.lang
%endif # tools


###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

%if %{with_tools}
%post tools
%{_sbindir}/ldconfig

%postun tools
%{_sbindir}/ldconfig
%endif

#
# This macro defines a %%post script for a kernel*-devel package.
#	%%kernel_devel_post [<subpackage>]
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x %{_sbindir}/hardlink ]\
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:.%{1}} &&\
     %{_bindir}/find . -type f | while read f; do\
       %{_sbindir}/hardlink -c /usr/src/kernels/*.%{dist}.*/$f $f\
     done)\
fi\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#	%%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans %{?1}}\
%{expand:\
%if %{with_dracut}\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --mkinitrd --make-default --dracut --depmod --install %{KVERREL}%{?1:-%{1}} || exit $?\
%else\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --mkinitrd --make-default --depmod --install %{KVERREL}%{?1:-%{1}} || exit $?\
%endif\
}\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --rpmposttrans %{KVERREL}%{?1:.%{1}} || exit $?\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#	%%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_variant_posttrans %{?-v*}}\
%{expand:%%post %{?-v*}}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  %{_bindir}/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#	%%kernel_variant_preun <subpackage>
#
%define kernel_variant_preun() \
%{expand:%%preun %{?1}}\
%{_sbindir}/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}%{?1:.%{1}} || exit $?\
%{nil}

%kernel_variant_preun
%kernel_variant_post

%kernel_variant_preun debug
%kernel_variant_post -v debug

if [ -x %{_sbindir}/ldconfig ]
then
    %{_sbindir}/ldconfig -X || exit $?
fi

###
### file lists
###

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}
%{_datadir}/man/man9/*
%endif

%if %{with_perf}
%files -n perf
%defattr(-,root,root)
%{_bindir}/perf
%{_bindir}/trace
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_datadir}/perf-core/*
%{_datadir}/doc/perf*/*
%dir %{_libdir}/traceevent/plugins
%{_libdir}/traceevent/plugins/*
%{_mandir}/man[1-8]/perf*
%doc linux-%{KVERREL}/tools/perf/Documentation/examples.txt

%files -n python-perf
%defattr(-,root,root)
%{python_sitearch}/*

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo
%defattr(-,root,root)

%files -f python-perf-debuginfo.list -n python-perf-debuginfo
%defattr(-,root,root)
%endif # with_debuginfo
%endif # with_perf

%if %{with_tools}
%files tools -f cpupower.lang
%defattr(-,root,root)
%{_mandir}/man[1-8]/cpupower*
%{_bindir}/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%endif
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.1
#%{_initddir}/cpupower
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower

%if %{with_debuginfo}
%files tools-debuginfo -f kernel-tools-debuginfo.list
%defattr(-,root,root)
%endif

%ifarch %{cpupowerarchs}
%files tools-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif
%endif # with_tools

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{1}\
%{expand:%%files %{?2}}\
%defattr(-,root,root)\
/%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?2:.%{2}}\
%attr(600,root,root) /boot/System.map-%{KVERREL}%{?2:.%{2}}\
%if %{with_fips} \
/%{image_install_path}/.vmlinuz-%{KVERREL}%{?2:.%{2}}.hmac \
%endif \
/boot/symvers-%{KVERREL}%{?2:.%{2}}.gz\
/boot/config-%{KVERREL}%{?2:.%{2}}\
%dir /lib/modules/%{KVERREL}%{?2:.%{2}}\
/lib/modules/%{KVERREL}%{?2:.%{2}}/kernel\
/lib/modules/%{KVERREL}%{?2:.%{2}}/build\
/lib/modules/%{KVERREL}%{?2:.%{2}}/source\
/lib/modules/%{KVERREL}%{?2:.%{2}}/extra\
/lib/modules/%{KVERREL}%{?2:.%{2}}/updates\
/lib/modules/%{KVERREL}%{?2:.%{2}}/weak-updates\
%ifarch %{vdso_arches}\
/lib/modules/%{KVERREL}%{?2:.%{2}}/vdso\
/etc/ld.so.conf.d/kernel-%{KVERREL}%{?2:.%{2}}.conf\
%endif\
/lib/modules/%{KVERREL}%{?2:.%{2}}/modules.*\
%if %{with_dracut}\
%ghost /boot/initramfs-%{KVERREL}%{?2:.%{2}}.img\
%else\
%ghost /boot/initrd-%{KVERREL}%{?2:.%{2}}.img\
%endif\
%{expand:%%files %{?2:%{2}-}devel}\
%defattr(-,root,root)\
%verify(not mtime) /usr/src/kernels/%{KVERREL}%{?2:.%{2}}\
%dir /usr/src/kernels\
%if %{with_debuginfo}\
%ifnarch noarch\
%if %{fancy_debuginfo}\
%{expand:%%files -f debuginfo%{?2}.list %{?2:%{2}-}debuginfo}\
%else\
%{expand:%%files %{?2:%{2}-}debuginfo}\
%endif\
%defattr(-,root,root)\
%if !%{fancy_debuginfo}\
%if "%{elf_image_install_path}" != ""\
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}%{?2:.%{2}}.debug\
%endif\
%{debuginfodir}/lib/modules/%{KVERREL}%{?2:.%{2}}\
%{debuginfodir}/usr/src/kernels/%{KVERREL}%{?2:.%{2}}\
%endif\
%endif\
%endif\
%endif\
%{nil}

%kernel_variant_files %{with_up}
%kernel_variant_files %{with_debug} debug

#
# Finally kernel-livepatch as it has it's own version/release
# NOTE: Don't move this anywhere else, otherwise it'll need
# it's own Name: and that affects all the packages that
# follow. Aslo having a Version, Release affects other subpackages
# so safely tuck this to the end.
# Other Caveats: This spec file uses a special hack for __spec_install_post
# Hence, all operations in __spec_install_post should not refer to
# either %%{version} or %%{release}
#
%ifarch x86_64
%package -n kernel-livepatch-%{rpmversion}-%{buildid}
Summary: Livepatches for the Linux Kernel
Version: 1.0
Release: 0%{?dist}
Requires: kpatch
%systemd_requires

%description -n kernel-livepatch-%{rpmversion}-%{buildid}
This package contains the live patch modules for bug fixes
against the version of the kernel. This package contains
version 0 (no real livepatches) and helps subscribe to
the kernel livepatch updates for the kernel.

%files -n kernel-livepatch-%{rpmversion}-%{buildid}
%defattr(-,root,root)
%{nil}
%endif

%changelog
* Thu May 07 2020 Builder <builder@amazon.com>
- builder/9b95f592f851611ed31936dd266111b402453c9f last changes:

- linux/841be2b45c2b8a9c5919a71e907d5409cf5e32f6 last changes:
  + [841be2b45c2b] [2020-05-07] netlabel: cope with NULL catmap (pabeni@redhat.com)
  + [92ae4476f41e] [2019-04-23] iommu/arm-smmu-v3: Don't disable SMMU in kdump kernel (will.deacon@arm.com)
  + [a214f9b1ca10] [2018-07-25] iommu/arm-smmu-v3: Abort all transactions if SMMU is enabled in kdump kernel (will.deacon@arm.com)
  + [dd3ab00307a6] [2018-07-12] iommu/arm-smmu-v3: Prevent any devices access to memory without registration (thunder.leizhen@huawei.com)
  + [1d8ac397724e] [2018-07-27] irqchip/gic-v3-its: Allow use of LPI tables in reserved memory (marc.zyngier@arm.com)
  + [ffa1eb91bede] [2018-07-27] irqchip/gic-v3-its: Register LPI tables with EFI config table (marc.zyngier@arm.com)
  + [7942811499bc] [2018-07-27] irqchip/gic-v3-its: Check that all RDs have the same property table (marc.zyngier@arm.com)
  + [9aa19791e4bd] [2018-06-26] irqchip/gic-v3-its: Use pre-programmed redistributor tables with kdump kernels (marc.zyngier@arm.com)
  + [c7f269102ce2] [2018-07-27] irqchip/gic-v3-its: Allow use of pre-programmed LPI tables (marc.zyngier@arm.com)
  + [1e0318173561] [2018-07-27] irqchip/gic-v3-its: Keep track of property table's PA and VA (marc.zyngier@arm.com)
  + [1abb611af336] [2018-07-27] irqchip/gic-v3-its: Move pending table allocation to init time (marc.zyngier@arm.com)
  + [94bf822f0fe8] [2018-07-27] irqchip/gic-v3-its: Split property table clearing from allocation (marc.zyngier@arm.com)
  + [304cda90ab2a] [2018-07-17] irqchip/gic-v3-its: Simplify LPI_PENDBASE_SZ usage (marc.zyngier@arm.com)
  + [fb08fbb70257] [2018-07-27] irqchip/gic-v3-its: Change initialization ordering for LPIs (marc.zyngier@arm.com)
  + [57b16dd75f0c] [2018-03-21] irqchip/gic-v3: Ensure GICR_CTLR.EnableLPI=0 is observed before enabling (shankerd@codeaurora.org)
  + [f9862a4b498f] [2019-12-06] efi/memreserve: Register reservations as 'reserved' in /proc/iomem (ardb@kernel.org)
  + [7f11e1c900b2] [2019-06-09] efi/memreserve: deal with memreserve entries in unmapped memory (ard.biesheuvel@linaro.org)
  + [ff35eaa7a7dd] [2018-11-29] efi: Reduce the amount of memblock reservations for persistent allocations (ard.biesheuvel@linaro.org)
  + [6cc2d6d8d421] [2018-11-29] efi: Permit multiple entries in persistent memreserve data structure (ard.biesheuvel@linaro.org)
  + [e50c71d15047] [2018-11-23] efi: Prevent GICv3 WARN() by mapping the memreserve table before first use (ard.biesheuvel@linaro.org)
  + [dc7a2f1f21d5] [2018-11-14] efi: Permit calling efi_mem_reserve_persistent() from atomic context (ard.biesheuvel@linaro.org)
  + [a245aba5552a] [2018-09-21] efi: add API to reserve memory persistently across kexec reboot (ard.biesheuvel@linaro.org)
  + [97dad6a1dcae] [2018-09-21] efi/arm: libstub: add a root memreserve config table (ard.biesheuvel@linaro.org)
  + [2213f6c1dc6d] [2018-09-21] efi: honour memory reservations passed via a linux specific config table (ard.biesheuvel@linaro.org)
  + [785b71e52e2a] [2020-04-07] kernel/sched/fair.c: Fix divide by zero (sblbir@amazon.com)
  + [5662b50ea995] [2020-04-01] Revert "ena: update to 2.2.3" (yishache@amazon.com)
  + [8bc8421d98ed] [2020-03-08] lustre: update to AmazonFSxLustreClient v2.10.8-1 (astroh@amazon.com)
  + [604e8fe8a16e] [2020-01-29] random: introduce RANDOM_WAIT_JITTER config option (fllinden@amazon.com)
  + [02a3a10804e7] [2019-09-28] random: try to actively add entropy rather than passively wait for it (torvalds@linux-foundation.org)
  + [a92934463e91] [2020-02-26] ena: update to 2.2.3 (fllinden@amazon.com)
  + [5d19f81c96f6] [2019-06-26] perf: arm_spe: Enable ACPI/Platform automatic module loading (jeremy.linton@arm.com)
  + [960b7b0ea624] [2019-06-26] arm_pmu: acpi: spe: Add initial MADT/SPE probing (jeremy.linton@arm.com)
  + [7261666d531f] [2019-06-26] ACPI/PPTT: Add function to return ACPI 6.3 Identical tokens (jeremy.linton@arm.com)
  + [2b187e1db89a] [2019-06-26] ACPI/PPTT: Modify node flag detection to find last IDENTICAL (jeremy.linton@arm.com)
  + [7cc0ea1d39bd] [2020-01-29] ACPICA: ACPI 6.3: PPTT add additional fields in Processor Structure Flags (erik.schmauss@intel.com)
  + [8a73fb66c542] [2020-01-28] ACPICA: ACPI 6.3: MADT: add support for statistical profiling in GICC (erik.schmauss@intel.com)
  + [b418386855d2] [2018-08-10] perf arm spe: Fix uninitialized record error variable (kim.phillips@arm.com)
  + [137ef2a4a018] [2018-01-14] perf tools: Add ARM Statistical Profiling Extensions (SPE) support (kim.phillips@arm.com)
  + [dcf0f2aa6a15] [2016-09-22] drivers/perf: Add support for ARMv8.2 Statistical Profiling Extension (will.deacon@arm.com)
  + [b9c74ca4e640] [2016-09-22] dt-bindings: Document devicetree binding for ARM SPE (will.deacon@arm.com)
  + [d169e3fb1768] [2017-07-07] arm64: head: Init PMSCR_EL2.{PA,PCT} when entered at EL2 without VHE (will.deacon@arm.com)
  + [669866229488] [2017-09-20] arm64: sysreg: Move SPE registers and PSB into common header files (will.deacon@arm.com)
  + [da5f2efeae5a] [2016-09-23] perf/core: Add PERF_AUX_FLAG_COLLISION to report colliding samples (will.deacon@arm.com)
  + [59d70f4c0e4f] [2016-08-16] perf/core: Export AUX buffer helpers to modules (will.deacon@arm.com)
  + [bdca209fa0bf] [2016-07-25] genirq: export irq_get_percpu_devid_partition to modules (will.deacon@arm.com)
  + [1f6c68871c5f] [2018-03-29] Don't log confusing message on reconnect by default (stfrench@microsoft.com)
  + [056fb00e8a8c] [2018-03-21] Don't log expected error on DFS referral request (smfrench@gmail.com)
  + [8fd2f8ae4e45] [2017-11-21] CIFS: don't log STATUS_NOT_FOUND errors for DFS (aaptel@suse.com)
  + [5c02aeb058e0] [2018-07-05] cifs: Fix slab-out-of-bounds in send_set_info() on SMB2 ACE setting (sbrivio@redhat.com)
  + [121571d62a14] [2019-12-31] lib/list-test: add a test for the 'list' doubly linked list (davidgow@google.com)
  + [e37ed0c6ab00] [2019-09-08] Documentation: kunit: Fix verification command (sj38.park@gmail.com)
  + [31db2c818eab] [2019-09-23] Documentation: kunit: add documentation for KUnit (brendanhiggins@google.com)
  + [4ba0ddad900a] [2019-09-07] kunit: Fix '--build_dir' option (sj38.park@gmail.com)
  + [b7fe19d7717d] [2019-09-23] kunit: defconfig: add defconfigs for building KUnit tests (brendanhiggins@google.com)
  + [e1e2af108920] [2019-09-23] kunit: tool: add Python wrappers for running KUnit tests (felixguoxiuping@gmail.com)
  + [d1044cd5beed] [2019-09-23] kunit: fix failure to build without printk (brendanhiggins@google.com)
  + [778525bad411] [2019-09-23] kunit: test: add tests for KUnit managed resources (akndr41@gmail.com)
  + [b1cdf0d56763] [2019-09-23] kunit: test: add the concept of assertions (brendanhiggins@google.com)
  + [f59c1c9a998b] [2019-09-23] kunit: test: add tests for kunit test abort (brendanhiggins@google.com)
  + [d71a39d21341] [2019-09-23] kunit: test: add support for test abort (brendanhiggins@google.com)
  + [a51211f0c78d] [2019-09-23] kunit: test: add initial tests (brendanhiggins@google.com)
  + [e9fe631f22f0] [2019-12-31] lib: enable building KUnit in lib/ (brendanhiggins@google.com)
  + [3d2e0b085731] [2019-09-23] kunit: test: add the concept of expectations (brendanhiggins@google.com)
  + [150b9f2f6934] [2019-09-23] kunit: test: add assertion printing library (brendanhiggins@google.com)
  + [415cb0e3f7a9] [2019-09-23] kunit: test: add string_stream a std::stream like string builder (brendanhiggins@google.com)
  + [1c0bac85d8ec] [2019-09-23] kunit: test: add test resource management API (brendanhiggins@google.com)
  + [6f3195e362bf] [2019-09-23] kunit: test: add KUnit test runner core (brendanhiggins@google.com)
  + [efa534f09cde] [2020-02-03] Revert "update ENA linux driver to version 2.2.1" (anchalag@amazon.com)
  + [0a3e27c31886] [2020-01-20] update ENA linux driver to version 2.2.1 (anchalag@amazon.com)
  + [1fe79c98a591] [2019-12-18] Add support for setting owner info, dos attributes, and create time (bprotopopov@hotmail.com)
  + [66032ec5c49e] [2018-08-28] SMB3: Backup intent flag missing from compounded ops (stfrench@microsoft.com)
  + [c181c7397cf9] [2019-12-19] drivers/amazon: efa: update to 1.5.0 (luqia@amazon.com)
  + [78e7942aac30] [2019-12-16] Revert "Fix the locking in dcache_readdir() and friends". (fllinden@amazon.com)
  + [bdc322cd1b21] [2019-12-04] lustre: hold lock while walking changelog dev list (astroh@amazon.com)
  + [1fd7858ca029] [2019-11-15] arm64: fix merge error in errata changes (fllinden@amazon.com)
  + [6b87e1b2a090] [2019-11-12] nvme-pci: use atomic bitops to mark a queue enabled (hch@lst.de)
  + [20688aae3d99] [2019-11-11] nvme-pci: Don't disable on timeout in reset state (keith.busch@intel.com)
  + [253425de96d7] [2019-11-11] nvme-pci: Unblock reset_work on IO failure (keith.busch@intel.com)
  + [fc3c86787f85] [2019-11-11] nvme-pci: shutdown on timeout during deletion (keith.busch@intel.com)
  + [5c4908c6c793] [2018-02-08] nvme-pci: Fix timeouts in connecting state (keith.busch@intel.com)
  + [5f7aa8cd1a0e] [2019-11-11] nvme: rename NVME_CTRL_RECONNECTING state to NVME_CTRL_CONNECTING (maxg@mellanox.com)
  + [4767030c5f68] [2017-10-25] nvme: allow controller RESETTING to RECONNECTING transition (jsmart2021@gmail.com)
  + [9f9e54f607dd] [2019-11-11] nvme-pci: introduce RECONNECTING state to mark initializing procedure (jianchao.w.wang@oracle.com)
  + [9e6ac1954231] [2019-11-11] Revert "nvme/pci: Better support for disabling controller" (sblbir@amazon.com)
  + [3ce6c8f31af3] [2019-11-04] update ena driver to version 2.1.3 (alakeshh@amazon.com)
  + [859624c8d881] [2018-06-22] arm64: Avoid flush_icache_range() in alternatives patching code (will.deacon@arm.com)
  + [8df9832589ed] [2018-09-27] arm64: pull in upstream erratum workarounds (fllinden@amazon.com)
  + [6d40835e5d43] [2018-03-13] arm64: kconfig: Ensure spinlock fastpaths are inlined if !PREEMPT (will.deacon@arm.com)
  + [ac3ff3a3fd73] [2018-03-13] arm64: locking: Replace ticket lock implementation with qspinlock (will.deacon@arm.com)
  + [0adcafee60c0] [2018-01-31] arm64: barrier: Implement smp_cond_load_relaxed (will.deacon@arm.com)
  + [87c4690f03dc] [2018-04-26] MAINTAINERS: Add myself as a co-maintainer for the locking subsystem (will.deacon@arm.com)
  + [5c4db1761210] [2018-04-26] locking/qspinlock: Use try_cmpxchg() instead of cmpxchg() when locking (will.deacon@arm.com)
  + [363728e09cce] [2018-04-26] locking/qspinlock: Elide back-to-back RELEASE operations with smp_wmb() (will.deacon@arm.com)
  + [428eb7735dcf] [2018-04-26] locking/qspinlock: Use smp_store_release() in queued_spin_unlock() (will.deacon@arm.com)
  + [8b38f789042c] [2018-04-26] locking/qspinlock: Use smp_cond_load_relaxed() to wait for next node (will.deacon@arm.com)
  + [ede411cf8365] [2018-04-26] locking/mcs: Use smp_cond_load_acquire() in MCS spin loop (jason.low2@hp.com)
  + [89aa7e53da83] [2018-04-26] locking/qspinlock: Use atomic_cond_read_acquire() (will.deacon@arm.com)
  + [489a1496e5e1] [2018-04-26] locking/barriers: Introduce smp_cond_load_relaxed() and atomic_cond_read_relaxed() (will.deacon@arm.com)
  + [275f8886fc33] [2017-10-12] locking/atomic: Add atomic_cond_read_acquire() (will.deacon@arm.com)
  + [833fd048d0d0] [2019-08-29] iommu: use config option to specify if iommu mode should be strict (fllinden@amazon.com)
  + [b26e27a5eecb] [2018-09-20] iommu/arm-smmu: Support non-strict mode (robin.murphy@arm.com)
  + [d9e549306851] [2018-09-20] iommu/io-pgtable-arm-v7s: Add support for non-strict mode (robin.murphy@arm.com)
  + [011a0cec0a5d] [2018-09-20] iommu/arm-smmu-v3: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [be4f8f89384a] [2018-09-20] iommu/io-pgtable-arm: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [e922b8b4d97e] [2018-09-20] iommu: Add "iommu.strict" command line option (thunder.leizhen@huawei.com)
  + [59de986b8eaf] [2018-09-20] iommu/dma: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [479758e487f4] [2018-09-20] iommu/arm-smmu-v3: Implement flush_iotlb_all hook (thunder.leizhen@huawei.com)
  + [9e00c165bb13] [2017-09-28] iommu/io-pgtable-arm-v7s: Convert to IOMMU API TLB sync (robin.murphy@arm.com)
  + [412aa375d925] [2017-09-28] iommu/io-pgtable-arm: Convert to IOMMU API TLB sync (robin.murphy@arm.com)
  + [0d209ad1ca4b] [2019-03-12] irqchip/gic-v3-its: Fix comparison logic in lpi_range_cmp (linux@rasmusvillemoes.dk)
  + [f7694a2ae1c3] [2019-01-29] irqchip/gic-v3-its: Gracefully fail on LPI exhaustion (marc.zyngier@arm.com)
  + [d2a2312aebf7] [2018-08-28] irqchip/gic-v3-its: Cap lpi_id_bits to reduce memory footprint (jia.he@hxt-semitech.com)
  + [70294faf1bc7] [2018-05-31] irqchip/gic-v3-its: Reduce minimum LPI allocation to 1 for PCI devices (marc.zyngier@arm.com)
  + [628002e598cf] [2018-05-31] irqchip/gic-v3-its: Honor hypervisor enforced LPI range (marc.zyngier@arm.com)
  + [8a98b641ca82] [2018-05-30] irqchip/gic-v3: Expose GICD_TYPER in the rdist structure (marc.zyngier@arm.com)
  + [3b3b711422c4] [2018-05-27] irqchip/gic-v3-its: Drop chunk allocation compatibility (marc.zyngier@arm.com)
  + [6f0f2fddc75c] [2018-05-27] irqchip/gic-v3-its: Move minimum LPI requirements to individual busses (marc.zyngier@arm.com)
  + [3d616084699b] [2018-05-27] irqchip/gic-v3-its: Use full range of LPIs (marc.zyngier@arm.com)
  + [2da88431a09a] [2018-05-27] irqchip/gic-v3-its: Refactor LPI allocator (marc.zyngier@arm.com)
  + [64fc042809c8] [2018-06-22] irqchip/gic-v3-its: Only emit VSYNC if targetting a valid collection (marc.zyngier@arm.com)
  + [bde110bc9d4c] [2018-06-22] irqchip/gic-v3-its: Only emit SYNC if targetting a valid collection (marc.zyngier@arm.com)
  + [3a986147b60c] [2017-07-28] irqchip/gic-v3-its: Pass its_node pointer to each command builder (marc.zyngier@arm.com)
  + [113763531709] [2018-05-17] nvme-pci: move ->cq_vector == -1 check outside of ->q_lock (axboe@kernel.dk)
  + [06e833ec7116] [2019-09-13] nvme/host/pci: Fix a race in controller removal (sblbir@amzn.com)
  + [483092e50f35] [2019-09-13] nvme/host/core: Allow overriding of wait_ready timeout (sblbir@amzn.com)
  + [cb98c4a2ff6e] [2019-09-10] nvme/pci: Better support for disabling controller (sblbir@amzn.com)
  + [1d35419be441] [2017-11-02] nvme: move the dying queue check from cancel to completion (hch@lst.de)
  + [da6017a1790d] [2019-08-28] blk-mq: fix hang caused by freeze/unfreeze sequence (bob.liu@oracle.com)
  + [808fb5c0c2e7] [2019-08-16] nvme: change namespaces_mutext to namespaces_rwsem (jianchao.w.wang@oracle.com)
  + [f07f609b9997] [2018-09-26] block: Allow unfreezing of a queue while requests are in progress (bvanassche@acm.org)
  + [cde5ae3939f0] [2019-08-16] percpu-refcount: Introduce percpu_ref_resurrect() (bvanassche@acm.org)
  + [ef399dae8090] [2019-09-05] Add Amazon EFA driver version 1.4 (alakeshh@amazon.com)
  + [d2c263f51370] [2019-04-02] block: don't show io_timeout if driver has no timeout handler (zhangweiping@didiglobal.com)
  + [5604a94d453c] [2018-11-29] block: add io timeout to sysfs (zhangweiping@didiglobal.com)
  + [5dd6e06468f2] [2019-08-15] xen: Restore xen-pirqs on resume from hibernation (anchalag@amazon.com)
  + [a2cac6bcdf37] [2019-01-09] livepatch: Change unsigned long old_addr -> void *old_func in struct klp_func (pmladek@suse.com)
  + [a79ba8b9c1d4] [2018-11-07] livepatch: Replace synchronize_sched() with synchronize_rcu() (paulmck@linux.ibm.com)
  + [ed3f017290b8] [2018-07-12] livepatch: Remove reliable stacktrace check in klp_try_switch_task() (kamalesh@linux.vnet.ibm.com)
  + [9d64fef42380] [2018-04-16] livepatch: Allow to call a custom callback when freeing shadow variables (pmladek@suse.com)
  + [8d23cd0c31e1] [2018-04-16] livepatch: Initialize shadow variables safely by a custom callback (pmladek@suse.com)
  + [9b2c3a5baf40] [2017-12-21] livepatch: add locking to force and signal functions (mbenes@suse.cz)
  + [5db47b21bcf1] [2018-01-10] livepatch: Remove immediate feature (mbenes@suse.cz)
  + [93e6e2b176f0] [2017-11-22] livepatch: force transition to finish (mbenes@suse.cz)
  + [c54b66741799] [2017-11-15] livepatch: send a fake signal to all blocking tasks (mbenes@suse.cz)
  + [35c6287f3678] [2017-10-20] livepatch: __klp_disable_patch() should never be called for disabled patches (pmladek@suse.com)
  + [52ce21ed38c7] [2017-10-20] livepatch: Correctly call klp_post_unpatch_callback() in error paths (pmladek@suse.com)
  + [758813a3c417] [2017-10-13] livepatch: add transition notices (joe.lawrence@redhat.com)
  + [06a640be0adc] [2017-10-13] livepatch: move transition "complete" notice into klp_complete_transition() (joe.lawrence@redhat.com)
  + [4dfb1a89e138] [2017-10-13] livepatch: add (un)patch callbacks (joe.lawrence@redhat.com)
  + [161696f3a7d0] [2017-09-14] livepatch: __klp_shadow_get_or_alloc() is local to shadow.c (jkosina@suse.cz)
  + [2d354ae84bea] [2017-08-31] livepatch: introduce shadow variable API (joe.lawrence@redhat.com)
  + [260c46a6c712] [2019-08-15] Partially revert cc946adcb9e983ad9fe56ebe35f1292e111ff10e (sblbir@amzn.com)
  + [bfb6b9f05b8b] [2019-07-11] PCI: Add ACS quirk for Amazon Annapurna Labs root ports (alisaidi@amazon.com)
  + [7eb9b2292115] [2019-07-11] PCI: Add Amazon's Annapurna Labs vendor ID (jonnyc@amazon.com)
  + [17541d027aa8] [2019-06-24] linux/ena: update ENA linux driver to version 2.1.1 (fllinden@amazon.com)
  + [80b108a221e9] [2019-07-02] microvm: enable debug in case of tcp out of memory (alakeshh@amazon.com)
  + [1dfdc8d0c4e5] [2019-07-03] Fix microvm config dependency in Kconfig (alakeshh@amazon.com)
  + [d870097db8d1] [2019-02-12] NFS: Remove redundant semicolon (zhangliguang@linux.alibaba.com)
  + [7bf10387e285] [2019-05-31] arm64: acpi/pci: invoke _DSM whether to preserve firmware PCI setup (fllinden@amazon.com)
  + [db44b69d7127] [2019-03-28] PCI: al: Add Amazon Annapurna Labs PCIe host controller driver (jonnyc@amazon.com)
  + [52790f9de6ec] [2019-04-24] irqchip/gic-v2m: invoke from gic-v3 initialization and add acpi quirk flow (zeev@amazon.com)
  + [0983a5f66c47] [2019-04-03] lustre: fix ACL handling (fllinden@amazon.com)
  + [bac3facf7361] [2018-05-18] x86/stacktrace: Enable HAVE_RELIABLE_STACKTRACE for the ORC unwinder (jslaby@suse.cz)
  + [4297ce719d2c] [2018-05-18] x86/unwind/orc: Detect the end of the stack (jpoimboe@redhat.com)
  + [518601c37927] [2018-05-18] x86/stacktrace: Do not fail for ORC with regs on stack (jslaby@suse.cz)
  + [cf8bec6fc488] [2018-05-18] x86/stacktrace: Clarify the reliable success paths (jslaby@suse.cz)
  + [0446a9d82be3] [2018-05-18] x86/stacktrace: Remove STACKTRACE_DUMP_ONCE (jslaby@suse.cz)
  + [ac4b65696b58] [2018-05-18] x86/stacktrace: Do not unwind after user regs (jslaby@suse.cz)
  + [6d1e579c802b] [2019-03-12] Add new config CONFIG_MICROVM to enable microvm optimized kernel (alakeshh@amazon.com)
  + [6eb487407aaf] [2019-02-19] tcp: Namespace-ify sysctl_tcp_rmem and sysctl_tcp_wmem (edumazet@google.com)
  + [8d1668ff24cd] [2017-11-07] net: allow per netns sysctl_rmem and sysctl_wmem for protos (edumazet@google.com)
  + [9604568f3a51] [2019-03-01] Config glue for lustre client. (fllinden@amazon.com)
  + [e0882b91ead2] [2019-03-01] Import lustre client 2.10.5 (fllinden@amazon.com)
  + [1f1e5754e718] [2018-06-05] iomap: fsync swap files before iterating mappings (darrick.wong@oracle.com)
  + [0e6dce505e18] [2018-06-01] iomap: inline data should be an iomap type, not a flag (hch@lst.de)
  + [c308a044c8c2] [2018-05-16] iomap: don't allow holes in swapfiles (osandov@fb.com)
  + [7c827701279d] [2018-05-16] iomap: provide more useful errors for invalid swap files (osandov@fb.com)
  + [77d0e622d357] [2018-05-10] iomap: add a swapfile activation function (darrick.wong@oracle.com)
  + [1b82f2085bfd] [2019-01-30] xfs, iomap: define and use the IOMAP_F_DIRTY flag in xfs (fllinden@amazon.com)
  + [7543a89c0642] [2018-08-01] xfs: only validate summary counts on primary superblock (darrick.wong@oracle.com)
  + [24ed6218d60a] [2018-07-26] libxfs: add more bounds checking to sb sanity checks (billodo@redhat.com)
  + [69bf8490c790] [2018-07-29] xfs: refactor superblock verifiers (darrick.wong@oracle.com)
  + [18f7a3c60057] [2019-01-31] xen-netfront: call netif_device_attach on resume (fllinden@amazon.com)
  + [506c323b425b] [2018-10-04] ACPI/PPTT: Handle architecturally unknown cache types (jhugo@codeaurora.org)
  + [193ba41bdef9] [2018-06-05] ACPI / PPTT: fix build when CONFIG_ACPI_PPTT is not enabled (sudeep.holla@arm.com)
  + [b1407f98b285] [2018-06-29] ACPI / PPTT: use ACPI ID whenever ACPI_PPTT_ACPI_PROCESSOR_ID_VALID is set (Sudeep.Holla@arm.com)
  + [ed6ca67d9ecc] [2018-05-11] arm64: topology: divorce MC scheduling domain from core_siblings (jeremy.linton@arm.com)
  + [4faf9eb94edc] [2018-05-11] ACPI: Add PPTT to injectable table list (jeremy.linton@arm.com)
  + [452571e324ad] [2018-05-11] arm64: topology: enable ACPI/PPTT based CPU topology (jeremy.linton@arm.com)
  + [8a960842b131] [2018-05-11] arm64: topology: rename cluster_id (jeremy.linton@arm.com)
  + [08ab180a050d] [2018-05-11] arm64: Add support for ACPI based firmware tables (jeremy.linton@arm.com)
  + [530d697647d1] [2018-05-11] drivers: base cacheinfo: Add support for ACPI based firmware tables (jeremy.linton@arm.com)
  + [d44a0a92dbc7] [2018-05-11] ACPI: Enable PPTT support on ARM64 (jeremy.linton@arm.com)
  + [cfa01af0fd4d] [2018-05-11] ACPI/PPTT: Add Processor Properties Topology Table parsing (jeremy.linton@arm.com)
  + [0a0be3a71669] [2018-05-11] arm64/acpi: Create arch specific cpu to acpi id helper (jeremy.linton@arm.com)
  + [1542bcffe270] [2018-05-11] cacheinfo: rename of_node to fw_token (jeremy.linton@arm.com)
  + [e0db56c37051] [2018-05-11] drivers: base: cacheinfo: setup DT cache properties early (jeremy.linton@arm.com)
  + [23f1c4fbc034] [2018-05-11] drivers: base: cacheinfo: move cache_setup_of_node() (jeremy.linton@arm.com)
  + [3ad45d5f4164] [2017-11-17] ACPICA: ACPI 6.2: Additional PPTT flags (jeremy.linton@arm.com)
  + [077c513d6c7f] [2018-07-23] arm64: acpi: fix alignment fault in accessing ACPI (takahiro.akashi@linaro.org)
  + [c2130d9ad476] [2018-07-02] arm64: kexec: always reset to EL2 if present (mark.rutland@arm.com)
  + [b5852384c7fc] [2018-03-08] efi/arm64: Check whether x18 is preserved by runtime services calls (ard.biesheuvel@linaro.org)
  + [006a5276352e] [2018-10-11] arm64: Fix /proc/iomem for reserved but not memory regions (will.deacon@arm.com)
  + [863436e58da2] [2018-07-23] arm64: export memblock_reserve()d regions via /proc/iomem (james.morse@arm.com)
  + [5b7a6e0b5bc3] [2018-11-10] net: ena: Import the ENA v2 driver (2.0.2g) (alakeshh@amazon.com)
  + [ba2abcf477c4] [2018-11-10] xen: Only restore the ACPI SCI interrupt in xen_restore_pirqs. (fllinden@amazon.com)
  + [55f8ff943e05] [2018-10-26] xen: restore pirqs on resume from hibernation. (fllinden@amazon.com)
  + [ffa0a5c26a63] [2018-10-29] ACPICA: Enable sleep button on ACPI legacy wake (anchalag@amazon.com)
  + [896cac3913ba] [2018-10-18] block: xen-blkfront: consider new dom0 features on restore (eduval@amazon.com)
  + [e15e6ddbda2d] [2017-11-30] vmxnet3: increase default rx ring sizes (skhare@vmware.com)
  + [0eb74d03b514] [2018-04-27] x86/CPU/AMD: Derive CPU topology from CPUID function 0xB when available (suravee.suthikulpanit@amd.com)
  + [4defcf0dbd65] [2017-09-07] sched/topology: Introduce NUMA identity node sched domain (suravee.suthikulpanit@amd.com)
  + [dd880bfc925e] [2018-06-13] x86/CPU/AMD: Fix LLC ID bit-shift calculation (suravee.suthikulpanit@amd.com)
  + [f0ebe08da236] [2018-04-27] x86/CPU/AMD: Calculate last level cache ID from number of sharing threads (suravee.suthikulpanit@amd.com)
  + [524f0df862f1] [2018-04-27] x86/CPU: Rename intel_cacheinfo.c to cacheinfo.c (bp@suse.de)
  + [9fd0bf224e07] [2018-05-17] x86/MCE/AMD: Read MCx_MISC block addresses on any CPU (bp@suse.de)
  + [3c23caa415fe] [2018-08-15] blk-wbt: Avoid lock contention and thundering herd issue in wbt_wait (anchalag@amazon.com)
  + [817cf371ba97] [2018-01-12] blk-mq: simplify queue mapping & schedule with each possisble CPU (hch@lst.de)
  + [7f31988908c9] [2018-04-09] x86: tsc: avoid system instability in hibernation (eduval@amazon.com)
  + [d1c77a4e9d88] [2018-06-05] xen-blkfront: Fixed blkfront_restore to remove a call to negotiate_mq (anchalag@amazon.com)
  + [cb05ed2acc21] [2018-03-24] KVM: X86: Fix setup the virt_spin_lock_key before static key get initialized (wanpengli@tencent.com)
  + [d67fbc433887] [2017-10-28] x86/paravirt: Set up the virt_spin_lock_key after static keys get initialized (douly.fnst@cn.fujitsu.com)
  + [362b119471cf] [2018-02-13] KVM: X86: Choose qspinlock when dedicated physical CPUs are available (wanpengli@tencent.com)
  + [2c7e56592b19] [2018-02-13] KVM: Introduce paravirtualization hints and KVM_HINTS_DEDICATED (wanpengli@tencent.com)
  + [90bdcdc042be] [2017-09-06] locking/paravirt: Use new static key for controlling call of virt_spin_lock() (jgross@suse.com)
  + [1a5402dce785] [2018-03-27] Revert "xen: dont fiddle with event channel masking in suspend/resume" (anchalag@amazon.com)
  + [f46564957af7] [2018-01-18] ACPI: SPCR: Make SPCR available to x86 (prarit@redhat.com)
  + [a21f4ce4f7ef] [2016-04-26] xen-blkfront: add 'persistent_grants' parameter (aliguori@amazon.com)
  + [c85f422c905c] [2017-03-10] xen-blkfront: resurrect request-based mode (kamatam@amazon.com)
  + [89383cdaf362] [2017-11-02] Not-for-upstream: PM / hibernate: Speed up hibernation by batching requests (cyberax@amazon.com)
  + [0df67493d3ac] [2017-10-27] PM / hibernate: update the resume offset on SNAPSHOT_SET_SWAP_AREA (cyberax@amazon.com)
  + [32c2931359a9] [2017-08-24] x86/xen: close event channels for PIRQs in system core suspend callback (kamatam@amazon.com)
  + [006854797724] [2017-08-24] xen/events: add xen_shutdown_pirqs helper function (kamatam@amazon.com)
  + [26153f57818b] [2017-07-21] x86/xen: save and restore steal clock (kamatam@amazon.com)
  + [04b0bfd880b5] [2017-07-13] xen/time: introduce xen_{save,restore}_steal_clock (kamatam@amazon.com)
  + [ed1e6563aaca] [2017-01-09] xen-netfront: add callbacks for PM suspend and hibernation support (kamatam@amazon.com)
  + [2de1a12eb9b3] [2017-06-08] xen-blkfront: add callbacks for PM suspend and hibernation (kamatam@amazon.com)
  + [7745f7441b78] [2017-02-11] x86/xen: add system core suspend and resume callbacks (kamatam@amazon.com)
  + [4e04f0e6ee3f] [2018-02-22] x86/xen: Introduce new function to map HYPERVISOR_shared_info on Resume (anchalag@amazon.com)
  + [89296fc1e946] [2017-07-13] xenbus: add freeze/thaw/restore callbacks support (kamatam@amazon.com)
  + [50655596284b] [2017-07-13] xen/manage: introduce helper function to know the on-going suspend mode (kamatam@amazon.com)
  + [9db89b7cce5e] [2017-07-12] xen/manage: keep track of the on-going suspend mode (kamatam@amazon.com)
  + [355891fb54d1] [2018-02-27] Importing Amazon ENA driver 1.5.0 into amazon-4.14.y/master. (vallish@amazon.com)
  + [339619747b44] [2018-02-12] drivers/amazon: introduce AMAZON_ENA_ETHERNET (vallish@amazon.com)
  + [fe6eafa6db96] [2018-02-12] drivers/amazon: add network device drivers support (vallish@amazon.com)
  + [90a685c71442] [2018-02-12] drivers: introduce AMAZON_DRIVER_UPDATES (vallish@amazon.com)
  + [57561504c91d] [2017-10-27] not-for-upstream: testmgr config changes to enable FIPS boot (alakeshh@amazon.com)
  + [d1f57020e880] [2017-09-19] nvme: update timeout module parameter type (vallish@amazon.com)
  + [66d24cb6b6c9] [2015-12-08] force perf to use /usr/bin/python instead of /usr/bin/python2 (kamatam@amazon.com)
  + [da8c32bda036] [2013-02-13] bump default tcp_wmem from 16KB to 20KB (gafton@amazon.com)
  + [6214f5a71929] [2016-01-26] bump the default TTL to 255 (kamatam@amazon.com)
  + [e78c71b7ba1f] [2012-02-10] scsi: sd_revalidate_disk prevent NULL ptr deref (kernel-team@fedoraproject.org)
  + [3340a96c886f] [2008-10-06] kbuild: AFTER_LINK (roland@redhat.com)


