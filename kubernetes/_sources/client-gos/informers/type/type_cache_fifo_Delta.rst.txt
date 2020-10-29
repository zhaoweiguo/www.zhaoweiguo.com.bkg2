DeltaFIFO
#########

.. code-block:: go
   :lineno-start: 96
   :caption: k8s.io/client-go/tools/cache/delta_fifo.go

    type DeltaFIFO struct {
        lock sync.RWMutex
        cond sync.Cond

        items map[string]Deltas
        queue []string
        populated bool

        initialPopulationCount int

        keyFunc KeyFunc

        knownObjects KeyListerGetter

        closed     bool
        closedLock sync.Mutex
    }


.. code-block:: go
   :lineno-start: 300
   :caption: k8s.io/client-go/tools/cache/delta_fifo.go

    func (f *DeltaFIFO) queueActionLocked(actionType DeltaType, obj interface{}) error {
      id, err := f.KeyOf(obj)   // 获取资源对象key

      newDeltas := append(f.items[id], Delta{actionType, obj})
      newDeltas = dedupDeltas(newDeltas)   // 去重

      if len(newDeltas) > 0 {
        if _, exists := f.items[id]; !exists {
          f.queue = append(f.queue, id)
        }
        f.items[id] = newDeltas
        f.cond.Broadcast()
      } else {
        // We need to remove this from our map (extra items in the queue are
        // ignored if they are not in the map).
        delete(f.items, id)
      }
      return nil
    }



.. code-block:: go
   :lineno-start: 397
   :caption: k8s.io/client-go/tools/cache/delta_fifo.go

    func (f *DeltaFIFO) Pop(process PopProcessFunc) (interface{}, error) {
      f.lock.Lock()
      defer f.lock.Unlock()
      for {
        for len(f.queue) == 0 {
          f.cond.Wait()
        }

        id := f.queue[0]   // 取出第一个
        f.queue = f.queue[1:]
        item, ok := f.items[id]

        delete(f.items, id)
        err := process(item)      // 调用回调函数，让上层处理
        if e, ok := err.(ErrRequeue); ok {
          f.addIfNotPresent(id, item)
          err = e.Err
        }
        return item, err
      }
    }














