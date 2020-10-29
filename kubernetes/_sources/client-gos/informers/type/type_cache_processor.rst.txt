processor
#########

listener
========

.. code-block:: go
   :lineno-start: 465
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    type processorListener struct {
      nextCh chan interface{}
      addCh  chan interface{}

      handler ResourceEventHandler

      pendingNotifications buffer.RingGrowing

      requestedResyncPeriod time.Duration

      resyncPeriod time.Duration

      nextResync time.Time
      resyncLock sync.Mutex
    }


.. code-block:: go
   :lineno-start: 585
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    func (p *processorListener) determineNextResync(now time.Time) {
      p.resyncLock.Lock()
      defer p.resyncLock.Unlock()

      p.nextResync = now.Add(p.resyncPeriod)
    }

    func (p *processorListener) add(notification interface{}) {
      p.addCh <- notification
    }



sharedProcessor
===============

.. code-block:: go
   :lineno-start: 375
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    type sharedProcessor struct {
      listenersStarted bool
      listenersLock    sync.RWMutex
      listeners        []*processorListener
      syncingListeners []*processorListener
      clock            clock.Clock
      wg               wait.Group
    }

.. code-block:: go
   :lineno-start: 384
   :caption: k8s.io/client-go/tools/cache/shared_informer.go


    func (p *sharedProcessor) addListener(listener *processorListener) {
      p.listenersLock.Lock()
      defer p.listenersLock.Unlock()

      p.addListenerLocked(listener)
      if p.listenersStarted {
        p.wg.Start(listener.run)    // @todo
        p.wg.Start(listener.pop)
      }
    }

    func (p *sharedProcessor) addListenerLocked(listener *processorListener) {
      p.listeners = append(p.listeners, listener)
      p.syncingListeners = append(p.syncingListeners, listener)
    }


listener
========

.. code-block:: go
   :lineno-start: 540
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    func (p *processorListener) run() {
      stopCh := make(chan struct{})
      wait.Until(func() {
        err := wait.ExponentialBackoff(retry.DefaultRetry, func() (bool, error) {
          for next := range p.nextCh {
            switch notification := next.(type) {
            case updateNotification:
              p.handler.OnUpdate(notification.oldObj, notification.newObj)
            case addNotification:
              p.handler.OnAdd(notification.newObj)
            case deleteNotification:
              p.handler.OnDelete(notification.oldObj)
            default:
              utilruntime.HandleError(fmt.Errorf("unrecognized notification: %#v", next))
            }
          }
          // the only way to get here is if the p.nextCh is empty and closed
          return true, nil
        })

        if err == nil {
          close(stopCh)
        }
      }, 1*time.Minute, stopCh)
    }

.. code-block:: go
   :lineno-start: 510
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    func (p *processorListener) pop() {
      defer utilruntime.HandleCrash()
      defer close(p.nextCh) // Tell .run() to stop

      var nextCh chan<- interface{}
      var notification interface{}
      for {
        select {
        case nextCh <- notification:
          var ok bool
          notification, ok = p.pendingNotifications.ReadOne()
          if !ok { // Nothing to pop
            nextCh = nil // Disable this select case
          }
        case notificationToAdd, ok := <-p.addCh:
          if !ok {
            return
          }
          if notification == nil { // No notification to pop (and pendingNotifications is empty)
            notification = notificationToAdd
            nextCh = p.nextCh
          } else { // There is already a notification waiting to be dispatched
            p.pendingNotifications.WriteOne(notificationToAdd)
          }
        }
      }
    }















