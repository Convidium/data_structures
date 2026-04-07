from abc import ABC, abstractmethod

class BaseHeap(ABC):
    def __init__(self, array, arity=2):
        self.heap = []
        self.arity = arity
        if isinstance(array, list) and len(array) > 0: 
            self.build_heap(array)
    
    def parent(self, index):
        if len(self.heap) > 0:
            return (index-1)//self.arity
        else: return 0
        
    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap)-1)
        
    def extract(self):
        if not self.heap:
            return None
        
        maximum = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heapify_down(0)
        return maximum
            
    def heapify_up(self, index):
        while index != 0 and self._compare(self.heap[self.heap[index], self.parent(index)]):
            self.heap[index], self.heap[self.parent(index)] = self.heap[self.parent(index)], self.heap[index]        
            index = self.parent(index)
    
    def heapify_down(self, index, heap_size=None):
        if heap_size is None:
            heap_size = len(self.heap)
        while True:
            extreme_idx = index
            for k in range(1, self.arity+1):
                child_idx = self.arity*index+k
                if child_idx < heap_size and self._compare(self.heap[child_idx], self.heap[extreme_idx]):
                    extreme_idx = child_idx
            if extreme_idx != index:
                self.heap[index], self.heap[extreme_idx] = self.heap[extreme_idx], self.heap[index]
                index = extreme_idx
            else:
                break
    
    def build_heap(self, array):
        self.heap = array[:]
        lowest_node_i = len(self.heap)//self.arity-2
        for i in range(lowest_node_i, -1, -1):
            self.heapify_down(i)
            
    def sort_heap(self):
        if not self.heap:
            return None
        
        arr_length = len(self.heap)
        for i in range(arr_length-1, 0, -1):
            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]
            self.heapify_down(0, heap_size=i)
        
    def __repr__(self):
        return f"Heap: {self.heap}"
    
    @abstractmethod
    def _compare(self, first_val, second_val):
        pass
    
class MaxHeap(BaseHeap):
    def _compare(self, first_val, second_val):
        return first_val > second_val

class MinHeap(BaseHeap):
    def _compare(self, first_val, second_val):
        return first_val < second_val