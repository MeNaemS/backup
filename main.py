from determinant.determinant import determinant
from disks.yandex_disk import yandex_backup


def choose_file() -> str:
    import sys
    from PyQt5.QtWidgets import QFileDialog, QApplication

    app = QApplication(sys.argv)
    return QFileDialog.getOpenFileNames(caption='Choose files')[0]


if __name__ == '__main__':
    file_path = choose_file()
    value = input('Enter email or phone number: ')
    password = input('Enter your account password: ')
    yandex_backup(value, password, determinant(value), file_path)
