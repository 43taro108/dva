import streamlit as st
import time
import random
import pandas as pd

# ============================================================================
# STREAMLIT APP: DYNAMIC VISUAL ACUITY TRAINING AND TESTING
# ============================================================================

# Language texts dictionary
TEXTS = {
    'ja': {
        'title': '🎯 動的視力トレーニング＆テスト',
        'intro': """
**動的視力テスト**へようこそ！このアプリケーションは、広い視野範囲での視覚刺激を素早く
追跡し反応する能力を測定します。現実世界で目を動かして物体を追跡する場面を想定しています。

### テストの流れ:
1. **移動ターゲットテスト**: 画面上の6×6グリッド（36マス）にランダムな位置でターゲットが表示されます。
   目を動かして、できるだけ素早くターゲットをクリックしてください！
2. **15回のトライアル**を実施します。各トライアルでターゲットは異なる位置に表示されます。
3. **結果**: 反応時間、正確性、パフォーマンス指標を確認できます。

**動的視力をテストする準備はできましたか？下のボタンをクリックして開始しましょう！**
        """,
        'test_area': '🏁 テストエリア',
        'start_test': '🚀 テスト開始',
        'trial_of': 'トライアル',
        'instruction': '🎯 ターゲット（🎯）をできるだけ速くクリックしてください！画面全体に目を動かしましょう！',
        'hit': 'ヒット！',
        'missed': '外れ！',
        'results': '📊 テスト結果',
        'targets_hit': 'ヒット数',
        'accuracy': '正確性',
        'avg_reaction_time': '平均反応時間',
        'best_time': '最速タイム',
        'slowest_time': '最遅タイム',
        'reaction_times_chart': 'トライアルごとの反応時間',
        'trial': 'トライアル',
        'performance_eval': '📈 パフォーマンス評価',
        'eval_intro': """
動的視力のパフォーマンスを評価しましょう：
- **正確性**: いくつのターゲットを正確にヒットできましたか？
- **スピード**: 広い視野範囲でどれだけ素早く反応できましたか？
- **一貫性**: 反応時間はどれだけ安定していましたか？
        """,
        'performance_feedback': '💡 パフォーマンスフィードバック',
        'feedback_outstanding': '🏆 **素晴らしい！** あなたの動的視力は優れています！広い視野でターゲットを追跡し反応する能力が卓越しています。',
        'feedback_excellent': '🎖️ **素晴らしい！** あなたの動的視力は平均以上です。移動するターゲットを効果的に追跡できています。',
        'feedback_good': '👍 **良好！** パフォーマンスは良好です。さらに練習することで追跡能力を向上できます。',
        'feedback_practice': '💪 **練習を続けましょう！** 動的視力は定期的なトレーニングで向上します。目を素早く滑らかに動かすことに集中しましょう。',
        'speed_analysis': '⚡ スピード分析',
        'speed_fast': f'🚀 **速い！** 平均反応時間が',
        'speed_fast_end': 'msで、視野全体での素早い眼球運動と反応を示しています。',
        'speed_moderate': f'⏱️ **標準的なスピード。** 平均',
        'speed_moderate_end': 'msは妥当です。ターゲットをより速く見つけられるようにしましょう！',
        'speed_slow': f'🐢 **改善の余地あり。** 平均',
        'speed_slow_end': 'msは、ターゲット捕捉の速度向上が必要です。',
        'consistency_analysis': '📊 一貫性分析',
        'consistency_good': f'📊 **一貫している！** 反応時間の変動は',
        'consistency_good_end': 'msのみです。素晴らしい一貫性！',
        'consistency_fair': f'📊 **まあまあの一貫性。** 時間変動',
        'consistency_fair_end': 'msは、より一貫性を高める余地があります。',
        'consistency_poor': f'📊 **一貫性が低い。** 大きな変動',
        'consistency_poor_end': 'ms。安定したパフォーマンスを維持するようにしましょう。',
        'retry_test': '🔄 テストを再実行',
        'footer': '💡 ヒント: 定期的な練習で動的視力と反応時間を向上できます！',
        'language': '言語 / Language'
    },
    'en': {
        'title': '🎯 Dynamic Visual Acuity Training & Testing',
        'intro': """
Welcome to the **Dynamic Visual Acuity Test**! This application measures your ability to
quickly track and react to visual stimuli across a wide field of view, simulating real-world
scenarios where you need to move your eyes to track moving objects.

### How the test works:
1. **Moving Target Test**: Targets will appear in random positions across a 6×6 grid (36 cells) on your screen.
   Move your eyes and click the targets as quickly as possible!
2. You will complete **15 trials**. Each target appears in a different location.
3. **Results**: You'll see your reaction times, accuracy, and performance metrics.

**Ready to test your dynamic visual acuity? Click the button below to begin!**
        """,
        'test_area': '🏁 Test Area',
        'start_test': '🚀 Start Test',
        'trial_of': 'Trial',
        'instruction': '🎯 Click the target (🎯) as quickly as you can! Move your eyes across the screen!',
        'hit': 'Hit!',
        'missed': 'Missed!',
        'results': '📊 Your Results',
        'targets_hit': 'Targets Hit',
        'accuracy': 'Accuracy',
        'avg_reaction_time': 'Average Reaction Time',
        'best_time': 'Best Time',
        'slowest_time': 'Slowest Time',
        'reaction_times_chart': 'Reaction Times per Trial',
        'trial': 'Trial',
        'performance_eval': '📈 Performance Evaluation',
        'eval_intro': """
Let's evaluate your dynamic visual acuity performance:
- **Accuracy**: How many targets did you successfully hit?
- **Speed**: How quickly did you respond across a wide field of view?
- **Consistency**: How consistent were your reaction times?
        """,
        'performance_feedback': '💡 Performance Feedback',
        'feedback_outstanding': '🏆 **Outstanding!** You have excellent dynamic visual acuity! Your ability to track and respond to targets across a wide field is exceptional.',
        'feedback_excellent': '🎖️ **Excellent!** Your dynamic visual acuity is above average. You\'re able to track moving targets effectively.',
        'feedback_good': '👍 **Good!** Your performance is solid. With more practice, you can improve your tracking ability.',
        'feedback_practice': '💪 **Keep practicing!** Dynamic visual acuity can be improved with regular training. Focus on moving your eyes quickly and smoothly.',
        'speed_analysis': '⚡ Speed Analysis',
        'speed_fast': '🚀 **Fast!** Your average reaction time of ',
        'speed_fast_end': 'ms shows quick eye movement and response across the field.',
        'speed_moderate': '⏱️ **Moderate speed.** Your average of ',
        'speed_moderate_end': 'ms is reasonable. Try to locate targets faster!',
        'speed_slow': '🐢 **Room for improvement.** Average of ',
        'speed_slow_end': 'ms suggests you can work on faster target acquisition.',
        'consistency_analysis': '📊 Consistency Analysis',
        'consistency_good': '📊 **Consistent!** Your times varied by only ',
        'consistency_good_end': 'ms. Great consistency!',
        'consistency_fair': '📊 **Fairly consistent.** Time variation of ',
        'consistency_fair_end': 'ms shows room for more consistency.',
        'consistency_poor': '📊 **Inconsistent.** Large variation of ',
        'consistency_poor_end': 'ms. Try to maintain steady performance.',
        'retry_test': '🔄 Retry Test',
        'footer': '💡 Tip: Regular practice can improve your dynamic visual acuity and reaction times!',
        'language': '言語 / Language'
    }
}

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
if 'language' not in st.session_state:
    st.session_state.language = 'ja'  # Default to Japanese

# Configuration
NUM_MOVING_TARGETS = 15  # Number of moving target trials (fixed)
GRID_ROWS = 6  # Number of rows in the grid
GRID_COLS = 6  # Number of columns in the grid

# ============================================================================
# SIDEBAR: LANGUAGE SELECTION
# ============================================================================

with st.sidebar:
    st.header(TEXTS[st.session_state.language]['language'])
    language = st.selectbox(
        "",
        options=['ja', 'en'],
        format_func=lambda x: '日本語' if x == 'ja' else 'English',
        index=0 if st.session_state.language == 'ja' else 1,
        key='language_selector'
    )

    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

# Get current language texts
t = TEXTS[st.session_state.language]

# ============================================================================
# SECTION 1: INTRODUCTION
# ============================================================================

st.title(t['title'])
st.write(t['intro'])

# ============================================================================
# SECTION 2: TRAINING/TEST SECTION
# ============================================================================

st.header(t['test_area'])

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
    if st.button(t['start_test'], type="primary", use_container_width=True):
        st.session_state.test_started = True
        st.session_state.reaction_times = []
        st.session_state.moving_target_trials = 0
        st.session_state.moving_target_score = 0
        st.rerun()

# Moving Target Test Logic
if st.session_state.test_started and not st.session_state.test_complete:

    if st.session_state.moving_target_trials < NUM_MOVING_TARGETS:
        st.subheader(f"{t['trial_of']} {st.session_state.moving_target_trials + 1}/{NUM_MOVING_TARGETS}")
        st.write(t['instruction'])

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
                            st.success(f"✅ {t['hit']} ({reaction_time:.0f} ms)")
                            time.sleep(0.3)
                            st.rerun()
                    else:
                        # Decoy button (empty/blank)
                        if st.button("⬜", key=f"decoy_{st.session_state.moving_target_trials}_{position_index}",
                                    use_container_width=True):
                            # Wrong button clicked
                            st.session_state.moving_target_trials += 1
                            st.session_state.target_start_time = None
                            st.error(f"❌ {t['missed']}")
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

    st.header(t['results'])

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
            label=t['targets_hit'],
            value=f"{st.session_state.moving_target_score}/{NUM_MOVING_TARGETS}"
        )

    with col2:
        st.metric(
            label=t['accuracy'],
            value=f"{accuracy:.0f}%"
        )

    with col3:
        st.metric(
            label=t['avg_reaction_time'],
            value=f"{avg_reaction_time:.0f} ms"
        )

    # Additional statistics
    col4, col5 = st.columns(2)
    with col4:
        st.metric(
            label=t['best_time'],
            value=f"{best_reaction_time:.0f} ms"
        )
    with col5:
        st.metric(
            label=t['slowest_time'],
            value=f"{worst_reaction_time:.0f} ms"
        )

    # Visualize reaction times across trials
    st.subheader(t['reaction_times_chart'])

    # Create DataFrame for visualization
    trial_data = pd.DataFrame({
        t['trial']: [f"{t['trial']} {i+1}" for i in range(len(all_reaction_times))],
        'Reaction Time (ms)': all_reaction_times
    })

    # Display as bar chart
    st.bar_chart(trial_data.set_index(t['trial']))

    # Also show as line chart to see trend
    st.line_chart(trial_data.set_index(t['trial']))

    # ============================================================================
    # SECTION 4: PERFORMANCE EVALUATION
    # ============================================================================

    st.header(t['performance_eval'])
    st.write(t['eval_intro'])

    # Provide personalized feedback based on accuracy
    st.subheader(t['performance_feedback'])

    if accuracy >= 90:
        st.success(t['feedback_outstanding'])
    elif accuracy >= 75:
        st.success(t['feedback_excellent'])
    elif accuracy >= 60:
        st.info(t['feedback_good'])
    else:
        st.warning(t['feedback_practice'])

    # Speed feedback
    st.subheader(t['speed_analysis'])
    if avg_reaction_time < 400:
        st.success(f"{t['speed_fast']}{avg_reaction_time:.0f}{t['speed_fast_end']}")
    elif avg_reaction_time < 600:
        st.info(f"{t['speed_moderate']}{avg_reaction_time:.0f}{t['speed_moderate_end']}")
    else:
        st.warning(f"{t['speed_slow']}{avg_reaction_time:.0f}{t['speed_slow_end']}")

    # Consistency analysis
    time_range = worst_reaction_time - best_reaction_time
    st.subheader(t['consistency_analysis'])
    if time_range < 300:
        st.success(f"{t['consistency_good']}{time_range:.0f}{t['consistency_good_end']}")
    elif time_range < 600:
        st.info(f"{t['consistency_fair']}{time_range:.0f}{t['consistency_fair_end']}")
    else:
        st.warning(f"{t['consistency_poor']}{time_range:.0f}{t['consistency_poor_end']}")

    # ============================================================================
    # RETRY BUTTON
    # ============================================================================

    st.write("---")

    if st.button(t['retry_test'], type="primary", use_container_width=True):
        reset_test()
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.write("---")
st.caption(t['footer'])
