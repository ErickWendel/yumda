# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name hslua

Name:           ghc-%{pkg_name}
Version:        0.3.10
Release:        1.1%{?dist}
Summary:        Lua language interpreter embedded in Haskell

License:        MIT
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-mtl-devel
BuildRequires:  pkgconfig(lua)
# End cabal-rpm deps

Prefix: %{_prefix}

%description
The Scripting.Lua module is a wrapper of the Lua language interpreter described
in www.lua.org.


%prep
%setup -q -n %{pkg_name}-%{version}

cabal-tweak-flag system-lua True
rm src/*.c src/*.h


%build
%ghc_lib_build


%install
%ghc_lib_install

for file in $(grep -v package.conf.d %{name}-devel.files); do rm -rf %{buildroot}$file || :; done


%files -f %{name}.files
%license COPYRIGHT
%exclude %{ghclibdir}/package.conf.d


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sat Dec  3 2016 Jens Petersen <petersen@redhat.com> - 0.3.10-1.1
- rebuild

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.3.10-1
- update to 0.3.10 (#1009375)
- update license to MIT (#1009375)
  see https://github.com/osa1/hslua/issues/14
- system-lua patch is now upstream
- tweak summary and description

* Wed Oct 16 2013 Jens Petersen <petersen@redhat.com> - 0.3.6.1-2
- add static provides to devel

* Wed Sep 18 2013 Jens Petersen <petersen@redhat.com> - 0.3.6.1-1
- summary and description
- patch to use system lua

* Wed Sep 18 2013 Fedora Haskell SIG <haskell@lists.fedoraproject.org> - 0.3.6.1-0
- spec file generated by cabal-rpm-0.8.3
