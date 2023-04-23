from collections import namedtuple

FileTree = namedtuple('FileTree', ['dirs', 'files', 'parent'])

# implement terminal class
class Terminal:
    def __init__(self):
        self.curr_root= '/'
        self.file_trees = {}
        self.file_trees[self.curr_root] = FileTree([], [], self.curr_root)

    # input command, and return current root and output
    # cd {dir}
    # mkdir {dir}
    # ls {dir}
    # rm {dir}
    # pwd
    def input(self, cmd_line):
        # split cmd into command and argument
        cmd = cmd_line.split(' ')[0]
        arg = cmd_line.split(' ')[1] if len(cmd_line.split(' ')) > 1 else ''

        if cmd == 'ls':
            return self.curr_root, self.ls()
        elif cmd == 'cd':
            return self.cd(arg), ''
        elif cmd == 'mkdir':
            self.mkdir(arg)
            return self.curr_root, ''
        elif cmd == 'rm':
            self.rm(arg)
            return self.curr_root, ''
        elif cmd == 'pwd':
            return self.curr_root, self.curr_root
        else:
            return self.curr_root, ''

    def ls(self):
        files_and_dirs = ''
        for dir in self.file_trees[self.curr_root].dirs:
            files_and_dirs += dir + '/ '
        for file in self.file_trees[self.curr_root].files:
            files_and_dirs += file + ' '
        return files_and_dirs

    def cd(self, dir):
        if dir == '..':
            self.curr_root = self.file_trees[self.curr_root].parent
        elif dir == '.':
            pass
        elif dir in self.file_trees[self.curr_root].dirs:
            self.curr_root += dir + '/'
        elif dir[0] == '/':
            self.curr_root = dir
        return self.curr_root

    def mkdir(self, dir):
        if len(dir) == 0 or dir in self.file_trees[self.curr_root].dirs:
            return
        self.file_trees[self.curr_root].dirs.append(dir)
        print(self.file_trees[self.curr_root].dirs)
        self.file_trees[self.curr_root + dir + '/'] = FileTree([], [], self.curr_root)

    def rm(self, dir):
        if dir in self.file_trees[self.curr_root].dirs:
            self.file_trees[self.curr_root].dirs.remove(dir)
            del self.file_trees[self.curr_root + dir + '/']
        elif dir in self.file_trees[self.curr_root].files:
            self.file_trees[self.curr_root].files.remove(dir)
        return self.curr_root

    def pwd(self):
        return self.curr_root
