Name:       libsolv
Summary:    A new approach to package dependency solving
Version:    0.7.20
Release:    1
License:    BSD
URL:        https://github.com/openSUSE/libsolv
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(rpm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  perl-devel
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  cmake
BuildRequires:  libxml2-devel

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# libzypp 12.2.0 doesn't work with this version of libsolv (it crashes),
# so make sure we have at least 14.35.0 (the new version) installed.
Conflicts:  libzypp < 14.35.0

%description
A new approach to package dependency solving.

%package demo
Summary:    Applications demoing the libsolv library
Requires:   curl
Requires:   gnupg2
Requires:   %{name} = %{version}-%{release}

%description demo
Applications demoing the libsolv library.

%package -n python3-solv
Summary:    Python bindings for the libsolv library
Requires:   %{name} = %{version}-%{release}

%description -n python3-solv
Python3 bindings for sat solver.

%package devel
Summary:    A new approach to package dependency solving
Requires:   %{name} = %{version}-%{release}
Requires:   rpm-devel

%description devel
Development files for libsolv, a new approach to package dependency solving.

%package -n perl-solv
Summary:    Perl bindings for the libsolv library
Requires:   perl = %{perl_version}
Requires:   %{name} = %{version}-%{release}

%description -n perl-solv
Perl bindings for sat solver.

%package tools
Summary:    A new approach to package dependency solving
Requires:   gzip
Requires:   bzip2
Requires:   coreutils
Requires:   %{name} = %{version}-%{release}

%description tools
A new approach to package dependency solving.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%cmake .  \
    -DFEDORA=1 \
    -DENABLE_COMPS=1 \
    -DENABLE_APPDATA=1 \
    -DENABLE_COMPLEX_DEPS=1 \
    -DENABLE_RPMDB=1 \
    -DENABLE_RPMDB_BYRPMHEADER=1 \
    -DENABLE_RPMDB_LIBRPM=1 \
    -DENABLE_RPMPKG_LIBRPM=1 \
    -DENABLE_RPMMD=1 \
    -DENABLE_LZMA_COMPRESSION=1 \
    -DENABLE_BZIP2_COMPRESSION=1 \
    -DENABLE_SUSEREPO=1 -DENABLE_HELIXREPO=1 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB=%{_lib} \
    -DCMAKE_VERBOSE_MAKEFILE=TRUE \
    -DCMAKE_BUILD_TYPE=Release \
    -DENABLE_PERL=1 \
    -DENABLE_PYTHON3=1 \
    -DUSE_VENDORDIRS=1 \
    -DCMAKE_SKIP_RPATH=1 \
    -DWITH_LIBXML2=1 \

%make_build

%install
%make_install

# we want to leave the .a file untouched
export NO_BRP_STRIP_DEBUG=true

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%license LICENSE*
%{_libdir}/libsolv.so.*
%{_libdir}/libsolvext.so.*

%files tools
%defattr(-,root,root,-)
%exclude %{_bindir}/helix2solv
%exclude %{_bindir}/solv
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libsolv.so
%{_libdir}/libsolvext.so
%{_includedir}/solv
%{_bindir}/helix2solv
%{_datadir}/cmake/Modules/*
%{_libdir}/pkgconfig/libsolv.pc
%{_libdir}/pkgconfig/libsolvext.pc
%{_datadir}/man/man?/*.?.gz

%files demo
%defattr(-,root,root,-)
%{_bindir}/solv

%files -n perl-solv
%defattr(-,root,root,-)
%{perl_vendorarch}/*

%files -n python3-solv
%defattr(-,root,root,-)
%{python3_sitearch}/*solv*
%{python3_sitearch}/__pycache__/solv.*
