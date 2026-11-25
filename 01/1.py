class BrowserHistory:
    def __init__(self, size):
        self.stack = []
        self.max_size = size

    # Push operation
    def push(self, page):
        if len(self.stack) == self.max_size:
            print("\nStack Overflow! Cannot visit more pages.")
        else:
            self.stack.append(page)
            print(f"\nVisited: {page}")

    # Pop operation
    def pop(self):
        if len(self.stack) == 0:
            print("\nStack Underflow! No page to go back.")
        else:
            page = self.stack.pop()
            print(f"\nRemoved: {page}")

    # Peek operation
    def peek(self):
        if len(self.stack) == 0:
            print("\nStack is empty. No current page.")
        else:
            print(f"\nCurrent Page: {self.stack[-1]}")

    # Display operation
    def display(self):
        if len(self.stack) == 0:
            print("\nBrowser history is empty.")
        else:
            print("\nBrowser History:")
            for page in reversed(self.stack):
                print(page)


# Main program
def main():
    print("======================================")
    print("   AI-Based Web Browser History")
    print("        Stack Implementation")
    print("======================================")

    size = int(input("\nEnter maximum stack size: "))

    browser = BrowserHistory(size)

    while True:
        print("\n----------- MENU -----------")
        print("1. Visit a Page (Push)")
        print("2. Go Back (Pop)")
        print("3. Current Page (Peek)")
        print("4. Display History")
        print("5. Exit")
        print("----------------------------")

        choice = input("Enter your choice: ")

        if choice == "1":
            page = input("Enter webpage name: ")
            browser.push(page)

        elif choice == "2":
            browser.pop()

        elif choice == "3":
            browser.peek()

        elif choice == "4":
            browser.display()

        elif choice == "5":
            print("\nExiting Browser History Manager...")
            break

        else:
            print("\nInvalid choice! Please enter 1-5.")


# Run the program
if __name__ == "__main__":
    main()