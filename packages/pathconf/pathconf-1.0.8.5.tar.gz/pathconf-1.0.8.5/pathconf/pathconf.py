import os
import json
import queue
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
workers = os.cpu_count() * 3
# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def search_directories(queue, dir_to_find, target, stop_event):
    while not queue.empty() and not stop_event.is_set():
        try:
            directory = queue.get_nowait()
        except queue.Empty:
            break  # Queue is empty

        if stop_event.is_set():  # Check if stop_event is set before processing
            break

        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                if stop_event.is_set():  # Check again inside the loop
                    break

                if dir_to_find and not dirpath.endswith(dir_to_find):
                    # Optionally add new subdirectories to the queue
                    for dirname in dirnames:
                        new_dir = os.path.join(dirpath, dirname)
                        queue.put(new_dir)

                if target in filenames:
                    stop_event.set()
                    return os.path.join(dirpath, target)
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


def find_path(target_path):
    """
    Main function to find the path of a target file. This version also
    supports searching within a specified subdirectory.

    Parameters:
        target_path (str): Path (including optional directories)
        to search for.

    Returns:
        str: Path to the found file.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    # Split the target_path into directory (if any) and filename
    *path_parts, target_file = os.path.normpath(target_path).split(os.sep)
    dir_to_find = os.path.join(*path_parts) if path_parts else None

    # Define the start path as the user's home directory
    start_path = os.path.expanduser("~")

    config_path_part = os.path.join(start_path, '.config')
    config_path = os.path.join(config_path_part, 'pathconf')
    config_filename = '.file_paths.json'
    config_file_path = os.path.join(config_path, config_filename)

    try:
        os.makedirs(config_path, exist_ok=True)

        config = {}

        if os.path.isfile(config_file_path):
            config = load_json_config(config_file_path)
            file_path = config.get(target_path)

            if file_path and os.path.isfile(file_path):
                return file_path

        dir_queue = queue.Queue()
        for d in os.listdir(start_path):
            if os.path.isdir(os.path.join(start_path, d)):
                dir_queue.put(os.path.join(start_path, d))

        stop_event = threading.Event()
        file_path = None

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(search_directories, dir_queue,
                       dir_to_find, target_file, stop_event)
                       for _ in range(os.cpu_count())]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    file_path = result
                    break  # Break the loop as soon as the file is found

        if file_path:
            config[target_path] = file_path
            with open(config_file_path, 'w+') as f:
                json.dump(config, f)
            return file_path
        else:
            raise FileNotFoundError(f"{target_path} not found.")
    except IOError as e:
        logging.error(f"IOError occurred: {e}")
