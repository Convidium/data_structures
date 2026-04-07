class MaxHeap:
    def __init__(self, value):
        self.heap = []
        if isinstance(value, list) and len(value) > 0: 
            self.build_heap(value)
    
    def parent(self, index):
        if index == 0: return self.heap[index]
        if len(self.heap) > 0:
            return (index-1)//2
        
    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap)-1)
            
    def heapify_up(self, index):
        while index != 0 and self.heap[self.parent(index)] < self.heap[index]:
            self.heap[index], self.heap[self.parent(index)] = self.heap[self.parent(index)], self.heap[index]        
            index = self.parent(index)
            
    def extract_max(self):
        if not self.heap:
            return None
        
        maximum = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heapify_down(0)
        return maximum
    
    def heapify_down(self, index, heap_size=None):
        if heap_size is None:
            heap_size = len(self.heap)
        largest = index
        
        while True:
            left = 2*index+1
            right = 2*index+2
            
            if left < heap_size and self.heap[left] > self.heap[largest]:
                largest = left
            if right < heap_size and self.heap[right] > self.heap[largest]:
                largest = right
            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
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