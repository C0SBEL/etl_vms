import statistics

class Transformer:
    def __init__(self, data):
        self.data = data.get("results", [])

    def average_registered_age(self):
        registered_ages = [user["registered"]["age"] for user in self.data if "registered" in user]
        if not registered_ages:
            return None
        return statistics.mean(registered_ages)

    def gender_distribution(self):
        genders = [user["gender"] for user in self.data if "gender" in user]
        total = len(genders)
        if total == 0:
            return {}
        return {
            "male": genders.count("male") / total * 100,
            "female": genders.count("female") / total * 100
        }

    def transform(self):
        return {
            "average_registered_age": self.average_registered_age(),
            "gender_distribution": self.gender_distribution(),
            "total_users": len(self.data)
        }
