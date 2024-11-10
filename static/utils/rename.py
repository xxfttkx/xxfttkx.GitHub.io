import os
import time
from datetime import datetime

def get_modification_time(file_path):
    return time.ctime(os.path.getmtime(file_path))

def rename_images():
    # 获取当前文件夹下的所有 .jpg 文件
    jpg_files = [f for f in os.listdir() if f.lower().endswith('.jpg')]
    # 按照文件创建时间升序排序
    jpg_files.sort(key=lambda f: time.ctime(os.path.getmtime(f)), reverse=False)
    
    # 依次重命名文件
    for idx, filename in enumerate(jpg_files, start=1):
        new_name = f"{idx}.jpg"
        print(f"Renamed {filename} to {new_name}  time:{get_modification_time(filename)}")
        os.rename(filename, new_name)
       

if __name__ == "__main__":
    rename_images()
