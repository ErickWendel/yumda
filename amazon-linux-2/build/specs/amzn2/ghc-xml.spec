# https://fedoraproject.org/wiki/Packaging:Haskell

%global pkg_name xml

Name:           ghc-%{pkg_name}
Version:        1.3.13
Release:        2%{?dist}
Summary:        A simple XML library

License:        BSD
URL:            http://hackage.haskell.org/package/%{pkg_name}
Source0:        http://hackage.haskell.org/packages/archive/%{pkg_name}/%{version}/%{pkg_name}-%{version}.tar.gz

BuildRequires:  ghc-Cabal-devel
BuildRequires:  ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-text-devel
# End cabal-rpm deps

%description
A simple XML library.


%package devel
Summary:        Haskell %{pkg_name} library development files
Requires:       ghc-compiler = %{ghc_version}
Requires(post): ghc-compiler = %{ghc_version}
Requires(postun): ghc-compiler = %{ghc_version}
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides the Haskell xml library development files.


%prep
%setup -q -n %{pkg_name}-%{version}


%build
%ghc_lib_build


%install
%ghc_lib_install


%post devel
%ghc_pkg_recache


%postun devel
%ghc_pkg_recache


%files -f %{name}.files
%doc LICENSE


%files devel -f %{name}-devel.files


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Jens Petersen <petersen@redhat.com> - 1.3.13-1
- update to 1.3.13
- update to new simplified Haskell Packaging Guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 1.3.12-6
- update with cabal-rpm

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jens Petersen <petersen@redhat.com> - 1.3.12-4
- change prof BRs to devel

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 1.3.12-3
- rebuild

* Fri Mar 23 2012 Jens Petersen <petersen@redhat.com> - 1.3.12-2
- add license to ghc_files

* Tue Feb  7 2012 Jens Petersen <petersen@redhat.com> - 1.3.12-1
- update to 1.3.12

* Wed Jan  4 2012 Jens Petersen <petersen@redhat.com> - 1.3.10-1
- update to 1.3.10 and cabal2spec-0.25.2
- new dependency on text library

* Mon Oct 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.9-1.3
- rebuild with new gmp without compat lib

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.9-1.2
- rebuild with new gmp without compat lib

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 1.3.9-1.1
- rebuild with new gmp

* Mon Jul 25 2011 Ben Boeckel <mathstuf@gmail.com> - 1.3.9-1
- Update to 1.3.9

* Sat Jul 09 2011 Ben Boeckel <mathstuf@gmail.com> - 1.3.8-3
- Update to cabal2spec-0.24

* Wed Jun 22 2011 Jens Petersen <petersen@redhat.com> - 1.3.8-2
- use ghc_arches (cabal2spec-0.23.2)

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 1.3.8-1
- update to 1.3.8
- update to cabal2spec-0.23: add ppc64

* Thu Mar 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.7-3
- Enable build on sparcv9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 05 2010 Ben Boeckel <mathstuf@gmail.com> - 1.3.7-1
- Initial package

* Sun Sep  5 2010 Fedora Haskell SIG <haskell-devel@lists.fedoraproject.org> - 1.3.7-0
- initial packaging for Fedora automatically generated by cabal2spec-0.22.2
