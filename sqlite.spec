# Mixed automake/non-automake use
%define _disable_rebuild_configure 1
%define realver %(echo %version |cut -d. -f1)%(echo %version |cut -d. -f2)0%(echo %version |cut -d. -f3)00%(echo %version |cut -d. -f4)

%define api 3
%define major 0
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} %{api} -d

%define _disable_lto 1


# (tpg) optimize it a bit
%if 0
#global optflags %{optflags} -O3 --rtlib=compiler-rt
%endif

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite
Version:	3.31.1
Release:	2
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%(date +%Y)/%{name}-autoconf-%{realver}.tar.gz
# (tpg) ClearLinux patches
%if 0
Patch1:		flags.patch
Patch2:		defaults.patch
Patch3:		walmode.patch
Patch4:		chunksize.patch
Patch5:		defaultwal.patch
%endif
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
%if 0
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(icu-uc)
%endif
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
%rename sqlite3-devel

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
#export CFLAGS="${CFLAGS:-%optflags} -Wall -fno-strict-aliasing -DNDEBUG=1 -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -DSQLITE_ENABLE_FTS3_TOKENIZER -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 -DSQLITE_ENABLE_ICU=0 -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -DSQLITE_ENABLE_JSON1=1 "
#export CFLAGS="${CFLAGS:-%optflags} -Wall -fno-strict-aliasing -DNDEBUG=0 -DSQLITE_ENABLE_API_ARMOR -DSQLITE_ENABLE_COLUMN_METADATA -DSQLITE_ENABLE_DBSTAT_VTAB -DSQLITE_ENABLE_HIDDEN_COLUMNS -DSQLITE_ENABLE_FTS3 -DSQLITE_ENABLE_FTS4 -DSQLITE_ENABLE_FTS5 -DSQLITE_ENABLE_JSON1 -DSQLITE_ENABLE_RBU -DSQLITE_ENABLE_RTREE -DSQLITE_ENABLE_UPDATE_DELETE_LIMIT -DSQLITE_SOUNDEX -DSQLITE_ENABLE_UNLOCK_NOTIFY -DSQLITE_SECURE_DELETE"
export CPPFLAGS="${CPPFLAGS:-%optflags} -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY -DSQLITE_ENABLE_DBSTAT_VTAB=1 -DSQLITE_ENABLE_FTS3_TOKENIZER=1 -DSQLITE_SECURE_DELETE -DSQLITE_MAX_VARIABLE_NUMBER=250000 -DSQLITE_MAX_EXPR_DEPTH=10000"
%configure \
	--disable-static \
	--disable-static-shell \
	--disable-amalgamation \
	--enable-fts3 \
	--enable-fts4 \
	--enable-fts5 \
	--enable-json1 \
	--enable-rtree

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
%{_mandir}/man1/*
