class DatabaseError(BaseException):
    pass


class DatabaseSyntaxError(DatabaseError):
    pass


class DatabaseStateError(DatabaseError):
    pass
