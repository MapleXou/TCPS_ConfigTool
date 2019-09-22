from PyQt5.QtCore import (QTimer, QByteArray, Qt)
from foo.ui_tcps import Ui_Form
from foo.command_queue import command_queue
from PyQt5.QtWidgets import (QWidget, QMessageBox)
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import time
import re


class Window(QWidget):
    _ui = Ui_Form()
    _serial = QSerialPort()
    _current_cmd = ''  # 当前指令
    _retry_count = 0  # 重试次数
    _buf = QByteArray()  # 读取到的数据

    _mode = None  # 主从模式（0表示主）
    _baud_rate_index = None  # 波特率索引,7为9600
    _address = None  # 网络地址（任意）
    _power = None  # 输出功率（20-30）

    def __init__(self, parent=None):
        super().__init__(parent)
        self._check_timer = QTimer(self)  # 超时监测定时器
        self._check_timer.setInterval(3000)  # 设定超时时间3秒

        self._read_timer = QTimer(self)  # 读数定时器
        self._read_timer.setInterval(100)
        # 初始化界面
        self._ui.setupUi(self)
        self._ui.tabWidget.setEnabled(False)  # 初始化控制面板不可编辑
        self._ui.tab_parameter_conf.setEnabled(False)
        # 设置只显示关闭按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # 初始化串口列表
        self._refresh_com()

        # 连接槽函数
        self._ui.btn_connect.clicked.connect(self.open_port)
        self._serial.readyRead.connect(self.read_data)
        self._ui.btn_config_mode.clicked.connect(self.on_config_mode_clicked)
        self._ui.btn_send.clicked.connect(self.on_send_clicked)
        self._ui.btn_update.clicked.connect(self.on_update_clicked)
        self._ui.btn_apply.clicked.connect(self.on_apply_clicked)
        self._check_timer.timeout.connect(self._check_timeout)
        self._read_timer.timeout.connect(self._read_timeout)

    def on_config_mode_clicked(self):
        if self._ui.btn_config_mode.text() == '进入配置模式':
            command_queue.push('+++')
            self._update_current_cmd()
            self._execute_current_cmd()
            self._ui.btn_config_mode.setText('保存并退出')
            self._ui.btn_config_mode.setStyleSheet("color:green;")
            self._ui.tab_parameter_conf.setEnabled(True)
        else:
            command_queue.push('at&wa')
            self._update_current_cmd()
            self._execute_current_cmd()
            self._ui.btn_config_mode.setText('进入配置模式')
            self._ui.btn_config_mode.setStyleSheet("color:black;")
            self._ui.tab_parameter_conf.setEnabled(False)

    def on_send_clicked(self):
        input_string = self._ui.txt_send.toPlainText()
        if input_string == '':
            now = time.strftime('%H:%M:%S', time.localtime())
            self._ui.txt_receive.append('[' + now + ']\t' + '输入指令为空')
            return
        command_queue.push(input_string)
        self._update_current_cmd()
        self._execute_current_cmd()

    def on_update_clicked(self):
        # 更新电台信息
        input_string = 'at&v'
        command_queue.push(input_string)
        self._update_current_cmd()
        self._execute_current_cmd()

    def on_apply_clicked(self):
        temp_address = self._ui.radio_address.text()
        temp_power = self._ui.radio_power.text()
        if temp_address == '' or temp_power == '':
            QMessageBox.critical(self, 'Message', '网络地址或功率为空')
            return
        if not temp_address.isdigit() or not temp_power.isdigit():
            QMessageBox.critical(self, 'Message', '网络地址或功率格式错误')
            return
        temp_mode = 0
        if self._ui.radio_client.isChecked():
            temp_mode = 2
        temp_baud_rate_index = self._ui.radio_baud_rate.currentIndex()
        # 修改配置
        if temp_mode != self._mode:
            command_queue.push('ats101=' + str(temp_mode))
        if temp_baud_rate_index != self._baud_rate_index:
            command_queue.push('ats102=' + str(temp_baud_rate_index))
        if temp_address != self._address:
            command_queue.push('ats104=' + temp_address)
        if temp_power != self._power:
            command_queue.push('ats108=' + temp_power)

        if command_queue.is_empty():
            now = time.strftime('%H:%M:%S', time.localtime())
            self._ui.txt_receive.append('[' + now + ']\t' + '参数未发生变化')
            return
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
                        self._ui.tabWidget.setEnabled(True)
                        self._ui.btn_config_mode.setEnabled(True)
                    else:
                        QMessageBox.critical(self, 'Message', '没有可用的串口或当前串口被占用')
                except:
                    QMessageBox.critical(self, 'Message', '串口异常')
        else:
            if self._ui.btn_config_mode.text() == '保存并退出':
                reply = QMessageBox.question(self, 'Message', '是否保存配置信息并退出配置模式？',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self._ui.btn_config_mode.click()
                    QTimer.singleShot(1000, self.close_port)  # 等待1s再关闭
                    return
            self.close_port()

    def close_port(self):
        self._serial.close()
        self._ui.btn_connect.setText('连接')
        self._ui.btn_connect.setStyleSheet("color:black;")
        self._ui.tabWidget.setEnabled(False)
        self._ui.btn_config_mode.setEnabled(False)

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

    # 接收数据(定时器开启以100ms内最后一次启动为准)
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
        if self._current_cmd == '':
            return
        if not self._check_timer.isActive():
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
        QMessageBox.critical(self, 'Message', '指令执行超时 指令：' + self._current_cmd)

    def _read_timeout(self):
        # 关闭定时器
        if self._read_timer.isActive():
            self._read_timer.stop()
        if self._check_timer.isActive():
            self._check_timer.stop()

        if not self._check_buf(self._buf):
            self._retry_count += 1
            if self._retry_count > 3:
                QMessageBox.critical(self, 'Message', '尝试重试三次失败 指令：' + self._current_cmd)
            else:
                self._execute_current_cmd()
            return
        self._out_result(self._buf)
        # print(self._buf)
        # print(str(self._buf, encoding='utf-8'))
        self._buf.clear()
        # 重试次数清零
        _retry_count = 0
        # 执行其他指令
        if not command_queue.is_empty():
            self._update_current_cmd()
            self._execute_current_cmd()

    # 检查返回值是否正确
    def _check_buf(self, buf):
        if self._current_cmd == '+++':
            if buf == b'\r\nNO CARRIER\r\nOK\r\n':
                return True
        else:
            buf_str = str(buf, encoding='utf-8')
            if buf_str.startswith('CONNECT') or buf_str.startswith(self._current_cmd):
                return True
            elif buf_str.startswith(self._current_cmd) and buf_str.endswith('OK\r\n'):
                return True
        return False

    # 结果输出
    def _out_result(self, buf):
        now = time.strftime('%H:%M:%S', time.localtime())
        result_str = str(buf, encoding='utf-8')
        if self._current_cmd == '+++':
            result_str = '进入配置模式'
        elif self._current_cmd == 'at&v':
            result_str = '刷新配置信息'
            # 刷新界面
            self._solve_info(buf)
        elif self._current_cmd == 'at&wa':
            result_str = '保存并退出'
            buf_str = str(buf, encoding='utf-8')
            if buf_str.startswith('CONNECT'):
                result_str = '配对成功'
        elif self._current_cmd.startswith('ats101'):
            if self._current_cmd.split('=')[1] == '0':
                result_str = '设置为主站<server>'
            else:
                result_str = '设置为从站<client>'
            self._mode = int(self._current_cmd.split('=')[1])
        elif self._current_cmd.startswith('ats102'):
            result_str = '设置波特率为：' + self._ui.radio_baud_rate.currentText()
            self._baud_rate_index = self._ui.radio_baud_rate.currentText()
        elif self._current_cmd.startswith('ats104'):
            result_str = '设置网络地址为：' + self._ui.radio_address.text()
            self._address = self._ui.radio_address.text()
        elif self._current_cmd.startswith('ats108'):
            result_str = '设置功率为：' + self._ui.radio_power.text()
            self._power = self._ui.radio_power.text()
        else:
            pass
        self._ui.txt_receive.append('[' + now + ']\t' + result_str)

    # 解析电台配置
    def _solve_info(self, buf):
        buf_str = str(buf, encoding='utf-8')
        # S101(主从站)
        ret = re.search(r'(S101)=(\d+)', buf_str)
        if ret:
            self._mode = int(ret.group(2))
            if self._mode == 0:
                self._ui.radio_server.setChecked(True)
            else:
                self._ui.radio_client.setChecked(True)

        # S102(波特率)
        ret = re.search(r'(S102)=(\d+)', buf_str)
        if ret:
            self._baud_rate_index = int(ret.group(2))
            self._ui.radio_baud_rate.setCurrentIndex(self._baud_rate_index)

        # S104(网络地址)
        ret = re.search(r'(S104)=(\d+)', buf_str)
        if ret:
            self._address = ret.group(2)
            self._ui.radio_address.setText(self._address)

        # S108(输出功率)
        ret = re.search(r'(S108)=(\d+)', buf_str)
        if ret:
            self._power = ret.group(2)
            self._ui.radio_power.setText(self._power)
