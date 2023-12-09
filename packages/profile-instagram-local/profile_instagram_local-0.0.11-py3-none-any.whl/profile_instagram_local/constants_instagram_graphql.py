from logger_local.LoggerComponentEnum import LoggerComponentEnum


class ConstantsInstagramAPI:

    CONSTANTS_INSTAGRAM_GRAPHQL_COMPONENT_ID = 158
    CONSTANTS_INSTAGRAM_GRAPHQL_COMPONENT_NAME = 'profile-instagram-graphql-imp-local-python-package'

    OBJECT_TO_INSERT_CODE = {
        'component_id': CONSTANTS_INSTAGRAM_GRAPHQL_COMPONENT_ID,
        'component_name': CONSTANTS_INSTAGRAM_GRAPHQL_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': 'tal.g@circ.zone'
    }

    OBJECT_TO_INSERT_TEST = {
        'component_id': CONSTANTS_INSTAGRAM_GRAPHQL_COMPONENT_ID,
        'component_name': CONSTANTS_INSTAGRAM_GRAPHQL_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'tal.g@circ.zone'
    }
