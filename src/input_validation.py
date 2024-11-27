import sys
import os


def show_error_text():
    print("Error: Incorrect number of arguments \n")
    print("Usage: python main.py <Source Folder Path> <Replica Folder Path> <Synchronization interval in Seconds> <Log File Location>")
    print("\nArguments:")
    print("  1. Source Folder Path - Path to the source folder.")
    print("  2. Replica Folder Path - Path to the destination folder.")
    print("  3. Synchronization interval - Time interval (in seconds) for synchronization.")
    print("  4. Log File Location - Path to the log file. \n")


def valid_path(path:str) -> bool:
    """
    Verifies if the given path exists or if it can be created. 
    Returns True if the path is valid or created, otherwise returns False.
    """
    if os.path.exists(path):
        return True

    try:
        os.makedirs(path)
        return True

    except OSError:
        return False 


def input_validation() -> bool:
    """
    Validates the user input by checking the number of arguments and ensuring 
    each argument is correct (valid paths, valid synchronization interval, 
    and valid log file).
    Returns True if all inputs are valid, otherwise returns False.
    """
    errors = []

    if len(sys.argv) < 5:
        show_error_text()
        return False

    else:
        if not os.path.exists(sys.argv[1]):
            errors.append(f"Error: The Original Folder Path '{sys.argv[1]}' is invalid.")
        
        if not valid_path(sys.argv[2]):
            errors.append(f"Error: The Replica Folder Path '{sys.argv[2]}' is invalid or could not be created.")
        
        try:
            interval = int(sys.argv[3])
            if interval <= 0:
                errors.append(f"Error: The Sync Interval '{sys.argv[3]}' is invalid. It should be a positive integer.")
        except ValueError:
            errors.append(f"Error: The Sync Interval '{sys.argv[3]}' is invalid. It should be an integer.")

        if not os.path.isfile(sys.argv[4]) or not sys.argv[4].endswith('.log'):
            errors.append(f"Error: The Log File Path '{sys.argv[4]}' is invalid or not a .log file.")

    if errors:
        for error in errors:
            print(error)
        return False

    return True


def validation() -> tuple:
    """
    Performs input validation and returns the valid arguments as a tuple.
    If validation fails, the program exits with a status code of 1.
    """
    if input_validation():
        return sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    else:
        sys.exit(1)


if __name__ == "__main__":
    validation()
