import csv
import os

ORDERS_FILE = 'orders.csv'
USERS = {'clerk': 'clerkpass', 'delivery': 'deliverypass', 'manager': 'managerpass'
}

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, newline='') as f:
        return list(csv.DictReader(f))

def save_orders(orders):
    with open(ORDERS_FILE, 'w', newline='') as f:
        fieldnames = ['id', 'customer', 'address', 'description', 'date', 'amount', 'completed']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)

def login():
    print("Login")
    username = input("Username: ")
    password = input("Password: ")
    if username in USERS and USERS[username] == password:
        print(f"Logged in as {username}")
        return username
    else:
        print("Wrong username or password.")
        return None

def clerk_menu():
    orders = load_orders()
    while True:
        print("\nClerk Menu")
        print("1. Add order")
        print("2. Logout")
        choice = input("Choose: ")
        if choice == '1':
            order = {}
            order['id'] = str(len(orders) + 1)
            order['customer'] = input("Customer name: ")
            order['address'] = input("Address: ")
            order['description'] = input("Description: ")
            order['date'] = input("Date (YYYY/MM/DD): ")
            order['amount'] = input("Total amount: ")
            order['completed'] = 'no'
            orders.append(order)
            save_orders(orders)
            print("Order added!")
        elif choice == '2':
            break

def delivery_menu():
    orders = load_orders()
    while True:
        print("\nDelivery Menu")
        print("1. Mark order as completed")
        print("2. Logout")
        choice = input("Choose: ")
        if choice == '1':
            print("Pending orders:")
            for order in orders:
                if order['completed'] == 'no':
                    print(f"ID: {order['id']} Customer: {order['customer']}")
            order_id = input("Enter order ID to mark as completed: ")
            found = False
            for order in orders:
                if order['id'] == order_id and order['completed'] == 'no':
                    order['completed'] = 'yes'
                    found = True
                    print("Order marked as completed.")
            if not found:
                print("Order not found or already completed.")
            save_orders(orders)
        elif choice == '2':
            break

def manager_menu():
    orders = load_orders()
    while True:
        print("\nManager Menu")
        print("1. Orders by customer")
        print("2. Show pending orders")
        print("3. Logout")
        choice = input("Choose: ")
        if choice == '1':
            name = input("Enter customer name: ")
            count = sum(1 for order in orders if order['customer'] == name)
            print(f"{name} has placed {count} orders.")
        elif choice == '2':
            print("Pending orders:")
            for order in orders:
                if order['completed'] == 'no':
                    print(f"ID: {order['id']} Customer: {order['customer']} Description: {order['description']}")
        elif choice == '3':
            break

def main():
    while True:
        user = login()
        if user == 'clerk':
            clerk_menu()
        elif user == 'delivery':
            delivery_menu()
        elif user == 'manager':
            manager_menu()
        else:
            continue

if __name__ == "__main__":
    main()
