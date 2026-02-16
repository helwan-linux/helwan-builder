# -*- coding: utf-8 -*-

import sys
import os
import re
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QMessageBox, QFileDialog,
	QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
	QLineEdit, QTextEdit, QPushButton, QLabel, QTabWidget, QComboBox,
	QAction, QMenuBar
)

from PyQt5.QtGui import QIcon
# استيراد النوافذ الفرعية
from about_dialog import AboutDialog
from help_dialog import HelpDialog

class HelPkgApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Hel-Builder: Global AI Package Architect')
		self.setGeometry(100, 100, 1100, 850)
		
		self.set_app_icon()
		self.init_ui()
		self.create_menu_bar()
		
	def set_app_icon(self):
		"""تحديد الأيقونة مع دعم المسار المحلي ومسار النظام"""
		icon_path = "assets/pkg.png" # المسار المحلي أثناء التطوير
		system_path = "/usr/share/pixmaps/hel-pkg.png" # مسار النظام بعد التثبيت
		
		if os.path.exists(icon_path):
			self.setWindowIcon(QIcon(icon_path))
		elif os.path.exists(system_path):
			self.setWindowIcon(QIcon(system_path))

	def create_menu_bar(self):
		"""إنشاء شريط القوائم العلوي"""
		menubar = self.menuBar()
		
		# قائمة Help
		help_menu = menubar.addMenu('&Help')
		
		help_action = QAction('📚 Usage Guide', self)
		help_action.triggered.connect(self.show_help)
		help_menu.addAction(help_action)
		
		about_action = QAction('ℹ️ About Hel-Builder', self)
		about_action.triggered.connect(self.show_about)
		help_menu.addAction(about_action)

	def show_help(self):
		dialog = HelpDialog(self)
		dialog.exec_()

	def show_about(self):
		dialog = AboutDialog(self)
		dialog.exec_()

	def init_ui(self):
		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		main_layout = QVBoxLayout(central_widget)

		# Header - Deep Analysis Engine
		self.btn_scan = QPushButton("🚀 DEEP ANALYZE LOCAL SOURCE & DETECT GIT")
		self.btn_scan.setStyleSheet("""
			QPushButton {
				background-color: #2c3e50; color: white; font-weight: bold; 
				padding: 20px; border-radius: 10px; font-size: 16px;
				border: 2px solid #34495e;
			}
			QPushButton:hover { background-color: #34495e; border-color: #3498db; }
		""")
		self.btn_scan.clicked.connect(self.run_deep_analysis)
		main_layout.addWidget(self.btn_scan)

		self.tab_widget = QTabWidget()
		main_layout.addWidget(self.tab_widget)

		# Tab 1: Configuration & Intelligence
		config_tab = QWidget()
		self.tab_widget.addTab(config_tab, "Project Intelligence")
		form = QFormLayout(config_tab)
		form.setContentsMargins(20, 20, 20, 20)
		form.setSpacing(15)

		self.le_source_git = QLineEdit()
		self.le_source_git.setPlaceholderText("Remote Git URL (GitHub/GitLab/Codeberg)")
		
		self.le_pkgname = QLineEdit()
		self.le_pkgver = QLineEdit("1.0.0")
		self.le_desc = QLineEdit("Application for Helwan Linux")
		self.le_depends = QLineEdit()
		
		self.cb_lang = QComboBox()
		self.cb_lang.addItems(["Auto-Detect", "Python", "Node.js (Electron)", "C++/CMake", "Rust (Cargo)", "Go", "Shell Script"])

		form.addRow(QLabel("<b>Git Source URL:</b>"), self.le_source_git)
		form.addRow(QLabel("<b>Package Name:</b>"), self.le_pkgname)
		form.addRow(QLabel("<b>Version:</b>"), self.le_pkgver)
		form.addRow(QLabel("<b>Detected Language:</b>"), self.cb_lang)
		form.addRow(QLabel("<b>Full Dependencies (Deep):</b>"), self.le_depends)
		form.addRow(QLabel("<b>Description:</b>"), self.le_desc)

		# Tab 2: Professional PKGBUILD Output
		output_tab = QWidget()
		output_layout = QVBoxLayout(output_tab)
		self.te_output = QTextEdit()
		self.te_output.setStyleSheet("font-family: 'Monospace'; background-color: #1e1e1e; color: #d4d4d4; padding: 15px;")
		output_layout.addWidget(self.te_output)
		self.tab_widget.addTab(output_tab, "Final PKGBUILD")

		# Bottom Actions
		footer_layout = QHBoxLayout()
		self.btn_gen = QPushButton("🔨 GENERATE PKGBUILD")
		self.btn_gen.setStyleSheet("background-color: #27ae60; color: white; padding: 15px; font-weight: bold; border-radius: 5px;")
		self.btn_gen.clicked.connect(self.generate_final_pkgbuild)
		
		self.btn_save = QPushButton("💾 SAVE TO FILE")
		self.btn_save.setStyleSheet("background-color: #2980b9; color: white; padding: 15px; font-weight: bold; border-radius: 5px;")
		self.btn_save.clicked.connect(self.save_pkgbuild)
		
		footer_layout.addWidget(self.btn_gen)
		footer_layout.addWidget(self.btn_save)
		main_layout.addLayout(footer_layout)

	def run_deep_analysis(self):
		path = QFileDialog.getExistingDirectory(self, "Select Local Project Folder")
		if not path: return

		raw_name = os.path.basename(path).lower()
		clean_name = raw_name.replace("-main", "").replace("-master", "")
		self.le_pkgname.setText(clean_name)

		git_config = os.path.join(path, ".git/config")
		if os.path.exists(git_config):
			try:
				with open(git_config, 'r') as f:
					content = f.read()
					match = re.search(r"url\s*=\s*(.+)", content)
					if match: self.le_source_git.setText(match.group(1).strip())
			except: pass

		lang_points = {"Python": 0, "Node.js (Electron)": 0, "C++/CMake": 0, "Rust (Cargo)": 0, "Go": 0}
		all_deps = set()

		for root, _, files in os.walk(path):
			for file in files:
				f_path = os.path.join(root, file)
				if file == "CMakeLists.txt": lang_points["C++/CMake"] += 20
				if file == "Cargo.toml": lang_points["Rust (Cargo)"] += 20
				if file == "package.json": lang_points["Node.js (Electron)"] += 20
				if file == "go.mod": lang_points["Go"] += 20
				
				try:
					with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
						content = f.read()
						if file.endswith(".py") or "import " in content:
							lang_points["Python"] += 1
							found = re.findall(r"^(?:import|from)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)
							for d in found: all_deps.add(f"python-{d.lower()}")
						elif "electron" in content.lower():
							lang_points["Node.js (Electron)"] += 5
							all_deps.add("electron")
				except: pass

		winner = max(lang_points, key=lang_points.get) if any(lang_points.values()) else "Shell Script"
		self.cb_lang.setCurrentText(winner)
		self.le_depends.setText(", ".join([f"'{d}'" for d in sorted(all_deps)]))
		QMessageBox.information(self, "Analysis Complete", f"Identified as {winner} project.")

	def generate_final_pkgbuild(self):
		name = self.le_pkgname.text()
		lang = self.cb_lang.currentText()
		git_url = self.le_source_git.text().strip()
		
		dir_nav = """
  cd "$srcdir"
  local _dir=$(find . -maxdepth 1 -type d ! -name "." ! -name ".." | head -n 1)
  if [ -n "$_dir" ]; then cd "$_dir"; fi"""

		build_sections = ""
		if lang == "Python":
			build_sections = f"package() {{{dir_nav}\n  if [ -f \"setup.py\" ]; then\n    python setup.py install --root=\"$pkgdir/\" --optimize=1\n  else\n    install -d \"$pkgdir/usr/bin\"\n    for f in *.py; do\n      install -m755 \"$f\" \"$pkgdir/usr/bin/${{f%.py}}\"\n    done\n  fi\n}}"
		elif "Node.js" in lang:
			build_sections = f"package() {{{dir_nav}\n  install -d \"$pkgdir/opt/{name}\"\n  cp -rv * \"$pkgdir/opt/{name}/\"\n  install -d \"$pkgdir/usr/bin\"\n  echo -e \"#!/bin/bash\\nelectron /opt/{name}\" > \"$pkgdir/usr/bin/{name}\"\n  chmod +x \"$pkgdir/usr/bin/{name}\"\n}}"
		elif lang == "C++/CMake":
			build_sections = f"build() {{{dir_nav}\n  cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/usr\n  cmake --build build\n}}\n\npackage() {{\n  cd \"$srcdir\"/$(find . -maxdepth 1 -type d ! -name \".\" | head -n 1)\n  DESTDIR=\"$pkgdir\" cmake --install build\n}}"
		else:
			build_sections = f"package() {{{dir_nav}\n  install -d \"$pkgdir/usr/bin\"\n  [ -f *.sh ] && install -m755 *.sh \"$pkgdir/usr/bin/{name}\"\n}}"

		final_pkg = f"""# Generated by Hel-Builder Professional
pkgname={name}
pkgver={self.le_pkgver.text()}
pkgrel=1
pkgdesc="{self.le_desc.text()}"
arch=('any')
depends=({self.le_depends.text()})
source=('git+{git_url}')
sha256sums=('SKIP')

{build_sections}
"""
		self.te_output.setPlainText(final_pkg)
		self.tab_widget.setCurrentIndex(1)

	def save_pkgbuild(self):
		path, _ = QFileDialog.getSaveFileName(self, "Save PKGBUILD", "PKGBUILD")
		if path:
			with open(path, 'w', encoding='utf-8') as f:
				f.write(self.te_output.toPlainText())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = HelPkgApp()
	window.show()
	sys.exit(app.exec_())
