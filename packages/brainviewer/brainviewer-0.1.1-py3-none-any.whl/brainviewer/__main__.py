# -*- coding: UTF-8 -*-
"""
@Project ：BrainViewer 
@File    ：main.py
@Author  ：Barry
@Date    ：2022/4/14 2:31 
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from gui.viewer import BrainViewer
    from gui.splash import SplashPanel


    app = QApplication(sys.argv)
    splash = SplashPanel()
    app.processEvents()
    viewer = BrainViewer()
    splash.finish(viewer)
    splash.deleteLater()
    viewer.showMaximized()
    viewer.show()
    sys.exit(app.exec_())
