# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>
pkgname=hel-builder
pkgver=1.0.0
pkgrel=1
pkgdesc="A GUI tool to generate PKGBUILD files for Arch Linux packages."
arch=('any')
url="https://github.com/helwan-linux/helwan-builder"
license=('MIT')
depends=('python' 'python-pyqt5' 'python-jsonschema')
makedepends=()
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/helwan-linux/helwan-builder/archive/refs/heads/main.tar.gz")
sha256sums=('SKIP')

package() {
  cd "${srcdir}/helwan-builder-main/hel-pkg"

  install -d "${pkgdir}/opt/${pkgname}"
  cp -r ./* "${pkgdir}/opt/${pkgname}/"

  install -d "${pkgdir}/usr/bin"
  ln -s "/opt/${pkgname}/hel_pkg_app.py" "${pkgdir}/usr/bin/${pkgname}"
  chmod +x "${pkgdir}/opt/${pkgname}/hel_pkg_app.py"

  install -d "${pkgdir}/usr/share/applications"
  cat <<EOF > "${pkgdir}/usr/share/applications/${pkgname}.desktop"
[Desktop Entry]
Name=Helwan Builder: PKGBUILD Generator
Comment=A GUI tool to generate PKGBUILD files for Arch Linux packages.
Exec=python3 /opt/hel-builder/hel_pkg_app.py
Icon=/opt/hel-builder/assets/pkg.png
Terminal=false
Type=Application
Categories=Development;Utility;
Keywords=PKGBUILD;Arch Linux;Generator;Package;Development;Utility;GUI;
StartupNotify=true
EOF
}

