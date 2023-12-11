import os

"""Constants and methods related to file integration between the UI container and the various AI Architecture 
containers"""


ROOT_DIR = os.path.join(os.path.expanduser('~'), 'hay_say')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')


if not os.path.exists(MODELS_DIR):
    # All Docker containers must have a shared volume mounted at MODELS_DIR. This is where character models are stored.
    raise Exception('"models" directory does not exist! Did you forget to mount the models volume?')


def model_pack_dirs(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns a list of absolute paths to all the model pack directories for the given architecture."""
    return [directory for directory in possible_model_pack_dirs(architecture_name) if os.path.isdir(directory)]


def possible_model_pack_dirs(architecture_name):
    """A helper method for model_pack_dirs"""
    return [os.path.join(ROOT_DIR, architecture_name + '_model_pack_' + str(index)) for index in range(100)]


def characters_dir(architecture_name):
    """Returns the directory containing all the character model subdirectories for the given architecture."""
    return guarantee_directory(os.path.join(MODELS_DIR, architecture_name, 'characters'))


def guarantee_directory(directory):
    """Creates the directory if it does not exist and returns the path to the directory that now definitely exists"""
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return directory


def character_dir(architecture_name, character_name):
    """Returns the directory where the files for a given character model in a given architecture are stored."""
    return os.path.join(MODELS_DIR, architecture_name, 'characters', character_name)


def multispeaker_model_dir(architecture_name, model_name):
    """Returns the directory where multi-speaker models are stored for the given architecture."""
    return os.path.join(MODELS_DIR, architecture_name, 'multispeaker_models', model_name)

