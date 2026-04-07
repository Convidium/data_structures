from abc import ABC, abstractmethod

class BaseHeap(ABC):
    def __init__(self, value):
        self.heap = []
        if isinstance(value, list) and len(value) > 0: 
            self.build_heap(value)
    
    def parent(self, index):
        if index == 0: return 0
        if len(self.heap) > 0:
            return (index-1)//2
        
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
        while index != 0 and self._compare(self.heap[self.parent(index)], self.heap[index]):
            self.heap[index], self.heap[self.parent(index)] = self.heap[self.parent(index)], self.heap[index]        
            index = self.parent(index)
    
    def heapify_down(self, index, heap_size=None):
        if heap_size is None:
            heap_size = len(self.heap)
        extreme_idx = index
        
        while True:
            left = 2*index+1
            right = 2*index+2
            
            if left < heap_size and self._compare(self.heap[extreme_idx], self.heap[left]):
                extreme_idx = left
            if right < heap_size and self._compare(self.heap[extreme_idx], self.heap[right]):
                extreme_idx = right
            if extreme_idx != index:
                self.heap[index], self.heap[extreme_idx] = self.heap[extreme_idx], self.heap[index]
                index = extreme_idx
            else:
                break
    
    def build_heap(self, array):
        self.heap = array[:]
        lowest_node_i = len(self.heap)//2-1
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
    def _compare(self, parent_val, child_val):
        pass
    
class MaxHeap(BaseHeap):
    def _compare(self, parent_val, child_val):
        return parent_val < child_val

class MinHeap(BaseHeap):
    def _compare(self, parent_val, child_val):
        return parent_val > child_val