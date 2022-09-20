class EmptyFieldException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f"Empty field is not Valid!"

class NotSelectedFolder(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f"You didn't select a folder!"

