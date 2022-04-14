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
            ],
            'close_que' : [
                self.ui.slider,
                self.ui.one_var
            ],
            'lines' : [
                self.ui.answer_1,
                self.ui.answer_2,
                self.ui.answer_3,
                self.ui.answer_4,
                self.ui.answer_5
            ],
            'que_red_generic' : [
                self.ui.text_que,
                self.ui.num_que,
                self.ui.close_que,
                self.ui.but_delete
            ]
        }

        self.Open('main')
        self.ButtonsWork()

    def Open(self,name,hide=True):

        #Метод открытия наборов элементов
        
        if hide:
            self.WidgetsHide(0)

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

    def ChangeWindowRed(self, num):

        if num == 0:
            self.TestJson = {
                'name':'',
                'questions':[]
            }
            self.WindowCreatTest = 0

        if self.WindowCreatTest == 0:
            self.TestJson['name'] = self.ui.line_name_test

        self.WindowCreatTest += num

        print(self.WindowCreatTest)

        if self.WindowCreatTest == len(self.TestJson['questions'])+1:
            self.TestJson['questions'].append(
                {
                    'text':'',
                    'type':'close',
                    'answer':
                    {
                        'value':4,
                        'right':[],
                        'type_close':1
                    }
                }
            )

        if self.WindowCreatTest == len(self.TestJson['questions']):
            self.ui.but_next.setText('+')
        else:
            self.ui.but_next.setText('>')
            
        try:
            if self.TestJson['questions'][self.WindowCreatTest-1]['type'] == 'close':
                self.Open('close_que')
                self.Open('que_red_generic',False)

                for index in range(5):
                    self.widgets['lines'][index].hide()

                for index in range(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value']):
                    self.widgets['lines'][index].show()

                self.ui.slider.setValue(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value'])

        except IndexError:
            pass

        if self.WindowCreatTest == 0:
            self.Open('first_win_test')
            self.ui.but_pre.hide()
        else:
            self.ui.num_que.setText('{}/{}'.format(self.WindowCreatTest, len(self.TestJson['questions'])))
            self.ui.but_pre.show()

        self.ui.but_next.show()

    
    def DeleteQue(self):

        self.TestJson['questions'].pop(self.WindowCreatTest-1)
        self.ChangeWindowRed(-1)


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

        self.widgets['main_test'][0].clicked.connect(lambda: self.ChangeWindowRed(0))

        self.widgets['generic_test'][0].clicked.connect(lambda: self.ChangeWindowRed(-1))
        self.widgets['generic_test'][1].clicked.connect(lambda: self.ChangeWindowRed(1))

        self.widgets['que_red_generic'][3].clicked.connect(lambda: self.DeleteQue())



    

if __name__ == '__main__':
    app = QApplication(argv)
    ex = App()
    app.exec_()