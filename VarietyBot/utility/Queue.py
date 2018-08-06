'''
Queue.py
Contains a Queue implementation
'''
from utility.DoublyLinkedList import DoublyLinkedList

class Queue:

    def __init__(self):
        '''
        initilize a empty queue as a 
        doubly linked list
        '''
        self._queue = DoublyLinkedList()

    def __len__(self) -> int:
        '''
        overloaded len()
        '''
        return len(self._queue)

    def __iter__(self):
        '''
        overloaded iterator method
        so this queue can be iterated
        using a for loop
        '''
        for value in self._queue:
            yield value

    def dequeue(self) -> 'value':
        '''
        remove and return the front
        value
        '''
        return self._queue.pop() if not self.is_empty() else None

    def enqueue(self, val):
        '''
        Add a value to the end
        of the queue
        '''
        self._queue.append(val)   

    def is_empty(self) -> bool:
        '''
        Return True if empty queue
        '''
        return len(self._queue) == 0

    def clear(self):
        ''' 
        clears this queue 
        '''
        self._queue = DoublyLinkedList()
