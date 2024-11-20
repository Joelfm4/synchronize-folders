import sys
import os


def show_error_text():
    print("Error: Incorrect number of arguments.")
    print("Usage: python main.py <Original Folder Path> <Replica Folder Path> <Sync Interval> <Log File Location>")
    print("\nArguments:")
    print("  1. Original Folder Path - Path to the source folder.")
    print("  2. Replica Folder Path - Path to the destination folder.")
    print("  3. Sync Interval - Time interval (in seconds) for synchronization.")
    print("  4. Log File Location - Path to the log file. If you don't have one, enter '0', and the script will create one in the 'logs' folder inside the project directory.")


def valid_path(path:str) -> bool:
    if os.path.exists(path):
        return True

    try:
        os.makedirs(path)
        return True

    except OSError:
        return False 



def input_validation() -> bool:
    if not os.path.exists(sys.argv[1]):
        print(f"Error: The Original Folder Path '{sys.argv[1]}' is invalid \n")
        sys.exit(1)

    if not valid_path(sys.argv[2]):
        print(f"Error: The Replica Folder Path '{sys.argv[2]}' is invalid. Make sure to specify a .log file \n")
        sys.exit(1)

    try:
        int(sys.argv[3])

    except ValueError:
        print(f"Error: The Interval '{sys.argv[3]}' is invalid. Make sure to use only integers without commas or any other special symbols. \n")

    if not os.path.isfile(sys.argv[4]) or not sys.argv[4].endswith('.log'):
        print(f"Error: The log file path '{sys.argv[4]}' is invalid. Make sure to specify a valid path to a .log file \n")
        sys.exit(1)
    
    return True



def validation() -> tuple|None:
    if len(sys.argv) != 5:
        show_error_text()

    if input_validation():
        return sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]



if __name__ == "__main__":
    print(validation())
