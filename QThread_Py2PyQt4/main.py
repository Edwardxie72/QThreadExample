"""
    Edward Xie 09-01-20
    Run in Python2.7 w/ PyQt4
    Constantly print a message into console from a thread, can be stopped at
        any time by either exiting the program or clicking the exit button
    Because messages are processed separately, we can stop at any time
    References:
        https://nikolak.com/pyqt-threading-tutorial/
        https://stackoverflow.com/questions/7311944/
"""

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


# Class ThreadExample
# Basic thread that emites signal to print a message every 1s
# Start thread using .start method
#     myThread = ThreadExample()
#     myThread.start()
#
# Stop thread using .terminate method
#     myThread = ThreadExample()
#     myThread.terminate()
class ThreadExample(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    # Code to execute when running the thread
    def run(self):
        while True:
            self.emit(QtCore.SIGNAL('printLine()'))

            # Using sleep between thread processes
            self.sleep(1)
            # self.msleep(10)
            """
            # Process all events while paused
            # More taxing on memory, more ideal to run with self.msleep()
            #     w/ low time value
            endTime = QtCore.QTime.currentTime().addSecs(1)
            while QtCore.QTime.currentTime() < endTime:
                QtCore.QCoreApplication.processEvents(
                    QtCore.QEventLoop.AllEvents, 1000)
            """


# Class ThreadMain
# Setup basic GUI and process signals
class ThreadMain(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(200, 200)

        self.center = QtGui.QWidget()
        self.setCentralWidget(self.center)

        self.layout = QtGui.QGridLayout()
        self.center.setLayout(self.layout)

        # Set up simple single button which mirrors 'X' button
        self.exitButton = QtGui.QPushButton('Exit')
        self.layout.addWidget(self.exitButton)

        self.startProgram()

    # Main program dealing with threads and signals
    def startProgram(self):
        # Start Thread and check for signals here
        self.getThread = ThreadExample()
        self.getThread.start()

        self.connect(self.getThread, QtCore.SIGNAL('printLine()'),
                     self.printLine)

        # Clicking passes different event object, so call .close method
        #     which will then call .closeEvent with proper event
        self.exitButton.clicked.connect(self.close)

    # Action executed during thread runtime
    def printLine(self):
        print "Look it's a message"

    # Upon stopping, terminate thread before closing window
    def closeEvent(self, event=None):
        # Exit thread
        self.getThread.terminate()
        # Accept event to close properly
        event.accept()
        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = ThreadMain()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()