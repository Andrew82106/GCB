"""
一键更新base包脚本
"""
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
shutil.rmtree(local_base_path)
shutil.copytree(remote_base_path, local_base_path)
print("Base package updated successfully.")