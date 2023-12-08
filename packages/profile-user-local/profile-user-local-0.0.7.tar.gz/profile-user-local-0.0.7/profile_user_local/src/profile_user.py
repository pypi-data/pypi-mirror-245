from multipledispatch import dispatch
from dotenv import load_dotenv
load_dotenv()
from profile_user_constants import ProfileUserConstants  # noqa: E402
from circles_local_database_python.generic_crud import GenericCRUD   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402


logger = Logger.create_logger(object=ProfileUserConstants.OBJECT_TO_INSERT_CODE)


PROFILE_USER_SCHEMA_NAME = "profile_user"
PROFILE_USER_TABLE_NAME = "profile_user_table"
PROFILE_USER_VIEW_NAME = "profile_user_view"
PROFILE_USER_DEFAULT_ID_COLUMN_NAME = "profile_user_id"


class ProfileUser(GenericCRUD):
    def __init__(self):
        super().__init__(default_schema_name=PROFILE_USER_SCHEMA_NAME, default_table_name=PROFILE_USER_TABLE_NAME,
                         default_view_table_name=PROFILE_USER_VIEW_NAME,
                         default_id_column_name=PROFILE_USER_DEFAULT_ID_COLUMN_NAME)

    @dispatch(int, int, int)
    def insert(self, profile_id: int, user_id: int, is_main: int) -> int:
        logger.start(object={'profile_id': profile_id, 'user_id': user_id, 'is_main': is_main})
        profile_user_id = super().insert(
            data_json={'profile_id': profile_id, 'user_id': user_id, 'is_main': is_main})
        logger.end(object={'profile_user_id': profile_user_id})
        return profile_user_id

    @dispatch(dict)
    def insert(self, data_json: dict[str, int]) -> int:     # noqa: F811
        logger.start(object={'data_json': data_json})
        profile_user_id = super().insert(data_json=data_json)
        logger.end(object={'profile_user_id': profile_user_id})
        return profile_user_id

    @dispatch(int, int, int, int)
    def update(self, profile_user_id: int, profile_id: int, user_id: int, is_main: int) -> None:
        logger.start(object={'profile_user_id': profile_user_id, 'profile_id': profile_id,
                     'user_id': user_id, 'is_main': is_main})
        data_json = {'profile_id': profile_id, 'user_id': user_id, 'is_main': is_main}
        profile_user_id = self.update_by_id(
            id_column_value=profile_user_id, data_json=data_json)
        logger.end()

    def delete_by_id(self, profile_user_id: int) -> None:
        logger.start(object={'profile_user_id': profile_user_id})
        super().delete_by_id(id_column_value=profile_user_id)
        logger.end()

    def select_one_dict_by_id(self, profile_user_id: int) -> dict[str, int]:
        logger.start(object={'profile_user_id': profile_user_id})
        select_clause_value = 'profile_id, user_id, is_main'
        profile_user_dict = super().select_one_dict_by_id(
            select_clause_value=select_clause_value,
            id_column_value=profile_user_id)
        logger.end(object={'profile_user_dict': profile_user_dict})
        return profile_user_dict
