class notificationMaker():
    def __init__(self):
        self.types = [
            NotifcationType("hygiene", "bathroom", "Clean your bathroom",
                            "Go clean your bathroom, it's disguisting"),

            NotifcationType("hygiene", "sheets", "Change your sheets",
                            "You really need to change your sheets today"),

            NotifcationType("hygiene", "house", "Clean your house",
                            "You really need to clean your house"),

            NotifcationType("hygiene", "kitchen", "Clean your kitchen",
                            "You need to clean your kitchen"),

            NotifcationType("hygiene", "dishes",
                            "Do the dishes", "Go do your dishes!"),

            NotifcationType("hygiene", "vacuum", "Go vacuum the house",
                            "You really need to vacuum your house")
        ]

    def get_notification_message(self, type, sub_type=None, title=None, message=None):
        for c_type in self.types:
            if c_type.type == type:
                return [c_type.title, c_type.message]


class NotifcationType:
    def __init__(self, type, sub_type=None, title=None, message=None):
        self.type = type
        if sub_type:
            self.sub_type = sub_type
        self.title = title
        self.message = message
