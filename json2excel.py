import pandas as pd
import json
import os

# 从 https://github.com/Kengxxiao/ArknightsGameData 中Clone或直接下载解包数据到根目录下
main_path = "ArknightsGameData-master/zh_CN/gamedata/excel/"
excel_folder = "configs/"

def create_folder_dir(_dir):
    """如果没文件夹就不能直接df.to_excel(path)，需要手动创建一下"""
    if not os.path.exists(_dir):
        os.makedirs(_dir)

def rebuild_tables():
    """从JSON数据反向重建Excel表，增强可读性"""
    create_folder_dir(excel_folder)
    for root, _, files in os.walk(main_path):
        for f in files:
            build_table(root,f,excel_folder)

def build_table(path,filename,output_folder=excel_folder):
    """写一张表"""

    # 暂时先只看这几个表
    if filename in ["item_table.json", "mission_table.json","activity_table.json"]:
        # 写入文件的对象
        writer = pd.ExcelWriter(output_folder+filename.replace(".json",".xlsx"))
        
        # 读取的JSON对象
        json_path = path+ filename
        this_json = json.load(open(json_path,encoding="utf-8"))
        
        for key in this_json.keys():
            if key in ["uniqueInfo"]:
                _df = pd.DataFrame(this_json[key].items(),columns=["uniqueID","count"])
            elif isinstance(this_json[key],dict):
                _df = pd.DataFrame(this_json[key].values())
            elif isinstance(this_json[key],list):
                _df = pd.DataFrame(this_json[key])
            _df.to_excel(writer,sheet_name=key,index=False)
        # 走你
        writer.save()
            

if __name__ == '__main__':
    rebuild_tables()
