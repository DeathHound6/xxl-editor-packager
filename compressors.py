from utils import compress_file, create_path_if_not_exists, Platform, get_threads_data_list
from typing import Any
import tempfile
import os
import os.path
import re
import gzip
import shutil

GAME_K_FILE_REGEX = rf'^GAME.({"|".join(list(Platform.__members__.keys()))})$'
K_FILE_REGEX = rf'^[A-Z0-9]+.({"|".join(list(Platform.__members__.keys()))})$'
LEVEL_DIR_REGEX = r'^LVL[0-9]{3}$'


def alice_compressor(indir_path: str, outdir_path: str):
    """
    Compress the files for Alice in Wonderland

    Args:
        indir_path (str) - The path where the uncompressed files are located
        outdir_path (str) - The path to write the compressed files
    """
    def thread_worker(data_list: list[dict[str, Any]]):
        COMPRESSION_LEVEL = 1
        COMPRESSION_FUNC = gzip.compress
        for data in data_list:
            compress_file(
                input_path=data['input'],
                output_path=data['output'],
                compression_level=COMPRESSION_LEVEL,
                compression_func=COMPRESSION_FUNC
            )

    try:
        print('[Info] Creating temp directory')
        temp_dir = tempfile.mkdtemp(prefix='temp-')
        paths = []
        for name in os.listdir(indir_path):

            # Cycle through level files
            if re.match(LEVEL_DIR_REGEX, name.upper()) is not None:
                for level_filename in os.listdir(f'{indir_path}/{name}'):

                    # Only package `kwn` files within the level folders
                    if re.match(K_FILE_REGEX, level_filename.upper()) is None:
                        print(f"[Info] Found file '{level_filename}' - skipping archival")
                        continue

                    # Create this level folder in temp dir
                    create_path_if_not_exists(f'{temp_dir}/{name}')

                    paths.append({
                        'input': os.path.abspath(f'{indir_path}/{name}/{level_filename}'),
                        'output': os.path.abspath(f'{temp_dir}/{name}/{level_filename}')
                    })

            # Cycle through root folder files
            elif re.match(K_FILE_REGEX, name.upper()) is not None:

                # GAME.K* is the only .k* file that should not be archived
                if re.match(GAME_K_FILE_REGEX, name.upper()) is not None:
                    print(f"[Info] Found file {name}' - skipping archival")
                    continue

                paths.append({
                    'input': os.path.abspath(f'{indir_path}/{name}'),
                    'output': os.path.abspath(f'{temp_dir}/{name}')
                })

        threads = get_threads_data_list(thread_worker, paths)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        # Create output directory if it doesn't exist
        outdir_path_parts = outdir_path.split(os.sep)
        for i in range(len(outdir_path_parts)):
            # Skip on the first folder
            # First - the drive/mount letter
            if i == 0:
                continue
            create_path_if_not_exists(os.sep.join(outdir_path_parts[0:i]))

        print("[Info] Copying archived files")
        shutil.copytree(src=temp_dir, dst=outdir_path, dirs_exist_ok=True)
    except KeyboardInterrupt:
        raise
    finally:
        print("[Info] Deleting temp directory")
        shutil.rmtree(temp_dir)
