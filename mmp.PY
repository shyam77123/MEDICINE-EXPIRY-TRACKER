import csv
from datetime import datetime, timedelta
from colorama import Fore, init

init(autoreset=True)

MEDICINE_FILE = "medicines.csv"

# ------------------------------
# Medicine Class
# ------------------------------
class Medicine:
    def __init__(self, name, price, expiry_date, quantity):
        self.name = name
        self.price = float(price)
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
        self.quantity = int(quantity)

    def is_expired(self):
        return datetime.now() > self.expiry_date

    def days_to_expiry(self):
        return (self.expiry_date - datetime.now()).days

    def reduce_stock(self, qty):
        if self.quantity >= qty:
            self.quantity -= qty
            return True
        return False

    def get_price(self):
        if 0 <= self.days_to_expiry() <= 30:
            return self.price * 0.8  # 20% discount
        return self.price

    def get_status_color(self):
        if self.is_expired():
            return Fore.RED + "Expired"
        elif 0 <= self.days_to_expiry() <= 30:
            return Fore.YELLOW + "Expiring Soon"
        else:
            return Fore.GREEN + "Safe"

    def __str__(self):
        return f"{self.name} | Price: ₹{self.price} | Expiry: {self.expiry_date.date()} | Stock: {self.quantity} | Status: {self.get_status_color()}"

    def to_list(self):
        return [self.name, str(self.price), self.expiry_date.strftime("%Y-%m-%d"), str(self.quantity)]


# ------------------------------
# Pharmacy Class
# ------------------------------
class Pharmacy:
    def __init__(self):
        self.inventory = []
        self.load_inventory()

    # Load medicines from CSV file
    def load_inventory(self):
        try:
            with open(MEDICINE_FILE, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        med = Medicine(row[0], float(row[1]), row[2], int(row[3]))
                        self.inventory.append(med)
            self.inventory.sort(key=lambda m: m.expiry_date)
        except FileNotFoundError:
            pass  # No file yet

    # Save medicines to CSV file
    def save_inventory(self):
        with open(MEDICINE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            for med in self.inventory:
                writer.writerow(med.to_list())

    # Admin Methods
    def add_medicine(self, medicine):
        self.inventory.append(medicine)
        self.inventory.sort(key=lambda m: m.expiry_date)
        self.save_inventory()
        print(Fore.GREEN + f"✅ {medicine.name} added successfully!")

    # Customer Methods
    def sell_medicine(self, name, qty):
        for med in self.inventory:
            if med.name.lower() == name.lower():
                if med.is_expired():
                    print(Fore.RED + f"❌ Cannot sell {name}, it is expired!")
                    return
                if med.reduce_stock(qty):
                    total_price = med.get_price() * qty
                    print(Fore.GREEN + f"✅ Sold {qty} units of {name} | Bill: ₹{total_price:.2f}")
                    if 0 <= med.days_to_expiry() <= 30:
                        print(Fore.YELLOW + "⚠️ Sold with 20% discount (near expiry)!")
                    self.save_inventory()
                else:
                    print(Fore.RED + f"❌ Not enough stock for {name}")
                return
        print(Fore.RED + f"❌ Medicine {name} not found!")

    # Common Methods
    def show_inventory(self):
        print("\n📦 Current Pharmacy Inventory (FEFO order):")
        if not self.inventory:
            print("No medicines available.")
        for med in self.inventory:
            print(med)


# ------------------------------
# Main Program
# ------------------------------
def main():
    pharmacy = Pharmacy()

    print("===== WELCOME TO MEDICINE TRACKER =====")
    print("Are you an Admin or Customer?")
    print("1. Admin")
    print("2. Customer")
    role_choice = input("Enter choice (1/2): ")

    if role_choice == "1":
        role = "admin"
    elif role_choice == "2":
        role = "customer"
    else:
        print(Fore.RED + "❌ Invalid choice! Exiting...")
        return

    while True:
        if role == "admin":
            print("\n--- ADMIN MENU ---")
            print("1. Add Medicine")
            print("2. Show Inventory")
            print("3. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter medicine name: ")
                price = float(input("Enter price: "))
                expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
                quantity = int(input("Enter quantity: "))
                med = Medicine(name, price, expiry_date, quantity)
                pharmacy.add_medicine(med)
            elif choice == "2":
                pharmacy.show_inventory()
            elif choice == "3":
                print("👋 Logging out...")
                break
            else:
                print(Fore.RED + "❌ Invalid choice!")

        elif role == "customer":
            print("\n--- CUSTOMER MENU ---")
            print("1. Buy Medicine")
            print("2. Show Inventory")
            print("3. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter medicine name to buy: ")
                qty = int(input("Enter quantity: "))
                pharmacy.sell_medicine(name, qty)
            elif choice == "2":
                pharmacy.show_inventory()
            elif choice == "3":
                print("👋 Logging out...")
                break
            else:
                print(Fore.RED + "❌ Invalid choice!")


if __name__ == "__main__":
    main()
