# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name aeson

Name:           ghc-%{pkg_name}
Version:        0.6.2.1
Release:        3%{?dist}
Summary:        Fast JSON parsing and encoding

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz
# for archs without ghci
Patch1:         aeson-disable-TH.patch

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-attoparsec-devel
BuildRequires:  ghc-blaze-builder-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-deepseq-devel
BuildRequires:  ghc-dlist-devel
BuildRequires:  ghc-hashable-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-template-haskell-devel
BuildRequires:  ghc-text-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-unordered-containers-devel
BuildRequires:  ghc-vector-devel
# End cabal-rpm deps

Prefix: %{_prefix}

%description
A JSON parsing and encoding library optimized for ease of use and
high performance.  Aeson was the father of Jason in Greek mythology.


%prep
%setup -q -n %{pkg_name}-%{version}
%ifnarch %{ghc_arches_with_ghci}
%patch1 -p1 -b .orig
%endif


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

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 20 2014 Jens Petersen <petersen@redhat.com> - 0.6.2.1-2
- disable TH module on arch's without ghci

* Wed Jan 22 2014 Jens Petersen <petersen@redhat.com> - 0.6.2.1-1
- update to 0.6.2.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Jens Petersen <petersen@redhat.com> - 0.6.1.0-2
- update to new simplified Haskell Packaging Guidelines

* Mon Mar 11 2013 Jens Petersen <petersen@redhat.com> - 0.6.1.0-1
- update to 0.6.1.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.2-5
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.2-3
- rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.2-2
- rebuild

* Sun May  6 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.2-1
- update to 0.6.0.2
- build needs ghci

* Sat Mar 24 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.0-2
- depends on dlist for ghc > 7.2

* Mon Feb 27 2012 Jens Petersen <petersen@redhat.com> - 0.6.0.0-1
- BSD license
- doc files

* Mon Feb 27 2012 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org>
- spec file template generated by cabal2spec-0.25.4
