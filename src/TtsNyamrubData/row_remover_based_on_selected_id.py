from config import IGNORE_LIST


def should_ignore(file_id):
    """Determines whether a file should be ignored based on a predefined ignore list.
    Args:
        file_id (str): The ID of the file to check.

    Returns:
        bool:
            - True if the file ID matches any entry in the `IGNORE_LIST`.
            - False otherwise.
    """
    for item in IGNORE_LIST:
        if "-" in item:
            start, end = item.split("-")
            start_num = int(start.split("AB")[-1])
            end_num = int(end.split("AB")[-1])
            file_num = int(file_id.split("AB")[-1])
            if start_num <= file_num <= end_num:
                return True
        elif file_id == item:
            return True
    return False
