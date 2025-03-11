#store order management 

from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import time
from collections import deque

@dataclass
class Customer:
    id: int
    name: str
    loyalty_points: int = 0

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int

@dataclass
class OrderItem:
    product_id: int
    quantity: int

@dataclass
class Order:
    id: int
    customer_id: int
    products: List[OrderItem]
    status: str
    timestamp: datetime

@dataclass
class HistoryEntry:
    order_id: int
    status: str
    timestamp: datetime

class Store:
    def __init__(self):
        self.customers: List[Customer] = []
        self.products: Dict[int, Product] = {}
        self.orders: List[Order] = []
        self.order_queue: deque = deque()
        self.priority_orders: List[int] = []
        self.order_history: List[HistoryEntry] = []
        
    def add_customer(self, name: str) -> int:
        customer_id = len(self.customers) + 1
        self.customers.append(Customer(id=customer_id, name=name))
        return customer_id
    
    def find_customer(self, customer_id: int) -> Optional[Customer]:
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None
    
    def add_product(self, name: str, price: float, initial_stock: int) -> int:
        product_id = len(self.products) + 1
        self.products[product_id] = Product(
            id=product_id, 
            name=name, 
            price=price, 
            stock=initial_stock
        )
        return product_id
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        if product_id not in self.products:
            return False
        
        self.products[product_id].stock += quantity
        return True
    
    def create_order(self, customer_id: int, products: List[OrderItem]) -> Optional[int]:
        customer = self.find_customer(customer_id)
        if not customer:
            return None
            
        for item in products:
            if (item.product_id not in self.products or 
                self.products[item.product_id].stock < item.quantity):
                return None
        
        order_id = len(self.orders) + 1
        order = Order(
            id=order_id,
            customer_id=customer_id,
            products=products,
            status='pending',
            timestamp=datetime.now()
        )
        
        self.orders.append(order)
        
        if customer.loyalty_points >= 100:
            self.priority_orders.append(order_id)
        else:
            self.order_queue.append(order_id)
        
        self.order_history.append(HistoryEntry(
            order_id=order_id,
            status='pending',
            timestamp=datetime.now()
        ))
        
        for item in products:
            self.products[item.product_id].stock -= item.quantity
        
        total_spent = sum(
            self.products[item.product_id].price * item.quantity
            for item in products
        )
        
        customer.loyalty_points += int(total_spent)
        
        return order_id
    
    def process_next_order(self) -> Optional[Order]:
        if self.priority_orders:
            order_id = self.priority_orders.pop()
            return self._process_order(order_id)
        
        if self.order_queue:
            order_id = self.order_queue.popleft()
            return self._process_order(order_id)
        
        return None
    
    def _process_order(self, order_id: int) -> Optional[Order]:
        order = next((order for order in self.orders if order.id == order_id), None)
        if not order:
            return None
        
        order.status = 'processing'
        
        self.order_history.append(HistoryEntry(
            order_id=order.id,
            status='processing',
            timestamp=datetime.now()
        ))
        
        def complete_order():
            time.sleep(2)
            order.status = 'completed'
            
            self.order_history.append(HistoryEntry(
                order_id=order.id,
                status='completed',
                timestamp=datetime.now()
            ))
        
        order.status = 'completed'
        self.order_history.append(HistoryEntry(
            order_id=order.id,
            status='completed',
            timestamp=datetime.now()
        ))
        
        return order
    
    def cancel_order(self, order_id: int) -> bool:
        order = next((order for order in self.orders if order.id == order_id), None)
        if not order:
            return False
        
        if order.status not in ['pending', 'processing']:
            return False
        
        order.status = 'cancelled'
        
        self.order_history.append(HistoryEntry(
            order_id=order_id,
            status='cancelled',
            timestamp=datetime.now()
        ))
        
        for item in order.products:
            self.update_stock(item.product_id, item.quantity)
        
        if order_id in self.order_queue:
            queue_list = list(self.order_queue)
            queue_list.remove(order_id)
            self.order_queue = deque(queue_list)
            
        if order_id in self.priority_orders:
            self.priority_orders.remove(order_id)
        
        return True
    
    def get_order_history(self, order_id: int) -> List[Dict[str, Union[str, datetime]]]:
        return [
            {"status": entry.status, "timestamp": entry.timestamp}
            for entry in self.order_history
            if entry.order_id == order_id
        ]
    
    def get_backlog_summary(self) -> Dict[str, int]:
        return {
            "regular": len(self.order_queue),
            "priority": len(self.priority_orders)
        }

def run_store_simulation():
    store = Store()
    
    customer1 = store.add_customer("Alice")
    customer2 = store.add_customer("Bob")
    
    laptop = store.add_product("Laptop", 999.99, 5)
    phone = store.add_product("Smartphone", 499.99, 10)
    headphones = store.add_product("Wireless Headphones", 129.99, 15)
    
    order1 = store.create_order(customer1, [
        OrderItem(product_id=laptop, quantity=1),
        OrderItem(product_id=headphones, quantity=1)
    ])
    
    customer = store.find_customer(customer2)
    if customer:
        customer.loyalty_points = 150
    
    order2 = store.create_order(customer2, [
        OrderItem(product_id=phone, quantity=2)
    ])
    
    print("Processing orders...")
    processed1 = store.process_next_order()
    if processed1:
        print(f"Processed order: {processed1.id}")
    
    backlog = store.get_backlog_summary()
    print(f"Orders in queue: Regular={backlog['regular']}, Priority={backlog['priority']}")
    
    processed2 = store.process_next_order()
    if processed2:
        print(f"Processed order: {processed2.id}")
    
    if order1:
        history = store.get_order_history(order1)
        print(f"Order {order1} history:", history)

if __name__ == "__main__":
    run_store_simulation()
