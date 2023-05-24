import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    print("\n")



for voice in voices:
    if "female" in voice.name.lower():
        female_voice = voice
        break

if female_voice:
    engine.setProperty('voice', female_voice.id)
else:
    print("No female voice found. Using default voice.")

voice_id = 'vietnam'  # Replace <voice_id> with the desired voice ID
engine.setProperty('voice', voice_id)
speech_rate = 150  # Adjust the speech rate as needed
engine.setProperty('rate', speech_rate)
engine.say("xin chào tôi tên là an.")
engine.runAndWait()


