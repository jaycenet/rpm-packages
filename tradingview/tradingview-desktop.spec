%global debug_package %{nil}
%global __strip /bin/true
%global __brp_mangle_shebangs /usr/bin/true

Name:           tradingview-desktop
Version:        3.4.1
Release:        1%{?dist}
Summary:        TradingView Desktop for Linux

License:        LicenseRef-Proprietary
URL:            https://www.tradingview.com/desktop/
Source0:        https://tvd-packages.tradingview.com/ubuntu/stable/pool/multiverse/t/tradingview/jammy/tradingview-%{version}-1_amd64.deb

ExclusiveArch:  x86_64
AutoReqProv:    no

BuildRequires:  binutils, tar, xz, zstd

Requires:       gtk3, nss, libappindicator-gtk3, xdg-utils
Requires:       alsa-lib, at-spi2-core, libnotify, libXScrnSaver, libXtst
Requires:       mesa-libgbm, libxkbcommon, cups-libs

%description
TradingView Desktop is a standalone application for TradingView with improved
performance, workspace management, and native notifications.

%prep
%setup -q -c -T

%build
# Rien à compiler

%install
mkdir -p %{buildroot}
ar x %{SOURCE0}
tar --no-same-owner -xf data.tar.* -C %{buildroot}

# Retire ce qui ne concerne pas un RPM (dépôt apt, clé GPG, cron, doc Debian)
rm -rf %{buildroot}/etc/apt \
       %{buildroot}/etc/cron.daily \
       %{buildroot}%{_datadir}/doc \
       %{buildroot}%{_datadir}/keyrings

# Sandbox Electron : SUID requis
chmod 4755 %{buildroot}/opt/TradingView/chrome-sandbox

# Lien /usr/bin (relatif)
mkdir -p %{buildroot}%{_bindir}
ln -sfn ../../opt/TradingView/tradingview %{buildroot}%{_bindir}/tradingview

# Fournit un .desktop seulement si le .deb n'en contient pas
if [ ! -f %{buildroot}%{_datadir}/applications/tradingview.desktop ]; then
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/tradingview.desktop <<EOF
[Desktop Entry]
Name=TradingView
Exec=/opt/TradingView/tradingview %%U
Icon=tradingview
Type=Application
Categories=Finance;Office;
EOF
fi

%files
%defattr(-,root,root,-)
/opt/TradingView
%{_bindir}/tradingview
%{_datadir}/applications/tradingview.desktop
%{_datadir}/icons/hicolor/*/apps/tradingview.png

%changelog
* Tue Oct 27 2026 Jérémy schneider <jayce.net@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Extract the .deb with ar/tar instead of alien

* Sat Nov 08 2025 Jérémy schneider <jayce.net@gmail.com> - 2.13.0-3
- RPM build for TradingView Desktop 2.13.0
