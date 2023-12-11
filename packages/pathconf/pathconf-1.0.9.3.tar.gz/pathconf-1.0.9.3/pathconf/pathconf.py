import os
import json
import queue
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
workers = os.cpu_count() * 3
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def has_extension(filename):
    """
    Check if the given filename has an extension.

    Parameters:
        filename (str): The filename to check.

    Returns:
        bool: True if the filename has an extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1] != ''


def search_directories(queue, dir_to_find, target, stop_event,
                       ignore_extension=False, search_folder=False):
    while not queue.empty() and not stop_event.is_set():
        try:
            directory = queue.get_nowait()
        except queue.Empty:
            break

        if stop_event.is_set():
            break

        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                dirnames[:] = [d for d in dirnames if 'Deprecated' not in d]

                if stop_event.is_set():
                    break

                if search_folder:
                    # Searching for directories
                    if target in dirnames:
                        stop_event.set()
                        return os.path.join(dirpath, target)
                else:
                    # Searching for files
                    for filename in filenames:
                        if ignore_extension and not search_folder:
                            if filename.split('.')[0] == target:
                                stop_event.set()
                                return os.path.join(dirpath, filename)
                        elif filename == target:
                            stop_event.set()
                            return os.path.join(dirpath, filename)

        except Exception as e:
            logging.error(f"Error occurred: {e}")
        finally:
            queue.task_done()

    return None


def load_json_config(file_path):
    """
    Load JSON configuration file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON object or empty dictionary if file is invalid.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error("JSON Decode Error occurred")
        return {}
    except IOError as e:
        logging.error(f"IOError occurred: {e}")
        return {}


def remove(target_path):
    config_file_path = os.path.join(os.path.expanduser("~"),
                                    '.config', 'pathconf',
                                    '.file_paths.json')

    if os.path.isfile(config_file_path):
        config = load_json_config(config_file_path)

        if target_path in config:
            del config[target_path]
            with open(config_file_path, 'w') as f:
                json.dump(config, f)
            logging.info(f"Removed {target_path} from config.")
        else:
            logging.info(f"{target_path} not found in config.")


def reset():
    """
    Reset the JSON configuration file, removing all items.
    """
    config_file_path = os.path.join(os.path.expanduser("~"),
                                    '.config', 'pathconf',
                                    '.file_paths.json')

    with open(config_file_path, 'w') as f:
        json.dump({}, f)
    logging.info("Configuration file reset.")


def list_paths():
    """
    List all file paths stored in the JSON configuration file.

    Returns:
        dict: A dictionary of all file paths in the config.
    """
    config_file_path = os.path.join(os.path.expanduser("~"),
                                    '.config', 'pathconf',
                                    '.file_paths.json')

    if os.path.isfile(config_file_path):
        return load_json_config(config_file_path)
    else:
        logging.info("No configuration file found.")
        return {}


def find_path(target_path, folder=False):
    """
    Main function to find the path of a target file or folder,
    considering file extensions and the possibility that the
    target might be a folder.

    Parameters:
        target_path (str): Path (including optional directories) to search for.
        folder (bool): Whether to search for a folder instead of a file.

    Returns:
        str: Path to the found file or folder.

    Raises:
        FileNotFoundError: If the file or folder is not found.
    """
    # Split the target_path into directory (if any) and target
    *path_parts, target = os.path.normpath(target_path).split(os.sep)
    dir_to_find = os.path.join(*path_parts) if path_parts else None

    # Define the start path as the user's home directory
    start_path = os.path.expanduser("~")

    # Determine whether to ignore file extension during the search
    ignore_extension = not has_extension(target) and not folder

    config_path_part = os.path.join(start_path, '.config')
    config_path = os.path.join(config_path_part, 'pathconf')
    config_filename = '.file_paths.json'
    config_file_path = os.path.join(config_path, config_filename)

    # Create the configuration directory if it doesn't exist
    os.makedirs(config_path, exist_ok=True)

    # Load existing config or initialize new one
    config = load_json_config(config_file_path)

    # Check directly in the home directory
    # only if no directory part is provided in target_path
    if not dir_to_find:
        direct_path = os.path.join(start_path, target)
        found = False
        if folder:
            if os.path.isdir(direct_path):
                found = True
        else:
            if ignore_extension:
                found = any(f.split('.')[0] ==
                            target for f in os.listdir(start_path))
            else:
                found = os.path.isfile(direct_path)

        if found:
            config[target_path] = direct_path
            with open(config_file_path, 'w+') as f:
                json.dump(config, f)
            return direct_path

    dir_queue = queue.Queue()
    for d in os.listdir(start_path):
        if os.path.isdir(os.path.join(start_path, d)):
            dir_queue.put(os.path.join(start_path, d))

    stop_event = threading.Event()
    target_path = None

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(search_directories, dir_queue,
                   dir_to_find, target, stop_event, ignore_extension, folder)
                   for _ in range(os.cpu_count())]
        for future in as_completed(futures):
            result = future.result()
            if result:
                target_path = result
                break

    if target_path:
        config[target_path] = target_path
        with open(config_file_path, 'w+') as f:
            json.dump(config, f)
        return target_path
    else:
        raise FileNotFoundError(f"{target_path} not found.")
