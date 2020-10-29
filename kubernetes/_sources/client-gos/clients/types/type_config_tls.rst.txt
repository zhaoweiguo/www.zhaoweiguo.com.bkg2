type config tls
###############


.. code-block:: go
   :lineno-start: 186
   :caption: k8s.io/client-go/rest/config.go

    type TLSClientConfig struct {
      // Server should be accessed without verifying the TLS certificate. For testing only.
      Insecure bool

      ServerName string

      CertFile string
      KeyFile string
      CAFile string

      CertData []byte
      KeyData []byte
      CAData []byte
    }















