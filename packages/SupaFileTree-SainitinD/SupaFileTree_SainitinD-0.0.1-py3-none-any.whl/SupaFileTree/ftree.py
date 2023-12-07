import os

class FileTree():
    def __init__(self, input_path, out_path=None, treeignore_path=None):
        self.input_path = input_path        
        self.out_path = out_path
        self.treeignore_path = treeignore_path
        self.ignore_folders = []
        self._read_tree_ignore()
    
    
    def _read_tree_ignore(self):
        if treeignore_path:
            print(f"Received tree ignore path: {self.treeignore_path}")
        else:
            print(f"Not received tree ignore path. Using input path: {self.input_path}")
            self.treeignore_path = self.input_path
        
        treeignore_path = os.path.join(self.tree_ignore_path, ".treeignore")

        # Optional: Reads provided '.treeignore' to not consider certain files/folders
        if os.path.isfile(treeignore_path):
            with open(treeignore_path) as f:
                self.ignore_folders = f.read().split("\n")
            print("Tree Ignore FOUND! Not considering the following files/folders \n", self.ignore_folders)
        else:
            print("Tree Ignore NOT Found. Continuing the process...")


    def create_file_tree(self, path=None, last_folder=False):
        """
        Creates a file tree when given a path.
        
        Args:
                path (string): A string containing the input path of the folder. Default value is the input_path
                last_folder (boolean): A boolean indicating if the path given is the last folder in the tree.
                                    Intended to be used by sub-folders so don't touch it unless you have to.
                                    Used to help formatting. 
            Returns:
                out (string): A string containing the file tree of the given path 
        """
        # Uncomment for debugging
        # print(path)
        
        if not path: path = self.input_path
        print(f"Received input path: {self.input_path}")

        if out_path:
            print(f"Received output path: {self.out_path}")
        else:
            print(f"Not received output path. Using input path: {self.input_path}")
            self.out_path = self.input_path
        
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

                folder_out = create_file_tree(cur_path, is_last_folder)
                folder_out = folder_out.split("\n")[:-1]
                for line in folder_out:
                    if is_last_folder:
                        out = out + "    " + line + "\n"
                    else:
                        out = out + "│   " + line + "\n"
        
        print("Starting the process...")
        out = create_file_tree(input_path)
        with open(os.path.join(output_path, "out.txt"), "w", encoding="utf-8") as f:
            f.write(out)
        print("Successfully Completed :D")
        print(f"Output stored at... {os.path.join(output_path, 'out.txt')}")
        
        return out