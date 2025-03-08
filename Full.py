
import sqlite3
def create_tables():
    """
    This function creates tables in the SQLite database.
    The database name is 'DB1.db' by default.
    """
    db_name = "DB2.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS plan_details (
        plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_type TEXT NOT NULL,  
        speed TEXT NOT NULL,      
        data_usage TEXT NOT NULL,  
        monthly_charge REAL NOT NULL 
    );
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS customers_table (
        customer_id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        plan_id INTEGER NOT NULL,  
        FOREIGN KEY (plan_id) REFERENCES plan_details(plan_id)
    );
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS paymenthistory (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        plan_id INTEGER NOT NULL,   -- Foreign key to plan_details
        start_date TEXT NOT NULL,   
        end_date TEXT NOT NULL,     
        price REAL NOT NULL,        
        due_date TEXT NOT NULL,     
        paid_date TEXT,             
        FOREIGN KEY (customer_id) REFERENCES customers_table(customer_id),
        FOREIGN KEY (plan_id) REFERENCES plan_details(plan_id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully.")
    
create_tables()

def insert_data():
    with sqlite3.connect("DB2.db") as conn:
        cursor = conn.cursor()

        cursor.executemany('''INSERT INTO plan_details (plan_type, speed, data_usage, monthly_charge) VALUES (?, ?, ?, ?)''', [
            ('Standard', '50 Mbps', '100 GB', 49.99),
            ('Premium', '100 Mbps', 'Unlimited', 79.99),
            ('Basic', '20 Mbps', '50 GB', 29.99)
        ])

        cursor.executemany('''INSERT INTO customers_table (customer_id, name, address, email, phone_number, plan_id) VALUES (?, ?, ?, ?, ?, ?)''', [
            (1, 'Alice Johnson', '123 Main St, Springfield', 'alice.johnson@example.com', '123-456-7890', 1),
            (2, 'Bob Smith', '456 Oak St, Springfield', 'bob.smith@example.com', '234-567-8901', 2),
            (3, 'Charlie Brown', '789 Pine St, Springfield', 'charlie.brown@example.com', '345-678-9012', 3),
            (4, 'David Lee', '101 Maple St, Springfield', 'david.lee@example.com', '456-789-0123', 1),
            (5, 'Eva White', '202 Birch St, Springfield', 'eva.white@example.com', '567-890-1234', 2),
        ])

        cursor.executemany('''INSERT INTO paymenthistory (customer_id, plan_id, start_date, end_date, price, due_date, paid_date) VALUES (?, ?, ?, ?, ?, ?, ?)''', [
            (1, 1, '2024-11-01', '2024-11-30', 49.99, '2024-11-30', '2024-11-29'),
            (1, 2, '2024-12-01', '2024-12-31', 79.99, '2024-12-30', '2024-12-30'),
            (1, 1, '2025-01-01', '2025-01-31', 49.99, '2025-01-30', '2025-02-02'),
            (2, 2, '2024-11-01', '2024-11-30', 79.99, '2024-11-30', '2024-11-29'),
            (2, 3, '2024-12-01', '2024-12-31', 29.99, '2024-12-30', '2024-12-30'),
            (2, 2, '2025-01-01', '2025-01-31', 79.99, '2025-01-30', '2025-02-05'),
            (3, 3, '2024-11-01', '2024-11-30', 29.99, '2024-11-30', '2024-11-30'),
            (3, 2, '2024-12-01', '2024-12-31', 79.99, '2024-12-30', '2024-12-28'),
            (3, 3, '2025-01-01', '2025-01-31', 29.99, '2025-01-30', '2025-01-30'),
            (4, 1, '2024-11-01', '2024-11-30', 49.99, '2024-11-30', '2024-11-30'),
            (4, 3, '2024-12-01', '2024-12-31', 29.99, '2024-12-30', '2025-01-05'),
            (4, 2, '2025-01-01', '2025-01-31', 79.99, '2025-01-30', '2025-01-29'),
            (5, 2, '2024-11-01', '2024-11-30', 79.99, '2024-11-30', '2024-11-30'),
            (5, 1, '2024-12-01', '2024-12-31', 49.99, '2024-12-30', '2024-12-29'),
            (5, 2, '2025-01-01', '2025-01-31', 79.99, '2025-01-30', '2025-02-02')
        ])

    print("Data inserted successfully.")
    
"""insert_data()"""


import sqlite3
def retrieve_data():
    """
    This function retrieves all data from all tables in the database and prints them.
    """

    db_name = "DB2.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(''' 
    SELECT * FROM customers_table
    ''')
    customers = cursor.fetchall()
    print("\nCustomer Information:")
    for customer in customers:
        print(customer)

    cursor.execute(''' 
    SELECT * FROM plan_details
    ''')
    plans = cursor.fetchall()
    print("\nPlan Information:")
    for plan in plans:
        print(plan)

    cursor.execute(''' 
    SELECT * FROM paymenthistory
    ''')
    paymenthistory = cursor.fetchall()
    print("\nPayment History:")
    for payment in paymenthistory:
        print(payment)

    conn.close()
retrieve_data()



import sqlite3

def collect_customer_data(customer_id: int):
    """
    Collects all data related to a customer from the database using the provided customer ID.
    
    Args:
        customer_id: The unique identifier for the customer (integer).
        
    Returns:
        A dictionary containing all related data for the customer.
    """
    
    db_name = "DB2.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id, name, email, plan_id FROM customers_table WHERE customer_id = ?", (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        conn.close()
        return {"error": "Customer not found."}

    customer_data = dict(zip(
        ("customer_id", "name", "email", "plan_id"),
        customer
    ))

    cursor.execute("SELECT plan_type, speed, data_usage, monthly_charge FROM plan_details WHERE plan_id = ?", (customer_data["plan_id"],))
    plan = cursor.fetchone()

    if plan:
        customer_data["current_plan"] = plan[0]
        customer_data["speed"] = plan[1]
        customer_data["data_usage"] = plan[2]
        customer_data["monthly_charge"] = plan[3]

    cursor.execute("SELECT start_date, end_date, price, due_date, paid_date FROM paymenthistory WHERE customer_id = ?", (customer_id,))
    payment_history = cursor.fetchall()

    payment_data = [
        dict(zip(["start_date", "end_date", "price", "due_date", "paid_date"], payment))
        for payment in payment_history
    ]

    customer_data["payment_history"] = payment_data
    
    conn.close()
    return customer_data
    
collect_customer_data(3)



from datetime import datetime, timedelta

def get_last_day_of_month(date):
    # Find the first day of the next month
    next_month = date.replace(day=28) + timedelta(days=4)
    # Subtract the days to get the last day of the current month
    return next_month - timedelta(days=next_month.day)

def generate_payment_statement(customer_data: dict, start: str = None, end: str = None) -> str:
    """
    Generates a payment statement for a customer based on their payment history, checks for late fees,
    and carries over unpaid fees to the current month.
    
    Args:
        customer_data (dict): A dictionary containing the customer's details including their payment history.
        start (str, optional): The start date (inclusive) in 'YYYY-MM-DD' format for the statement.
        end (str, optional): The end date (inclusive) in 'YYYY-MM-DD' format for the statement.

    Returns:
        str: A formatted string representing the customer's payment statement.
    """
    current_date = datetime.now()  # Current date for comparison
    late_fee_carry_over = 0  # To carry over the late fee to the next month if there is any
    statement = []

    # Parse start and end dates if provided
    start_date = datetime.strptime(start, '%Y-%m-%d') if start else None
    end_date = datetime.strptime(end, '%Y-%m-%d') if end else current_date

    # Header
    statement.extend([
        f"Payment Statement for {customer_data['name']} (ID: {customer_data['customer_id']})",
        f"Email: {customer_data['email']}",
        f"Plan: {customer_data['current_plan']} - {customer_data['speed']}, {customer_data['data_usage']}",
        f"Monthly Charge: ${customer_data['monthly_charge']:.2f}",
        "=" * 50
    ])

    # Iterate through the payment history and calculate late fees if necessary
    last_payment_end_date = None
    for payment in customer_data["payment_history"]:
        payment_start_date = datetime.strptime(payment["start_date"], '%Y-%m-%d')
        payment_end_date = datetime.strptime(payment["end_date"], '%Y-%m-%d')
        due_date = datetime.strptime(payment["due_date"], '%Y-%m-%d')
        paid_date = payment.get("paid_date")  # Might be None if not paid
        price = payment["price"]
        
        # Skip payments outside the specified date range
        if (start_date and payment_end_date < start_date) or payment_start_date > end_date:
            continue
        
        overdue = False
        if paid_date:
            paid_date = datetime.strptime(paid_date, '%Y-%m-%d')
            if paid_date > due_date:
                overdue = True  # Payment was made after the due date
        
        late_fee = 0
        if overdue:
            late_fee = 0.1 * price  # 10% late fee
            price += late_fee  # Add late fee to the current month's payment
            late_fee_carry_over += late_fee  # Carry over the late fee to the next month

        payment_status = "Late fee applied" if overdue else "Paid on time"
        statement.append(f"Payment for {payment['start_date']} - {payment['end_date']}: {payment_status}. Total: ${price:.2f} (Late Fee: ${late_fee:.2f})")
        last_payment_end_date = payment["end_date"]  # Keep track of the last payment's end date

    # Print plan details month-wise
    if last_payment_end_date:
        statement.append("=" * 50)
        statement.append(f"Monthly Plan Details:")
        
        # Dynamically calculate the start and end dates for each month based on the last payment's end date
        start_of_current_month = datetime.strptime(last_payment_end_date, '%Y-%m-%d') + timedelta(days=1)
        while start_of_current_month < current_date:
            end_of_current_month = get_last_day_of_month(start_of_current_month)  # Get the last day of the current month dynamically
            
            next_month_start_date = start_of_current_month.strftime('%Y-%m-%d')
            next_month_end_date = end_of_current_month.strftime('%Y-%m-%d')
            next_month_due_date = end_of_current_month.strftime('%Y-%m-%d')
            
            # Skip months outside the specified date range
            if (start_date and end_of_current_month < start_date) or start_of_current_month > end_date:
                start_of_current_month = end_of_current_month + timedelta(days=1)
                continue
            
            total_this_month = customer_data["monthly_charge"] + late_fee_carry_over
            statement.extend([
                f"Plan for {next_month_start_date} - {next_month_end_date}: ${total_this_month:.2f}",
                f"Due Date: {next_month_due_date}",
                "=" * 50
            ])
            
            start_of_current_month = end_of_current_month + timedelta(days=1)

    # Convert the list to a string and return the formatted statement
    result = "\n".join(statement)
    return result

# Example usage:
customer_data = collect_customer_data(1)
# Generate statement for a specific date range
statement1 = generate_payment_statement(customer_data, start='2025-01-01', end='2025-02-28')
print(statement1)

# Generate statement for the entire history
statement2 = generate_payment_statement(customer_data)
print(statement2)
