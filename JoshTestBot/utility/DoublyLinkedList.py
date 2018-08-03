'''
DoublyLinkedList.py

Contains a DoublyLinkedList implementation to be used
in the Queue implementation
'''

class Node:
	'''
	A list node, representing each
	node in a doubly linked list data 
	structure
	'''
	def __init__(self, value, prev, next):
		self._value = value
		self._prev = prev
		self._next = next

	#### GETTERS ####

	def get_value(self):
		return self._value

	def get_prev(self):
		return self._prev

	def get_next(self):
		return self._next

	#### SETTERS ####

	def set_value(self, v):
		self._value = v

	def set_prev(self, p):
		self._prev = p

	def set_next(self, n):
		self._next = n

class DoublyLinkedList:
	'''
	The doubly linked list implementation
	containing some basic methods for 
	queues
	'''
	def __init__(self):
		self._head = None
		self._tail = None
		self._size = 0

	def __len__(self):
		''' 
		Overloaded the len()
		operator
		'''
		return self._size

	def __iter__(self):
		'''
		Overloaded the iterator
		operator. Allows this
		doubly linked list to 
		be iterated through with a 
		for loop
		'''
		node = self._head
		while node:
			yield node.get_value()
			node = node.get_next()

	def append(self, value):
		'''
		Adds a node containing the given
		value to the end of this list

		Basically an "addToEnd" method
		'''
		new_node = Node(value, None, None)

		if self._head == None:
			self._head = new_node
			self._tail = new_node

		else:
			self._tail.set_next(new_node)
			new_node.set_prev(self._tail)
			self._tail = new_node

		self._size += 1

	def pop(self) -> 'value':
		'''
		Removes the first node from
		this list, returning the value
		that the node contains

		Basically, a "removeFromStart"
		method
		'''
		val = None

		if self._size == 1:
			val = self._head.get_value()
			self._head = self._tail = None

		elif self._size > 1:
			val = self._head.get_value()
			next_node = self._head.get_next()
			self._head = next_node
			if self._head != None: 
				self._head.set_prev(None)

		self._size -= 1

		return val
			

