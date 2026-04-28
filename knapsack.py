"""
knapsack.py
-----------
0/1 Knapsack dynamic programming implementation.

The 0/1 Knapsack Problem:
    Given n items each with a price (weight) and a value (rating score),
    and a maximum budget W, find the subset of items that:
      - Has a total price <= W
      - Maximizes the total rating score
    Each item is either selected (1) or not (0) — it cannot be bought
    more than once.

Time complexity:  O(n * W)  where n = number of items, W = budget in cents
Space complexity: O(n * W)  for the DP table used in backtracking
"""


def solve_knapsack(items: list, budget_dollars: float) -> dict:
    """
    Solve the 0/1 Knapsack problem for a list of grocery items.

    Parameters
    ----------
    items : list of dict
        Each dict must have:
            'title'        : str   - product name
            'price'        : float - price in dollars
            'rating'       : float - customer rating (1.0 to 5.0)
            'subcategory'  : str   - grocery category
            'vegetarian'   : bool  - whether the item is vegetarian
    budget_dollars : float
        The user's total grocery budget in dollars.

    Returns
    -------
    dict with keys:
        'selected_items' : list of dict - the optimal set of items chosen
        'total_price'    : float        - total cost of selected items
        'total_score'    : float        - sum of rating scores
    """

    # --- Step 1: Convert prices to integer cents ---
    # Dynamic programming requires the budget to be a discrete integer.
    # A decimal like $12.99 cannot be used as an array index directly.
    # Multiplying by 100 and rounding converts $12.99 -> 1299 cents,
    # making the table index exact and avoiding floating-point errors.
    budget_cents = int(round(budget_dollars * 100))

    # Filter out items that cost more than the entire budget — they
    # can never be selected regardless of the DP, so we skip them early.
    valid_items = []
    for item in items:
        price_cents = int(round(item["price"] * 100))
        if price_cents > 0 and price_cents <= budget_cents:
            valid_items.append({
                **item,
                "price_cents": price_cents,
                # Scale rating to integer (4.7 -> 470) to keep all
                # arithmetic in integers throughout the DP table.
                "value": int(round(item["rating"] * 100)),
            })

    n = len(valid_items)
    W = budget_cents

    if n == 0 or W == 0:
        return {"selected_items": [], "total_price": 0.0, "total_score": 0.0}

    # --- Step 2: Build the DP table ---
    # dp[i][w] = the maximum total value achievable by considering the
    #            first i items with a budget of exactly w cents.
    #
    # Recurrence relation:
    #   Option A — skip item i:
    #       dp[i][w] = dp[i-1][w]
    #   Option B — include item i (only if it fits):
    #       dp[i][w] = dp[i-1][w - price_i] + value_i
    #   We take whichever option gives the higher value.
    #
    # Base case: dp[0][w] = 0 for all w (no items considered = no value).

    # We store the full table (not just one row) so we can backtrack
    # afterwards to find which specific items were selected.
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        price_i = valid_items[i - 1]["price_cents"]
        value_i = valid_items[i - 1]["value"]

        for w in range(W + 1):
            # Start with: do not take item i
            dp[i][w] = dp[i - 1][w]
            # Consider: take item i if it fits within budget w
            if w >= price_i:
                with_item = dp[i - 1][w - price_i] + value_i
                if with_item > dp[i][w]:
                    dp[i][w] = with_item

    # --- Step 3: Backtrack to recover which items were selected ---
    # Starting from dp[n][W], walk backwards through the table.
    # If dp[i][w] differs from dp[i-1][w], item i was included —
    # record it and subtract its price from the remaining budget w.
    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(valid_items[i - 1])
            w -= valid_items[i - 1]["price_cents"]

    selected.reverse()  # restore original dataset order

    total_price = sum(item["price"] for item in selected)
    total_score = sum(item["rating"] for item in selected)

    return {
        "selected_items": selected,
        "total_price": round(total_price, 2),
        "total_score": round(total_score, 2),
    }
