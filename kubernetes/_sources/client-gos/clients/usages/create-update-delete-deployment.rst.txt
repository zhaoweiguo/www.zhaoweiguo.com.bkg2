实例create-update-delete-deployment
###################################

生成clientset对象
===================

.. code-block:: go
   :lineno-start: 54
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
    ...
    clientset, err := kubernetes.NewForConfig(config)
    ...
    deploymentsClient := clientset.AppsV1().Deployments(apiv1.NamespaceDefault)

上面这部分代码基本与 :ref:`out-of-cluster-client-configuration <example_out-of-cluster-client-configuration>` 实例相同，只不过我们现在获取的是deployment的client，就这一点不同。看完上两节的各位，对这块肯定不陌生了，那我们继续往下看：

创建deployment
====================

.. code-block:: go
   :lineno-start: 65
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    deployment := &appsv1.Deployment{
      ObjectMeta: metav1.ObjectMeta{
        Name: "demo-deployment",            // 指定deploy name
      },
      Spec: appsv1.DeploymentSpec{
        Replicas: int32Ptr(2),              // 指定replicas
        Selector: &metav1.LabelSelector{
          MatchLabels: map[string]string{
            "app": "demo",                  // 设定selector
          },
        },
        Template: apiv1.PodTemplateSpec{    // 指定template
          ObjectMeta: metav1.ObjectMeta{
            Labels: map[string]string{
              "app": "demo",
            },
          },
          Spec: apiv1.PodSpec{              // 指定spec
            Containers: []apiv1.Container{
              {
                Name:  "web",
                Image: "nginx:1.12",
                Ports: []apiv1.ContainerPort{
                  {
                    Name:          "http",
                    Protocol:      apiv1.ProtocolTCP,
                    ContainerPort: 80,
                  },
                },
              },
            },
          },
        },
      },
    }

上面我已经加了些注释方便大家理解，为了更方便理解，我把它转化成大家很熟悉的yaml文件：

.. literalinclude:: ./files/create-update-delete-deployment.yaml

yaml文件有了，下一步就是执行 ``kubectl create`` 命令了，那我们接着看如何执行 ``kubectl create`` 命令：

.. code-block:: go
   :lineno-start: 103
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    result, err := deploymentsClient.Create(deployment)
    fmt.Printf("Created deployment %q.\n", result.GetObjectMeta().GetName())

上面的命令就是执行了 ``kubectl create`` 命令并返回生成的deploy的name。因为大家对yaml文件很熟悉，所以有yaml文件解释，这一段应该比较容易理解。

修改deployment
==============

创建命令就完成了，下面看看修改deployment命令，在看修改之前，先看下这么一段注释:

.. code-block:: go
   :lineno-start: 112
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    //    You have two options to Update() this Deployment:
    //
    //    1. Modify the "deployment" variable and call: Update(deployment).
    //       This works like the "kubectl replace" command and it overwrites/loses changes
    //       made by other clients between you Create() and Update() the object.
    //    2. Modify the "result" returned by Get() and retry Update(result) until
    //       you no longer get a conflict error. This way, you can preserve changes made
    //       by other clients between Create() and Update(). This is implemented below
    //       using the retry utility package included with client-go. (RECOMMENDED)
    //
    // More Info:
    // https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency

上面这段注释，简单来说就是更新有两种：一种是直接修改deployment变量然后执行Update(deployment)函数，这种类似 ``kubectl replace`` 命令，有执行失败或覆盖掉其他client执行效果的副作用；另一种是使用retry工具包，多次尝试Get()得到result，然后修改变更点，最后再执行Update(result)函数，直到不再有 ``冲突`` 错误，即执行成功。

.. note:: 上面的deployment变量和使用Get()函数获取的result变量的不同主要在于result有版本的概念，即resourceVersion。当请求的resourceVersion与etcd中保存的不一致时，就会报conflict错误。


.. code-block:: go
   :lineno-start: 125
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    retryErr := retry.RetryOnConflict(retry.DefaultRetry, func() error {

      // 1. 获取deployment当前状态
      result, getErr := deploymentsClient.Get("demo-deployment", metav1.GetOptions{})

      // 2. 修改replicas和image
      result.Spec.Replicas = int32Ptr(1)                           // reduce replica count
      result.Spec.Template.Spec.Containers[0].Image = "nginx:1.13" // change nginx version

      // 3. 更新
      _, updateErr := deploymentsClient.Update(result)
      return updateErr
    })

看上面代码，其实就3步：获取、修改、更新。如果在获取和更新之间有其他client成功执行了更新操作，那么updateErr就会返回错误，retry机制会过段时间重新再试这3步，直到成功或重试次数用完。

查看deployment
==============


这块看完，我们再接着往下看，如何查看deployment：

.. code-block:: go
   :lineno-start: 146
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    list, err := deploymentsClient.List(metav1.ListOptions{})
    ...
    for _, d := range list.Items {
      fmt.Printf(" * %s (%d replicas)\n", d.Name, *d.Spec.Replicas)
    }

这段代码就是获取deploy列表，并打印相关信息，没啥说的，和 :ref:`实例out-of-cluster-client-configuration<example_out-of-cluster-client-configuration>` 类似，只不过这次是获取deployment列表。

删除deployment
==============

再接着往下看删除：

.. code-block:: go
   :lineno-start: 157
   :caption: k8s.io/client-go/examples/create-update-delete-deployment/main.go

    deletePolicy := metav1.DeletePropagationForeground
    err := deploymentsClient.Delete("demo-deployment", &metav1.DeleteOptions{
      PropagationPolicy: &deletePolicy,
    })

这里要说的删除机制有3种：Orphan，Background和Foreground::

    Foreground:删除控制器之前，所管理的资源对象必须先删除；
    Background：删除控制器后，所管理的资源对象由GC删除；
    Orphan：只删除控制器对象,不删除控制器所管理的资源对象。













