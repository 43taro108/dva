import streamlit as st
import time
import random
import pandas as pd

# ============================================================================
# STREAMLIT APP: DYNAMIC VISUAL ACUITY TRAINING AND TESTING
# ============================================================================

# Initialize session state variables to persist data across reruns
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'reaction_times' not in st.session_state:
    st.session_state.reaction_times = []
if 'target_start_time' not in st.session_state:
    st.session_state.target_start_time = None
if 'moving_target_score' not in st.session_state:
    st.session_state.moving_target_score = 0
if 'moving_target_trials' not in st.session_state:
    st.session_state.moving_target_trials = 0
if 'test_complete' not in st.session_state:
    st.session_state.test_complete = False

# Configuration
NUM_MOVING_TARGETS = 15  # Number of moving target trials
GRID_ROWS = 3  # Number of rows in the grid
GRID_COLS = 6  # Number of columns in the grid

# ============================================================================
# SECTION 1: INTRODUCTION
# ============================================================================

st.title("🎯 Dynamic Visual Acuity Training & Testing")

st.write("""
Welcome to the **Dynamic Visual Acuity Test**! This application measures your ability to
quickly track and react to visual stimuli across a wide field of view, simulating real-world
scenarios where you need to move your eyes to track moving objects.

### How the test works:
1. **Moving Target Test**: Targets will appear in random positions across a wide grid on your screen.
   Move your eyes and click the targets as quickly as possible!
2. You will complete 15 trials where each target appears in a different location.
3. **Results**: You'll see your reaction times, accuracy, and performance metrics.

**Ready to test your dynamic visual acuity? Click the button below to begin!**
""")

# ============================================================================
# SECTION 2: TRAINING/TEST SECTION
# ============================================================================

st.header("🏁 Test Area")

# Function to reset the test
def reset_test():
    st.session_state.test_started = False
    st.session_state.reaction_times = []
    st.session_state.target_start_time = None
    st.session_state.moving_target_score = 0
    st.session_state.moving_target_trials = 0
    st.session_state.test_complete = False

# Start Test Button
if not st.session_state.test_started and not st.session_state.test_complete:
    if st.button("🚀 Start Test", type="primary", use_container_width=True):
        st.session_state.test_started = True
        st.session_state.reaction_times = []
        st.session_state.moving_target_trials = 0
        st.session_state.moving_target_score = 0
        st.rerun()

# Moving Target Test Logic
if st.session_state.test_started and not st.session_state.test_complete:

    if st.session_state.moving_target_trials < NUM_MOVING_TARGETS:
        st.subheader(f"Trial {st.session_state.moving_target_trials + 1} of {NUM_MOVING_TARGETS}")
        st.write("🎯 Click the target (🎯) as quickly as you can! Move your eyes across the screen!")

        # Record start time for moving target
        if st.session_state.target_start_time is None:
            st.session_state.target_start_time = time.time()

        # Create a wide grid layout (multiple rows and columns)
        total_positions = GRID_ROWS * GRID_COLS
        target_position = random.randint(0, total_positions - 1)

        # Create grid with multiple rows
        position_index = 0
        for row in range(GRID_ROWS):
            columns = st.columns(GRID_COLS)

            for col_idx, col in enumerate(columns):
                with col:
                    if position_index == target_position:
                        # This is the target button
                        if st.button("🎯", key=f"target_{st.session_state.moving_target_trials}_{position_index}",
                                    type="primary", use_container_width=True):
                            # Target hit! Record reaction time
                            reaction_time = (time.time() - st.session_state.target_start_time) * 1000
                            st.session_state.reaction_times.append(reaction_time)
                            st.session_state.moving_target_score += 1
                            st.session_state.moving_target_trials += 1
                            st.session_state.target_start_time = None
                            st.success(f"✅ Hit! ({reaction_time:.0f} ms)")
                            time.sleep(0.3)
                            st.rerun()
                    else:
                        # Decoy button (empty/blank)
                        if st.button("⬜", key=f"decoy_{st.session_state.moving_target_trials}_{position_index}",
                                    use_container_width=True):
                            # Wrong button clicked
                            st.session_state.moving_target_trials += 1
                            st.session_state.target_start_time = None
                            st.error("❌ Missed!")
                            time.sleep(0.3)
                            st.rerun()

                    position_index += 1

    else:
        # Test complete!
        st.session_state.test_complete = True
        st.session_state.test_started = False
        st.rerun()

# ============================================================================
# SECTION 3: RESULTS DISPLAY
# ============================================================================

if st.session_state.test_complete and len(st.session_state.reaction_times) > 0:

    st.header("📊 Your Results")

    # Calculate statistics for all trials
    all_reaction_times = st.session_state.reaction_times
    avg_reaction_time = sum(all_reaction_times) / len(all_reaction_times)
    best_reaction_time = min(all_reaction_times)
    worst_reaction_time = max(all_reaction_times)
    accuracy = (st.session_state.moving_target_score / NUM_MOVING_TARGETS) * 100

    # Display key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Targets Hit",
            value=f"{st.session_state.moving_target_score}/{NUM_MOVING_TARGETS}"
        )

    with col2:
        st.metric(
            label="Accuracy",
            value=f"{accuracy:.0f}%"
        )

    with col3:
        st.metric(
            label="Average Reaction Time",
            value=f"{avg_reaction_time:.0f} ms"
        )

    # Additional statistics
    col4, col5 = st.columns(2)
    with col4:
        st.metric(
            label="Best Time",
            value=f"{best_reaction_time:.0f} ms"
        )
    with col5:
        st.metric(
            label="Slowest Time",
            value=f"{worst_reaction_time:.0f} ms"
        )

    # Visualize reaction times across trials
    st.subheader("Reaction Times per Trial")

    # Create DataFrame for visualization
    trial_data = pd.DataFrame({
        'Trial': [f"Trial {i+1}" for i in range(len(all_reaction_times))],
        'Reaction Time (ms)': all_reaction_times
    })

    # Display as bar chart
    st.bar_chart(trial_data.set_index('Trial'))

    # Also show as line chart to see trend
    st.line_chart(trial_data.set_index('Trial'))

    # ============================================================================
    # SECTION 4: COMPARISON WITH BASELINE VALUES
    # ============================================================================

    st.header("📈 Performance Evaluation")

    st.write("""
    Let's evaluate your dynamic visual acuity performance:
    - **Accuracy**: How many targets did you successfully hit?
    - **Speed**: How quickly did you respond across a wide field of view?
    - **Consistency**: How consistent were your reaction times?
    """)

    # Provide personalized feedback based on accuracy
    st.subheader("💡 Performance Feedback")

    if accuracy >= 90:
        st.success("🏆 **Outstanding!** You have excellent dynamic visual acuity! Your ability to track and respond to targets across a wide field is exceptional.")
    elif accuracy >= 75:
        st.success("🎖️ **Excellent!** Your dynamic visual acuity is above average. You're able to track moving targets effectively.")
    elif accuracy >= 60:
        st.info("👍 **Good!** Your performance is solid. With more practice, you can improve your tracking ability.")
    else:
        st.warning("💪 **Keep practicing!** Dynamic visual acuity can be improved with regular training. Focus on moving your eyes quickly and smoothly.")

    # Speed feedback
    st.subheader("⚡ Speed Analysis")
    if avg_reaction_time < 400:
        st.success(f"🚀 **Fast!** Your average reaction time of {avg_reaction_time:.0f}ms shows quick eye movement and response across the field.")
    elif avg_reaction_time < 600:
        st.info(f"⏱️ **Moderate speed.** Your average of {avg_reaction_time:.0f}ms is reasonable. Try to locate targets faster!")
    else:
        st.warning(f"🐢 **Room for improvement.** Average of {avg_reaction_time:.0f}ms suggests you can work on faster target acquisition.")

    # Consistency analysis
    time_range = worst_reaction_time - best_reaction_time
    if time_range < 300:
        st.success(f"📊 **Consistent!** Your times varied by only {time_range:.0f}ms. Great consistency!")
    elif time_range < 600:
        st.info(f"📊 **Fairly consistent.** Time variation of {time_range:.0f}ms shows room for more consistency.")
    else:
        st.warning(f"📊 **Inconsistent.** Large variation of {time_range:.0f}ms. Try to maintain steady performance.")

    # ============================================================================
    # RETRY BUTTON
    # ============================================================================

    st.write("---")

    if st.button("🔄 Retry Test", type="primary", use_container_width=True):
        reset_test()
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.write("---")
st.caption("💡 Tip: Regular practice can improve your dynamic visual acuity and reaction times!")
