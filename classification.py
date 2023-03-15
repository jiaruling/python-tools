import os
import sys
import re
import shutil
from unrar import rarfile
from typing import List, Tuple

"""
    项目资源管理器
"""

# 扫描当前目录下的文件夹名称
filepath = os.getcwd()  # 获取文件当前工作目录路径
readfile = "readme.md"
menufile = "menu.md"
buffer = "【未检查】"
output = []
suffix_rar = "rar"
suffix_py = "py"
requirements = "requirements.txt"
backup = "d:\\backup"


# done: 解压加密rar文件
def UnRar(name: str, path: str, destDir: str, pwd:str=None):
    # 解压
    try:
        print(f"正在解压【{name}】文件")
        rar_file = rarfile.RarFile(path, "r", pwd)
        rar_list = rar_file.namelist() # 得到压缩包里所有文件
        for f in rar_list:
            print(f"{f}...")
            rar_file.extract(f, destDir)
        print(f"解压文件【{name}】完成")
    except Exception as e:
        print(f"解压文件【{name}】失败：{e}")
    return

# 删除url文件
def DeleteFile(path: str):
    os.remove(path)
    print(f"delete file -> {f}")

# done: 文件目录重名了
def Rename(name: str) -> str:
    """
        eg:
            这是【参考】一本书  -> 这是一本书
            这是【参考】       -> 这是
            【参考】一本书      -> 一本书
            这是一本书         -> 这是一本书
    """
    matchObj = re.search(r"【.*】", name, re.M|re.I)
    if matchObj:
        return name[:matchObj.start()] + name[matchObj.end():]
    else:
        return name

# 文件备份
def Backup(path):
    shutil.move(path, backup)
    return

# done: 添加目录文件
def AddMenu(path: str, title: str):
    path = os.path.join(path, menufile)
    if not os.path.exists(path):
        try:
            # 没有就添加，并写入【未检查】
            f = open(path, "w", encoding='utf-8')
            f.write("# " + title)
        except Exception as e:
            print(f"添加目录文件 {path} 失败")
        finally:
            if f:
                f.close
    return

# done: 添加readme文件
def AddReadme(path: str):
    out = os.path.basename(path)
    path = os.path.join(path, readfile)
    try:
        # 读取readme.md文件
        f = open(path, 'r', encoding="utf-8")
        line = f.readline()
        while line:
            line = line.strip()
            if line:
                out = out +  f" -> {line}"
            line = f.readline()
    except Exception as e:
        # 没有就添加，并写入【未检查】
        f = open(path, "w", encoding='utf-8')
        f.write(buffer)
        out = out + f" -> {buffer}"
    finally:
        if f:
            f.close
        output.append(out)
    return

# done: 获取文件前缀和后缀
def GetFix(name: str) -> Tuple:
    fix = os.path.splitext(name)
    prefix = fix[0]       # 前缀
    suffix = fix[-1][1:]  # 后缀
    return prefix, suffix

# done: 给压缩包创建解压文件夹
def CreateDir(name: str) -> Tuple:
    newName = GetFix(Rename(name))[0]
    os.mkdir(newName)
    newPath = os.path.join(root, newName)
    return newName, newPath

# 删除当前目录及子目录下指定文件
def DeletedSpecificFile(name: List[str]):
    path = os.getcwd()  # 获取文件当前工作目录路径
    for root,dirs,files in os.walk(path):
        for file in files:
            if file in name:
                print(f"删除文件: {os.path.join(root, file)}")
                os.remove(os.path.join(root, file))

# 给指定目录下文件解压
def UnrarSpecificDir(pwd: str):
    path = os.getcwd()  # 获取文件当前工作目录路径
    for root,dirs,files in os.walk(path):
        for file in files:
            prefix, suffix = GetFix(file)
            if suffix == suffix_rar:
                # 解压
                try:
                    print(f"正在解压【{file}】文件")
                    rar_file = rarfile.RarFile(os.path.join(root, file), "r", pwd)
                    rar_list = rar_file.namelist() # 得到压缩包里所有文件
                    for f in rar_list:
                        rar_file.extract(f, root)  # 解压到当前文件夹
                    print(f"解压文件【{file}】完成")
                except Exception as e:
                    print(f"解压文件【{file}】失败：{e}")

# 给指定目录下文件及文件夹重命名
def RenameAll():
    path = os.getcwd()  # 获取文件当前工作目录路径
    for root,dirs,files in os.walk(path):
        # 重命名文件
        for f in files:
            if Rename(f) != f:
                print(f"重命名文件: {f} -> {Rename(f)}")
                os.rename(os.path.join(root, f), os.path.join(root, Rename(f)))
        # 重名了文件夹
        for d in dirs:
            if Rename(d) != d:
                print(f"重命名目录: {d} -> {Rename(d)}")
                os.rename(os.path.join(root, d), os.path.join(root, Rename(d)))

# 创建备份
def CreateBackup():
    root = os.getcwd()  # 获取文件当前工作目录路径
    for f in os.listdir(root):
        path = os.path.join(root, f)
        if os.path.isdir(path):
            shutil.copyfile(path, os.path.join(backup, path))

# 删除指定备份
def DeleteBackup():
    os.chdir(backup)
    pass

# 删除所有备份
def DeleteBackupAll():
    os.chdir(backup)
    root = os.getcwd()  # 获取文件当前工作目录路径
    for f in os.listdir(root):
        path = os.path.join(root, f)
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    return

# 比较两个目录或文件时候相同
def Compare():
    pass

# 更新备份
def UpdateBackup():
    pass

# 设置工作目录
def SetWorking():
    if len(sys.argv) > 1:
        os.chdir(os.path.join(os.getcwd(), sys.argv[1]))
    else:
        os.chdir(os.getcwd())
    print(f"Working:{os.getcwd()}")

def main():
    root = os.getcwd()  # 获取文件当前工作目录路径
    for f in os.listdir(root): # 读取当前路径下的所有文件夹以及文件
        path = os.path.join(root, f)
        # 目录
        if os.path.isdir(path):
            # done: 添加readme和添加目录
            AddReadme(path)
            AddMenu(path, Rename(f))
        # 文件
        elif os.path.isfile(path):
            prefix, suffix = GetFix(f)
            # done: 压缩文件
            if suffix in suffix_rar:
                # 解压
                newName, destDir = CreateDir(f)
                UnRar(newName, path, destDir)
                AddReadme(destDir)
                AddMenu(destDir, newName)
                # Backup(newPath)
            # .py文件
            elif suffix == suffix_py or f == requirements:
                # done: 忽略python脚本文件和依赖文件
                print(f"ignore file -> {f}")
            # 其它文件
            else:
                # done: 删除根目录下的冗余文件
                os.remove(path)
                print(f"delete file -> {f}")
        else:
            print(f"{f} is err")

    # 打印结果
    for item in output:
        print(item)


if __name__ == '__main__':
    SetWorking()
    UnrarSpecificDir(sys.argv[2] if len(sys.argv) == 3 else None)
    RenameAll()
    DeletedSpecificFile([readfile,menufile])
