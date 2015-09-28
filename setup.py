import py_compile, os,cx_Freeze,sys,shutil

executables = [cx_Freeze.Executable("PythianRealms.py")]

cx_Freeze.setup(
    name="PythianRealms",
    author="Adonis Megalos",
    version="2016.132",
    options={"build_exe": {"packages":["pygame"],
                           "excludes": [],
                           "include_files":["data","graphics","music","com","changelog.md","Docs","libraries2.zip","GNU GPL.txt"]} },
    executables = executables

    )

shutil.copyfile("PythianRealms.py", 'build/exe.win32-3.2/PythianRealms.py')
