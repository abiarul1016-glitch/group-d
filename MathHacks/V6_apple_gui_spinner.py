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

if "generated_groups" not in st.session_state:
    st.session_state.generated_groups = None

import streamlit as st
import random
import time
import string

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="group'd", layout="wide")

# -------------------------------------------------
# BRAND STYLE
# -------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: -apple-system, BlinkMacSystemFont,
    "SF Pro Display", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.main {
    background: linear-gradient(135deg, #f4f8f6 0%, #e8f5ef 100%);
}

.brand {
    font-size: 48px;
    font-weight: 700;
    color: #30D158;
    letter-spacing: -1px;
}

.subtitle {
    color: #6b7280;
    margin-bottom: 40px;
}

.card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

.group-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown('<div class="brand">group\'d</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Balanced classroom groups, beautifully generated.</div>', unsafe_allow_html=True)

# -------------------------------------------------
# STUDENTS INPUT
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
students_input = st.text_area("Paste student names (one per line)")
students = students_input.splitlines() if students_input else []
st.markdown('</div>', unsafe_allow_html=True)

if students:

    # -------------------------------------------------
    # GROUP SETTINGS
    # -------------------------------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    number_of_groups = st.number_input("Number of Groups", min_value=1, value=2)

    st.subheader("Works Well Together")
    together_count = st.number_input("How many pairs?", min_value=0, value=0, key="together")

    together_pairs = []
    for i in range(together_count):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox(f"Pair {i+1} - Student 1", students, key=f"t1_{i}")
        with col2:
            p2 = st.selectbox(f"Pair {i+1} - Student 2", students, key=f"t2_{i}")
        together_pairs.append((p1, p2))

    st.subheader("Should NOT Work Together")
    not_count = st.number_input("How many pairs?", min_value=0, value=0, key="not")

    not_pairs = []
    for i in range(not_count):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox(f"Conflict {i+1} - Student 1", students, key=f"n1_{i}")
        with col2:
            p2 = st.selectbox(f"Conflict {i+1} - Student 2", students, key=f"n2_{i}")
        not_pairs.append((p1, p2))

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------
    # GENERATE BUTTON
    # -------------------------------------------------
    if st.button("✨ Create Groups"):

        animation_placeholder = st.empty()

        # -------------------------------------------------
        # CRYPTEX ANIMATION
        # -------------------------------------------------
        import string
        import random
        import time

        animation_placeholder = st.empty()

        group_labels = list(string.ascii_uppercase[:number_of_groups])

        # Speed curve (fast → slow)
        frames = 25
        for frame in range(frames):

            with animation_placeholder.container():
                st.markdown("## Generating Groups")

                cols = st.columns(number_of_groups)

                for i, col in enumerate(cols):
                    with col:
                        # Random letter spin
                        random_letter = random.choice(string.ascii_uppercase)
                        st.markdown(
                            f"""
                            <div style="
                                font-size: 48px;
                                font-weight: 700;
                                text-align:center;
                                color:#30D158;
                                letter-spacing:4px;
                            ">
                                {random_letter}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # Slow down gradually
            time.sleep(0.02 + frame * 0.01)

        # Lock into final letters
        with animation_placeholder.container():
            cols = st.columns(number_of_groups)
            for i, col in enumerate(cols):
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            font-size: 48px;
                            font-weight: 700;
                            text-align:center;
                            color:#30D158;
                            letter-spacing:4px;
                            text-shadow: 0 0 12px rgba(48,209,88,0.7);
                        ">
                            {group_labels[i]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        time.sleep(0.6)
        animation_placeholder.empty()

        # FINAL DISPLAY
        st.markdown("## Final Groups")

        cols = st.columns(len(groups))

        for i, (col, group) in enumerate(zip(cols, groups)):
            with col:
                st.markdown('<div class="group-card">', unsafe_allow_html=True)
                st.markdown(f"### Group {string.ascii_uppercase[i]}")
                for student in group:
                    st.write(student)
                st.markdown('</div>', unsafe_allow_html=True)
