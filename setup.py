import cx_Freeze
import shutil

executables = [cx_Freeze.Executable("PythianRealms.py",
                                    icon="icon.ico")]

cx_Freeze.setup(
    name="PythianRealms",
    author="Damian Heaton",
    version="0.1.1",
    options={"build_exe": {"packages":["pygame"],
                           "excludes": [],
                           "include_files":["data","graphics","music","com","changelog.md","Docs","libraries2.zip","GNU GPL.txt"]},
             "bdist_msi": { } },
    executables = executables

    )

print("copying PythianRealms.py -> build/exe.win32-3.2")
shutil.copyfile("PythianRealms.py", 'build/exe.win32-3.2/PythianRealms.py')
print("compiled.")
