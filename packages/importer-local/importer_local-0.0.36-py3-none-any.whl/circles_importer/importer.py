from circles_local_database_python.connector import Connector
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from user_context_remote.user_context import UserContext

load_dotenv()

IMPORTER_LOCAL_PYTHON_COMPONENT_ID = 114
IMPORTER_LOCAL_PYTHON_COMPONENT_NAME = 'importer-local-python-package'

logger_code_init = {
    'component_id': IMPORTER_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': IMPORTER_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'developer_email': 'idan.a@circlez.ai'
}
logger = Logger.create_logger(object=logger_code_init)


class Importer(GenericCRUD):
    def __init__(self):
        super().__init__(default_schema_name="importer", default_table_name="importer_table",
                         default_view_table_name="importer_view", default_id_column_name="id")
        self.user = UserContext()
        connection = Connector.connect("location")
        self.cursor = connection.cursor()

    def insert(self, data_source_id: int, location_id: int, entity_type_id: int, entity_id: int, url: str,
               user_id: int) -> int:
        object1 = {
            'data_source_id': data_source_id,
            'location_id': location_id,
            'entity_type_name': entity_type_id,
            'entity_id': entity_id,
            'url': url,
            'user_id': user_id
        }
        logger.start(object=object1)
        try:

            country_id = self._get_country(location_id)
            data_json = {
                "data_source_id": data_source_id,
                "country_id": country_id,
                "entity_type_id": entity_type_id,
                "entity_id": entity_id,
                "url": url,
                "created_user_id": user_id  # TODO should we use self.user.get_effective_user_id()
            }
            importer_id = super().insert(data_json=data_json)
            if importer_id is None or importer_id == -1:
                raise Exception("insert importer record failed")

            # view logger_local.end at the end of the function
            logger.end("add importer record succeeded", object={'importer_id': importer_id})
            return importer_id
        except Exception as e:
            logger.exception(object=e)
            raise

    def _get_country(self, location_id):
        self.cursor.execute("SELECT country_id FROM location.location_table WHERE location_id = %s", (location_id,))
        country_id = self.cursor.fetchone()[0]
        return country_id

