class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return int(key) % self.size
        #return int(key) % len(self.table)
    
    def insert(self, key, value):
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]
        #self.table[bucket].append((key, value))
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
            
        bucket.append([key, value])
        
    def lookup(self, key):
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]
        
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None
    
    def remove(self, key):
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]
        for pair in bucket:
            if pair[0] == key:
                bucket.remove(pair)
                return True
        return False