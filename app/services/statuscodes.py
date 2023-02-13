#The request has succeeded. The information returned with the response
OK=200
#The request has been fulfilled and resulted in a new resource being  created
CREATED=201
#
NON_AUTH_INFO=203
#The server has fulfilled the request but does not need to return an entity-body, and might want to return updated meta information
NO_CONTENT=204
#The request requires user authentication. The response MUST include a  WWW-Authenticate header field 
UN_AUTH=401
#
NOT_FOUND=404
#The method specified in the Request-Line is not allowed for the  resource identified by the Request-URI
METH_NOT_ALLOW=405
#The request could not be completed due to a conflict with the current state of the resource.
CONFLICT=409
#The pre condition given in the request evaluated to false by the server.
CONDITION_FAIL=412
#unprocessable entity 
VALD_FAIL=422
#Bad Gateway when problem with different server ex data base server
BAD_GATEWAY=502