from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtGui import  QPixmap, QPainter, QColor, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QComboBox, QCheckBox, QStackedWidget, QFileDialog
from elementeditor import ElementEditor
from PyQt5.QtCore import QCoreApplication as QC
from pythonic_binance.client import Client
import pandas as pd
import os.path, datetime, logging, requests, json
from time import sleep
from Pythonic.record_function import Record, Function
from Pythonic.elementmaster import ElementMaster
from email.message import EmailMessage
from email.contentmanager import raw_data_manager
from sys import getsizeof
#from smtplib import SMTP

class MLSVM(ElementMaster):

    pixmap_path = 'images/MLSVM.png'
    child_pos = (True, False)

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # train_eval, decision_function, gamma_mode, gamma_value, filename, log_state

        train_eval          = 2
        decision_function   = 0
        gamma_mode          = 0
        gamma_value         = '1.0'
        filename            = None
        log_state           = False

        self.config = train_eval, decision_function, gamma_mode, gamma_value, filename, log_state

        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        logging.debug('MLSVM::__init__() called at row {}, column {}'.format(row, column))
        self.addFunction(MLSVMFunction)

    def __setstate__(self, state):
        logging.debug('MLSVM::__setstate__() called')
        self.row, self.column, self.config = state
        super().__init__(self.row, self.column, QPixmap(self.pixmap_path), True, self.config)
        super().edit_sig.connect(self.edit)
        self.addFunction(MLSVMFunction)

    def __getstate__(self):
        logging.debug('MLSVM::__getstate__() called')
        return (self.row, self.column, self.config)

    def openEditor(self):
        logging.debug('MLSVM::openEditor() called')

    def edit(self):

        logging.debug('MLSVM::edit()')

        """
        gamma: auto oder float eingabe
        decision function shape: ovr oder ovo

        data split train / eval
        """
        # train_eval, decision_function, gamma_mode, gamma_value, filename, log_state
        self.train_eval, self.decision_function, self.gamma_mode, \
            self.gamma_value, self.filename, self.log_state = self.config

        self.train_test_label = QLabel()
        self.train_test_label.setText(
                QC.translate('', 'Choose train / evalutaion ratio:'))

        self.train_test_list = QComboBox()
        self.train_test_list.addItem('90/10', QVariant(90))
        self.train_test_list.addItem('80/20', QVariant(80))
        self.train_test_list.addItem('70/30', QVariant(70))
        self.train_test_list.addItem('60/40', QVariant(60))
        self.train_test_list.addItem('50/50', QVariant(50))

        self.decision_function_label = QLabel()
        self.decision_function_label.setText(QC.translate('', 'Choose decision function shape:'))

        self.decision_function_list = QComboBox()
        self.decision_function_list.addItem('ovo', QVariant('ovo'))
        self.decision_function_list.addItem('ovr', QVariant('ovr'))

        self.gamma_label = QLabel()
        self.gamma_label.setText(QC.translate('', 'Gamma:'))

        self.gamma_list = QComboBox()
        self.gamma_list.addItem('Auto', QVariant('auto'))
        self.gamma_list.addItem('Scaled', QVariant('scaled'))
        self.gamma_list.addItem('Manual', QVariant('manual'))

        self.gamma_input_line = QWidget()
        #self.gamma_input_line.setMinimumHeight(100)
        self.gamma_input_line_layout = QHBoxLayout(self.gamma_input_line)
        self.gamma_input_txt = QLabel()
        self.gamma_input_txt.setText(QC.translate('', 'Gamma:'))
        self.gamma_input = QLineEdit()
        self.gamma_input.setPlaceholderText('1.0')
        self.gamma_input.setValidator(QDoubleValidator(0, 999, 3))
        self.gamma_input_line_layout.addWidget(self.gamma_input_txt)
        self.gamma_input_line_layout.addWidget(self.gamma_input)

        self.conn_rest_layout = QVBoxLayout()
        self.confirm_button = QPushButton(QC.translate('', 'Ok'))

        self.filename_text = QLabel()
        
        self.file_button = QPushButton(QC.translate('', 'Select model output file'))
        self.file_button.clicked.connect(self.ChooseFileDialog)

        
        """
        self.pass_input_line = QWidget()
        self.pass_input_txt = QLabel()
        self.pass_input_txt.setText(QC.translate('','Use input string as URL?'))
        self.pass_input_check = QCheckBox()
        self.pass_input_line_layout = QHBoxLayout(self.pass_input_line)
        self.pass_input_line_layout.addWidget(self.pass_input_txt)
        self.pass_input_line_layout.addWidget(self.pass_input_check)
        self.pass_input_line_layout.addStretch(1)


        self.url_address_txt = QLabel()
        self.url_address_txt.setText(QC.translate('', 'URL:'))
        self.url_address_input = QLineEdit()
        self.url_address_input.setPlaceholderText(
                QC.translate('', 'https://www.bitstamp.net/api/ticker/'))

        """
        self.help_text_1 = QLabel()
        self.help_text_1.setText(QC.translate('', 'GET answer is transformed to Python list object'))

        

        # hier logging option einfügen
        self.log_line = QWidget()
        self.ask_for_logging = QLabel()
        self.ask_for_logging.setText(QC.translate('', 'Log output?'))
        self.log_checkbox = QCheckBox()
        self.log_line_layout = QHBoxLayout(self.log_line)
        self.log_line_layout.addWidget(self.ask_for_logging)
        self.log_line_layout.addWidget(self.log_checkbox)
        self.log_line_layout.addStretch(1)

        
        self.ml_svm_edit = ElementEditor(self)
        self.ml_svm_edit.setWindowTitle(QC.translate('', 'Support Vector Machine'))
        self.ml_svm_edit.setMinimumHeight(500)

        # signals and slots
        self.gamma_list.currentIndexChanged.connect(self.indexChanged)
        self.confirm_button.clicked.connect(self.ml_svm_edit.closeEvent)
        self.ml_svm_edit.window_closed.connect(self.edit_done)

        # load config
        self.loadLastConfig()

        self.conn_rest_layout.addWidget(self.train_test_label)
        self.conn_rest_layout.addWidget(self.train_test_list)
        self.conn_rest_layout.addWidget(self.decision_function_label)
        self.conn_rest_layout.addWidget(self.decision_function_list)
        self.conn_rest_layout.addWidget(self.gamma_label)
        self.conn_rest_layout.addWidget(self.gamma_list)
        self.conn_rest_layout.addWidget(self.gamma_input_line)
        self.conn_rest_layout.addWidget(self.filename_text)
        self.conn_rest_layout.addWidget(self.file_button)
        self.conn_rest_layout.addStretch(1)
        self.conn_rest_layout.addWidget(self.help_text_1)
        self.conn_rest_layout.addWidget(self.log_line)
        self.conn_rest_layout.addWidget(self.confirm_button)
        self.ml_svm_edit.setLayout(self.conn_rest_layout)
        self.ml_svm_edit.show()

    def loadLastConfig(self):

        logging.debug('MLSVM::loadLastConfig() called')
        
        self.train_test_list.setCurrentIndex(self.train_eval)
        self.decision_function_list.setCurrentIndex(self.decision_function)
        self.gamma_list.setCurrentIndex(self.gamma_mode)
        self.gamma_input.setText(self.gamma_value)
        self.indexChanged(self.gamma_mode)
        if self.filename:
            self.filename_text.setText(self.filename)

    def indexChanged(self, event):

        current_index = event
        logging.debug('MLSVM::indexChanged() called: {}'.format(event))
        if event == 2 :
            self.gamma_input_line.setVisible(True)
        else:
            self.gamma_input_line.setVisible(False)

    def ChooseFileDialog(self, event):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, \
                QC.translate('', 'Choose file'),"","All Files (*);;Text Files (*.txt)", \
                options=options)
        if fileName:
            logging.debug('ChooseFileDialog() called with filename: {}'.format(fileName))
            self.filename = fileName
            self.filename_text.setText(self.filename)


    def edit_done(self):

        logging.debug('MLSVM::edit_done() called')

        """
        # pass_input, url, log_state

        pass_input  = self.pass_input_check.isChecked()
        url         = self.url_address_input.text()
        log_state   = self.log_checkbox.isChecked()

        self.config = pass_input, url, log_state
        logging.debug('########CONFIG: {}'.format(self.config))
        """

        self.addFunction(MLSVMFunction)

class MLSVMFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        logging.debug('MLSVMFunction::__init__() called')

    def execute(self, record):

        # pass_input, url, log_state
        pass_input, url, log_state = self.config

        if pass_input:
            recv_string = requests.get(str(record))
        else:
            recv_string = requests.get(url)

        record = json.loads(recv_string.text)


        log_txt = '{REST call succesfull}'
        log_output = '{} bytes received'.format(getsizeof(recv_string.text))

        result = Record(self.getPos(), (self.row +1, self.column), record,
                 log=log_state, log_txt=log_txt, log_output=log_output)

        
        return result