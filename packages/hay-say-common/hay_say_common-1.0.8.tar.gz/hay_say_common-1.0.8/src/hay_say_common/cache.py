import json
import os
import shutil
import time
from datetime import datetime
from enum import Enum, auto

import soundfile

from .utility import read_audio
from .file_integration import guarantee_directory

CACHE_FORMAT, CACHE_EXTENSION, CACHE_MIMETYPE = 'FLAC', '.flac', 'audio/flac;base64'  # FLAC compression is lossless
MAX_FILES_PER_STAGE = 25
TIMESTAMP_FORMAT = '%Y/%m/%d %H:%M:%S.%f'


class Stage(Enum):
    RAW = auto()  # Raw file supplied by the user
    PREPROCESSED = auto()  # User file after it has undergone preprocessing
    OUTPUT = auto()  # Generated file, without any preprocessing
    POSTPROCESSED = auto()  # Generated file after it has undergone postprocessing


class FileImpl:
    METADATA_FILENAME = 'metadata.json'

    ROOT_DIR = os.path.join(os.path.expanduser('~'), 'hay_say')
    AUDIO_FOLDER = os.path.join(ROOT_DIR, 'audio_cache')

    folder_map = {
        Stage.RAW: 'raw',
        Stage.PREPROCESSED: 'preprocessed',
        Stage.OUTPUT: 'output',
        Stage.POSTPROCESSED: 'postprocessed'
    }

    @classmethod
    def map_folder(cls, stage, session_id):
        args = (cls.AUDIO_FOLDER, session_id, cls.folder_map[stage])
        args = (item for item in args if item)  # Remove any arguments that evaluate to "None".
        return os.path.join(*args)

    @classmethod
    def read_metadata(cls, stage, session_id):
        """Return the metadata dictionary of the cache at the specified stage. The metadata dictionary describes all the
        files stored in the cache at a given stage.
        'stage' should be one of the Stage enums"""
        path_to_file = os.path.join(cls.map_folder(stage, session_id), cls.METADATA_FILENAME)
        metadata = dict()
        if os.path.isfile(path_to_file):
            with open(path_to_file, 'r') as file:
                metadata = json.load(file)
        return metadata

    @classmethod
    def write_metadata(cls, stage, session_id, dict_contents):
        """Sets the metadata dictionary to the supplied dictionary for the cache at the specified stage, overwriting
        existing contents. The metadata dictionary describes all the files stored in the cache at a given stage.
        'stage' should be one of the Stage enums"""
        path = os.path.join(cls.map_folder(stage, session_id), cls.METADATA_FILENAME)
        guarantee_directory(os.path.dirname(path))
        with open(path, 'w') as file:
            file.write(json.dumps(dict_contents, sort_keys=True, indent=4))

    @classmethod
    def read_audio_from_cache(cls, stage, session_id, filename_sans_extension):
        """Reads the specified file from the cache at the specified stage, returning the data array and sample rate.
        'stage' should be one of the Stage enums"""
        path = os.path.join(cls.map_folder(stage, session_id), filename_sans_extension + CACHE_EXTENSION)
        return read_audio(path)

    @classmethod
    def save_audio_to_cache(cls, stage, session_id, filename_sans_extension, array, samplerate):
        """saves the supplied audio data to the cache at the specified stage with the specified filename. The oldest file in
        the cache for the stage is deleted if saving this file would cause the total number of files cached in that stage to
        exceed MAX_FILES_PER_STAGE.
        'stage' should be one of the Stage enums"""
        if cls.count_audio_cache_files(stage, session_id) >= MAX_FILES_PER_STAGE:
            cls.delete_oldest_cache_file(stage, session_id)
        cls.write_audio_file(stage, session_id, filename_sans_extension, array, samplerate)

    @classmethod
    def write_audio_file(cls, stage, session_id, filename_sans_extension, array, samplerate):
        """writes audio data to the cache at the specified stage with the specified filename.
        'stage' should be one of the Stage enums"""
        path = os.path.join(cls.map_folder(stage, session_id), filename_sans_extension + CACHE_EXTENSION)
        guarantee_directory(os.path.dirname(path))
        soundfile.write(path, array, samplerate, format=CACHE_FORMAT)

    @classmethod
    def count_audio_cache_files(cls, stage, session_id):
        """Return the number of audio files stored in the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        metadata = cls.read_metadata(stage, session_id)
        return len(metadata.keys())

    @classmethod
    def delete_oldest_cache_file(cls, stage, session_id):
        """Deletes the oldest file from the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        # delete the file itself
        oldest_filename_sans_extension = cls.get_hashes_sorted_by_timestamp(stage, session_id)[-1]
        oldest_path = os.path.join(cls.map_folder(stage, session_id), oldest_filename_sans_extension + CACHE_EXTENSION)
        os.remove(oldest_path)

        # remove entry from metadata file
        metadata = cls.read_metadata(stage, session_id)
        del metadata[oldest_filename_sans_extension]
        cls.write_metadata(stage, session_id, metadata)

    @classmethod
    def get_hashes_sorted_by_timestamp(cls, stage, session_id):
        """Returns the hashes/filenames (without extension) of the audio files in the cache at the specified stage, sorted
        by their timestamp.
        'stage' should be one of the Stage enums"""
        metadata = cls.read_metadata(stage, session_id)
        return sorted(metadata.keys(),
                      key=lambda key: datetime.strptime(metadata[key]['Time of Creation'], TIMESTAMP_FORMAT),
                      reverse=True)

    @classmethod
    def file_is_already_cached(cls, stage, session_id, filename_sans_extension):
        """Return True if the specified file is already present in the cache at the specified stage, otherwise False
        'stage' should be one of the Stage enums"""
        metadata = cls.read_metadata(stage, session_id)
        return True if filename_sans_extension in metadata.keys() else False

    @classmethod
    def delete_all_files_at_stage(cls, stage, session_id):
        """Deletes all files, including the metadata file, at the specified stage
        'stage' should be one of the Stage enums"""
        base_path = os.path.join(cls.map_folder(stage, session_id))
        for filename in os.listdir(base_path):
            path = os.path.join(base_path, filename)
            os.remove(path)

    @classmethod
    def read_file_bytes(cls, stage, session_id, filename_sans_extension):
        """Reads the specified file at the specified stage and returns the raw bytes of the file.
        'stage' should be one of the Stage enums"""
        path = os.path.join(cls.map_folder(stage, session_id), filename_sans_extension + CACHE_EXTENSION)
        with open(path, 'rb') as file:
            byte_data = file.read()
        return byte_data

    @classmethod
    def delete_old_session_data(cls, cutoff_in_seconds=3600 * 24):
        """Deletes all session data for all session IDs that are older than the given cutoff"""
        session_paths = [os.path.join(cls.AUDIO_FOLDER, item) for item in os.listdir(cls.AUDIO_FOLDER)
                        if os.path.isdir(os.path.join(cls.AUDIO_FOLDER, item)) and item not in cls.folder_map.values()]
        old_session_dirs = [path for path in session_paths
                            if (time.time() - os.path.getmtime(path)) > cutoff_in_seconds]
        for path in old_session_dirs:
            cls.delete_session_data(os.path.basename(path))

    @classmethod
    def delete_session_data(cls, session_id):
        """Deletes all data associated with the given session ID"""
        path = os.path.join(cls.AUDIO_FOLDER, session_id)
        shutil.rmtree(path)


class MongoImpl:
    # todo: implement this class

    @classmethod
    def read_metadata(cls, stage):
        """Return the metadata dictionary of the cache at the specified stage. The metadata dictionary describes all the
        files stored in the cache at a given stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def write_metadata(cls, stage, dict_contents):
        """Sets the metadata dictionary to the supplied dictionary for the cache at the specified stage, overwriting
        existing contents. The metadata dictionary describes all the files stored in the cache at a given stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def read_audio_from_cache(cls, stage, filename_sans_extension):
        """Reads the specified file from the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def save_audio_to_cache(cls, stage, filename_sans_extension, array, samplerate):
        """saves the supplied audio data to the cache at the specified stage with the specified filename. The oldest file in
        the cache for the stage is deleted if saving this file would cause the total number of files cached in that stage to
        exceed MAX_FILES_PER_STAGE.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def write_audio_file(cls, stage, filename_sans_extension, array, samplerate):
        """writes audio data to the cache at the specified stage with the specified filename.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def count_audio_cache_files(cls, stage):
        """Return the number of audio files stored in the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def delete_oldest_cache_file(cls, stage):
        """Deletes the oldest file from the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def get_hashes_sorted_by_timestamp(cls, stage):
        """Returns the hashes/filenames (without extension) of the audio files in the cache at the specified stage, sorted
        by their timestamp.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def file_is_already_cached(cls, stage, filename_sans_extension):
        """Return True if the specified file is already present in the cache at the specified stage, otherwise False"""
        pass

    @classmethod
    def delete_all_files_at_stage(cls, stage):
        """Deletes all files, including the metadata file, at the specified stage
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def read_file_bytes(cls, stage, filename_sans_extension):
        """Reads the specified file at the specified stage and returns the raw bytes of the file.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def delete_old_session_data(cls, cutoff_in_seconds=3600 * 24):
        """Deletes all session data for all session IDs that are older than the given cutoff"""
        pass

    @classmethod
    def delete_session_data(cls, session_id):
        """Deletes all data associated with the given session ID"""
        pass


class RedisImpl:
    # todo: implement this class (but MongoImpl is definitely higher priority)
    # REDIS_URL = 'redis://redis:6379'
    # redis_db = redis.StrictRedis.from_url(REDIS_URL)
    # Note: Redis databases are limited to 25 GB each.
    @classmethod
    def read_metadata(cls, stage):
        """Return the metadata dictionary of the cache at the specified stage. The metadata dictionary describes all the
        files stored in the cache at a given stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def write_metadata(cls, stage, dict_contents):
        """Sets the metadata dictionary to the supplied dictionary for the cache at the specified stage, overwriting
        existing contents. The metadata dictionary describes all the files stored in the cache at a given stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def read_audio_from_cache(cls, stage, filename_sans_extension):
        """Reads the specified file from the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def save_audio_to_cache(cls, stage, filename_sans_extension, array, samplerate):
        """saves the supplied audio data to the cac+he at the specified stage with the specified filename. The oldest file in
        the cache for the stage is deleted if saving this file would cause the total number of files cached in that stage to
        exceed MAX_FILES_PER_STAGE.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def write_audio_file(cls, stage, filename_sans_extension, array, samplerate):
        """writes audio data to the cache at the specified stage with the specified filename.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def count_audio_cache_files(cls, stage):
        """Return the number of audio files stored in the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def delete_oldest_cache_file(cls, stage):
        """Deletes the oldest file from the cache at the specified stage.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def get_hashes_sorted_by_timestamp(cls, stage):
        """Returns the hashes/filenames (without extension) of the audio files in the cache at the specified stage, sorted
        by their timestamp.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def file_is_already_cached(cls, stage, filename_sans_extension):
        """Return True if the specified file is already present in the cache at the specified stage, otherwise False"""
        pass

    @classmethod
    def delete_all_files_at_stage(cls, stage):
        """Deletes all files, including the metadata file, at the specified stage
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def read_file_bytes(cls, stage, filename_sans_extension):
        """Reads the specified file at the specified stage and returns the raw bytes of the file.
        'stage' should be one of the Stage enums"""
        pass

    @classmethod
    def delete_old_session_data(cls, cutoff_in_seconds=3600 * 24):
        """Deletes all session data for all session IDs that are older than the given cutoff"""
        pass

    @classmethod
    def delete_session_data(cls, session_id):
        """Deletes all data associated with the given session ID"""
        pass

cache_implementation_map = {'mongo': MongoImpl,
                            'file': FileImpl}


def select_cache_implementation(choice):
    return cache_implementation_map[choice]
