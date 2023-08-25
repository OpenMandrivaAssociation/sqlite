# Mixed automake/non-automake use
%define _disable_rebuild_configure 1
%define realver %(echo %version |cut -d. -f1)%(echo %version |cut -d. -f2)0%(echo %version |cut -d. -f3)00%(echo %version |cut -d. -f4)

%define api 3
%define major 0
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} %{api} -d

%ifarch %{ix86} %{arm}
%define _disable_lto 1
%endif

# (tpg) optimize it a bit
%ifnarch riscv64
%global optflags %{optflags} -O3
%endif

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite
Version:	3.43.0
Release:	1
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%(date +%Y)/%{name}-autoconf-%{realver}.tar.gz
# (tpg) ClearLinux patches
# NOTE: NEVER add the ClearLinux patches "walmode.patch" and
# "defaultwal.patch". While those improve performance, they
# require additional permissions (write access for any user
# trying to *read* a file to the directory containing the file!)
# and therefore cause subtle breakages.
Patch4:		chunksize.patch
# (tpg) do not enable ICU support as it just bloats everything
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(zlib)
%rename	sqlite3

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

%package -n %{libname}
Summary:	C library that implements an embeddable SQL database engine
Group:		System/Libraries

%description -n %{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}

%package -n %{devname}
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%mklibname %{name}_ %{major} -d
%rename	sqlite3-devel

%description -n %{devname}
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
Requires:	%{libname} >= %{EVRD}
%rename	sqlite3-tools

%description tools
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains command line tools for managing the
%{libname} library.

%prep
%autosetup -n %{name}-autoconf-%{realver} -p1
autoreconf -fi

%build
# BIG FAT WARNING !!!
# DO NOT FIDDLE WITH COMPILE-TIME OPTIONS AS YOU MAY BREAK THINGS BADLY !!!
# (tpg) firefox needs SQLITE_ENABLE_FTS3
# Qt5 needs SQLITE_ENABLE_COLUMN_METADATA
# For information on some of the flags, see
# https://www.sqlite.org/compile.html
export CFLAGS="%{optflags} -Wall -fno-strict-aliasing -DNDEBUG=1 \
	-DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 \
	-DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -DSQLITE_ENABLE_FTS3_TOKENIZER=1 \
	-DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
	-DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
	-DSQLITE_ENABLE_FTS3=1 -DSQLITE_MAX_WORKER_THREADS=16 -DSQLITE_ENABLE_FTS4=1 \
	-DSQLITE_DEFAULT_WORKER_THREADS=4 -DSQLITE_DEFAULT_PAGE_SIZE=4096 \
	-DSQLITE_TEMP_STORE=2 -DSQLITE_MAX_DEFAULT_PAGE_SIZE=32768 \
	-DSQLITE_DEFAULT_SYNCHRONOUS=1 -DSQLITE_DEFAULT_MMAP_SIZE=67108864 \
	-DSQLITE_DEFAULT_WAL_SYNCHRONOUS=1 -DSQLITE_USE_ALLOCA=1 \
	-DSQLITE_ENABLE_MATH_FUNCTIONS -DSQLITE_ENABLE_DBSTAT_VTAB=1 -DSQLITE_ENABLE_JSON=1"

%configure \
	--disable-static \
	--disable-static-shell \
	--enable-fts4 \
	--enable-fts5 \
	--enable-json1 \
	--enable-threadsafe \
	--enable-threads-override-locks \
	--enable-load-extension

# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

# cleanup
ln -s sqlite3 %{buildroot}%{_bindir}/sqlite

%files -n %{libname}
%{_libdir}/lib%{name}%{api}.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/sqlite*
%doc %{_mandir}/man1/*
