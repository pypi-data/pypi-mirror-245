### build 방법
```
1. prerequisite
$ python -m pip install --upgrade build
$ python -m pip install --upgrade twine

$ vi pyproject.toml 에서 버전 수정
version = "1.0.20-{seq num}"
ex) "1.0.20-1"

$ vi /src/bentoml/_internal/bento/build_config.py 에서 버전 수정
ex) kcai-bentoml=="$BENTOML_VERSION".post1

2. build
$ python -m build

...
Successfully built kentoml-1.0.20.post6.tar.gz and kentoml-1.0.20.post6-py3-none-any.whl

3. deploy (cdpdev 계정)
$ python -m twine upload dist/*

Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: cdpdev
Enter your password: 

Uploading kentoml-1.0.20.post6-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 992.6/992.6 kB • 00:01 • 843.1 kB/s
Uploading kentoml-1.0.20.post6.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 19.8/19.8 MB • 00:01 • 15.2 MB/s
```

### setup
```
1. pip upgrade
$ pip install --upgrade pip

2. install
$ pip install kentoml
```