import shutil

from base.pathconfig import Pathconfig
import os

cfg = Pathconfig()

local_base_path = cfg.basePath
print(local_base_path)

remote_base_path = cfg.rootPth

while True:
    if os.path.exists(os.path.join(remote_base_path, 'GCB')):
        remote_base_path = os.path.join(remote_base_path, 'GCB')
        break

    remote_base_path = os.path.dirname(remote_base_path)

remote_base_path = os.path.join(remote_base_path, 'base')
print(remote_base_path)

# 将local_base_path下的文件全部删掉
for file in os.listdir(local_base_path):
    file_path = os.path.join(local_base_path, file)
    shutil.rmtree(file_path)
    print(f"Deleted file: {file_path}")

# 将remote_base_path下的文件全部复制到local_base_path
for file in os.listdir(remote_base_path):
    src_file = os.path.join(remote_base_path, file)
    dest_file = os.path.join(local_base_path, file)
    shutil.copyfile(src_file, dest_file)
    print(f"Copied file: {dest_file}")

print("Base package updated successfully.")
