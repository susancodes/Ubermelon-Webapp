"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request

from collections import Counter

import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing melons added

    list_of_melons_in_cart = session['cart']
    melonid_qty_dict = Counter(list_of_melons_in_cart)
    melon_bought_list = []
    total_list = []

    for id, qty in melonid_qty_dict.items():
        melon = model.Melon.get_by_id(id)
        melon_price = melon.price
        total_list.append(melon_price * qty)
        melon_bought_list.append((melon, qty))
    
    total = '%.2f' % sum(total_list)
        
    # for id in list_of_melons_bought:
    #     melon = model.Melon.get_by_id(id)
    #     melon_bought_list.append(melon)

    return render_template("cart.html", melon_bought_list = melon_bought_list, total=total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list

    melon = model.Melon.get_by_id(id)
    melon_id = melon.id
    melon_name = melon.common_name

    if 'cart' not in session:
        session['cart'] = []
        session['cart'].append(melon_id)
    else:
        session['cart'].append(melon_id)
    

    flash("%s has been Successfully added to cart." % melon_name)

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login_confirm", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    username = request.form.get('email')
    password = request.form.get('password')

    if username:
        session['username'] = username

    return "Your email is %s" % (session['username'])

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
