import os
import sys

projectName = 'GCB'


def find_root_path():
    current_path = os.getcwd()
    while True:
        if os.path.exists(os.path.join(current_path, projectName)):
            return os.path.join(current_path, projectName)
        parent_path = os.path.dirname(current_path)
        if current_path == parent_path:
            return None
        current_path = parent_path


rootPth = find_root_path()
if rootPth:
    print(f"Project root path found: {rootPth}")
else:
    raise Exception("Unable to find the project root path.")

ClientCodePath = os.path.join(rootPth, "ClientCode")
WheelsPath = os.path.join(rootPth, "Wheels")
print(f"ClientCodePath: {ClientCodePath}")
print(f"WheelsPath: {WheelsPath}")