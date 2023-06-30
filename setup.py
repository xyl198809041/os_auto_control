import setuptools
import os_auto_control.data

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="os_auto_control",  # Replace with your own username
    version=os_auto_control.data.v,
    author="xyl",
    author_email="author@example.com",
    description="我的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyl198809041/os_auto_control",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'schedule',
        'pyautogui',
        'opencv-python'
    ]
)
