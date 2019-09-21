from PyQt5 import QtCore
from foo.ui_tcps import Ui_Form
from PyQt5.QtWidgets import (QWidget, QMessageBox)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class Window(QWidget):
    ui = Ui_Form()
    serial = QSerialPort()

    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化界面
        self.ui.setupUi(self)
        # 设置只显示关闭按钮
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 初始化串口列表
        self._refresh_com()

        # 连接槽函数
        self.ui.btn_connect.clicked.connect(self.open_port)
        self.serial.readyRead.connect(self.read_data)
        self.ui.btn_send.clicked.connect(self.on_send_clicked)

    def on_send_clicked(self):
        input_string = self.ui.txt_send.toPlainText()
        if input_string != '+++':
            input_string += '\r\n'
        self.send_data(input_string)

    # 打开串口
    def open_port(self):
        if self.ui.btn_connect.text() == '连接':
            com = self.ui.cbb_comlist.currentText()
            if com == '':
                return
            else:
                self.serial.close()
                self.serial.setPortName(com)
                baud_rate = self.ui.cbb_baud_rate.currentText()
                self.serial.setBaudRate(int(baud_rate))
                try:
                    if self.serial.open(QSerialPort.ReadWrite):
                        self.serial.open(QSerialPort.ReadWrite)
                        self.ui.btn_connect.setText('断开')
                        self.ui.btn_connect.setStyleSheet("color:red;")
                        self.ui.radio_address.setEnabled(True)
                        self.ui.radio_power.setEnabled(True)
                        self.ui.radio_baud_rate.setEnabled(True)
                        self.ui.radio_client.setEnabled(True)
                        self.ui.radio_server.setEnabled(True)
                        # 初始化配置
                        self.init_config()
                    else:
                        QMessageBox.critical(self, 'Message', '没有可用的串口或当前串口被占用')
                except:
                    QMessageBox.critical(self, 'Message', '串口异常')
        else:
            self.serial.close()
            self.ui.btn_connect.setText('连接')
            self.ui.btn_connect.setStyleSheet("color:black;")
            self.ui.radio_address.setEnabled(False)
            self.ui.radio_power.setEnabled(False)
            self.ui.radio_baud_rate.setEnabled(False)
            self.ui.radio_client.setEnabled(False)
            self.ui.radio_server.setEnabled(False)

    def init_config(self):
        # # 进入配置模式
        # self.send_data('+++')
        # # 读取配置
        # self.send_data('at&v\r\n')
        pass

    # 发送数据
    def send_data(self, input_string):
        if self.serial.isOpen():
            input_string = input_string.encode('UTF-8')  # 输出的数据为UTF-8码
            self.serial.write(input_string)
        else:
            QMessageBox.critical(self, 'Message', '请打开串口')

    # 接收数据
    def read_data(self):
        response = str(self.serial.readAll(), encoding='utf-8')
        self.ui.txt_receive.append(response)

    # 串口号更新
    def _refresh_com(self):
        # 获取串口列表
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            self.ui.cbb_comlist.addItem(info.portName())
