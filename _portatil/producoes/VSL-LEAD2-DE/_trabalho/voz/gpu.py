import os, glob, site
for sp in site.getsitepackages():
    for d in glob.glob(os.path.join(sp, "nvidia", "*", "bin")):
        os.add_dll_directory(d); os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]
