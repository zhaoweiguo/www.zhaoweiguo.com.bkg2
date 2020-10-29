.. _example_in-cluster-client-configuration:

实例in-cluster-client-configuration
###################################

我们上一节讲了在集群外使用``client-go``的例子，这一节讲一下在集群内部怎么使用``client-go``，先看下核心代码

.. code-block:: go
   :lineno-start: 51
   :caption: k8s.io/client-go/examples/in-cluster-client-configuration/main.go

    config, err := rest.InClusterConfig()
    ...
    clientset, err := kubernetes.NewForConfig(config)
    ...
    pods, err := clientset.CoreV1().Pods("").List(metav1.ListOptions{})
    fmt.Printf("There are %d pods in the cluster\n", len(pods.Items))

我们看到这段代码和上一节看的代码很相似，只有每一步获取「配置文件对象」的方法不同。它也是三步::

    1. 获取「配置文件对象」
    2. 生成「clientset对象」
    3. 获取需要查询的结果，即「pod列表对象」

我们只简单讲下与上一节不同的第一步::

    第一步本质是获取 「*k8s.io/client-go/rest.Config 对象」
    这一块，我们后面再详细讲，现在我们只需要知道
    在集群内部凭证在/var/run/secrets/kubernetes.io/serviceaccount目录中
    使用方法rest.InClusterConfig()能够获取*rest.Config对象








