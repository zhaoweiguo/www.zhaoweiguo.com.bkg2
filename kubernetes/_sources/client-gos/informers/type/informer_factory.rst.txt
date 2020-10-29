Informer Factory
################





resyncPeriod指每过一段时间，清空本地缓存，从apiserver中做一次list。这样可以避免list&watch机制错误导致业务逻辑错误，但在大规模集群中，重新list的代价不容小视。部分人喜欢设成一个较大的值，部分人喜欢设为0，即完全信任etcd的能力。









