func request
############

.. code-block:: go
   :lineno-start: 115
   :caption: k8s.io/client-go/rest/request.go

    func NewRequest(client HTTPClient, verb string, baseURL *url.URL, versionedAPIPath string, content ContentConfig, serializers Serializers, backoff BackoffManager, throttle flowcontrol.RateLimiter, timeout time.Duration) *Request {

      pathPrefix := "/"
      r := &Request{
        client:      client,
        verb:        verb,
        baseURL:     baseURL,
        pathPrefix:  path.Join(pathPrefix, versionedAPIPath),
        content:     content,
        serializers: serializers,
        backoffMgr:  backoff,
        throttle:    throttle,
        timeout:     timeout,
      }
      switch {
      case len(content.AcceptContentTypes) > 0:
        r.SetHeader("Accept", content.AcceptContentTypes)
      case len(content.ContentType) > 0:
        r.SetHeader("Accept", content.ContentType+", */*")
      }
      return r
    }







