
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
   git tag -a v0.1.7 -m "Release version 0.1.7"
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
