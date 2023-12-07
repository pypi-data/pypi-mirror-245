# TODO: This is an example file which you should delete after implementing
import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
# from api_management_local.Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,NotEnoughStarsForActivityException,PassedTheHardLimitException
from user_context_remote.user_context import UserContext
from .entity_constants import StarLocalConstants
from .star_transaction import StarTransaction
from .exception_star import NotEnoughStarsForActivityException
import  mysql.connector 
object1 =StarLocalConstants.STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT
logger=Logger.create_logger(object=object1)


class StarsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="action_star_subscription")
   
    @staticmethod
    def __get_the_action_stars_by_profile_id_action_id(profile_id, action_id)->int:
        start_obj = {"profile_id": str(profile_id), "action_id": str(action_id)}
        logger.start(object=start_obj)
        try:
            user=UserContext.login_using_user_identification_and_password()
            subscription_id = user.get_effective_subscription_id()
            select_clause = "action_stars"
            where = "subscription_id = {} AND action_id = {}".format(subscription_id, action_id)
            stars_local=StarsLocal()
            action_star = stars_local.select_one_tuple_by_where(
                    view_table_name="action_star_subscription_view", select_clause_value=select_clause, where=where)
        except Exception as e:
            logger.exception(object=e)
            raise
        logger.end(object={'action_star': str(action_star[0])})
        return action_star[0]
    @staticmethod
    def __update_profile_stars(profile_id:int,action_id:int):
        start_obj = {"profile_id": str(profile_id), "action_id": str(action_id)}
        logger.start(object=start_obj)
        try:
            action_stars = StarsLocal.__get_the_action_stars_by_profile_id_action_id(profile_id, action_id)
            connection = Connector.connect("profile")
            cursor = connection.cursor()
            query = """ UPDATE profile.profile_table SET stars=stars+ %s WHERE profile_id= %s"""
            try:
                cursor.execute(query, (action_stars,profile_id))
            except mysql.connector.errors.DataError as excption:
                logger.exception(object=excption)
                raise NotEnoughStarsForActivityException
            connection.commit()
            dict={'action_id':action_id,'action_stars':action_stars}
            Star_Transaction=StarTransaction()
            Star_Transaction.insert(data_json=dict)
            logger.info( {'action_id': action_id, #'stars': stars,# 
                        'action_stars': action_stars })
        except Exception as e:
            logger.exception(object=e)
            raise
        logger.info( {'action_id': action_id, #'stars': stars,# 
                      'action_stars': action_stars })
        logger.end()

    @staticmethod
    def api_executed(api_type_id:int):
        start_obj = {"api_type_id": str(api_type_id)}
        logger.start(object=start_obj)
        try:
            
            connection = Connector.connect("api_type")
            cursor = connection.cursor()
            query = f"""SELECT action_id FROM api_type.api_type_view WHERE api_type_id=%s"""
            cursor.execute(query, (api_type_id,))
            action_id=cursor.fetchone()
            user_context=UserContext.login_using_user_identification_and_password()
            profile_id = user_context.get_effective_profile_id()
            StarsLocal.__update_profile_stars(profile_id,action_id[0])
        except Exception as e:
            logger.exception(object=e)
            raise
        logger.end()
    @staticmethod
    def __how_many_stars_for_action_id(action_id:int)->int:
        start_obj = {"action_id": str(action_id)}
        logger.start(object=start_obj)
        try:
            connection = Connector.connect("action_star_subscription")
            cursor = connection.cursor()
            query="SELECT action_stars FROM action_star_subscription.action_star_subscription_view WHERE action_id=%s"
            cursor.execute(query, (action_id,))
            action_stars=cursor.fetchone()
        except Exception as e:
            logger.exception(object=e)
            raise
        logger.end(object={'action_star': str(action_stars[0])})

        return action_stars[0]
    @staticmethod
    def __how_many_stars_for_profile_id_and_user_id(profile_id:int,user_id:int)->int:
        start_obj = {"profile_id": str(profile_id)}
        logger.start(object=start_obj)
        try:
            connection = Connector.connect("profile")
            cursor = connection.cursor()
            query ="SELECT stars FROM profile.profile_view WHERE profile_id=%s"
            cursor.execute(query, (profile_id,))
            profile_stars=cursor.fetchone()
            query ="SELECT stars FROM user.user_view WHERE user_id=%s"
            cursor.execute(query, (user_id,))
            user_stars=cursor.fetchone()
            star_total=profile_stars[0]+user_stars[0]
        except Exception as e:
            logger.exception(object=e)
            raise
        logger.end(object={'action_star': str(star_total)})
        return star_total
        
    @staticmethod
    def profile_star_before_action(action_id:int):
        start_obj = {"action_id": str(action_id)}
        logger.start(object=start_obj)
        try:
            stars_for_action=StarsLocal.__how_many_stars_for_action_id(action_id)
            user_context=UserContext.login_using_user_identification_and_password()
            profile_id=user_context.get_effective_profile_id()
            user_id=user_context.get_effective_user_id()
            stars_for_profile=StarsLocal.__how_many_stars_for_profile_id_and_user_id(profile_id,user_id)
            if stars_for_profile+stars_for_action < 0:
                raise NotEnoughStarsForActivityException
            else:
                return
        except Exception as e:
            logger.exception(object=e)
            raise
        logger.end()
        

       
        
        
        
       

