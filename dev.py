import datetime
import toml

developing = True

if developing:
    time_now = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    f = open("pyproject.toml", "r")
    data = toml.load(f)
    data["project"]["version"] = data["project"]["version"] + ".dev" + time_now
    f.close()
    new_f = open("pyproject.toml", "w")
    new_f.write(toml.dumps(data))
    new_f.close()
