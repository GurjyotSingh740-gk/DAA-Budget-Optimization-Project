import matplotlib.pyplot as plt

user_data = {
    "income": 3000, 
    "expenses": {
        "rent": 1000,
        "groceries": 300,
        "utilities": 200,
        "entertainment": 150,
        "transport": 100,
    },
    "savings_goal": 500 
}

expense_priorities = {
    "rent": 10,
    "groceries": 8,
    "utilities": 7,
    "entertainment": 4,
    "transport": 5
}


def optimize_budget(expenses, priorities, savings_goal):
    expense_list = [(k, v, priorities[k]) for k, v in expenses.items()]
    n = len(expense_list)
    dp = [[0] * (savings_goal + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(savings_goal + 1):
            category, cost, priority = expense_list[i - 1]
            if cost <= w:
                dp[i][w] = max(priority + dp[i - 1][w - cost], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    
    w = savings_goal
    adjustments = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            category, cost, priority = expense_list[i - 1]
            adjustments.append((category, cost))
            w -= cost
    
    return adjustments


def greedy_expense_reduction(expenses, priorities, savings_goal):
    sorted_expenses = sorted(expenses.items(), key=lambda x: priorities[x[0]])
    remaining_goal = savings_goal
    reductions = []
    
    for category, amount in sorted_expenses:
        if remaining_goal <= 0:
            break
        reducible_amount = min(amount, remaining_goal)
        reductions.append((category, reducible_amount))
        remaining_goal -= reducible_amount
    
    return reductions


def display_suggestions(adjustments, expenses, savings_goal, method="Knapsack"):
    print(f"\n=== {method} Budget Optimization Suggestions ===")
    total_savings = sum(amount for _, amount in adjustments)
    
    if total_savings >= savings_goal:
        print(f"To reach your savings goal of ${savings_goal}, consider adjusting these expenses:")
        for category, amount in adjustments:
            print(f"- Reduce {category} by ${amount}")
    else:
        print("Your expenses are too high to meet the savings goal with adjustments alone.")


def visualize_expenses(expenses):
    categories = list(expenses.keys())
    amounts = list(expenses.values())
    
    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='skyblue')
    plt.xlabel('Expense Categories')
    plt.ylabel('Amount Spent ($)')
    plt.title('Monthly Expenses')
    plt.show()
    
    # Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution')
    plt.show()


def main():
    print("=== Personal Finance Management System ===")
    print("Income: $", user_data["income"])
    print("Expenses:")
    for category, amount in user_data["expenses"].items():
        print(f"  {category}: ${amount}")
    print("Savings Goal: $", user_data["savings_goal"])
    
    knapsack_adjustments = optimize_budget(user_data["expenses"], expense_priorities, user_data["savings_goal"])
    display_suggestions(knapsack_adjustments, user_data["expenses"], user_data["savings_goal"], method="Knapsack")
    
    greedy_adjustments = greedy_expense_reduction(user_data["expenses"], expense_priorities, user_data["savings_goal"])
    display_suggestions(greedy_adjustments, user_data["expenses"], user_data["savings_goal"], method="Greedy")
    
    visualize_expenses(user_data["expenses"])


if __name__ == "__main__":
    main()
