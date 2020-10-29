gen
###

使用::

    sharedInformers := informers.NewSharedInformerFactory(clientSet, 0)
    informer := sharedInformers.Core().V1().Pods().Informer()
    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
      AddFunc: func(obj interface{}) {
      },
      UpdateFunc: func(oldObj, newObj interface{}) {
      },
      DeleteFunc: func(obj interface{}) {
      }
    })
    informer.Run(stopCh)











