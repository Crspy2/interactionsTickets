from pymongo import MongoClient


class DBClient:
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client['dev']

    def create_guild(self, guild_id: str, owner_id: str):
        settings_collection = self.db[guild_id]
        settings = {
            "admins": [owner_id],
            "support": [],
            "transcript_channel": None,
            "ticket_limit": 1,
            "default_category": None,
            "claim": False,
            "use_threads": False,
            "ticket_number": 1,
            "welcome_message": """Thank you for contacting support.
Please describe your issue (and provide an invite to your server if applicable) and wait for a response.""",
            "panels": [],
        }
        settings_collection.insert_one(settings)

    def get_guild_settings(self, guild_id: str):
        settings_collection = self.db[guild_id]
        settings = settings_collection.find_one()
        return settings

    def update_guild_settings(self, guild_id: str, **kwargs):
        settings_collection = self.db[guild_id]
        settings_collection.update_one({}, {"$set": kwargs})

    def search_guild_settings(self, guild_id: str, query):
        settings_collection = self.db[guild_id]
        settings = settings_collection.find_one(query)
        return settings

    def delete_guild(self, guild_id: str):
        settings_collection = self.db[guild_id]
        settings_collection.delete_one({})

    def create_ticket(self, guild_id: str, owner_id: str, first_msg: str, category_id: str, open_time: str):
        tickets_collection = self.db[guild_id]
        ticket = {
            "creator": owner_id,
            "id": self.db[guild_id]['ticket_number'],
            "first_message": first_msg,
            "category": category_id,
            "open_time": open_time,
            "claimed_by": None,
            "closed_by": None,
            "closed_reason": None,
            "support_roles": [],
            "added_users": [],
            "open": True,
        }
        tickets_collection.insert_one(ticket)

    def get_ticket(self, guild_id: str, owner_id: str):
        tickets_collection = self.db[guild_id]
        ticket = tickets_collection.find_one({"creator": owner_id})
        return ticket

    def update_ticket(self, guild_id: str, owner_id: str, **kwargs):
        tickets_collection = self.db[guild_id]
        tickets_collection.update_one({"creator": owner_id}, {"$set": kwargs})

    def delete_ticket(self, guild_id: str, owner_id: str):
        tickets_collection = self.db[guild_id]
        tickets_collection.delete_one({"creator": owner_id})

    def is_user_admin(self, guild_id: str, user_id: str) -> bool:
        settings_collection = self.db[guild_id]
        settings = settings_collection.find_one()
        if settings and "admins" in settings and user_id in settings["admins"]:
            return True
        else:
            return False

    def is_user_support(self, guild_id: str, user_id: str) -> bool:
        settings_collection = self.db[guild_id]
        settings = settings_collection.find_one()
        if settings and "support" in settings and user_id in settings["support"]:
            return True
        else:
            return False