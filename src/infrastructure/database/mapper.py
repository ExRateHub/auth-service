from adaptix import Retort, name_mapping

from infrastructure.database.models import UserModel


def get_mapper() -> Retort:
    mapper = Retort()
    mapper.extend(recipe=[name_mapping(UserModel, map={"email": ["email", "value"]})])
    return mapper
