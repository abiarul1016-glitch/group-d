import pandas as pd
import random
import string
import streamlit as st

# ---------- Logic ----------
def find_best_groups(iterations, students, number_of_groups, together_pairs, not_together_pairs):
    best_score = float('inf')
    best_assignment = None

    for _ in range(iterations):
        shuffled = students[:]
        random.shuffle(shuffled)

        groups = [[] for _ in range(number_of_groups)]

        for i, student in enumerate(shuffled):
            groups[i % number_of_groups].append(student)

        score = get_score(groups, together_pairs, not_together_pairs)

        if score < best_score:
            best_score = score
            best_assignment = groups

        if best_score == 0:
            break

    return best_assignment, best_score


def get_score(groups, together_pairs, not_together_pairs):
    score = 0
    for group in groups:
        for p1, p2 in together_pairs:
            if (p1 in group) ^ (p2 in group):
                score += 10

        for p1, p2 in not_together_pairs:
            if p1 in group and p2 in group:
                score += 50

    return score


# ---------- UI ----------
st.set_page_config(page_title="Smart Group Generator", layout="wide")

st.title("🎓 Smart Group Generator")
st.caption("Create optimized student groups with smart constraints")

# Upload Section
st.header("1️⃣ Upload Students")

uploaded_file = st.file_uploader("Upload a .txt file of student names")

students = []

if uploaded_file:
    students = uploaded_file.read().decode("utf-8").splitlines()
else:
    text_input = st.text_area("Or paste student names (one per line)")
    if text_input:
        students = text_input.splitlines()

if students:
    st.success(f"{len(students)} students loaded.")

# Group Settings
st.header("2️⃣ Group Settings")

col1, col2 = st.columns(2)

with col1:
    number_of_groups = st.number_input("Number of Groups", min_value=1, value=2)

with col2:
    iterations = st.number_input("Optimization Iterations", min_value=1000, value=5000, step=1000)

# Constraints
st.header("3️⃣ Constraints")

together_pairs = []
not_together_pairs = []

if students:

    st.subheader("✅ Work Well Together")
    num_together = st.number_input("How many pairs?", min_value=0, value=0, key="together_count")

    for i in range(num_together):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox(f"Pair {i+1} - Student 1", students, key=f"t1_{i}")
        with col2:
            p2 = st.selectbox(f"Pair {i+1} - Student 2", students, key=f"t2_{i}")
        together_pairs.append((p1, p2))

    st.subheader("❌ Should NOT Work Together")
    num_not = st.number_input("How many pairs?", min_value=0, value=0, key="not_count")

    for i in range(num_not):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox(f"Conflict {i+1} - Student 1", students, key=f"n1_{i}")
        with col2:
            p2 = st.selectbox(f"Conflict {i+1} - Student 2", students, key=f"n2_{i}")
        not_together_pairs.append((p1, p2))

import pandas as pd

# --- Generate Button ---
if students:
    if st.button("🎯 Generate Groups"):
        with st.spinner("Optimizing groups..."):
            groups, _ = find_best_groups(
                iterations,
                students,
                number_of_groups,
                together_pairs,
                not_together_pairs
            )

        # Store results in session state
        st.session_state.generated_groups = groups


# --- Display Results (only if they exist) ---
import streamlit as st
import pandas as pd
import string
import time

# ---------- Apple Style CSS ----------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: -apple-system, BlinkMacSystemFont,
    "SF Pro Display", "SF Pro Text",
    "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.main {
    background: linear-gradient(180deg, #f5f7fa 0%, #e4ecf5 100%);
}

.apple-card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 30px;
    transition: all 0.25s ease;
}

.apple-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}

.group-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.group-title {
    font-size: 20px;
    font-weight: 600;
    margin: 0;
}

.group-badge {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 500;
}

.student-pill {
    background: rgba(0,0,0,0.04);
    padding: 10px 14px;
    border-radius: 14px;
    margin-bottom: 8px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ---------- Generate Button ----------
if students:
    if st.button("✨ Generate Groups"):
        with st.spinner("Optimizing groups..."):
            groups, _ = find_best_groups(
                iterations,
                students,
                number_of_groups,
                together_pairs,
                not_together_pairs
            )
            time.sleep(0.8)

        st.session_state.generated_groups = groups
        st.success("Groups generated successfully")


# ---------- Display Results ----------
if "generated_groups" in st.session_state:

    groups = st.session_state.generated_groups
    st.markdown("## Final Groups")

    group_labels = list(string.ascii_uppercase)
    max_cols = 3
    rows = [groups[i:i+max_cols] for i in range(0, len(groups), max_cols)]

    for row_index, row in enumerate(rows):
        cols = st.columns(len(row))

        for col_index, (col, group) in enumerate(zip(cols, row)):
            group_number = row_index * max_cols + col_index
            label = group_labels[group_number]

            with col:
                st.markdown('<div class="apple-card">', unsafe_allow_html=True)

                st.markdown(f"""
                <div class="group-header">
                    <div class="group-title">Group {label}</div>
                    <div class="group-badge">{len(group)} students</div>
                </div>
                """, unsafe_allow_html=True)

                for student in group:
                    st.markdown(
                        f'<div class="student-pill">{student}</div>',
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)


    # ---------- Download Button ----------
    max_len = max(len(group) for group in groups)
    data = {
        f"Group {group_labels[i]}":
        group + [""] * (max_len - len(group))
        for i, group in enumerate(groups)
    }

    df = pd.DataFrame(data)

    st.download_button(
        "⬇ Download Groups",
        df.to_csv(index=False),
        "groups.csv",
        "text/csv"
    )


    # ---------- Regenerate ----------
    if st.button("🔄 Generate Again"):
        with st.spinner("Re-optimizing groups..."):
            groups, _ = find_best_groups(
                iterations,
                students,
                number_of_groups,
                together_pairs,
                not_together_pairs
            )
            time.sleep(0.6)

        st.session_state.generated_groups = groups
        st.rerun()
