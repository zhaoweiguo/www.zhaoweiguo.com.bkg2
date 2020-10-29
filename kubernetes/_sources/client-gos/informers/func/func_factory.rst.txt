informers.NewSharedInformerFactory
==================================

.. code-block:: go
   :lineno-start: 79
   :caption: k8s.io/client-go/informers/factory.go

    func NewSharedInformerFactory(client kubernetes.Interface, defaultResync time.Duration) SharedInformerFactory {
      return NewSharedInformerFactoryWithOptions(client, defaultResync)
    }

    func NewSharedInformerFactoryWithOptions(client kubernetes.Interface, defaultResync time.Duration, options ...SharedInformerOption) SharedInformerFactory {
      factory := &sharedInformerFactory{
        client:           client,
        namespace:        v1.NamespaceAll,
        defaultResync:    defaultResync,
        informers:        make(map[reflect.Type]cache.SharedIndexInformer),
        startedInformers: make(map[reflect.Type]bool),
        customResync:     make(map[reflect.Type]time.Duration),
      }

      // Apply all options
      for _, opt := range options {
        factory = opt(factory)
      }

      return factory
    }





