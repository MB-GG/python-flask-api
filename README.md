- Path: http://127.0.0.1:5000/

- http://127.0.0.1:5000/apidocs/ - API Docs.

- curl -X PUT "http://127.0.0.1:5000/item/test1" -H "Content-Type: application/json" -d '{"value": "data1"}' - Create new Element

- curl -X GET "http://127.0.0.1:5000/item/test1" - Get Element

- curl -X DELETE "http://127.0.0.1:5000/item/test1" - Delete Element
