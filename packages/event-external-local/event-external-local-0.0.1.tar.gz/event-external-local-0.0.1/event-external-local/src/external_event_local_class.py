import sys
import os
from typing import Any
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
#from user_context_remote.user_context import UserContext
from src.external_event_constants import ExternalEventLocalConstants


object1 = ExternalEventLocalConstants.EXTERNAL_EVENT_LOCAL_CODE_LOGGER_OBJECT
logger=Logger.create_logger(object=object1)
class ExternalEventsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name=ExternalEventLocalConstants.EXTERNAL_EVENT_SCHEMA_NAME,
                         default_table_name=ExternalEventLocalConstants.EXTERNAL_EVENT_TABLE_NAME,
                         default_id_column_name=ExternalEventLocalConstants.EXTERNAL_EVENT_ID_COLUMN_NAME)


    def insert(self, system_id:int, subsystem_id:int, url:str, external_event_identifier:str, environment_id:int) -> int:
        #adding variables validation might be good 
        external_event_data = {
            'system_id':system_id,
            'subsystem_id':subsystem_id,
            'url':url,
            'external_event_identifier':external_event_identifier,
            'environment_id':environment_id
        }
        logger.start("start insert external_event", object=external_event_data)

        external_event_id = super().insert(data_json=external_event_data)
        object_end={
            'external_event_id':external_event_id
        }
        logger.end("end insert external_event", object=object_end)
        return external_event_id
    

    def delete_by_external_event_id(self, external_event_id) -> None:
        object_start={
            'external_event_id':external_event_id
        }
        logger.start("start delete_by_external_event_id", object=object_start)

        super().delete_by_id(id_column_value=external_event_id)
        logger.end("end delete_by_external_event_id external_event")
        return
    
    
    def update_by_external_event_id(self, external_event_id:int, system_id:int=None, subsystem_id:int=None,
                      url:str=None, external_event_identifier:str=None, environment_id:int=None) -> None:
        
        external_event_data = {
            key: value for key, value in {
                'system_id': system_id,
                'subsystem_id': subsystem_id,
                'url': url,
                'external_event_identifier': external_event_identifier,
                'environment_id': environment_id
            }.items() if value is not None
        }
        
        logger.start("start update_by_external_event_id external_event", object = external_event_data)

        super().update_by_id(id_column_value=external_event_id, data_json=external_event_data)
        logger.end("end update_by_external_event_id external_event")
        return

    def select_by_external_event_id(self, external_event_id:int) -> dict:
        object_start={
            'external_event_id':external_event_id
        }
        logger.start("start select_by_external_event_id", object=object_start)

        #external_event_view needs to be created for a select, after creating it define default_view_table_name in the constructor
        #after creating it view_table_name=ExternalEventLocalConstants.EXTERNAL_EVENT_TABLE_NAME can be deleted
        external_event=super().select_one_dict_by_id(id_column_value=external_event_id)
        logger.end("end select_by_external_event_id", object=external_event)
        return external_event
