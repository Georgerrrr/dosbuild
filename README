#DOSBUILD

A really simple build tool for generating makefiles to be used with Borlands C and dosbox.

You create a python file in your source tree to configure the makefile.

Example:

configure.py

```py 
from dosbuild import Project

test = Project("test")

test.add_sources(
        "src/main.c",
        "src/second.c"
)
test.set_include_dir("includes")
test.set_c_path("/home/user/Documents/DOS/c/")
test.set_memory_model("c") # s for small, c for compact, etc... For full list see Borlands C manual.
test.configure()
```

To run

```
mkdir build 
cd build
python ../configure.py -S .. -B .
```

This will generate a makefile which can be used inside of dosbox to compile a project.

This project is simple and really just for me there may be better alternatives out there, I don't know. 
