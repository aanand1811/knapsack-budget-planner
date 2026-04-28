# Smart Budget Planner
### Optimizing Grocery Shopping Using the 0/1 Knapsack Algorithm

**MSML606 Extra Credit Project 2**  
Anoushka Anand, FNU Hardik

---

## What Is This?

The Smart Budget Planner is a simple web app that answers one question:

> Given my Costco budget, what should I buy to get the best value?

You enter your budget and the app finds the best combination of grocery items that fits within that amount while maximizing the total customer rating. You do not need any technical background to use it.

---

## The Algorithm

Each item has:
- a price  
- a customer rating  

The budget acts as a limit. The goal is to pick items so that:
- the total price stays within the budget  
- the total rating is as high as possible  
- each item is chosen at most once  

This is solved using the 0/1 Knapsack approach. The algorithm builds a table based on the number of items and the budget, then traces back to find which items were selected.

Prices are converted into cents so the calculations stay exact.

Time complexity is O(n x W), where n is the number of items and W is the budget in cents.

---

## Dataset

Source: Costco Grocery Dataset from Kaggle  
https://www.kaggle.com/datasets/elvinrustam/grocery-dataset

The dataset comes from Costco’s online store. The version used here is a cleaned subset of 54 items across different categories.

| Column | Description |
|--------|------------|
| title | Product name |
| price | Price in USD |
| rating | Customer rating (1 to 5) |
| subcategory | Category for filtering |
| vegetarian | Whether the item is vegetarian |

---

## Features

- Budget slider to set how much you want to spend  
- Option to include must-have items  
- Vegetarian mode to filter out non-vegetarian items  
- Category filter to focus on specific types of products  

---

## How to Run

### 1. Clone the repository

```
git clone https://github.com/aanand1811/knapsack-budget-planner.git
cd knapsack-budget-planner
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

## AI Usage Statement

This project follows the MSML606 AI policy.

The following parts were written manually:
- Knapsack algorithm implementation in knapsack.py  
- Data processing and filtering in data_loader.py  
- Overall application logic  
- This README  

AI tools were used only for:
- UI assistance in app.py  
- Minor help with formatting  

No AI was used to generate the algorithm or the core solution.

---

## For Non-CS Readers

Think of this like a smart shopping assistant.

You give it a budget. It checks different combinations of items and finds the one that gives you the best overall rating without going over your budget.

It then tells you exactly what to buy.
