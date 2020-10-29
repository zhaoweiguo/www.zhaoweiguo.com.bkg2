type
####

sharedInformerFactory
=====================

.. code-block:: go
   :lineno-start: 186
   :caption: k8s.io/client-go/informers/factory.go

    type SharedInformerFactory interface {
      internalinterfaces.SharedInformerFactory
      ForResource(resource schema.GroupVersionResource) (GenericInformer, error)
      WaitForCacheSync(stopCh <-chan struct{}) map[reflect.Type]bool

      Apps() apps.Interface
      Batch() batch.Interface
      Core() core.Interface
      ...
    }

.. code-block:: go
   :lineno-start: 34
   :caption: k8s.io/client-go/informers/interalinterface/factory_interfaces.go

    type SharedInformerFactory interface {
      Start(stopCh <-chan struct{})
      InformerFor(obj runtime.Object, newFunc NewInformerFunc) cache.SharedIndexInformer
    }
    type NewInformerFunc func(kubernetes.Interface, time.Duration) cache.SharedIndexInformer


.. code-block:: go
   :lineno-start: 54
   :caption: k8s.io/client-go/informers/factory.go

    type sharedInformerFactory struct {
      client           kubernetes.Interface
      namespace        string
      tweakListOptions internalinterfaces.TweakListOptionsFunc
      lock             sync.Mutex
      defaultResync    time.Duration
      customResync     map[reflect.Type]time.Duration

      informers map[reflect.Type]cache.SharedIndexInformer

      startedInformers map[reflect.Type]bool
    }

.. code-block:: go
   :lineno-start: 238
   :caption: k8s.io/client-go/informers/factory.go

    func (f *sharedInformerFactory) Core() core.Interface {
      return core.New(f, f.namespace, f.tweakListOptions)
    }

.. code-block:: go
   :lineno-start: 238
   :caption: k8s.io/client-go/informers/core/interface.go

    func New(f internalinterfaces.SharedInformerFactory, namespace string, tweakListOptions internalinterfaces.TweakListOptionsFunc) Interface {
      return &group{factory: f, namespace: namespace, tweakListOptions: tweakListOptions}
    }

group
=====


.. code-block:: go
   :lineno-start: 27
   :caption: k8s.io/client-go/informers/core/interface.go

    type Interface interface {
      V1() v1.Interface
    }

.. code-block:: go
   :lineno-start: 32
   :caption: k8s.io/client-go/informers/core/interface.go

    type group struct {
      factory          internalinterfaces.SharedInformerFactory
      namespace        string
      tweakListOptions internalinterfaces.TweakListOptionsFunc
    }

.. code-block:: go
   :lineno-start: 44
   :caption: k8s.io/client-go/informers/core/interface.go

    func (g *group) V1() v1.Interface {
      return v1.New(g.factory, g.namespace, g.tweakListOptions)
    }

.. code-block:: go
   :lineno-start: 68
   :caption: k8s.io/client-go/informers/core/v1/interface.go

    func New(f internalinterfaces.SharedInformerFactory, namespace string, tweakListOptions internalinterfaces.TweakListOptionsFunc) Interface {
      return &version{factory: f, namespace: namespace, tweakListOptions: tweakListOptions}
    }

version
=======

.. code-block:: go
   :lineno-start: 26
   :caption: k8s.io/client-go/informers/core/v1/interface.go

    type Interface interface {
      Namespaces() NamespaceInformer
      Nodes() NodeInformer
      Pods() PodInformer
      Services() ServiceInformer
      ...
    }

.. code-block:: go
   :lineno-start: 61
   :caption: k8s.io/client-go/informers/core/v1/interface.go

    type version struct {
      factory          internalinterfaces.SharedInformerFactory
      namespace        string
      tweakListOptions internalinterfaces.TweakListOptionsFunc
    }

.. code-block:: go
   :lineno-start: 118
   :caption: k8s.io/client-go/informers/core/v1/interface.go

    func (v *version) Pods() PodInformer {
      return &podInformer{factory: v.factory, namespace: v.namespace, tweakListOptions: v.tweakListOptions}
    }

podInformer
===========

.. code-block:: go
   :lineno-start: 26
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    type PodInformer interface {
      Informer() cache.SharedIndexInformer
      Lister() v1.PodLister
    }

.. code-block:: go
   :lineno-start: 41
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    type podInformer struct {
      factory          internalinterfaces.SharedInformerFactory
      tweakListOptions internalinterfaces.TweakListOptionsFunc
      namespace        string
    }

.. code-block:: go
   :lineno-start: 83
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    func (f *podInformer) Informer() cache.SharedIndexInformer {
      return f.factory.InformerFor(&corev1.Pod{}, f.defaultInformer)
    }

    func (f *podInformer) Lister() v1.PodLister {
      return v1.NewPodLister(f.Informer().GetIndexer())
    }

.. code-block:: go
   :lineno-start: 79
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    func (f *podInformer) defaultInformer(client kubernetes.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
      indexers := cache.Indexers{"namespace": cache.MetaNamespaceIndexFunc}
      return NewFilteredPodInformer(client, f.namespace, resyncPeriod, indexers, f.tweakListOptions)
    }



sharedInformerFactory
=====================

.. code-block:: go
   :lineno-start: 163
   :caption: k8s.io/client-go/informers/factory.go

    func (f *sharedInformerFactory) InformerFor(obj runtime.Object, newFunc internalinterfaces.NewInformerFunc) cache.SharedIndexInformer {
      f.lock.Lock()
      defer f.lock.Unlock()

      informerType := reflect.TypeOf(obj)
      informer, exists := f.informers[informerType]
      if exists {
        return informer
      }

      resyncPeriod, exists := f.customResync[informerType]
      if !exists {
        resyncPeriod = f.defaultResync
      }

      informer = newFunc(f.client, resyncPeriod)
      f.informers[informerType] = informer

      return informer
    }
















