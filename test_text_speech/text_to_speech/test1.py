import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Tìm giọng nữ tiếng Việt
for voice in voices:
    print(voice.name.lower())
    if "vietnam" in voice.name.lower() and "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('voice', 'asia/vi+f3')
# Sử dụng pyttsx3 để phát âm một đoạn văn bằng giọng nữ tiếng Việt
engine.say("Xin chào, đây là giọng nữ tiếng Việt!")
engine.runAndWait()
