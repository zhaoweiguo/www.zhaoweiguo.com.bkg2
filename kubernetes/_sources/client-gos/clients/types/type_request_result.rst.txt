type request Result
###################

.. code-block:: go
   :lineno-start: 1043
   :caption: k8s.io/client-go/rest/request.go

    type Result struct {
      body        []byte
      contentType string
      err         error
      statusCode  int

      decoder runtime.Decoder
    }

.. code-block:: go
   :lineno-start: 1094
   :caption: k8s.io/client-go/rest/request.go

    func (r Result) Into(obj runtime.Object) error {
      out, _, err := r.decoder.Decode(r.body, nil, obj)
      return nil
    }













