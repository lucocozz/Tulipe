from cx_Freeze import setup, Executable
from tulipe import __version__

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

BASE = 'console'

executables = [
    Executable('.', base=BASE, target_name = 'tulipe')
]

setup(name='Tulipe',
      version = __version__,
      description = 'Tulipe is a lightweight tool designed to lists the ports used on a machine and the associated processes, including those in Docker containers.',
      options = {'build_exe': build_options},
      executables = executables,
      url = "https://github.com/lucocozz/Tulipe",
      author = "Luigi Cocozza",
    )
