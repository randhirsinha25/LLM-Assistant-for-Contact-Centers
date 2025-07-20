from prompt import response_type_prompt,get_user_input
import openai
# Set your OpenAI API key
openai.api_key = "enter your openai Key"

def get_prompt(type,transcript):
    response_prompt = response_type_prompt[type]
    prompt = get_user_input(type) + response_prompt
    return prompt


def get_openai_response(prompt, model="gpt-4-0613", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature)
    return response.choices[0].message['content']
def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")

    # Whisper model is used for transcription under the hood (GPT-4o-compatible)
    transcript = openai.Audio.transcribe(
        model="whisper-1",  # GPT-4o uses this Whisper backend for audio
        file=audio_file
    )

    return transcript['text']
