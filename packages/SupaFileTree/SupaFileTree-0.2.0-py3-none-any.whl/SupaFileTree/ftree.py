import os

class FileTree():
    def __init__(self, input_path, out_path=None, tree_ignore_path=None, debug=False):
        self.input_path = input_path        
        self.out_path = out_path
        self.tree_ignore_path = tree_ignore_path
        self.debug = debug
        self.ignore_folders = []
        self._read_tree_ignore()
    
    
    def _read_tree_ignore(self):
        """
        Reads the .treeignore file at the tree ignore path or input path. Intended to be used internally
        """
        if self.tree_ignore_path:
            if self.debug: print(f"Received tree ignore path: {self.tree_ignore_path}")
        else:
            if self.debug: print(f"Not received tree ignore path. Using input path: {self.input_path}")
            self.tree_ignore_path = self.input_path
        
        self.tree_ignore_path = os.path.join(self.tree_ignore_path, ".treeignore")

        # Optional: Reads provided '.treeignore' to not consider certain files/folders
        if os.path.isfile(self.tree_ignore_path):
            with open(self.tree_ignore_path) as f:
                self.ignore_folders = f.read().split("\n")
            if self.debug: print("Tree Ignore FOUND! Not considering the following files/folders \n", self.ignore_folders)
        else:
            if self.debug: print("Tree Ignore NOT Found. Continuing the process...")

    def create(self):
        """
        Creates a file tree using the provided input path and stores it in "out.txt" in the provided output path (or in inputpath)
        """
        if self.debug: print(f"Received input path: {self.input_path}")

        if self.out_path:
            if self.debug: print(f"Received output path: {self.out_path}")
        else:
            if self.debug: print(f"Not received output path. Using input path: {self.input_path}")
            self.out_path = self.input_path
        
        
        print("Starting the process...")
        out = self._create_file_tree(self.input_path)
        with open(os.path.join(self.out_path, "out.txt"), "w", encoding="utf-8") as f:
            f.write(out)
        print("Successfully Completed :D")
        print(f"Output stored at... {os.path.join(self.out_path, 'out.txt')}")
        
        return out
        
        

    def _create_file_tree(self, path, last_folder=False):
        """
        Creates a file tree when given a path. Intended to be used internally.
        
        Args:
                path (string): A string containing the input path of the folder
                last_folder (boolean): A boolean indicating if the path given is the last folder in the tree.
                                    Intended to be used by sub-folders so don't touch it unless you have to.
                                    Used to help formatting. 
            Returns:
                out (string): A string containing the file tree of the given path 
        """
        # Uncomment for debugging
        if self.debug: print(path)
        
        out = ""
        files = os.listdir(path)
        files = [f for f in files if f not in self.ignore_folders]  # O(N*K)
        
        # Handle edge case
        if len(files) == 0:
            return out
        elif len(files) == 1:
            if os.path.isfile(files[0]):
                out += f"└── {files[0]}\n"
                return out

        for i, file_name in enumerate(files):
            # Add files/folders into file tree
            cur_path = os.path.join(path, file_name)
            if i != len(files)-1:
                out = out +  f"├── {file_name}\n"
            else:
                out += f"└── {file_name}\n"
            

            # if file is a folder, format and add contents of the folder into the file tree
            if not os.path.isfile(cur_path):
                is_last_folder = False if i != len(files)-1 else True

                folder_out = self._create_file_tree(cur_path, is_last_folder)
                folder_out = folder_out.split("\n")[:-1]
                for line in folder_out:
                    if is_last_folder:
                        out = out + "    " + line + "\n"
                    else:
                        out = out + "│   " + line + "\n"
        
        return out