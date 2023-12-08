import os
import multiprocessing

def get_cpu_info():
    cpu_count = os.cpu_count()
    logical_cores = multiprocessing.cpu_count()
    return cpu_count, logical_cores

# if __name__ == "__main__":
#    cpu_count, logical_cores = get_cpu_info()
#    print(f"Number of physical cores: {cpu_count}")
#    print(f"Number of logical cores (threads): {logical_cores}")