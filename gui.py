from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QFormLayout, QWidget, QPushButton, QLabel, QLineEdit,
                             QCheckBox, QSpinBox, QComboBox)


class AH_Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Form Layout Example")

        # Create the layout for the main window
        self.layout = QVBoxLayout()

        # Create a QFormLayout that will be dynamically populated
        self.form_layout = QFormLayout()

        # Add the form layout to the main layout
        self.layout.addLayout(self.form_layout)

        # Create checkboxes to control which fields should appear in the form
        self.name_checkbox = QCheckBox("Include Name")
        self.age_checkbox = QCheckBox("Include Age")
        self.gender_checkbox = QCheckBox("Include Gender")

        # Add checkboxes to the layout
        self.layout.addWidget(self.name_checkbox)
        self.layout.addWidget(self.age_checkbox)
        self.layout.addWidget(self.gender_checkbox)

        # Create a button to generate the form
        self.generate_button = QPushButton("Generate Form")
        self.generate_button.clicked.connect(self.generate_form)

        # Add the button to the layout
        self.layout.addWidget(self.generate_button)

        # Set the layout for the window
        self.setLayout(self.layout)

    def generate_form(self):
        # Clear any existing fields from the form
        self.clear_form()

        # Dynamically add fields based on checkbox state
        if self.name_checkbox.isChecked():
            name_label = QLabel("Name:")
            name_input = QLineEdit()
            self.form_layout.addRow(name_label, name_input)

        if self.age_checkbox.isChecked():
            age_label = QLabel("Age:")
            age_input = QSpinBox()
            age_input.setRange(0, 120)  # Age range
            self.form_layout.addRow(age_label, age_input)

        if self.gender_checkbox.isChecked():
            gender_label = QLabel("Gender:")
            gender_input = QComboBox()
            gender_input.addItems(["Select", "Male", "Female", "Other"])
            self.form_layout.addRow(gender_label, gender_input)

    def clear_form(self):
        # Clear the current layout (remove all widgets)
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()