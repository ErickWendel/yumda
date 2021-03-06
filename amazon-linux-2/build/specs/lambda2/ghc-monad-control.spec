# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name monad-control

Name:           ghc-%{pkg_name}
Version:        0.3.2.1
Release:        2%{?dist}
Summary:        Lift control operations through monad transformers

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-base-unicode-symbols-devel
BuildRequires:  ghc-transformers-devel
BuildRequires:  ghc-transformers-base-devel
# End cabal-rpm deps

Prefix: %{_prefix}

%description
This package defines the type class MonadBaseControl, a subset of
MonadBase into which generic control operations such as catch can be
lifted from IO or any other base monad. Instances are based on monad
transformers in MonadTransControl, which includes all standard monad
transformers in the transformers library except ContT.

See the lifted-base package which uses monad-control to lift IO
operations from the base library (like catch or bracket) into any
monad that is an instance of MonadBase or MonadBaseControl.

This package is a rewrite of Anders Kaseorg's monad-peel library.
The main difference is that this package provides CPS style operators
and exploits the RankNTypes and TypeFamilies language extensions to
simplify and speedup most definitions.  A criterion-based benchmark shows
that monad-control is on average about 99% faster than monad-peel.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install

for file in $(grep -v package.conf.d %{name}-devel.files); do rm -rf %{buildroot}$file || :; done


%files -f %{name}.files
%license LICENSE
%exclude %{ghclibdir}/package.conf.d


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Jens Petersen <petersen@redhat.com> - 0.3.2.1-1
- update to 0.3.2.1
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.4-1
- update to 0.3.1.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.3-2
- rebuild

* Tue May  1 2012 Jens Petersen <petersen@redhat.com> - 0.3.1.3-1
- update to 0.3.1.3

* Thu Mar 22 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-2
- add license to ghc_files

* Thu Jan 26 2012 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- BSD license
- depends on base-unicode-symbols and transformers-base

* Thu Jan 26 2012 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org>
- spec file template generated by cabal2spec-0.25.4
