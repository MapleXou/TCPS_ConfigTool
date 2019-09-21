import unittest
from foo.command_queue import command_queue


class CommandQueueTest(unittest.TestCase):
    def test_push_and_pop(self):
        command_queue.push('command_test')
        self.assertEqual(command_queue.pop(), 'command_test')

    def test_is_empty(self):
        self.assertEqual(command_queue.is_empty(), True)
        command_queue.push('command_test')
        self.assertEqual(command_queue.is_empty(), False)
        self.assertEqual(command_queue.pop(), 'command_test')
        self.assertEqual(command_queue.is_empty(), True)


if __name__ == '__main__':
    unittest.main()
