import sys

from PyQt6.QtWidgets import QApplication, QWidget
from Text_UI import Ui_Form
from PyQt6.QtTextToSpeech import QTextToSpeech




class Window(QWidget):
    def __init__(self):
        super().__init__()


        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.engine = None
        engineNames = QTextToSpeech.availableEngines()

        self.ui.pushButton.clicked.connect(self.say)

        if len(engineNames) > 0:
            engineName = engineNames[0]
            self.engine = QTextToSpeech(engineName)
            self.engine.stateChanged.connect(self.stateChanged)

            self.voices = []

            for voice in self.engine.availableVoices():
                self.voices.append(voice)
                self.ui.comboBox.addItem(voice.name())
        else:
            self.ui.pushButton.setEnabled(False)


    def say(self):
        self.ui.pushButton.setEnabled(False)
        self.engine.setVoice(self.voices[self.ui.comboBox.currentIndex()])
        self.engine.setVolume(float(self.ui.horizontalSlider.value() / 100))
        self.engine.say(self.ui.lineEdit.text())


    def stateChanged(self, state):
        if(state == QTextToSpeech.State.Ready):
            self.ui.pushButton.setEnabled(True)


app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())