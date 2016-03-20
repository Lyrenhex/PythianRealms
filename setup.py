import cx_Freeze
import shutil

executables = [cx_Freeze.Executable("PythianRealms.py",
                                    icon="icon.ico",
                                    shortcutName="PythianRealms 2016 [Google]",
                                    shortcutDir="DesktopFolder")]

# version number:
# a.b.c
#
# where a is 0, or 1. 0 = non-release, 1 = release. (beta and below is 0)
# b is the year of release.
# c is the edit number (147, as an example.)

cx_Freeze.setup(
    name="PythianRealms 2016 [Google]",
    author="Adonis Megalos",
    version="0.2016.147",
    options={"build_exe": {"packages":["pygame"],
                           "excludes": [],
                           "include_files":["data","graphics","music","com","changelog.md","Docs","libraries2.zip","GNU GPL.txt"]},
             "bdist_msi": { } },
    executables = executables

    )

print("copying PythianRealms.py -> build/exe.win32-3.2")
shutil.copyfile("PythianRealms.py", 'build/exe.win32-3.2/PythianRealms.py')
print("compiled.")
