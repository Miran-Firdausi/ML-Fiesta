from googletrans import Translator


def translate_to_english(kannada_text):
    translator = Translator()
    translated_text = translator.translate(kannada_text, src="kn", dest="en")
    return translated_text.text
