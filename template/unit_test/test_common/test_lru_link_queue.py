# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/5/28 12:28

# desc:

import logging
import unittest

import common.lru_link_queue as lru_link_queue


class TestLRULinkQueue(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("LRU link setUp:")

    def test_PushPop(self):
        LRULinkQueueObj = lru_link_queue.LRULinkQueue()
        LRULinkQueueObj.Push(1)
        LRULinkQueueObj.Push(2)
        self.assertListEqual(LRULinkQueueObj.GetMd5QueueList(), [1, 2])
        LRULinkQueueObj.Push(3)
        self.assertListEqual(LRULinkQueueObj.GetMd5QueueList(), [1, 2, 3])
        LRULinkQueueObj.Push(2)
        self.assertListEqual(LRULinkQueueObj.GetMd5QueueList(), [1, 3, 2])
        LRULinkQueueObj.Pop(3)
        self.assertListEqual(LRULinkQueueObj.GetMd5QueueList(), [1, 2])
        LRULinkQueueObj.Pop(1)
        self.assertListEqual(LRULinkQueueObj.GetMd5QueueList(), [2])
        LRULinkQueueObj.Pop(2)
        self.assertListEqual(LRULinkQueueObj.GetMd5QueueList(), [])

    def tearDown(self):
        logging.getLogger("myLog").debug("TestLRULinkQueue tearDown\n\n\n")
