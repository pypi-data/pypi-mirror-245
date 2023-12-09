import requests
import os
import threading
from playsound import playsound
import re

def generate_url(text, lang):
    # URL-encode the text
    encoded_text = requests.utils.quote(text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={encoded_text}"

def play_and_remove_file(file_path):
    playsound(file_path)
    os.remove(file_path)

def play_tts(text, lang):
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    for sentence in sentences:
         # Generate the URL for each sentence
        url = generate_url(sentence, lang)

        # Send a request to get the audio for each sentence
        response = requests.get(url)

        if response.status_code == 200:
            # Save the audio to a temporary file
            temp_audio_file = "temp_tts.mp3"
            with open(temp_audio_file, "wb") as audio_file:
                audio_file.write(response.content)

            # Create a thread to play the sound and then remove the file
            play_thread = threading.Thread(target=play_and_remove_file, args=(temp_audio_file,))
            play_thread.start()
            play_thread.join()  # Wait for the audio to finish playing before continuing

# Example usage
# play_tts("Наравно, ево трећег корака: Загреј маслиново уље у тигању на средње јакој ватри, додај ситно исецкан бели лук, чили и оригано, и пржи док бели лук не постане златан, отприлике 2 минута. Ту настављаш процес прављења соса за пасту. Срећно!", "sr")
