type cache store
################

Store
=====

.. code-block:: go
   :lineno-start: 34
   :caption: k8s.io/client-go/tools/cache/store.go

    type Store interface {
      Add(obj interface{}) error
      Update(obj interface{}) error
      Delete(obj interface{}) error
      List() []interface{}
      ListKeys() []string
      Get(obj interface{}) (item interface{}, exists bool, err error)
      GetByKey(key string) (item interface{}, exists bool, err error)

      // Replace will delete the contents of the store, using instead the
      // given list. Store takes ownership of the list, you should not reference
      // it after calling this function.
      Replace([]interface{}, string) error
      Resync() error
    }

.. code-block:: go
   :lineno-start: 112
   :caption: k8s.io/client-go/tools/cache/store.go

    // cache responsibilities are limited to:
    //  1. Computing keys for objects via keyFunc
    //  2. Invoking methods of a ThreadSafeStorage interface
    type cache struct {
      // cacheStorage bears the burden of thread safety for the cache
      cacheStorage ThreadSafeStore
      // keyFunc is used to make the key for objects stored in and retrieved from items, and
      // should be deterministic.
      keyFunc KeyFunc
    }

thread_safe_store
=================

.. code-block:: go
   :lineno-start: 37
   :caption: k8s.io/client-go/tools/cache/thread_safe_store.go

    type ThreadSafeStore interface {
      Add(key string, obj interface{})
      Update(key string, obj interface{})
      Delete(key string)
      Get(key string) (item interface{}, exists bool)
      List() []interface{}
      ListKeys() []string
      Replace(map[string]interface{}, string)
      Index(indexName string, obj interface{}) ([]interface{}, error)
      IndexKeys(indexName, indexKey string) ([]string, error)
      ListIndexFuncValues(name string) []string
      ByIndex(indexName, indexKey string) ([]interface{}, error)
      GetIndexers() Indexers

      // AddIndexers adds more indexers to this store.  If you call this after you already have data
      // in the store, the results are undefined.
      AddIndexers(newIndexers Indexers) error
      Resync() error
    }

.. code-block:: go
   :lineno-start: 58
   :caption: k8s.io/client-go/tools/cache/thread_safe_store.go

    type threadSafeMap struct {
      lock  sync.RWMutex
      items map[string]interface{}

      // indexers maps a name to an IndexFunc
      indexers Indexers
      // indices maps a name to an Index
      indices Indices
    }


.. code-block:: go
   :lineno-start: 175
   :caption: k8s.io/client-go/tools/cache/thread_safe_store.go

    func (c *threadSafeMap) ByIndex(indexName, indexKey string) ([]interface{}, error) {
      c.lock.RLock()
      defer c.lock.RUnlock()

      indexFunc := c.indexers[indexName]

      index := c.indices[indexName]

      set := index[indexKey]

      list := make([]interface{}, 0, set.Len())
      for _, key := range set.List() {
        list = append(list, c.items[key])
      }

      return list, nil
    }












