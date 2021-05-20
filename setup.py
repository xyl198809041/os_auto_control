import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="os_auto_control",  # Replace with your own username
    version="1.2",
    author="xyl",
    author_email="author@example.com",
    description="我的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyl198809041/os_auto_control",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'schedule'
    ]
)
