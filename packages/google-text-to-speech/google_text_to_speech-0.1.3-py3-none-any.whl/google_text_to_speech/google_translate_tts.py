import requests
import os
import threading
from playsound import playsound
import re
import tempfile

SPLIT_POINTS = [
    ",",
    ";",
    " i ",
    " ali ",
    " ili ",
    " međutim ",
    " zato ",
    " jer ",
    " kao ",
    " dok ",
    " kada ",
]


def generate_url(text, lang):
    encoded_text = requests.utils.quote(text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={encoded_text}"


def play_and_remove_file(file_path):
    playsound(file_path)
    os.remove(file_path)


def split_long_sentence(sentence, max_length=200):
    parts = []
    current_part = ""
    current_length = 0

    words = sentence.split()

    for word in words:
        if current_length + len(word) + 1 > max_length:
            # Pronalazimo poslednju tačku za podelu u trenutnom delu
            last_split_point = max(
                current_part.rfind(split_point) for split_point in SPLIT_POINTS
            )
            if last_split_point > 0:
                # Delimo po poslednjoj tački za podelu
                parts.append(current_part[:last_split_point].strip())
                current_part = current_part[last_split_point:].strip() + " "
                current_length = len(current_part)
            else:
                # Ako nema tačke za podelu, jednostavno delimo ovde
                parts.append(current_part.strip())
                current_part = ""
                current_length = 0

        current_part += word + " "
        current_length += len(word) + 1

    if current_part:
        parts.append(current_part.strip())

    return parts


def split_text(text, max_length=200):
    sentences = re.split(r"(?<=[.!?]) +", text)
    parts = []

    for sentence in sentences:
        if len(sentence) <= max_length:
            parts.append(sentence)
        else:
            parts.extend(split_long_sentence(sentence, max_length))

    return parts


def play_tts(text, lang):
    parts = split_text(text, max_length=200)

    for part in parts:
        url = generate_url(part, lang)
        response = requests.get(url)

        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
                audio_file.write(response.content)
                temp_audio_file = audio_file.name

            play_thread = threading.Thread(
                target=play_and_remove_file, args=(temp_audio_file,)
            )
            play_thread.start()
            play_thread.join()
        else:
            print(f"Error: Unable to fetch audio for part: {part}")


# Example usage
"""play_tts(
    "Наравно, ево трећег корака: Загреј маслиново уље у тигању на средње јакој ватри, додај ситно исецкан бели лук, чили и оригано, и пржи док бели лук не постане златан, отприлике 2 минута. Ту настављаш процес прављења соса за пасту. Срећно!",
    "sr",
)"""
