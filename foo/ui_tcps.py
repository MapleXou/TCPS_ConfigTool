# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tcps.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(230, 360)
        Form.setMinimumSize(QtCore.QSize(230, 360))
        Form.setMaximumSize(QtCore.QSize(230, 360))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.cbb_comlist = QtWidgets.QComboBox(self.groupBox)
        self.cbb_comlist.setObjectName("cbb_comlist")
        self.gridLayout_2.addWidget(self.cbb_comlist, 0, 1, 1, 1)
        self.btn_connect = QtWidgets.QPushButton(self.groupBox)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout_2.addWidget(self.btn_connect, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.cbb_baud_rate = QtWidgets.QComboBox(self.groupBox)
        self.cbb_baud_rate.setObjectName("cbb_baud_rate")
        self.cbb_baud_rate.addItem("")
        self.cbb_baud_rate.addItem("")
        self.cbb_baud_rate.addItem("")
        self.cbb_baud_rate.addItem("")
        self.cbb_baud_rate.addItem("")
        self.gridLayout_2.addWidget(self.cbb_baud_rate, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_parameter_conf = QtWidgets.QWidget()
        self.tab_parameter_conf.setObjectName("tab_parameter_conf")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_parameter_conf)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.tab_parameter_conf)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.radio_address = QtWidgets.QLineEdit(self.tab_parameter_conf)
        self.radio_address.setEnabled(True)
        self.radio_address.setObjectName("radio_address")
        self.gridLayout.addWidget(self.radio_address, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_parameter_conf)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.radio_power = QtWidgets.QLineEdit(self.tab_parameter_conf)
        self.radio_power.setEnabled(True)
        self.radio_power.setObjectName("radio_power")
        self.gridLayout.addWidget(self.radio_power, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab_parameter_conf)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.radio_baud_rate = QtWidgets.QComboBox(self.tab_parameter_conf)
        self.radio_baud_rate.setEnabled(True)
        self.radio_baud_rate.setObjectName("radio_baud_rate")
        self.radio_baud_rate.addItem("")
        self.radio_baud_rate.addItem("")
        self.radio_baud_rate.addItem("")
        self.radio_baud_rate.addItem("")
        self.radio_baud_rate.addItem("")
        self.gridLayout.addWidget(self.radio_baud_rate, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radio_client = QtWidgets.QRadioButton(self.tab_parameter_conf)
        self.radio_client.setEnabled(True)
        self.radio_client.setChecked(True)
        self.radio_client.setObjectName("radio_client")
        self.horizontalLayout.addWidget(self.radio_client)
        self.radio_server = QtWidgets.QRadioButton(self.tab_parameter_conf)
        self.radio_server.setEnabled(True)
        self.radio_server.setObjectName("radio_server")
        self.horizontalLayout.addWidget(self.radio_server)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_update = QtWidgets.QPushButton(self.tab_parameter_conf)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout_3.addWidget(self.btn_update)
        self.btn_apply = QtWidgets.QPushButton(self.tab_parameter_conf)
        self.btn_apply.setObjectName("btn_apply")
        self.horizontalLayout_3.addWidget(self.btn_apply)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_parameter_conf, "")
        self.tab_command_send = QtWidgets.QWidget()
        self.tab_command_send.setObjectName("tab_command_send")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_command_send)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txt_send = QtWidgets.QTextEdit(self.tab_command_send)
        self.txt_send.setEnabled(True)
        self.txt_send.setObjectName("txt_send")
        self.verticalLayout.addWidget(self.txt_send)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_send = QtWidgets.QPushButton(self.tab_command_send)
        self.btn_send.setEnabled(True)
        self.btn_send.setObjectName("btn_send")
        self.horizontalLayout_2.addWidget(self.btn_send)
        spacerItem = QtWidgets.QSpacerItem(88, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab_command_send, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.txt_receive = QtWidgets.QTextEdit(Form)
        self.txt_receive.setReadOnly(False)
        self.txt_receive.setObjectName("txt_receive")
        self.verticalLayout_3.addWidget(self.txt_receive)

        self.retranslateUi(Form)
        self.cbb_baud_rate.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.radio_baud_rate.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "电台调试助手"))
        self.groupBox.setTitle(_translate("Form", "连接配置"))
        self.label.setText(_translate("Form", "端口号"))
        self.btn_connect.setText(_translate("Form", "连接"))
        self.label_2.setText(_translate("Form", "波特率"))
        self.cbb_baud_rate.setCurrentText(_translate("Form", "9600"))
        self.cbb_baud_rate.setItemText(0, _translate("Form", "4800"))
        self.cbb_baud_rate.setItemText(1, _translate("Form", "9600"))
        self.cbb_baud_rate.setItemText(2, _translate("Form", "19200"))
        self.cbb_baud_rate.setItemText(3, _translate("Form", "57600"))
        self.cbb_baud_rate.setItemText(4, _translate("Form", "115200"))
        self.label_3.setText(_translate("Form", "网络地址"))
        self.label_4.setText(_translate("Form", "输出功率"))
        self.label_5.setText(_translate("Form", "波特率"))
        self.radio_baud_rate.setCurrentText(_translate("Form", "9600"))
        self.radio_baud_rate.setItemText(0, _translate("Form", "4800"))
        self.radio_baud_rate.setItemText(1, _translate("Form", "9600"))
        self.radio_baud_rate.setItemText(2, _translate("Form", "19200"))
        self.radio_baud_rate.setItemText(3, _translate("Form", "57600"))
        self.radio_baud_rate.setItemText(4, _translate("Form", "115200"))
        self.radio_client.setText(_translate("Form", "从站"))
        self.radio_server.setText(_translate("Form", "主站"))
        self.btn_update.setText(_translate("Form", "刷新"))
        self.btn_apply.setText(_translate("Form", "应用"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_parameter_conf), _translate("Form", "参数配置"))
        self.btn_send.setText(_translate("Form", "发送"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_command_send), _translate("Form", "指令发送"))
        self.txt_receive.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
