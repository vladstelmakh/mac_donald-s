# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

with open('BD/base.json', 'r', encoding='utf-8') as file:
    products_data = json.load(file)

@app.route('/all_products/', methods=['GET'])
def get_all_products():
    """
        Get information about all products.

        Returns:
            JSON: JSON response containing information about all products.
        """
    return jsonify(products_data)

@app.route('/products/<product_name>', methods=['GET'])
def get_product(product_name):
    """
        Get information about a specific product by its name.

        Args:
            product_name (str): The name of the product.

        Returns:
            JSON: JSON response containing information about the product.
                  If the product is not found, suggests closest matches.
        """
    for product in products_data:
        if product['name'] == product_name:
            return jsonify(product)
    closest_matches = get_close_matches(product_name, [product['name'] for product in products_data])
    if closest_matches:
        return jsonify({'error': f'Product not found. Did you mean {closest_matches[0]}?'}), 404
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<product_name>/<product_field>', methods=['GET'])
def get_product_field(product_name, product_field):
    """
        Get a specific field of a specific product.

        Args:
            product_name (str): The name of the product.
            product_field (str): The field of the product to retrieve.

        Returns:
            JSON: JSON response containing the specified field of the product.
                  If the product or field is not found, returns an error message.
        """
    for product in products_data:
        if product['name'] == product_name:
            if product_field in product:
                return jsonify({product_field: product[product_field]})
            else:
                return jsonify({'error': 'Field not found for this product'}), 404
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
