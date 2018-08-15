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
	value = None
	prev = None
	next = None

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
		while node != None:
			yield node.value
			node = node.next

	def _create_node(self, value, prev, next):
		node = Node()
		node.value = value
		node.prev = prev
		node.next = next

		return node

	def append(self, value):
		'''
		Adds a node containing the given
		value to the end of this list

		Basically an "addToEnd" method
		'''
		new_node = self._create_node(value, None, None)

		if self._head == None:
			self._head = new_node
			self._tail = new_node

		else:
			self._tail.next = new_node
			new_node.prev = self._tail
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
			val = self._head.value
			self._head = self._tail = None

		elif self._size > 1:
			val = self._head.value
			next_node = self._head.next
			self._head = next_node
			if self._head != None: 
				self._head.prev = None

		self._size -= 1

		return val
			

