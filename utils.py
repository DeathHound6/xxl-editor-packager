from typing import Callable
import os.path
import shutil


def compress_file(input_path: str, output_path: str, compression_level: int, compression_func: Callable):
    """
    Compress the input file with the compression level, and write the compressed data to the output file

    Args:
        input_path (str) - The input file to compress
        output_path (str) - The file to write the compressed data to
        compression_level (int) - The level of compression to use when compressing the input file
    """
    print(f"[Info] Compressing file '{input_path}'")
    with open(input_path, "rb") as read:
        compressed_bytes = compression_func(read.read(), compresslevel=compression_level)
    # Write compressed file to temp dir
    with open(output_path, "wb") as write:
        write.write(compressed_bytes)

def post_compress_all_files(temp_dir: str, dst: str):
    print("[Info] Copying archived files")
    shutil.copytree(src=temp_dir, dst=dst, dirs_exist_ok=True)
    print("[Info] Deleting temp directory")
    shutil.rmtree(temp_dir)

def create_path_if_not_exists(path: str) -> str:
    if not os.path.exists(path):
        os.mkdir(path)