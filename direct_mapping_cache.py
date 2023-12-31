# -*- coding: utf-8 -*-
"""direct_mapping_cache.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EdsVRuVf_9ElyUgXiFj6I-V3nn9TUpBX
"""



import math

class CacheSimulator:
    def __init__(self, cache_size, memory_size, write_policy, write_allocation, offset_bits):
        self.cache_size = cache_size  # Total cache size in bytes
        self.memory_size = memory_size  # Total memory size in bytes
        self.offset_bits = offset_bits  # Number of offset bits
        self.cache_block_size = 2 ** offset_bits  # Size of a cache block in bytes
        self.num_blocks = cache_size // self.cache_block_size  # Number of cache blocks
        self.cache = [[None, False, False] for _ in range(self.num_blocks)]  # Cache structure [tag, valid, dirty]
        self.hits = 0  # Number of cache hits
        self.misses = 0  # Number of cache misses
        self.write_policy = write_policy  # Write policy: "write-through" or "write-back"
        self.write_allocation = write_allocation  # Write allocation policy: "write-on-allocate" or "write-around"

    def access_memory(self, address, write=False):
        tag, index = self.extract_address_components(address)

        block = self.cache[index]

        if block[0] == tag and block[1]:
            # Cache hit
            self.hits += 1
            if write:
                if self.write_policy == "write-back":
                    if self.write_allocation == "write-on-allocate":
                        block[2] = True  # Set dirty bit
                    elif self.write_allocation == "write-around":
                        # Update data only in memory (write-around policy)
                        # (In this example, we are not simulating actual data storage)
                        pass
                elif self.write_policy == "write-through":
                    # Update data in both cache and memory
                    # (In this example, we are not simulating actual data storage)
                    self.update_cache_block(index, tag)
            status = "Hit"
        else:
            # Cache miss
            self.misses += 1
            if write:
                if self.write_policy == "write-back":
                    if self.write_allocation == "write-on-allocate":
                        if block[1] and block[2]:
                            # Evict block if it is valid and dirty
                            # (In this example, we are not simulating actual data storage)
                            pass
                        self.update_cache_block(index, tag)
                        block = self.cache[index]
                        block[2] = True  # Set dirty bit
                    elif self.write_allocation == "write-around":
                        # Update data only in memory (write-around policy)
                        # (In this example, we are not simulating actual data storage)
                        pass
                elif self.write_policy == "write-through":
                    # Update data in both cache and memory
                    # (In this example, we are not simulating actual data storage)
                    self.update_cache_block(index, tag)
            else:
                self.update_cache_block(index, tag)
            status = "Miss"

        return status

    def update_cache_block(self, index, tag):
        self.cache[index][0] = tag
        self.cache[index][1] = True
        self.cache[index][2] = False  # Clear dirty bit

    def extract_address_components(self, address):
        index_bits = self.log2(self.num_blocks)
        tag_bits = 32 - index_bits - self.offset_bits

        index = (address >> self.offset_bits) & (2 ** index_bits - 1)
        tag = (address >> (self.offset_bits + index_bits)) & (2 ** tag_bits - 1)

        return tag, index

    def get_hit_rate(self):
        total_accesses = self.hits + self.misses
        hit_rate = (self.hits / total_accesses) * 100
        return hit_rate

    def get_miss_rate(self):
        total_accesses = self.hits + self.misses
        miss_rate = (self.misses / total_accesses) * 100
        return miss_rate

    @staticmethod
    def log2(x):
        return int(math.log2(x))


# User-defined input
cache_size = int(input("Enter cache size in bytes: "))
memory_size = int(input("Enter memory size in bytes (greater than cache size): "))
while memory_size <= cache_size:
    print("Memory size should be greater than cache size.")
    memory_size = int(input("Enter memory size in bytes (greater than cache size): "))

write_policy = input("Enter write policy (write-through / write-back): ")
while write_policy != "write-through" and write_policy != "write-back":
    print("Invalid write policy. Please choose 'write-through' or 'write-back'.")
    write_policy = input("Enter write policy (write-through / write-back): ")

write_allocation = input("Enter write allocation policy (write-on-allocate / write-around): ")
while write_allocation != "write-on-allocate" and write_allocation != "write-around":
    print("Invalid write allocation policy. Please choose 'write-on-allocate' or 'write-around'.")
    write_allocation = input("Enter write allocation policy (write-on-allocate / write-around): ")

offset_bits = int(input("Enter the number of offset bits: "))

cache = CacheSimulator(cache_size, memory_size, write_policy, write_allocation, offset_bits)

# Access memory addresses
addresses = []
num_addresses = int(input("Enter the number of memory addresses: "))
for i in range(num_addresses):
    address = int(input(f"Enter memory address {i+1}: "))
    addresses.append(address)

results = []

for address in addresses:
    result = cache.access_memory(address)
    results.append(result)

# Print results
print("******** DIRECT MAPPED CACHE SIMULATOR ********")
print("Cache size:", cache.cache_size)
print("Memory size:", cache.memory_size)
print("Write policy:", cache.write_policy)
print("Write allocation policy:", cache.write_allocation)
print("Offset bits:", cache.offset_bits)
print("Cache hits:", cache.hits)
print("Cache misses:", cache.misses)
print("Hit rate: {:.2f}%".format(cache.get_hit_rate()))
print("Miss rate: {:.2f}%".format(cache.get_miss_rate()))
print("**********************************")
print("Memory Address\tStatus")
for i in range(num_addresses):
    print("{}\t\t{}".format(addresses[i], results[i]))
print("**********************************")

