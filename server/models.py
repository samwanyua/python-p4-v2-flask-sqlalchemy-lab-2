from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Relationship with Review model
    reviews = db.relationship("Review", back_populates="customer")
    
    # Association proxy to get items through reviews relationship
    items = association_proxy("reviews", "item")
    
    serialize_rules = ('-reviews.customer',)  

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship with Review model
    reviews = relationship("Review", back_populates="item")
    
    # Relationship with Customer model through Review
    customers = relationship("Customer", secondary="reviews", back_populates="items")
    
    serialize_rules = ('-reviews.item',)  

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    
    # Foreign keys to establish relationships
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationship with Customer model
    customer = relationship("Customer", back_populates="reviews")
    
    # Relationship with Item model
    item = relationship("Item", back_populates="reviews")
    
    serialize_rules = ('-customer.reviews', '-item.reviews')
