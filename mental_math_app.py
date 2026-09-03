# import streamlit as st
# import random
# import time
# from datetime import datetime
# import pandas as pd

# # Set page config
# st.set_page_config(
#     page_title="Mental Math Master",
#     page_icon="🧮",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
#     <style>
#     .main-header {
#         text-align: center;
#         color: #2E86AB;
#         margin-bottom: 30px;
#     }
#     .score-box {
#         background-color: #A23B72;
#         color: white;
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         font-size: 24px;
#     }
#     .timer-box {
#         background-color: #F18F01;
#         color: white;
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         font-size: 32px;
#         font-weight: bold;
#     }
#     .correct {
#         background-color: #06A77D;
#         color: white;
#         padding: 10px;
#         border-radius: 5px;
#     }
#     .incorrect {
#         background-color: #D62828;
#         color: white;
#         padding: 10px;
#         border-radius: 5px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'problems' not in st.session_state:
#     st.session_state.problems = []
# if 'current_problem_idx' not in st.session_state:
#     st.session_state.current_problem_idx = 0
# if 'score' not in st.session_state:
#     st.session_state.score = 0
# if 'total_questions' not in st.session_state:
#     st.session_state.total_questions = 0
# if 'session_history' not in st.session_state:
#     st.session_state.session_history = []
# if 'session_active' not in st.session_state:
#     st.session_state.session_active = False
# if 'start_time' not in st.session_state:
#     st.session_state.start_time = None
# if 'question_start_time' not in st.session_state:
#     st.session_state.question_start_time = None
# if 'time_per_question' not in st.session_state:
#     st.session_state.time_per_question = None
# if 'submitted_current' not in st.session_state:
#     st.session_state.submitted_current = False
# if 'answer_submitted' not in st.session_state:
#     st.session_state.answer_submitted = {}

# def generate_problem(operation, num_digits):
#     """Generate a random math problem"""
#     min_val = 10 ** (num_digits - 1)
#     max_val = (10 ** num_digits) - 1
    
#     num1 = random.randint(min_val, max_val)
#     num2 = random.randint(min_val, max_val)
    
#     if operation == "Addition":
#         answer = num1 + num2
#         problem = f"{num1} + {num2}"
#     elif operation == "Subtraction":
#         # Ensure positive result
#         if num1 < num2:
#             num1, num2 = num2, num1
#         answer = num1 - num2
#         problem = f"{num1} - {num2}"
#     elif operation == "Multiplication":
#         answer = num1 * num2
#         problem = f"{num1} × {num2}"
#     elif operation == "Division":
#         # Ensure clean division
#         num1 = random.randint(min_val, max_val)
#         num2 = random.randint(2, 9)
#         num1 = num1 * num2  # Make division clean
#         answer = num1 // num2
#         problem = f"{num1} ÷ {num2}"
    
#     return problem, answer

# def generate_session(operations, num_digits, num_questions):
#     """Generate a complete session of problems"""
#     problems = []
#     for _ in range(num_questions):
#         operation = random.choice(operations)
#         problem, answer = generate_problem(operation, num_digits)
#         problems.append({
#             'problem': problem,
#             'answer': answer,
#             'user_answer': None,
#             'is_correct': None,
#             'time_taken': 0
#         })
#     return problems

# def format_time(seconds):
#     """Format seconds to MM:SS"""
#     mins = int(seconds) // 60
#     secs = int(seconds) % 60
#     return f"{mins:02d}:{secs:02d}"

# # Sidebar configuration
# st.sidebar.markdown("# ⚙️ Settings")

# # Session settings
# st.sidebar.markdown("## Session Configuration")
# selected_operations = st.sidebar.multiselect(
#     "Select Operations:",
#     ["Addition", "Subtraction", "Multiplication", "Division"],
#     default=["Addition", "Subtraction"]
# )

# num_digits = st.sidebar.slider(
#     "Number of Digits:",
#     min_value=1,
#     max_value=5,
#     value=2,
#     help="Range of numbers in problems (1-5 digits)"
# )

# num_questions = st.sidebar.slider(
#     "Number of Questions:",
#     min_value=5,
#     max_value=50,
#     value=10,
#     step=5
# )

# timer_duration = st.sidebar.number_input(
#     "Timer Duration per Question (seconds):",
#     min_value=0,
#     max_value=600,
#     value=10,
#     step=5,
#     help="Time limit for each question (0 = no timer)"
# )

# difficulty = st.sidebar.selectbox(
#     "Difficulty Level:",
#     ["Easy (1-2 digits)", "Medium (2-3 digits)", "Hard (3-4 digits)", "Expert (4-5 digits)"]
# )

# # Update num_digits based on difficulty
# difficulty_map = {
#     "Easy (1-2 digits)": 2,
#     "Medium (2-3 digits)": 3,
#     "Hard (3-4 digits)": 4,
#     "Expert (4-5 digits)": 5
# }

# if st.sidebar.checkbox("Use Difficulty Level", value=False):
#     num_digits = difficulty_map[difficulty]

# # Main area
# st.markdown("<h1 class='main-header'>🧮 Mental Math Master</h1>", unsafe_allow_html=True)

# # Session control buttons
# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("🚀 Start Session", use_container_width=True, key="start_btn"):
#         if not selected_operations:
#             st.error("Please select at least one operation!")
#         else:
#             st.session_state.problems = generate_session(
#                 selected_operations, 
#                 num_digits, 
#                 num_questions
#             )
#             st.session_state.current_problem_idx = 0
#             st.session_state.score = 0
#             st.session_state.total_questions = num_questions
#             st.session_state.session_active = True
#             st.session_state.start_time = time.time()
#             st.session_state.question_start_time = time.time()
#             st.session_state.time_per_question = timer_duration if timer_duration > 0 else None
#             st.session_state.submitted_current = False
#             st.session_state.answer_submitted = {}
#             st.rerun()

# with col2:
#     if st.button("🔄 Reset Session", use_container_width=True):
#         st.session_state.session_active = False
#         st.session_state.problems = []
#         st.session_state.score = 0
#         st.session_state.total_questions = 0
#         st.session_state.submitted_current = False
#         st.session_state.answer_submitted = {}
#         st.rerun()

# with col3:
#     if st.button("📊 View Statistics", use_container_width=True):
#         st.session_state.show_stats = not st.session_state.get('show_stats', False)

# # Display session if active
# if st.session_state.session_active and st.session_state.problems:
    
#     # Current problem
#     if st.session_state.current_problem_idx < len(st.session_state.problems):
#         problem = st.session_state.problems[st.session_state.current_problem_idx]
        
#         # Calculate remaining time for current question
#         question_elapsed = time.time() - st.session_state.question_start_time
#         remaining = st.session_state.time_per_question - question_elapsed if st.session_state.time_per_question else None
        
#         # Top metrics
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.markdown(f"<div class='score-box'>Score: {st.session_state.score}/{st.session_state.total_questions}</div>", unsafe_allow_html=True)
        
#         with col2:
#             progress = (st.session_state.current_problem_idx / st.session_state.total_questions) * 100
#             st.markdown(f"<div class='score-box'>Progress: {progress:.0f}%</div>", unsafe_allow_html=True)
        
#         # Timer with auto-refresh
#         timer_placeholder = col3.empty()
#         if st.session_state.time_per_question:
#             if remaining <= 0:
#                 timer_bg_color = "#D62828"
#                 timer_text = "Time's Up!"
#                 timer_placeholder.markdown(f"<div class='timer-box' style='background-color: {timer_bg_color};'>{timer_text}</div>", unsafe_allow_html=True)
                
#                 # Auto-skip to next question
#                 if problem['is_correct'] is None:
#                     problem['user_answer'] = -9999
#                     problem['is_correct'] = False
#                     st.session_state.current_problem_idx += 1
#                     st.session_state.question_start_time = time.time()
#                     time.sleep(0.5)
#                     st.rerun()
#             else:
#                 timer_bg_color = "#D62828" if remaining < 5 else "#F18F01"
#                 timer_text = f"{remaining:.0f}s"
#                 timer_placeholder.markdown(f"<div class='timer-box' style='background-color: {timer_bg_color};'>{timer_text}</div>", unsafe_allow_html=True)
        
#         with col4:
#             accuracy = (st.session_state.score / st.session_state.current_problem_idx * 100) if st.session_state.current_problem_idx > 0 else 0
#             st.markdown(f"<div class='score-box'>Accuracy: {accuracy:.1f}%</div>", unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         st.markdown(f"### Question {st.session_state.current_problem_idx + 1} of {st.session_state.total_questions}")
#         st.markdown(f"## {problem['problem']} = ?", unsafe_allow_html=True)
        
#         # Input columns
#         col1, col2, col3 = st.columns([2, 1, 1])
        
#         # Only show input if not submitted
#         if not st.session_state.submitted_current:
#             with col1:
#                 user_answer_str = st.text_input(
#                     "Your Answer:",
#                     value="",
#                     key=f"answer_{st.session_state.current_problem_idx}",
#                     label_visibility="collapsed",
#                     placeholder="Enter your answer and press Enter or click Submit",
#                     on_change=lambda: handle_enter_key(st.session_state.current_problem_idx, problem)
#                 )
#                 try:
#                     user_answer = int(user_answer_str) if user_answer_str else None
#                 except ValueError:
#                     user_answer = None
            
#             with col2:
#                 if st.button("✓ Submit", use_container_width=True, key=f"submit_btn_{st.session_state.current_problem_idx}"):
#                     if user_answer is not None:
#                         submit_answer(problem, user_answer)
#                     else:
#                         st.error("Please enter a valid number!")
            
#             with col3:
#                 st.empty()
#         else:
#             # Show feedback after submission
#             with col1:
#                 st.empty()
            
#             with col2:
#                 st.empty()
            
#             with col3:
#                 st.empty()
            
#             # Show result
#             st.markdown("---")
#             if problem['is_correct']:
#                 st.markdown("<div class='correct'>✓ Correct! Great job!</div>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"<div class='incorrect'>✗ Incorrect! The correct answer is: {problem['answer']}</div>", unsafe_allow_html=True)
            
#             st.markdown("---")
            
#             # Next button
#             col1, col2, col3 = st.columns([1, 1, 1])
#             with col2:
#                 if st.button("→ Next Question", use_container_width=True, key=f"next_btn_{st.session_state.current_problem_idx}"):
#                     st.session_state.current_problem_idx += 1
#                     st.session_state.submitted_current = False
#                     st.session_state.question_start_time = time.time()
#                     st.rerun()
#     else:
#         # Session complete - show results
#         st.success("🎉 Session Complete!")
#         st.markdown("---")
        
#         total_time = time.time() - st.session_state.start_time
#         accuracy = (st.session_state.score / st.session_state.total_questions) * 100
        
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("Final Score", f"{st.session_state.score}/{st.session_state.total_questions}")
#         with col2:
#             st.metric("Accuracy", f"{accuracy:.1f}%")
#         with col3:
#             st.metric("Total Time", format_time(total_time))
#         with col4:
#             avg_time = total_time / st.session_state.total_questions
#             st.metric("Avg Time/Q", f"{avg_time:.1f}s")
        
#         # Performance emoji
#         if accuracy == 100:
#             st.markdown("## 🏆 Perfect Score! Outstanding!")
#         elif accuracy >= 80:
#             st.markdown("## 🌟 Excellent Performance!")
#         elif accuracy >= 60:
#             st.markdown("## 👍 Good Job! Keep Practicing!")
#         else:
#             st.markdown("## 💪 Don't Give Up! Practice Makes Perfect!")
        
#         # Save to history
#         session_record = {
#             'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
#             'score': f"{st.session_state.score}/{st.session_state.total_questions}",
#             'accuracy': f"{accuracy:.1f}%",
#             'total_time': f"{format_time(total_time)}",
#             'operations': ', '.join(selected_operations),
#             'difficulty': f"{num_digits} digits"
#         }
#         st.session_state.session_history.append(session_record)
        
#         st.markdown("---")
        
#         # Problem review
#         st.markdown("### 📋 Problem Review")
#         for idx, prob in enumerate(st.session_state.problems, 1):
#             if prob['is_correct']:
#                 st.markdown(f"✓ Q{idx}: {prob['problem']} = {prob['answer']} ✓", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"✗ Q{idx}: {prob['problem']} = {prob['answer']} (Your answer: {prob['user_answer'] if prob['user_answer'] != -9999 else 'No Answer'}) ✗", unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         # New session button
#         col1, col2, col3 = st.columns(3)
#         with col2:
#             if st.button("🚀 Start New Session", use_container_width=True, key="new_session_btn"):
#                 st.session_state.session_active = False
#                 st.rerun()

# # Helper functions
# def submit_answer(problem, user_answer):
#     """Submit answer for current problem"""
#     problem['user_answer'] = user_answer
#     problem['is_correct'] = (user_answer == problem['answer'])
#     problem['time_taken'] = time.time() - st.session_state.start_time
    
#     if problem['is_correct']:
#         st.session_state.score += 1
    
#     st.session_state.submitted_current = True
#     st.rerun()

# def handle_enter_key(idx, problem):
#     """Handle Enter key submission"""
#     try:
#         user_answer_str = st.session_state.get(f"answer_{idx}", "")
#         if user_answer_str:
#             user_answer = int(user_answer_str)
#             submit_answer(problem, user_answer)
#     except:
#         pass

# # Statistics section
# if st.session_state.get('show_stats', False) and st.session_state.session_history:
#     st.markdown("---")
#     st.markdown("## 📊 Session Statistics")
    
#     df = pd.DataFrame(st.session_state.session_history)
#     st.dataframe(df, use_container_width=True)
    
#     # Summary stats
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Sessions", len(st.session_state.session_history))
#     with col2:
#         total_score = sum([int(s.split('/')[0]) for s in df['score']])
#         total_max = sum([int(s.split('/')[1]) for s in df['score']])
#         st.metric("Overall Accuracy", f"{(total_score/total_max*100):.1f}%")
#     with col3:
#         st.metric("Sessions Today", len([s for s in st.session_state.session_history if s['date'].split()[0] == datetime.now().strftime("%Y-%m-%d")]))

# # Help section
# with st.expander("❓ How to Use"):
#     st.markdown("""
#     ### Getting Started
#     1. **Configure Settings**: Use the sidebar to select operations, difficulty, and number of questions
#     2. **Set Timer**: Choose time per question (0 = no timer)
#     3. **Start Session**: Click "🚀 Start Session" to begin
#     4. **Solve Problems**: Enter your answer and press Enter or click "✓ Submit"
#     5. **Review**: Click "→ Next Question" to move forward
#     6. **Results**: After completing all questions, view your final results and review all problems
    
#     ### Features
#     - **Multiple Operations**: Addition, Subtraction, Multiplication, Division
#     - **Per-Question Timer**: Set time limit for each question (0 = no timer)
#     - **Difficulty Levels**: Choose based on your skill level (1-5 digits)
#     - **Performance Tracking**: View accuracy and statistics over time
#     - **Problem Review**: See correct answers for all problems after session
#     - **Auto-Skip**: Questions auto-skip when time runs out
    
#     ### Keyboard Shortcuts
#     - **Enter Key**: Submit your answer quickly
#     - **Escape Key**: Can be used to cancel input
    
#     ### Tips for Better Results
#     - Start with easier levels and progress gradually
#     - Practice regularly for consistent improvement
#     - Try timed sessions to improve speed
#     - Focus on accuracy first, then speed
#     """)

# # Footer
# st.markdown("---")
# st.markdown("""
#     <div style='text-align: center; color: gray; font-size: 12px;'>
#     Mental Math Master v2.0 | Keep practicing to improve your skills! 🚀
#     </div>
# """, unsafe_allow_html=True)



import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Mental Math Master",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 30px;
    }
    .score-box {
        background-color: #A23B72;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    .timer-box {
        background-color: #F18F01;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
    }
    .correct {
        background-color: #06A77D;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .incorrect {
        background-color: #D62828;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'problems' not in st.session_state:
    st.session_state.problems = []
if 'current_problem_idx' not in st.session_state:
    st.session_state.current_problem_idx = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'session_history' not in st.session_state:
    st.session_state.session_history = []
if 'session_active' not in st.session_state:
    st.session_state.session_active = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = None
if 'time_per_question' not in st.session_state:
    st.session_state.time_per_question = None
if 'submitted_current' not in st.session_state:
    st.session_state.submitted_current = False

def generate_problem(operation, num_digits):
    """Generate a random math problem"""
    min_val = 10 ** (num_digits - 1)
    max_val = (10 ** num_digits) - 1
    
    num1 = random.randint(min_val, max_val)
    num2 = random.randint(min_val, max_val)
    
    if operation == "Addition":
        answer = num1 + num2
        problem = f"{num1} + {num2}"
    elif operation == "Subtraction":
        # Ensure positive result
        if num1 < num2:
            num1, num2 = num2, num1
        answer = num1 - num2
        problem = f"{num1} - {num2}"
    elif operation == "Multiplication":
        answer = num1 * num2
        problem = f"{num1} × {num2}"
    elif operation == "Division":
        # Ensure clean division
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(2, 9)
        num1 = num1 * num2  # Make division clean
        answer = num1 // num2
        problem = f"{num1} ÷ {num2}"
    
    return problem, answer

def generate_session(operations, num_digits, num_questions):
    """Generate a complete session of problems"""
    problems = []
    for _ in range(num_questions):
        operation = random.choice(operations)
        problem, answer = generate_problem(operation, num_digits)
        problems.append({
            'problem': problem,
            'answer': answer,
            'user_answer': None,
            'is_correct': None,
            'time_taken': 0
        })
    return problems

def format_time(seconds):
    """Format seconds to MM:SS"""
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"

# Sidebar configuration
st.sidebar.markdown("# ⚙️ Settings")

# Session settings
st.sidebar.markdown("## Session Configuration")
selected_operations = st.sidebar.multiselect(
    "Select Operations:",
    ["Addition", "Subtraction", "Multiplication", "Division"],
    default=["Addition", "Subtraction"]
)

num_digits = st.sidebar.slider(
    "Number of Digits:",
    min_value=1,
    max_value=5,
    value=2,
    help="Range of numbers in problems (1-5 digits)"
)

num_questions = st.sidebar.slider(
    "Number of Questions:",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

timer_duration = st.sidebar.number_input(
    "Timer Duration per Question (seconds):",
    min_value=0,
    max_value=600,
    value=10,
    step=5,
    help="Time limit for each question (0 = no timer)"
)

difficulty = st.sidebar.selectbox(
    "Difficulty Level:",
    ["Easy (1-2 digits)", "Medium (2-3 digits)", "Hard (3-4 digits)", "Expert (4-5 digits)"]
)

# Update num_digits based on difficulty
difficulty_map = {
    "Easy (1-2 digits)": 2,
    "Medium (2-3 digits)": 3,
    "Hard (3-4 digits)": 4,
    "Expert (4-5 digits)": 5
}

if st.sidebar.checkbox("Use Difficulty Level", value=False):
    num_digits = difficulty_map[difficulty]

# Main area
st.markdown("<h1 class='main-header'>🧮 Mental Math Master</h1>", unsafe_allow_html=True)

# Session control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Start Session", use_container_width=True, key="start_btn"):
        if not selected_operations:
            st.error("Please select at least one operation!")
        else:
            st.session_state.problems = generate_session(
                selected_operations, 
                num_digits, 
                num_questions
            )
            st.session_state.current_problem_idx = 0
            st.session_state.score = 0
            st.session_state.total_questions = num_questions
            st.session_state.session_active = True
            st.session_state.start_time = time.time()
            st.session_state.question_start_time = time.time()
            st.session_state.time_per_question = timer_duration if timer_duration > 0 else None
            st.session_state.submitted_current = False
            st.rerun()

with col2:
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.session_active = False
        st.session_state.problems = []
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.session_state.submitted_current = False
        st.rerun()

with col3:
    if st.button("📊 View Statistics", use_container_width=True):
        st.session_state.show_stats = not st.session_state.get('show_stats', False)

# Display session if active
if st.session_state.session_active and st.session_state.problems:
    
    # Current problem
    if st.session_state.current_problem_idx < len(st.session_state.problems):
        problem = st.session_state.problems[st.session_state.current_problem_idx]
        
        # Calculate remaining time for current question
        question_elapsed = time.time() - st.session_state.question_start_time
        remaining = st.session_state.time_per_question - question_elapsed if st.session_state.time_per_question else None
        
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"<div class='score-box'>Score: {st.session_state.score}/{st.session_state.total_questions}</div>", unsafe_allow_html=True)
        
        with col2:
            progress = (st.session_state.current_problem_idx / st.session_state.total_questions) * 100
            st.markdown(f"<div class='score-box'>Progress: {progress:.0f}%</div>", unsafe_allow_html=True)
        
        # Timer display
        timer_placeholder = col3.empty()
        if st.session_state.time_per_question:
            if remaining <= 0:
                timer_bg_color = "#D62828"
                timer_text = "Time's Up!"
                timer_placeholder.markdown(f"<div class='timer-box' style='background-color: {timer_bg_color};'>{timer_text}</div>", unsafe_allow_html=True)
                
                # Auto-skip to next question
                if problem['is_correct'] is None:
                    problem['user_answer'] = -9999
                    problem['is_correct'] = False
                    st.session_state.current_problem_idx += 1
                    st.session_state.question_start_time = time.time()
                    st.session_state.submitted_current = False
                    time.sleep(0.5)
                    st.rerun()
            else:
                timer_bg_color = "#D62828" if remaining < 5 else "#F18F01"
                timer_text = f"{remaining:.0f}s"
                timer_placeholder.markdown(f"<div class='timer-box' style='background-color: {timer_bg_color};'>{timer_text}</div>", unsafe_allow_html=True)
        
        with col4:
            accuracy = (st.session_state.score / st.session_state.current_problem_idx * 100) if st.session_state.current_problem_idx > 0 else 0
            st.markdown(f"<div class='score-box'>Accuracy: {accuracy:.1f}%</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"### Question {st.session_state.current_problem_idx + 1} of {st.session_state.total_questions}")
        st.markdown(f"## {problem['problem']} = ?", unsafe_allow_html=True)
        
        # Only show input if not submitted
        if not st.session_state.submitted_current:
            # Input columns
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                user_answer_str = st.text_input(
                    "Your Answer:",
                    value="",
                    key=f"answer_{st.session_state.current_problem_idx}",
                    label_visibility="collapsed",
                    placeholder="Enter your answer and click Submit or press Enter"
                )
                try:
                    user_answer = int(user_answer_str) if user_answer_str else None
                except ValueError:
                    user_answer = None
            
            with col2:
                if st.button("✓ Submit", use_container_width=True, key=f"submit_btn_{st.session_state.current_problem_idx}"):
                    if user_answer is not None:
                        # Submit the answer
                        problem['user_answer'] = user_answer
                        problem['is_correct'] = (user_answer == problem['answer'])
                        problem['time_taken'] = time.time() - st.session_state.start_time
                        
                        if problem['is_correct']:
                            st.session_state.score += 1
                        
                        st.session_state.submitted_current = True
                        st.rerun()
                    else:
                        st.error("Please enter a valid number!")
            
            with col3:
                st.empty()
        else:
            # Show feedback after submission
            st.markdown("---")
            if problem['is_correct']:
                st.markdown("<div class='correct'>✓ Correct! Great job!</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='incorrect'>✗ Incorrect! The correct answer is: {problem['answer']}</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Next button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("→ Next Question", use_container_width=True, key=f"next_btn_{st.session_state.current_problem_idx}"):
                    st.session_state.current_problem_idx += 1
                    st.session_state.submitted_current = False
                    st.session_state.question_start_time = time.time()
                    st.rerun()
    else:
        # Session complete - show results
        st.success("🎉 Session Complete!")
        st.markdown("---")
        
        total_time = time.time() - st.session_state.start_time
        accuracy = (st.session_state.score / st.session_state.total_questions) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Final Score", f"{st.session_state.score}/{st.session_state.total_questions}")
        with col2:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        with col3:
            st.metric("Total Time", format_time(total_time))
        with col4:
            avg_time = total_time / st.session_state.total_questions
            st.metric("Avg Time/Q", f"{avg_time:.1f}s")
        
        # Performance emoji
        if accuracy == 100:
            st.markdown("## 🏆 Perfect Score! Outstanding!")
        elif accuracy >= 80:
            st.markdown("## 🌟 Excellent Performance!")
        elif accuracy >= 60:
            st.markdown("## 👍 Good Job! Keep Practicing!")
        else:
            st.markdown("## 💪 Don't Give Up! Practice Makes Perfect!")
        
        # Save to history
        session_record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'score': f"{st.session_state.score}/{st.session_state.total_questions}",
            'accuracy': f"{accuracy:.1f}%",
            'total_time': f"{format_time(total_time)}",
            'operations': ', '.join(selected_operations),
            'difficulty': f"{num_digits} digits"
        }
        st.session_state.session_history.append(session_record)
        
        st.markdown("---")
        
        # Problem review
        st.markdown("### 📋 Problem Review")
        for idx, prob in enumerate(st.session_state.problems, 1):
            if prob['is_correct']:
                st.markdown(f"✓ Q{idx}: {prob['problem']} = {prob['answer']} ✓", unsafe_allow_html=True)
            else:
                st.markdown(f"✗ Q{idx}: {prob['problem']} = {prob['answer']} (Your answer: {prob['user_answer'] if prob['user_answer'] != -9999 else 'No Answer'}) ✗", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # New session button
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🚀 Start New Session", use_container_width=True, key="new_session_btn"):
                st.session_state.session_active = False
                st.rerun()

# Statistics section
if st.session_state.get('show_stats', False) and st.session_state.session_history:
    st.markdown("---")
    st.markdown("## 📊 Session Statistics")
    
    df = pd.DataFrame(st.session_state.session_history)
    st.dataframe(df, use_container_width=True)
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sessions", len(st.session_state.session_history))
    with col2:
        total_score = sum([int(s.split('/')[0]) for s in df['score']])
        total_max = sum([int(s.split('/')[1]) for s in df['score']])
        st.metric("Overall Accuracy", f"{(total_score/total_max*100):.1f}%")
    with col3:
        st.metric("Sessions Today", len([s for s in st.session_state.session_history if s['date'].split()[0] == datetime.now().strftime("%Y-%m-%d")]))

# Help section
with st.expander("❓ How to Use"):
    st.markdown("""
    ### Getting Started
    1. **Configure Settings**: Use the sidebar to select operations, difficulty, and number of questions
    2. **Set Timer**: Choose time per question (0 = no timer)
    3. **Start Session**: Click "🚀 Start Session" to begin
    4. **Solve Problems**: Enter your answer and click "✓ Submit"
    5. **Review**: Click "→ Next Question" to move forward
    6. **Results**: After completing all questions, view your final results and review all problems
    
    ### Features
    - **Multiple Operations**: Addition, Subtraction, Multiplication, Division
    - **Per-Question Timer**: Set time limit for each question (0 = no timer)
    - **Difficulty Levels**: Choose based on your skill level (1-5 digits)
    - **Performance Tracking**: View accuracy and statistics over time
    - **Problem Review**: See correct answers for all problems after session
    - **Auto-Skip**: Questions auto-skip when time runs out
    
    ### Tips for Better Results
    - Start with easier levels and progress gradually
    - Practice regularly for consistent improvement
    - Try timed sessions to improve speed
    - Focus on accuracy first, then speed
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    Mental Math Master v3.0 | Keep practicing to improve your skills! 🚀
    </div>
""", unsafe_allow_html=True)