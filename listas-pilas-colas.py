
# Simulador de un Sistema de Gestión de Restaurante
class Restaurant:
    def __init__(self):
        self.menu = []
        self.pending_orders = []
        self.completed_orders = []
        self.inventory = []
        self.tables = []

    def add_dish(self, name, price):
        self.menu.append({"name": name, "price": price})

    def add_ingredient(self, name, quantity, unit):
        self.inventory.append([name, quantity, unit])

    def take_order(self, dishes):
        self.pending_orders.append(dishes)
        print("Order taken:", dishes)

    def prepare_order(self):
        if self.pending_orders:
            order = self.pending_orders.pop(0)
            self.completed_orders.append(order)
            print("Order prepared:", order)
        else:
            print("No pending orders.")

    def serve_order(self):
        if self.completed_orders:
            order = self.completed_orders.pop()
            print("Order served:", order)
        else:
            print("No completed orders.")

    def show_menu(self):
        print("Menu:")
        for dish in self.menu:
            print(f"- {dish['name']}: ${dish['price']}")

    def show_inventory(self):
        print("Inventory:")
        for ingredient in self.inventory:
            print(f"- {ingredient[0]}: {ingredient[1]} {ingredient[2]}")

    def show_completed_orders(self):
        print("Completed orders:")
        for order in reversed(self.completed_orders):
            print("-", order)

    def initialize_tables(self, num_tables):
        for _ in range(num_tables):
            self.tables.append(["free", 0])

    def assign_table(self, table_number, num_customers):
        if 0 <= table_number < len(self.tables):
            if self.tables[table_number][0] == "free":
                self.tables[table_number] = ["occupied", num_customers]
                print(f"Table {table_number + 1} assigned to {num_customers} customers.")
            else:
                print(f"Table {table_number + 1} is not available.")
        else:
            print("Invalid table number.")

    def show_table_status(self):
        print("Table status:")
        for i, table in enumerate(self.tables):
            print(f"- Table {i + 1}: {table[0]}, Customers: {table[1]}")

restaurant = Restaurant()
restaurant.add_dish("Burger", 10)
restaurant.add_dish("Pizza", 12)
restaurant.add_ingredient("Bread", 100, "units")
restaurant.add_ingredient("Meat", 50, "kg")
restaurant.take_order(["Burger", "Soda"])
restaurant.prepare_order()
restaurant.serve_order()
restaurant.show_menu()
restaurant.show_inventory()
restaurant.show_completed_orders()
restaurant.initialize_tables(5)
restaurant.assign_table(0, 4)
restaurant.show_table_status()
