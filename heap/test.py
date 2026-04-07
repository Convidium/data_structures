from heap_class import MaxHeap, MinHeap
from benchmark import benchmark_heapsort
import random


list_amplitude = random.randint(1, 300)
list_size = 20000

random_list = [list_amplitude for _ in range(list_size)]
print(benchmark_heapsort(MaxHeap, random_list))
print(benchmark_heapsort(MaxHeap, random_list))