#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : uniform_queue
# @Time         : 2023/12/6 17:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from queue import Queue, Empty


class UniformQueue(object):

    def __init__(self, generator: Generator):
        self.queue = Queue()
        self.producer(generator)

    def consumer(self, interval: float = 0.02, timeout: float = 30):
        """

        :param interval:
        :param timeout:
        :param break_fn: lambda line: line.choices[0].finish_reason == 'stop'
        :return:
        """
        while True:
            try:
                item = self.queue.get(timeout=timeout)
                if item is None:  # 跳出队列，很重要：break_fn: Callable = lambda item: item is None
                    break
                yield item
            except Empty:
                break
            time.sleep(interval)

    @background
    def producer(self, generator):
        for i in generator:
            self.queue.put(i)


if __name__ == '__main__':

    def gen():
        while 1:
            yield '#'


    for i in tqdm(UniformQueue(gen()).consumer(interval=0.1)):
        print(i)
