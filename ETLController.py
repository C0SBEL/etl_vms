from userExtractor import UserExtractor

class ETLController:
    def __init__(self, extractor):
        self.extractor = extractor

    def run(self):
        data = self.extractor.get_users()
        print(f"Se han extraído {len(data.get('results', []))} usuarios.")
        return data

if __name__ == "__main__":
    extractor = UserExtractor("https://randomuser.me/api/", num_users=1000)
    controller = ETLController(extractor)
    controller.run()
