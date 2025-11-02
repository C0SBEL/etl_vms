import requests

class Extractor:
    def __init__(self, base_url, num_users):
        self.base_url = base_url
        self.num_users = num_users

    def get_users(self):
        try:
            response = requests.get(self.base_url, params={"results": self.num_users})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return {}
