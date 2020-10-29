Request
#######

.. code-block:: go
   :lineno-start: 80
   :caption: k8s.io/client-go/rest/request.go

    type Request struct {
      // required
      client HTTPClient
      verb   string

      baseURL     *url.URL
      content     ContentConfig
      serializers Serializers

      // generic components accessible via method setters
      pathPrefix string
      subpath    string
      params     url.Values
      headers    http.Header

      // structural elements of the request that are part of the Kubernetes API conventions
      namespace    string
      namespaceSet bool
      resource     string
      resourceName string
      subresource  string
      timeout      time.Duration

      // output
      err  error
      body io.Reader

      // This is only used for per-request timeouts, deadlines, and cancellations.
      ctx context.Context

      backoffMgr BackoffManager
      throttle   flowcontrol.RateLimiter
    }

.. code-block:: go
   :lineno-start: 244
   :caption: k8s.io/client-go/rest/request.go

    func (r *Request) Namespace(namespace string) *Request {
      ... ...
      r.namespaceSet = true
      r.namespace = namespace
      return r
    }
    func (r *Request) Resource(resource string) *Request {
      r.resource = resource
      return r
    }
    func (r *Request) VersionedParams(obj runtime.Object, codec runtime.ParameterCodec) *Request {
        params, err := codec.EncodeParameters(obj, version)
        for k, v := range params {
          if r.params == nil {
            r.params = make(url.Values)
          }
          r.params[k] = append(r.params[k], v...)
        }
        return r
    }
    func (r *Request) Timeout(d time.Duration) *Request {
      r.timeout = d
      return r
    }

.. code-block:: go
   :lineno-start: 800
   :caption: k8s.io/client-go/rest/request.go

    func (r *Request) Do() Result {
      var result Result
      err := r.request(func(req *http.Request, resp *http.Response) {
        result = r.transformResponse(resp, req)
      })
      return result
    }


.. code-block:: go
   :lineno-start: 678
   :caption: k8s.io/client-go/rest/request.go

    func (r *Request) request(fn func(*http.Request, *http.Response)) error {
      start := time.Now()
      client := r.client
      maxRetries := 10
      retries := 0

      for {
        url := r.URL().String()
        req, err := http.NewRequest(r.verb, url, r.body)
        req.Header = r.headers

        // 具体的http请求执行
        resp, err := client.Do(req)   // @todo 制造一个例子来走一遍逻辑

        done := func() bool {
          defer func() {
            const maxBodySlurpSize = 2 << 10
            if resp.ContentLength <= maxBodySlurpSize {
              io.Copy(ioutil.Discard, &io.LimitedReader{R: resp.Body, N: maxBodySlurpSize})
            }
            resp.Body.Close()
          }()

          retries++
          if seconds, wait := checkWait(resp); wait && retries < maxRetries {
            if seeker, ok := r.body.(io.Seeker); ok && r.body != nil {
              _, err := seeker.Seek(0, 0)
            }

            r.backoffMgr.Sleep(time.Duration(seconds) * time.Second)
            return false
          }
          fn(req, resp)
          return true
        }()
        if done {
          return nil
        }
      }
    }

.. code-block:: go
   :lineno-start: 1020
   :caption: k8s.io/client-go/rest/request.go

    func checkWait(resp *http.Response) (int, bool) {
      switch r := resp.StatusCode; {
      // any 500 error code and 429 can trigger a wait
      case r == http.StatusTooManyRequests, r >= 500:
      default:
        return 0, false
      }
      i, ok := retryAfterSeconds(resp)
      return i, ok
    }


.. code-block:: go
   :lineno-start: 832
   :caption: k8s.io/client-go/rest/request.go

    func (r *Request) transformResponse(resp *http.Response, req *http.Request) Result {
      var body []byte
      if resp.Body != nil {
        data, err := ioutil.ReadAll(resp.Body)
        switch err.(type) {
        case nil:
          body = data
        default:
          klog.Errorf("Unexpected error when reading response body: %#v", err)
          unexpectedErr := fmt.Errorf("Unexpected error %#v reading response body.", err)
          return Result{
            err: unexpectedErr,
          }
        }
      }

      // verify the content type is accurate
      contentType := resp.Header.Get("Content-Type")
      decoder := r.serializers.Decoder

      return Result{
        body:        body,
        contentType: contentType,
        statusCode:  resp.StatusCode,
        decoder:     decoder,   // config.NegotiatedSerializer.DecoderToVersion(info.Serializer, internalGV)
      }
    }










