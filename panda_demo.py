import os
import pandas as pd

def read_excel(file):
    lists = []
    df = pd.read_excel(file)
    g = df.drop_duplicates(subset="案号全")
    for name in g.index:
        data = df.loc[name].to_dict()
        lists.append(data)
    return lists

def paper_click():
    print(11111)
    return True

def run():
    file = r"C:\Users\9000\Desktop\新建文件夹 (4)\pandas测试.xlsx"
    demo_read = read_excel(file)
    listes = []

    for i in demo_read:
        print(i)
        types = paper_click()
        if types is True:
            listes.append('ok')
        else:
            listes.append('no')
        
    df = pd.read_excel(file)
    num_cle = int(str(df.shape).split(',')[1].replace(")", ''))
    data = {'状态': listes}
    data = pd.DataFrame(data)
    save_data = pd.concat([df, data], axis=num_cle)
    save_data.to_excel(file, index=False)


if __name__ == '__main__':
    run()