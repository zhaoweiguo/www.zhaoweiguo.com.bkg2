前言
####

在Kubernetes系统中，其他组件都是通过client-go的Informer机制与Kubernetes API Server进行通信的。也是通过Informer机制实现了不依赖任何中间件的情况下，保证消息的**实时性**，**可靠性**和**顺序性**。

3大核心组件
===========

Reflector::

    用于监控(Watch)指定的Kubernetes资源
    有Added, Updated, Deleted三种事件

DeltaFIFO::

    有两部分作用: FIFO队列和Delta对象
    它有队列的基本方法，如:
      Add, Update, Delete, List, Pop, Close等
    资源对象存储，保存资源的基本操作类型

Indexer::

    存储资源对象并自带索引的本地存储
    Indexer与etcd集群中的数据完全保持一致
    client-go可以直接从本地存储中存储数据，而不用再请求Kubernetes API Server，减轻API Server和etcd的压力






