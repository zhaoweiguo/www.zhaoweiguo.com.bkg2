informer启动
############


.. code-block:: go
   :lineno-start: 189
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    func (s *sharedIndexInformer) Run(stopCh <-chan struct{}) {
      defer utilruntime.HandleCrash()

      fifo := NewDeltaFIFO(MetaNamespaceKeyFunc, s.indexer)

      cfg := &Config{
        Queue:            fifo,
        ListerWatcher:    s.listerWatcher,
        ObjectType:       s.objectType,
        FullResyncPeriod: s.resyncCheckPeriod,
        RetryOnError:     false,
        ShouldResync:     s.processor.shouldResync,

        Process: s.HandleDeltas,
      }

      func() {
        s.startedLock.Lock()
        defer s.startedLock.Unlock()

        s.controller = New(cfg)
        s.controller.(*controller).clock = s.clock
        s.started = true
      }()

      // Separate stop channel because Processor should be stopped strictly after controller
      processorStopCh := make(chan struct{})
      var wg wait.Group
      defer wg.Wait()              // Wait for Processor to stop
      defer close(processorStopCh) // Tell Processor to stop
      wg.StartWithChannel(processorStopCh, s.cacheMutationDetector.Run)
      wg.StartWithChannel(processorStopCh, s.processor.run)

      defer func() {
        s.startedLock.Lock()
        defer s.startedLock.Unlock()
        s.stopped = true // Don't want any new listeners
      }()
      s.controller.Run(stopCh)
    }

.. code-block:: go
   :lineno-start: 127
   :caption: k8s.io/client-go/informers/factory.go

    func (f *sharedInformerFactory) Start(stopCh <-chan struct{}) {
      f.lock.Lock()
      defer f.lock.Unlock()

      for informerType, informer := range f.informers {
        if !f.startedInformers[informerType] {
          go informer.Run(stopCh)
          f.startedInformers[informerType] = true
        }
      }
    }

.. code-block:: go
   :lineno-start: 140
   :caption: k8s.io/client-go/informers/factory.go


    func (f *sharedInformerFactory) WaitForCacheSync(stopCh <-chan struct{}) map[reflect.Type]bool {
      informers := func() map[reflect.Type]cache.SharedIndexInformer {
        f.lock.Lock()
        defer f.lock.Unlock()

        informers := map[reflect.Type]cache.SharedIndexInformer{}
        for informerType, informer := range f.informers {
          if f.startedInformers[informerType] {
            informers[informerType] = informer
          }
        }
        return informers
      }()

      res := map[reflect.Type]bool{}
      for informType, informer := range informers {
        res[informType] = cache.WaitForCacheSync(stopCh, informer.HasSynced)
      }
      return res
    }
























