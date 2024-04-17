"""
-*- coding: utf-8 -*-
@Time : 2023/7/27 13:51
"""
import asyncio
import time

#
# class demo:
#     def __init__(self):
#         self.num = 10
#
#     async def main(self):
#         for i in range(self.num):
#             print(i)
#             await asyncio.sleep(2)
#
#     async def run(self):
#         await asyncio.gather(self.main(), self.main())
#
# if __name__ == '__main__':
#     demo().run()
import pandas as pd
import sys
# data = {"name": ['tom', 'jack'], "age": [12]}
data = [{"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}]
df = pd.DataFrame(data)
# print(df)
df = df.fillna("None")
for i in df.index:
    print(df.loc[i].to_dict()["c"])
    if df.loc[i].to_dict()["c"] == "None":

        print(i)
    else:
        print(1111111)
    # sys.exit()


# print(df.isnull)



# for i in df.to_dict('records'):
#     for j in i.keys():
#         if pd.isna(i[j]):
#             print(1111)
#             print(j)





    # if df.iloc[i].isnull:
    #     print(i)
    #
    # else:
    #     print(111)



# print(df.df)
# for i in df.index:
#     das = df.loc[i].to_dict()
# print(das)
#     print(i)
#     print(df.iloc[i])
#     print("-"*10)
#     print(df.columns)
#     print("*"*100)
# # print(df)