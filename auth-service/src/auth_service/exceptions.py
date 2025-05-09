
class CodeException(Exception):
    def __init__(self, message: str, status_code: int):
        self.__message = message
        self.__status_code = status_code
        super().__init__(message)

    @property
    def message(self):
        return self.__message

    @property
    def status_code(self):
        return self.__status_code


# 2xx
class OKException(CodeException):  # 200
    def __init__(self, message: str = "Запрос выполнен успешно"):
        super().__init__(message=message, status_code=200)

class AcceptedException(CodeException):  # 202
    def __init__(self, message: str = "Запрос принят, но еще не обработан"):
        super().__init__(message=message, status_code=202)

class NoContentException(CodeException):  # 204
    def __init__(self, message: str = "Нет содержимого"):
        super().__init__(message=message, status_code=204)


# 4xx
class BadRequestException(CodeException):
    def __init__(self, message: str = "Некорректный запрос"):
        super().__init__(message=message, status_code=400)

class UnauthorizedException(CodeException):
    def __init__(self, message: str = "Неавторизованный доступ"):
        super().__init__(message=message, status_code=401)

class PaymentRequiredException(CodeException):
    def __init__(self, message: str = "Требуется оплата"):
        super().__init__(message=message, status_code=402)

class ForbiddenException(CodeException):
    def __init__(self, message: str = "Access denied."):
        super().__init__(message=message, status_code=403)

class NotFoundException(CodeException):
    def __init__(self, message: str = "Recource not found."):
        super().__init__(message=message, status_code=404)

class ConflictException(CodeException):
    def __init__(self, message: str = "Some conflict in db."):
        super().__init__(message=message, status_code=409)


# 5xx
class InternalServerErrorException(CodeException):
    def __init__(self, message: str = "Внутренняя ошибка сервера"):
        super().__init__(message=message, status_code=500)

class NotImplementedException(CodeException):
    def __init__(self, message: str = "Функция не реализована"):
        super().__init__(message=message, status_code=501)

class BadGatewayException(CodeException):
    def __init__(self, message: str = "Ошибка шлюза"):
        super().__init__(message=message, status_code=502)


