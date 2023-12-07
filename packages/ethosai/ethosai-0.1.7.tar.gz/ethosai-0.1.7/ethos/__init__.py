from .ethos_objects import *


def init_model(*, workspace_id, model_name):
    return Model(workspace_id=workspace_id, name=model_name)


# Use ethos.config to access the global config object.
config = Config()
