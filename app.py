from datetime import datetime
from flask import Flask, jsonify, request
from extentions import db
from model import Customer, Order

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://upu4ozux3dkb0kkpwusa:pWHFUECWXXcfGEo0poKdFWaiEI0cvv@b7zabufywrnnt4i8piy9-postgresql.services.clever-cloud.com:50013/b7zabufywrnnt4i8piy9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/customers')
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])

@app.route('/orders')
def get_orders():
    orders  = Order.query.all()
    return jsonify([c.to_dict() for c in orders])

# orders for one customer
@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_order_customer(customer_id):
    client_order = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify([c.to_dict() for c in client_order])


# add new order for customer
@app.route('/customers/<int:customer_id>/orders', methods=['POST'])
def post_order(customer_id):
   data = request.get_json()

   customer = Customer.query.get(customer_id)
   if not customer:
       return jsonify({'error: Customer not found'}), 404

   new_order = Order(
       customer_id = customer_id,
       product_name = data.get('product_name'),
       quantity = data.get('quantity')
   )
   try:
       db.session.add(new_order)
       db.session.commit()
       return jsonify(new_order.to_dict()), 201
   except Exception as e:
       db.session.rollback()
       return jsonify({'error': str(e)}), 500

#uprava polozky
@app.route('/orders/<int:id>', methods =['PUT'])
def put_order(id):
    data = request.get_json()

    item = Order.query.get(id)
    if not item:
        return jsonify({'error': f'item with {id} not found'}), 404

    item.customer_id = data.get('customer_id', item.customer_id)
    item.product_name = data.get('product_name', item.product_name)
    item.quantity = data.get('quantity', item.quantity)

    order_date_string = data.get('order_date')
    if order_date_string:
        try:
            item.order_date = datetime.strptime(order_date_string, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use correct YYYY-MM-DD'}), 400

    try:
        db.session.commit()
        return jsonify(item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# vymazanie polozky
@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    item = Order.query.get(id)

    if not item:
        return jsonify({'error': f'Order with id {id} not found'}), 404

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': f'Order with id {id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)