from gradio_client import Client
import uuid
import shutil
import os


CLIENT = Client("http://localhost:8888/")
SPEED = 1.0
MAPPING = {
    "EN-Default": {"base_language": "EN", "speaker_id": "EN-Default"},
    "EN-US": {"base_language": "EN", "speaker_id": "EN-US"},
    "EN-BR": {"base_language": "EN", "speaker_id": "EN-BR"},
    "EN-IN": {"base_language": "EN", "speaker_id": "EN_INDIA"},
    "EN-AU": {"base_language": "EN", "speaker_id": "EN-AU"},
    "ES": {"base_language": "ES", "speaker_id": "ES"},
    "FR": {"base_language": "FR", "speaker_id": "FR"},
    "ZH": {"base_language": "ZH", "speaker_id": "ZH"},
    "JP": {"base_language": "JP", "speaker_id": "JP"},
    "KR": {"base_language": "KR", "speaker_id": "KR"},
}


def text_to_speech(text, language="EN-Default"):
    if language in MAPPING:
        base_language = MAPPING[language]["base_language"]
        speaker_id = MAPPING[language]["speaker_id"]
    else:
        raise ValueError(
            f"Language {language} not supported. Please choose one of {MAPPING.keys()}."
        )

    result: str = CLIENT.predict(
        language=base_language,
        speaker=speaker_id,
        text=text,
        speed=SPEED,
        api_name="/synthesize",
    )

    output_path = f"tts_output/{base_language}_{text[:10]}_{uuid.uuid4()}.wav"
    print(result)

    shutil.move(result, os.path.join(os.getcwd(), output_path))

    return output_path


if __name__ == "__main__":
    # Remember the first time you load a model it will take longer so running all of these for the first time may take a bit.
    text = "The field of text-to-speech has seen rapid development recently."
    text_to_speech(text, "EN-Default")
    text_to_speech(text, "EN-US")
    text_to_speech(text, "EN-BR")
    text_to_speech(text, "EN-IN")
    text_to_speech(text, "EN-AU")
    spanish_text = "El campo de la conversión de texto a voz ha experimentado un rápido desarrollo recientemente."
    text_to_speech(spanish_text, "ES")
    french_text = (
        "Le domaine de la synthèse vocale a connu un développement rapide récemment"
    )
    text_to_speech(french_text, "FR")
    chinese_text = "text-to-speech 领域近年来发展迅速"
    text_to_speech(chinese_text, "ZH")
    japanese_text = "テキスト読み上げの分野は最近急速な発展を遂げています"
    text_to_speech(japanese_text, "JP")
    korean_text = "최근 텍스트 음성 변환 분야가 급속도로 발전하고 있습니다."
    text_to_speech(korean_text, "KR")
