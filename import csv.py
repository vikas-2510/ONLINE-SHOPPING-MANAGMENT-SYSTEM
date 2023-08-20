import csv


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


class OnlineShop:
    def __init__(self):
        self.products = []
        self.load_products()

    def load_products(self):
        with open('products.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0]
                price = float(row[1])
                quantity = int(row[2])
                product = Product(name, price, quantity)
                self.products.append(product)

    def display_products(self):
        print("Available products:")
        for index, product in enumerate(self.products, start=1):
            print(f"{index}. {product.name} - ${product.price} - Quantity: {product.quantity}")

    def search_product(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None

    def buy_product(self, name, quantity):
        product = self.search_product(name)
        if product is None:
            print(f"Product '{name}' not found.")
        elif product.quantity < quantity:
            print(f"Insufficient quantity of '{name}'. Available: {product.quantity}")
        else:
            product.quantity -= quantity
            self.save_products()
            print(f"Purchased {quantity} {name}(s) successfully.")

    def save_products(self):
        with open('products.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for product in self.products:
                writer.writerow([product.name, product.price, product.quantity])


def main():
    shop = OnlineShop()

    while True:
        print("\n===== Online Shopping System =====")
        print("1. Display available products")
        print("2. Search product")
        print("3. Buy product")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            shop.display_products()
        elif choice == '2':
            name = input("Enter the name of the product: ")
            product = shop.search_product(name)
            if product is None:
                print(f"Product '{name}' not found.")
            else:
                print(f"Product '{product.name}' - Price: ${product.price} - Quantity: {product.quantity}")
        elif choice == '3':
            name = input("Enter the name of the product to buy: ")
            quantity = int(input("Enter the quantity: "))
            shop.buy_product(name, quantity)
        elif choice == '4':
            print("Thank you for using the Online Shopping System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
