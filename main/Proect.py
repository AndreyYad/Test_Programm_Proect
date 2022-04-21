from ast import Delete
from sys import argv
from textwrap import indent
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QButtonGroup
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

        self.groupb = QButtonGroup()

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
            'open_que' : [
                self.ui.line_que
            ],
            'lines' : [
                self.ui.answer_1,
                self.ui.answer_2,
                self.ui.answer_3,
                self.ui.answer_4,
                self.ui.answer_5
            ],
            'var_ans' : [
                self.ui.var_ans_1,
                self.ui.var_ans_2,
                self.ui.var_ans_3,
                self.ui.var_ans_4,
                self.ui.var_ans_5
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



    def ChangeWindowRed(self, num, delete=True):

        for obj in self.widgets['var_ans']:
            self.groupb.removeButton(obj)

        if num == 0:
            self.TestJson = {
                'name':'',
                'questions':[]
            }
            self.WindowCreatTest = 0

        if self.WindowCreatTest == 0:
            self.TestJson['name'] = self.ui.line_name_test.text()
        else:
            if delete:
                self.TestJson['questions'][self.WindowCreatTest-1]['text'] = self.ui.text_que.toPlainText()
                if type(self.TestJson['questions'][self.WindowCreatTest-1]['answer']) == dict:
                    for index in range(5):
                        self.TestJson['questions'][self.WindowCreatTest-1]['answer']['list_ans'][index] = self.widgets['lines'][index].text()
                else:
                    self.TestJson['questions'][self.WindowCreatTest-1]['answer'] = self.ui.line_que.text()

        self.WindowCreatTest += num


        if self.WindowCreatTest == len(self.TestJson['questions'])+1:
            self.TestJson['questions'].append(
                {
                    'text':'',
                    'answer':
                    {
                        'value':4,
                        'right':[],
                        'type_close':1,
                        'list_ans':['' for i in range(5)]
                    }
                }
            )

        if self.WindowCreatTest != 0:
            self.ui.text_que.setText(self.TestJson['questions'][self.WindowCreatTest-1]['text'])
            if type(self.TestJson['questions'][self.WindowCreatTest-1]['answer']) == dict:
                for index in range(5):
                    self.ui.line_que.setText('')
                    self.widgets['lines'][index].setText(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['list_ans'][index])
                    self.ChageBox = True
                    self.widgets['var_ans'][index].setChecked(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right'].count(index))
            else:
                self.ui.line_que.setText(self.TestJson['questions'][self.WindowCreatTest-1]['answer'])
                

        if self.WindowCreatTest == len(self.TestJson['questions']):
            self.ui.but_next.setText('+')
        else:
            self.ui.but_next.setText('>')
            
        try:
            if type(self.TestJson['questions'][self.WindowCreatTest-1]['answer']) == dict:
                self.Open('close_que')

                for index in range(5):
                    self.widgets['lines'][index].hide()

                for index in range(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value']):
                    self.widgets['lines'][index].show()

                for index in range(5):
                    self.widgets['var_ans'][index].hide()

                for index in range(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value']):
                    self.widgets['var_ans'][index].show()

                if not self.TestJson['questions'][self.WindowCreatTest-1]['answer']['type_close']:
                    self.ui.one_var.setText('Один')
                    for obj in self.widgets['var_ans']:
                        self.groupb.addButton(obj)
                else:
                    self.ui.one_var.setText('Несколько')


                self.ui.slider.setValue(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value'])
            elif type(self.TestJson['questions'][self.WindowCreatTest-1]['answer']) == str:
                self.Open('open_que')
            self.Open('que_red_generic',False)

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
        self.ChangeWindowRed(-1,delete=False)

    def UpdateSlider(self):

        self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value'] = self.ui.slider.value()

        for index in self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right']:
            if index+1 > self.ui.slider.value():
                self.widgets['var_ans'][index].setChecked(False)
        
        for index in range(self.ui.slider.value()-1+1,5):
            self.widgets['lines'][index].setText('')

        for index in range(5):
            self.widgets['lines'][index].hide()

        for index in range(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value']):
            self.widgets['lines'][index].show()

        for index in range(5):
            self.widgets['var_ans'][index].hide()

        for index in range(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['value']):
            self.widgets['var_ans'][index].show()

    def ChangeValueVar(self,num):

        if self.widgets['var_ans'][num].isChecked() and not self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right'].count(num):
            self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right'].append(num)
        elif not self.ChageBox:
            self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right'].pop(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right'].index(num))

        self.ChageBox = False

        print(self.TestJson['questions'][self.WindowCreatTest-1]['answer']['right'])

    def Debug(self):

        print(self.TestJson['questions'])

    def ChangeTypeQue(self):

        if type(self.TestJson['questions'][self.WindowCreatTest-1]['answer']) == dict:
            self.TestJson['questions'][self.WindowCreatTest-1]['answer'] = ''
            self.ui.close_que.setText('Открытый')
            for obj in ['lines','var_ans','close_que']:
                self.WidgetsHide(obj)
            self.ui.line_que.show()
        else:
            self.TestJson['questions'][self.WindowCreatTest-1]['answer'] = {
                'value':4,
                'right':[],
                'type_close':1,
                'list_ans':['' for i in range(5)]
            }
            self.ui.close_que.setText('Закрытый')

        self.ChangeWindowRed(-1)
        self.ChangeWindowRed(1)
        


    def ChangeValueAns(self):

        if self.TestJson['questions'][self.WindowCreatTest-1]['answer']['type_close']:
            self.TestJson['questions'][self.WindowCreatTest-1]['answer']['type_close'] = 0
        else:
            self.TestJson['questions'][self.WindowCreatTest-1]['answer']['type_close'] = 1

        self.ChangeWindowRed(-1)
        self.ChangeWindowRed(1)


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
        self.widgets['que_red_generic'][2].clicked.connect(lambda: self.ChangeTypeQue())

        self.widgets['close_que'][0].valueChanged.connect(lambda: self.UpdateSlider())
        self.widgets['close_que'][1].clicked.connect(lambda: self.ChangeValueAns())

        self.widgets['var_ans'][0].toggled.connect(lambda: self.ChangeValueVar(0))
        self.widgets['var_ans'][1].toggled.connect(lambda: self.ChangeValueVar(1))
        self.widgets['var_ans'][2].toggled.connect(lambda: self.ChangeValueVar(2))
        self.widgets['var_ans'][3].toggled.connect(lambda: self.ChangeValueVar(3))
        self.widgets['var_ans'][4].toggled.connect(lambda: self.ChangeValueVar(4))

        self.ui.debug.clicked.connect(lambda: self.Debug())
    

if __name__ == '__main__':
    app = QApplication(argv)
    ex = App()
    app.exec_()