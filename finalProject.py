import json
import os

ITEMS_FILE = "items.json"

class Item:
    def __init__(self, item_id, item_name, category, location_found, status="Unclaimed"):
        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.location_found = location_found
        self.status = status

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "category": self.category,
            "location_found": self.location_found,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return Item(
            item_id=data.get("item_id", ""),
            item_name=data.get("item_name", ""),
            category=data.get("category", ""),
            location_found=data.get("location_found", ""),
            status=data.get("status", "Unclaimed"),
        )


def load_items():
    if not os.path.exists(ITEMS_FILE):
        return []

    try:
        with open(ITEMS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Item.from_dict(item) for item in data]
    except json.JSONDecodeError:
        print("Warning: items.json is corrupted. Starting with an empty dataset.")
        return []
    except Exception as error:
        print(f"Error loading items: {error}")
        return []


def save_items(items):
    try:
        with open(ITEMS_FILE, "w", encoding="utf-8") as file:
            json.dump([item.to_dict() for item in items], file, indent=2)
    except Exception as error:
        print(f"Error saving items: {error}")


def generate_item_id(items):
    if not items:
        return "1"

    existing_ids = [int(item.item_id) for item in items if item.item_id.isdigit()]
    next_id = max(existing_ids, default=0) + 1
    return str(next_id)


def prompt_non_empty(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def press_enter_to_continue():
    input("\nPress Enter to continue...")


def display_item(item):
    print(f"ID: {item.item_id}")
    print(f"Name: {item.item_name}")
    print(f"Category: {item.category}")
    print(f"Location Found: {item.location_found}")
    print(f"Status: {item.status}")
    print("-" * 40)


def display_items(items):
    if not items:
        print("No records found.")
        return

    for item in items:
        display_item(item)


def add_lost_item(items):
    print("\nAdd Lost Item")
    print("----------------")
    item_name = prompt_non_empty("Item name: ")
    category = prompt_non_empty("Category: ")
    location_found = prompt_non_empty("Location found: ")

    item_id = generate_item_id(items)
    item = Item(item_id=item_id, item_name=item_name, category=category, location_found=location_found)
    items.append(item)
    save_items(items)
    print(f"Item added successfully with ID: {item_id}")


def view_all_items(items):
    print("\nAll Lost and Found Items")
    print("-------------------------")
    display_items(items)


def search_items(items):
    print("\nSearch Items")
    print("------------")
    print("Search by:")
    print("1. Name")
    print("2. Category")
    print("3. Location Found")

    choice = input("Choose search type: ").strip()
    if choice == "1":
        term = prompt_non_empty("Enter item name to search: ").lower()
        results = [item for item in items if term in item.item_name.lower()]
    elif choice == "2":
        term = prompt_non_empty("Enter category to search: ").lower()
        results = [item for item in items if term in item.category.lower()]
    elif choice == "3":
        term = prompt_non_empty("Enter location found to search: ").lower()
        results = [item for item in items if term in item.location_found.lower()]
    else:
        print("Invalid choice.")
        return

    if results:
        print(f"\nFound {len(results)} item(s):")
        display_items(results)
    else:
        print("No matching items found.")


def mark_item_claimed(items):
    print("\nMark Item as Claimed")
    print("----------------------")
    item_id = prompt_non_empty("Enter item ID: ")
    for item in items:
        if item.item_id == item_id:
            if item.status.lower() == "claimed":
                print("This item has already been marked as claimed.")
                return
            item.status = "Claimed"
            save_items(items)
            print("Item status updated to Claimed.")
            return
    print("Item ID not found.")


def delete_item(items):
    print("\nDelete Item")
    print("-----------")
    item_id = prompt_non_empty("Enter item ID to delete: ")
    for index, item in enumerate(items):
        if item.item_id == item_id:
            confirm = input(f"Delete item '{item.item_name}' (ID: {item_id})? (y/n): ").strip().lower()
            if confirm == "y":
                items.pop(index)
                save_items(items)
                print("Item deleted successfully.")
            else:
                print("Deletion cancelled.")
            return
    print("Item ID not found.")


def sort_items_by_category(items):
    print("\nItems Sorted by Category")
    print("-------------------------")
    sorted_items = sorted(items, key=lambda item: item.category.lower())
    display_items(sorted_items)


def count_claimed_unclaimed(items):
    claimed = sum(1 for item in items if item.status.lower() == "claimed")
    unclaimed = sum(1 for item in items if item.status.lower() != "claimed")
    print("\nItem Counts")
    print("-----------")
    print(f"Total claimed items: {claimed}")
    print(f"Total unclaimed items: {unclaimed}")


def show_menu():
    print("\nLost and Found Management System")
    print("1. Add Lost Item")
    print("2. View All Items")
    print("3. Search Item")
    print("4. Mark Item as Claimed")
    print("5. Delete Item")
    print("6. Sort Items by Category")
    print("7. Count Claimed / Unclaimed Items")
    print("8. Exit")


def main():
    items = load_items()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_lost_item(items)
        elif choice == "2":
            view_all_items(items)
        elif choice == "3":
            search_items(items)
        elif choice == "4":
            mark_item_claimed(items)
        elif choice == "5":
            delete_item(items)
        elif choice == "6":
            sort_items_by_category(items)
        elif choice == "7":
            count_claimed_unclaimed(items)
        elif choice == "8":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please select a number from the menu.")

        press_enter_to_continue()


if __name__ == "__main__":
    main()