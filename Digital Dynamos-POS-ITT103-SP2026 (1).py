from datetime import datetime
TAX_RATE = 0.10
DISCOUNT_THRESHOLD = 5000.00
DISCOUNT_RATE = 0.05
LOW_STOCK_LEVEL = 5
STORE_NAME = "Best Buy Retail Store"

# Product catalog with price and stock levels
catalog = {
    "rice": {"price": 250.00, "stock": 20},
    "flour": {"price": 180.00, "stock": 15},
    "bag juice": {"price": 60.00, "stock": 18},
    "cooking oil": {"price": 750.00, "stock": 10},
    "milk": {"price": 220.00, "stock": 12},
    "bread": {"price": 200.00, "stock": 14},
    "eggs": {"price": 420.00, "stock": 9},
    "soap": {"price": 130.00, "stock": 8},
    "bulla": {"price": 295.00, "stock": 30},
    "syrup": {"price": 175.00, "stock": 16},
}

# Utility function to print a line separator
def line(width=70, char="-"):
    print(char * width)

# Utility function to pause program until user presses Enter
def pause():
    input("\nPress Enter to continue...")

# Ensures user enters a valid menu choice
def get_menu_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice in {"1", "2", "3", "4", "5", "6", "7"}:
            return choice
        print("Invalid choice. Please enter a number from 1 to 7.")

# Main program loop
def main():
    print(f"Welcome to {STORE_NAME} POS System")

    while True:
        cart = {} # Shopping cart for current transaction

        while True:
            # Display main menu
            print("\nMain Menu")
            line(40)
            print("1. Display Products")
            print("2. Add Item to Cart")
            print("3. Remove Item from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Show Low Stock Alerts")
            print("7. Exit")
            line(40)

            choice = get_menu_choice()

            # Handles menu options
            if choice == "1":
                show_products()
                pause()
            elif choice == "2":
                add_to_cart(cart)
                pause()
            elif choice == "3":
                remove_from_cart(cart)
                pause()
            elif choice == "4":
                view_cart(cart)
                pause()
            elif choice == "5":
                transaction_done = checkout(cart)
                if transaction_done:
                    another = input("\nStart a new transaction? (y/n): ")
                    while another not in {"y", "n"}:
                        another = input("Please enter 'y' for yes or 'n' for no: ")
                    if another == "y":
                        break # Start new transaction
                    print("Goodbye Customer.")
                    return
                pause()
            elif choice == "6":
                show_low_stock_items()
                pause()
            elif choice == "7":
                print("Goodbye Customer.")
                return

# Ensures user enters a valid positive integer
def get_positive_integer(prompt):
    while True:
        value = input(prompt)
        try:
            number = int(value)
            if number <= 0:
                print("Please enter a whole number greater than 0.")
            else:
                return number
        except ValueError:
            print("Invalid input. Please enter a whole number.")

# Ensures payments are enough to cover total due
def get_payment_amount(total_due):
    while True:
        value = input("Enter amount received from customer: $ ")
        try:
            amount = float(value)
            if amount < total_due:
                print("Payment is not enough. Please enter an amount that covers the total due.")
            else:
                return amount
        except ValueError:
            print("Invalid input. Please enter a valid numeric amount.")

# Displays all products with stock status
def show_products():
    line()
    print(f"{STORE_NAME:^70}")
    print(f"{'AVAILABLE PRODUCTS':^70}")
    line()
    print(f"{'Product':<20}{'Price ($)':>15}{'Stock':>12}{'Status':>20}")
    line()
    for name, details in catalog.items():
        status = "LOW STOCK" if details["stock"] < LOW_STOCK_LEVEL else "OK"
        print(f"{name.title():<20}{details['price']:>15.2f}{details['stock']:>12}{status:>20}")
    line()

# Finds product in the catalog by name
def find_product(name):
    return catalog.get(name.strip().lower())

# Adds product to cart
def add_to_cart(cart):
    show_products()
    product_name = input("Enter product name to add: ").strip().lower()
    product = find_product(product_name)

    if product is None:
        print("Product not found in catalog.")
        return

    quantity = get_positive_integer("Enter quantity: ")

    if quantity > product["stock"]:
        print("Insufficient stock. Please enter a smaller quantity.")
        return

    if product_name in cart:
        cart[product_name]["quantity"] += quantity
    else:
        cart[product_name] = {
            "price": product["price"],
            "quantity": quantity
        }

    product["stock"] -= quantity
    print(f"{quantity} x {product_name.title()} added to cart.")

    if product["stock"] < LOW_STOCK_LEVEL:
        print(f"Alert: {product_name.title()} is now low in stock ({product['stock']} left).")

# Removes product from cart
def remove_from_cart(cart):
    if not cart:
        print("The cart is empty. Nothing to remove.")
        return

    view_cart(cart)
    product_name = input("Enter product name to remove: ").strip().lower()

    if product_name not in cart:
        print("That item is not currently in the cart.")
        return

    quantity = get_positive_integer("Enter quantity to remove: ")
    cart_quantity = cart[product_name]["quantity"]

    if quantity > cart_quantity:
        print("You cannot remove more than the quantity in the cart.")
        return

    cart[product_name]["quantity"] -= quantity
    catalog[product_name]["stock"] += quantity

    if cart[product_name]["quantity"] == 0:
        del cart[product_name]

    print(f"{quantity} x {product_name.title()} removed from cart.")

# Calculates subtotal, discount, tax, and total
def calculate_totals(cart):
    subtotal = sum(item["price"] * item["quantity"] for item in cart.values())
    discount = subtotal * DISCOUNT_RATE if subtotal > DISCOUNT_THRESHOLD else 0.0
    taxable_amount = subtotal - discount
    tax = taxable_amount * TAX_RATE
    total = taxable_amount + tax
    return subtotal, discount, tax, total

# Display cart contents and totals
def view_cart(cart):
    if not cart:
        print("The cart is empty.")
        return

    subtotal, discount, tax, total = calculate_totals(cart)

    line()
    print(f"{'CURRENT SHOPPING CART':70}")
    line()
    print(f"{'Item':<20}{'Qty':>8}{'Unit Price':>15}{'Total Price':>18}")
    line()

    for name, item in cart.items():
        item_total = item["price"] * item["quantity"]
        print(f"{name.title():<20}{item['quantity']:>8}{item['price']:>15.2f}{item_total:>18.2f}")

    line()
    print(f"{'Subtotal:':<52}${subtotal:>10.2f}")
    print(f"{'Discount:':<52}-${discount:>10.2f}")
    print(f"{'Tax (10%):':<52}${tax:>10.2f}")
    print(f"{'Total Due:':<52}${total:>10.2f}")
    line()

# Print receipt after checkout
def print_receipt(cart, amount_paid, change):
    subtotal, discount, tax, total = calculate_totals(cart)
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    print("\n")
    line(char="=")
    print(f"{STORE_NAME:^70}")
    print(f"{'POINT OF SALE RECEIPT':^70}")
    print(f"{now:^70}")
    line(char="=")
    print(f"{'Item':<20}{'Qty':>8}{'Unit Price':>15}{'Total Price':>18}")
    line()

    for name, item in cart.items():
        item_total = item["price"] * item["quantity"]
        print(f"{name.title():<20}{item['quantity']:>8}{item['price']:>15.2f}{item_total:>18.2f}")

    line()
    print(f"{'Subtotal:':<52}${subtotal:>10.2f}")
    print(f"{'Discount:':<52}-${discount:>10.2f}")
    print(f"{'Tax (10%):':<52}${tax:>10.2f}")
    print(f"{'Total Due:':<52}${total:>10.2f}")
    print(f"{'Amount Paid:':<52}${amount_paid:>10.2f}")
    print(f"{'Change:':<52}${change:>10.2f}")
    line(char="=")
    print(f"{'Thank you for shopping with us':70}")
    line(char="=")


def checkout(cart):
    if not cart:
        print("The cart is empty. Add items before checkout.")
        return False

    view_cart(cart)
    _, _, _, total = calculate_totals(cart)
    amount_paid = get_payment_amount(total)
    change = amount_paid - total
    print_receipt(cart, amount_paid, change)
    cart.clear()
    return True

# Displays alert when stock is low
def show_low_stock_items():
    low_items = [(name, details) for name, details in catalog.items() if details["stock"] < LOW_STOCK_LEVEL]

    if not low_items:
        print("no products are currently below the low stock level.")
        return

    line()
    print(f"{'LOW STOCK ALERTS':^70}")
    line()
    print(f"{'Product':<25}{'Remaining Stock':>20}")
    line()
    for name, details in low_items:
        print(f"{name.title():<25}{details['stock']:>20}")
    line()



if __name__ == "__main__":
    main()