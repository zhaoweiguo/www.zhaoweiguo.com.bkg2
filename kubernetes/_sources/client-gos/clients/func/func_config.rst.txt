func config
###########


.. code-block:: go
   :lineno-start: 549
   :caption: k8s.io/client-go/tools/clientcmd/client_config.go

    func BuildConfigFromFlags(masterUrl, kubeconfigPath string) (*restclient.Config, error) {
      loadingClientConfig := NewNonInteractiveDeferredLoadingClientConfig(
        &ClientConfigLoadingRules{ExplicitPath: kubeconfigPath},
        &ConfigOverrides{ClusterInfo: clientcmdapi.Cluster{Server: masterUrl}})
      return loadingClientConfig.ClientConfig()
    }

    func NewNonInteractiveDeferredLoadingClientConfig(loader ClientConfigLoader, overrides *ConfigOverrides) ClientConfig {
      return &DeferredLoadingClientConfig{
          loader: loader, 
          overrides: overrides, 
          icc: &inClusterClientConfig{overrides: overrides}
      }
    }






