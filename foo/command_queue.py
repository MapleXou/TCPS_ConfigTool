from collections import deque


class CommandQueue:
    def __init__(self):
        self._queue = deque()

    def push(self, command):
        self._queue.append(command)

    def pop(self):
        if self.is_empty():
            return ''
        return self._queue.popleft()

    def is_empty(self):
        if len(self._queue) == 0:
            return True
        else:
            return False


command_queue = CommandQueue()
