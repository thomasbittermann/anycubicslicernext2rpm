Name: anycubicslicernext
Version: 2.0.0.5
Release: 1
Summary: Anycubic Slicer is an open source slicer for FDM printers
License: see %{_datadir}/doc/anycubicslicernext/copyright
Distribution: Debian
Group: Converted/utils
Source0: %{name}-%{version}.tar.bz2

%description
Anycubic Slicer is an open source slicer for FDM printers

(Converted from a deb package by alien version 8.95.)

%define debug_package %{nil}

%prep
%setup -q

%build

%install
pwd
mv -v ./usr %{buildroot}

%files
%dir %{_datadir}/AnycubicSlicerNext/
%{_bindir}/AnycubicSlicerNext
%{_includedir}/spline/spline.h
%{_includedir}/stb_dxt/stb_dxt.h
%{_libdir}/*
%{_datadir}/AnycubicSlicerNext/resources/AnycubicSlicer.icns
%{_datadir}/AnycubicSlicerNext/resources/build-timestamp.txt
%{_datadir}/AnycubicSlicerNext/resources/build-version.txt
%{_datadir}/AnycubicSlicerNext/resources/check_access_code.txt
%{_datadir}/AnycubicSlicerNext/resources/debugTimeStamp.txt
%{_datadir}/AnycubicSlicerNext/resources/calib/filament_flow/flowrate-test-pass1.3mf
%{_datadir}/AnycubicSlicerNext/resources/calib/filament_flow/flowrate-test-pass2.3mf
%{_datadir}/AnycubicSlicerNext/resources/calib/filament_flow/Orca-LinearFlow.3mf
%{_datadir}/AnycubicSlicerNext/resources/calib/filament_flow/Orca-LinearFlow_fine.3mf
%{_datadir}/AnycubicSlicerNext/resources/calib/filament_flow/pass1.3mf
%{_datadir}/AnycubicSlicerNext/resources/calib/input_shaping/fast_tower_test.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/input_shaping/ringing_tower.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/pressure_advance/pa_pattern.3mf
%{_datadir}/AnycubicSlicerNext/resources/calib/pressure_advance/pressure_advance_test.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/pressure_advance/tower_with_seam.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/retraction/retraction_tower.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/temperature_tower/temperature_tower.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/vfa/VFA.stl
%{_datadir}/AnycubicSlicerNext/resources/calib/volumetric_speed/SpeedTestStructure.step
%{_datadir}/AnycubicSlicerNext/resources/calib/volumetric_speed/SpeedTestStructure.stp
%{_datadir}/AnycubicSlicerNext/resources/cert/printer.cer
%{_datadir}/AnycubicSlicerNext/resources/cert/slicer_base64.cer
%{_datadir}/AnycubicSlicerNext/resources/cloud/cloud_profile.ini
%{_datadir}/AnycubicSlicerNext/resources/cloud/pingying.txt
%{_datadir}/AnycubicSlicerNext/resources/dailytip/index.html
%{_datadir}/AnycubicSlicerNext/resources/data/hints.ini
%{_datadir}/AnycubicSlicerNext/resources/flush/flush_data_k4.txt
%{_datadir}/AnycubicSlicerNext/resources/flush/flush_data_kx.txt
%{_datadir}/AnycubicSlicerNext/resources/fonts/*
%{_datadir}/AnycubicSlicerNext/resources/handy_models/*
%{_datadir}/AnycubicSlicerNext/resources/i18n/placeholder.txt
%{_datadir}/AnycubicSlicerNext/resources/i18n/ca/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/cs/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/de/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/en/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/es/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/fr/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/hu/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/it/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/ja/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/ko/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/nl/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/pl/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/pt_BR/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/ru/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/sv/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/tr/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/uk/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/zh_CN/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/i18n/zh_TW/AnycubicSlicer.mo
%{_datadir}/AnycubicSlicerNext/resources/images/*
%{_datadir}/AnycubicSlicerNext/resources/info/filament_info.json
%{_datadir}/AnycubicSlicerNext/resources/info/nozzle_info.json
%{_datadir}/AnycubicSlicerNext/resources/printers/*
%{_datadir}/AnycubicSlicerNext/resources/profiles/Anycubic.json
%{_datadir}/AnycubicSlicerNext/resources/profiles/Anycubic/*
%{_datadir}/AnycubicSlicerNext/resources/shaders/110/*
%{_datadir}/AnycubicSlicerNext/resources/shaders/140/*
%{_datadir}/AnycubicSlicerNext/resources/tooltip/*
%{_datadir}/AnycubicSlicerNext/resources/tooltip/.md
%{_datadir}/AnycubicSlicerNext/resources/web/anycubic/anycubic_workbench.html
%{_datadir}/AnycubicSlicerNext/resources/web/anycubic/missing_connection.html
%{_datadir}/AnycubicSlicerNext/resources/web/anycubic/setup_connection.png
%{_datadir}/AnycubicSlicerNext/resources/web/anycubic/test.html
%{_datadir}/AnycubicSlicerNext/resources/web/anycubic/css/dark.css
%{_datadir}/AnycubicSlicerNext/resources/web/anycubic/css/home.css
%{_datadir}/AnycubicSlicerNext/resources/web/data/text.js
%{_datadir}/AnycubicSlicerNext/resources/web/flush/WipingDialog.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/1/1.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/1/1.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/1/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/11/11.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/11/11.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/11/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/11/location.png
%{_datadir}/AnycubicSlicerNext/resources/web/guide/21/21.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/21/21.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/21/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/21/test.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/22/22.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/22/22.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/22/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/22/test.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/23/23.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/23/23.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/23/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/24/24.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/24/24.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/24/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/3/3.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/3/3.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/3/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/31/31.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/31/31.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/31/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/5/5.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/5/5.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/5/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/6/6.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/6/6.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/6/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/guide/6/restart.png
%{_datadir}/AnycubicSlicerNext/resources/web/guide/css/common.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/css/dark.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/css/home.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/css/test.css
%{_datadir}/AnycubicSlicerNext/resources/web/guide/js/common.js
%{_datadir}/AnycubicSlicerNext/resources/web/guide/js/home.js
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/disconnect.html
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/homebody.html
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/leftmenu.html
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/test.html
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/css/*
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/img/*
%{_datadir}/AnycubicSlicerNext/resources/web/homepage/js/*
%{_datadir}/AnycubicSlicerNext/resources/web/image/edit.svg
%{_datadir}/AnycubicSlicerNext/resources/web/image/logo2.png
%{_datadir}/AnycubicSlicerNext/resources/web/image/logo.png
%{_datadir}/AnycubicSlicerNext/resources/web/include/globalapi.js
%{_datadir}/AnycubicSlicerNext/resources/web/include/jquery-2.1.1.min.js
%{_datadir}/AnycubicSlicerNext/resources/web/include/jquery-3.6.0.min.js
%{_datadir}/AnycubicSlicerNext/resources/web/include/json2.js
%{_datadir}/AnycubicSlicerNext/resources/web/include/swiper/*
%{_datadir}/AnycubicSlicerNext/resources/web/include/viewer/viewer.css
%{_datadir}/AnycubicSlicerNext/resources/web/include/viewer/viewer-jquery.min.js
%{_datadir}/AnycubicSlicerNext/resources/web/include/viewer/viewer.js
%{_datadir}/AnycubicSlicerNext/resources/web/include/viewer/viewer.min.css
%{_datadir}/AnycubicSlicerNext/resources/web/model/index.html
%{_datadir}/AnycubicSlicerNext/resources/web/model/model.css
%{_datadir}/AnycubicSlicerNext/resources/web/model/model.js
%{_datadir}/AnycubicSlicerNext/resources/web/model/test.js
%{_datadir}/AnycubicSlicerNext/resources/web/model/css/dark.css
%{_datadir}/AnycubicSlicerNext/resources/web/model/img/*
%{_datadir}/applications/AnycubicSlicer.desktop
%changelog
* Sun Sep 27 2026 Automated Build <automated@build.local> - 2.0.0.5-1
- Updated to version 2.0.0.5
- converted from AnycubicSlicerNext_linux-v2.0.0.5-20260913065625.deb deb packages

* Wed Apr 29 2026 Thomas Bittermann <pufferbrater@cobonet.de> - 1.3.9.4-1
- Updated to version 1.3.9.4
- converted from 1.3.96_20260319_224609 deb packages

* Fri Mar 27 2026 Thomas Bittermann <thomas@cobonet.de> - 1.3.96-3
- converted from 1.3.96-20260131_153250 deb packages

* Wed Feb 18 2026 Thomas Bittermann <thomas@cobonet.de> - 1.3.96-2
- converted from 1.3.96_20260218 deb packages

* Tue Jan 27 2026 Thomas Bittermann <thomas@cobonet.de> - 1.3.995-2
- converted from 1.3.995_20260127 deb packages

