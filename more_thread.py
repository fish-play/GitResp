"""
-*- coding: utf-8 -*-
@Time : 2023/2/16 11:06
"""
from concurrent.futures import ThreadPoolExecutor
import time

tasklist = ["任务1", "任务2", "任务3", "任务4"]


def task(task_name: str):
    time.sleep(5)
    print(task_name + "已完成\n")
    return task_name + "的执行结果"


executor = ThreadPoolExecutor(max_workers=3)
future_a = executor.submit(task, tasklist[0])
future_b = executor.submit(task, tasklist[1])
future_c = executor.submit(task, tasklist[2])
future_d = executor.submit(task, tasklist[3])
print(future_a.result(), future_b.result())
