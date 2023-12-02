from _common.exceptions import ConflictException, NotFoundException


class AdopterNotFound(NotFoundException):
    pass


class AdopterAlreadyExists(ConflictException):
    pass
