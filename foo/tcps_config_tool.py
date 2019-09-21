from PyQt5.QtCore import (QTimer,QByteArray , Qt)
from foo.ui_tcps import Ui_Form
from foo.command_queue import command_queue
from PyQt5.QtWidgets import (QWidget, QMessageBox)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class Window(QWidget):
    _ui = Ui_Form()
    _serial = QSerialPort()
    _current_cmd = ''  # 当前指令
    _retry_count = 0  # 重试次数
    _buf = QByteArray()  # 读取到的数据

    def __init__(self, parent=None):
        super().__init__(parent)
        self._check_timer = QTimer(self)  # 超时监测定时器
        self._check_timer.setInterval(3000)  # 设定超时时间3秒

        self._read_timer = QTimer(self)  # 读数定时器
        self._read_timer.setInterval(100)
        # 初始化界面
        self._ui.setupUi(self)
        # 设置只显示关闭按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # 初始化串口列表
        self._refresh_com()

        # 连接槽函数
        self._ui.btn_connect.clicked.connect(self.open_port)
        self._serial.readyRead.connect(self.read_data)
        self._ui.btn_send.clicked.connect(self.on_send_clicked)
        self._check_timer.timeout.connect(self._check_timeout)
        self._read_timer.timeout.connect(self._read_timeout)

    def on_send_clicked(self):
        input_string = self._ui.txt_send.toPlainText()
        command_queue.push(input_string)
        self._update_current_cmd()
        self._execute_current_cmd()

    # 打开串口
    def open_port(self):
        if self._ui.btn_connect.text() == '连接':
            com = self._ui.cbb_comlist.currentText()
            if com == '':
                return
            else:
                self._serial.close()
                self._serial.setPortName(com)
                baud_rate = self._ui.cbb_baud_rate.currentText()
                self._serial.setBaudRate(int(baud_rate))
                try:
                    if self._serial.open(QSerialPort.ReadWrite):
                        self._serial.open(QSerialPort.ReadWrite)
                        self._ui.btn_connect.setText('断开')
                        self._ui.btn_connect.setStyleSheet("color:red;")
                        self._ui.radio_address.setEnabled(True)
                        self._ui.radio_power.setEnabled(True)
                        self._ui.radio_baud_rate.setEnabled(True)
                        self._ui.radio_client.setEnabled(True)
                        self._ui.radio_server.setEnabled(True)
                        # 初始化配置
                        self._init_config()
                    else:
                        QMessageBox.critical(self, 'Message', '没有可用的串口或当前串口被占用')
                except:
                    QMessageBox.critical(self, 'Message', '串口异常')
        else:
            self._serial.close()
            self._ui.btn_connect.setText('连接')
            self._ui.btn_connect.setStyleSheet("color:black;")
            self._ui.radio_address.setEnabled(False)
            self._ui.radio_power.setEnabled(False)
            self._ui.radio_baud_rate.setEnabled(False)
            self._ui.radio_client.setEnabled(False)
            self._ui.radio_server.setEnabled(False)

    # 发送数据
    def send_data(self, input_string):
        if input_string == '':
            return
        if input_string != '+++':
            input_string += '\r\n'
        if self._serial.isOpen():
            input_string = input_string.encode('UTF-8')  # 输出的数据为UTF-8码
            self._serial.write(input_string)
        else:
            QMessageBox.critical(self, 'Message', '请打开串口')

    # 接收数据
    def read_data(self):
        self._read_timer.start()
        self._buf.append(self._serial.readAll())

    # 串口号更新
    def _refresh_com(self):
        # 获取串口列表
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            self._ui.cbb_comlist.addItem(info.portName())

    # 执行当前指令，开启超时定时器
    def _execute_current_cmd(self):
        self._check_timer.start()
        self.send_data(self._current_cmd)

    def _update_current_cmd(self):
        self._current_cmd = command_queue.pop()

    def _check_timeout(self):
        # 关闭定时器
        if self._check_timer.isActive():
            self._check_timer.stop()
        # 清空指令
        while not command_queue.is_empty():
            command_queue.pop()
        QMessageBox.critical(self, 'Message', '指令执行超时' + self._current_cmd)

    def _read_timeout(self):
        # 关闭定时器
        if self._read_timer.isActive():
            self._read_timer.stop()
        if self._check_timer.isActive():
            self._check_timer.stop()

        response = str(self._buf, encoding='utf-8')
        if not self._check_buf(self._buf):
            self._retry_count += 1
            if self._retry_count > 3:
                QMessageBox.critical(self, 'Message', '尝试重试三次失败 指令：' + response)
            else:
                self._execute_current_cmd()
            return
        print(self._buf)
        self._ui.txt_receive.append(response)
        self._buf.clear()
        # 重试次数清零
        _retry_count = 0
        # 执行其他指令
        if not command_queue.is_empty():
            self._update_current_cmd()
            self._execute_current_cmd()

    def _init_config(self):
        # 进入配置模式
        command_queue.push('+++')
        # 读取配置
        command_queue.push('at&v')
        self._update_current_cmd()
        self._execute_current_cmd()

    # 检查返回值是否正确
    def _check_buf(self, buf):
        if self._current_cmd == '+++':
            if buf == b'ok\r\n':
                return True
        elif self._current_cmd == 'at&v':
            buf_str = str(buf, encoding='utf-8')
            if buf_str.startswith('at&v'):
                return True
        elif self._current_cmd == 'at&wa':
            buf_str = str(buf, encoding='utf-8')
            if buf_str.startswith('at&wa'):
                return True
        return False
