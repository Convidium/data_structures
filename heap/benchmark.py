import time

def benchmark_heapsort(Heap_class, original_data, iterations=10):
    execution_times = []
    
    for _ in range(iterations):
        test_data = original_data[:]
        time_start = time.perf_counter()
        
        heap_instance = Heap_class(original_data)
        heap_instance.sort_heap()
        
        time_end = time.perf_counter()
        
        execution_times.append(time_end - time_start)
    avg_time = sum(execution_times) / len(execution_times)
        
    return avg_time
