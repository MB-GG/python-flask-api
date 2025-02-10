from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
import requests
import pytest

app = Flask(__name__)
app.config['SWAGGER'] = {
		'title': 'API Жокументация',
		'uiversion': 3
}
swagger = Swagger(app)
api = Api(app)

DATABASE = []

class Item(Resource):
	def get(self, item_id):
		"""
		Получить элемент по ID
		---
		parameters:
			- name: item_id
				in: path
				type: string
				required: true
		responses:
			200:
				description: Успешный запрос
			404:
				description: Хуевый запрос
		"""
		if item_id in DATABASE:
			return jsonify({"item_id": item_id, "value": DATABASE[item_id]})
		return {"message": "Item not found"}, 404

	def put(self, item_id):
		"""
		Создать или обновить элемент
		---
		parameters:
			- name: item_id
				in: path
				type: string
				required: true
				schema:
					type: object
					properties:
						value:
							type: string
		responses:
			200:
				description: Элемент обновлен
		"""
		data = request.get_json()
		DATABASE[item_id] = data.get("value", "")
		return jsonify({"message": "Item saved", "item_id": item_id, "value": DATABASE[item_id]})
	
	def delete(self, item_id):
		"""
		Удалить элемент
		---
		parameters:
			- name: item_id
				in: path
				type: string
				required: true
			responses:
				200:
					description: Элемент удален
		"""
		if item_id in DATABASE:
			del DATABASE[item_id]
			return {"message": "Item deleted"}
		return {"message": "Item not found"}, 404

# Tests	
@pytest.fixture
def base_url():
	return "http://127.0.0.1:5000/item/"

def test_create_item(base_url):
	response = request.put(base_url + "test1", json={"value": "data1"})
	assert response.status_code == 200
	assert response.json()["value"] == "data1"

def tets_get_item(base_url):
	response = request.get(base_url + "test1")
	assert response.status_code == 200
	assert response.json() ["item_id"] == "test1"

def test_delete_item(base_url):
	response = request.delete(base_url + "test1")
	assert response.status_code == 200
	assert response.json() ["message"] == "Item deleted"

def test_get_noneexistent_item(base_url):
	response = request.get(base_url + "test2")
	assert response.status_code == 404
	assert response.json()["message"] == "Item not found"

if __name__ == "__main__":
	app.run(debug=True)