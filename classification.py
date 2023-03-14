import os
import zipfile
import shutil

"""
    项目资源管理器
"""

# 扫描当前目录下的文件夹名称
filepath = os.getcwd()  # 获取文件当前工作目录路径
readfile = "readme.md"
buffer = "【未检查】"
output = []
suffix_package = [".zip", ".rar"]
suffix_py = ".py"
backup = "C:\\Users\\Public\\Documents"

# 读取当前路径下的所有文件夹以及文件
for f in os.listdir(filepath):
    path = os.path.join(filepath, f)
    # 项目
    if os.path.isdir(path):
        path = os.path.join(path, readfile)
        out = path
        try:
            # 读取readme.md文件
            f = open(path, 'r', encoding="utf-8")
            line = f.readline()
            while line:
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
            out.replace("\n", "")
            output.append(out)
    # 文件
    elif os.path.isfile(path):
        suffix = os.path.splitext(f)[-1]
        # 压缩文件
        if suffix in suffix_package:
            # 创建与压缩包同名的文件夹
            preffix = os.path.splitext(f)[0]
            os.mkdir(preffix)
            # 解压
            try:
                print(f"正在解压【{f}】文件")
                zip_file = zipfile.ZipFile(path, "r")
                zip_list = zip_file.namelist() # 得到压缩包里所有文件
                for ff in zip_list:
                    zip_file.extract(ff, os.path.join(filepath, preffix))
                print(f"解压文件【{f}】完成")
            except Exception as e:
                print(f"解压文件【{f}】失败")
                print(e)
            finally:
                zip_file.close()
            # 添加readme.md文件
            try:
                # 没有就添加，并写入【未检查】
                f = open(os.path.join(os.path.join(filepath, preffix), readfile), "w", encoding='utf-8')
                f.write(buffer)
                out = os.path.join(os.path.join(filepath, preffix), readfile) + f" -> {buffer}"
            finally:
                if f:
                    f.close
                output.append(out)
            # 备份
            shutil.move(path, backup)
        # .py文件
        elif suffix == suffix_py:
            print(f"ignore file -> {f}")
        # 其它文件
        else:
            os.remove(path)
            print(f"delete file -> {f}")
    else:
        print(f"{f} is err")

# 打印结果
for item in output:
    print(item)

