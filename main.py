import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QWidget,
    QListWidget,
    QMessageBox,
    QSplitter,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from scrape import fetch_tables_from_url, extract_table_to_dataframe, generate_extraction_script


class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Browser with Table Selection")
        self.setGeometry(100, 100, 1200, 800)  # Default size
        self.setMinimumSize(800, 600)  # Allow resizing

        # Main browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://example.com"))  # Default URL

        # Input and navigation
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL and press Enter")
        self.url_input.returnPressed.connect(self.load_url)

        # Extract button
        self.extract_button = QPushButton("Extract Tables")
        self.extract_button.clicked.connect(self.extract_tables)

        # Table selection list
        self.table_list = QListWidget()
        self.table_list.itemDoubleClicked.connect(self.extract_selected_table)

        # Top controls layout
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.url_input)
        controls_layout.addWidget(self.extract_button)

        controls_widget = QWidget()
        controls_widget.setLayout(controls_layout)

        # Splitter to make widgets resizable
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(controls_widget)
        splitter.addWidget(self.browser)
        splitter.addWidget(self.table_list)
        splitter.setStretchFactor(1, 5)  # Give more space to the browser
        splitter.setCollapsible(0, False)  # Prevent collapsing of controls

        # Set the main layout
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.tables = []  # Store extracted tables

    def load_url(self):
        url = self.url_input.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def extract_tables(self):
        self.browser.page().toHtml(self.process_html)

    def process_html(self, html):
        # Extract tables from the page
        self.tables = fetch_tables_from_url(html)
        self.table_list.clear()

        if self.tables:
            for i, table_data in enumerate(self.tables):
                self.table_list.addItem(f"Table {i + 1} - {table_data['rows']} rows")
            QMessageBox.information(self, "Tables Found", "Double-click a table to extract.")
        else:
            QMessageBox.warning(self, "No Tables Found", "No tables were found on this page.")

    def extract_selected_table(self, item):
        selected_index = self.table_list.row(item)
        selected_table = self.tables[selected_index]["content"]

        df = extract_table_to_dataframe(selected_table)

        # Save table as CSV
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Table", "", "CSV Files (*.csv)")
        if file_path:
            df.to_csv(file_path, index=False)
            QMessageBox.information(self, "Success", f"Table data saved to {file_path}")

            # Generate Python script
            script_path = file_path.replace(".csv", "_extractor.py")
            try:
                generate_extraction_script(script_path, file_path, self.browser.url().toString(), selected_index)
                QMessageBox.information(self, "Script Generated", f"Python script saved to {script_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save script: {e}")
        else:
            QMessageBox.warning(self, "Save Cancelled", "No file was saved.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomBrowser()
    browser.show()
    sys.exit(app.exec_())
