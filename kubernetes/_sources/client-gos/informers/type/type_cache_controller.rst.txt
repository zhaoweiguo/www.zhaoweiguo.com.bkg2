Controller
##########



.. code-block:: go
   :lineno-start: 82
   :caption: k8s.io/client-go/tools/cache/controller.go

    type Controller interface {
      Run(stopCh <-chan struct{})
      HasSynced() bool
      LastSyncResourceVersion() string
    }


.. code-block:: go
   :lineno-start: 75
   :caption: k8s.io/client-go/tools/cache/controller.go

    type controller struct {
      config         Config
      reflector      *Reflector
      reflectorMutex sync.RWMutex
      clock          clock.Clock
    }


.. code-block:: go
   :lineno-start: 100
   :caption: k8s.io/client-go/tools/cache/controller.go

    func (c *controller) Run(stopCh <-chan struct{}) {
      defer utilruntime.HandleCrash()
      go func() {
        <-stopCh
        c.config.Queue.Close()
      }()
      r := NewReflector(
        c.config.ListerWatcher,
        c.config.ObjectType,
        c.config.Queue,
        c.config.FullResyncPeriod,
      )
      r.ShouldResync = c.config.ShouldResync
      r.clock = c.clock

      c.reflectorMutex.Lock()
      c.reflector = r
      c.reflectorMutex.Unlock()

      var wg wait.Group
      defer wg.Wait()

      wg.StartWithChannel(stopCh, r.Run)

      wait.Until(c.processLoop, time.Second, stopCh)
    }


Config
======

.. code-block:: go
   :lineno-start: 30
   :caption: k8s.io/client-go/tools/cache/controller.go

    type Config struct {
      Queue

      ListerWatcher

      Process ProcessFunc

      ObjectType runtime.Object

      FullResyncPeriod time.Duration

      ShouldResync ShouldResyncFunc

      RetryOnError bool
    }











