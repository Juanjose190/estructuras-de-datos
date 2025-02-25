
//Caso de Estudio: Simulación de una Cola de Atención al Cliente

class Queue {
    private items: string[] = [];

    enqueue(item: string): void {
        this.items.push(item);
        console.log(`${item} added to the queue.`);
    }

    dequeue(): void {
        if (this.isEmpty()) {
            console.log("Queue is empty.");
        } else {
            const served = this.items.shift();
            console.log(`${served} served.`);
        }
    }

    viewQueue(): void {
        if (this.isEmpty()) {
            console.log("Queue is empty.");
        } else {
            console.log("\nCurrent queue:");
            this.items.forEach((item, index) => {
                console.log(`${index + 1}. ${item}`);
            });
        }
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }
}

const queue = new Queue();

while (true) {
    console.log("\n1. Add customer\n2. Serve customer\n3. View queue\n4. Exit");
    const choice = prompt("Choose: ");

    if (choice === "1") {
        const customer = prompt("Enter customer name: ");
        if (customer) {
            queue.enqueue(customer);
        }
    } 
    else if (choice === "2") {
        queue.dequeue();
    } 
    else if (choice === "3") {
        queue.viewQueue();
    } 
    else if (choice === "4") {
        console.log("Exiting...");
        break;
    } 
    else {
        console.log("Invalid option.");
    }
}
