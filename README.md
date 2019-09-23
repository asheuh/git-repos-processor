# git repos processor

## Application installation

- Virtual Environment

```
$ python3 -m venv venv
$ source venv/bin/activate
```

- Dependencies

```
$ pip install -r requirements.txt
```

## Try it

- Clone from file
```
$ mkdir cloned-repos && cd cloned-repos
$ python ../run_process.py start-process {number_of_threads} {filename_with_repos}
```

- For help
```
$ python run_process.py --help
```
