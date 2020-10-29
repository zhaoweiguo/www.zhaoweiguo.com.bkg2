func gen
########

clientset::

    config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
    clientset, err := kubernetes.NewForConfig(config)
    pods, err := clientset.CoreV1().Pods("").List(metav1.ListOptions{})

restClient::

    config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)

    config.APIPath = "api"
    config.GroupVersion = &corev1.SchemeGroupVersion
    config.NegotiatedSerializer = scheme.Codecs

    restClient, err := rest.RESTClientFor(config)

    result := &corev1.PodList{}
    err = restClient.Get().Namespace("default").
      Resource("pods").
      VersionedParams(&metav1.ListOptions{Limit: 500}, scheme.ParameterCodec).
      Do().Into(result)













