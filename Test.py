from FileFilter import FileFilter


fileFilter = FileFilter(".")
my_file = open("file.txt", "w+")
my_file.close()


print(fileFilter.filter())