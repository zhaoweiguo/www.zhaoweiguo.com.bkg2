tool2
=====


.. code-block:: go
   :lineno-start: 47
   :caption: k8s.io/client-go/tools/clientcmd/merged_client_builder.go

    type InClusterConfig interface {
      ClientConfig
      Possible() bool
    }


.. code-block:: go
   :lineno-start: 56
   :caption: k8s.io/client-go/tools/clientcmd/client_config.go

    // ClientConfig is used to make it easy to get an api server client
    type ClientConfig interface {
      // RawConfig returns the merged result of all overrides
      RawConfig() (clientcmdapi.Config, error)
      // ClientConfig returns a complete client config
      ClientConfig() (*restclient.Config, error)
      // Namespace returns the namespace resulting from the merged
      // result of all overrides and a boolean indicating if it was
      // overridden
      Namespace() (string, bool, error)
      // ConfigAccess returns the rules for loading/persisting the config.
      ConfigAccess() ConfigAccess
    }

.. code-block:: go
   :lineno-start: 34
   :caption: k8s.io/client-go/tools/clientcmd/merged_client_builder.go

    // DeferredLoadingClientConfig is a ClientConfig interface that is backed by a client config loader.
    // It is used in cases where the loading rules may change after you've instantiated them 
    //    and you want to be sure that the most recent rules are used.  
    // This is useful in cases where you bind flags to loading rule parameters 
    // before the parse happens and you want your calling code to be ignorant of 
    // how the values are being mutated to avoid
    // passing extraneous information down a call stack
    type DeferredLoadingClientConfig struct {
      loader         ClientConfigLoader
      overrides      *ConfigOverrides
      fallbackReader io.Reader

      clientConfig ClientConfig
      loadingLock  sync.Mutex

      // provided for testing
      icc InClusterConfig
    }

    func (config *DeferredLoadingClientConfig) ClientConfig() (*restclient.Config, error) {
      mergedClientConfig, err := config.createClientConfig()

      // load the configuration and return on non-empty errors and if the
      // content differs from the default config
      mergedConfig, err := mergedClientConfig.ClientConfig()
      switch {
      case err != nil:
        if !IsEmptyConfig(err) {
          // return on any error except empty config
          return nil, err
        }
      case mergedConfig != nil:
        // the configuration is valid, but if this is equal to the defaults we should try
        // in-cluster configuration
        if !config.loader.IsDefaultConfig(mergedConfig) {
          return mergedConfig, nil
        }
      }

      // check for in-cluster configuration and use it
      if config.icc.Possible() {
        klog.V(4).Infof("Using in-cluster configuration")
        return config.icc.ClientConfig()
      }

      // return the result of the merged client config
      return mergedConfig, err
    }











    type ConfigOverrides struct {
      AuthInfo clientcmdapi.AuthInfo
      // ClusterDefaults are applied before the configured cluster info is loaded.
      ClusterDefaults clientcmdapi.Cluster
      ClusterInfo     clientcmdapi.Cluster
      Context         clientcmdapi.Context
      CurrentContext  string
      Timeout         string
    }

    type ClientConfigLoadingRules struct {
      ExplicitPath string
      Precedence   []string

      // MigrationRules is a map of destination files to source files.  
      // If a destination file is not present, then the source file is checked.
      // If the source file is present, then it is copied to the destination file 
      // BEFORE any further loading happens.
      MigrationRules map[string]string

      // DoNotResolvePaths indicates whether or not to resolve paths 
      // with respect to the originating files.  
      // This is phrased as a negative so
      // that a default object that doesn't set this will usually get the behavior it wants.
      DoNotResolvePaths bool

      // DefaultClientConfig is an optional field indicating 
      // what rules to use to calculate a default configuration.
      // This should match the overrides passed in to ClientConfig loader.
      DefaultClientConfig ClientConfig
    }

