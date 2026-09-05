class Session:
    def __init__(self):
        self._current_user = None

    def login(self, user):
        self._current_user = {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }

    def logout(self):
        self._current_user = None

    def get_current_user(self):
        return self._current_user

    def is_logged_in(self):
        return self._current_user is not None