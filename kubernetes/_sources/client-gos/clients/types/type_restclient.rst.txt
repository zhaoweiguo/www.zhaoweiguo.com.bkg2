type2
#####

RESTClient
==========

.. code-block:: go
   :lineno-start: 43
   :caption: k8s.io/client-go/rest/client.go

    type Interface interface {
      GetRateLimiter() flowcontrol.RateLimiter
      Verb(verb string) *Request
      Post() *Request
      Put() *Request
      Patch(pt types.PatchType) *Request
      Get() *Request
      Delete() *Request
      APIVersion() schema.GroupVersion
    }

.. code-block:: go
   :lineno-start: 61
   :caption: k8s.io/client-go/rest/client.go

    type RESTClient struct {
      base *url.URL
      versionedAPIPath string

      contentConfig ContentConfig

      serializers Serializers

      createBackoffMgr func() BackoffManager

      Throttle flowcontrol.RateLimiter

      Client *http.Client
    }

.. code-block:: go
   :lineno-start: 246
   :caption: k8s.io/client-go/rest/client.go

    func (c *RESTClient) Get() *Request {
      return c.Verb("GET")
    }

    func (c *RESTClient) Verb(verb string) *Request {
      backoff := c.createBackoffMgr()

      if c.Client == nil {
        return NewRequest(nil, verb, c.base, c.versionedAPIPath, c.contentConfig, c.serializers, backoff, c.Throttle, 0)
      }
      return NewRequest(c.Client, verb, c.base, c.versionedAPIPath, c.contentConfig, c.serializers, backoff, c.Throttle, c.Client.Timeout)
    }

















