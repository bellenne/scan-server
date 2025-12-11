import winsound
from pathlib import Path

class AudioPlayer:
    def __init__(self, global_sounds: dict, mode_sounds: dict):
        self.global_sounds = global_sounds
        self.mode_sounds = mode_sounds

    def play_async(self, path):
        if not path:
            return
        winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)

    def play_sync(self, path):
        if not path:
            return
        # SND_SYNC == 0, поэтому просто не используем SND_ASYNC
        winsound.PlaySound(str(path), winsound.SND_FILENAME)

    def play_global(self, name: str):
        self.play_async(self.global_sounds.get(name))

    def play_global_sync(self, name: str):
        self.play_sync(self.global_sounds.get(name))

    def play_mode(self, mode_name: str, sound_type: str):
        mode_cfg = self.mode_sounds.get(mode_name, {})
        self.play_async(mode_cfg.get(sound_type))

    def play_mode_sync(self, mode_name: str, sound_type: str):
        mode_cfg = self.mode_sounds.get(mode_name, {})
        self.play_sync(mode_cfg.get(sound_type))
