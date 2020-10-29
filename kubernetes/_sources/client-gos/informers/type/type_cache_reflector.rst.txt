Reflector
#########

.. code-block:: go
   :lineno-start: 46
   :caption: k8s.io/client-go/tools/cache/reflector.go

    type Reflector struct {
      name string
      metrics *reflectorMetrics

      expectedType reflect.Type
      store Store
      listerWatcher ListerWatcher

      period       time.Duration
      resyncPeriod time.Duration
      ShouldResync func() bool
      clock clock.Clock

      lastSyncResourceVersion string
      lastSyncResourceVersionMutex sync.RWMutex
    }


.. code-block:: go
   :lineno-start: 297
   :caption: k8s.io/client-go/tools/cache/reflector.go

    func (r *Reflector) syncWith(items []runtime.Object, resourceVersion string) error {
      found := make([]interface{}, 0, len(items))
      for _, item := range items {
        found = append(found, item)
      }
      return r.store.Replace(found, resourceVersion)
    }



.. code-block:: go
   :lineno-start: 382
   :caption: k8s.io/client-go/tools/cache/reflector.go

    func (r *Reflector) setLastSyncResourceVersion(v string) {
      r.lastSyncResourceVersionMutex.Lock()
      defer r.lastSyncResourceVersionMutex.Unlock()
      r.lastSyncResourceVersion = v
    }

.. code-block:: go
   :lineno-start: 160
   :caption: k8s.io/client-go/tools/cache/reflector.go

    func (r *Reflector) ListAndWatch(stopCh <-chan struct{}) error {
      var resourceVersion string
      options := metav1.ListOptions{ResourceVersion: "0"}

      var list runtime.Object
      var err error
      list, err = r.listerWatcher.List(options)   // 1. 获取资源下所有对象的数据
      listMetaInterface, err := meta.ListAccessor(list)
      resourceVersion = listMetaInterface.GetResourceVersion()  // 2. 获取资源版本号

      items, err := meta.ExtractList(list)    // 3. 资源数据=>资源对象列表
      r.syncWith(items, resourceVersion)      // 4. 把资源对象和资源版本号存储到DeltaFIFO

      r.setLastSyncResourceVersion(resourceVersion)   // 5. 设置最新的资源版本号

      resyncerrc := make(chan error, 1)
      cancelCh := make(chan struct{})
      defer close(cancelCh)

      for {
        timeoutSeconds := int64(minWatchTimeout.Seconds() * (rand.Float64() + 1.0))
        options = metav1.ListOptions{
          ResourceVersion: resourceVersion,
          TimeoutSeconds: &timeoutSeconds,
        }

        w, err := r.listerWatcher.Watch(options)   // 最终会调用PodInformer的WatchFunc函数

        r.watchHandler(w, &resourceVersion, resyncerrc, stopCh)
      }
    }


.. code-block:: go
   :lineno-start: 306
   :caption: k8s.io/client-go/tools/cache/reflector.go

    func (r *Reflector) watchHandler(w watch.Interface, resourceVersion *string, 
                    errc chan error, stopCh <-chan struct{}) error {
      start := r.clock.Now()
      eventCount := 0

      defer w.Stop()

      for {
        select {
        case event, ok := <-w.ResultChan():
          meta, err := meta.Accessor(event.Object)
          newResourceVersion := meta.GetResourceVersion()

          switch event.Type {

          case watch.Added:
            err := r.store.Add(event.Object)
          case watch.Modified:
            err := r.store.Update(event.Object)
          case watch.Deleted:
            err := r.store.Delete(event.Object)
          }
          *resourceVersion = newResourceVersion
          r.setLastSyncResourceVersion(newResourceVersion)
          eventCount++
        }
      }
    }







