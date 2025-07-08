# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("hel-pkg Help")
        self.setGeometry(100, 100, 700, 500) # حجم افتراضي أعرض وأطول شوية عشان النص

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.text_browser = QTextBrowser()
        self.text_browser.setReadOnly(True) # جعل النص للقراءة فقط

        # محتوى المساعدة (استخدم تنسيق HTML لتحكم أفضل)
        help_text = """
        <h2><b>Usage Instructions for hel-pkg</b></h2>
        <p>This tool helps you create and manage <b>PKGBUILD</b> files easily for <b>Arch Linux</b> packages.</p>
        
        <h3>1. Package Data Tab:</h3>
        <ul>
            <li><b>Package Name (pkgname):</b> The unique name for your package.</li>
            <li><b>Package Version (pkgver):</b> The version number of the upstream software.</li>
            <li><b>Package Release (pkgrel):</b> The release number of the PKGBUILD itself for this version. Typically starts at <code>1</code> and increments for PKGBUILD changes.</li>
            <li><b>Description (pkgdesc):</b> A concise, single-line description of the package.</li>
            <li><b>Architecture (arch):</b> The architecture(s) the package is built for (e.g., <code>'any'</code> for arch-independent, <code>'x86_64'</code>). Use single quotes and separate with spaces for multiple.</li>
            <li><b>URL:</b> The official project website or upstream URL for the software.</li>
            <li><b>License:</b> The license type under which the software is distributed (e.g., <code>'GPL'</code>, <code>'MIT'</code>, <code>'LGPL'</code>). Use single quotes.</li>
            <li><b>Dependencies (depends):</b> Runtime dependencies required by the package. Enter them comma-separated (e.g., <code>'bash', 'python'</code>).</li>
            <li><b>Make Dependencies (makedepends):</b> Dependencies only needed during the build process. Enter them comma-separated (e.g., <code>'gcc', 'make'</code>).</li>
            <li><b>Source Files (source):</b> Paths or URLs to the source files (e.g., tarballs, git repositories). Enter each source on a new line.</li>
            <li><b>MD5 Sums (md5sums):</b> MD5 checksums for each source file, in the same order as listed in 'Source Files'. Enter each sum on a new line. You can leave this field <b>empty</b> to set <code>md5sums=('SKIP')</code> in the generated PKGBUILD.</li>
        </ul>

        <h3>2. PKGBUILD Output Tab:</h3>
        <ul>
            <li>This tab displays the generated PKGBUILD content. You can review, copy, and directly edit the content here before saving.</li>
        </ul>

        <h3>3. Control Buttons:</h3>
        <ul>
            <li><b>Generate PKGBUILD:</b> Compiles data from the 'Package Data' tab into a PKGBUILD.</li>
            <li><b>Load PKGBUILD:</b> Opens an existing PKGBUILD file, displays its content, and attempts to populate the input fields in the 'Package Data' tab.</li>
            <li><b>Save PKGBUILD:</b> Saves the current content from the 'PKGBUILD Output' tab to a file.</li>
            <li><b>Generate .SRCINFO:</b> Creates or updates the <code>.SRCINFO</code> file based on the current PKGBUILD content. This requires <code>makepkg</code> to be installed and available in your system's PATH.</li>
            <li><b>Save Template:</b> Saves the current input values from the 'Package Data' tab as a reusable template.</li>
            <li><b>Load Template:</b> Loads saved input values from a template file.</li>
            <li><b>Settings:</b> Access application settings, such as defining the default directory for saving/loading templates.</li>
            <li><b>About:</b> Displays information about this application (version, developer, etc.).</li>
            <li><b>Help:</b> Shows this comprehensive help guide.</li>
        </ul>

        <p><b>Important Notes:</b></p>
        <ul>
            <li>Remember to fill in the <code>build()</code> and <code>package()</code> functions manually in the 'PKGBUILD Output' tab after generation. The tool provides placeholders.</li>
            <li>Always verify the generated PKGBUILD for correctness, especially for complex packages.</li>
            <li>For more in-depth information on PKGBUILD structure and best practices, refer to the <a href="https://wiki.archlinux.org/title/PKGBUILD">Arch Linux PKGBUILD Wiki</a>.</li>
        </ul>
        """
        self.text_browser.setHtml(help_text) # تعيين المحتوى كـ HTML

        layout.addWidget(self.text_browser)

        # زر الإغلاق
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch(1)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept) # يتم قبول النافذة عند الضغط على Close
        close_button_layout.addWidget(close_button)
        close_button_layout.addStretch(1)
        
        layout.addLayout(close_button_layout)

        self.setLayout(layout)
