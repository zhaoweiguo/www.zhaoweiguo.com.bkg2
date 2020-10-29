.. _demo-rest-client:

实例: rest client
#################

client-go项目的example中并没有提供rest client的实例，但它本身是构成clientset的基础，学习它有助于我们更好的了解client-go项目。

.. code-block:: go
   :lineno-start: 15
   :caption: github.com/gosources/demo-kubernetes/client-go/client/rest/main.go

    config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
    ...
    config.APIPath="api"
    config.GroupVersion=&corev1.SchemeGroupVersion
    config.NegotiatedSerializer = scheme.Codecs
    restClient, err := rest.RESTClientFor(config)
    ...
    result := &corev1.PodList{}
    err = restClient.Get().Namespace("default").
      Resource("pods").
      VersionedParams(&metav1.ListOptions{Limit: 500}, scheme.ParameterCodec).
      Do().Into(result)
    ...
    for _, d := range result.Items {
      log.Printf("NameSpace:%v \t Name:%v \t Status:%+v\n", d.Namespace, d.Name, d.Status)
    }

需要手工指定group, version, kind。

.. todo:: 实例先放这儿，解读后补上






