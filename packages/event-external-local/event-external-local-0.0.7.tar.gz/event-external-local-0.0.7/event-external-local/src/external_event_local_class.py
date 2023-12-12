import sys
import os
from dotenv import load_dotenv
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa
from logger_local.Logger import Logger  # noqa
from .external_event_constants import ExternalEventLocalConstants  # noqa
from .external_event import EventExternal  # noqa


object1 = ExternalEventLocalConstants.EXTERNAL_EVENT_LOCAL_CODE_LOGGER_OBJECT
logger = Logger.create_logger(object=object1)


class ExternalEventsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name=ExternalEventLocalConstants.EXTERNAL_EVENT_SCHEMA_NAME,  # noqa
                         default_table_name=ExternalEventLocalConstants.EXTERNAL_EVENT_TABLE_NAME,  # noqa
                         default_id_column_name=ExternalEventLocalConstants.EXTERNAL_EVENT_ID_COLUMN_NAME,  # noqa
                         default_view_table_name=ExternalEventLocalConstants.EXTERNAL_EVENT_VIEW_NAME)  # noqa

    def insert(self, system_id: int, url: str,
               external_event_identifier: str, environment_id: int,
               subsystem_id: int = None) -> int:
        # adding variables validation might be good
        external_event_json = {
            key: value for key, value in {
                'system_id': system_id,
                'subsystem_id': subsystem_id,
                'url': url,
                'external_event_identifier': external_event_identifier,
                'environment_id': environment_id
            }.items() if value is not None
        }
        start_object = external_event_json
        logger.start("start insert external_event", object=start_object)

        external_event_id = super().insert(data_json=external_event_json)
        object_end = {
            'external_event_id': external_event_id
        }
        logger.end("end insert external_event", object=object_end)
        return external_event_id

    def delete_by_external_event_id(self, external_event_id) -> None:
        object_start = {
            'external_event_id': external_event_id
        }
        logger.start("start delete_by_external_event_id", object=object_start)

        super().delete_by_id(id_column_value=external_event_id)
        logger.end("end delete_by_external_event_id external_event")
        return

    def update_by_external_event_id(self, external_event_id: int,
                                    system_id: int = None,
                                    subsystem_id: int = None,
                                    url: str = None,
                                    external_event_identifier: str = None,
                                    environment_id: int = None) -> None:

        external_event_json = {
            key: value for key, value in {
                'system_id': system_id,
                'subsystem_id': subsystem_id,
                'url': url,
                'external_event_identifier': external_event_identifier,
                'environment_id': environment_id
            }.items() if value is not None
        }

        logger.start("start update_by_external_event_id external_event",
                     object=external_event_json)

        super().update_by_id(id_column_value=external_event_id,
                             data_json=external_event_json)
        logger.end("end update_by_external_event_id external_event")
        return

    def update(self, external_event: EventExternal) -> None:
        external_event_json = {
            'system_id': external_event.system_id,
            'subsystem_id': external_event.subsystem_id,
            'url': external_event.url,
            'external_event_identifier': external_event.external_event_identifier, # noqa
            'environment_id': external_event.environment_id
        }

        logger.start(f"start update external_event {
                     external_event.external_event_id}",
                     object=external_event_json)

        super().update_by_id(id_column_value=external_event._external_event_id,
                             data_json=external_event_json)
        logger.end("end update external_event")
        return

    def select_by_external_event_id(self, external_event_id: int) -> dict:
        object_start = {
            'external_event_id': external_event_id
        }
        logger.start("start select_by_external_event_id", object=object_start)

        external_event = super().select_one_dict_by_id(id_column_value=external_event_id) # noqa
        logger.end("end select_by_external_event_id", object=external_event)
        return external_event
