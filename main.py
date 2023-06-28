from checker.checker import Checker
from disks.yandex_disk import yandex_backup


def choose_file() -> str:
    import sys
    from PyQt5.QtWidgets import QFileDialog, QApplication

    app = QApplication(sys.argv)
    return QFileDialog.getOpenFileNames(caption='Choose files')[0]


if __name__ == '__main__':
    file_path = choose_file()
    value = 'ilikesleeping268@ya.ru'
    check_adress = Checker(value)
    if check_adress.boolean is False:
        raise ValueError('Email address is not valid')
    if check_adress.option == 'phone':
        from sys import exit

        print('We apologize, at the moment support for a phone number for backup in Yandex Disk is not available')
        exit()
    password = 'GooglePasswordMadeWithMe'
    yandex_backup(value, password, check_adress.option, file_path)
