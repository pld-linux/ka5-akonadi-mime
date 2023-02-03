#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.12.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		akonadi-mime
Summary:	Akonadi Mime
Name:		ka5-%{kaname}
Version:	22.12.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	8ea129c444e10a6cc2f9e077e6397348
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	ka5-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka5-kmime-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-kconfig-devel >= %{kframever}
BuildRequires:	kf5-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kio-devel >= %{kframever}
BuildRequires:	kf5-kitemmodels-devel >= %{kframever}
BuildRequires:	kf5-kxmlgui-devel >= %{kframever}
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi Mime is a library that effectively bridges the type-agnostic
API of the Akonadi client libraries and the domain-specific KMime
library. It provides jobs, models and other helpers to make working
with emails through Akonadi easier.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build install

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libKF5AkonadiMime.so.5
%attr(755,root,root) %{_libdir}/libKF5AkonadiMime.so.*.*.*
%{_datadir}/config.kcfg/specialmailcollections.kcfg
%{_datadir}/mime/packages/x-vnd.kde.contactgroup.xml
%{_libdir}/qt5/plugins/akonadi_serializer_mail.so
%{_datadir}/akonadi/plugins
%{_datadir}/qlogging-categories5/akonadi-mime.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/AkonadiMime
%{_libdir}/cmake/KF5AkonadiMime
%{_libdir}/libKF5AkonadiMime.so
%{_libdir}/qt5/mkspecs/modules/qt_AkonadiMime.pri
