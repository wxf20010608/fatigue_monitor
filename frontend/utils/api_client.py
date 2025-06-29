import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def start_recognition(self, image_path=None):
        url = f"{self.base_url}/recognize"
        files = {'file': open(image_path, 'rb')} if image_path else None
        response = requests.post(url, files=files)
        return response.json() if response.status_code == 200 else None

    def clear_history(self):
        url = f"{self.base_url}/clear_history"
        response = requests.post(url)
        return response.status_code == 200

    def get_results(self):
        url = f"{self.base_url}/results"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None

    def exit_system(self):
        url = f"{self.base_url}/exit"
        response = requests.post(url)
        return response.status_code == 200