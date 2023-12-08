## WRITE FILE #######################################################
def file_writer(filepath, data):
    """
    Write to `filepath` with `data` content.

    Args:
        filepath <string>   path of file
        data <string> content of file

    Returns: no
    """
    with open(filepath, "w+") as file_handle:
        file_handle.write(data)


## READ FILE #######################################################
def file_reader(filepath):
    """
    Read content in `filepath`.

    Args:
        filepath <string>    path of file

    Returns:
        string
    """
    with open(filepath, 'r') as file_handle:
        file_data = file_handle.read()
    return file_data
