import sys

def save(conf, file_path):
    fw = open(file_path, 'w')
    for key in conf.__dict__:
        fw.write(key + "=" + conf.__dict__[key] + "\n")
