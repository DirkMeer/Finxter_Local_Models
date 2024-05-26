from transformers import pipeline
import scipy
import uuid


synthesizer = pipeline("text-to-audio", "facebook/musicgen-large")

music = synthesizer(
    "Gangster rap beat with a piano riff",
    forward_params={"do_sample": True},
)

scipy.io.wavfile.write(
    f"musicgen_out_{uuid.uuid4()}.wav", rate=music["sampling_rate"], data=music["audio"]
)
