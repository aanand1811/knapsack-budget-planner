"""
app.py
------
Smart Budget Planner — Streamlit Application

Uses the 0/1 Knapsack dynamic programming algorithm to find the optimal
set of Costco grocery items within a user-defined budget, maximizing
total customer rating score.

Each item is either selected or not — no partial selections, no multiples.
Must-have items are pinned by the user, their cost is deducted from the
budget first, and the algorithm optimizes over the rest.
"""

import streamlit as st
import pandas as pd
from knapsack import solve_knapsack
from data_loader import load_data, filter_items, get_subcategories

# Page config 
st.set_page_config(
    page_title="Smart Budget Planner",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f7f4ef; }

[data-testid="stSidebar"] { background-color: #1a2e1a; }
[data-testid="stSidebar"] * { color: #e8f0e8 !important; }
[data-testid="stSidebar"] label {
    color: #b8d4b8 !important;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.hero {
    background: linear-gradient(135deg, #1a2e1a 0%, #2d5a2d 60%, #4a7c4a 100%);
    border-radius: 14px;
    padding: 2.2rem 2rem;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    margin: 0 0 0.35rem 0;
    color: #e8f5e8;
    line-height: 1.2;
}
.hero p { font-size: 0.95rem; color: #a8cca8; margin: 0; }

.stat-card {
    background: white;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    border-left: 4px solid #2d5a2d;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 0.5rem;
}
.stat-card .label {
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.08em; color: #999; margin-bottom: 0.25rem;
}
.stat-card .value { font-size: 1.7rem; font-weight: 700; color: #1a2e1a; line-height: 1; }
.stat-card .sub   { font-size: 0.78rem; color: #bbb; margin-top: 0.2rem; }

.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem; color: #1a2e1a;
    margin: 1.4rem 0 0.7rem 0;
    padding-bottom: 0.35rem;
    border-bottom: 2px solid #ddd;
}

.item-card {
    background: white;
    border-radius: 9px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.55rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid #eae6df;
}
.item-card:hover { box-shadow: 0 3px 12px rgba(0,0,0,0.09); }

.item-card-pinned {
    background: #f6fbf6;
    border-radius: 9px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.55rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1.5px solid #2d5a2d;
}

/* Left badge on each card */
.item-badge {
    background: #1a2e1a;
    color: white;
    font-weight: 700;
    font-size: 0.72rem;
    border-radius: 6px;
    min-width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    letter-spacing: 0.02em;
}
.item-badge-pinned {
    background: #2d5a2d;
    color: #c8e6c8;
    font-weight: 700;
    font-size: 0.72rem;
    border-radius: 6px;
    min-width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.item-info  { flex: 1; }
.item-title { font-weight: 600; color: #1a2e1a; font-size: 0.93rem; }
.item-sub   { font-size: 0.76rem; color: #999; margin-top: 2px; }
.item-price { font-weight: 700; color: #2d5a2d; font-size: 1rem; text-align: right; }
.item-rating-sub { font-size: 0.74rem; color: #aaa; text-align: right; }

.veg-badge {
    display: inline-block;
    background: #dcfce7; color: #166534;
    font-size: 0.68rem; padding: 1px 7px;
    border-radius: 20px; font-weight: 600; margin-left: 6px;
}
.pin-badge {
    display: inline-block;
    background: #1a2e1a; color: #a8cca8;
    font-size: 0.68rem; padding: 1px 7px;
    border-radius: 20px; font-weight: 600; margin-left: 6px;
}

.cat-label {
    font-size: 0.75rem; text-transform: uppercase;
    letter-spacing: 0.08em; color: #999;
    margin: 0.75rem 0 0.3rem 0; font-weight: 600;
}

.algo-note {
    background: #f0f7f0;
    border: 1px solid #c3dfc3;
    border-left: 4px solid #2d5a2d;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    font-size: 0.84rem; color: #2d5a2d;
    margin-top: 1rem; line-height: 1.6;
}

.budget-breakdown {
    background: #fff8ec;
    border: 1px solid #f0d9a0;
    border-left: 4px solid #d97706;
    border-radius: 8px;
    padding: 0.75rem 1.1rem;
    font-size: 0.84rem; color: #92400e;
    margin-bottom: 1rem; line-height: 1.7;
}

.empty-state {
    text-align: center; padding: 3rem;
    color: #bbb; font-size: 0.95rem;
}

.budget-bar-wrap {
    background: #e8ede8; border-radius: 6px;
    height: 8px; margin: 0.4rem 0 1rem 0; overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# Load data 
@st.cache_data
def get_data():
    return load_data()

df = get_data()
all_subcategories = get_subcategories(df)
all_titles = sorted(df["title"].tolist())

# Sidebar
with st.sidebar:
    st.markdown("## Planner Settings")
    st.markdown("---")

    st.markdown("**Your Budget**")
    budget = st.slider(
        "Budget", min_value=10, max_value=300, value=100,
        step=5, format="$%d", label_visibility="collapsed",
    )
    st.markdown(
        f"<div style='font-size:2rem;font-weight:700;color:#a8cca8;"
        f"margin-bottom:1rem;'>${budget}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("**Must-Have Items**")
    st.markdown(
        "<div style='font-size:0.74rem;color:#7a9a7a;margin-bottom:0.5rem;line-height:1.5;'>"
        "These items are always included. Their cost is deducted from your "
        "budget before the algorithm runs on the rest.</div>",
        unsafe_allow_html=True,
    )
    must_have_titles = st.multiselect(
        "Must-have items", options=all_titles, default=[],
        label_visibility="collapsed", placeholder="Search and select...",
    )

    st.markdown("---")

    vegetarian_only = st.checkbox(
        "Vegetarian Mode", value=False,
        help="Exclude all meat and non-vegetarian products",
    )

    st.markdown("---")

    st.markdown("**Filter by Category**")
    selected_subs = st.multiselect(
        "Categories", options=all_subcategories,
        default=all_subcategories, label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size:0.74rem;color:#7a9a7a;line-height:1.65;'>
        <b>How it works:</b><br>
        The <b>0/1 Knapsack</b> algorithm finds the combination of grocery
        items that fits your budget while maximizing total customer rating
        score. Each item is either included or excluded — no partial
        selections.<br><br>
        Must-have items are locked in first; the algorithm optimizes the
        rest of your budget.<br><br>
        Dataset: <a href='https://www.kaggle.com/datasets/elvinrustam/grocery-dataset'
        style='color:#a8cca8;'>Costco Grocery (Kaggle)</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Hero 
st.markdown(
    """
    <div class='hero'>
        <h1>Smart Budget Planner</h1>
        <p>Set your budget, pin any must-have items, and the 0/1 Knapsack
        algorithm instantly finds the best combination of groceries for you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Prepare pools
all_items = filter_items(
    df,
    subcategories=selected_subs if selected_subs else None,
    vegetarian_only=vegetarian_only,
)

must_have_items = [
    row for row in df.to_dict(orient="records")
    if row["title"] in must_have_titles
]
must_have_set    = {item["title"] for item in must_have_items}
must_have_cost   = round(sum(item["price"] for item in must_have_items), 2)
remaining_budget = round(budget - must_have_cost, 2)
pool_items       = [item for item in all_items if item["title"] not in must_have_set]

# Guard: must-haves exceed budget
if must_have_cost > budget:
    st.error(
        f"Your must-have items total ${must_have_cost:.2f}, which exceeds your "
        f"${budget} budget. Please increase your budget or remove some must-have items."
    )
    st.stop()

if not pool_items and not must_have_items:
    st.markdown(
        "<div class='empty-state'>No items match your current filters. "
        "Try selecting more categories or disabling Vegetarian Mode.</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# Run 0/1 Knapsack 
if pool_items and remaining_budget > 0:
    result        = solve_knapsack(pool_items, budget_dollars=remaining_budget)
    algo_selected = result["selected_items"]
    algo_price    = result["total_price"]
    algo_score    = result["total_score"]
else:
    algo_selected = []
    algo_price    = 0.0
    algo_score    = 0.0

# Totals
all_selected = must_have_items + algo_selected
total_price  = round(must_have_cost + algo_price, 2)
total_score  = round(sum(i["rating"] for i in must_have_items) + algo_score, 2)
remaining    = round(budget - total_price, 2)
avg_rating   = round(total_score / len(all_selected), 2) if all_selected else 0.0
budget_pct   = int((total_price / budget) * 100) if budget > 0 else 0
pinned_pct   = int((must_have_cost / budget) * 100) if budget > 0 else 0

# Stats 
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"<div class='stat-card'><div class='label'>Items Selected</div>"
        f"<div class='value'>{len(all_selected)}</div>"
        f"<div class='sub'>{len(must_have_items)} pinned + {len(algo_selected)} optimal</div></div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"<div class='stat-card'><div class='label'>Total Spent</div>"
        f"<div class='value'>${total_price:.2f}</div>"
        f"<div class='sub'>${remaining:.2f} remaining</div></div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"<div class='stat-card'><div class='label'>Avg Rating</div>"
        f"<div class='value'>{avg_rating}</div>"
        f"<div class='sub'>out of 5.0</div></div>",
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"<div class='stat-card'><div class='label'>Budget Used</div>"
        f"<div class='value'>{budget_pct}%</div>"
        f"<div class='sub'>of ${budget} total</div></div>",
        unsafe_allow_html=True,
    )

# Two-tone budget bar: amber = pinned, green = algorithm
algo_bar_pct = max(budget_pct - pinned_pct, 0)
st.markdown(
    f"<div class='budget-bar-wrap'>"
    f"<div style='height:8px;display:flex;border-radius:6px;overflow:hidden;'>"
    f"<div style='width:{pinned_pct}%;background:#d97706;'></div>"
    f"<div style='width:{algo_bar_pct}%;background:linear-gradient(90deg,#2d5a2d,#4a9a4a);'></div>"
    f"</div></div>",
    unsafe_allow_html=True,
)

if must_have_items:
    st.markdown(
        f"<div class='budget-breakdown'>"
        f"<b>Budget breakdown:</b>&nbsp; "
        f"${must_have_cost:.2f} reserved for {len(must_have_items)} pinned item(s)"
        f" &nbsp;|&nbsp; ${remaining_budget:.2f} available for the algorithm"
        f"</div>",
        unsafe_allow_html=True,
    )

#  Render helper 
def render_card(item: dict, pinned: bool = False) -> None:
    veg_html  = "<span class='veg-badge'>Veg</span>" if item["vegetarian"] else ""
    pin_html  = "<span class='pin-badge'>Pinned</span>" if pinned else ""
    card_cls  = "item-card-pinned" if pinned else "item-card"
    badge_cls = "item-badge-pinned" if pinned else "item-badge"
    badge_txt = "PIN" if pinned else "#1"

    st.markdown(
        f"""
        <div class='{card_cls}'>
            <div class='{badge_cls}'>{badge_txt}</div>
            <div class='item-info'>
                <div class='item-title'>{item['title']}{veg_html}{pin_html}</div>
                <div class='item-sub'>
                    {item['subcategory']}
                    &nbsp;&middot;&nbsp;
                    Rating: {item['rating']} / 5.0
                </div>
            </div>
            <div>
                <div class='item-price'>${item['price']:.2f}</div>
                <div class='item-rating-sub'>single unit</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Must-have items 
if must_have_items:
    st.markdown(
        "<div class='section-header'>Must-Have Items (Pinned)</div>",
        unsafe_allow_html=True,
    )
    for item in must_have_items:
        render_card(item, pinned=True)

# Algorithm-selected items
if algo_selected:
    header = "Algorithm Selection" if must_have_items else "Optimal Selection"
    st.markdown(
        f"<div class='section-header'>{header}</div>",
        unsafe_allow_html=True,
    )

    # Group by subcategory
    by_sub: dict = {}
    for item in algo_selected:
        by_sub.setdefault(item["subcategory"], []).append(item)

    for sub, sub_items in by_sub.items():
        st.markdown(
            f"<div class='cat-label'>{sub}</div>",
            unsafe_allow_html=True,
        )
        for item in sub_items:
            render_card(item, pinned=False)

elif not must_have_items:
    st.markdown(
        "<div class='empty-state'>No items fit within your budget and filters. "
        "Try increasing the budget or selecting more categories.</div>",
        unsafe_allow_html=True,
    )
elif remaining_budget <= 0:
    st.markdown(
        "<div class='empty-state'>Must-have items have used the entire budget. "
        "Increase your budget to let the algorithm add more items.</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div class='empty-state'>No additional items fit within the remaining budget.</div>",
        unsafe_allow_html=True,
    )

#  Algorithm note 
if all_selected:
    pinned_note = (
        f" After reserving ${must_have_cost:.2f} for {len(must_have_items)} "
        f"pinned item(s), the algorithm had ${remaining_budget:.2f} to work with."
        if must_have_items else ""
    )
    st.markdown(
        f"<div class='algo-note'>"
        f"<b>How the algorithm chose these items:</b><br>"
        f"Running the <b>0/1 Knapsack</b> algorithm across {len(pool_items)} available items, "
        f"the algorithm found the combination that fits within the "
        f"<b>${remaining_budget:.2f} budget</b> while achieving the highest possible "
        f"total customer rating score "
        f"(<b>{round(algo_score, 1)} points</b> from algorithm picks, "
        f"<b>{round(total_score, 1)} points</b> total). "
        f"Each item is either fully included or excluded — no partial selections.{pinned_note} "
        f"Prices were converted to integer cents for exact DP computation."
        f"</div>",
        unsafe_allow_html=True,
    )

#  All available items 
with st.expander("View All Available Items"):
    display_df = pd.DataFrame(all_items)[
        ["title", "subcategory", "price", "rating", "vegetarian"]
    ]
    display_df.columns = ["Product", "Category", "Price ($)", "Rating", "Vegetarian"]
    display_df["Price ($)"] = display_df["Price ($)"].map("${:.2f}".format)
    display_df["Vegetarian"] = display_df["Vegetarian"].map({True: "Yes", False: "No"})
    st.dataframe(display_df, use_container_width=True, hide_index=True)