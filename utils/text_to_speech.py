import asyncio
import edge_tts
import pygame
import tempfile
import os


async def speak_edge_tts(text, voice="en-US-AriaNeural", rate="+0%", pitch="+0Hz"):
    """
    High-quality TTS using Microsoft Edge voices

    Popular voices:
    - en-US-AriaNeural (female)
    - en-US-GuyNeural (male)
    - en-GB-SoniaNeural (British female)
    - en-AU-NatashaNeural (Australian female)
    """
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)

        # Create a uniquely named temp file and close it before Edge-TTS writes
        # to it. On Windows, keeping the file open will prevent other writers
        # from opening the same path.
        fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

        try:
            await communicate.save(tmp_path)

            # Play using pygame
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            pygame.mixer.quit()
        finally:
            # Ensure we remove the temp file
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    except Exception as e:
        print(f"Edge-TTS Error: {e}")
        print("Text:", text)


def speak_text(text, voice="en-US-GuyNeural", rate="+0%", pitch="+0Hz"):
    """Synchronous wrapper for Edge-TTS"""
    asyncio.run(speak_edge_tts(text, voice, rate, pitch))
