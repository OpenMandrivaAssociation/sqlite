%define	major 0
%define libname	%mklibname %{name} %{major}

Summary:	SQLite is a C library that implements an embeddable SQL database engine
Name:		sqlite
Version:	2.8.17
Release:	%mkrel 7
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{name}-%{version}.tar.bz2
Patch0:		sqlite-2.8.14-lib64.patch
Patch1:		sqlite-64bit-fixes.patch
Patch2:		sqlite-2.8.15-arch-double-differences.patch
Patch3:		sqlite-CVE-2007-1887_1888.patch
BuildRequires:	chrpath
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl tcl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

%package -n	%{libname}
Summary:	SQLite is a C library that implements an embeddable SQL database engine
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
Requires:	%{libname} = %{version}-%{release}
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

%package -n	%{libname}-static-devel
Summary:	Static development library for the %{name} library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library.

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

%build
%define __libtoolize true
%serverbuild

export CFLAGS="${CFLAGS:-%optflags} -DNDEBUG=1"
export CXXFLAGS="${CXXFLAGS:-%optflags} -DNDEBUG=1"
export FFLAGS="${FFLAGS:-%optflags} -DNDEBUG=1"

%configure2_5x \
    --enable-utf8

%make
make doc

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -m644 sqlite.1 %{buildroot}%{_mandir}/man1/

chrpath -d %{buildroot}%{_bindir}/*

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files -n	%{libname}
%defattr(-,root,root)
%doc README
%{_libdir}/lib*.so.*

%files -n	%{libname}-devel
%defattr(-,root,root)
%doc doc/*.html doc/*.png
%{_includedir}/*.h
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files -n	%{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%files		tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
