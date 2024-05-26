from dataclasses import dataclass, field

import requests
import time


@dataclass
class LeapMusicGenerator:
    _api_key: str | None = None  # API Key for the Leap Music API
    _url: str = "https://api.tryleap.ai/api/v1/music"  # URL for the Leap Music API
    _headers: dict[str, str] = field(default_factory=lambda: {
        "accept": "application/json",
        "content-type": "application/json"
    })  # Headers for the API request

    def __post_init__(self):
        self._headers['authorization'] = f"Bearer {self._api_key}"

    def _generate_music(self, prompt: str, mode: str, duration: int) -> str | None:
        payload = {
            "prompt": prompt,
            "mode": mode,
            "duration": duration
        }

        response = requests.post(self._url, json=payload, headers=self._headers)

        if response.status_code == 200:
            job_id = response.json().get('id')
            print(f"Job ID: {job_id}")
            return job_id
        else:
            print("Error:", response.text)
            return None

    def _get_audio_url(self, job_id: str) -> str | None:
        get_url = f"{self._url}/{job_id}"

        while True:
            result_response = requests.get(get_url, headers=self._headers)
            result_data = result_response.json()
            if result_data['status'] == 'completed':
                audio_url = result_data['audio_url']
                print(f"Audio URL: {audio_url}")
                return audio_url
            elif result_data['status'] == 'failed':
                print("Generation failed.")
                return None
            else:
                print("Still processing...")
                time.sleep(5)

    def _download_audio(self, audio_url: str, path: str, filename: str) -> None:
        audio_response = requests.get(audio_url)
        with open(f"{path}/{filename}", 'wb') as f:
            f.write(audio_response.content)
        print(f"Music saved as {filename}")

    def generate(self, prompt: str, mode: str, duration: int, path: str, filename: str) -> None:
        job_id = self._generate_music(prompt, mode, duration)
        if job_id:
            audio_url = self._get_audio_url(job_id)
            if audio_url:
                self._download_audio(audio_url, path, filename)
            else:
                raise ValueError("Failed to get audio URL.")
        else:
            raise ValueError("Failed to generate music - Check the if your API Key is valid.")

    def set_api_key(self, api_key: str) -> None:
        self._api_key = api_key
        self._headers['authorization'] = f"Bearer {self._api_key}"
