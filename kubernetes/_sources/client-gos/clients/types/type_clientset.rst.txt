type Clientset
##############

Clientset
=========

.. code-block:: go
   :lineno-start: 63
   :caption: k8s.io/client-go/kubernetes/clientset.go

    type Interface interface {
      Discovery() discovery.DiscoveryInterface
      AppsV1() appsv1.AppsV1Interface
      AppsV1beta1() appsv1beta1.AppsV1beta1Interface
      AppsV1beta2() appsv1beta2.AppsV1beta2Interface
      BatchV1() batchv1.BatchV1Interface
      BatchV1beta1() batchv1beta1.BatchV1beta1Interface
      BatchV2alpha1() batchv2alpha1.BatchV2alpha1Interface
      CoreV1() corev1.CoreV1Interface
      ... ...
    }

.. code-block:: go
   :lineno-start: 105
   :caption: k8s.io/client-go/kubernetes/clientset.go

    type Clientset struct {
      *discovery.DiscoveryClient
      appsV1                       *appsv1.AppsV1Client
      appsV1beta1                  *appsv1beta1.AppsV1beta1Client
      appsV1beta2                  *appsv1beta2.AppsV1beta2Client
      batchV1                      *batchv1.BatchV1Client
      batchV1beta1                 *batchv1beta1.BatchV1beta1Client
      batchV2alpha1                *batchv2alpha1.BatchV2alpha1Client
      coreV1                       *corev1.CoreV1Client
      ... ...
    }

.. code-block:: go
   :lineno-start: 236
   :caption: k8s.io/client-go/kubernetes/clientset.go

    func (c *Clientset) CoreV1() corev1.CoreV1Interface {
      return c.coreV1
    }

CoreV1Client
============

.. code-block:: go
   :lineno-start: 105
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/core_client.go

    type CoreV1Interface interface {
      RESTClient() rest.Interface
      ComponentStatusesGetter
      ConfigMapsGetter
      EndpointsGetter
      EventsGetter
      LimitRangesGetter
      NamespacesGetter
      NodesGetter
      PersistentVolumesGetter
      PersistentVolumeClaimsGetter
      PodsGetter
      PodTemplatesGetter
      ReplicationControllersGetter
      ResourceQuotasGetter
      SecretsGetter
      ServicesGetter
      ServiceAccountsGetter
    }

.. code-block:: go
   :lineno-start: 105
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/pod.go

    type PodsGetter interface {
      Pods(namespace string) PodInterface
    }

.. code-block:: go
   :lineno-start: 49
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/core_client.go

    type CoreV1Client struct {
      restClient rest.Interface
    }

.. code-block:: go
   :lineno-start: 89
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/core_client.go

    func (c *CoreV1Client) Pods(namespace string) PodInterface {
      return &pods{
        client: c.RESTClient(),
        ns:     namespace,
      }
    }
    func (c *CoreV1Client) RESTClient() rest.Interface {
      if c == nil {
        return nil
      }
      return c.restClient
    }

pods
====

.. code-block:: go
   :lineno-start: 105
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/pod.go

    type PodInterface interface {
      Create(*v1.Pod) (*v1.Pod, error)
      Update(*v1.Pod) (*v1.Pod, error)
      UpdateStatus(*v1.Pod) (*v1.Pod, error)
      Delete(name string, options *metav1.DeleteOptions) error
      DeleteCollection(options *metav1.DeleteOptions, listOptions metav1.ListOptions) error
      Get(name string, options metav1.GetOptions) (*v1.Pod, error)
      List(opts metav1.ListOptions) (*v1.PodList, error)
      Watch(opts metav1.ListOptions) (watch.Interface, error)
      Patch(name string, pt types.PatchType, data []byte, subresources ...string) (result *v1.Pod, err error)
      PodExpansion
    }

.. code-block:: go
   :lineno-start: 53
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/pod.go

    type pods struct {
      client rest.Interface
      ns     string
    }

.. code-block:: go
   :lineno-start: 80
   :caption: k8s.io/client-go/kubernetes/typed/core/v1/pod.go

    func (c *pods) List(opts metav1.ListOptions) (result *v1.PodList, err error) {
      var timeout time.Duration

      result = &v1.PodList{}
      err = c.client.Get().   // 返回Request类型
        Namespace(c.ns).
        Resource("pods").
        VersionedParams(&opts, scheme.ParameterCodec).
        Timeout(timeout).     // 设置Request类型的几个参数
        Do().                 // 执行http请求
        Into(result)          // 把请求结果赋值到result
      return
    }


.. code-block:: go
   :lineno-start: 53
   :caption: k8s.io/client-go/kubernetes/core/v1/type.go

    type PodList struct {
      metav1.TypeMeta `json:",inline"`
      // Standard list metadata.
      // More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      // +optional
      metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

      // List of pods.
      // More info: https://git.k8s.io/community/contributors/devel/api-conventions.md
      Items []Pod `json:"items" protobuf:"bytes,2,rep,name=items"`
    }










