FIFO
####


.. code-block:: go
   :lineno-start: 47
   :caption: k8s.io/client-go/tools/cache/fifo.go

    type Queue interface {
      Store

      Pop(PopProcessFunc) (interface{}, error)

      AddIfNotPresent(interface{}) error

      HasSynced() bool

      Close()
    }













