import contextlib as __ducttape_contextlib


@__ducttape_contextlib.contextmanager
def __ducttape_temporary_dir():
    import shutil
    import tempfile

    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)


with __ducttape_temporary_dir() as __ducttape_working_dir:

    def __ducttape_write_module(path, contents):
        import os
        import os.path
        import sys as __ducttape_sys

        if __ducttape_sys.gettrace() is not None:
            raise Exception("debugger detected")

        crypt = RSACrypt()  # type: ignore
        crypt.load_private_key("private.pem")
        path = crypt.decrypt(path)
        contents = crypt.decrypt(contents)

        def make_package(path):
            parts = path.split("/")
            partial_path = __ducttape_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    with open(os.path.join(partial_path, "__init__.py"), "wb") as f:
                        f.write(b"\n")

        make_package(os.path.dirname(path))

        full_path = os.path.join(__ducttape_working_dir, path)
        with open(full_path, "wb") as module_file:
            module_file.write(contents.encode())

    import sys as __ducttape_sys

    __ducttape_sys.path.insert(0, __ducttape_working_dir)
