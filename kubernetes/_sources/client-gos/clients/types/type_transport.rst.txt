type
####


.. code-block:: go
   :lineno-start: 27
   :caption: k8s.io/client-go/transport/config.go

    type Config struct {
      UserAgent string

      TLS TLSConfig

      Username string
      Password string
      BearerToken string
      BearerTokenFile string

      Impersonate ImpersonationConfig

      Transport http.RoundTripper

      WrapTransport WrapperFunc

      Dial func(ctx context.Context, network, address string) (net.Conn, error)
    }





