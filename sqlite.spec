%define realname sqlite
%define realver %(echo %version |cut -d. -f1)0%(echo %version |cut -d. -f2)0%(echo %version |cut -d. -f3)0%(echo %version |cut -d. -f4)

%define api 3
%define major 0
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} %{api} -d

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite
Version:	3.8.7.3
Release:	1
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/2014/%{realname}-autoconf-%{realver}.tar.gz
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
%rename	sqlite3

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

%package -n	%{libname}
Summary:	C library that implements an embeddable SQL database engine
Group:		System/Libraries

%description -n	%{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}

%package -n	%{devname}
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}_ %{major} -d
%rename sqlite3-devel

%description -n	%{devname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library and its header
files.

%package tools
Summary:	Command line tools for managing the %{libname} library
Group:		Databases
Requires:	%{libname} >= %{version}-%{release}
%rename	sqlite3-tools

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
%setup -qn %{realname}-autoconf-%{realver}

%build
export CFLAGS="${CFLAGS:-%optflags} -Wall -fno-strict-aliasing -DNDEBUG=1 -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_DISABLE_DIRSYNC=1"

%configure2_5x \
	--disable-static \
	--enable-threadsafe \
	--enable-dynamic-extensions

# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

# cleanup
ln -s sqlite3 %buildroot%_bindir/sqlite

%files -n %{libname}
%{_libdir}/lib%{name}%{api}.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/sqlite*
%{_mandir}/man1/*
