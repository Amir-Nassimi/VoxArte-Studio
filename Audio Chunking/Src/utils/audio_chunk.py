class AudioChunkProcessor:
    def __init__(self, chunk_duration_sec=0.5):
        self.chunk_duration_ms = chunk_duration_sec * 1000  # Convert to milliseconds

    def process_chunks(self, audio):
        total_length_ms = len(audio)

        for start_ms in range(0, int(total_length_ms), int(self.chunk_duration_ms)):
            end_ms = min(start_ms + self.chunk_duration_ms, total_length_ms)
            chunk = audio[start_ms:end_ms]

            # Save the chunk to a temporary file
            chunk_file = f"Dataset/chunk_{start_ms//1000}_{end_ms//1000}.wav"
            chunk.export(chunk_file, format="wav")

            # os.remove(chunk_file)