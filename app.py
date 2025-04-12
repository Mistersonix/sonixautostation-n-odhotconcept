from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Simpan produk di memori (untuk demo, bukan database)
products = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    price = request.form['price']
    image = request.files['image']
    filename = None

    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    product = {
        'id': str(uuid.uuid4()),
        'name': name,
        'price': price,
        'image': filename,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    products.append(product)
    return redirect(url_for('products_page'))

@app.route('/products')
def products_page():
    return render_template('products.html', products=products)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_product(id):
    product = next((p for p in products if p['id'] == id), None)
    if not product:
        return "Produk tidak ditemukan", 404

    if request.method == 'POST':
        product['name'] = request.form['name']
        product['price'] = request.form['price']
        image = request.files['image']
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product['image'] = filename
        return redirect(url_for('products_page'))

    return render_template('edit.html', product=product)

@app.route('/delete/<id>')
def delete_product(id):
    global products
    products = [p for p in products if p['id'] != id]
    return redirect(url_for('products_page'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
