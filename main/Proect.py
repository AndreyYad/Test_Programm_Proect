from sys import argv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from subprocess import check_output
from os.path import dirname, abspath
import json

class App(QWidget):

    def __init__(self):

        #print(check_output('wmic csproduct get uuid').decode().split('\n')[1].strip())

        #запуск дизайна
        self.path = abspath(dirname(argv[0]))
        self.ui = uic.loadUi(self.path[:self.path.rindex('\\')] + '\\design\\Design.ui')
        self.ui.show()

        self.WindowCreatTest = 0

        #"Наборы" элементов дизайна
        self.widgets = {
            'main' : [
                self.ui.label,
                self.ui.but_reg,
                self.ui.but_sign,
                self.ui.but_info,
                self.ui.but_create_test
            ],
            'info' : [
                self.ui.info_text,
                self.ui.but_info_back,
                self.ui.label_2
            ],
            'reg' : [
                self.ui.text_reg_login,
                self.ui.text_reg_password,
                self.ui.text_reg_password_2,

                self.ui.line_reg_login,
                self.ui.line_reg_password,
                self.ui.line_reg_password_2,

                self.ui.but_reg_enter,
                self.ui.but_reg_back
            ],
            'sign' : [
                self.ui.but_sign_enter,
                self.ui.line_sign_login,
                self.ui.line_sign_password,
                self.ui.text_sign_login,
                self.ui.text_sign_password,
                self.ui.but_sign_back
            ],
            'main_test' : [
                self.ui.but_new_test,
                self.ui.but_old_test,
                self.ui.but_tmain_back
            ],
            'generic_test': [
                self.ui.but_pre,
                self.ui.but_next
            ],
            'first_win_test' : [
                self.ui.line_name_test,
                self.ui.label_name_test
            ],
            'exit_red' : [
                self.ui.but_no_exit,
                self.ui.but_exit,
                self.ui.info_text_2
            ]
        }

        self.Open('main')
        self.ButtonsWork()

    def Open(self,name):

        #Метод открытия наборов элементов
        
        self.WidgetsHide(0)

        if ['first_win_test'].count(name):
            self.Open('generic_test')
        else:
            self.WidgetsHide('generic_test')

        #Сброс текстовых строк
        if name == 'reg' or name == 'sign':
            for Obj in [self.ui.line_reg_login, self.ui.line_reg_password, self.ui.line_reg_password_2, self.ui.line_sign_password, self.ui.line_sign_login]:
                Obj.setText('')

        for obj in self.widgets[name]:
            obj.show()
                
                
    def WidgetsHide(self, name):

        if name == 0:
            ListKeys = list(self.widgets.keys())
        else:
            ListKeys = [name]
                
        for Key in ListKeys:
            for Object in self.widgets[Key]:
                Object.hide()

    def ButtonsWork(self):

        #Действие кнопок

        self.widgets['main'][3].clicked.connect(lambda: self.Open('info'))
        self.widgets['main'][2].clicked.connect(lambda: self.Open('sign'))
        self.widgets['main'][4].clicked.connect(lambda: self.Open('main_test'))
        self.widgets['main'][1].clicked.connect(lambda: self.Open('reg'))

        self.widgets['info'][1].clicked.connect(lambda: self.Open('main'))

        self.widgets['reg'][7].clicked.connect(lambda: self.Open('main'))

        self.widgets['sign'][5].clicked.connect(lambda: self.Open('main'))

        self.widgets['main_test'][2].clicked.connect(lambda: self.Open('main'))

        self.widgets['main_test'][0].clicked.connect(lambda: self.Open('first_win_test'))




    

if __name__ == '__main__':
    app = QApplication(argv)
    ex = App()
    app.exec_()