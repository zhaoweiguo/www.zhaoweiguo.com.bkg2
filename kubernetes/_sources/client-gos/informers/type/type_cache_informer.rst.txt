cache
#####


cache.SharedIndexInformer
=========================

.. code-block:: go
   :lineno-start: 66
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    type SharedIndexInformer interface {
      SharedInformer
      // AddIndexers add indexers to the informer before it starts.
      AddIndexers(indexers Indexers) error
      GetIndexer() Indexer
    }

.. code-block:: go
   :lineno-start: 43
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    type SharedInformer interface {
      AddEventHandler(handler ResourceEventHandler)
      AddEventHandlerWithResyncPeriod(handler ResourceEventHandler, resyncPeriod time.Duration)
      GetStore() Store
      GetController() Controller
      Run(stopCh <-chan struct{})
      HasSynced() bool
      LastSyncResourceVersion() string
    }

.. code-block:: go
   :lineno-start: 127
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    type sharedIndexInformer struct {
      indexer    Indexer
      controller Controller

      processor             *sharedProcessor
      cacheMutationDetector CacheMutationDetector

      listerWatcher ListerWatcher
      objectType    runtime.Object

      resyncCheckPeriod time.Duration
      defaultEventHandlerResyncPeriod time.Duration
      clock clock.Clock

      started, stopped bool
      startedLock      sync.Mutex

      blockDeltas sync.Mutex
    }

.. code-block:: go
   :lineno-start: 273
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    func (s *sharedIndexInformer) AddEventHandler(handler ResourceEventHandler) {
      s.AddEventHandlerWithResyncPeriod(handler, s.defaultEventHandlerResyncPeriod)
    }


.. code-block:: go
   :lineno-start: 294
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    func (s *sharedIndexInformer) AddEventHandlerWithResyncPeriod(handler ResourceEventHandler, resyncPeriod time.Duration) {
      s.startedLock.Lock()
      defer s.startedLock.Unlock()
      ... ...
      listener := newProcessListener(handler, resyncPeriod, 
              determineResyncPeriod(resyncPeriod, s.resyncCheckPeriod), 
              s.clock.Now(), initialBufferSize)

      // in order to safely join, we have to
      // 1. stop sending add/update/delete notifications
      // 2. do a list against the store
      // 3. send synthetic "Add" events to the new handler
      // 4. unblock
      s.blockDeltas.Lock()
      defer s.blockDeltas.Unlock()

      s.processor.addListener(listener)
      for _, item := range s.indexer.List() {
        listener.add(addNotification{newObj: item})
      }
    }


ResourceEventHandler
====================

.. code-block:: go
   :lineno-start: 177
   :caption: k8s.io/client-go/tools/cache/controller.go

    type ResourceEventHandler interface {
      OnAdd(obj interface{})
      OnUpdate(oldObj, newObj interface{})
      OnDelete(obj interface{})
    }

.. code-block:: go
   :lineno-start: 186
   :caption: k8s.io/client-go/tools/cache/controller.go

    type ResourceEventHandlerFuncs struct {
      AddFunc    func(obj interface{})
      UpdateFunc func(oldObj, newObj interface{})
      DeleteFunc func(obj interface{})
    }


















