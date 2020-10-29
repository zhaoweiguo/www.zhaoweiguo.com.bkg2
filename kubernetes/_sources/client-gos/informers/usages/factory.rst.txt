工厂模式
########

实例
====


.. code-block:: go
   :lineno-start: 32
   :caption: github.com/gosources/demo-kubernetes/client-go/informer/informer/main.go

    sharedInformers := informers.NewSharedInformerFactory(clientSet, 0)
    informer := sharedInformers.Core().V1().Pods().Informer()
    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
      AddFunc: func(obj interface{}) {
      ...
      },
      UpdateFunc: func(oldObj, newObj interface{}) {
      ...
      },
      DeleteFunc: func(obj interface{}) {
      ...
      },
    })
    sharedInformers.Start(stopCh)



构造生成factory
===============

前面已经学了如何生成clientset对象，现在来看下如何生成shareInformer对象。但这儿有个问题，如果每个资源实例都实例化一个informer，太多的informer同时ListAndWatch时，会执行过多重复的序列化和反序列化操作，这会导致API Server负载过重。不同的资源类型使用的是不同的Informer，所以我们使用每个资源类型共享一个Informer的工厂、单例模式来解决这个问题。下面我们来用一个例子来讲述一下工厂模式的实现：

.. code-block:: go
   :lineno-start: 32
   :caption: github.com/gosources/demo-kubernetes/client-go/informer/informer/main.go

    sharedInformers := informers.NewSharedInformerFactory(clientSet, 0)

基于前面生成的clientSet对象，执行 ``informers.NewSharedInformerFactory`` 命令就可以得到factory对象。我们进去看看


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

代码也很简单，就是实例化结构 ``sharedInformerFactory`` ，我们来看看 ``sharedInformerFactory`` 的结构：

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

结构比较简单，clientset对象client，命名空间namespace，同步锁lock，默认同步间隔时间defaultResync，基于对象类型来区分的个性化同步间隔数组customResync，基于对象类型的Informer数组informers，是否有Informer数组startedInformers（用于工厂模式判定factory是否已经实例化Informer）。下面再来看看``sharedInformerFactory``实现了什么接口：

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

通过factory获取informer资源
===========================

.. code-block:: go
   :lineno-start: 34
   :caption: github.com/gosources/demo-kubernetes/client-go/informer/informer/main.go

    informer := sharedInformers.Core().V1().Pods().Informer()

sharedInformers是informer的factory，所以它可以生成各种资源类型的Informer。上例就是生成Pod资源的Informer，还可以通过类似接口生成其他资源的Informer。

.. note:: 注意这儿的Core().V1().Pods()分别是GVR(Group, Version, Resource)。所以接口SharedInformerFactory实现了所有的Group对应的方法，如Apps(), Batch(), Core()...。

我们再进入informer目录，看下目录结构::

    $ cd informer
    $ tree -L 2
    ├── apps
    │   ├── interface.go
    │   ├── v1
    │   ├── v1beta1
    │   └── v1beta2
    ├── batch
    │   ├── interface.go
    │   ├── v1
    │   ├── v1beta1
    │   └── v2alpha1
    ├── core
    │   ├── interface.go
    │   └── v1
    ... ...

看目录就基本知道有哪些Group和Version。以app目录为例，再看下目录结构::

    $ cd ./apps 
    $ tree
    .
    ├── interface.go
    ├── v1
    │   ├── controllerrevision.go
    │   ├── daemonset.go
    │   ├── deployment.go
    │   ├── interface.go
    │   ├── replicaset.go
    │   └── statefulset.go
    ├── v1beta1
    │   ├── controllerrevision.go
    │   ├── deployment.go
    │   ├── interface.go
    │   └── statefulset.go
    └── v1beta2
        ├── controllerrevision.go
        ├── daemonset.go
        ├── deployment.go
        ├── interface.go
        ├── replicaset.go
        └── statefulset.go

其中每个Group目录下有一个interface.go文件，每一个子文件夹下的文件都是一个资源类型，文件名就是资源类型名。interface.go里面定义了一个Interface接口指定了这个Group下的接口方法，定义了一个group类来做具体的实现。如：


.. code-block:: go
   :lineno-start: 29
   :caption: k8s.io/client-go/informers/apps/interface.go

    type Interface interface {
      // V1 provides access to shared informers for resources in V1.
      V1() v1.Interface
      // V1beta1 provides access to shared informers for resources in V1beta1.
      V1beta1() v1beta1.Interface
      // V1beta2 provides access to shared informers for resources in V1beta2.
      V1beta2() v1beta2.Interface
    }

.. code-block:: go
   :lineno-start: 38
   :caption: k8s.io/client-go/informers/apps/interface.go

    type group struct {
      factory          internalinterfaces.SharedInformerFactory
      namespace        string
      tweakListOptions internalinterfaces.TweakListOptionsFunc
    }

上面实例以app组为例，app.Interface接口实现了V1(), V1beta1(), V1beta2()方法。app.group类的则做具体的实现，如：

.. code-block:: go
   :lineno-start: 50
   :caption: k8s.io/client-go/informers/apps/interface.go

    func (g *group) V1() v1.Interface {
      return v1.New(g.factory, g.namespace, g.tweakListOptions)
    }

同理可以继续往下看，调用PodInformer接口的Informer()方法，得到一个cache.SharedIndexInformer类型的Informer对象：

.. code-block:: go
   :lineno-start: 26
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    type PodInformer interface {
      Informer() cache.SharedIndexInformer
      Lister() v1.PodLister
    }

.. code-block:: go
   :lineno-start: 83
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    func (f *podInformer) Informer() cache.SharedIndexInformer {
      return f.factory.InformerFor(&corev1.Pod{}, f.defaultInformer)
    }





最后得到的Infomer对象的实现podInformer：

.. code-block:: go
   :lineno-start: 118
   :caption: k8s.io/client-go/informers/core/v1/interface.go

    func (v *version) Pods() PodInformer {
      return &podInformer{factory: v.factory, namespace: v.namespace, tweakListOptions: v.tweakListOptions}
    }



Informer增加事件处理
====================

.. code-block:: go
   :lineno-start: 35
   :caption: github.com/gosources/demo-kubernetes/client-go/informer/informer/main.go

    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
      AddFunc: func(obj interface{}) {
      ...
      },
      UpdateFunc: func(oldObj, newObj interface{}) {
      ...
      },
      DeleteFunc: func(obj interface{}) {
      ...
      },
    })

SharedIndexInformer包括两部分，一部分是index部分定义了索引部分，实现了AddIndexers和GetIndexer方法：

.. code-block:: go
   :lineno-start: 66
   :caption: k8s.io/client-go/tools/cache/shared_informer.go

    type SharedIndexInformer interface {
      SharedInformer
      // AddIndexers add indexers to the informer before it starts.
      AddIndexers(indexers Indexers) error
      GetIndexer() Indexer
    }

另一部分是SharedInformer接口定义的SharedInformer接口定义的Informer相关的方法，如：

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

在上面的例子中，我们主要是实现AddEventHandler方法，由于本部分主要讲解决factory的实现，这块暂不做详细讲述，只需要知道增加了事件处理。

Factory运行
===========

.. code-block:: go
   :lineno-start: 52
   :caption: github.com/gosources/demo-kubernetes/client-go/informer/informer/main.go

    sharedInformers.Start(stopCh)

前面看到Run方法来实现SharedInformer接口的运行，factory执行start方法时，就是把所有的sharedInformer都很行下Run()方法，我们看下它的主要实现：

.. code-block:: go
   :lineno-start: 127
   :caption: k8s.io/client-go/informer/factory.go

    func (f *sharedInformerFactory) Start(stopCh <-chan struct{}) {
    f.lock.Lock()
    defer f.lock.Unlock()

    for informerType, informer := range f.informers {
      if !f.startedInformers[informerType] {
        go informer.Run(stopCh)
        f.startedInformers[informerType] = true
      }
    }


到此，整个facotry就基本运行完毕。





