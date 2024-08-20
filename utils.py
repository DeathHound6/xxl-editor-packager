from models import XXLProject, XXLProjectEditor, XXLProjectGame, XXLProjectMeta, XXLProjectPaths, Platform
from typing import Callable, Any, Union
import os.path
import shutil
import winreg
import platform
import json
import re

STEAM_APP_IDS = [
    None, # xxl1
    None, # xxl2
    None, # arthur
    None, # olympic
    None, # spyro
    '316030', # alice
    None # httyd
]


def compress_file(input_path: str, output_path: str, compression_level: int, compression_func: Callable):
    """
    Compress the input file with the compression level, and write the compressed data to the output file

    Args:
        input_path (str) - The input file to compress
        output_path (str) - The file to write the compressed data to
        compression_level (int) - The level of compression to use when compressing the input file
        compression_func (Callable) - The function to use when compressing the file
    """
    print(f"[Info] Compressing file '{input_path}'")
    with open(input_path, "rb") as read:
        compressed_bytes = compression_func(read.read(), compresslevel=compression_level)
    print(f"[Info] Writing compressed data to '{output_path}'")
    with open(output_path, "wb") as write:
        write.write(compressed_bytes)


def post_compress_all_files(temp_dir: str, dest_dir: str):
    """
    Perform the final cleanup after the files have been compressed

    Args:
        temp_dir (str) - The path to the temp directory
        dest_dir (str) - The directory path where the compressed files will be copied to
    """
    print("[Info] Copying archived files")
    shutil.copytree(src=temp_dir, dst=dest_dir, dirs_exist_ok=True)
    print("[Info] Deleting temp directory")
    shutil.rmtree(temp_dir)


def create_path_if_not_exists(path: str):
    """
    Create the given directory or file if it does not yet exist

    Args:
        path (str) - The path to the directory or file
    """
    if os.path.exists(path) is False:
        os.mkdir(path)


def read_xxl_editor_xecproj_file(file_path: str) -> Union[XXLProject, None]:
    """
    Args:
        file_path (str) - The path to the `xecproj` file
    Returns:
        None - If the file does not exist
        XXLProject - A representation of the `xecproj` file
    """
    if os.path.exists(file_path) is False:
        return

    with open(file_path, "r") as file:
        file_json = json.loads(file.read())
        xxl_proj = XXLProject(
            editor=XXLProjectEditor(
                initial_level=file_json['editor']['initialLevel']
            ),
            format_version=file_json['formatVersion'],
            game=XXLProjectGame(
                id=file_json['game']['id'],
                is_remaster=file_json['game']['isRemaster'],
                platform=Platform[file_json['game']['platform']]
            ),
            meta=XXLProjectMeta(
                name=file_json['meta']['name']
            ),
            paths=XXLProjectPaths(
                game_module=file_json['paths']['gameModule'],
                input_path=file_json['paths']['inputPath'],
                output_path=file_json['paths']['outputPath']
            )
        )

    return xxl_proj


def replace_steam_game_files(compressed_dir: str, game_id: int):
    """
    Copy the output of compression into the game's install folder via Steam

    Args:
        compressed_dir (str) - The path to the output folder of this program
        game_id (int) - The game's id from xxl editor config
    """
    app_id = STEAM_APP_IDS[game_id - 1]

    # Get the steam install folder from windows registry
    reg_handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    arch = 64 if platform.architecture()[0] == '64bit' else 32
    reg_key_path = "SOFTWARE\\" + ('Wow6432Node\\' if arch == 64 else '') + "Valve\\Steam"
    steam_install_path = winreg.OpenKey(reg_handle, reg_key_path)
    install_path, _ = winreg.QueryValueEx(steam_install_path, "InstallPath")
    steam_install_path.Close()
    reg_handle.Close()

    # Read steam files to find where the game is installed to
    file_path = f'{install_path}\\steamapps\\libraryfolders.vdf'
    libraries_json = read_steam_vdf_acf_file(file_path)
    if libraries_json is None:
        print(f"[Error] File '{file_path}' does not exist")
        return

    game_install_path = None
    for app in libraries_json.values():
        if 'apps' in app and str(app_id) in app['apps']:
            game_install_path = app.get('path', None) or None
            break
    if game_install_path is None:
        print('[Error] The game does not appear to be installed via Steam')
        return

    file_path = f'{game_install_path}\\steamapps\\appmanifest_{app_id}.acf'
    app_manifest = read_steam_vdf_acf_file(file_path)
    if app_manifest is None:
        print(f"[Error] File '{file_path}' does not exist")
        return
    folder_name = app_manifest.get('installdir', None) or None
    if folder_name is None:
        print('[Error] Could not find the name of the games installed folder')
        return

    steam_game_dir = f'{game_install_path}\\steamapps\\common\\{folder_name}'
    if os.path.exists(steam_game_dir) is False:
        print('[Error] The game does not appear to be installed')
        return

    print('[Info] Replacing game files')
    shutil.copytree(src=compressed_dir, dst=steam_game_dir, dirs_exist_ok=True)


def read_steam_vdf_acf_file(file_path: str) -> Union[dict[str, Any], None]:
    """
    Read Steam's `vdf` or `acf` files and return them as JSON

    Args:
        file_path (str) - The abslute path to the vdf or acf file
    Returns:
        None - If the file does not exist
        dict[str, Any] - The JSON representation of the file
    """
    if os.path.exists(file_path) is False:
        return

    json_str = ""
    with open(file_path, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            # Line 1 - "LibraryFolders", "AppState" etc
            if index == 0:
                continue

            # When opening or closing a dict
            if (char := line.strip()) in ['{', '}']:
                json_str += char
                # If closing an dict and there is more fields after
                # We also don't want to throw an index error
                if char == '}' and index + 1 < len(lines) and lines[index + 1].strip() not in ['}', '']:
                    json_str += ','

            # Dict key names
            # Opening the inner dict is on the line after
            if re.match(r'^"[0-9a-zA-Z]+"$', (l := line.strip())) is not None and \
               lines[index + 1].strip() == '{':
                json_str += f'{l}:'

            # String fields
            if re.match(r'^"[a-zA-Z0-9]+":"(.+)?"$', (l := line.strip().replace('\t\t', ':'))) is not None:
                json_str += l
                # If there is another field after
                if lines[index + 1].strip() not in ['}', '']:
                    json_str += ','

    file_json = json.loads(json_str)
    return file_json
