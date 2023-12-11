class Status(object):

    def __init__(self, errorMessage=None):
        self.errorMessage = errorMessage

    @staticmethod
    def ok():
        return Status()

    @staticmethod
    def error(errorMessage):
        return Status(errorMessage)
