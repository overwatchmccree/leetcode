# coding: utf-8

class LFUCache(object):
       
    def __init__(self, capacity):
        self.capacity = capacity
        self.bykey = {}
        self.freq_head = New_freq_node()
               
    def set(self, key, value):      
        if self.capacity == 0:
            return
        
        if key not in self.bykey:
            if len(self.bykey) >= self.capacity:
                self.delete_LFU_item()
            
            freq = self.freq_head.next
            if freq.value != 1:
                freq = self.get_new_node(1, self.freq_head, freq)
            freq.items.append(key)
            self.bykey[key] = New_LFU_item(value, freq)     
        else:
            tmp = self.bykey[key]
            freq = tmp.parent
            next_freq = freq.next

            if next_freq is self.freq_head or next_freq.value != freq.value + 1:
                next_freq = self.get_new_node(freq.value + 1, freq, next_freq)
            next_freq.items.append(key)
            tmp.parent = next_freq
            
            tmp.data = value

            freq.items.remove(key)
            if len(freq.items) == 0:
                self.delete_node(freq)
           
    def get(self, key):    
        if key not in self.bykey:
            return -1
        tmp = self.bykey[key]
        freq = tmp.parent
        next_freq = freq.next
        
        if next_freq is self.freq_head or next_freq.value != freq.value + 1:
            next_freq = self.get_new_node(freq.value + 1, freq, next_freq)
        next_freq.items.append(key)
        tmp.parent = next_freq
        
        freq.items.remove(key)
        if len(freq.items) == 0:
            self.delete_node(freq)
        return tmp.data

    def get_new_node(self, value, prev, next):
        nn = New_freq_node()
        nn.value = value
        nn.prev = prev
        nn.next = next
        prev.next = nn
        next.prev = nn
        return nn
    
    def delete_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        
    def delete_LFU_item(self):
        if len(self.bykey) == 0:
            return
        else:
            del_key = self.freq_head.next.items[0]
            self.freq_head.next.items = self.freq_head.next.items[1:]
            del self.bykey[del_key]
            if len(self.freq_head.next.items) == 0:
                self.delete_node(self.freq_head.next)
        
        
class New_freq_node(object):
    def __init__(self):
        self.value = 0
        self.items = []
        self.prev = self
        self.next = self

class New_LFU_item(object):
    def __init__(self, data, parent):
        
        self.data = data
        self.parent = parent

