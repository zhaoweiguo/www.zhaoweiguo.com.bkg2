.. _example_out-of-cluster-client-configuration:

实例out-of-cluster-client-configuration
#######################################

好了，我们先一起看下这一个项目，这个实例实现的是在集群外部连接集群获取clientset并返回pod列表。先看下核心代码：

.. code-block:: go
   :lineno-start: 52
   :caption: k8s.io/client-go/examples/out-of-cluster-client-configuration/main.go

    config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
    ...
    clientset, err := kubernetes.NewForConfig(config)
    ...
    podClient := clientset.CoreV1().Pods("")
    pods, err := podClient.List(metav1.ListOptions{})
    fmt.Printf("There are %d pods in the cluster\n", len(pods.Items))

核心代码就这么少，先看下它的步骤::

    1. 把~/.kube/config文件内容转化为「配置文件对象」
    2. 生成「clientset对象」
    3. 获取需要查询的结果，即「pod列表对象」

1. 获取 ``*k8s.io/client-go/rest.Config`` 对象::

    即把~/.kube/config中的凭证信息通过如下函数转化为rest.Config对象
    clientcmd.BuildConfigFromFlags("", *kubeconfig)

2. 获取 ``*k8s.io/client-go/kubernetes/Clientset`` 对象::

    clientset看名字需要知道，它是一个client集合，里面存放着多种client
    它的本质是对restClient的封装(这块后面会详解)
    通过如下命令：
    kubernetes.NewForConfig(config)
    获取kubernetes.Clientset对象
    client对象获取后就可以请求api-server(操作k8s本质是请求api-server)

3. 获取 ``k8s.io/client-go/kubernetes/typed/core/v1/PodList`` 对象::

    先获取Pod类型的client
    podClient := clientset.CoreV1().Pods("")
    前面说了clientset是client集合，里面有pod, deploy, service...类型的client

    podClient实现了 k8s.io/client-go/kubernetes/typed/core/v1/PodInterface 接口
    里面有List方法获取v1.PodList列表
    podClient.List(metav1.ListOptions{})








