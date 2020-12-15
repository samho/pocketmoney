# coding=utf-8

from pocketmoney import dufile_class

if __name__ == "__main__":
    dufile = dufile_class.DuFile()
    dufile.run("http://dufile.com/file/a665169e9e73bd65.html")
