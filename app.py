from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = "icecream_secret_2024"

# Product catalog
PRODUCTS = [
    {"id": 1, "name": "Mango Sorbet", "price": 120, "emoji": "🥭", "tag": "Bestseller", "desc": "Sun-kissed Alphonso mangoes, churned into silk"},
    {"id": 2, "name": "Dark Choco Fudge", "price": 140, "emoji": "🍫", "tag": "Rich", "desc": "72% Belgian cocoa, velvety and intense"},
    {"id": 3, "name": "Strawberry Dream", "price": 110, "emoji": "🍓", "tag": "Fresh", "desc": "Handpicked strawberries, cream and a kiss of vanilla"},
    {"id": 4, "name": "Pista Royale", "price": 150, "emoji": "🌿", "tag": "Premium", "desc": "Iranian pistachios, rose water, saffron threads"},
    {"id": 5, "name": "Blueberry Swirl", "price": 130, "emoji": "🫐", "tag": "Tangy", "desc": "Wild blueberries, lemon zest, cream cheese swirl"},
    {"id": 6, "name": "Salted Caramel", "price": 135, "emoji": "🍯", "tag": "Classic", "desc": "Burnt sugar, fleur de sel, Madagascar vanilla"},
    {"id": 7, "name": "Tender Coconut", "price": 115, "emoji": "🥥", "tag": "Tropical", "desc": "Fresh Kerala coconut, pandan leaf, light cream"},
    {"id": 8, "name": "Rainbow Sherbet", "price": 105, "emoji": "🌈", "tag": "Fun", "desc": "Three flavours, one scoop – fruity and fizzy"},
]

def get_cart():
    return session.get("cart", {})

def cart_total():
    cart = get_cart()
    total = sum(
        next((p["price"] for p in PRODUCTS if p["id"] == int(pid)), 0) * qty
        for pid, qty in cart.items()
    )
    return total

def cart_count():
    return sum(get_cart().values())

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS, cart_count=cart_count())

@app.route("/menu")
def menu():
    return render_template("menu.html", products=PRODUCTS, cart_count=cart_count())

@app.route("/cart")
def cart():
    cart = get_cart()
    items = []
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            items.append({**product, "qty": qty, "subtotal": product["price"] * qty})
    return render_template("cart.html", items=items, total=cart_total(), cart_count=cart_count())

@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return jsonify({"success": True, "cart_count": cart_count()})

@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        session["cart"] = {}
        return render_template("success.html", cart_count=0)
    cart = get_cart()
    if not cart:
        return redirect(url_for("cart"))
    items = []
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            items.append({**product, "qty": qty, "subtotal": product["price"] * qty})
    return render_template("checkout.html", items=items, total=cart_total(), cart_count=cart_count())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

