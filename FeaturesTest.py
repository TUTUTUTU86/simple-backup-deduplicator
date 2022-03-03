import os


class FeaturesTest:

    @staticmethod
    def osWalkTest(root_dir):
        for root, dirs, files in os.walk(root_dir):
            print("Root "+root + " has: ")
            print()
            print("Directories: ")
            for dir in dirs:
                print(dir + " ")
            print()
            print("Files: ")
            for file in files:
                print(file + " ")

