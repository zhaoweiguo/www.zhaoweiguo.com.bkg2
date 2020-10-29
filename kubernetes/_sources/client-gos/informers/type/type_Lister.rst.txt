Lister
######



.. code-block:: go
   :lineno-start: 29
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    type PodLister interface {
      List(selector labels.Selector) (ret []*v1.Pod, err error)
      Pods(namespace string) PodNamespaceLister
                            // type PodListerExpansion interface{}
      PodListerExpansion    // PodListerExpansion allows custom methods to be added to PodLister
    }

.. code-block:: go
   :lineno-start: 38
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    type podLister struct {
      indexer cache.Indexer
    }


.. code-block:: go
   :lineno-start: 77
   :caption: k8s.io/client-go/informers/core/v1/pod.go

    func (s podNamespaceLister) List(selector labels.Selector) (ret []*v1.Pod, err error) {
      err = cache.ListAllByNamespace(s.indexer, s.namespace, selector, func(m interface{}) {
        ret = append(ret, m.(*v1.Pod))
      })
      return ret, err
    }

    func (s podNamespaceLister) Get(name string) (*v1.Pod, error) {
      obj, exists, err := s.indexer.GetByKey(s.namespace + "/" + name)
      if err != nil {
        return nil, err
      }
      if !exists {
        return nil, errors.NewNotFound(v1.Resource("pod"), name)
      }
      return obj.(*v1.Pod), nil
    }

















