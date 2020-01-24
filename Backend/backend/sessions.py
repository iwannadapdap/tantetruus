class TtSession():
    def __init__(self, session_list):
        self.admin = session_list.get("admin", None)
        self.admin_username = session_list.get("admin_username", None)
        self.admin_password = session_list.get("admin_password", None)

    def update_ses(self, session_list):
        session_list["admin"] = self.admin
        session_list["admin_username"] = self.admin_username
        session_list["admin_password"] = self.admin_password

    def login_admin(self, admin_email, admin_password):
        self.admin_username = admin_email
        self.admin_password = admin_password
        self.admin = True

    def logout_admin(self):
        self.admin_username = None
        self.admin_password = None
        self.admin = None
