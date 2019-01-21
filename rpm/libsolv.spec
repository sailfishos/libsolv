%global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(True);")

Name:       libsolv
Summary:    A new approach to package dependency solving
Version:    0.6.35
Release:    1
Group:      Development/Libraries/C and C++
License:    BSD 3-Clause
URL:        https://github.com/openSUSE/libsolv
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(rpm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  perl-devel
BuildRequires:  python-devel
BuildRequires:  swig
BuildRequires:  cmake
BuildRequires:  libxml2-devel

Patch1:  0001-Fix-repo2solv-to-work-with-Busybox-find-tool.patch

%description
A new approach to package dependency solving.

%package demo
Summary:    Applications demoing the libsolv library
Group:      System/Management
Requires:   curl
Requires:   gnupg2
Requires:   libsolv0 = %version

%description demo
Applications demoing the libsolv library.

%package -n python-solv
Summary:    Python bindings for the libsolv library
Group:      Development/Languages/Python
Requires:   libsolv0 = %version

%description -n python-solv
Python bindings for sat solver.

%package devel
Summary:    A new approach to package dependency solving
Group:      Development/Libraries/C and C++
Requires:   libsolv-tools = %version
Requires:   libsolv0 = %version
Requires:   rpm-devel

%description devel
Development files for libsolv, a new approach to package dependency solving.

%package -n perl-solv
Summary:    Perl bindings for the libsolv library
Group:      Development/Languages/Perl
Requires:   perl = %{perl_version}
Requires:   libsolv0 = %version

%description -n perl-solv
Perl bindings for sat solver.

%package -n libsolv0
Summary:    A new approach to package dependency solving
Group:      Development/Libraries/C and C++
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# libzypp 12.2.0 doesn't work with this version of libsolv (it crashes),
# so make sure we have at least 14.35.0 (the new version) installed.
Conflicts:  libzypp < 14.35.0

%description -n libsolv0
A new approach to package dependency solving.

%package tools
Summary:    A new approach to package dependency solving
Group:      Development/Libraries/C and C++
Requires:   gzip
Requires:   bzip2
Requires:   coreutils
Requires:   libsolv0 = %version
Provides:   satsolver-tools = 0.18
Obsoletes:  satsolver-tools < 0.18

%description tools
A new approach to package dependency solving.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch1 -p1

%build
%cmake .  \
    -DFEDORA=1 \
    -DENABLE_COMPS=1 \
    -DENABLE_APPDATA=1 \
    -DENABLE_COMPLEX_DEPS=1 \
    -DENABLE_RPMDB_BYRPMHEADER=1 \
    -DENABLE_RPMDB_LIBRPM=1 \
    -DENABLE_RPMPKG_LIBRPM=1 \
    -DENABLE_LZMA_COMPRESSION=1 \
    -DENABLE_BZIP2_COMPRESSION=1 \
    -DENABLE_SUSEREPO=1 -DENABLE_HELIXREPO=1 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB=%{_lib} \
    -DCMAKE_VERBOSE_MAKEFILE=TRUE \
    -DCMAKE_BUILD_TYPE=Release \
    -DENABLE_PERL=1 \
    -DENABLE_PYTHON=1 \
    -DUSE_VENDORDIRS=1 \
    -DCMAKE_SKIP_RPATH=1 \
    -DWITH_LIBXML2=1 \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

# we want to leave the .a file untouched
export NO_BRP_STRIP_DEBUG=true

%post -n libsolv0 -p /sbin/ldconfig

%postun -n libsolv0 -p /sbin/ldconfig


%files demo
%defattr(-,root,root,-)
%{_bindir}/solv

%files -n python-solv
%defattr(-,root,root,-)
%{python_sitearch}/*

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

%files -n perl-solv
%defattr(-,root,root,-)
%{perl_vendorarch}/*

%files -n libsolv0
%defattr(-,root,root,-)
%doc LICENSE*
%{_libdir}/libsolv.so.*
%{_libdir}/libsolvext.so.*

%files tools
%defattr(-,root,root,-)
%exclude %{_bindir}/helix2solv
%exclude %{_bindir}/solv
%{_bindir}/*
