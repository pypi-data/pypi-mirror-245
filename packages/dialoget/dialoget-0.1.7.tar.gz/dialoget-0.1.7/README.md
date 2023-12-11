# [dialoget](htttp://www.dialoget.com) - python library

[![PyPI](https://img.shields.io/pypi/v/dialoget?style=flat-square)](https://pypi.org/project/dialoget/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/dialoget.svg)](https://pypi.org/project/dialoget/)
[![Downloads](https://static.pepy.tech/badge/dialoget/month)](https://pepy.tech/project/dialoget)
[![check](https://github.com/dialoget/python/actions/workflows/check.yml/badge.svg)](https://github.com/dialoget/python/actions/workflows/check.yml)
[![Documentation Status](https://docs.org/dialoget/python/badge/?version=latest)](https://docs.dialoget.com/en/latest/?badge=latest)

python.dialoget.com is a test framework for multilanguage source code, based on decorators

The test directory structure for Python and Java projects will often follow conventions that are supported by popular testing frameworks and project management tools.
Below, are typical structures for both languages, which help in organizing tests based on their type (e.g., unit tests, functional tests, integration tests).


## Project
```
dialoget/
│
├── src/
│   └── dialoget.py       # Python file with code for the package
│
├── tests/               # Unit tests for the package
│   └── dialoget.py
│
├── docs/                # Documentation for the package
│   ├── conf.py
│   ├── index.rst
│   └── ...
│
├── README.md            # README file with a description of the package, installation instructions, etc.
├── LICENSE              # License file specifying how the package can be used and shared
├── pyproject.toml       # Setuptools script for installation and distribution of the package
├── setup.cfg            # Configuration settings for setuptools
├── requirements.txt     # File listing all dependencies for the package
└── .gitignore           # Specifies intentionally untracked files to ignore for git
```


## Usage

```bash
pip install dialoget==0.0.1
```



## Contribution


### Github preparation

+ [Git - First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
   ```shell
   git config --global user.name "John Doe"
   git config --global user.email johndoe@example.com
   ```
  
+ [About remote repositories - GitHub Docs](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls)
```shell
ssh-keygen -p -f ~/.ssh/id_ed25519
```

+ [SSH and GPG keys on Github](https://github.com/settings/keys)
```shell
cat ~/.ssh/id_ed25519.pub
```

if, after git push will ask for credentials put the API key as passwort
+ [Personal Access Tokens (Classic)](https://github.com/settings/tokens)


### Repository update

To update a release of a Python package, you'll typically go through the following general steps:

1. Update the code or documentation to incorporate the new changes or improvements.
   
2. Update the package version number to indicate a new release:
   - Follow semantic versioning (or "semver") principles, using version numbers like MAJOR.MINOR.PATCH:
     - Increment the MAJOR version when you make incompatible API changes,
     - Increment the MINOR version when you add functionality in a backward-compatible manner, and
     - Increment the PATCH version when you make backward-compatible bug fixes.
   - Change the version number in your package's `__init__.py` file, `setup.cfg`, `pyproject.toml` file, wherever it's defined.

3. Update the `CHANGELOG` or `HISTORY` file (if you have one) to document the changes introduced in the new version.

4. Commit the changes and push them to your version control system (e.g., git).
   ```shell
   git status
   git add .
   git commit -m "updated version"
   git push
   ```
   
5. Tag the commit with the version number:
   ```shell
   git tag -a v0.1.5 -m "Release version 0.1.5"
   git push --tags
   ```
   
## Build
+ [build 1.0.3](https://pypa-build.readthedocs.io/en/latest/)

Build the new distribution files for the package using your chosen build tool, typically the build package:
Run the build module from the root of the project where the `pyproject.toml` file is located:
This command will generate distribution files in the newly created `dist/` directory within your project. You will find both a source archive (`.tar.gz`) and a wheel file (`.whl`).
   ```shell
   pip install build
   python -m build --version 0.1.5
   python -m build
   ```


+ [Versioning - Hatch](https://hatch.pypa.io/latest/version/)
```bash
hatch version release
```

### Publish
After the build completes successfully, upload the new distribution files to the Python Package Index (PyPI).
Upload your package to PyPI using `twine`
   ```shell
   twine upload dist/*
   ```

### Github Release



If your project is hosted on GitHub or a similar platform, you may also want to create a GitHub release:
- Go to the "Releases" section of your repository.
- Draft a new release, using the new tag you've created.
- Add release notes summarizing the changes.
- Optionally, attach binaries or additional files that accompany the release.
- Publish the release.


### Test
```bash
pytest
```

## Strategies

### Python

In Python projects, tests are often placed in a separate directory, commonly named `tests`. Each category of test may be placed in its own subdirectory. Here is an example structure that might be used in a Python project:

```
my_python_project/
│
├── my_project/
│   ├── module1.py
│   └── module2.py
│
├── tests/
│   ├── unit/
│   │   ├── test_module1.py
│   │   └── test_module2.py
│   │
│   ├── functional/
│   │   └── test_something_functional.py
│   │
│   └── integration/
│       └── test_integration.py
│
└── setup.py (or pyproject.toml, or requirements.txt, depending on the project)
```

This structure separates the test types into different subdirectories, making it easier to manage them and execute them separately. Note that each test directory typically contains an `__init__.py` file, which is necessary for the Python test discovery mechanisms in most testing frameworks, such as `unittest` or `pytest`.

### Java

Java projects often use Maven or Gradle as build tools, and the default conventions for these tools define specific directories for different types of tests. Here's how a Maven project might structure its tests:

```
my_java_project/
│
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── mycompany/
│   │               └── myproject/
│   │                   ├── Module1.java
│   │                   └── Module2.java
│   │
│   └── test/
│       ├── java/
│       │   └── com/
│       │       └── mycompany/
│       │           └── myproject/
│       │               ├── unit/
│       │               │   ├── Module1Test.java
│       │               │   └── Module2Test.java
│       │               │
│       │               ├── functional/
│       │               │   └── SomethingFunctionalTest.java
│       │               │
│       │               └── integration/
│       │                   └── IntegrationTest.java
│       │
│       └── resources/
│
└── pom.xml
```

In this structure, all Java source files are located in `src/main/java`, and test files are located in `src/test/java`. Tests are further organized into subdirectories (unit, functional, and integration), corresponding to each type of test within the `test` directory.

It's important to note that while you can organize the tests into subdirectories in Java, the use of package naming conventions is more common. Test frameworks like JUnit do not enforce a particular directory structure, but they do differentiate tests based on annotations or naming conventions within the code.

The Maven directory structure (`src/main/java` for source code and `src/test/java` for test code) is a convention that tools recognize, and they are configured to compile and execute tests based on this layout.

As best practice, both Python and Java projects should have good separation of test types. This makes it clear what each test is designed to achieve and allows for the selective execution of test suites based on the scope of changes or the stage of the development pipeline.