import streamlit as st
import random

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

# Generate Button
if students and st.button("🎯 Generate Groups"):

    groups, score = find_best_groups(
        iterations,
        students,
        number_of_groups,
        together_pairs,
        not_together_pairs
    )

    st.header("📋 Final Groups")

    # Create columns equal to number of groups (max 4 per row for cleanliness)
    max_cols = 4
    rows = [groups[i:i+max_cols] for i in range(0, len(groups), max_cols)]

    for row in rows:
        cols = st.columns(len(row))
        for col, group in zip(cols, row):
            with col:
                st.markdown(
                    """
                    <div style="
                        background-color: #f8f9fa;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    ">
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("### Group")

                for student in group:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #e9ecef;
                            padding: 6px 10px;
                            border-radius: 20px;
                            margin: 4px 0;
                            font-size: 14px;
                        ">
                            {student}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)
