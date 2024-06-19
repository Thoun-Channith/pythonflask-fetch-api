from datetime import date
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def get_all():
    res = requests.get('https://fakestoreapi.com/products')
    res_json = res.json()
    return render_template('components/card.html', product_list=res_json)


@app.route('/products_detail')
def get_product_detail():
    pid = request.args.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{pid}")
    res_json = res.json()
    return render_template('layout/detail.html', product_detail=res_json)


@app.route('/checkout')
def checkout():
    pid = request.args.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{pid}")
    res_json = res.json()
    return render_template('layout/confirm_booking.html', product_detail=res_json)


@app.post('/confirm_checkout')
def confirm_checkout():
    pid = request.form.get('id')
    res = requests.get(f"https://fakestoreapi.com/products/{pid}")
    product = res.json()

    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    quantity = request.form.get('quantity')

    if quantity is None or quantity == '':
        quantity = 1
    else:
        quantity = int(quantity)

    total_price = product['price'] * quantity

    msg = (
        "<code> =========[ New Order ]========= </code>\n"
        "<code> - Name: {name}</code>\n"
        "<code> - Phone: {phone}</code>\n"
        "<code> - Email: {email}</code>\n"
        "<code> - Address: {address}</code>\n"
        "<code> - Date: {date}</code>\n"
        "<code> =========[ Order Detail ]========= </code>\n"
        "<b>🔔 Order Detail 🔔</b>\n"
        "<code>1. {product_name} {quantity}x{price} = ${total_price}</code>\n"
    ).format(
        name=name,
        phone=phone,
        email=email,
        address=address,
        date=date.today(),
        product_name=product['title'],
        quantity=quantity,
        price=product['price'],
        total_price=total_price
    )

    send_notification(msg)

    return redirect('/')


def send_notification(msg):
    bot_token = '6860228565:AAEim7Sci1srx5ws3HL-W6G5WWN7doV9A-c'
    chat_id = '@tg_bot_send_msg'

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={requests.utils.quote(msg)}&parse_mode=HTML"
    res = requests.get(url)
    return res


if __name__ == '__main__':
    app.run()
