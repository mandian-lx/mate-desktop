%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	api_version	2
%define api		2.0
%define major		17
%define libname	%mklibname %{name} %{api_version} %{major}
%define devname	%mklibname -d %{name} %{api_version}
%define girname %mklibname %{name}-gir  %{api}

Summary:	Package containing code shared among mate-panel, mate-session-manager etc
Name:		mate-desktop
Version:	1.18.0
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Url:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	ldetect-lst
BuildRequires:	mate-common
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	yelp-tools

Requires:	ldetect-lst
Requires:	mate-control-center
Requires:	mate-notification-daemon
Requires:	mate-panel
Requires:	xdg-user-dirs-gtk

Suggests:	mate-user-guide
Suggests:       yelp

%description
This package contains some data files and other shared components of the
GNOME user environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n %{libname}
This package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop.

%package -n %{devname}
Summary:	Development libraries, include files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development libraries, include files for internal library %{name}.

%package -n %{girname}
Summary: GObject introspection interface library for %{name}
Group: System/Libraries
Requires: %{libname} = %{EVRD}

%description -n %{girname}
GObject introspection interface library for %{name}.

%prep
%setup -q

%build
#NOCONFIGURE=yes ./autogen.sh
%configure \
	--with-pnp-ids-path=%{_datadir}/misc/pnp.ids \
	--enable-gtk-doc \
	%{nil}
%make 

%install
%makeinstall_std 

# locales
%find_lang %{name}-%{api} --with-gnome --all-name

%files -f %{name}-%{api}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/mate-about
%{_bindir}/mate-color-select
%{_datadir}/applications/mate-about.desktop
%{_datadir}/applications/mate-color-select.desktop
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%dir %{_datadir}/mate-about
%{_datadir}/mate-about/mate-version.xml
%{_iconsdir}/*/*/*/mate*
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/libmate-desktop-%{api_version}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MateDesktop-%{api}.typelib

%files -n %{devname}
%doc COPYING COPYING-DOCS
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/MateDesktop-%{api}.gir

