from PySide6 import QtWidgets, QtCore
from src.client.api import resolvers
from src.server.base.models import Zoo


class AddZoo(QtWidgets.QDialog):
    cities: {str: int}

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__settingUi()
        self.show()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QGridLayout()
        self.city_label = QtWidgets.QLabel()
        self.title_label = QtWidgets.QLabel()
        self.phone_label = QtWidgets.QLabel()
        self.city_combo_box = QtWidgets.QComboBox()
        self.title_line_edit = QtWidgets.QLineEdit()
        self.phone_line_edit = QtWidgets.QLineEdit()
        self.create_button = QtWidgets.QPushButton()
        self.close_button = QtWidgets.QPushButton()
        self.spacer = QtWidgets.QWidget()

    def __settingUi(self) -> None:
        self.setWindowTitle('Create zoo')
        self.setLayout(self.main_v_layout)

        self.main_v_layout.addWidget(self.city_label, row=1, column=1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.title_label, row=1, column=2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.phone_label, row=1, column=3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.city_combo_box, row=2, column=1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.title_line_edit, row=2, column=2, alignment=QtCore.Qt.AlignmentFag.AlignCenter)
        self.main_v_layout.addWidget(self.phone_line_edit, row=2, column=3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.spacer, row=3, column=2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.create_button, row=4, column=2, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.main_v_layout.addWidget(self.close_button, row=4, column=3, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.city_label.setText('City')
        self.title_label.setText('Title')
        self.phone_label.setText('Phone')
        self.create_button.setText('Create')
        self.close_button.setText('Close')

        self.create_button.clicked.connect(self.on_create_click)
        self.close_button.clicked.connect(self.on_close_click)

        for city in resolvers.get_all_zoos()["result"]:
            self.cities[city['title']] = city['id']

            self.city_combo_box.insertItem(self.city_combo_box.count(), city['name'])

        self.spacer.setFixedHeight(10)
        self.create_button.setFixedWidth(50)
        self.close_button.setFixedWidth(50)

    def data_validate(self) -> bool:
        return self.title_line_edit.text() != '' or self.phone_line_edit.text() != ''

    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        messagebox = QtWidgets.QMessageBox(self if not parent else parent)
        messagebox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        messagebox.setWindowTitle("Error" if error else "Information")
        messagebox.setText(text)
        messagebox.setIcon(QtWidgets.QMessageBox.Icon.Critical if error else QtWidgets.QMessageBox.Icon.Information)
        messagebox.show()

    def on_create_click(self) -> None:
        if not self.data_validate():
            self.show_message(
                text='One or more fields is empty',
                error=True,
                parent=self
            )

        zoo = Zoo(
            city_id=self.cities[self.city_combo_box.currentText()],
            title=self.title_line_edit.text(),
            phone=self.phone_line_edit.text()
        )

        answer = resolvers.create_zoo(zoo)

        match answer:
            case {"code": 400, "message": message}:
                self.show_message(
                    text=message,
                    error=True,
                    parent=self)
                return

            case {"code": 200, "message": message}:
                self.show_message(
                    text=message,
                    parent=self
                )

        self.parent().add_zoo(
            zoo_id=str(answer["result"]["id"]),
            city=self.city_combo_box.currentText(),
            title=str(answer["result"]["title"]),
            phone=str(answer["result"]["phone"])
        )

        self.close()

    def on_close_click(self) -> None:
        self.close()

