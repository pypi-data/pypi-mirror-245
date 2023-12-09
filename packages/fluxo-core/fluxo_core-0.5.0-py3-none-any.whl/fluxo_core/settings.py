import os


class App:
    NAME = 'Fluxo'
    VERSION = 'v0.5.0'


settings_app = App()


class Db:
    NAME = 'database_fluxo.sqlite3'
    PATH = os.path.join(os.getcwd(), NAME)


settings_db = Db()


class PathFilesPython:
    FOLDER = 'python_files'
    PATH_FILES_PYTHON = os.path.join(os.getcwd(), FOLDER)


settings_path_files_python = PathFilesPython()
