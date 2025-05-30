from extentions import db
from datetime import date

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, default = date.today)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'order_date': self.order_date.isoformat() if self.order_date else None
        }