func clientset
##############

.. code-block:: go
   :lineno-start: 334
   :caption: k8s.io/client-go/kubernetes/clientset.go

    func NewForConfig(c *rest.Config) (*Clientset, error) {
      cs.appsV1, err = appsv1.NewForConfig(&configShallowCopy)
      cs.appsV1beta1, err = appsv1beta1.NewForConfig(&configShallowCopy)
      cs.appsV1beta2, err = appsv1beta2.NewForConfig(&configShallowCopy)
      cs.batchV1, err = batchv1.NewForConfig(&configShallowCopy)
      cs.batchV1beta1, err = batchv1beta1.NewForConfig(&configShallowCopy)
      cs.batchV2alpha1, err = batchv2alpha1.NewForConfig(&configShallowCopy)
      cs.coreV1, err = corev1.NewForConfig(&configShallowCopy)
      ... ...
    }

.. code-block:: go
   :lineno-start: 118
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/core_client.go

    func NewForConfig(c *rest.Config) (*CoreV1Client, error) {
      config := *c
      err := setConfigDefaults(&config);
      
      client, err := rest.RESTClientFor(&config)
      return &CoreV1Client{client}, nil
    }

.. code-block:: go
   :lineno-start: 49
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/core_client.go

    func setConfigDefaults(config *rest.Config) error {
      GroupName := ""
      config.GroupVersion = &schema.GroupVersion{Group: GroupName, Version: "v1"}
      config.APIPath = "/api"
      config.NegotiatedSerializer = serializer.DirectCodecFactory{CodecFactory: scheme.Codecs}
    }






