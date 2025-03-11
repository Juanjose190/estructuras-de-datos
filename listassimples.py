class TaskNode:
    def __init__(self, title, description, priority, due_date, category, status="Pending"):
      
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.status = status

        
        self.next = None

class TaskList:
    def __init__(self):
        self.head = None
        self.count = 0
    
    def add_task(self, title, description, priority, due_date, category):
        new_task = TaskNode(title, description, priority, due_date, category)
        
        if self.head is None:
            self.head = new_task
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_task
        
        self.count = self.count + 1
        return new_task
    
    def remove_task(self, title):
        if self.head is None:
            return False
        
        if self.head.title == title:
            self.head = self.head.next
            self.count = self.count - 1
            return True
        
        current = self.head
        while current.next is not None and current.next.title != title:
            current = current.next
            
        if current.next is not None:
            current.next = current.next.next
            self.count = self.count - 1
            return True
        
        return False
    
    def update_task_status(self, title, new_status):
        current = self.head
        while current is not None and current.title != title:
            current = current.next
            
        if current is not None:
            current.status = new_status
            return True
        
        return False
    
    def print_tasks(self):
        if self.head is None:
            print("No tasks in the list")
            return
            
        current = self.head
        task_number = 1
        
        while current is not None:
            print(f"Task {task_number}:")
            print(f"Title: {current.title}")
            print(f"Description: {current.description}")
            print(f"Priority: {current.priority}")
            print(f"Due Date: {current.due_date}")
            print(f"Category: {current.category}")
            print(f"Status: {current.status}")
            print("-" * 30)
            
            current = current.next
            task_number = task_number + 1
    
    def find_task(self, title):
        current = self.head
        while current is not None:
            if current.title == title:
                return current
            current = current.next
        return None

if __name__ == "__main__":
    todo_list = TaskList()
    
    todo_list.add_task("Complete report", "Finish quarterly sales report", "High", "2025-03-20", "Work")
    todo_list.add_task("Buy groceries", "Milk, eggs, bread, vegetables", "Medium", "2025-03-15", "Personal")
    todo_list.add_task("Fix website bug", "Repair login functionality", "High", "2025-03-12", "Work")
    
    print("Initial task list:")
    todo_list.print_tasks()
    
    todo_list.update_task_status("Buy groceries", "Completed")
    todo_list.remove_task("Complete report")
    
    print("\nAfter updates:")
    todo_list.print_tasks()
    
    print("\nTraversing and checking each task manually:")
    node = todo_list.head
    task_number = 1
    
    while node is not None:
        print(f"Task {task_number}: {node.title} - {node.status}")
        node = node.next
        task_number = task_number + 1
