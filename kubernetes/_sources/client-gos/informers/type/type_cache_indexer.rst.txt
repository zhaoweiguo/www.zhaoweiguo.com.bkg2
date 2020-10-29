Indexer
#######


Indexer
=======

.. code-block:: go
   :lineno-start: 83
   :caption: k8s.io/client-go/tools/cache/index.go

    type Indexers map[string]IndexFunc

    type Indices map[string]Index

    type Index map[string]sets.String
    
    type IndexFunc func(obj interface{}) ([]string, error)

.. code-block:: go
   :lineno-start: 27
   :caption: k8s.io/client-go/tools/cache/index.go

    type Indexer interface {
      Store

      Index(indexName string, obj interface{}) ([]interface{}, error)
      IndexKeys(indexName, indexKey string) ([]string, error)
      ListIndexFuncValues(indexName string) []string

      ByIndex(indexName, indexKey string) ([]interface{}, error)
      GetIndexers() Indexers

      AddIndexers(newIndexers Indexers) error
    }

.. code-block:: go
   :lineno-start: 112
   :caption: k8s.io/client-go/tools/cache/store.go

    type cache struct {
      // cacheStorage bears the burden of thread safety for the cache
      cacheStorage ThreadSafeStore
      // keyFunc is used to make the key for objects stored in and retrieved from items, and
      // should be deterministic.
      keyFunc KeyFunc
    }







