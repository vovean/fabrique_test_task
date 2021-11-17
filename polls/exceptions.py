from rest_framework.exceptions import APIException


class EndDateBeforeStartException(APIException):
    status_code = 400
    default_detail = "End date of the poll cannot be before its start date"
    default_code = "end_date_before_start"


class NotEnoughAnswersException(APIException):
    status_code = 400
    default_detail = "Not all questions were answered"
    default_code = "not_enough_answers"


class AnswersNotFoundException(APIException):
    status_code = 400
    default_detail = "Answers not provided"
    default_code = "answers_not_found"


class InvalidUserIDException(APIException):
    status_code = 400
    default_detail = "Provided user_id is invalid. It should be a numeric value"
    default_code = "invalid_user_id"


class UserIDNotProvidedException(APIException):
    status_code = 400
    default_detail = "Failed to find user_id key"
    default_code = "user_id_not_provided"


class InvalidAnswerFormatException(APIException):
    status_code = 400
    default_detail = "Each answer should be string or int"
    default_code = "invalid_answer_format"


class IdInCreateRequestException(APIException):
    status_code = 400
    default_detail = "You cannot specify id when creating new object"
    default_code = "id_specified_in_create"
