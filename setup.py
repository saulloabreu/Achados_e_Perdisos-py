# import sys
# from cx_Freeze import setup, Executable
# import os

# # Dependências que devem ser incluídas no pacote
# includes = []
# excludes = []
# packages = []
# include_files = ['static', 'templates', 'DATABASES']

# # Verificar a plataforma para definir a base correta
# base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'  # Use 'Win32GUI' para aplicativos sem interface gráfica no Windows

# # Definir o executável e suas opções
# icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'digital_key.ico')
# executables = [Executable('app.py', base=base, icon=icon_path)]

# # Configuração do build
# build_options = {
#     'includes': includes,
#     'excludes': excludes,
#     'packages': packages,
#     'include_files': include_files
# }

# # Configuração principal do setup
# setup(
#     name='Achados e Perdidos',
#     version='7.3',
#     description='Sistema de Cadastro de Achados e Perdidos',
#     options={
#         'build_exe': build_options
#     },
#     executables=executables
# )

# #codigo para colocar no terminal
# # python setup.py build

import sys
from cx_Freeze import setup, Executable
import os

# Dependências que devem ser incluídas no pacote
includes = []
excludes = []
packages = []
include_files = ['static', 'templates', 'DATABASES']

# Verificar a plataforma para definir a base correta
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'  # Definido para aplicativos sem interface gráfica no Windows

# Caminho do ícone, somente para Windows
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'digital_key.ico')

# Definir o executável e suas opções
executables = [Executable('app.py', base=base, icon=icon_path if sys.platform == 'win32' else None)]

# Configuração do build
build_options = {
    'includes': includes,
    'excludes': excludes,
    'packages': packages,
    'include_files': include_files
}

# Configuração principal do setup
setup(
    name='Achados e Perdidos',
    version='7.3',
    description='Sistema de Cadastro de Achados e Perdidos',
    options={
        'build_exe': build_options
    },
    executables=executables
)
