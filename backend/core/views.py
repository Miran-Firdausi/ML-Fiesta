import os
import json
import uuid
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .functionalities import (
    ResourceManager,
    generate_speech_and_viseme_from_text,
    generate_answer,
)


@api_view(["POST"])
def get_tts(request: HttpRequest):
    text = request.data.get("text")

    audio_output_file = os.path.join(
        settings.MEDIA_ROOT, "temp_assets", f"{uuid.uuid4()}.wav"
    )
    try:
        visemes = generate_speech_and_viseme_from_text(
            text=text,
            audio_output_file=audio_output_file,
        )

        with open(audio_output_file, "rb") as audio_file:
            if audio_file is None:
                return Response(
                    {"error": "Text-to-speech synthesis failed"}, status=500
                )

            response = HttpResponse(audio_file.read(), content_type="audio/wav")

            # Set headers for the response
            response["Content-Disposition"] = "inline; filename=tts.wav"
            response["visemes"] = json.dumps(
                visemes
            )  # Include the viseme data as JSON in a header

        return response
    finally:
        # Clean up temporary file
        # if os.path.exists(audio_output_file):
        #     os.remove(audio_output_file)
        pass


@api_view(["POST"])
def get_answer(request: HttpRequest):
    question = request.data.get("question")

    if not question:
        return Response(
            {"error": "Question parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cache_key = f"response_{question}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return Response({"answer": cached_response})

    resource_manager = ResourceManager.get_instance()

    answer = generate_answer(question, resource_manager)

    if answer:
        cache.set(cache_key, answer, timeout=3600)
        return Response({"answer": answer}, status=status.HTTP_200_OK)

    return Response(
        {"error": "There was an generating an answer"},
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
