import requests
import json

URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-type": "application/json"}


def preload_model(model_name: str = "llama3") -> bool:
    print(f"Running model preloader for {model_name}...")
    data = {"model": model_name, "keep_alive": "5m"}

    response = requests.post(URL, data=json.dumps(data), headers=HEADERS)

    return True if response.status_code == 200 else False


if __name__ == "__main__":
    print(preload_model())
