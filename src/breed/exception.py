from _common.exceptions import ConflictException, NotFoundException


class BreedNotFound(NotFoundException):
    pass


class BreedAlreadyExists(ConflictException):
    pass
