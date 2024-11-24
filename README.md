# Folder Synchronization 

A simple script for synchronizing the contents of a **source folder** with a **destination folder**.

## Features
- **Folder Synchronization**: Reflects all changes made in the source folder to the replica.
- **Change Detection**: Detects new, moved, modified, or deleted files in the source folder and automatically updates the destination folder accordingly.
- **Performance**: Uses **multithreading** for efficient I/O operations and **parallelism** to watch for changes
- **Logs**: Keeps a record of all logs.

## Installation

#### 1. Clone the repository:
```
git clone https://github.com/Joelfm4/synchronize-folders
cd synchronize-folders
```

#### 2. Install dependencies:
```
pip install -r requirements.txt
```
## How to Use
``` 
python main.py <Source Directory Path> <Destination Directory Path> <Synchronization interval in Seconds> <Log file Location>
```


#### To Do
- Default log file
- Windows compatibility 
- Remove wathdog dependency
- Improve changes filter 
- Reduce the number of os.join and os.path.normpath
- Cache (files hash)



