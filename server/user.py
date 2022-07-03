
class User:
    """
    Represents a user who connects to chat server. Holds their name, client socket, and IP address.
    """
    def __init__(self, client, addr):
        self.client = client
        self.addr = addr
        self.name = None

    def set_name(self, name):
        """
        Sets the user's name.
        :params name: str
        :return: None
        """
        self.name = name

    def __repr__(self):
        return f"User({self.name}, {self.client}, {self.addr})"