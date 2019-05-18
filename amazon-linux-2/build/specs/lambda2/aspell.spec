Summary: Spell checker
Name: aspell
Version: 0.60.6.1
Release: 9%{?dist}.0.1
Epoch: 12
# LGPLv2+ .. common/gettext.h
# LGPLv2  .. modules/speller/default/phonet.hpp,
#            modules/speller/default/phonet.cpp,
#            modules/speller/default/affix.cpp
# GPLv2+  .. ltmain.sh, misc/po-filter.c
# BSD     .. myspell/munch.c
License: LGPLv2+ and LGPLv2 and GPLv2+ and BSD
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz

Patch0: aspell-0.60.3-install_info.patch
Patch1: aspell-0.60.5-fileconflict.patch
Patch2: aspell-0.60.5-pspell_conf.patch
# resolves: #447428
Patch3: aspell-0.60.6-zero.patch
Patch4: aspell-0.60.6-mp.patch
# resolves: #813261
Patch5: aspell-0.60.6.1-dump-personal-abort.patch
# resolves: #925034
Patch6: aspell-0.60.6.1-aarch64.patch

BuildRequires: chrpath, gettext, ncurses-devel, pkgconfig

Prefix: %{_prefix}

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%prep
%setup -q
%patch0 -p1 -b .iinfo
%patch1 -p1 -b .fc
%patch2 -p1 -b .mlib
%patch3 -p1 -b .zero
%patch4 -p1 -b .ai
%patch5 -p1 -b .dump-personal
%patch6 -p1 -b .aarch64
iconv -f iso-8859-2 -t utf-8 < manual/aspell.info > manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

patch -p1 <<\EOF
From 8089fa02122fed0a6394eba14bbedcb1d18e2384 Mon Sep 17 00:00:00 2001
From: Kevin Atkinson <kevina@gnu.org>
Date: Thu, 29 Dec 2016 00:50:31 -0500
Subject: [PATCH] Compile Fixes for GCC 7.

Closes #519.
---
 modules/filter/tex.cpp | 2 +-
 prog/check_funs.cpp    | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)

diff --git a/modules/filter/tex.cpp b/modules/filter/tex.cpp
index a979539..19ab63c 100644
--- a/modules/filter/tex.cpp
+++ b/modules/filter/tex.cpp
@@ -174,7 +174,7 @@ namespace {
 
     if (c == '{') {
 
-      if (top.in_what == Parm || top.in_what == Opt || top.do_check == '\0')
+      if (top.in_what == Parm || top.in_what == Opt || *top.do_check == '\0')
 	push_command(Parm);
 
       top.in_what = Parm;
diff --git a/prog/check_funs.cpp b/prog/check_funs.cpp
index db54f3d..89ee09d 100644
--- a/prog/check_funs.cpp
+++ b/prog/check_funs.cpp
@@ -647,7 +647,7 @@ static void print_truncate(FILE * out, const char * word, int width) {
     }
   }
   if (i == width-1) {
-    if (word == '\0')
+    if (*word == '\0')
       put(out,' ');
     else if (word[len] == '\0')
       put(out, word, len);
EOF

%build
%configure --disable-rpath
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
# make install DESTDIR=$RPM_BUILD_ROOT doesn't work
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//nroff-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//sgml-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//context-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//email-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//tex-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//texinfo-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_bindir}/aspell
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/libpspell.so.*

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libaspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libpspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*-filter.la
rm -f ${RPM_BUILD_ROOT}%{_bindir}/aspell-import

%files
%license COPYING
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*

%exclude %{_mandir}
%exclude %{_datadir}
%exclude %{_includedir}
%exclude %{_bindir}/pspell-config
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 12:0.60.6.1-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 12:0.60.6.1-8
- Mass rebuild 2013-12-27

* Mon Mar 25 2013 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-7
- resolves: #925034
  add support for aarch64

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-5
- done some minor .spec file cleanup

* Thu Jul 19 2012 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-4
- resolves: #813261
  fixed crash when trying to run "aspell dump personal"

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-1
- resolves: #718946
  update to 0.60.6.1

* Mon May  2 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 12.0.60.6-15
- fix minor problems in spec file

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 12.0.60.6-13
- remove obsolete links from man-pages

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 12.0.60.6-12
- fix -devel scriptlets

* Tue Dec 15 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-11
- remove obsolete patch

* Fri Dec  4 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-10
- fix rpath problem (chrpath)

* Tue Dec  1 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-9
- add --disable-rpath to configure part
  remove remanent obsolete tags
  fix license field

* Fri Nov 27 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-8
- change summary name
  remove outdated Obsoletes, Conflicts and Provides flag
  fix requirement to install-info (pre -> post)
  move aspell-import to documentation part
  remove exit 0 from scriptlets

* Mon Aug 10 2009 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-7
- fix installation with --excludedocs option (#515911)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-4
- remove aspell-en require

* Mon Sep  1 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-3
- fix patch format

* Thu May 29 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-2
- Resolves: #447428
  aspell sigserv on checking file with 0 length

* Wed May  7 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-1
- update to 0.60.6

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 12:0.60.5-5
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-4
- add gcc43 patch

* Thu Feb  8 2007 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-3
- incorporate package review feedback

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-2
- Resolves: 223676
  fix non-failsafe install-info problem

* Tue Jan  2 2007 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-1
- update to 0.60.4
- cleanup spec file

* Wed Nov  8 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.4-1
- update to 0.60.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 12:0.60.3-7.1
- rebuild

* Tue May 23 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-7
- fix multilib problem (used pkgconfig)

* Wed Mar 22 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-6
- remove .la files (bug 184184)

* Thu Mar  2 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-5
- update aspell man page (bug 183205)

* Tue Feb 21 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-4
- fix multilib file conflict

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 12:0.60.3-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 12:0.60.3-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Ivana Varekova <varekova@redhat.com> 12:0.60.3-3
- fix for gcc 4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 15 2005 Ivana Varekova <varekova@redhat.com> 12:0.60.3-2
- fix install-info problem 

* Wed Jul 13 2005 Ivana Varekova <varekova@redhat.com> 12:0.60.3-1
- update to 0.60.3 - (bug 141968) thanks to Dawid Gajownik 
- add BuildRequires: ncurses-devel, gettext 
- add config script patch (thanks tmraz@redhat.com)


* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 12:0.50.5-6
- rebuilt

* Thu Jan 13 2005 Adrian Havill <havill@redhat.com> 12:0.50.5-5
- added aspell-pt_BR to the obsoletes

* Fri Nov 12 2004 Warren Togami <wtogami@redhat.com> 12:0.50.5-4
- rebuild

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 12:0.50.5-3.fc3
- add obsolete aspell-config

* Mon Aug 23 2004 Adrian Havill <havill@redhat.com> 12:0.50.5-2.fc3
- fix doc dir (#128140) (don't flag aspell doc stuff with the doc macro
  flag due to rpm badness)

* Mon Jun 21 2004 Warren Togami <wtogami@redhat.com> 12:0.50.5-1
- update to 0.50.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Adrian Havill <havill@redhat.com> 12:0.50.50.3-18
- make rpm own some unclaimed dirs (#112984, #113778)
- explicitly claim kbd anbd dat files in /usr/share/aspell
- a little spec file files cleanup-- macro subs, dir prefix
- make /usr/lib/aspell; don't make the dictionary packages do it

* Mon Nov 17 2003 Thomas Woerner <twoerner@redhat.com> 12:0.50.3-17
- fixed build: added make to %%build to avoid rpath for build directory

* Tue Oct 07 2003 Adrian Havill <havill@redhat.com> 12:0.50.3-16
- moved spell compat script from /usr/share/aspell to /usr/bin (#105921)

* Tue Jul 01 2003 Adrian Havill <havill@redhat.com> 11:0.50.3-15
- moved ispell compat script from /usr/share/aspell to /usr/bin (#90907)

* Tue Jun 24 2003 Adrian Havill <havill@redhat.com> 10:0.50.3-14
- removed emacs/xemacs el files which are already provided

* Wed Jun 18 2003 Adrian Havill <havill@redhat.com> 9:0.50.3-13
- provide pspell-devel in addition to obsoleting it

* Tue Jun 10 2003 Adrian Havill <havill@redhat.com> 8:0.50.3-12
- obsolete old dicts designed for previous aspell

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 30 2003 Joe Orton <jorton@redhat.com> 7:0.50.3-10
- rebuild again to fix libpspell deps

* Fri May 30 2003 Joe Orton <jorton@redhat.com> 7:0.50.3-9
- remove ExcludeArch

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 7:0.50.3-8
- fix build with gcc 3.3

* Wed May 21 2003 Adrian Havill <havill@redhat.com> 0.50.3-7
- require aspell-en for upgrades

* Sun May 11 2003 Jeremy Katz <katzj@redhat.com> 6:0.50.3-6
- -devel should obsolete pspell-devel

* Tue May  6 2003 Joe Orton <jorton@redhat.com> 0.50.3-5
- include libpspell.so in devel package

* Thu May  1 2003 Adrian Havill <havill@redhat.com> 0.50.3-4
- removed .la files

* Wed Apr 16 2003 Adrian Havill <havill@redhat.com> 0.50.3-3
- Changed the header for provides, obsoletes, epoch
- fixed config prefix in dirs.h

* Wed Apr 16 2003 Adrian Havill <havill@redhat.com> 0.50.3-1
- upgrade to 0.50.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov  8 2002 Tim Powers <timp@redhat.com>
- fix broken pspell epoch dep
- create $RPM_BUILD_ROOT/usr/bin by hand
- remove /usr/doc
- fix hardcoding of /usr/lib so that we can build on x86_64

* Tue Aug 13 2002 Nalin Dahyabhai <nalin@redhat.com> 0.33.7.1-16
- require pspell and pspell-devel using the proper epoch

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 0.33.7.1-14
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.33.7.1-13
- automated rebuild

* Thu Jun 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-12
- Rebuild to make it work again... #66708

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-10
- Rebuild

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-9
- Disable evil patch

* Mon Jan 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-8
- Build on more archs (doh)

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-7
- Make it compile with new compiler (evil workaround)

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-5
- Rebuild
- Unexclude alpha

* Fri Dec 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-3
- Rebuild
- Don't build on alpha

* Mon Oct 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.33.7.1-2
- "make it work with gcc 3.1" ;)

* Tue Sep 18 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-1
- 0.33.7.1, which is a "make it work with gcc 3" release

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Thu Aug  9 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7-1
- 0.33.7 bugfix release. Requested by the author, it fixes
  coredumps in sug-mode and when not using typo-analyses.
  It also contains code cleanups so it compiles with -ansi
- should fix coredump on IA64 (#49746)

* Wed Jul 11 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add the .la files in the main package - used for dynamic loading

* Sun Jun  3 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.6.3, which includes the fix made yesterday

* Sat Jun  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make it search for directories in the correct location

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- No more workarounds at the specfile level

* Tue May 29 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Use custom ltmain.sh to work around buggy bundled libtool

* Sun May 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.6
- use standard %%configure macro - it works now.

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.33.5-2
- Rebuild with new libltdl

* Mon Apr 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.5

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use new emacs init scheme for Emacs and XEmacs

* Wed Nov 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
-  .32.6

* Sat Aug 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32.5 bugfix release (also contains improved documentation),
  obsolete old patch
- the compatibility scripts are now part of the package itself
- clean up build procedure
- remove manual.aux file from docs (#16424)

* Sun Aug 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32.1 bugfix release, obsolete old patch
- rename to 0.32.1
- add patch from author to change his email address
- add spell and ispell compatibility scripts

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Aug 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remember to obsolete ispell
- build the Canadian and British dictionaries here now,
  as part of the main package. Same package names and 
  descriptions.

* Mon Jul 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32
- remove old patches, add a patch since namespace isn't 
  polluted as much anymore (as opposed to older toolchain)

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use RPM_OPT_FLAGS, not just -O0
- dont include .la-files

* Fri Jun 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- excludearch ia64

* Fri Jun 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patch to work around compiler bug(?) wrt. inline functions
- use CFLAGS and CXXFLAGS
- set them to -O0 to work around YACB
- copy libtool files for IA64 support

* Sun Jun 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update to .31.1. My patch was upstreamed and is no longer needed.
- new patch added so DESTDIR works properly

* Fri Jun 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- (this entry includes some old ones...)
- update to .31
- added patch to make it compile with a pickier compiler
- include /usr/share/pspell

* Mon May 1 2000 Tim Powers <timp@redhat.com>
- updated to .30.1
- used build fixes from Ryan Weaver's 0.30.1-1 package on sourceforge
- updated URL, download/ftp location
- removed redundant define's at top of spec file

* Thu Jul 8 1999 Tim Powers <timp@redhat.com>
- built for Powertools 6.1
- removed serial macro definitions from spec file to make versioning
  consistant with the other packages we ship.
- changed build root path
- general spec file cleanups

* Tue Mar  2 1999 Ryan Weaver <ryanw@infohwy.com>
  [aspell-.27.2-2]
- Changes from .27.1 to .27.2 (Mar 1, 1999)
- Fixed a major bug that caused aspell to dump core when used
  without any arguments
- Fixed another major bug that caused aspell to do nothing when used
  in interactive mode.
- Added an option to exit in Aspell's interactive mode.
- Removed some old documentation files from the distribution.
- Minor changes on to the section on using Aspell with egcs.
- Minor changes to remove -Wall warnings.
