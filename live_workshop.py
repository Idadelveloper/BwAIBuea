import os
import asyncio
import pyaudio
from dotenv import load_dotenv

from google import genai
from google.genai import types
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()


load_dotenv()

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024
MODEL = "models/gemini-2.0-flash-live-001"

# Function declaration JSON schema for Gemini / function calling
get_gdg_buea_organizers_declaration = {
    "name": "get_gdg_buea_organizers",
    "description": "Returns a list of all GDG Buea organizers and their roles.",
    "parameters": {
        "type": "object",
        "properties": {
            # No parameters required for this function
        },
        "required": []
    }
}

def get_gdg_buea_organizers() -> dict:
    """
    Returns a dictionary with all GDG Buea organizers and their roles.

    Returns:
        dict: A dictionary containing a list of organizers with 'name' and 'role' keys.
    """
    return {
        "organizers": [
            {"name": "Fongoh Tayong", "role": "GDG Organizer and Digital Renter"},
            {"name": "Collins Chuwa", "role": "Software Engineer & DevOps"},
            {"name": "Gilda Nyenti", "role": "Organizer"},
            {"name": "Mamoudou Yaya", "role": "Organizer"},
            {"name": "Atem Randy Asong", "role": "Organizer"},
            {"name": "Shekinah Manyi", "role": "Organizer"},
            {"name": "Tambe Salome", "role": "Organizer"},
            {"name": "Derick Alangi", "role": "Senior Software Engineer at Wikimedia Foundation"}
        ]
    }

tools = types.Tool(function_declarations=[get_gdg_buea_organizers_declaration])

# Setup client
client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GOOGLE_API_KEY"),
)

CONFIG = types.LiveConnectConfig(
system_instruction=(
        "You are an assistant knowledgeable about GDG Buea and its events. "
        "If asked about the organizers of GDG Buea, call the function 'get_gdg_buea_organizers'."
    ),
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        language_code="en-US",
        voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck"))
    ),
    tools=[tools],
)

pya = pyaudio.PyAudio()

class AudioChat:
    def __init__(self):
        self.audio_out_queue = asyncio.Queue()

    async def stream_microphone(self, session):
        mic_info = pya.get_default_input_device_info()
        stream = await asyncio.to_thread(pya.open,
                                         format=FORMAT,
                                         channels=CHANNELS,
                                         rate=SEND_SAMPLE_RATE,
                                         input=True,
                                         frames_per_buffer=CHUNK_SIZE)

        try:
            while True:
                data = await asyncio.to_thread(stream.read, CHUNK_SIZE, exception_on_overflow=False)
                await session.send(input={"data": data, "mime_type": "audio/pcm"})
        finally:
            stream.stop_stream()
            stream.close()

    async def play_audio(self):
        output = await asyncio.to_thread(pya.open,
                                         format=FORMAT,
                                         channels=CHANNELS,
                                         rate=RECEIVE_SAMPLE_RATE,
                                         output=True)
        while True:
            data = await self.audio_out_queue.get()
            await asyncio.to_thread(output.write, data)

    async def receive_from_gemini(self, session):
        while True:
            turn = session.receive()
            async for response in turn:
                if response.data:
                    self.audio_out_queue.put_nowait(response.data)
                if response.text:
                    print("Text:", response.text)

    async def run(self):
        async with client.aio.live.connect(model=MODEL, config=CONFIG) as session, asyncio.TaskGroup() as tg:
            tg.create_task(self.stream_microphone(session))
            tg.create_task(self.receive_from_gemini(session))
            tg.create_task(self.play_audio())

if __name__ == "__main__":
    asyncio.run(AudioChat().run())
