import py_compile, os,cx_Freeze,sys,shutil

os.chdir("C:\\Users\\Scratso\\Documents\\GitHub\\PythianRealms-Dev")

executables = [cx_Freeze.Executable("PythianRealms.py")]

cx_Freeze.setup(
    name="PythianRealms",
    author="Damian Heaton",
    version="0.0.0.1",
    options={"build_exe": {"packages":["pygame"],
                           "excludes": [],
                           "include_files":["data","graphics","music","changelog.md","Docs","libraries2.zip"]} },
    executables = executables

    )

shutil.copyfile("PythianRealms.py", 'build/exe.win32-3.2/PythianRealms.py')
#py_compile.compile("dbstuff.pyc", 'PythianRealms-Dev/build/dbstuff.pyc')

##os.remove("build/nsis/dbstuff.py")
##os.remove("build/nsis/pythianrealms.py")
##
##from distutils.core import setup
##setup(name='PythianRealms',
##      version='0.0.0.3',
##      py_modules=['PythianRealms'],
##      )
