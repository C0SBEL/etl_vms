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
    def top_5_ancient (self, top_n: int = 5 ):
        valid_users = [user for user in self.data if 'registered' in user]
        ordered_users = sorted( valid_users, key=lambda user: user['registered']['age'],
            reverse=True)
        top_users = ordered_users[:top_n]
        formatted_top_users = []
        for user in top_users:
            formatted_top_users.append({
                'nombre_completo': f"{user['name']['first']} {user['name']['last']}",
                'email': user['email'],
                'antiguedad_años': user['registered']['age'],
                'fecha_registro': user['registered']['date']
            })
        return formatted_top_users

    def transform(self):
        return {
            "average_registered_age": self.average_registered_age(),
            "gender_distribution": self.gender_distribution(),
            "total_users": len(self.data),
            "top_5_ancient": self.top_5_ancient(top_n=5)
        }
