
//Simulador de un Sistema de Gestión de Restaurante
interface Dish {
    name: string;
    price: number;
}

interface Ingredient {
    name: string;
    quantity: number;
    unit: string;
}

interface Table {
    status: 'free' | 'occupied';
    customers: number;
}

class Restaurant {
    private menu: Dish[] = [];
    private pendingOrders: string[][] = [];
    private completedOrders: string[][] = [];
    private inventory: Ingredient[] = [];
    private tables: Table[] = [];

    public addDish(name: string, price: number): void {
        this.menu.push({ name, price });
    }

    public addIngredient(name: string, quantity: number, unit: string): void {
        this.inventory.push({ name, quantity, unit });
    }

    public takeOrder(dishes: string[]): void {
        this.pendingOrders.push(dishes);
        console.log("Order taken:", dishes);
    }

    public prepareOrder(): void {
        if (this.pendingOrders.length > 0) {
            const order = this.pendingOrders.shift();
            if (order) {
                this.completedOrders.push(order);
                console.log("Order prepared:", order);
            }
        } else {
            console.log("No pending orders.");
        }
    }

    public serveOrder(): void {
        if (this.completedOrders.length > 0) {
            const order = this.completedOrders.pop();
            console.log("Order served:", order);
        } else {
            console.log("No completed orders.");
        }
    }

    public showMenu(): void {
        console.log("Menu:");
        this.menu.forEach(dish => {
            console.log(`- ${dish.name}: $${dish.price}`);
        });
    }

    public showInventory(): void {
        console.log("Inventory:");
        this.inventory.forEach(ingredient => {
            console.log(`- ${ingredient.name}: ${ingredient.quantity} ${ingredient.unit}`);
        });
    }

    public showCompletedOrders(): void {
        console.log("Completed orders:");
        [...this.completedOrders].reverse().forEach(order => {
            console.log("-", order);
        });
    }

    public initializeTables(numTables: number): void {
        this.tables = Array(numTables).fill(null).map(() => ({
            status: 'free',
            customers: 0
        }));
    }

    public assignTable(tableNumber: number, numCustomers: number): void {
        if (tableNumber >= 0 && tableNumber < this.tables.length) {
            if (this.tables[tableNumber].status === 'free') {
                this.tables[tableNumber] = {
                    status: 'occupied',
                    customers: numCustomers
                };
                console.log(`Table ${tableNumber + 1} assigned to ${numCustomers} customers.`);
            } else {
                console.log(`Table ${tableNumber + 1} is not available.`);
            }
        } else {
            console.log("Invalid table number.");
        }
    }

    public showTableStatus(): void {
        console.log("Table status:");
        this.tables.forEach((table, index) => {
            console.log(`- Table ${index + 1}: ${table.status}, Customers: ${table.customers}`);
        });
    }
}

const restaurant = new Restaurant();
restaurant.addDish("Burger", 10);
restaurant.addDish("Pizza", 12);
restaurant.addIngredient("Bread", 100, "units");
restaurant.addIngredient("Meat", 50, "kg");
restaurant.takeOrder(["Burger", "Soda"]);
restaurant.prepareOrder();
restaurant.serveOrder();
restaurant.showMenu();
restaurant.showInventory();
restaurant.showCompletedOrders();
restaurant.initializeTables(5);
restaurant.assignTable(0, 4);
restaurant.showTableStatus();
