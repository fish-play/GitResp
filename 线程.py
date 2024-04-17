"""
-*- coding: utf-8 -*-
@Time : 2023/7/25 16:13
"""
import threading, time
from threading import Event


class demo:
    def __init__(self, num: int):
        super().__init__()
        self.num = num
        self.running = True

    def myseed(self):
        while self.running:
            print("检查")
            time.sleep(3)

    def stop(self):
        self.running = False

    def run(self):
        for i in range(self.num):
            print(i)
            time.sleep(2)

    def main(self):
        self.thread = threading.Thread(target=self.myseed)
        self.thread.start()
        self.run()
        time.sleep(2)
        self.stop()
        self.thread.join()


if __name__ == '__main__':
    demo(20).main()
