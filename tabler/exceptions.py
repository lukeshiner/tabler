class ExtensionNotRecognised(Exception):

    def __init__(self, extension):
        super().__init__("Extension '{}' not recognised.".format(extension))
