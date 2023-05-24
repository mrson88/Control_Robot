import sys
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit,QAction
import PyQt5.QtCore
import pyttsx3
#from PyQt6.QtGui import QAction
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Speech to Text")
        self.setGeometry(100, 100, 800, 600)

        # Create the text box to display the converted text
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.setCentralWidget(self.textbox)

        # Create the "Convert" action
        convert_action = QAction("Convert", self)
        convert_action.setShortcut("Ctrl+R")
        convert_action.triggered.connect(self.convert_speech_to_text)

        # Add the "Convert" action to the main menu
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        file_menu.addAction(convert_action)

        # Initialize the speech recognizer
        self.recognizer = sr.Recognizer()

    def SpeakText(self,command):
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()
    def convert_speech_to_text(self):
        r = sr.Recognizer()
        # Use the default microphone as the audio source
        # with sr.Microphone() as source:
        #     print("Listening...")
        #     # Adjust the energy threshold to account for ambient noise
        #     self.recognizer.adjust_for_ambient_noise(source)
        #     # Listen for speech and convert it to text
        #     audio = self.recognizer.listen(source)
        #     try:
        #         text = self.recognizer.recognize_google(audio)
        #         self.textbox.setPlainText(text)
        #         print("Converted text:", text)
        #     except sr.UnknownValueError:
        #         print("Unable to recognize speech")
        #     except sr.RequestError as e:
        #         print("Request error:", e)
        # while (1):

            # Exception handling to handle
            # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("Did you say ", MyText)
                self.SpeakText(MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
