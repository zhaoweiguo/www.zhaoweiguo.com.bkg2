tool
====


.. code-block:: go
   :lineno-start: 549
   :caption: k8s.io/client-go/tools/clientcmd/client_config.go

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



    type DirectClientConfig struct {
      config         clientcmdapi.Config
      contextName    string
      overrides      *ConfigOverrides
      fallbackReader io.Reader
      configAccess   ConfigAccess
      // promptedCredentials store the credentials input by the user
      promptedCredentials promptedCredentials
    }


    type inClusterClientConfig struct {
      overrides               *ConfigOverrides
      inClusterConfigProvider func() (*restclient.Config, error)
    }














