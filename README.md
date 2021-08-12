# yaml2env
Parse and merge YAML file(s) and convert Environment Variables

## Requirements

```
apt-get install python3 python3-pip
pip3 install hiyapyco visitor
```

## Usage:

* Display the help:
  ```
  ./yaml2env -h
  ```
* Merge two config files together and output the environment variables
  ```
  ./yaml2env -f config.yaml -f config.dev.yaml
  ```  
* Dump the merged config files as YAML output
  ```
  ./yaml2env -f config.yaml -f config.foo.yaml --dump
  ```



## Create single binary with pyInstaller

### Long method

* Dependencies
```
apt-get install python3 python3-dev python3-pip python3-setuptools zlib1g-dev
pip3 install pyinstaller
```
* Instal the required python modules for yaml2env
```
pip3 install hiyapyco visitor
```
* Create binary
```
pyinstaller --onefile --console --clean --strip ./yaml2env.py
```

You will find the binary under `./dist`

### TLDR

```
docker run -it --rm -v $(pwd):/app python sh \
  -c "pip3 install pyinstaller hiyapyco visitor; \
      pyinstaller --onefile --console --clean --strip /app/yaml2env.py"
```

You will find the binary under `./dist`
