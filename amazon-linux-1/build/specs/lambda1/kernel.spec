%define buildid 105.231

# We have to override the new %%install behavior because, well... the kernel is special.
%global __spec_install_pre %%{___build_pre}

Summary: The Linux kernel

# Sign modules on x86.  Make sure the config files match this setting if more
# architectures are added.
%ifarch %{ix86} x86_64
%global signmodules 1
%else
%global signmodules 0
%endif

# Amazon: no signing yet
%if %{?amzn}
%global signmodules 0
%endif

# Save original buildid for later if it's defined
%if 0%{?buildid:1}
%global orig_buildid %{buildid}
%undefine buildid
%endif

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
%global kversion 4.14.171
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
%define with_up        0
# kernel-debug
%define with_debug     0
# kernel-doc
%define with_doc       0
# kernel-headers
%define with_headers   1
# perf
%define with_perf      0
# tools
%define with_tools     0
# kernel-debuginfo
%define with_debuginfo 0
# Want to build a the vsdo directories installed
%define with_vdso_install 0
# Use dracut instead of mkinitrd for initrd image generation
%define with_dracut       0

# Build the kernel-doc package, but don't fail the build if it botches.
# Here "true" means "continue" and "false" means "fail the build".
%define doc_build_fail true

# should we do C=1 builds with sparse
%define with_sparse	0

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

%define KVERREL %{version}-%{release}.%{_target_cpu}
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir %{_prefix}/lib/debug

%define all_x86 i386 i686

%if %{with_vdso_install}
# These arches install vdso/ directories.
%define vdso_arches %{all_x86} x86_64 %{arm}
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

%ifarch %{arm}
%define all_arch_configs kernel-%{version}-arm*.config
%define asmarch arm
%define hdrarch arm
%define image_install_path boot
%define kernel_image arch/%{asmarch}/boot/zImage
%endif

# amazon: don't use nonint config target - we want to know when our config files are
# not complete
%define oldconfig_target oldconfig

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# Architectures we build tools/cpupower on
%define cpupowerarchs %{ix86} x86_64
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
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0, nvidia-dkms < 2:352.99-2017.03.104.amzn1, amdgpu-pro-dkms < 16.60-378247.2.amzn1

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
ExclusiveArch: noarch %{all_x86} x86_64 %{arm}
ExclusiveOS: Linux

%kernel_reqprovconf
%ifarch x86_64
Requires(pre): microcode_ctl >= 2:2.1-47.36
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
BuildRequires: gcc >= 7.2.1
# Required for kernel documentation build
BuildRequires: python-virtualenv, python-sphinx, ImageMagick-perl
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
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel perl(ExtUtils::Embed) bison
BuildRequires: audit-libs-devel
BuildRequires: numactl-devel
%if 0%{?sys_python_pkg:1}
BuildRequires: %{sys_python_pkg}-devel
%else
BuildRequires: python-devel
%endif

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
BuildRequires: openssl
BuildRequires: pesign >= 0.10-4
%endif

Source0: linux-4.14.171.tar
Source1: linux-4.14.171-patches.tar

# this is for %{signmodules}
Source11: x509.genkey

Source15: kconfig.py
Source16: mod-extra.list
Source17: mod-extra.sh
Source18: mod-extra-sign.sh
%define modsign_cmd %{SOURCE18}

Source19: Makefile.config
Source20: config-generic
Source30: config-x86_32-generic
Source40: config-x86_64-generic
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
Patch0224: 0224-netfilter-nf_conntrack-resolve-clash-for-matching-co.patch
Patch0225: 0225-ext4-fix-potential-race-between-online-resizing-and-.patch
Patch0226: 0226-ext4-fix-potential-race-between-s_group_info-online-.patch
Patch0227: 0227-ext4-fix-potential-race-between-s_flex_groups-online.patch
Patch0228: 0228-ena-update-to-2.2.3.patch
Patch0229: 0229-random-try-to-actively-add-entropy-rather-than-passi.patch
Patch0230: 0230-random-introduce-RANDOM_WAIT_JITTER-config-option.patch

BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

Prefix: %{_prefix}

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46
Prefix: %{_prefix}
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.


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

# Dynamically generate kernel .config files from config-* files
make -f %{SOURCE19} VERSION=%{version} config

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
ApplyPatch 0224-netfilter-nf_conntrack-resolve-clash-for-matching-co.patch
ApplyPatch 0225-ext4-fix-potential-race-between-online-resizing-and-.patch
ApplyPatch 0226-ext4-fix-potential-race-between-s_group_info-online-.patch
ApplyPatch 0227-ext4-fix-potential-race-between-s_flex_groups-online.patch
ApplyPatch 0228-ena-update-to-2.2.3.patch
ApplyPatch 0229-random-try-to-actively-add-entropy-rather-than-passi.patch
ApplyPatch 0230-random-introduce-RANDOM_WAIT_JITTER-config-option.patch

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

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

###
### install
###

%install

cd linux-%{KVERREL}

%if %{with_headers}
# Install kernel headers
make -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT%{_prefix} headers_install

# Do headers_check but don't die if it fails.
make -s ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT%{_prefix} headers_check \
     > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT%{_includedir}/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   # exit 1
fi

find $RPM_BUILD_ROOT%{_includedir} \
     \( -name .install -o -name .check -o \
     	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

# glibc provides scsi headers for itself, for now
rm -rf $RPM_BUILD_ROOT%{_includedir}/scsi
rm -f $RPM_BUILD_ROOT%{_includedir}/asm*/atomic.h
rm -f $RPM_BUILD_ROOT%{_includedir}/asm*/io.h
rm -f $RPM_BUILD_ROOT%{_includedir}/asm*/irq.h
%endif


###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### file lists
###

%files headers
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Thu Apr 2 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Feb 27 2020 Builder <builder@amazon.com>
- builder/a0848101af192173ab8b8423548517fdf5347c42 last changes:
  + [a084810] [2020-02-27] Add disabled CONFIG_RANDOM_WAIT_JITTER option (only used on AL2/arm64). (fllinden@amazon.com)

- linux/bfb8522db261d5eed0acd0a9c7c176d3b345e1e6 last changes:
  + [bfb8522db261] [2020-01-29] random: introduce RANDOM_WAIT_JITTER config option (fllinden@amazon.com)
  + [95128f158d05] [2019-09-28] random: try to actively add entropy rather than passively wait for it (torvalds@linux-foundation.org)
  + [6355321e13ec] [2020-02-26] ena: update to 2.2.3 (fllinden@amazon.com)
  + [0602114d5e2e] [2020-02-18] ext4: fix potential race between s_flex_groups online resizing and access (surajjs@amazon.com)
  + [c090690f9ee5] [2020-02-18] ext4: fix potential race between s_group_info online resizing and access (surajjs@amazon.com)
  + [d5e73ddc0fa4] [2020-02-15] ext4: fix potential race between online resizing and write operations (tytso@mit.edu)
  + [ffbd980a9af1] [2018-07-02] netfilter: nf_conntrack: resolve clash for matching conntracks (martynas@weave.works)
  + [bece8afa03dd] [2019-06-26] perf: arm_spe: Enable ACPI/Platform automatic module loading (jeremy.linton@arm.com)
  + [a5c9500a75ce] [2019-06-26] arm_pmu: acpi: spe: Add initial MADT/SPE probing (jeremy.linton@arm.com)
  + [0a8e723e5d68] [2019-06-26] ACPI/PPTT: Add function to return ACPI 6.3 Identical tokens (jeremy.linton@arm.com)
  + [99e0bbad0d68] [2019-06-26] ACPI/PPTT: Modify node flag detection to find last IDENTICAL (jeremy.linton@arm.com)
  + [5b1e9775465a] [2020-01-29] ACPICA: ACPI 6.3: PPTT add additional fields in Processor Structure Flags (erik.schmauss@intel.com)
  + [1498d79117b6] [2020-01-28] ACPICA: ACPI 6.3: MADT: add support for statistical profiling in GICC (erik.schmauss@intel.com)
  + [50b90ee9545e] [2018-08-10] perf arm spe: Fix uninitialized record error variable (kim.phillips@arm.com)
  + [4c252c23c96a] [2018-01-14] perf tools: Add ARM Statistical Profiling Extensions (SPE) support (kim.phillips@arm.com)
  + [23f25b35819f] [2016-09-22] drivers/perf: Add support for ARMv8.2 Statistical Profiling Extension (will.deacon@arm.com)
  + [c4cf49866b44] [2016-09-22] dt-bindings: Document devicetree binding for ARM SPE (will.deacon@arm.com)
  + [7a3cdba7bb1f] [2017-07-07] arm64: head: Init PMSCR_EL2.{PA,PCT} when entered at EL2 without VHE (will.deacon@arm.com)
  + [28fc388b01d2] [2017-09-20] arm64: sysreg: Move SPE registers and PSB into common header files (will.deacon@arm.com)
  + [07cd91df5689] [2016-09-23] perf/core: Add PERF_AUX_FLAG_COLLISION to report colliding samples (will.deacon@arm.com)
  + [26fd68b7be40] [2016-08-16] perf/core: Export AUX buffer helpers to modules (will.deacon@arm.com)
  + [44eb5f6fe409] [2016-07-25] genirq: export irq_get_percpu_devid_partition to modules (will.deacon@arm.com)
  + [ba384643d240] [2018-03-29] Don't log confusing message on reconnect by default (stfrench@microsoft.com)
  + [1150faf1217a] [2018-03-21] Don't log expected error on DFS referral request (smfrench@gmail.com)
  + [bd6963ac2017] [2017-11-21] CIFS: don't log STATUS_NOT_FOUND errors for DFS (aaptel@suse.com)
  + [ed33bd26f3f4] [2018-07-05] cifs: Fix slab-out-of-bounds in send_set_info() on SMB2 ACE setting (sbrivio@redhat.com)
  + [b7a18d2a2afb] [2019-12-31] lib/list-test: add a test for the 'list' doubly linked list (davidgow@google.com)
  + [5caeeb4151cc] [2019-09-08] Documentation: kunit: Fix verification command (sj38.park@gmail.com)
  + [ef3c678233e3] [2019-09-23] Documentation: kunit: add documentation for KUnit (brendanhiggins@google.com)
  + [df579fdadee7] [2019-09-07] kunit: Fix '--build_dir' option (sj38.park@gmail.com)
  + [eaba3efa0ff4] [2019-09-23] kunit: defconfig: add defconfigs for building KUnit tests (brendanhiggins@google.com)
  + [607e2875f382] [2019-09-23] kunit: tool: add Python wrappers for running KUnit tests (felixguoxiuping@gmail.com)
  + [63748912d8f2] [2019-09-23] kunit: fix failure to build without printk (brendanhiggins@google.com)
  + [9b58d908698c] [2019-09-23] kunit: test: add tests for KUnit managed resources (akndr41@gmail.com)
  + [f96cac380f1e] [2019-09-23] kunit: test: add the concept of assertions (brendanhiggins@google.com)
  + [b1f23de0f26c] [2019-09-23] kunit: test: add tests for kunit test abort (brendanhiggins@google.com)
  + [30116d5e1c5a] [2019-09-23] kunit: test: add support for test abort (brendanhiggins@google.com)
  + [b68637569c04] [2019-09-23] kunit: test: add initial tests (brendanhiggins@google.com)
  + [6528948f892d] [2019-12-31] lib: enable building KUnit in lib/ (brendanhiggins@google.com)
  + [4925bfe76484] [2019-09-23] kunit: test: add the concept of expectations (brendanhiggins@google.com)
  + [ad7c795fc8d2] [2019-09-23] kunit: test: add assertion printing library (brendanhiggins@google.com)
  + [319ede268121] [2019-09-23] kunit: test: add string_stream a std::stream like string builder (brendanhiggins@google.com)
  + [b8abf543c63e] [2019-09-23] kunit: test: add test resource management API (brendanhiggins@google.com)
  + [713e423c0d67] [2019-09-23] kunit: test: add KUnit test runner core (brendanhiggins@google.com)
  + [7013451aebcd] [2020-02-03] Revert "update ENA linux driver to version 2.2.1" (anchalag@amazon.com)
  + [fa907b05a3df] [2020-01-20] update ENA linux driver to version 2.2.1 (anchalag@amazon.com)
  + [203b1606fbef] [2019-12-18] Add support for setting owner info, dos attributes, and create time (bprotopopov@hotmail.com)
  + [c5ed28c06c13] [2018-08-28] SMB3: Backup intent flag missing from compounded ops (stfrench@microsoft.com)
  + [286818197727] [2019-12-19] drivers/amazon: efa: update to 1.5.0 (luqia@amazon.com)
  + [85821f3b05b0] [2019-12-16] Revert "Fix the locking in dcache_readdir() and friends". (fllinden@amazon.com)
  + [a145d073ef7d] [2019-12-04] lustre: hold lock while walking changelog dev list (astroh@amazon.com)
  + [a6c8fccc7e30] [2019-11-15] arm64: fix merge error in errata changes (fllinden@amazon.com)
  + [ffb13949549c] [2019-11-12] nvme-pci: use atomic bitops to mark a queue enabled (hch@lst.de)
  + [bc2629f5a128] [2019-11-11] nvme-pci: Don't disable on timeout in reset state (keith.busch@intel.com)
  + [b24d19a26406] [2019-11-11] nvme-pci: Unblock reset_work on IO failure (keith.busch@intel.com)
  + [2a9d52931000] [2019-11-11] nvme-pci: shutdown on timeout during deletion (keith.busch@intel.com)
  + [88ca5a08f761] [2018-02-08] nvme-pci: Fix timeouts in connecting state (keith.busch@intel.com)
  + [e5f06c18a73d] [2019-11-11] nvme: rename NVME_CTRL_RECONNECTING state to NVME_CTRL_CONNECTING (maxg@mellanox.com)
  + [fbc8b6fbf748] [2017-10-25] nvme: allow controller RESETTING to RECONNECTING transition (jsmart2021@gmail.com)
  + [2846e1660adc] [2019-11-11] nvme-pci: introduce RECONNECTING state to mark initializing procedure (jianchao.w.wang@oracle.com)
  + [45f554cb1127] [2019-11-11] Revert "nvme/pci: Better support for disabling controller" (sblbir@amazon.com)
  + [e02da6a526b6] [2019-11-04] update ena driver to version 2.1.3 (alakeshh@amazon.com)
  + [e3410f45977b] [2018-06-22] arm64: Avoid flush_icache_range() in alternatives patching code (will.deacon@arm.com)
  + [422dea88dfeb] [2018-09-27] arm64: pull in upstream erratum workarounds (fllinden@amazon.com)
  + [f47524688d1d] [2018-03-13] arm64: kconfig: Ensure spinlock fastpaths are inlined if !PREEMPT (will.deacon@arm.com)
  + [0113517f8523] [2018-03-13] arm64: locking: Replace ticket lock implementation with qspinlock (will.deacon@arm.com)
  + [cbc36dd512af] [2018-01-31] arm64: barrier: Implement smp_cond_load_relaxed (will.deacon@arm.com)
  + [ff6aed0a098b] [2018-04-26] MAINTAINERS: Add myself as a co-maintainer for the locking subsystem (will.deacon@arm.com)
  + [ab6466a02e7f] [2018-04-26] locking/qspinlock: Use try_cmpxchg() instead of cmpxchg() when locking (will.deacon@arm.com)
  + [d0217856acae] [2018-04-26] locking/qspinlock: Elide back-to-back RELEASE operations with smp_wmb() (will.deacon@arm.com)
  + [afff942765b9] [2018-04-26] locking/qspinlock: Use smp_store_release() in queued_spin_unlock() (will.deacon@arm.com)
  + [756371b40f73] [2018-04-26] locking/qspinlock: Use smp_cond_load_relaxed() to wait for next node (will.deacon@arm.com)
  + [18e486596c4e] [2018-04-26] locking/mcs: Use smp_cond_load_acquire() in MCS spin loop (jason.low2@hp.com)
  + [7bce094f3796] [2018-04-26] locking/qspinlock: Use atomic_cond_read_acquire() (will.deacon@arm.com)
  + [fa98dfd47ab2] [2018-04-26] locking/barriers: Introduce smp_cond_load_relaxed() and atomic_cond_read_relaxed() (will.deacon@arm.com)
  + [326f32a65412] [2017-10-12] locking/atomic: Add atomic_cond_read_acquire() (will.deacon@arm.com)
  + [7db1d2a321f9] [2019-08-29] iommu: use config option to specify if iommu mode should be strict (fllinden@amazon.com)
  + [94d5314d9378] [2018-09-20] iommu/arm-smmu: Support non-strict mode (robin.murphy@arm.com)
  + [e2c3aa66d9eb] [2018-09-20] iommu/io-pgtable-arm-v7s: Add support for non-strict mode (robin.murphy@arm.com)
  + [3cd47ff9c072] [2018-09-20] iommu/arm-smmu-v3: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [1f478545f2f3] [2018-09-20] iommu/io-pgtable-arm: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [f6caa948f1c0] [2018-09-20] iommu: Add "iommu.strict" command line option (thunder.leizhen@huawei.com)
  + [5de979b191fd] [2018-09-20] iommu/dma: Add support for non-strict mode (thunder.leizhen@huawei.com)
  + [a872d8c30828] [2018-09-20] iommu/arm-smmu-v3: Implement flush_iotlb_all hook (thunder.leizhen@huawei.com)
  + [072fed303f3d] [2017-09-28] iommu/io-pgtable-arm-v7s: Convert to IOMMU API TLB sync (robin.murphy@arm.com)
  + [772db136570b] [2017-09-28] iommu/io-pgtable-arm: Convert to IOMMU API TLB sync (robin.murphy@arm.com)
  + [06c069330121] [2019-03-12] irqchip/gic-v3-its: Fix comparison logic in lpi_range_cmp (linux@rasmusvillemoes.dk)
  + [18079f630004] [2019-01-29] irqchip/gic-v3-its: Gracefully fail on LPI exhaustion (marc.zyngier@arm.com)
  + [0bcfcbac978a] [2018-08-28] irqchip/gic-v3-its: Cap lpi_id_bits to reduce memory footprint (jia.he@hxt-semitech.com)
  + [a193bc5500b3] [2018-05-31] irqchip/gic-v3-its: Reduce minimum LPI allocation to 1 for PCI devices (marc.zyngier@arm.com)
  + [5dfbca067262] [2018-05-31] irqchip/gic-v3-its: Honor hypervisor enforced LPI range (marc.zyngier@arm.com)
  + [e04b6d50d787] [2018-05-30] irqchip/gic-v3: Expose GICD_TYPER in the rdist structure (marc.zyngier@arm.com)
  + [e5a152daa950] [2018-05-27] irqchip/gic-v3-its: Drop chunk allocation compatibility (marc.zyngier@arm.com)
  + [46d7b3416b7e] [2018-05-27] irqchip/gic-v3-its: Move minimum LPI requirements to individual busses (marc.zyngier@arm.com)
  + [821604a17b49] [2018-05-27] irqchip/gic-v3-its: Use full range of LPIs (marc.zyngier@arm.com)
  + [1cba3787747b] [2018-05-27] irqchip/gic-v3-its: Refactor LPI allocator (marc.zyngier@arm.com)
  + [bf1f450fe216] [2018-06-22] irqchip/gic-v3-its: Only emit VSYNC if targetting a valid collection (marc.zyngier@arm.com)
  + [baa711752df1] [2018-06-22] irqchip/gic-v3-its: Only emit SYNC if targetting a valid collection (marc.zyngier@arm.com)
  + [8635dcbd594d] [2017-07-28] irqchip/gic-v3-its: Pass its_node pointer to each command builder (marc.zyngier@arm.com)
  + [f8721b96a580] [2018-05-17] nvme-pci: move ->cq_vector == -1 check outside of ->q_lock (axboe@kernel.dk)
  + [1159e108ca42] [2019-09-13] nvme/host/pci: Fix a race in controller removal (sblbir@amzn.com)
  + [a15a85021405] [2019-09-13] nvme/host/core: Allow overriding of wait_ready timeout (sblbir@amzn.com)
  + [0348fee21371] [2019-09-10] nvme/pci: Better support for disabling controller (sblbir@amzn.com)
  + [bec829762e4f] [2017-11-02] nvme: move the dying queue check from cancel to completion (hch@lst.de)
  + [0057c006755c] [2019-08-28] blk-mq: fix hang caused by freeze/unfreeze sequence (bob.liu@oracle.com)
  + [190870b39842] [2019-08-16] nvme: change namespaces_mutext to namespaces_rwsem (jianchao.w.wang@oracle.com)
  + [3c95767e005e] [2018-09-26] block: Allow unfreezing of a queue while requests are in progress (bvanassche@acm.org)
  + [e8c89c3c2fa1] [2019-08-16] percpu-refcount: Introduce percpu_ref_resurrect() (bvanassche@acm.org)
  + [40beb7b1c2f9] [2019-09-05] Add Amazon EFA driver version 1.4 (alakeshh@amazon.com)
  + [9cdf56e8e7ff] [2019-04-02] block: don't show io_timeout if driver has no timeout handler (zhangweiping@didiglobal.com)
  + [e470f6bc3e78] [2018-11-29] block: add io timeout to sysfs (zhangweiping@didiglobal.com)
  + [de16e168d3f1] [2019-08-15] xen: Restore xen-pirqs on resume from hibernation (anchalag@amazon.com)
  + [55bb4fb85f26] [2019-01-09] livepatch: Change unsigned long old_addr -> void *old_func in struct klp_func (pmladek@suse.com)
  + [08fda1268671] [2018-11-07] livepatch: Replace synchronize_sched() with synchronize_rcu() (paulmck@linux.ibm.com)
  + [fb5cebaf7835] [2018-07-12] livepatch: Remove reliable stacktrace check in klp_try_switch_task() (kamalesh@linux.vnet.ibm.com)
  + [e094f6174968] [2018-04-16] livepatch: Allow to call a custom callback when freeing shadow variables (pmladek@suse.com)
  + [2383bfd3d65d] [2018-04-16] livepatch: Initialize shadow variables safely by a custom callback (pmladek@suse.com)
  + [9689a300d903] [2017-12-21] livepatch: add locking to force and signal functions (mbenes@suse.cz)
  + [de5058728b2f] [2018-01-10] livepatch: Remove immediate feature (mbenes@suse.cz)
  + [dcb6965521de] [2017-11-22] livepatch: force transition to finish (mbenes@suse.cz)
  + [4cccf79e3be2] [2017-11-15] livepatch: send a fake signal to all blocking tasks (mbenes@suse.cz)
  + [8d81df75a264] [2017-10-20] livepatch: __klp_disable_patch() should never be called for disabled patches (pmladek@suse.com)
  + [4d8a3269df57] [2017-10-20] livepatch: Correctly call klp_post_unpatch_callback() in error paths (pmladek@suse.com)
  + [2599e65e1be6] [2017-10-13] livepatch: add transition notices (joe.lawrence@redhat.com)
  + [e07777531860] [2017-10-13] livepatch: move transition "complete" notice into klp_complete_transition() (joe.lawrence@redhat.com)
  + [4e8c6b0eef6d] [2017-10-13] livepatch: add (un)patch callbacks (joe.lawrence@redhat.com)
  + [fb04e7c3c53f] [2017-09-14] livepatch: __klp_shadow_get_or_alloc() is local to shadow.c (jkosina@suse.cz)
  + [6b7bd7ef29a2] [2017-08-31] livepatch: introduce shadow variable API (joe.lawrence@redhat.com)
  + [9a4ee046afc0] [2019-08-15] Partially revert cc946adcb9e983ad9fe56ebe35f1292e111ff10e (sblbir@amzn.com)
  + [26408adfde0b] [2019-07-11] PCI: Add ACS quirk for Amazon Annapurna Labs root ports (alisaidi@amazon.com)
  + [553ea3b047a7] [2019-07-11] PCI: Add Amazon's Annapurna Labs vendor ID (jonnyc@amazon.com)
  + [087820c173d1] [2019-06-24] linux/ena: update ENA linux driver to version 2.1.1 (fllinden@amazon.com)
  + [fd0584e89ff5] [2019-07-02] microvm: enable debug in case of tcp out of memory (alakeshh@amazon.com)
  + [0a01574f7c34] [2019-07-03] Fix microvm config dependency in Kconfig (alakeshh@amazon.com)
  + [937a7cfe1f0c] [2019-02-12] NFS: Remove redundant semicolon (zhangliguang@linux.alibaba.com)
  + [0ee0cac0c6c9] [2019-05-31] arm64: acpi/pci: invoke _DSM whether to preserve firmware PCI setup (fllinden@amazon.com)
  + [b2c07a0e25b4] [2019-03-28] PCI: al: Add Amazon Annapurna Labs PCIe host controller driver (jonnyc@amazon.com)
  + [47cb2d4235c5] [2019-04-24] irqchip/gic-v2m: invoke from gic-v3 initialization and add acpi quirk flow (zeev@amazon.com)
  + [dd46da8fefbd] [2019-04-03] lustre: fix ACL handling (fllinden@amazon.com)
  + [6cd007a19b01] [2018-05-18] x86/stacktrace: Enable HAVE_RELIABLE_STACKTRACE for the ORC unwinder (jslaby@suse.cz)
  + [92102022a16d] [2018-05-18] x86/unwind/orc: Detect the end of the stack (jpoimboe@redhat.com)
  + [d19798ccaef0] [2018-05-18] x86/stacktrace: Do not fail for ORC with regs on stack (jslaby@suse.cz)
  + [1fcc5f8a4926] [2018-05-18] x86/stacktrace: Clarify the reliable success paths (jslaby@suse.cz)
  + [edcf6278513a] [2018-05-18] x86/stacktrace: Remove STACKTRACE_DUMP_ONCE (jslaby@suse.cz)
  + [1bfc0114f39a] [2018-05-18] x86/stacktrace: Do not unwind after user regs (jslaby@suse.cz)
  + [a483e72e065d] [2019-03-12] Add new config CONFIG_MICROVM to enable microvm optimized kernel (alakeshh@amazon.com)
  + [7047459d5201] [2019-02-19] tcp: Namespace-ify sysctl_tcp_rmem and sysctl_tcp_wmem (edumazet@google.com)
  + [4d090d8a97be] [2017-11-07] net: allow per netns sysctl_rmem and sysctl_wmem for protos (edumazet@google.com)
  + [d75dbcb59513] [2019-03-01] Config glue for lustre client. (fllinden@amazon.com)
  + [4088bb8c06c2] [2019-03-01] Import lustre client 2.10.5 (fllinden@amazon.com)
  + [826214aec2ad] [2018-06-05] iomap: fsync swap files before iterating mappings (darrick.wong@oracle.com)
  + [6dbbe49dc138] [2018-06-01] iomap: inline data should be an iomap type, not a flag (hch@lst.de)
  + [96339cf3b0b7] [2018-05-16] iomap: don't allow holes in swapfiles (osandov@fb.com)
  + [a46d999aa80d] [2018-05-16] iomap: provide more useful errors for invalid swap files (osandov@fb.com)
  + [31576b4ad74b] [2018-05-10] iomap: add a swapfile activation function (darrick.wong@oracle.com)
  + [d2c1702220a0] [2019-01-30] xfs, iomap: define and use the IOMAP_F_DIRTY flag in xfs (fllinden@amazon.com)
  + [f463366898d6] [2018-08-01] xfs: only validate summary counts on primary superblock (darrick.wong@oracle.com)
  + [b1c87ab2b7b1] [2018-07-26] libxfs: add more bounds checking to sb sanity checks (billodo@redhat.com)
  + [46bd44a37a2c] [2018-07-29] xfs: refactor superblock verifiers (darrick.wong@oracle.com)
  + [4d05667de659] [2019-01-31] xen-netfront: call netif_device_attach on resume (fllinden@amazon.com)
  + [e103526182bc] [2018-10-04] ACPI/PPTT: Handle architecturally unknown cache types (jhugo@codeaurora.org)
  + [654dbbcdf26f] [2018-06-05] ACPI / PPTT: fix build when CONFIG_ACPI_PPTT is not enabled (sudeep.holla@arm.com)
  + [2ee880e2d9a2] [2018-06-29] ACPI / PPTT: use ACPI ID whenever ACPI_PPTT_ACPI_PROCESSOR_ID_VALID is set (Sudeep.Holla@arm.com)
  + [ea6c7321182f] [2018-05-11] arm64: topology: divorce MC scheduling domain from core_siblings (jeremy.linton@arm.com)
  + [b40030858a00] [2018-05-11] ACPI: Add PPTT to injectable table list (jeremy.linton@arm.com)
  + [76a1d76a0d37] [2018-05-11] arm64: topology: enable ACPI/PPTT based CPU topology (jeremy.linton@arm.com)
  + [2eae8840e487] [2018-05-11] arm64: topology: rename cluster_id (jeremy.linton@arm.com)
  + [f39c0e5f2d03] [2018-05-11] arm64: Add support for ACPI based firmware tables (jeremy.linton@arm.com)
  + [3545c6c7bedd] [2018-05-11] drivers: base cacheinfo: Add support for ACPI based firmware tables (jeremy.linton@arm.com)
  + [ad09270873cb] [2018-05-11] ACPI: Enable PPTT support on ARM64 (jeremy.linton@arm.com)
  + [1416fd0359e4] [2018-05-11] ACPI/PPTT: Add Processor Properties Topology Table parsing (jeremy.linton@arm.com)
  + [aa4566b3dea4] [2018-05-11] arm64/acpi: Create arch specific cpu to acpi id helper (jeremy.linton@arm.com)
  + [75269e12f07a] [2018-05-11] cacheinfo: rename of_node to fw_token (jeremy.linton@arm.com)
  + [0adc07dcf450] [2018-05-11] drivers: base: cacheinfo: setup DT cache properties early (jeremy.linton@arm.com)
  + [30ad303a6c44] [2018-05-11] drivers: base: cacheinfo: move cache_setup_of_node() (jeremy.linton@arm.com)
  + [dc6f3c134d80] [2017-11-17] ACPICA: ACPI 6.2: Additional PPTT flags (jeremy.linton@arm.com)
  + [efac162ea662] [2018-07-23] arm64: acpi: fix alignment fault in accessing ACPI (takahiro.akashi@linaro.org)
  + [4fd554d23c66] [2018-07-02] arm64: kexec: always reset to EL2 if present (mark.rutland@arm.com)
  + [67f4e96bc83e] [2018-03-08] efi/arm64: Check whether x18 is preserved by runtime services calls (ard.biesheuvel@linaro.org)
  + [41b0952a1160] [2018-10-11] arm64: Fix /proc/iomem for reserved but not memory regions (will.deacon@arm.com)
  + [b61369be673b] [2018-07-23] arm64: export memblock_reserve()d regions via /proc/iomem (james.morse@arm.com)
  + [c39ef6768340] [2018-11-10] net: ena: Import the ENA v2 driver (2.0.2g) (alakeshh@amazon.com)
  + [c2883da24108] [2018-11-10] xen: Only restore the ACPI SCI interrupt in xen_restore_pirqs. (fllinden@amazon.com)
  + [77431940618d] [2018-10-26] xen: restore pirqs on resume from hibernation. (fllinden@amazon.com)
  + [df92243dd94e] [2018-10-29] ACPICA: Enable sleep button on ACPI legacy wake (anchalag@amazon.com)
  + [4d6be08b72e0] [2018-10-18] block: xen-blkfront: consider new dom0 features on restore (eduval@amazon.com)
  + [a8266a0a34b9] [2017-11-30] vmxnet3: increase default rx ring sizes (skhare@vmware.com)
  + [bc426be1be00] [2018-04-27] x86/CPU/AMD: Derive CPU topology from CPUID function 0xB when available (suravee.suthikulpanit@amd.com)
  + [89c85a824b2d] [2017-09-07] sched/topology: Introduce NUMA identity node sched domain (suravee.suthikulpanit@amd.com)
  + [382985e3ffbe] [2018-06-13] x86/CPU/AMD: Fix LLC ID bit-shift calculation (suravee.suthikulpanit@amd.com)
  + [09f988b4425d] [2018-04-27] x86/CPU/AMD: Calculate last level cache ID from number of sharing threads (suravee.suthikulpanit@amd.com)
  + [57b5f4b0b442] [2018-04-27] x86/CPU: Rename intel_cacheinfo.c to cacheinfo.c (bp@suse.de)
  + [f48861c77ba3] [2018-05-17] x86/MCE/AMD: Read MCx_MISC block addresses on any CPU (bp@suse.de)
  + [ec4b9880bdb2] [2018-08-15] blk-wbt: Avoid lock contention and thundering herd issue in wbt_wait (anchalag@amazon.com)
  + [6edca1af4a17] [2018-01-12] blk-mq: simplify queue mapping & schedule with each possisble CPU (hch@lst.de)
  + [afa1c2b69403] [2018-04-09] x86: tsc: avoid system instability in hibernation (eduval@amazon.com)
  + [a43ceb279d70] [2018-06-05] xen-blkfront: Fixed blkfront_restore to remove a call to negotiate_mq (anchalag@amazon.com)
  + [8d3e73f34b05] [2018-03-24] KVM: X86: Fix setup the virt_spin_lock_key before static key get initialized (wanpengli@tencent.com)
  + [72b136126436] [2017-10-28] x86/paravirt: Set up the virt_spin_lock_key after static keys get initialized (douly.fnst@cn.fujitsu.com)
  + [019d1a5d8993] [2018-02-13] KVM: X86: Choose qspinlock when dedicated physical CPUs are available (wanpengli@tencent.com)
  + [89dc6e160b29] [2018-02-13] KVM: Introduce paravirtualization hints and KVM_HINTS_DEDICATED (wanpengli@tencent.com)
  + [923ed65857e7] [2017-09-06] locking/paravirt: Use new static key for controlling call of virt_spin_lock() (jgross@suse.com)
  + [a12e61acf902] [2018-03-27] Revert "xen: dont fiddle with event channel masking in suspend/resume" (anchalag@amazon.com)
  + [503170679185] [2018-01-18] ACPI: SPCR: Make SPCR available to x86 (prarit@redhat.com)
  + [d7b5920fd860] [2016-04-26] xen-blkfront: add 'persistent_grants' parameter (aliguori@amazon.com)
  + [1919b8168501] [2017-03-10] xen-blkfront: resurrect request-based mode (kamatam@amazon.com)
  + [47a5039bc325] [2017-11-02] Not-for-upstream: PM / hibernate: Speed up hibernation by batching requests (cyberax@amazon.com)
  + [5f51ed00826c] [2017-10-27] PM / hibernate: update the resume offset on SNAPSHOT_SET_SWAP_AREA (cyberax@amazon.com)
  + [3c3c13908fbe] [2017-08-24] x86/xen: close event channels for PIRQs in system core suspend callback (kamatam@amazon.com)
  + [6006a9e49737] [2017-08-24] xen/events: add xen_shutdown_pirqs helper function (kamatam@amazon.com)
  + [9c21bd7064d5] [2017-07-21] x86/xen: save and restore steal clock (kamatam@amazon.com)
  + [9630e20eae36] [2017-07-13] xen/time: introduce xen_{save,restore}_steal_clock (kamatam@amazon.com)
  + [be0e804c574c] [2017-01-09] xen-netfront: add callbacks for PM suspend and hibernation support (kamatam@amazon.com)
  + [6063dbd3c4cd] [2017-06-08] xen-blkfront: add callbacks for PM suspend and hibernation (kamatam@amazon.com)
  + [b8bcb9caa36b] [2017-02-11] x86/xen: add system core suspend and resume callbacks (kamatam@amazon.com)
  + [cb0cf7faf3f2] [2018-02-22] x86/xen: Introduce new function to map HYPERVISOR_shared_info on Resume (anchalag@amazon.com)
  + [d8f523fc5964] [2017-07-13] xenbus: add freeze/thaw/restore callbacks support (kamatam@amazon.com)
  + [4440644e53ac] [2017-07-13] xen/manage: introduce helper function to know the on-going suspend mode (kamatam@amazon.com)
  + [22dc52ff136b] [2017-07-12] xen/manage: keep track of the on-going suspend mode (kamatam@amazon.com)
  + [b2f7fb9fa491] [2018-02-27] Importing Amazon ENA driver 1.5.0 into amazon-4.14.y/master. (vallish@amazon.com)
  + [429c220276a8] [2018-02-12] drivers/amazon: introduce AMAZON_ENA_ETHERNET (vallish@amazon.com)
  + [afe75e21f0d5] [2018-02-12] drivers/amazon: add network device drivers support (vallish@amazon.com)
  + [981ba05bfc63] [2018-02-12] drivers: introduce AMAZON_DRIVER_UPDATES (vallish@amazon.com)
  + [4b25072fae60] [2017-10-27] not-for-upstream: testmgr config changes to enable FIPS boot (alakeshh@amazon.com)
  + [16d548b7cebc] [2017-09-19] nvme: update timeout module parameter type (vallish@amazon.com)
  + [f9d27b2f15fe] [2015-12-08] force perf to use /usr/bin/python instead of /usr/bin/python2 (kamatam@amazon.com)
  + [7e27d2fd4134] [2013-02-13] bump default tcp_wmem from 16KB to 20KB (gafton@amazon.com)
  + [b07e2a1fd50d] [2016-01-26] bump the default TTL to 255 (kamatam@amazon.com)
  + [be144c8fdb7f] [2012-02-10] scsi: sd_revalidate_disk prevent NULL ptr deref (kernel-team@fedoraproject.org)
  + [1b24d07cb06b] [2008-10-06] kbuild: AFTER_LINK (roland@redhat.com)


