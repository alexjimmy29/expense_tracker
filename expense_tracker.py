import sqlite3
from datetime import date

DB_NAME="expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn=get_connection()
    conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL
                )
        """)
    conn.commit()
    conn.close

def add_expenses():
    print("\n---Add Expenses---")
    category=input("Catergory (e.g. Food, Travel, Rent): ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return

    description=input("Description (optional): ").strip()
    try:
        amount= float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount<=0:
        print("Amount must be greater than zero.")
        return

    today=date.today().isoformat()

    conn=get_connection()
    conn.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES(?,?,?,?)",
        (today,category,description, amount),
    )

    conn.commit()
    conn.close()
    print(f"Added: {category} - Rs. {amount:.2f} on {today}")

def view_expenses():
    conn=get_connection()
    rows=conn.execute(
        "SELECT id, date, category, description, amount "
        "FROM  expenses ORDER BY date DESC, id DESC"
    ).fetchall()
    conn.close()

    if not rows:
        print("\nNo recorded expenses yet.")
        return

    print("\n---All Expenses---")
    print(f"{'ID':<4} {'Date':<12} {'Category':<12} {'Description':<20} {'Amount':>10}")
    print("-" * 62)

    for row in rows:
        expenses_id, expenses_date, category, description, amount = row
        description=(description or "")[:20]
        print(f"{expenses_id:<4} {expenses_date:<12} {category:<12} {description:<20} {amount:>10.2f}")

    print("-" *62)
    total= sum(row[4] for row in rows)
    print(f" {'Total':<51} {total:>10.2f}")

def category_totals():
    conn=get_connection()
    rows=conn.execute(
        "SELECT category, COUNT(*) AS num_expenses, SUM(amount) As total "
        "FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()
    conn.close()

    if not rows:
        print("\nNo expenses recorded yet")
        return

    grand_total=sum(row[2] for row in rows)

    print("\n---Spending by Category---")
    print(f"{'Category':<15} {'Count':>6} {'Total':>12} {'Share':>8}")
    print("-"* 44)

    for category, count , total in rows:
        share= total/grand_total*100
        print(f"{category:<15} {count:>6} {total:>12.2f} {share:>7.1f}%")

    print("-" *44)
    total_count=sum(row[1] for row in rows)
    print(f"{'Total':<15} {total_count:>6} {grand_total:>12.2f}")

def show_menu():
    print("\n==== Expense Tracker =====")
    print("1. Add expenses")
    print("2. View all expenses")
    print("3. Spending by category")
    print("4. Exit")

def main():
    create_table()

    while True:
        show_menu()
        choice=input("Choose an option (1-4): ").strip()

        if choice=="1":
            add_expenses()
        elif choice=="2":
            view_expenses()
        elif choice=="3":
            category_totals()
        elif choice=="4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1,2,3 or 4")

if __name__== "__main__":
    main()