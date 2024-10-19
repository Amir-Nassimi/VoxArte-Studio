import torch
from pyannote.audio import Pipeline


class SpeakerDiarization:
    def __init__(self, model_name: str, access_token: str):
        self.pipeline = Pipeline.from_pretrained(
            model_name,
            use_auth_token=access_token
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.pipeline.to(self.device)

    def process_audio(self, audio_file: str):
        diarization = self.pipeline(audio_file)

        results = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start = turn.start
            stop = turn.end
            
            # Ignore segments shorter than 0.5 seconds
            if (stop - start) < 0.5:
                continue
    
            result = {
                "start": start,
                "stop": stop,
                "speaker": f"speaker_{speaker}"
            }
            results.append(result)

        return results
