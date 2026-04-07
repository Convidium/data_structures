from heap_class import MaxHeap, MinHeap

init_list = [1, 7, 3, 5, 6, 22, 11, 34, 5, 2, 7, 10]

my_list = MaxHeap(init_list[:], 3)
print(my_list)
my_list.sort_heap()
print(my_list)