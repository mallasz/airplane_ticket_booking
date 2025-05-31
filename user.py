# Represents a user in the system
class User:
    def __init__(self, user_name, real_name):
        self.user_name = user_name    # Username used for login or identification
        self.real_name = real_name    # Full legal name of the user

    def __str__(self):
        # Returns a readable string representation of the user
        return f"User {self.user_name=} {self.real_name=}"
