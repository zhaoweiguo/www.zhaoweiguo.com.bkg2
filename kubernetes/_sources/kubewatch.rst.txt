kubewatch项目
#############

入口::

    main()

Cobra配置相关, root.go::

    cmd.Execute()
    cobra.Run(config)
    pkg/client.Run(config)

eventHandler处理相关, run.go::

    eventHandler = ParseEventHandler(config) => webhook.Webhook, Slack...
    pkg/controller.start(config, eventHandler)

controller::

    kubeClient = 
        1. 集群外: utils.GetClientOutOfCluster
        2. 集群内: utils.GetClient()
    informer=tool/cache.NewSharedIndexInformer(lw ListerWatcher, runtime.Object, time.Duration, Indexers)
    其中:
      lw=&tool/cache.ListWatch{lf ListFunc{}, wf WatchFunc{}}
      其中:
        lw = kubeClient.CoreV1().Events(conf.Namespace).List(options)
        wf = kubeClient.CoreV1().Events(conf.Namespace).Watch(options)

    controller:=pkg/controller.newResourceController(kubeClient, eventHandler, informer, "NodeNotReady")
      queue := util/workqueue.NewRateLimitingQueue(workqueue.DefaultControllerRateLimiter())
      @client-go/informer.AddEventHandler(handler ResourceEventHandler)
      handler=tool/cache.ResourceEventHandlerFuncs{AddFunc, UpdateFunc, DeleteFunc}
      其中:
        AddFunc, UpdateFunc, DeleteFunc
          logrus.Infof(xxx)
          queue.Add(newEvent)
      返回:
        &Controller{
          logger:       logrus.WithField("pkg", "kubewatch-"+resourceType),
          clientset:    client,
          informer:     informer,
          queue:        queue,
          eventHandler: eventHandler,
        }
    controller.Run()
    controller.informer.Run()






