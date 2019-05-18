%global _trivial .0
%global _buildid .4
%if 0%{?rhel}
%define with_private_llvm 1
%else
%define with_private_llvm 0
%endif

%define with_vdpau 1

%define with_llvm 1

%define _default_patch_fuzz 2

%define gitdate 20171019
#% define snapshot 

Summary: Mesa graphics libraries
Name: mesa
Version: 17.2.3
Release: 8.%{gitdate}%{?dist}%{?_trivial}%{?_buildid}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

# Source0: MesaLib-%{version}.tar.xz
Source0: %{name}-%{gitdate}.tar.xz
Source1: sanitize-tarball.sh
Source2: make-release-tarball.sh
Source3: make-git-snapshot.sh

# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source4 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source4: Mesa-MLAA-License-Clarification-Email.txt

Patch0: mesa-17.3-final.patch
Patch1: nv50-fix-build.patch
Patch2: 0001-mesa-Squash-merge-of-S3TC-support.patch
Patch9: mesa-8.0-llvmpipe-shmget.patch
Patch12: mesa-8.0.1-fix-16bpp.patch
Patch15: mesa-9.2-hardware-float.patch
Patch20: mesa-10.2-evergreen-big-endian.patch

# For bz1503861, fix visual artifacts on DRI PRIME offloading
# Feel free to drop these patches during the next mesa rebase (>17.2.3)
Patch30: 0001-intel-blorp-Use-mocs.tex-for-depth-stencil.patch
Patch31: 0002-anv-blorp-Add-a-device-parameter-to-blorp_surf_for_a.patch
Patch32: 0003-blorp-Turn-anv_CmdCopyBuffer-into-a-blorp_buffer_cop.patch
Patch33: 0004-intel-blorp-Make-the-MOCS-setting-part-of-blorp_addr.patch
Patch34: 0005-i965-Use-PTE-MOCS-for-all-external-buffers.patch

Patch40: 0001-intel-Add-more-Coffee-Lake-PCI-IDs.patch

Patch1000: glvnd-fix-gl-dot-pc.patch

BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: kernel-headers
BuildRequires: xorg-x11-server-devel
BuildRequires: libatomic
BuildRequires: libdrm-devel >= 2.4.83
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: makedepend
BuildRequires: libselinux-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: libxshmfence-devel
BuildRequires: elfutils
BuildRequires: python
BuildRequires: python-mako
BuildRequires: gettext
%if 0%{?with_private_llvm}
BuildRequires: llvm-private-devel >= 5.0
%else
BuildRequires: llvm-devel >= 3.0
%endif
BuildRequires: elfutils-libelf-devel
BuildRequires: libxml2-python
BuildRequires: libudev-devel
BuildRequires: bison flex
BuildRequires: pkgconfig(wayland-client) >= 1.11
BuildRequires: pkgconfig(wayland-server) >= 1.11
BuildRequires: pkgconfig(wayland-protocols) >= 1.8.0
BuildRequires: mesa-libGL-devel
%if 0%{?with_vdpau}
BuildRequires: libvdpau-devel
%endif
BuildRequires: zlib-devel
BuildRequires: libglvnd-core-devel

Prefix: %{_prefix}

%description
Mesa

%package filesystem
Summary: Mesa driver filesystem
Group: User Interface/X Hardware Support
Provides: mesa-dri-filesystem = %{version}-%{release}
Obsoletes: mesa-dri-filesystem < %{version}-%{release}
Prefix: %{_prefix}
%description filesystem
Mesa driver filesystem

%package libOSMesa
Summary: Mesa offscreen rendering libraries
Group: System Environment/Libraries
Provides: libOSMesa
Requires: mesa-libglapi = %{version}-%{release}
Prefix: %{_prefix}

%description libOSMesa
Mesa offscreen rendering libraries


%package libwayland-egl
Summary: Mesa libwayland-egl library
Group: System Environment/Libraries
Provides: libwayland-egl
Prefix: %{_prefix}

%description libwayland-egl
Mesa libwayland-egl runtime library.


%package libglapi
Summary: Mesa shared glapi
Group: System Environment/Libraries
Prefix: %{_prefix}

%description libglapi
Mesa shared glapi

%prep
#setup -q -n Mesa-%{version}%{?snapshot}
%setup -q -n mesa-%{gitdate}
# make sure you run sanitize-tarball.sh on mesa source tarball or next line will exit
grep -q ^/ src/gallium/auxiliary/vl/vl_decoder.c && exit 1
%patch0 -p1 -b .mesa17.2.3
%patch1 -p1 -b .nv50rtti
%patch2 -p1 -b .s3tc

# this fastpath is:
# - broken with swrast classic
# - broken on 24bpp
# - not a huge win anyway
# - ABI-broken wrt upstream
# - eventually obsoleted by vgem
#
# dear ajax: fix this one way or the other
#patch9 -p1 -b .shmget
#patch12 -p1 -b .16bpp

%patch15 -p1 -b .hwfloat
#patch20 -p1 -b .egbe

%patch30 -p1 -b .bz1503861_patch1
%patch31 -p1 -b .bz1503861_patch2
%patch32 -p1 -b .bz1503861_patch3
%patch33 -p1 -b .bz1503861_patch4
%patch34 -p1 -b .bz1503861_patch5

%patch40 -p1 -b .cfl_ids
%patch1000 -p1 -b .pc_fix

%if 0%{with_private_llvm}
sed -i 's/\[llvm-config\]/\[llvm-private-config-%{__isa_bits}\]/g' configure.ac
sed -i 's/`$LLVM_CONFIG --version`/$LLVM_VERSION_MAJOR.$LLVM_VERSION_MINOR-rhel/' configure.ac
%endif

sed -i 's|LIBGLVND_DATADIR=.*$|LIBGLVND_DATADIR="%{_datadir}"|' configure.ac

# need to use libdrm_nouveau2 on F17
%if !0%{?rhel}
%if 0%{?fedora} < 18
sed -i 's/\<libdrm_nouveau\>/&2/' configure.ac
%endif
%endif

cp %{SOURCE4} docs/

%build

autoreconf --install

export CFLAGS="$RPM_OPT_FLAGS"
# C++ note: we never say "catch" in the source.  we do say "typeid" once,
# in an assert, which is patched out above.  LLVM doesn't use RTTI or throw.
#
# We do say 'catch' in the clover and d3d1x state trackers, but we're not
# building those yet.
export CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define asm_flags --disable-asm
%endif

%configure \
    %{?asm_flags} \
    --enable-selinux \
    --enable-osmesa \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
    --disable-xvmc \
    --enable-vdpau \
    --with-platforms=x11,drm,wayland \
    --enable-shared-glapi \
    --enable-gbm \
    --disable-opencl \
    --enable-glx-tls \
    --enable-libglvnd \
    --enable-texture-float=yes \
    --with-vulkan-drivers=radeon,intel \
    --enable-llvm \
    --enable-dri \
    --enable-xa \
    --with-gallium-drivers=svga,radeonsi,swrast,r600,r300,nouveau,virgl \
    --with-dri-drivers=nouveau,radeon,r200,i915,i965

make %{?_smp_mflags} MKDEP=/bin/true

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files filesystem
%defattr(-,root,root,-)
%license docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%dir %{_libdir}/vdpau

%files libglapi
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%files libOSMesa
%defattr(-,root,root,-)
%{_libdir}/libOSMesa.so.8*

%files libwayland-egl
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so.1
%{_libdir}/libwayland-egl.so.1.*

%exclude %{_sysconfdir}
%exclude %{_includedir}
%exclude %{_datadir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/dri
%exclude %{_libdir}/vdpau
%exclude %{_libdir}/libEGL*
%exclude %{_libdir}/libGLES*
%exclude %{_libdir}/libGLX*
%exclude %{_libdir}/libgbm*
%exclude %{_libdir}/libxatracker*

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Jun 12 2018 Praveen Paladugu <praween@amazon.com> - 17.2.3-8.20171019.0.1
- enable libglvnd support

* Mon Jan 15 2018 Dave Airlie <airlied@redhat.com> - 17.2.3-8.20171019
- Add missing Intel CFL ids.

* Thu Nov 30 2017 Lyude Paul <lyude@redhat.com> - 17.2.3-7.20171019
- Add patches to fix cache lines with DRI_PRIME + amdgpu (#1503861)

* Fri Nov 17 2017 Dave Airlie <airlied@redhat.com> - 17.2.3-6.20171019
- fix libgbm/dri-drivers requires on libdrm

* Wed Oct 25 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 17.2.3-5.20171019
- Enable hardware drivers on aarch64 (#1358444)

* Tue Oct 24 2017 Dave Airlie <airlied@redhat.com> - 17.2.3-4.20171019
- Update gitdate and clean out sources.

* Tue Oct 24 2017 Dave Airlie <airlied@redhat.com> - 17.2.3-3.20171019
- Add final 17.2.3 patch.

* Thu Oct 19 2017 Tom Stellard <tstellar@redhat.com> - 17.2.3-2.20171019
- Switch to llvm-private

* Thu Oct 19 2017 Dave Airlie <airlied@redhat.com> - 17.2.3-1.20171019
- rebase to 17.2.3

* Thu Oct 05 2017 Dave Airlie <airlied@redhat.com> - 17.2.2-1.20171005
- rebase to 17.2.2 final release + s3tc support

* Thu Sep 28 2017 Olivier Fourdan <ofourdan@redhat.com> - 17.2.0-2.20170911
- Enable wayland-egl, add dependencies on wayland-protocols (#1481412)

* Mon Sep 11 2017 Dave Airlie <airlied@redhat.com> - 17.2.0-1.20170911
- rebase to 17.2.0 final release

* Tue Aug 15 2017 Dave Airlie <airlied@redhat.com> - 17.2.0-0.1.20170815
- rebase to 17.2-rc4

* Thu May 11 2017 Dave Airlie <airlied@redhat.com> - 17.0.1-6.20170307
- enable VDPAU drivers (#1297276)

* Tue May 09 2017 Tom Stellard <tstellar@redhat.com> - 17.0.1-5.20170307
- Use correct datalayout for llvmpipe (#1445423)

* Fri May 05 2017 Adam Jackson <ajax@redhat.com> - 17.0.1-4.20170307
- Add ppc64le vulkan build

* Wed May 03 2017 Lyude Paul <lyude@redhat.com> - 17.0.1-3.20170307
- Add temporary revert for #1438891

* Tue Mar 28 2017 Dave Airlie <airlied@redhat.com> - 17.0.1-2.20170307
- Allow compat shaders override. (#1429813)

* Tue Mar 07 2017 Dave Airlie <airlied@redhat.com> - 17.0.1-1.20170307
- mesa 17.0.1 release

* Tue Feb 28 2017 Dave Airlie <airlied@redhat.com> - 17.0.0-2.20170215
- enable more drivers on aarch64 + vulkan drivers (#1358444)

* Wed Feb 15 2017 Dave Airlie <airlied@redhat.com> - 17.0.0-1.20170215
- mesa 17.0.0 release

* Mon Feb 06 2017 Adam Jackson <ajax@redhat.com> - 17.0.0-0.2.20170123
- Rebuild against (and BuildRequire) mesa-private-llvm >= 3.9

* Mon Jan 23 2017 Dave Airlie <airlied@redhat.com> - 17.0.0-0.1.20170123
- mesa 17.0.0-rc1

* Tue Aug 09 2016 Rob Clark <rclark@redhat.com> - 11.2.2-2.20160614
- update kbl pci ids.

* Tue Jun 14 2016 Dave Airlie <airlied@redhat.com> - 11.2.2-1.20160614
- mesa 11.2.2 release

* Tue Apr 05 2016 Dave Airlie <airlied@redhat.com> 11.2.0-1.20160405
- mesa 11.2.0 final release

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 11.2.0-0.2.20160310
- mesa 11.2.0-rc2 release + enable virgl

* Thu Sep 17 2015 Oded Gabbay <oded.gabbay@redhat.com> 10.6.5-3.20150824
- Fix texture compression for big-endian (#1250168)

* Wed Sep 16 2015 Oded Gabbay <oded.gabbay@redhat.com> 10.6.5-2.20150824
- Fix llvmpipe implicit conversion for POWER (#1261988)

* Mon Aug 24 2015 Oded Gabbay <oded.gabbay@redhat.com> 10.6.5-1.20150824
- mesa 10.6.5 release

* Tue Jun 16 2015 Dave Airlie <airlied@redhat.com> 10.6.0-1.20150616
- mesa 10.6.0 release

* Thu May 28 2015 Dave Airlie <airlied@redhat.com> 10.6.0-0.3.20150528
- mesa 10.6.0-rc2

* Fri May 22 2015 Dave Airlie <airlied@redhat.com> 10.6.0-0.2.20150521
- rebuild for ppc64le relro issue

* Thu May 21 2015 Dave Airlie <airlied@redhat.com> 10.6.0-0.1.20150521
- mesa 10.6.0-rc1

* Wed Jan 28 2015 Adam Jackson <ajax@redhat.com> 10.2.7-5.20140910
- Fix color clears and colorformat selection on big-endian evergreen

* Wed Sep 17 2014 Dave Airlie <airlied@redhat.com> 10.2.7-3.20140910
- backport regression fix for old x86 cpus

* Wed Sep 17 2014 Dave Airlie <airlied@redhat.com> 10.2.7-2.20140910
- backport upstream big endian format fixes

* Wed Sep 10 2014 Dave Airlie <airlied@redhat.com> 10.2.7-1.20140910
- rebase to latest 10.2.x branch - fixes HSW gnome-shell

* Tue Sep 09 2014 Adam Jackson <ajax@redhat.com> 10.2.5-3.20140827
- Backport a ppc64le fix

* Wed Aug 27 2014 Adam Jackson <ajax@redhat.com> 10.2.5-2.20140827
- Rebuild against llvm 3.5.0rc3

* Wed Aug 27 2014 Dave Airlie <airlied@redhat.com> 10.2.5-1.20140827
- rebase to 10.2.5 (well .6 in branch has hawaii fixes)

* Mon Feb 24 2014 Dave Airlie <airlied@redhat.com> 9.2.5-5.20131218
- fix GLX attribs against binary drivers (#1064117)

* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 9.2.5-4.20131218
- Mass rebuild

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 9.2.5-3.20131218
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Dave Airlie <airlied@redhat.com> 9.2.5-2.20131218
- obsolete correct dri1 drivers package (#1043903)

* Mon Jan 13 2014 Dave Airlie <airlied@redhat.com> 9.2.5-1.20131218
- rebase to final 9.2.5 release + copy sub buffer enable for swrast

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 9.2-5.20131023
- Mass rebuild 2013-12-27

* Wed Nov 06 2013 Dave Airlie <airlied@redhat.com> 9.2-4.20131023
- fix build for now on aarch64

* Thu Oct 31 2013 Jerome Glisse <jglisse@redhat.com> 9.2-3.20131023
- Add missing kaveri pci id

* Wed Oct 23 2013 Jerome Glisse <jglisse@redhat.com> 9.2-2.20131023
- 9.2 upstream release + fixes from git branch

* Mon Sep 02 2013 Dave Airlie <airlied@redhat.com> 9.2-1.20130902
- 9.2 upstream release + fixes from git branch

* Tue Jul 23 2013 Adam Jackson <ajax@redhat.com> 9.2-0.14.20130723
- Today's git snap of 9.2 branch

* Sun Jul 14 2013 Kyle McMartin <kyle@redhat.com> 9.2-0.13.20130610
- Use LLVM::MCJIT on ARM and AArch64.

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.12.20130610
- Re-enable hardware float support (#975204)

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.11.20130610
- Fix evergreen on big-endian

* Wed Jun 12 2013 Adam Jackson <ajax@redhat.com> 9.2-0.10.20130610
- Fix s390x build
- Fold khrplatform-devel in to libEGL-devel

* Tue Jun 11 2013 Adam Jackson <ajax@redhat.com> 9.2-0.9.20130610
- 0001-Revert-i965-Disable-unused-pipeline-stages-once-at-s.patch: Fix some
  hangs on ivb+

* Mon Jun 10 2013 Adam Jackson <ajax@redhat.com> 9.2-0.8.20130610
- Today's git snap

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 9.2-0.7.20130528
- Today's git snap

* Sun May 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 9.2-0.6.20130514
- Update the name of the freedreno driver

* Fri May 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.5.20130514
- Fix build issues on ppc32

* Thu May 16 2013 Adam Jackson <ajax@redhat.com> 9.2-0.4.20130514
- Fix yet more build issues on s390{,x}

* Wed May 15 2013 Adam Jackson <ajax@redhat.com> 9.2-0.3.20130514
- Fix build ordering issue on s390x

* Wed May 15 2013 Adam Jackson <ajax@redhat.com> 9.2-0.2.20130514
- Fix filesystem for with_hardware == 0

* Tue May 14 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1.20130514
- Today's git snap
- Revert to swrast on ppc32 and s390 since llvm doesn't actually work
- Build freedreno on arm
- Drop snb hang workaround (upstream 1dfea559)
- Rename filesystem package

* Wed May 08 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1.20130508
- Switch to Mesa master (pre 9.2)
- Fix llvmpipe on big-endian and enable llvmpipe everywhere
- Build vdpau drivers for r600/radeonsi/nouveau
- Enable hardware floating-point texture support
- Drop GLESv1, nothing's using it, let's not start

* Sat Apr 27 2013 Dave Airlie <airlied@redhat.com> 9.1.1-1
- rebase to Mesa 9.1.1 + fixes from git

* Thu Apr 11 2013 Dave Airlie <airlied@redhat.com> 9.1-6
- enable glx tls for glamor to work properly

* Thu Apr 04 2013 Adam Jackson <ajax@redhat.com> 9.1-5
- Enable llvmpipe even on non-SSE2 machines (#909473)

* Tue Mar 26 2013 Adam Jackson <ajax@redhat.com> 9.1-4
- Fix build with private LLVM

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 9.1-3
- mesa-9.1-53-gd0ccb5b.patch: Sync with today's git

* Tue Mar 19 2013 Dave Airlie <airlied@redhat.com> 9.1-2
- add SNB hang workaround from chromium

* Fri Mar 08 2013 Adam Jackson <ajax@redhat.com> 9.1-1
- Mesa 9.1

* Wed Feb 27 2013 Dan Horák <dan[at]danny.cz> - 9.1-0.4
- /etc/drirc is always created, so exclude it on platforms without hw drivers

* Tue Feb 26 2013 Adam Jackson <ajax@redhat.com> 9.1-0.3
- Fix s390*'s swrast to be classic not softpipe

* Tue Feb 19 2013 Jens Petersen <petersen@redhat.com> - 9.1-0.2
- build against llvm-3.2
- turn on radeonsi

* Wed Feb 13 2013 Dave Airlie <airlied@redhat.com> 9.1-0.1
- snapshot mesa 9.1 branch

* Tue Jan 15 2013 Tom Callaway <spot@fedoraproject.org> 9.0.1-4
- clarify license on pp_mlaa* files

* Thu Dec 20 2012 Adam Jackson <ajax@redhat.com> 9.0.1-3
- mesa-9.0.1-22-gd0a9ab2.patch: Sync with git
- Build with -fno-rtti -fno-exceptions, modest size and speed win
- mesa-9.0.1-less-cxx-please.patch: Remove the only use of typeid() so the
  above works.

* Wed Dec 05 2012 Adam Jackson <ajax@redhat.com> 9.0.1-2
- Allow linking against a private version of LLVM libs for RHEL7
- Build with -j again

* Mon Dec 03 2012 Adam Jackson <ajax@redhat.com> 9.0.1-1
- Mesa 9.0.1

* Wed Nov 07 2012 Dave Airlie <airlied@redhat.com> 9.0-5
- mesa-9.0-19-g895a587.patch: sync with 9.0 branch with git
- drop wayland patch its in git now.

* Thu Nov 01 2012 Adam Jackson <ajax@redhat.com> 9.0-4
- mesa-9.0-18-g5fe5aa8: sync with 9.0 branch in git
- Portability fixes for F17: old wayland, old llvm.

* Sat Oct 27 2012 Dan Horák <dan[at]danny.cz> 9.0-3
- gallium drivers must be set explicitely for s390(x) otherwise also r300, r600 and vmwgfx are built

* Fri Oct 19 2012 Adam Jackson <ajax@redhat.com> 9.0-2
- Rebuild for wayland 0.99

* Wed Oct 10 2012 Adam Jackson <ajax@redhat.com> 9.0-1
- Mesa 9.0
- mesa-9.0-12-gd56ee24.patch: sync with 9.0 branch in git

* Wed Oct 10 2012 Adam Jackson <ajax@redhat.com> 9.0-0.4
- Switch to external gl-manpages and libGLU
- Drop ShmGetImage fastpath for a bit

* Mon Oct 01 2012 Dan Horák <dan[at]danny.cz> 9.0-0.3
- explicit BR: libGL-devel is required on s390(x), it's probbaly brought in indirectly on x86
- gallium drivers must be set explicitely for s390(x) otherwise also r300, r600 and vmwgfx are built

* Mon Sep 24 2012 Adam Jackson <ajax@redhat.com> 9.0-0.2
- Switch to swrast classic instead of softpipe for non-llvm arches
- Re-disable llvm on ppc until it can draw pixels

* Mon Sep 24 2012 Dave Airlie <airlied@redhat.com> 9.0-0.1
- rebase to latest upstream 9.0 pre-release branch
- add back glu from new upstream (split for f18 later)

* Fri Sep 14 2012 Dave Airlie <airlied@redhat.com> 8.1-0.21
- why fix one yylex when you can fix two

* Fri Sep 14 2012 Dave Airlie <airlied@redhat.com> 8.1-0.20
- fix yylex collision reported on irc by hughsie

* Mon Aug 27 2012 Adam Jackson <ajax@redhat.com> 8.1-0.19
- Today's git snap
- Revert dependency on libkms
- Patch from Mageia to fix some undefined symbols

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.18
- parallel make seems broken - on 16 way machine internally.

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 8.1-0.17
- upstream snapshot

* Wed Jul 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 8.1-0.16
- Enable LLVM on ARM

* Wed Jul 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 8.1-0.15
- Fix building on platforms with HW and without LLVM

* Tue Jul 24 2012 Adam Jackson <ajax@redhat.com> 8.1-0.14
- Re-enable llvm on ppc, being worked on
- Don't BuildReq on wayland things in RHEL

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 8.1-0.13
- Build radeonsi (#842194)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1-0.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.11
- upstream snapshot: fixes build issues

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.10
- snapshot mesa: add some build hackarounds 

* Sat Jul 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 8.1-0.9
- Call ldconfig at -libglapi and -libxatracker post(un)install time.
- Drop redundant ldconfig dependencies, let rpm auto-add them.

* Wed Jun 13 2012 Dave Airlie <airlied@redhat.com> 8.1-0.8
- enable shared llvm usage.

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 8.1-0.7
- Disable llvm on non-x86 (#829020)

* Sun Jun 03 2012 Dave Airlie <airlied@redhat.com> 8.1-0.6
- rebase to git master + build on top of llvm 3.1

* Thu May 17 2012 Adam Jackson <ajax@redhat.com> 8.1-0.5
- mesa-8.0-llvmpipe-shmget.patch: Rediff for 8.1.

* Thu May 10 2012 Karsten Hopp <karsten@redhat.com> 8.1-0.4
- revert disabling of hardware drivers, disable only llvm on PPC*
  (#819060)

* Tue May 01 2012 Adam Jackson <ajax@redhat.com> 8.1-0.3
- More RHEL tweaking: no pre-DX7 drivers, no wayland.

* Thu Apr 26 2012 Karsten Hopp <karsten@redhat.com> 8.1-0.2
- move drirc into with_hardware section (Dave Airlie)
- libdricore.so and libglsl.so get built and installed on
  non-hardware archs, include them in the file list

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 8.1-0.2
- Don't build vmware stuff on non-x86 (#815444)

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> 8.0.3-0.1
- Rebuild with new git snapshot
- Remove upstreamed patches
