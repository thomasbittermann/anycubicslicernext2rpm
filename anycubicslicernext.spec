%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none
%global __brp_check_rpaths %{nil}
%global __brp_mangle_shebangs %{nil}

# Bundled private libs: don't export them as Provides, don't require them from elsewhere
%global __provides_exclude_from ^%{_libdir}/.*$
%global __requires_exclude ^lib(cloud_mqtt|cloud_sdk_cpp|common_encrypt|common_log|compress|mach_mqtt|MachMQTT|mqtt_client|RequestFilter|ssdplib|Workbench|reason_code)\\.so.*$

Name:           anycubicslicernext
Version:        2.0.0.5
Release:        2
Summary:        Anycubic Slicer is an open source slicer for FDM printers
License:        AGPL-3.0-only
URL:            https://www.anycubic.com/
Source0:        %{name}-%{version}.tar.bz2
ExclusiveArch:  x86_64

Requires:       webkit2gtk4.1
Requires:       gtk3
Requires:       mesa-libGLU
Requires:       dbus-libs
Requires:       gstreamer1-plugin-libav

%description
Anycubic Slicer is an open source slicer for FDM printers.

Repackaged from the upstream Ubuntu deb.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}
cp -a usr %{buildroot}/
rm -f %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_includedir} %{buildroot}%{_libdir}/cmake

%files
%{_bindir}/AnycubicSlicerNext
%{_libdir}/lib*.so*
%{_datadir}/AnycubicSlicerNext/
%{_datadir}/applications/AnycubicSlicer.desktop

%changelog
* Thu Oct 22 2026 Thomas Bittermann <pufferbrater@cobonet.de> - 2.0.0.5-2
- added missing requires for gstreamer1-plugin-libav

* Thu Oct 22 2026 Thomas Bittermann <pufferbrater@cobonet.de> - 2.0.0.5-1
- Updated to version 2.0.0.5
- converted from AnycubicSlicerNext_linux-v2.0.0.5-20260913065625.deb

* Wed Apr 29 2026 Thomas Bittermann <pufferbrater@cobonet.de> - 1.3.9.4-1
- Updated to version 1.3.9.4
- converted from 1.3.96_20260319_224609 deb packages

* Fri Mar 27 2026 Thomas Bittermann <thomas@cobonet.de> - 1.3.96-3
- converted from 1.3.96-20260131_153250 deb packages

* Wed Feb 18 2026 Thomas Bittermann <thomas@cobonet.de> - 1.3.96-2
- converted from 1.3.96_20260218 deb packages

* Tue Jan 27 2026 Thomas Bittermann <thomas@cobonet.de> - 1.3.995-2
- converted from 1.3.995_20260127 deb packages
