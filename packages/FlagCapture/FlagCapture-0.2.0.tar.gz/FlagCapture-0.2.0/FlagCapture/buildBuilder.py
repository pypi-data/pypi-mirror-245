file = open('newBuild.py', 'w')
file.write("""import os
import shutil

def get_real_path(file):
    abs_path_module = os.path.realpath(__file__)
    module_dir, _ = os.path.split(abs_path_module)
    path = os.path.join(module_dir, file)
    return path

def get_dir_path():
    abs_path_module = os.path.realpath(__file__)
    module_dir, _ = os.path.split(abs_path_module)
    return module_dir

def BUILD():
    if not os.path.exists(get_real_path('zip.zip')):
        file = open(get_real_path('zip.zip'), 'wb')
        """)

zipedfile = open('zip.zip', 'rb')
zipInfo = zipedfile.read()
zipedfile.close()

file.write(f"""Data={zipInfo}""")

file.write("""
        file.write(Data)
        file.close()
        shutil.unpack_archive(get_real_path('zip.zip'), extract_dir=get_dir_path())""")
file.close()
        