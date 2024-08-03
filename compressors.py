from utils import compress_file, create_path_if_not_exists, post_compress_all_files
import tempfile
import os
import os.path
import re
import gzip

FILE_FORMATS = {
    'PC': 'KWN',
    'Wii': 'KRV',
    'GameCube': 'KGC',
    'PS2': 'KP2',
    'PS3': 'KP3',
    'PSP': 'KPP',
    'Xbox360': 'KXE'
}
_K_FILE_EXTENSION_LIST = list(FILE_FORMATS.values())
GAME_K_FILE_REGEX = rf'GAME.({"|".join(_K_FILE_EXTENSION_LIST)})'
K_FILE_REGEX = rf'[A-Z0-9]+.({"|".join(_K_FILE_EXTENSION_LIST)})'
LEVEL_DIR_REGEX = r'LVL[0-9]{3}'


def alice_compressor(indir_path: str, outdir_path: str):
    COMPRESSION_LEVEL = 1
    COMPRESSION_FUNC = gzip.compress

    print('[Info] Creating temp directory')
    temp_dir = tempfile.mkdtemp(prefix='temp-')
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

                compress_file(
                    input_path=os.path.abspath(f'{indir_path}/{name}/{level_filename}'),
                    output_path=os.path.abspath(f'{temp_dir}/{name}/{level_filename}'),
                    compression_level=COMPRESSION_LEVEL,
                    compression_func=COMPRESSION_FUNC
                )

        # Cycle through root folder files
        elif re.match(K_FILE_REGEX, name.upper()) is not None:

            # GAME.K* is the only .k* file that should not be archived
            if re.match(GAME_K_FILE_REGEX, name.upper()) is not None:
                print(f"[Info] Found file {name}' - skipping archival")
                continue

            compress_file(
                input_path=os.path.abspath(f'{indir_path}/{name}'),
                output_path=os.path.abspath(f'{temp_dir}/{name}'),
                compression_level=COMPRESSION_LEVEL,
                compression_func=COMPRESSION_FUNC
            )

    # Create output directory if it doesn't exist
    outdir_path_parts = outdir_path.split(os.sep)
    create_path_if_not_exists(os.sep.join(outdir_path_parts)[0:len(outdir_path_parts) - 1])
    create_path_if_not_exists(outdir_path)

    post_compress_all_files(temp_dir=temp_dir, dst=outdir_path)
