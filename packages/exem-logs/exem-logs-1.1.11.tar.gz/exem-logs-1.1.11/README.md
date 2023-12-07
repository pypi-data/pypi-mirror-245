# Logs

### Log anything from anywhere.

A better and simplified logging system.

## Getting started

### To add this library to your project
 * Directly use the git command:
```
git clone https://gitlab.com/exem2/libraries/logs.git
```

 * As a submodule use the git command:
```
git submodule add https://gitlab.com/exem2/libraries/logs.git
```

*You need your project to be git init to add this project as a submodule.*

### How it works

Initialise your log with:

    log = Log()

To log info, warning, error or debug use the corresponding methods:

    log.info("This is an info")
    log.warning("This is a warning")
    log.error("This is an error")
    log.debug("This is a debug")

A folder named **logs** will automatically be created at the root of the project.

When logging a folder with the *current date* as name is created in the **logs** folder, and a file for each script 
that as a log is created with the corresponding script as name.

ex: *logs/2021-05-05/main.log*

The **any.log** file in each sub **logs** folder contains all the logs from all the scripts.

In the case you don't launch your project with a main script at the root of the project, or if you want to log in a
specific folder, you can use `Log.set_root()` to set the root folder of the logs.

More details in [Log.py](Log.py)

If you are using an old version of python <= 3.6, before installing the library you need to do:

    pip3 install --upgrade pip
    python3 -m pip install --upgrade setuptools
