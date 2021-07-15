from cx_Freeze import setup, Executable


executables = [Executable('main.py', target_name='dromSearch.exe')]


excludes = ['pygame', 'unittest', 'tkinter', 'numpy', 'concurrent', 'ctypes', 'distutils', 'PyQt5']

include_files = ['.env', 'cars', 'config.json', 'readme.txt', 'logs']


options = {'build_exe': {
      'include_msvcr': True,
      'excludes': excludes,
      'include_files': include_files,
      }
}


setup(name='dromSearch',
      version='1.0',
      description='ищем на дроме машинки',
      executables=executables,
      options=options
      )
