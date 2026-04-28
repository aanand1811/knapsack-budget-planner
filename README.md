# Smart Budget Planner
### Optimizing Grocery Shopping Using the 0/1 Knapsack Algorithm

**MSML606 Extra Credit Project 2 — Spring 2026**
Anoushka Anand · FNU Hardik · University of Maryland

---

## What Is This?

The Smart Budget Planner is a web application that answers a simple question:

> Given my Costco budget, which items should I buy to get the best value?

You set your budget. The app instantly finds the optimal combination of grocery items that fits within your spending limit while achieving the highest possible total customer rating score. No computer science background is needed to use it.

---

## The Algorithm: 0/1 Knapsack (Dynamic Programming)

Each grocery item has a price (the cost) and a customer rating score (the value). The user's budget is the capacity. The 0/1 Knapsack algorithm finds the combination of items that:

- Fits within the budget
- Maximizes the total rating score
- Selects each item at most once (0 or 1 times — no partial selections)

The algorithm builds a 2D dynamic programming table of size n x W, where n is the number of items and W is the budget in cents. It then backtracks through the table to recover exactly which items were selected.

Prices are converted to integer cents (for example, $12.99 becomes 1299) so the DP table index is exact and avoids floating-point errors.

**Time complexity:** O(n x W)

---

## Dataset

**Source:** Costco Grocery Dataset on Kaggle
**Link:** https://www.kaggle.com/datasets/elvinrustam/grocery-dataset

The dataset was scraped from Costco's online marketplace. The working file (costco_grocery.csv) is a cleaned subset of 54 items across 7 grocery categories.

| Column | Description | Role in Algorithm |
|---|---|---|
| title | Product name | Shown to user |
| price | Price in USD | Knapsack weight (cost constraint) |
| rating | Customer rating (1 to 5 stars) | Knapsack value (what we maximize) |
| subcategory | Grocery category | UI category filter |
| vegetarian | True or False | Vegetarian mode filter |

---

## Features

**Budget Slider** — Set any budget from $10 to $300. The algorithm recalculates the optimal selection instantly.

**Must-Have Items** — Pin specific items that must always be included. Their cost is deducted from the budget first and the algorithm optimizes the remainder.

**Vegetarian Mode** — A single toggle excludes all non-vegetarian products before the algorithm runs.

**Subcategory Filter** — Focus on specific grocery categories such as Dairy, Produce, Proteins, Grains, Snacks, Pantry, or Beverages.

---

## How to Run

### 1. Clone the repository
```
git clone https://github.com/[your-username]/smart-budget-planner.git
cd smart-budget-planner
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the app
```
streamlit run app.py
```

The app will open in your browser at http://localhost:8501.

---

## Project Structure

```
smart_budget_planner/
├── app.py                 Streamlit UI (AI-assisted styling, per project rules)
├── knapsack.py            Core 0/1 Knapsack DP algorithm (manually authored)
├── data_loader.py         Dataset loading and filtering (manually authored)
├── costco_grocery.csv     Cleaned grocery dataset
├── requirements.txt       Python dependencies
└── README.md              This file
```

---

## Academic Integrity Statement

This project was completed for MSML606 Extra Credit Project 2 at the University of Maryland, Spring 2026.

**Manually authored by the team:**
- Core knapsack algorithm (knapsack.py) including all DP logic, backtracking, and cent conversion
- Data loading and preprocessing (data_loader.py)
- All code comments throughout the codebase
- This README

**AI-assisted (per project rules):**
- UI styling and layout in app.py
- Slide design and layout for the presentation

No AI was used to generate the core algorithm logic or the initial approach to solving the problem.

**Dataset:** Costco Grocery Dataset sourced from Kaggle (see link above). No proprietary data was used.

---

## For Non-CS Readers

Think of it like a very smart shopping list generator:

1. You tell it your budget (say $100)
2. It looks at every possible combination of grocery items
3. It picks the combination where the items' customer ratings add up to the highest total without going over your budget
4. It shows you exactly what to buy and how much it costs

The math behind it is the same kind used in logistics, resource planning, and financial portfolio optimization — applied to your grocery cart.
