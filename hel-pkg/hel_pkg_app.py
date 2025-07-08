# -*- coding: utf-8 -*-

import sys
import os
import re
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog,
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QTextEdit, QPushButton, QLabel, QTabWidget, QScrollArea, QInputDialog,
    QDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir, QStandardPaths # استيراد QStandardPaths

# استيراد النوافذ الجديدة
from about_dialog import AboutDialog
from help_dialog import HelpDialog

# --- كلاس نافذة الإعدادات ---
class SettingsDialog(QDialog):
    def __init__(self, parent=None, initial_settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 150) # حجم النافذة

        self.settings = initial_settings if initial_settings else {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # حقل مسار مجلد القوالب
        self.templates_dir_label = QLabel("Templates Directory:")
        self.templates_dir_edit = QLineEdit(self.settings.get("templates_dir", ""))
        self.templates_dir_btn = QPushButton("Browse...")
        self.templates_dir_btn.clicked.connect(self._browse_templates_dir)

        templates_dir_h_layout = QHBoxLayout()
        templates_dir_h_layout.addWidget(self.templates_dir_edit)
        templates_dir_h_layout.addWidget(self.templates_dir_btn)
        form_layout.addRow(self.templates_dir_label, templates_dir_h_layout)

        layout.addLayout(form_layout)

        # أزرار الحفظ والإلغاء
        save_cancel_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        save_cancel_layout.addWidget(self.save_btn)
        save_cancel_layout.addWidget(self.cancel_btn)
        layout.addLayout(save_cancel_layout)

        self.setLayout(layout)

    def _browse_templates_dir(self):
        initial_dir = self.templates_dir_edit.text() if self.templates_dir_edit.text() else QDir.homePath()
        directory = QFileDialog.getExistingDirectory(self, "Select Templates Directory", initial_dir)
        if directory:
            self.templates_dir_edit.setText(directory)

    def get_settings(self):
        return {
            "templates_dir": self.templates_dir_edit.text()
        }

# --- نهاية كلاس SettingsDialog ---


class HelPkgApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('hel-pkg: PKGBUILD Generator')
        self.setGeometry(100, 100, 800, 650)

        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'pkg.png') 
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Warning: Icon file not found at {icon_path}")

        self.settings = self.load_settings()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        # --- تخطيط جديد لأزرار About و Help في الأعلى ---
        top_buttons_layout = QHBoxLayout()
        self.btn_about = QPushButton("About")
        self.btn_help = QPushButton("Help")
        
        top_buttons_layout.addStretch(1) # لدفع الأزرار لليمين
        top_buttons_layout.addWidget(self.btn_about)
        top_buttons_layout.addWidget(self.btn_help)
        top_buttons_layout.addStretch(1) # لدفع الأزرار لليسار

        main_layout.addLayout(top_buttons_layout)
        # --- نهاية تخطيط أزرار About و Help ---

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # --------------------- Tab 1: Package Data (بيانات الحزمة) ---------------------
        package_data_tab = QWidget()
        self.tab_widget.addTab(package_data_tab, "Package Data")

        scroll_area = QScrollArea(package_data_tab)
        scroll_area.setWidgetResizable(True)
        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        package_form_layout = QFormLayout(scroll_content_widget)
        package_form_layout.setContentsMargins(10, 10, 10, 10)
        
        # --------------------- حقول إدخال بيانات PKGBUILD ---------------------
        self.le_pkgname = QLineEdit()
        package_form_layout.addRow(QLabel("Package Name:"), self.le_pkgname)

        self.le_pkgver = QLineEdit()
        package_form_layout.addRow(QLabel("Package Version:"), self.le_pkgver)

        self.le_pkgrel = QLineEdit()
        self.le_pkgrel.setText("1")
        package_form_layout.addRow(QLabel("Package Release:"), self.le_pkgrel)

        self.le_pkgdesc = QLineEdit()
        package_form_layout.addRow(QLabel("Description:"), self.le_pkgdesc)

        self.le_arch = QLineEdit()
        self.le_arch.setText("'any'")
        package_form_layout.addRow(QLabel("Architecture (e.g., 'any', 'x86_64'):"), self.le_arch)

        self.le_url = QLineEdit()
        package_form_layout.addRow(QLabel("URL:"), self.le_url)

        self.le_license = QLineEdit()
        package_form_layout.addRow(QLabel("License:"), self.le_license)

        self.le_depends = QLineEdit()
        self.le_depends.setPlaceholderText("comma-separated, e.g., 'bash', 'python'")
        package_form_layout.addRow(QLabel("Dependencies:"), self.le_depends)

        self.le_makepends = QLineEdit()
        self.le_makepends.setPlaceholderText("comma-separated, e.g., 'gcc', 'make'")
        package_form_layout.addRow(QLabel("Make Dependencies:"), self.le_makepends)

        self.te_source = QTextEdit()
        self.te_source.setPlaceholderText("Each source file on a new line. URLs are fine.")
        self.te_source.setFixedHeight(80)
        package_form_layout.addRow(QLabel("Source Files:"), self.te_source)

        self.te_md5sums = QTextEdit()
        self.te_md5sums.setPlaceholderText("Each MD5 sum on a new line, or leave empty for 'SKIP'.")
        self.te_md5sums.setFixedHeight(80)
        package_form_layout.addRow(QLabel("MD5 Sums:"), self.te_md5sums)

        package_data_tab_layout = QVBoxLayout(package_data_tab)
        package_data_tab_layout.addWidget(scroll_area)

        # --------------------- Tab 2: PKGBUILD Output (مخرج PKGBUILD) ---------------------
        pkgbuild_output_tab = QWidget()
        self.tab_widget.addTab(pkgbuild_output_tab, "PKGBUILD Output")
        
        output_layout = QVBoxLayout(pkgbuild_output_tab)
        self.te_pkgbuild_output = QTextEdit()
        self.te_pkgbuild_output.setReadOnly(False)
        output_layout.addWidget(self.te_pkgbuild_output)

        # --------------------- أزرار التحكم (في الأسفل) ---------------------
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        self.btn_create_pkgbuild = QPushButton("Generate PKGBUILD")
        buttons_layout.addWidget(self.btn_create_pkgbuild)

        self.btn_load_pkgbuild = QPushButton("Load PKGBUILD")
        buttons_layout.addWidget(self.btn_load_pkgbuild)

        self.btn_save_pkgbuild = QPushButton("Save PKGBUILD")
        buttons_layout.addWidget(self.btn_save_pkgbuild)
        
        self.btn_generate_srcinfo = QPushButton("Generate .SRCINFO")
        buttons_layout.addWidget(self.btn_generate_srcinfo)

        self.btn_save_template = QPushButton("Save Template")
        buttons_layout.addWidget(self.btn_save_template)

        self.btn_load_template = QPushButton("Load Template")
        buttons_layout.addWidget(self.btn_load_template)

        self.btn_settings = QPushButton("Settings")
        buttons_layout.addWidget(self.btn_settings)
        
        # --------------------- ربط الأزرار بالوظائف ---------------------
        self.btn_create_pkgbuild.clicked.connect(self.create_pkgbuild)
        self.btn_load_pkgbuild.clicked.connect(self.load_pkgbuild)
        self.btn_save_pkgbuild.clicked.connect(self.save_pkgbuild)
        self.btn_generate_srcinfo.clicked.connect(self.generate_srcinfo)
        self.btn_save_template.clicked.connect(self.save_template)
        self.btn_load_template.clicked.connect(self.load_template)
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_about.clicked.connect(self.show_about_dialog)
        self.btn_help.clicked.connect(self.show_help_dialog)

    # --- دوال الإعدادات (تم التعديل هنا) ---
    def _get_settings_file_path(self):
        """
        تحدد مسار ملف الإعدادات (pkgsettings.json) في مجلد بيانات التطبيق الخاص بالمستخدم.
        """
        # الحصول على مسار مجلد بيانات التطبيق (مثل ~/.config على Linux)
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        
        # التأكد من وجود المجلد، وإنشائه إذا لم يكن موجودًا
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        # تحديد اسم الملف الجديد
        settings_file_name = "pkgsettings.json"
        return os.path.join(config_dir, settings_file_name)

    def load_settings(self):
        """تحمل الإعدادات من ملف JSON."""
        settings_path = self._get_settings_file_path()
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Settings Error", "Settings file is corrupted. Loading default settings.")
                return {}
            except Exception as e:
                QMessageBox.critical(self, "Settings Error", f"Failed to load settings: {e}. Loading default settings.")
                return {}
        return {}

    def save_settings(self, settings_data):
        """تحفظ الإعدادات في ملف JSON."""
        settings_path = self._get_settings_file_path()
        # التأكد من وجود المجلد قبل الحفظ
        settings_dir = os.path.dirname(settings_path)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
            
        try:
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Settings Error", f"Failed to save settings: {e}")

    def open_settings(self):
        dialog = SettingsDialog(self, initial_settings=self.settings)
        if dialog.exec_() == QDialog.Accepted:
            new_settings = dialog.get_settings()
            self.settings.update(new_settings)
            self.save_settings(self.settings)

            QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully.")

    # --- دوال About و Help الجديدة (تستدعي الكلاسات الجديدة) ---
    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def show_help_dialog(self):
        dialog = HelpDialog(self)
        dialog.exec_()

    # --- باقي دوال التطبيق كما هي ---
    def _extract_pkgbuild_array(self, line):
        match = re.search(r'\((.*?)\)', line)
        if match:
            items = [item.strip(" '\"") for item in match.group(1).split() if item.strip()]
            return items
        return []

    def _extract_pkgbuild_string(self, line):
        match = re.search(r'=(.*?)$', line)
        if match:
            value = match.group(1).strip()
            if value.startswith(('"', "'")) and value.endswith(('"', "'")):
                return value[1:-1]
            return value
        return ""

    def _validate_inputs(self):
        pkg_name = self.le_pkgname.text().strip()
        pkg_version = self.le_pkgver.text().strip()
        pkg_release = self.le_pkgrel.text().strip()
        pkg_url = self.le_url.text().strip()

        if not pkg_name:
            QMessageBox.warning(self, "Validation Error", "Package Name cannot be empty.")
            self.tab_widget.setCurrentIndex(0)
            self.le_pkgname.setFocus()
            return False

        if not pkg_version:
            QMessageBox.warning(self, "Validation Error", "Package Version cannot be empty.")
            self.tab_widget.setCurrentIndex(0)
            self.le_pkgver.setFocus()
            return False
        
        if not pkg_release.isdigit():
            QMessageBox.warning(self, "Validation Error", "Package Release must be a number.")
            self.tab_widget.setCurrentIndex(0)
            self.le_pkgrel.setFocus()
            return False

        if pkg_url and not re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', pkg_url):
            QMessageBox.warning(self, "Validation Error", "Invalid URL format. Please enter a valid URL (e.g., https://example.com).")
            self.tab_widget.setCurrentIndex(0)
            self.le_url.setFocus()
            return False

        return True

    def create_pkgbuild(self):
        if not self._validate_inputs():
            return

        pkg_name = self.le_pkgname.text().strip()
        pkg_version = self.le_pkgver.text().strip()
        pkg_release = self.le_pkgrel.text().strip()
        pkg_description = self.le_pkgdesc.text().strip()
        architecture = self.le_arch.text().strip() or "'any'"
        pkg_url = self.le_url.text().strip()
        license_type = self.le_license.text().strip()
        
        dependencies_input = self.le_depends.text().strip()
        make_dependencies_input = self.le_makepends.text().strip()
        source_files_input = self.te_source.toPlainText().strip()
        md5_sums_input = self.te_md5sums.toPlainText().strip()

        pkgbuild_content = f"""# Maintainer: Your Name <your@email.com>
pkgname={pkg_name}
pkgver={pkg_version}
pkgrel={pkg_release}
pkgdesc="{pkg_description}"
arch=({architecture})
url="{pkg_url}"
license=('{license_type}')
"""
        if dependencies_input:
            dep_list = [f"'{d.strip()}'" for d in dependencies_input.split(',') if d.strip()]
            if dep_list:
                pkgbuild_content += f"depends=({' '.join(dep_list)})\n"
        
        if make_dependencies_input:
            makep_list = [f"'{m.strip()}'" for m in make_dependencies_input.split(',') if m.strip()]
            if makep_list:
                pkgbuild_content += f"makedepends=({' '.join(makep_list)})\n"

        if source_files_input:
            src_list = [f"'{s.strip()}'" for s in source_files_input.split('\n') if s.strip()]
            if src_list:
                pkgbuild_content += f"source=({' '.join(src_list)})\n"

        if md5_sums_input:
            md5_list = [f"'{m.strip()}'" for m in md5_sums_input.split('\n') if m.strip()]
            if md5_list:
                pkgbuild_content += f"md5sums=({' '.join(md5_list)})\n"
        else:
            pkgbuild_content += "md5sums=('SKIP')\n"

        pkgbuild_content += """
build() {
    true # Placeholder command to ensure valid syntax
    # Change directory to the source folder
    # cd "$srcdir/$pkgname-$pkgver"
    # Example: ./configure --prefix=/usr
    # Example: make
}

package() {
    true # Placeholder command to ensure valid syntax
    # Change directory to the source folder
    # cd "$srcdir/$pkgname-$pkgver"
    # Example: make install DESTDIR="$pkgdir"
}
"""
        self.te_pkgbuild_output.setPlainText(pkgbuild_content)
        self.tab_widget.setCurrentIndex(1)

        QMessageBox.information(self, "Success", "PKGBUILD content generated. You can review and edit it in the 'PKGBUILD Output' tab.")

    def load_pkgbuild(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load PKGBUILD", "", "PKGBUILD Files (PKGBUILD);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.te_pkgbuild_output.setPlainText(content)

                    lines = content.split('\n')
                    
                    self.le_pkgname.clear()
                    self.le_pkgver.clear()
                    self.le_pkgrel.setText("1")
                    self.le_pkgdesc.clear()
                    self.le_arch.setText("'any'")
                    self.le_url.clear()
                    self.le_license.clear()
                    self.le_depends.clear()
                    self.le_makepends.clear()
                    self.te_source.clear()
                    self.te_md5sums.clear()

                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        
                        if line.startswith("pkgname="):
                            self.le_pkgname.setText(self._extract_pkgbuild_string(line))
                        elif line.startswith("pkgver="):
                            self.le_pkgver.setText(self._extract_pkgbuild_string(line))
                        elif line.startswith("pkgrel="):
                            self.le_pkgrel.setText(self._extract_pkgbuild_string(line))
                        elif line.startswith("pkgdesc="):
                            self.le_pkgdesc.setText(self._extract_pkgbuild_string(line))
                        elif line.startswith("arch="):
                            arch_values = self._extract_pkgbuild_array(line)
                            self.le_arch.setText(' '.join(f"'{a}'" for a in arch_values))
                        elif line.startswith("url="):
                            self.le_url.setText(self._extract_pkgbuild_string(line))
                        elif line.startswith("license="):
                            license_values = self._extract_pkgbuild_array(line)
                            self.le_license.setText(', '.join(license_values))
                        elif line.startswith("depends="):
                            dep_values = self._extract_pkgbuild_array(line)
                            self.le_depends.setText(', '.join(dep_values))
                        elif line.startswith("makedepends="):
                            makep_values = self._extract_pkgbuild_array(line)
                            self.le_makepends.setText(', '.join(makep_values))
                        elif line.startswith("source="):
                            src_values = self._extract_pkgbuild_array(line)
                            self.te_source.setPlainText('\n'.join(src_values))
                        elif line.startswith("md5sums="):
                            md5_values = self._extract_pkgbuild_array(line)
                            self.te_md5sums.setPlainText('\n'.join(md5_values))
                        
                    self.tab_widget.setCurrentIndex(0)
                    QMessageBox.information(self, "Success", "PKGBUILD file loaded and parsed successfully. Data is now in the 'Package Data' tab.")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load or parse file: {e}")

    def save_pkgbuild(self):
        pkgbuild_content = self.te_pkgbuild_output.toPlainText()
        if not pkgbuild_content.strip():
            QMessageBox.warning(self, "Warning", "No content to save.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save PKGBUILD", "PKGBUILD", "PKGBUILD Files (PKGBUILD);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(pkgbuild_content)
                QMessageBox.information(self, "Success", f"PKGBUILD saved successfully to: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def generate_srcinfo(self):
        pkgbuild_content = self.te_pkgbuild_output.toPlainText()
        if not pkgbuild_content.strip():
            QMessageBox.warning(self, "Action Required", "Please generate or load a PKGBUILD first.")
            return

        temp_pkgbuild_path = "PKGBUILD"
        try:
            with open(temp_pkgbuild_path, 'w', encoding='utf-8') as f:
                f.write(pkgbuild_content)

            result = subprocess.run(
                ['mksrcinfo', '-f'], 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=os.getcwd()
            )
            
            self.te_pkgbuild_output.setPlainText(result.stdout)
            self.tab_widget.setCurrentIndex(1)
            QMessageBox.information(self, "Success", ".SRCINFO generated successfully. You can review it in the 'PKGBUILD Output' tab.")

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Command 'mksrcinfo' not found. Please ensure 'pacman' and 'makepkg' are installed and in your system's PATH.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Error generating .SRCINFO: {e.stderr}\n\nPKGBUILD content might be invalid.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
        finally:
            if os.path.exists(temp_pkgbuild_path):
                os.remove(temp_pkgbuild_path)

    def _get_templates_dir(self):
        if "templates_dir" in self.settings and self.settings["templates_dir"]:
            templates_dir = self.settings["templates_dir"]
        else:
            app_dir = os.path.dirname(__file__)
            templates_dir = os.path.join(app_dir, 'templates')
            self.settings["templates_dir"] = templates_dir 
            self.save_settings(self.settings)

        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        return templates_dir

    def save_template(self):
        template_name, ok = QInputDialog.getText(self, "Save Template", "Enter template name:")
        if ok and template_name:
            template_name = template_name.strip()
            if not template_name:
                QMessageBox.warning(self, "Warning", "Template name cannot be empty.")
                return

            template_data = {
                "pkgname": self.le_pkgname.text(),
                "pkgver": self.le_pkgver.text(),
                "pkgrel": self.le_pkgrel.text(),
                "pkgdesc": self.le_pkgdesc.text(),
                "arch": self.le_arch.text(),
                "url": self.le_url.text(),
                "license": self.le_license.text(),
                "depends": self.le_depends.text(),
                "makedepends": self.le_makepends.text(),
                "source": self.te_source.toPlainText(),
                "md5sums": self.te_md5sums.toPlainText()
            }

            templates_dir = self._get_templates_dir()
            template_file_path = os.path.join(templates_dir, f"{template_name}.json")

            try:
                with open(template_file_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, indent=4)
                QMessageBox.information(self, "Success", f"Template '{template_name}' saved successfully to:\n{templates_dir}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save template: {e}")

    def load_template(self):
        templates_dir = self._get_templates_dir()
        
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Template", templates_dir, "JSON Templates (*.json);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)

                self.le_pkgname.setText(template_data.get("pkgname", ""))
                self.le_pkgver.setText(template_data.get("pkgver", ""))
                self.le_pkgrel.setText(template_data.get("pkgrel", "1"))
                self.le_pkgdesc.setText(template_data.get("pkgdesc", ""))
                self.le_arch.setText(template_data.get("arch", "'any'"))
                self.le_url.setText(template_data.get("url", ""))
                self.le_license.setText(template_data.get("license", ""))
                self.le_depends.setText(template_data.get("depends", ""))
                self.le_makepends.setText(template_data.get("makedepends", ""))
                self.te_source.setPlainText(template_data.get("source", ""))
                self.te_md5sums.setPlainText(template_data.get("md5sums", ""))
                
                self.tab_widget.setCurrentIndex(0)
                QMessageBox.information(self, "Success", f"Template loaded successfully from: {os.path.basename(file_name)}")
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Error", "Invalid template file. Please select a valid JSON template.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load template: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # تعيين اسم المنظمة والتطبيق لـ QStandardPaths
    app.setOrganizationName("YourOrganization") # يمكنك تغيير هذا
    app.setApplicationName("hel-pkg") # يجب أن يتطابق مع الاسم المستخدم في AppConfigLocation

    window = HelPkgApp()
    window.show()
    sys.exit(app.exec_())
