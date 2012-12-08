%define __libtoolize true
%define	major 0
%define libname %mklibname %{name} %{major}

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite
Version:	2.8.17
Release:	15
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{name}-%{version}.tar.bz2
Patch0:		sqlite-2.8.14-lib64.patch
Patch1:		sqlite-64bit-fixes.patch
Patch2:		sqlite-2.8.15-arch-double-differences.patch
Patch3:		sqlite-CVE-2007-1887_1888.patch
Patch4:		sqlite-2.8.17-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	chrpath
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl tcl-devel

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

%package -n	%{libname}
Summary:	C library that implements an embeddable SQL database engine
Group:          System/Libraries

%description -n	%{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}

%package -n	%{libname}-devel
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	lib%{name}-devel
Provides:	%{name}-devel

%description -n	%{libname}-devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library and its header
files.

%package	tools
Summary:	Command line tools for managing the %{libname} library
Group:		Databases
Requires:	%{libname} = %{version}-%{release}

%description	tools
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains command line tools for managing the
%{libname} library.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0 -b .lib64
%patch1 -p1 -b .64bit-fixes
%patch2 -p1 -b .double-fixes
%patch3 -p0 -b .CVE-2007-1887_1888
%patch4 -p0 -b .format_not_a_string_literal_and_no_format_arguments

%build
export CFLAGS="${CFLAGS:-%optflags} -DNDEBUG=1"
export CXXFLAGS="${CXXFLAGS:-%optflags} -DNDEBUG=1"
export FFLAGS="${FFLAGS:-%optflags} -DNDEBUG=1"

%configure2_5x \
    --enable-utf8

%make
make doc

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -m644 sqlite.1 %{buildroot}%{_mandir}/man1/

chrpath -d %{buildroot}%{_bindir}/*

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%doc README
%{_libdir}/lib*.so.%{major}*

%files -n %{libname}-devel
%doc doc/*.html doc/*.png
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Mon Dec 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-15
+ Revision: 737879
- don't use the serverbuild macro here
- drop the static lib, its sub package and the libtool *.la file
- various fixes

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-14
+ Revision: 670010
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-13mdv2011.0
+ Revision: 607558
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-12mdv2010.1
+ Revision: 524121
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.8.17-11mdv2010.0
+ Revision: 427212
- rebuild

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-10mdv2009.1
+ Revision: 344738
- added P4 to fix build with -Werror=format-security
- rebuilt against new readline

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 2.8.17-9mdv2009.1
+ Revision: 311081
- rebuild for new tcl

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 2.8.17-8mdv2009.0
+ Revision: 225472
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.8.17-7mdv2008.1
+ Revision: 171124
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon May 28 2007 Andreas Hasenack <andreas@mandriva.com> 2.8.17-6mdv2008.0
+ Revision: 32113
- added security patch for CVE-2007-1887 and CVE-2007-1888
- disabled test if using tcl >= 8.5

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild


* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-5mdv2007.0
+ Revision: 74474
- Import sqlite

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.8.17-5mdv2007.0
- Rebuild

* Tue Jun 13 2006 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-3mdv2007.1
- rebuild

* Sun May 28 2006 Stefan van der Eijk <stefan@eijk.nu> 2.8.17-3mdk
- %%mkrel

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-2mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Thu Dec 22 2005 Oden Eriksson <oeriksson@mandriva.com> 2.8.17-1mdk
- 2.8.17

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.16-1mdk
- 2.8.16

* Fri Jan 28 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.8.15-5mdk
- patch2: fix test suite for differences in double precision float implementation

* Fri Jan 21 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.8.15-4mdk
- rebuild for new readline

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.15-3mdk
- revert latest "lib64 fixes"

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.15-2mdk
- lib64 fixes

* Tue Nov 09 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.8.15-1mdk
- New release 2.8.15

* Tue Oct 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.14-3mdk
- rebuild (due to missing devel package)

* Thu Sep 30 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.8.14-2mdk
- backport some 64-bit related fixes for the testsuite
- add libsqlite-static-devel, sqlite-static-devel provides

* Sat Jun 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.14-1mdk
- 2.8.14 
- fix P0
- run the tests

* Sun Jun 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.13-3mdk
- rebuilt with gcc v3.4.x

* Sun May 16 2004 Luca Berra <bluca@vodka.it> 2.8.13-2mdk 
- lib64 install fixes

* Mon May 03 2004 Luca Berra <bluca@vodka.it> 2.8.13-1mdk 
- 2.8.13
- dropped p0 (merged upstream)

