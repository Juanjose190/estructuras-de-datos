
enum OrderStage {
  SolicitudPedido = 'Request order',
  RecepcionPedido = 'Receive order',
  ElaboracionPedido = 'Prepare order',
  SolicitudCuenta = 'Request bill',
  CalculoTotal = 'Calculate total',
  SirvePedido = 'Serve order',
  PedirCuenta = 'Ask for bill',
  Pago = 'Pay',
  Fin = 'End'
}

enum Actor {
  Cliente = 'Customer',
  Mozo = 'Waiter',
  Caja = 'Cashier',
  Cocina = 'Kitchen'
}

interface Order {
  id: string;
  currentStage: OrderStage;
  actor: Actor;
  items: string[];
  total?: number;
}

class RestaurantOrderProcess {
  private order: Order;

  constructor() {
    this.order = {
      id: this.generateOrderId(),
      currentStage: OrderStage.SolicitudPedido,
      actor: Actor.Cliente,
      items: []
    };
  }

  private generateOrderId(): string {
    return `ORDER-${Date.now()}`;
  }

  selectItems(items: string[]): void {
    this.order.items = items;
    this.order.currentStage = OrderStage.RecepcionPedido;
    this.order.actor = Actor.Mozo;
  }

  receiveOrder(): void {
    this.order.currentStage = OrderStage.ElaboracionPedido;
    this.order.actor = Actor.Cocina;
  }

  prepareOrder(): void {
    this.order.currentStage = OrderStage.SirvePedido;
    this.order.actor = Actor.Mozo;
  }

  serveOrder(): void {
    this.order.currentStage = OrderStage.SolicitudCuenta;
    this.order.actor = Actor.Cliente;
  }

  requestBill(): void {
    this.order.currentStage = OrderStage.CalculoTotal;
    this.order.actor = Actor.Caja;
  }

  calculateTotal(): void {
    this.order.total = this.order.items.length * 10;
    this.order.currentStage = OrderStage.PedirCuenta;
    this.order.actor = Actor.Cliente;
  }

  payBill(): void {
    this.order.currentStage = OrderStage.Fin;
    this.order.actor = Actor.Mozo;
  }

  getOrderStatus(): Order {
    return this.order;
  }
}

const orderProcess = new RestaurantOrderProcess();
orderProcess.selectItems(['Pizza', 'Soda']);
orderProcess.receiveOrder();
orderProcess.prepareOrder();
orderProcess.serveOrder();
orderProcess.requestBill();
orderProcess.calculateTotal();
orderProcess.payBill();

console.log(orderProcess.getOrderStatus());
