import sys, os

def last_arg(args: list, arg: str, a: int) -> bool:
    if (a+1) >= len(args):
        print("Error: Arg {} has no value provided!")
        return True 
    return False 
    
def add_variable(name, value):
    return "{}={}\n".format(name, value)

class ParseArgs:
    source_dir = ""
    build_dir = ""

    def __init__(self, args):
        skip_next = False

        for a, arg in enumerate(args):
            if skip_next:
                skip_next = False 
                continue

            if arg == "-S" and not last_arg(args, arg, a):
                skip_next = True
                self.source_dir = args[a+1]

            if arg == "-B" and not last_arg(args, arg, a):
                skip_next = True 
                self.build_dir = args[a+1]

class Project:
    sources = []
    include_directory = ""
    link_directories = []
    project_name = ""
    memory_model = "s"
    c_path = ""

    def __init__(self, project_name):
        self.project_name = project_name

    def add_sources(self, *sources):
        for source in sources:
            self.sources.append(source)
    
    def set_include_dir(self, include):
        self.include_directory = include

    def set_memory_model(self, model):
        self.memory_model = model
        
    def set_c_path(self, path):
        self.c_path = os.path.abspath(path)

    def configure(self) -> bool:
        args = ParseArgs(sys.argv)
        makefile = ""
        
        source_dir = os.path.abspath(args.source_dir)
        build_dir = os.path.abspath(args.build_dir)
        
        if self.c_path == "":
            print("C Path must be set. Aborting!")
            return False

        if source_dir == "":
            print("Source dir not provided. Aborting!")
            return False 
        if args.build_dir == "":
            print("Build dir not provided. Aborting!")
            return False 
        if source_dir == build_dir:
            print("Source and build dir are equal. Not valid! Aborting!")
            return False
            
        dos_source_dir = source_dir.replace(self.c_path, "C:")
        dos_build_dir = build_dir.replace(self.c_path, "C:")

        makefile += add_variable("SOURCE_DIR", dos_source_dir)
        makefile += add_variable("BUILD_DIR", dos_build_dir)
        makefile += add_variable("PROJECT_NAME", self.project_name)
        
        clean_target = "\nclean:\n"

        objs = ""

        project_target = "\n{}:\n".format(self.project_name)
        for i, source in enumerate(self.sources):
            obj = "{}.obj ".format(i)
            clean_target += "\tdel {}\n".format(obj)
            objs += obj
            if source.endswith(".asm"):
                project_target += "\ttasm -mx $(SOURCE_DIR)/{} -o $(BUILD_DIR)/{}.obj\n".format(source, i)
            else:
                project_target += "\ttcc -m{} -I$(SOURCE_DIR)/{} -n$(BUILD_DIR) -c -o{}.obj $(SOURCE_DIR)/{}\n".format(self.memory_model, self.include_directory, i, source)
        
        project_target += "\ttcc -m{} -e$(PROJECT_NAME) {}\n".format(self.memory_model, objs)

        makefile += project_target + "\n"
        makefile += clean_target 
        
        with open(args.build_dir + "/Makefile", "w") as f:
            f.write(makefile.replace("/", "\\"))

        return True

