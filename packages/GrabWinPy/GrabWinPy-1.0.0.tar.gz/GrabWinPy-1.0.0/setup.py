from setuptools import setup, find_packages

setup(
    name='GrabWinPy',
    version='1.0.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description='Take Screenshots of specific window',
    include_package_data=True,
    install_requires=[
        'pyautogui>=0.9.53',
        'pygetwindow>=0.0.9'
    ],
)
