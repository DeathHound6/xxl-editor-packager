import sys
import os.path
import compressors
from utils import replace_steam_game_files, read_xxl_editor_xecproj_file
from models import XXLProject, Platform, GAME_NAMES

COMPRESSIONS = [
    None,
    None,
    None,
    None,
    None,
    compressors.alice_compressor,
    None
]


def main():
    if sys.platform != "win32":
        print("[Error] This program can only be run on Windows systems")
        exit(1)

    path = os.path.abspath(f"{os.getcwd()}/../projectPaths.txt")
    if not os.path.exists(path):
        print("[Error] Please ensure that you have created a project using the XXL Editor first")
        exit(1)

    print(f"[Info] Reading '{path}'")
    projects: list[XXLProject] = []
    with open(path) as project_paths_file:
        paths = project_paths_file.readlines()
        for path in paths:
            path = os.path.abspath(path.replace("\r", "").replace("\n", ""))
            xxl_proj = read_xxl_editor_xecproj_file(path)
            if xxl_proj is not None:
                projects.append(xxl_proj)

    if len(projects) == 0:
        print("[Error] Please ensure that you have created a project using the XXL Editor first")
        exit(1)

    project_index = get_index_input(
        input_message="[Input] Select the project path number you wish to package > ",
        items_list=[f'{xxl.meta.name} ({xxl.paths.output_path})' for xxl in projects]
    )
    project = projects[project_index]
    print('')

    print("[Info] Beginning packaging. This may take a while...")
    game_name = GAME_NAMES[project.game.id - 1]
    out_path = os.path.abspath(f'{os.getcwd()}/out/{game_name}')
    compression_func = COMPRESSIONS[project.game.id - 1]
    compression_func(
        indir_path=projects[project_index].paths.output_path,
        outdir_path=out_path
    )

    print(f"[Info] Packaging has succeeded and the new files are available at '{out_path}'")

    if projects[project_index].game.platform is Platform.KWN:
        replace_steam_files_input = get_index_input(
            input_message="[Input] Do you want to replace the Steam files? > ",
            items_list=['Yes', 'No']
        )
        if replace_steam_files_input == 0:
            replace_steam_game_files(compressed_dir=out_path, game_id=project.game.id)
            return
        print('[Info] The compressed files will not be automatically installed to Steam')

    print("[Info] To install these changes, replace the game files with the packaged ones")


def get_index_input(input_message: str, items_list: list[str]) -> int:
    """
    Return the index from user input for the selected item from the given list

    Args:
        input_message (str) - The message to display to the user when asking for input
        items_list (list[str]) - The list of items to ask the user for
    Returns:
        index (int) - The index of the chosen item
    """
    for i, item in enumerate(items_list):
        print(f'{i + 1}) {item}')

    index = -1
    input_index = ""
    while index == -1:
        try:
            input_index = input(input_message)
            if input_index.lower() == "exit":
                raise KeyboardInterrupt
            index = int(input_index) - 1
            if index < 0:
                raise IndexError
            items_list[index]
        except KeyboardInterrupt:
            if input_index.lower() != "exit":
                print("")
            print("[Info] Exit command entered")
            exit(0)
        # TODO: Can I merge the 2 below except blocks?
        except IndexError:
            print("[Warning] Please enter a valid number from the list")
            index = -1
        except ValueError:
            print("[Warning] Please enter a valid number from the list")
            index = -1
    return index


if __name__ == '__main__':
    main()
