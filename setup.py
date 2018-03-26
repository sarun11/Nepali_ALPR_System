from cx_Freeze import setup, Executable

setup(name='ALPRsystem',
      version='0.1',
      description='ALPR system using ANN',
      options = {"build_exe": {"packages": ["cv2", "numpy", "decimal", "os", "shutil","wx","pickle","scipy"], "include_files": []}},
      executables= [Executable("main.py", base = "Win32GUI")])

