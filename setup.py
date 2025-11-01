from setuptools import setup
from Cython.Build import cythonize
# for linux編譯
# 指定您想要編譯的 .py 檔案
modules_to_compile = [
    "app/models.py",
    "app/routes.py"
]

setup(
    ext_modules=cythonize(modules_to_compile, compiler_directives={'language_level': "3"})
)