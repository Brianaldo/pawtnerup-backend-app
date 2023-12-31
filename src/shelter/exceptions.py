from _common.exceptions import ConflictException, NotFoundException


class ShelterNotFound(NotFoundException):
    pass


class ShelterAlreadyExists(ConflictException):
    pass
