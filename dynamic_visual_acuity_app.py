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
if 'current_trial' not in st.session_state:
    st.session_state.current_trial = 0
if 'waiting_for_click' not in st.session_state:
    st.session_state.waiting_for_click = False
if 'target_start_time' not in st.session_state:
    st.session_state.target_start_time = None
if 'moving_target_score' not in st.session_state:
    st.session_state.moving_target_score = 0
if 'moving_target_trials' not in st.session_state:
    st.session_state.moving_target_trials = 0
if 'moving_target_phase' not in st.session_state:
    st.session_state.moving_target_phase = False
if 'test_complete' not in st.session_state:
    st.session_state.test_complete = False

# Configuration
NUM_TRIALS = 5  # Number of reaction time trials
NUM_MOVING_TARGETS = 8  # Number of moving target trials
MIN_DELAY = 1.0  # Minimum delay in seconds before target appears
MAX_DELAY = 3.0  # Maximum delay in seconds before target appears

# ============================================================================
# SECTION 1: INTRODUCTION
# ============================================================================

st.title("🎯 Dynamic Visual Acuity Training & Testing")

st.write("""
Welcome to the **Dynamic Visual Acuity Test**! This application measures your ability to
quickly react to visual stimuli, which is an important component of dynamic visual acuity.

### How the test works:
1. **Reaction Time Test**: You will complete 5 trials where a target button will appear
   after a random delay. Click the target as quickly as possible when it appears.
2. **Moving Target Test**: After the reaction test, targets will appear in random positions.
   Try to click as many as you can!
3. **Results**: You'll see your reaction times, average performance, and how you compare
   to baseline values.

**Ready to test your visual reflexes? Click the button below to begin!**
""")

# ============================================================================
# SECTION 2: TRAINING/TEST SECTION
# ============================================================================

st.header("🏁 Test Area")

# Function to reset the test
def reset_test():
    st.session_state.test_started = False
    st.session_state.reaction_times = []
    st.session_state.current_trial = 0
    st.session_state.waiting_for_click = False
    st.session_state.target_start_time = None
    st.session_state.moving_target_score = 0
    st.session_state.moving_target_trials = 0
    st.session_state.moving_target_phase = False
    st.session_state.test_complete = False

# Start Test Button
if not st.session_state.test_started and not st.session_state.test_complete:
    if st.button("🚀 Start Test", type="primary", use_container_width=True):
        st.session_state.test_started = True
        st.session_state.current_trial = 0
        st.session_state.reaction_times = []
        st.rerun()

# Reaction Time Test Logic
if st.session_state.test_started and not st.session_state.test_complete:

    # Phase 1: Reaction Time Trials
    if not st.session_state.moving_target_phase:

        if st.session_state.current_trial < NUM_TRIALS:
            st.subheader(f"Trial {st.session_state.current_trial + 1} of {NUM_TRIALS}")
            st.write("⏳ Get ready... The target will appear shortly!")

            # Create placeholder for the target button
            target_placeholder = st.empty()

            # If not waiting for click, show preparation phase
            if not st.session_state.waiting_for_click:
                # Random delay before showing target
                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                time.sleep(delay)

                # Now show the target and record start time
                st.session_state.waiting_for_click = True
                st.session_state.target_start_time = time.time()
                st.rerun()

            # Display the target button and wait for click
            if st.session_state.waiting_for_click:
                with target_placeholder.container():
                    st.write("### 🎯 TARGET APPEARED! CLICK NOW! 👇")
                    if st.button("⚡ CLICK ME! ⚡", type="primary", key=f"target_{st.session_state.current_trial}", use_container_width=True):
                        # Calculate reaction time in milliseconds
                        reaction_time = (time.time() - st.session_state.target_start_time) * 1000
                        st.session_state.reaction_times.append(reaction_time)

                        # Reset for next trial
                        st.session_state.waiting_for_click = False
                        st.session_state.current_trial += 1

                        # Show feedback
                        st.success(f"✅ Reaction time: {reaction_time:.0f} ms")
                        time.sleep(0.5)
                        st.rerun()

        else:
            # Transition to moving target phase
            st.session_state.moving_target_phase = True
            st.rerun()

    # Phase 2: Moving Target Test
    else:
        if st.session_state.moving_target_trials < NUM_MOVING_TARGETS:
            st.subheader(f"Moving Target Trial {st.session_state.moving_target_trials + 1} of {NUM_MOVING_TARGETS}")
            st.write("🎯 Click the target that appears in random positions!")

            # Create random columns layout (target appears in random position)
            num_columns = 5
            columns = st.columns(num_columns)
            target_position = random.randint(0, num_columns - 1)

            # Record start time for moving target
            if st.session_state.target_start_time is None:
                st.session_state.target_start_time = time.time()

            # Display buttons in columns, with target in random position
            for i, col in enumerate(columns):
                with col:
                    if i == target_position:
                        # This is the target button
                        if st.button("🎯 HIT!", key=f"moving_{st.session_state.moving_target_trials}_{i}", type="primary"):
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
                        # Decoy button
                        if st.button("❌", key=f"decoy_{st.session_state.moving_target_trials}_{i}"):
                            # Wrong button clicked
                            st.session_state.moving_target_trials += 1
                            st.session_state.target_start_time = None
                            st.error("❌ Missed!")
                            time.sleep(0.3)
                            st.rerun()

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

    # Calculate statistics for reaction time trials (first NUM_TRIALS)
    reaction_trial_times = st.session_state.reaction_times[:NUM_TRIALS]
    moving_target_times = st.session_state.reaction_times[NUM_TRIALS:]

    avg_reaction_time = sum(reaction_trial_times) / len(reaction_trial_times)
    best_reaction_time = min(reaction_trial_times)

    # Display key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Average Reaction Time",
            value=f"{avg_reaction_time:.0f} ms"
        )

    with col2:
        st.metric(
            label="Best Reaction Time",
            value=f"{best_reaction_time:.0f} ms"
        )

    with col3:
        st.metric(
            label="Moving Targets Hit",
            value=f"{st.session_state.moving_target_score}/{NUM_MOVING_TARGETS}"
        )

    # Additional moving target statistics
    if len(moving_target_times) > 0:
        avg_moving_target_time = sum(moving_target_times) / len(moving_target_times)
        accuracy = (st.session_state.moving_target_score / NUM_MOVING_TARGETS) * 100

        col4, col5 = st.columns(2)
        with col4:
            st.metric(
                label="Avg Moving Target Time",
                value=f"{avg_moving_target_time:.0f} ms"
            )
        with col5:
            st.metric(
                label="Accuracy",
                value=f"{accuracy:.0f}%"
            )

    # Visualize reaction times across trials
    st.subheader("Reaction Times per Trial")

    # Create DataFrame for visualization
    trial_data = pd.DataFrame({
        'Trial': [f"Trial {i+1}" for i in range(len(reaction_trial_times))],
        'Reaction Time (ms)': reaction_trial_times
    })

    # Display as bar chart
    st.bar_chart(trial_data.set_index('Trial'))

    # Also show as line chart to see trend
    st.line_chart(trial_data.set_index('Trial'))

    # ============================================================================
    # SECTION 4: COMPARISON WITH BASELINE VALUES
    # ============================================================================

    st.header("📈 Performance Comparison")

    st.write("""
    Let's see how your performance compares to typical baseline values:
    - **Average Person**: ~250 ms reaction time
    - **Athlete**: ~200 ms reaction time
    - **Your Performance**: How do you stack up?
    """)

    # Create comparison DataFrame
    comparison_data = pd.DataFrame({
        'Category': ['Your Average', 'Average Person', 'Athlete'],
        'Reaction Time (ms)': [avg_reaction_time, 250, 200]
    })

    # Display comparison as bar chart
    st.subheader("Reaction Time Comparison")
    st.bar_chart(comparison_data.set_index('Category'))

    # Provide personalized feedback
    st.subheader("💡 Feedback")

    if avg_reaction_time < 200:
        st.success("🏆 **Outstanding!** Your reaction time is at an elite athlete level!")
    elif avg_reaction_time < 250:
        st.success("🎖️ **Excellent!** Your reaction time is better than average!")
    elif avg_reaction_time < 300:
        st.info("👍 **Good!** Your reaction time is around the average range.")
    else:
        st.warning("💪 **Keep practicing!** With training, you can improve your reaction time.")

    # Moving target feedback
    if st.session_state.moving_target_score >= NUM_MOVING_TARGETS * 0.8:
        st.success(f"🎯 **Excellent tracking ability!** You hit {st.session_state.moving_target_score} out of {NUM_MOVING_TARGETS} moving targets!")
    elif st.session_state.moving_target_score >= NUM_MOVING_TARGETS * 0.6:
        st.info(f"👍 **Good tracking!** You hit {st.session_state.moving_target_score} out of {NUM_MOVING_TARGETS} moving targets.")
    else:
        st.warning(f"💪 **Keep practicing!** You hit {st.session_state.moving_target_score} out of {NUM_MOVING_TARGETS} moving targets. Try to improve your spatial awareness!")

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
