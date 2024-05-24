from dataclasses import dataclass, field

import requests
import time


@dataclass
class LeapMusicGenerator:
    api_key: str | None = None
    url: str = "https://api.tryleap.ai/api/v1/music"
    headers: dict[str, str] = field(default_factory=lambda: {
        "accept": "application/json",
        "content-type": "application/json"
    })

    def __post_init__(self):
        self.headers['authorization'] = f"Bearer {self.api_key}"

    def _generate_music(self, prompt, mode, duration):
        payload = {
            "prompt": prompt,
            "mode": mode,
            "duration": duration
        }

        response = requests.post(self.url, json=payload, headers=self.headers)

        if response.status_code == 200:
            job_id = response.json().get('id')
            print(f"Job ID: {job_id}")
            return job_id
        else:
            print("Error:", response.text)
            return None

    def _get_audio_url(self, job_id):
        get_url = f"{self.url}/{job_id}"

        while True:
            result_response = requests.get(get_url, headers=self.headers)
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

    def _download_audio(self, audio_url, path, filename):
        audio_response = requests.get(audio_url)
        with open(f"{path}/{filename}", 'wb') as f:
            f.write(audio_response.content)
        print(f"Music saved as {filename}")

    def generate(self, prompt, mode, duration, path, filename):
        job_id = self._generate_music(prompt, mode, duration)
        if job_id:
            audio_url = self._get_audio_url(job_id)
            if audio_url:
                self._download_audio(audio_url, path, filename)
            else:
                raise ValueError("Failed to get audio URL.")
        else:
            raise ValueError("Failed to generate music - Check the if your API Key is valid.")

    def set_api_key(self, api_key):
        self.api_key = api_key
        self.headers['authorization'] = f"Bearer {self.api_key}"

