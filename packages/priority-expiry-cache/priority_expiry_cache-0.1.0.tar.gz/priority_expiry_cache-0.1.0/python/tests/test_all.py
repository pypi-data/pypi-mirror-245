from priority_expiry_cache import PECache

def test_new_cache():
    PECache()

def test_get_missing_key():
    assert None == PECache().get("")

def test_evict_from_empty_cache():
    PECache().evict(0)

def test_get_and_set_single_element():
    cache = PECache()
    key,value,priority,expiry = "key","value",1,1
    cache.set(key,value,priority,expiry)
    assert cache.get(key) == value

def test_set_2_items_same_key_override():
    cache = PECache()
    key,value,priority,expiry = "key","value",1,1
    cache.set(key, value, priority, expiry)
    value1,priority1,expiry = "value1",2,2
    cache.set(key, value1, priority1, expiry)
    assert cache.get(key) == value1
    assert cache.len() == 1

def test_get_and_set_evict_single_element():
    cache = PECache()
    key,value,priority,expiry = "key","value",1,1
    cache.set(key,value,priority,expiry)
    cache.evict(2)
    assert cache.get(key) is None

def test_insert_2_elements_evict_get_different_time():
    cache = PECache()
    key, value, priority, expiry = "key", "value", 1, 0
    cache.set(key, value, priority, expiry)
    key1, value1, priority1, expiry1 = ("key1", "value1", 2, 2)
    cache.set(key1, value1, priority1, expiry1)

    assert cache.get(key) == value
    assert cache.get(key1) == value1
    cache.evict(1)
    assert cache.get(key1) == value1
    assert cache.get(key) is None
    cache.evict(3)
    assert cache.get(key1) is None
    assert cache.get(key) is None
    cache.evict(0)

def test_insert_2_elements_evict_by_priority():
    cache = PECache()
    key, value, priority, expiry = "z_key", "z_value", 2, 10
    cache.set(key, value, priority, expiry)
    key1, value1, priority1, expiry1 = "key1", "value1", 1, 10
    cache.set(key1, value1, priority1, expiry1)
    assert cache.get(key) == value
    assert cache.get(key1) == value1
    cache.evict(2)
    assert cache.get(key1) is None
    assert cache.get(key)  == value
    cache.evict(0)
    assert cache.get(key1) is None
    assert cache.get(key) is None
    cache.evict(0)

def test_eviction_by_lru():
    cache = PECache()
    key, value, priority, expiry = "z_key", "z_value", 2, 10
    cache.set(key, value, priority, expiry)

    key1, value1, priority1, expiry1 = "key1", "value1", 2, 11
    cache.set(key1, value1, priority1, expiry1)

    key2, value2, priority2, expiry2 = "key2", "value2", 2, 12
    cache.set(key2, value2, priority2, expiry2)
    cache.get(key)
    cache.evict(5)
    assert cache.get(key)  == value
    assert cache.get(key1) is None
    assert cache.get(key2)  == value2
