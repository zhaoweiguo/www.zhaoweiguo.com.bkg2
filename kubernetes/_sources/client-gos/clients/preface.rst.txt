前言
####

大家好，在深入到代码深处之前，我们先在外围研究研究。所谓外围就是写一些小例子来使用client-go，在使用的过程中加深对``client-go``的理解。可能现在我们连用都不会呢，所以我们这一节先从``client-go``的``examples`` 目录下的几个小例子来讲一讲对``client-go``的使用。先看下``examples``目录内容::

     tree -L 1
    .
    ├── create-update-delete-deployment
    ├── fake-client
    ├── in-cluster-client-configuration
    ├── out-of-cluster-client-configuration
    └── workqueue

好了，这5个项目已经列出来了，每个项目都是干嘛的呢？我先在这儿给大家做一个简单的介绍:

* ``out-of-cluster-client-configuration``::

    首先大家要知道的是，使用client-go写的程序是操作Kubernetes的。
    我们之前已经使用kubectl操作过Kubernetes了，这样的操作基本步骤是:
    1. 从文件~/.kube/config获取连接Kubernetes凭证
    2. 连接api-server，发送http请求执行操作并获取结果
    本实例就是实现了类似kubectl get po的功能。

* ``in-cluster-client-configuration``::

    上面的例子是从文件~/.kube/config获取连接Kubernetes凭证
    这就有一个问题，这个程序可不可以(以及如何)在Kubernetes内部运行(以pod的形式)呢？
    答案是肯定的，如何获取凭证、如何运行我们后面介绍。
    实例 in-cluster-client-configuration 就是介绍了如何实现此目的。


* ``create-update-delete-deployment``::
    
    上面的2个实例比较简单，里面重点是实现了in-cluster和out-of-cluster情景下获取client实例。
    之后用获取pod列表和获取指定pod的信息来证明client创建成功。
    本实例实现了:
    1. 创建deployment的过程，类似命令: kubectl create -f deploy.yaml
    2. 修改deployment的过程，类似命令: kubectl apply -f deploy.yaml
    3. 查看deployment的过程，类似命令: kubectl get deploy
    4. 删除deployment的过程，类似命令: kubectl delete -f deploy.yaml

* ``fake-client``::
  
    这么大的一个项目，单元测试的重要性不言而喻，但我们不能弄一个真实的Kubernetes集群用于测试。
    因为:
    1. 即使单元测试失败，你不知道是集群出问题，还是功能有问题。
    2. 创建、修改、删除等操作是有状态的，大概率会出现数据问题导致单元测试失败。
    所以 fake-client 项目教你如何使用 k8s.io/client-go/kubernetes/fake 项目构造一个假的集群来做单元测试。
    我们先暂不讲，等后面讲单元测试时再专门拿出来讲。

* ``workqueue``::

    是client-go项目实现的一个队列，属于内容结构的用法
    我们暂不讲，等我们后面讲到时再回来看这个实例。


上面把五个例子简单介绍了一下，下面讲解这五个例子的源码。讲解的目的是对每一行代码的作用有个了解，不作更深入的源码剖析，更深入的剖析留给后面章节。






