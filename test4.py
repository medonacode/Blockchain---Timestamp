import pywintypes
import win32file
import win32con
import datetime

def change_creation_time(file_path, new_time):
    # Open the file with GENERIC_WRITE access
    handle = win32file.CreateFile(
        file_path,
        win32con.GENERIC_WRITE,
        0,
        None,
        win32con.OPEN_EXISTING,
        0,
        None
    )

    # Convert datetime to Windows file time
    win_time = pywintypes.Time(new_time)

    # Set file times: (creation, access, modification)
    win32file.SetFileTime(handle, win_time, None, None)

    handle.close()

# Example usage
#new_created_time = datetime.datetime(2022, 1, 1, 12, 0, 0)
new_created_time="2023-05-20 10:30:55"

change_creation_time('D:/a1/data1.txtd', new_created_time)
print("Creation time changed successfully.")
