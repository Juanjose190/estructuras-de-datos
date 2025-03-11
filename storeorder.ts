//Store Order Management System

interface Customer {
  id: number;
  name: string;
  loyaltyPoints: number;
}

interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
}

interface Order {
  id: number;
  customerId: number;
  products: Array<{ productId: number; quantity: number }>;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  timestamp: Date;
}

class Store {
  private customers: Customer[] = [];
  private products: Map<number, Product> = new Map();
  private orders: Order[] = [];
  private orderQueue: number[] = [];
  private priorityOrders: number[] = [];
  private orderHistory: { orderId: number, status: string, timestamp: Date }[] = [];

  constructor() {}

  addCustomer(name: string): number {
    const id = this.customers.length + 1;
    this.customers.push({ id, name, loyaltyPoints: 0 });
    return id;
  }

  findCustomer(id: number): Customer | undefined {
    return this.customers.find(customer => customer.id === id);
  }

  addProduct(name: string, price: number, initialStock: number): number {
    const id = this.products.size + 1;
    this.products.set(id, { id, name, price, stock: initialStock });
    return id;
  }

  updateStock(productId: number, quantity: number): boolean {
    const product = this.products.get(productId);
    if (!product) return false;
    
    product.stock += quantity;
    this.products.set(productId, product);
    return true;
  }

  createOrder(customerId: number, products: Array<{ productId: number; quantity: number }>): number | null {
    const customer = this.findCustomer(customerId);
    if (!customer) return null;

    for (const item of products) {
      const product = this.products.get(item.productId);
      if (!product || product.stock < item.quantity) {
        return null;
      }
    }

    const orderId = this.orders.length + 1;
    const order: Order = {
      id: orderId,
      customerId,
      products,
      status: 'pending',
      timestamp: new Date()
    };
    
    this.orders.push(order);
    
    if (customer.loyaltyPoints >= 100) {
      this.priorityOrders.push(orderId);
    } else {
      this.orderQueue.push(orderId);
    }
    
    this.orderHistory.push({
      orderId,
      status: 'pending',
      timestamp: new Date()
    });
    
    for (const item of products) {
      const product = this.products.get(item.productId)!;
      product.stock -= item.quantity;
      this.products.set(item.productId, product);
    }
    
    const totalSpent = products.reduce((sum, item) => {
      const product = this.products.get(item.productId)!;
      return sum + (product.price * item.quantity);
    }, 0);
    
    customer.loyaltyPoints += Math.floor(totalSpent);
    
    return orderId;
  }

  processNextOrder(): Order | null {
    if (this.priorityOrders.length > 0) {
      const orderId = this.priorityOrders.pop()!;
      return this.processOrder(orderId);
    }
    
    if (this.orderQueue.length > 0) {
      const orderId = this.orderQueue.shift()!;
      return this.processOrder(orderId);
    }
    
    return null;
  }

  private processOrder(orderId: number): Order | null {
    const orderIndex = this.orders.findIndex(order => order.id === orderId);
    if (orderIndex === -1) return null;
    
    const order = this.orders[orderIndex];
    order.status = 'processing';
    
    this.orderHistory.push({
      orderId: order.id,
      status: 'processing',
      timestamp: new Date()
    });
    
    setTimeout(() => {
      order.status = 'completed';
      
      this.orderHistory.push({
        orderId: order.id,
        status: 'completed',
        timestamp: new Date()
      });
    }, 2000);
    
    return order;
  }

  cancelOrder(orderId: number): boolean {
    const orderIndex = this.orders.findIndex(order => order.id === orderId);
    if (orderIndex === -1) return false;
    
    const order = this.orders[orderIndex];
    if (order.status !== 'pending' && order.status !== 'processing') {
      return false;
    }
    
    order.status = 'cancelled';
    
    this.orderHistory.push({
      orderId,
      status: 'cancelled',
      timestamp: new Date()
    });
    
    for (const item of order.products) {
      this.updateStock(item.productId, item.quantity);
    }
    
    const queueIndex = this.orderQueue.indexOf(orderId);
    if (queueIndex !== -1) {
      this.orderQueue.splice(queueIndex, 1);
    }
    
    const priorityIndex = this.priorityOrders.indexOf(orderId);
    if (priorityIndex !== -1) {
      this.priorityOrders.splice(priorityIndex, 1);
    }
    
    return true;
  }

  getOrderHistory(orderId: number): { status: string, timestamp: Date }[] {
    return this.orderHistory
      .filter(entry => entry.orderId === orderId)
      .map(({ status, timestamp }) => ({ status, timestamp }));
  }

  getBacklogSummary(): { regular: number, priority: number } {
    return {
      regular: this.orderQueue.length,
      priority: this.priorityOrders.length
    };
  }
}

function runStoreSimulation() {
  const store = new Store();
  
  const customer1 = store.addCustomer("Alice");
  const customer2 = store.addCustomer("Bob");
  
  const laptop = store.addProduct("Laptop", 999.99, 5);
  const phone = store.addProduct("Smartphone", 499.99, 10);
  const headphones = store.addProduct("Wireless Headphones", 129.99, 15);
  
  const order1 = store.createOrder(customer1, [
    { productId: laptop, quantity: 1 },
    { productId: headphones, quantity: 1 }
  ]);
  
  store.findCustomer(customer2)!.loyaltyPoints = 150;
  const order2 = store.createOrder(customer2, [
    { productId: phone, quantity: 2 }
  ]);
  
  console.log("Processing orders...");
  const processed1 = store.processNextOrder();
  console.log(`Processed order: ${processed1?.id}`);
  
  const backlog = store.getBacklogSummary();
  console.log(`Orders in queue: Regular=${backlog.regular}, Priority=${backlog.priority}`);
  
  const processed2 = store.processNextOrder();
  console.log(`Processed order: ${processed2?.id}`);
  
  if (order1) {
    const history = store.getOrderHistory(order1);
    console.log(`Order ${order1} history:`, history);
  }
}

runStoreSimulation();
