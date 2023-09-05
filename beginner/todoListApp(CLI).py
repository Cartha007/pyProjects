import json

def loadTodo():
    try:
        with open('todos.json', 'r') as todoFile:
            return json.load(todoFile)
    except FileNotFoundError:
        return {}

def save(todoList):
    with open('todos.json', 'w') as todoFile:
        json.dump(todoList, todoFile)

def viewTasks(todoList):
    for taskId, task in todoList.items():
        status = "✓" if task["completed"] else " "
        print(f"{taskId}. [{status}] {task['task']}")
    
def addTask(todoList, task: str, completed: bool = False):
    taskId = str(len(todoList) + 1)
    todoList[taskId] = {
        "task": task,
        "completed": completed
    }
    print(f'Added task: {task}')
    
def removeTask(todoList, taskId: str):
    if taskId in todoList:
        del todoList[taskId]
        print(f"Task with ID {taskId} removed.")
    else:
        print(f"No task found with ID {taskId}")
        
def markComplete(todoList, taskId: str):
    if taskId in todoList:
        todoList[taskId]["completed"] = True
        print(f"Task {taskId} has been marked as completed.")
    elif taskId in todoList and todoList[taskId]["completed"]:
        print(f"Task {taskId} is already marked as completed.")
    else:
        print(f"No task found with ID {taskId}.")
        
def unmarkComplete(todoList, taskId: str):
    if taskId in todoList:
        todoList[taskId]["completed"] = False
        print(f"Task {taskId} has been unmarked as completed.")
    elif taskId in todoList and not todoList[taskId]["completed"]:
        print(f"Task {taskId} is already marked as uncompleted.")
    else:
        print(f"No task found with ID {taskId}.")

def main():
    todoList = loadTodo()
    print("====== TODO APPLICATION ======")
    while True:
        print("\nWhat would you like to do.(Select by number)")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Mark task as completed")
        print("5. Unmark task as completed")
        print("6. Save and quit")

        choice = input(">")
        
        if choice == "1":
            viewTasks(todoList)
        elif choice == "2":
            task = input("Enter the task: ")
            addTask(todoList, task)
            print(f"Task '{task}' added.")
        elif choice == "3":
            viewTasks(todoList)
            taskId = input("Enter the ID of the task to remove: ")
            removeTask(todoList, taskId)
        elif choice == "4":
            viewTasks(todoList)
            taskId = input("Enter the ID of the task to mark as completed: ")
            markComplete(todoList, taskId)
        elif choice == "5":
            viewTasks(todoList)
            taskId = input("Enter the ID of the task to unmark as completed: ")
            unmarkComplete(todoList, taskId)
        elif choice == "6":
            save(todoList)
            print("\nTodo list saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
    
if __name__ == "__main__":
    print("Starting, please wait...")
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
    # except Exception as e:
    #     print(f'Error: {e}')