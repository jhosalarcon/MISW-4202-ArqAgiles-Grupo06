def createNotification(sesion_id):






    order = Order.query.get(order_id)
    product = Product.query.get(order.product)
    if product.stock >= order.quantity:
        product.stock = product.stock-order.quantity
        q2.enqueue(update_product, {
            'id': product.id,
            'quantity': order.quantity
        })
        order.state = "completed"
    else:
        order.state = "failed"
    db.session.commit()