func RESTClient
###############



.. code-block:: go
   :lineno-start: 61
   :caption: k8s.io/client-go/rest/config.go

    func RESTClientFor(config *Config) (*RESTClient, error) {
      qps := config.QPS
      burst := config.Burst
      baseURL, versionedAPIPath, err := defaultServerUrlFor(config)
      transport, err := TransportFor(config)

      var httpClient *http.Client
      if transport != http.DefaultTransport {
        httpClient = &http.Client{Transport: transport}
        if config.Timeout > 0 {
          httpClient.Timeout = config.Timeout
        }
      }

      return NewRESTClient(baseURL, versionedAPIPath, config.ContentConfig, qps, burst, config.RateLimiter, httpClient)
    }

.. code-block:: go
   :lineno-start: 94
   :caption: k8s.io/client-go/rest/client.go

    func NewRESTClient(baseURL *url.URL, versionedAPIPath string, config ContentConfig, maxQPS float32, maxBurst int, rateLimiter flowcontrol.RateLimiter, client *http.Client) (*RESTClient, error) {
      base := *baseURL

      config.ContentType = "application/json"
      serializers, err := createSerializers(config)

      var throttle flowcontrol.RateLimiter
      if maxQPS > 0 && rateLimiter == nil {
        throttle = flowcontrol.NewTokenBucketRateLimiter(maxQPS, maxBurst)
      } else if rateLimiter != nil {
        throttle = rateLimiter
      }
      return &RESTClient{
        base:             &base,
        versionedAPIPath: versionedAPIPath,
        contentConfig:    config,
        serializers:      *serializers,
        createBackoffMgr: readExpBackoffConfig,
        Throttle:         throttle,
        Client:           client,
      }, nil
    }


.. code-block:: go
   :lineno-start: 161
   :caption: k8s.io/client-go/rest/client.go

    func createSerializers(config ContentConfig) (*Serializers, error) {
      mediaTypes := config.NegotiatedSerializer.SupportedMediaTypes()
      contentType := config.ContentType
      mediaType, _, err := mime.ParseMediaType(contentType)
      info, ok := runtime.SerializerInfoForMediaType(mediaTypes, mediaType)

      internalGV := schema.GroupVersions{
        {
          Group:   config.GroupVersion.Group,
          Version: runtime.APIVersionInternal,
        },
        // always include the legacy group as a decoding target to handle non-error `Status` return types
        {
          Group:   "",
          Version: runtime.APIVersionInternal,
        },
      }

      s := &Serializers{
        Encoder: config.NegotiatedSerializer.EncoderForVersion(info.Serializer, *config.GroupVersion),
        Decoder: config.NegotiatedSerializer.DecoderToVersion(info.Serializer, internalGV),

        RenegotiatedDecoder: func(contentType string, params map[string]string) (runtime.Decoder, error) {
          info, ok := runtime.SerializerInfoForMediaType(mediaTypes, contentType)
          if !ok {
            return nil, fmt.Errorf("serializer for %s not registered", contentType)
          }
          return config.NegotiatedSerializer.DecoderToVersion(info.Serializer, internalGV), nil
        },
      }
      if info.StreamSerializer != nil {
        s.StreamingSerializer = info.StreamSerializer.Serializer
        s.Framer = info.StreamSerializer.Framer
      }

      return s, nil
    }







