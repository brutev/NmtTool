from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name = 'nmtcli',
    version = '0.0.1',
    author = 'Novac Mobile Team',
    author_email = 'novacmobileteam@gmail.com',
    license = 'MIT',
    description = 'CLI tool for automating repetitive task',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = '<github url where the tool code will remain>',
    py_modules = ['nmt_cli', 'app'],
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'cooltool=nmt_cli:cli',
        ],
    }
)


# from setuptools import setup, find_packages
# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
# with open("requirements.txt", "r", encoding="utf-8") as fh:
#     requirements = fh.read()
# setup(
#     name = 'nmtcli',
#     version = '0.0.1',
#     author = 'Novac Mobile Team',
#     author_email = 'novacmobileteam@gmail.com',
#     license = 'MIT',
#     description = 'CLI tool for automating repetitive task',
#     long_description = long_description,
#     long_description_content_type = "text/markdown",
#     url = '<github url where the tool code will remain>',
#     py_modules = ['nmt_cli', 'app'],
#     packages = find_packages(),
#     install_requires = [requirements],
#     python_requires='>=3.7',
#     classifiers=[
#         "Programming Language :: Python :: 3.8",
#         "Operating System :: OS Independent",
#     ],
#     entry_points = '''
#         [console_scripts]
#         cooltool=my_tool:cli
#     '''
# )