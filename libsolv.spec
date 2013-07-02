# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.26
# 

Name:       libsolv

# >> macros
%global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(True);")
# << macros

Summary:    A new approach to package dependency solving
Version:    0.1.0
Release:    1
Group:      Development/Libraries/C and C++
License:    BSD 3-Clause
URL:        git://gitorious.org/opensuse/libsolv.git
Source0:    libsolv-%{version}.tar.bz2
Source100:  libsolv.yaml
Patch0:     fix-armv7tnhl-typo.patch
BuildRequires:  pkgconfig(rpm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  db4-devel
BuildRequires:  expat-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  perl-devel
BuildRequires:  python-devel
BuildRequires:  swig
BuildRequires:  cmake

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
%setup -q -n %{name}-%{version}

# fix-armv7tnhl-typo.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
# << build pre

%cmake .  \
    -DFEDORA=1 \
    -DENABLE_HELIXREPO=1 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB=%{_lib} \
    -DCMAKE_VERBOSE_MAKEFILE=TRUE \
    -DCMAKE_BUILD_TYPE=Release \
    -DENABLE_PERL=1 \
    -DENABLE_PYTHON=1 \
    -DUSE_VENDORDIRS=1 \
    -DCMAKE_SKIP_RPATH=1

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
# we want to leave the .a file untouched
export NO_BRP_STRIP_DEBUG=true
# << install post

%post -n libsolv0 -p /sbin/ldconfig

%postun -n libsolv0 -p /sbin/ldconfig


%files demo
%defattr(-,root,root,-)
# >> files demo
%{_bindir}/solv
# << files demo

%files -n python-solv
%defattr(-,root,root,-)
# >> files python-solv
%{python_sitearch}/*
# << files python-solv

%files devel
%defattr(-,root,root,-)
# >> files devel
%{_libdir}/libsolv.so
%{_libdir}/libsolvext.so
%{_includedir}/solv
%{_bindir}/helix2solv
%{_datadir}/cmake/Modules/*
# << files devel

%files -n perl-solv
%defattr(-,root,root,-)
# >> files perl-solv
%{perl_vendorarch}/*
# << files perl-solv

%files -n libsolv0
%defattr(-,root,root,-)
# >> files libsolv0
%doc LICENSE*
%{_libdir}/libsolv.so.*
%{_libdir}/libsolvext.so.*
# << files libsolv0

%files tools
%defattr(-,root,root,-)
# >> files tools
%exclude %{_bindir}/helix2solv
%exclude %{_bindir}/solv
%{_bindir}/*
# << files tools
