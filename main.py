import os.path
import compressors

COMPRESSIONS = {
    "Alice": compressors.alice_compressor
}


def main():
    path = os.path.abspath(f"{os.getcwd()}/../projectPaths.txt")
    if not os.path.exists(path):
        print("[Error] Please ensure that you have created a project using the XXL Editor first")
        exit(1)

    print(f"[Info] Reading '{path}'")
    project_paths: list[str] = []
    with open(path) as project_paths_file:
        paths = project_paths_file.readlines()
        for path in paths:
            path = path.replace("\r", "").replace("\n", "")
            path_parts = path.split(os.sep)
            path_parts.pop()
            project_paths.append(os.sep.join(path_parts))

    if len(project_paths) == 0:
        print("[Error] Please ensure that you have created a project using the XXL Editor first")
        exit(1)

    project_path_index = get_index_input(
        input_message="[Input] Select the project path number you wish to package > ",
        items_list=project_paths
    )

    print('')

    compressors_list = list(COMPRESSIONS.keys())
    compressor_index = get_index_input(
        input_message="[Input] Select the game number to package for > ",
        items_list=compressors_list
    )

    print("[Info] Beginning packaging. This may take a while...")
    game_name = compressors_list[compressor_index]
    out_path = os.path.abspath(f'{os.getcwd()}/out/{game_name}')
    compression_func = COMPRESSIONS[game_name]
    compression_func(
        indir_path=project_paths[project_path_index],
        outdir_path=out_path
    )

    print(f"[Info] Packaging has succeeded and the new files are available at the folder '{out_path}'")
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
