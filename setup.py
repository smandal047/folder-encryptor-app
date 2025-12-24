from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["cx-Freeze", "unittest"],
    "zip_include_packages": ["PyQt5.QtWidgets","PyQt5.QtGui","PyQt5.QtCore","cryptography.fernet"],
    "bin_path_includes": ["src"]
}


setup(
    name="Encryptor",
    version="1.0",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui.py", base="Win32GUI")],
)

# code to run setup.py
# for ref: https://cx-freeze.readthedocs.io/en/6.15.16/setup_script.html
# python setup.py bdist_msi
