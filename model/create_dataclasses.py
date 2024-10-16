import shutil
import subprocess

from fastlite import create_mod

from data.fastlite_db import DB, recreate_db


recreate_db()
name = "custom_ds"
create_mod(DB, name)
shutil.move(f"{name}.py", f"model/{name}.py")
subprocess.run(["black", f"model/{name}.py"])
