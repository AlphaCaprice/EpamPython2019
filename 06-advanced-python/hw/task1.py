"""
Реализовать метод __str__, позволяющий выводить все папки и файлы из данной, например так:

> print(folder1)

V folder1
|-> V folder2
|   |-> V folder3
|   |   |-> file3
|   |-> file2
|-> file1

А так же возможность проверить, находится ли файл или папка в другой папке:
> print(file3 in folder2)
True

"""
import os
import pprint


class PrintableFile:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"|-> {self.name}"


class PrintableFolder:
    def __init__(self, name: str, content=None):
        content = content or {}
        for address, dirs, files in os.walk(name):
            content[os.path.basename(address)] = (dirs, files)
        self.name = os.path.basename(name)
        self.content = content

    def __get_all_files(self, result: list, dir_name: str, counter=0) -> None:
        """ Рекурсивно обходит все директории в словаре и добавляет в список
        файлы и папки взависимости от вложенности рекурсии"""
        if counter:
            result.append("|\t"*(counter-1) + f"|-> V {dir_name}\n")
        for name in self.content[dir_name][0]:
            counter += 1
            self.__get_all_files(result, name, counter)
            counter -= 1
        for file in self.content[dir_name][1]:
            result.append("|\t"*counter + f"{str(PrintableFile(file))}\n")

    def __str__(self):
        out_str = [f"V {self.name}\n"]
        self.__get_all_files(out_str, self.name)
        return "".join(out_str)

    def __contains__(self, item: PrintableFile):
        # print(self.content[self.name][1])
        return item.name in self.content[self.name][1]



if __name__ == "__main__":
    current_path = os.path.abspath(os.curdir)
    work_path = os.path.abspath(r"..\..\06-advanced-python\hw_test1")

    pfile = PrintableFile("file4.txt")
    print(pfile)

    pfolder = PrintableFolder(work_path)
    print(pfolder)

    print(pfile in pfolder)
    print(PrintableFile("task0.py") in PrintableFolder(os.path.abspath(os.curdir)))



