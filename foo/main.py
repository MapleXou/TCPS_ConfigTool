from PyQt5.QtWidgets import QApplication
from foo.tcps_config_tool import Window
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
