import os
from dotenv import load_dotenv, find_dotenv
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import azure.cognitiveservices.speech as speechsdk
from .utility import translate_to_english


load_dotenv(find_dotenv())

import threading
from sentence_transformers import SentenceTransformer
import faiss


class ResourceManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if ResourceManager._instance is not None:
            raise Exception("This class is a singleton!")

        current_file_directory = os.path.dirname(os.path.abspath(__file__))

        # Resolve file paths dynamically
        main_index_path = os.path.join(
            current_file_directory, "faiss_index", "faiss_index_4.bin"
        )
        main_chunks_path = os.path.join(
            current_file_directory, "faiss_index", "faiss_index_4_texts3.txt"
        )
        side_index_path = os.path.join(
            current_file_directory, "faiss_index", "faiss_index_side.bin"
        )
        side_chunks_path = os.path.join(
            current_file_directory, "faiss_index", "faiss_index_side.txt"
        )

        self.main_index = faiss.read_index(main_index_path)
        self.main_chunks = self._load_chunks(main_chunks_path)
        self.side_index = faiss.read_index(side_index_path)
        self.side_chunks = self._load_chunks(side_chunks_path)
        self.labse_model = SentenceTransformer("sentence-transformers/LaBSE")
        self.minilm_model = SentenceTransformer("all-MiniLM-L6-v2")

    @staticmethod
    def get_instance():
        if ResourceManager._instance is None:
            with ResourceManager._lock:
                if ResourceManager._instance is None:
                    ResourceManager._instance = ResourceManager()
        return ResourceManager._instance

    def _load_chunks(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return file.readlines()


class RAGResources:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RAGResources, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Load model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load text corpus and prepare chunks
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_file_directory, "complete_text.txt")
        self.text_corpus = self.load_text_file(file_path)
        self.chunks = self.split_into_chunks(self.text_corpus)

        # Generate embeddings and create FAISS index
        self.embeddings = self.model.encode(self.chunks)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    @staticmethod
    def load_text_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

    @staticmethod
    def split_into_chunks(paragraphs, chunk_size=100):
        chunks = []
        for paragraph in paragraphs:
            words = paragraph.split()
            chunks.extend(
                [
                    " ".join(words[i : i + chunk_size])
                    for i in range(0, len(words), chunk_size)
                ]
            )
        return chunks


def generate_answer(question: str, resource_manager):
    # question_en = translate_to_english(kannada_text=question)
    # relevant_chunks = retrieve_relevant_chunks(query=question_en)
    # context = "\n".join(relevant_chunks)
    # answer = query_llm(prompt=question, context=context)

    # Retrieve relevant chunks from the main index
    main_chunks = retrieve_relevant_chunks(
        question,
        resource_manager.main_index,
        resource_manager.main_chunks,
        resource_manager.labse_model,
    )

    # Retrieve relevant chunks from the side index
    side_chunks = retrieve_relevant_chunks(
        question,
        resource_manager.side_index,
        resource_manager.side_chunks,
        resource_manager.minilm_model,
    )

    # Combine, translate, and query LLM
    combined_chunks = main_chunks + side_chunks
    translated_chunks = [translate_to_english(chunk) for chunk in combined_chunks]
    context = " ".join(translated_chunks)
    answer = query_llm(question, context)

    return answer


def retrieve_relevant_chunks(query, index, chunks, model, top_k=5):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]


# def retrieve_relevant_chunks(query, top_k=5):
#     resources = RAGResources()  # Get the singleton instance
#     query_embedding = resources.model.encode([query])
#     distances, indices = resources.index.search(query_embedding, top_k)
#     return [resources.chunks[i] for i in indices[0]]


def query_llm(prompt, context):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    complete_prompt = f"{context}\n\nQuestion: {prompt}\nRespond with plain unformatted text like a person explaining which will be then fed to a text-to-speech engine:"
    response = model.generate_content([complete_prompt])
    return response.text


def generate_speech_and_viseme_from_text(
    text: str,
    audio_output_file: str = "output.wav",
):
    load_dotenv(find_dotenv())
    speech_key = os.environ["AZURE_SPEECH_API_KEY"]
    service_region = "eastus"

    # Create a speech configuration object
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_language = "kn-IN"
    speech_config.speech_synthesis_voice_name = "kn-IN-SapnaNeural"

    # Create an audio configuration for saving the audio to a file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_output_file)

    # Create a speech synthesizer object
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    viseme_data = []

    def viseme_callback(evt):
        viseme_data.append(
            [evt.audio_offset / 10000, evt.viseme_id]  # Convert to milliseconds
        )

    # capture visemes
    synthesizer.viseme_received.connect(viseme_callback)

    # Synthesize the text
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Text-to-speech conversion successful.")
    else:
        print(f"Text-to-speech conversion failed: {result.reason}")
        return None, None

    return viseme_data
