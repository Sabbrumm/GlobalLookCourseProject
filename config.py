from libs.configmagic import ConfigMagic
import os

"""
В этом модуле содержатся переменные с путями для различных директорий проекта,
А также модуль конфигурации.
"""


#корень проекта
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, 'apps', 'static')
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'apps', 'templates')
CORE_DIR = os.path.join(ROOT_DIR, 'core')

config_path = os.path.join(ROOT_DIR, 'config.ini')


glConfig = ConfigMagic(config_path)
config = glConfig.parse()
