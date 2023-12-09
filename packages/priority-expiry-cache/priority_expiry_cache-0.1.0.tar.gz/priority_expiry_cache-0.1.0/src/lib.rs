use pyo3::prelude::*;
extern crate lru;

use std::collections::{BTreeMap, BTreeSet,HashMap};
use lru::LruCache;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyclass]
struct Page{
    key: String,
    value: String,
    priority: u32,
    expiry: u32,
}

#[pyclass]
#[derive(Ord,PartialOrd,Eq, PartialEq)]
struct ItemExpiry{
    expiry: u32,
    key: String,
}
#[pyclass]
pub struct PECache{
    access_map: HashMap<String, Page>,
    evict_expiry: BTreeSet<ItemExpiry>,
    evict_priority: BTreeMap<u32, LruCache<String, bool>>,
}

#[pymethods]
impl PECache{
    #[new]
    pub fn new() -> Self {
        Self {
            access_map: Default::default(),
            evict_expiry: Default::default(),
            evict_priority: Default::default(),
        }
    }
    pub fn set(&mut self, key: String, value: String,priority: u32, expiry: u32) {
        // addition to the btree for time
        let key_expiry = ItemExpiry {
            expiry: expiry.clone(),
            key: key.clone(),
        };
        self.evict_expiry.insert(key_expiry);
        // addition to the btree for priority
        self.evict_priority.entry(priority.clone())
            .or_insert(LruCache::unbounded()).push(key.clone(), true);
        // add to the map
        let page = Page { key: key.clone(), value, expiry, priority };
        self.access_map.insert(key, page);
        return;
    }
    pub fn get(&mut self, key: String) -> Option<String> {
        if let Some(page) = self.access_map.get(&key) {
            // change the order in the last recently data structure
            self.evict_priority.get_mut(&page.priority).unwrap().promote(&page.key);
            return Some(page.value.clone());
        }
        None
    }
    pub fn evict(&mut self, barrier: u32) {
        if self.access_map.len() == 0 {
            return;
        }
        // get key by check firs by time and then by priority/lru
        let target_item = self.evict_expiry.first().unwrap();

        let key_target = if target_item.expiry <= barrier { target_item.key.clone() } else {
            let target_item = self.evict_priority.first_entry().unwrap();
            let (key,_) = target_item.get().peek_lru().unwrap();
            key.clone()
        };
        // delete from the map
        let page = self.access_map.remove(&key_target).unwrap();
        // delete from the expiry tree
        self.evict_expiry.remove(&ItemExpiry{expiry: page.expiry.clone(),key: page.key.clone()});
        // delete from priority tree
        let node_priority = self.evict_priority.get_mut(&page.priority).unwrap();
        node_priority.pop(&page.key);
        // delete the node if empty after the item removal
        if node_priority.len() == 0 {
            self.evict_priority.remove(&page.priority);
        }
        return
    }
    pub fn len(&self)->usize{
        self.access_map.len()
    }
}



/// A Python module implemented in Rust.
#[pymodule]
fn priority_expiry_cache(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PECache>()?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
