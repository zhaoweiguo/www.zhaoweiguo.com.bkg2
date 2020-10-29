.. _demo-discovery-client:

实例: discovery client
######################




.. code-block:: go
   :lineno-start: 11
   :caption: github.com/gosources/demo-kubernetes/client-go/client/discovery/main.go

    config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
    ...
    discoveryClient, err := discovery.NewDiscoveryClientForConfig(config)
    ...
    groups, apiResourceLists, err := discoveryClient.ServerGroupsAndResources()
    ...
    for _, group := range groups {
      log.Println(group)
    }
    for _, apiResourceList := range apiResourceLists {
      kind := apiResourceList.Kind
      apiVersion := apiResourceList.APIVersion
      apiResources := apiResourceList.APIResources
      groupVersion := apiResourceList.GroupVersion
    }

.. todo:: 实例先放这儿，解读后补上




