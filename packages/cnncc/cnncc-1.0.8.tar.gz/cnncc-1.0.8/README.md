### Build package 

```console
$ python setup.py sdist bdist_wheel
```

### Reinstall package 

```console 
$ pip install dist/<package-name> --force-reinstall
```

### Publish package to PyPi 

```console
$ twine upload dist/*
```