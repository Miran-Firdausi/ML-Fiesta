import os
import time
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()


def recognize_from_audio():
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_API_KEY"),
        region="eastus",
    )
    speech_config.speech_recognition_language = "kn-IN"

    audio_config = speechsdk.audio.AudioConfig(
        filename="E:/Programming-Projects/Hackathon/ML-Fiesta/backend/audios/SandalWoodNewsStories_107.wav"
    )
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    recognized_text = []  # List to hold recognized text

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print("CLOSING on {}".format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        pass  # You can skip or add logic here if you need it during recognizing

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text.append(evt.result.text)  # Collect recognized text

    # Register the callbacks
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(
        lambda evt: print("SESSION STARTED: {}".format(evt))
    )
    speech_recognizer.session_stopped.connect(
        lambda evt: print("SESSION STOPPED {}".format(evt))
    )
    speech_recognizer.canceled.connect(lambda evt: print("CANCELED {}".format(evt)))

    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    done = False
    while not done:
        time.sleep(0.5)

    # Join all recognized texts and print them at the end
    print("Recognized Text: ", " ".join(recognized_text))

    speech_recognizer.stop_continuous_recognition()


recognize_from_audio()
