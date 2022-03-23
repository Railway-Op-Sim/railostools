
class ParsingError(Exception):
    """Exceptions relating to the parsing of strings"""
    def __init__(self, msg) -> None:
        super().__init__(msg)


class IOError(Exception):
    """Exceptions relating to the writing/reading of files"""
    def __init__(self, msg) -> None:
        super().__init__(msg)


class MetadataError(Exception):
    """Exceptions relating to project metadata"""
    def __init__(self, msg) -> None:
        super().__init__(msg)
