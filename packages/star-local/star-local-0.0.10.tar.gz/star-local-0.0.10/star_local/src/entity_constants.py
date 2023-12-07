# TODO rename the file from entity_constants.py to i.e. country_constants.py

from logger_local.LoggerComponentEnum import LoggerComponentEnum
import os
from user_context_remote.user_context import UserContext
 
# <Entity> i.e. Country
class StarLocalConstants:

    # TODO Please update your email  v
    
    DEVELOPER_EMAIL = 'heba.a@circ.zone'

    # TODO <PROJECT_NAME> i.e COUNTRY_LOCAL_PYTHON
    # TODO Please send a message in the Slack to #request-to-open-component-id and get your COMPONENT_ID
    STAR_LOCAL_PYTHON_COMPONENT_ID = 244
    STAR_LOCAL_PYTHON_COMPONENT_NAME = "star-local-python-package"
    STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT = {
        'component_id': STAR_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': STAR_LOCAL_PYTHON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    STAR_LOCAL_PYTHONE_TEST_LOGGER_OBJECT = {
        'component_id': STAR_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': STAR_LOCAL_PYTHON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        # TODO Please add the framework you use
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': DEVELOPER_EMAIL
    }

  

    # TODO Please update if you need default values i.e. for testing
    #DEFAULT_XXX_NAME = None
    #DEFAULT_XXX_NAME = None
    USER_CONTEXT=UserContext.login_using_user_identification_and_password()
    PROFILE_ID = USER_CONTEXT.get_effective_profile_id()
    USER_ID=USER_CONTEXT.get_effective_user_id()

    # TODO In the case of non-ML Table, please replace <entity> i.e. country
    STAR_TABLE_NAME = 'star_table'
    STAR_VIEW_NAME = 'star_ml_table'

    # TODO In the case of ML Table, please replace <entity> i.e. country
    STAR_TABLE_NAME = 'star_table'
    STAR_ML_TABLE_NAME = 'star_ml_table'
    STAR_ML_VIEW_NAME = 'star_ml_view'
