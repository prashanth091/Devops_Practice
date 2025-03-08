def generate_payment_statement(customer_data: dict):
    """
    Generates a payment statement for a customer based on their payment history, checks for late fees,
    and carries over unpaid fees to the current month.
    
    Args:
        customer_data (dict): A dictionary containing the customer's details including their payment history.

    Returns:
        str: A formatted string representing the customer's payment statement.
    """
    
    current_date = datetime.now()  # Current date for comparison
    late_fee_carry_over = 0  # To carry over the late fee to the next month if there is any
    statement = []
    
    statement.append(f"Payment Statement for {customer_data['name']} (ID: {customer_data['customer_id']})")
    statement.append(f"Email: {customer_data['email']}")
    statement.append(f"Plan: {customer_data['current_plan']} - {customer_data['speed']}, {customer_data['data_usage']}")
    statement.append(f"Monthly Charge: ${customer_data['monthly_charge']:.2f}")
    statement.append("=" * 50)

    # Iterate through the payment history and calculate late fees if necessary
    last_payment_end_date = None
    for payment in customer_data["payment_history"]:
        due_date = datetime.strptime(payment["due_date"], '%Y-%m-%d')
        paid_date = payment.get("paid_date")  # Might be None if not paid
        price = payment["price"]
        
        # Check if the payment is overdue
        overdue = False
        late_fee = 0

        if paid_date:
            paid_date = datetime.strptime(paid_date, '%Y-%m-%d')
        
        if paid_date and paid_date > due_date:
            overdue = True  # Payment was made after the due date
        
        if overdue:
            late_fee = 0.1 * price  # 10% late fee
            price += late_fee  # Add late fee to the current month's payment
            late_fee_carry_over += late_fee  # Carry over the late fee to the next month
            statement.append(f"Payment for {payment['start_date']} - {payment['end_date']}: Late fee applied. Total: ${price:.2f} (Late Fee: ${late_fee:.2f})")
        else:
            statement.append(f"Payment for {payment['start_date']} - {payment['end_date']}: Paid on time. Total: ${price:.2f}")

        last_payment_end_date = payment["end_date"]  # Keep track of the last payment's end date

    # If there's any carry-over late fee, add it to the current month's payment
    if last_payment_end_date:
        statement.append("=" * 50)
        statement.append(f"Carry-Over Late Fee for this month: ${late_fee_carry_over:.2f}")
        
        # Dynamically calculate the start and end dates for the ongoing month based on the last payment's end date
        start_of_current_month = datetime.strptime(last_payment_end_date, '%Y-%m-%d') + timedelta(days=1)  # Start date is the day after the last payment's end date
        end_of_current_month = start_of_current_month.replace(day=28) + timedelta(days=4)  # This gets the last day of the current month
        end_of_current_month = end_of_current_month - timedelta(days=end_of_current_month.day)

        next_month_start_date = start_of_current_month.strftime('%Y-%m-%d')
        next_month_end_date = end_of_current_month.strftime('%Y-%m-%d')
        next_month_due_date = end_of_current_month.strftime('%Y-%m-%d')

        # Add the late fee to the ongoing month's total charge (e.g., February 2025)
        total_this_month = customer_data["monthly_charge"] + late_fee_carry_over
        statement.append(f"Ongoing Plan Payment ({next_month_start_date} - {next_month_end_date}): ${total_this_month:.2f}")
        statement.append(f"Due Date: {next_month_due_date}")
    
    statement.append("=" * 50)
    statement.append(f"Total Amount Due for this Month: ${total_this_month:.2f}")
    statement.append("=" * 50)

    # Convert the list to a string and return the formatted statement
    result = "\n".join(statement)
    return result
customer_data = collect_customer_data(1)
statement1 = generate_payment_statement(customer_data)
print(statement1)