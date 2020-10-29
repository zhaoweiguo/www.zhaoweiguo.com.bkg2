type config
###########


.. code-block:: go
   :lineno-start: 246
   :caption: k8s.io/client-go/rest/config.go

    type ContentConfig struct {
      AcceptContentTypes string
      // default: "application/json"
      ContentType string

      GroupVersion *schema.GroupVersion

      NegotiatedSerializer runtime.NegotiatedSerializer
    }

.. code-block:: go
   :lineno-start: 52
   :caption: k8s.io/client-go/rest/config.go

    type Config struct {
      Host string
      APIPath string

      ContentConfig

      Username string
      Password string
      BearerToken string
      BearerTokenFile string

      Impersonate ImpersonationConfig

      AuthProvider *clientcmdapi.AuthProviderConfig
      AuthConfigPersister AuthProviderConfigPersister

      ExecProvider *clientcmdapi.ExecConfig

      TLSClientConfig

      UserAgent string

      Transport http.RoundTripper
      WrapTransport transport.WrapperFunc

      // DefaultQPS: 5
      QPS float32
      Burst int
      RateLimiter flowcontrol.RateLimiter

      Timeout time.Duration

      Dial func(ctx context.Context, network, address string) (net.Conn, error)
    }




