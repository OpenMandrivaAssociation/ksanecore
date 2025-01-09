#define git 20240217
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

%define major 5
%define oldlibname %mklibname KF5SaneCore 5
%define lib5name %mklibname KF5SaneCore
%define dev5name %mklibname KF5SaneCore -d
%define libname %mklibname KSaneCore6
%define devname %mklibname KSaneCore6 -d
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

%bcond_without qt5

Summary:	A library for dealing with scanners
Name:		ksanecore
Version:	24.12.1
Release:	%{?git:0.%{git}.}1
Group:		System/Libraries
License:	GPLv2
Url:		https://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/libraries/ksanecore/-/archive/%{gitbranch}/ksanecore-%{gitbranchd}.tar.bz2#/ksanecore-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/release-service/%{version}/src/%{name}-%{version}.tar.xz
%endif
%if %{with qt5}
# Qt 5 support was dropped in 24.12.0
Source1:	http://download.kde.org/%{stable}/release-service/24.08.3/src/%{name}-24.08.3.tar.xz
%endif
BuildRequires:	sane-devel
BuildRequires:	cmake(ECM)
%if %{with qt5}
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5Wallet)
BuildRequires:	cmake(KF5WidgetsAddons)
BuildRequires:	cmake(KF5TextWidgets)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Test)
%endif
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6Wallet)
BuildRequires:  cmake(KF6WidgetsAddons)
BuildRequires:  cmake(KF6TextWidgets)
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Test)

%description
LibKSane is a KDE interface for SANE library to control flat scanner.

%files -f ksanecore.lang

#------------------------------------------------

%package -n %{libname}
Summary:	A library for dealing with scanners for Qt 6.x
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{libname}
LibKSane is a KDE interface for SANE library to control flat scanners.

%files -n %{libname} -f ksanecore.lang
%{_libdir}/libKSaneCore6.so.1*
%{_libdir}/libKSaneCore6.so.%(echo %{version} |cut -d. -f1)*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Devel stuff for %{name}
Group:		Development/KDE and Qt
Requires:	sane-devel
Requires:	%{libname} = %{EVRD}

%description  -n %{devname}
This package contains header files needed if you wish to build applications
based on %{name}.

%files  -n %{devname}
%{_includedir}/KSaneCore6
%{_libdir}/libKSaneCore6.so
%{_libdir}/cmake/KSaneCore6

#------------------------------------------------

%package -n %{lib5name}
Summary:	A library for dealing with scanners
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Version:	24.08.3
%rename %{oldlibname}

%description -n %{lib5name}
LibKSane is a KDE interface for SANE library to control flat scanners.

%files -n %{lib5name}
%{_libdir}/libKSaneCore.so.1*
%{_libdir}/libKSaneCore.so.%(echo %{version} |cut -d. -f1)*

#-----------------------------------------------------------------------------

%package -n %{dev5name}
Summary:	Devel stuff for %{name}
Group:		Development/KDE and Qt
Requires:	sane-devel
Requires:	%{lib5name} = %{EVRD}
Version:	24.08.3

%description  -n %{dev5name}
This package contains header files needed if you wish to build applications
based on %{name}.

%files  -n %{dev5name}
%{_includedir}/KSaneCore
%{_libdir}/libKSaneCore.so
%{_libdir}/cmake/KSaneCore

#----------------------------------------------------------------------

%package fake
# Just to reset version -- drop once we get rid of P5
Version:	24.12.1
Summary:	Fake package that doesn't exist

%description fake

%prep
%autosetup -p1 -n %{name}-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
        -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
        -DQT_MAJOR_VERSION=6 \
        -G Ninja

%if %{with qt5}
cd ..
tar xf %{S:1}
export CMAKE_BUILD_DIR=build-qt5
%cmake \
        -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
        -DQT_MAJOR_VERSION=5 \
        -G Ninja \
	../ksanecore-24.08.3
%endif

%build
%ninja_build -C build
%if %{with qt5}
%ninja_build -C build-qt5
%endif

%install
%if %{with qt5}
%ninja_install -C build-qt5
%endif
%ninja_install -C build
%find_lang ksanecore
