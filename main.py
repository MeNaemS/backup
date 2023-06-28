from checker.checker import Checker
from disks.yandex_disk import yandex_backup


def choose_file() -> str:
    import sys
    from PyQt5.QtWidgets import QFileDialog, QApplication

    app = QApplication(sys.argv)
    return QFileDialog.getOpenFileNames(caption='Choose files')[0]


if __name__ == '__main__':
    file_path = choose_file()
    value = input()
    check_adress = Checker(value)
    password = input()
    yandex_backup(value, password, check_adress.option, file_path)
