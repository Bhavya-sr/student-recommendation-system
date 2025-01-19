import pandas as pd
import matplotlib.pyplot as plt
import ast

# Load dataset
file_path = "student_quiz_performance.csv"
quiz_data = pd.read_csv(file_path)

# Standardize column names (strip spaces, lowercase)
quiz_data.columns = quiz_data.columns.str.strip().str.lower()

# Function to safely convert string representation of dictionary to actual dictionary
def parse_dict_column(column_data):
    try:
        return column_data.apply(ast.literal_eval)
    except (ValueError, SyntaxError):
        print(f"Error parsing column: {column_data.name}")
        return None

quiz_data['parsed_response_map'] = parse_dict_column(quiz_data['response_map'])

quiz_data['parsed_quiz'] = parse_dict_column(quiz_data['quiz'])

quiz_data['quiz_title'] = quiz_data['parsed_quiz'].apply(lambda x: x.get('title') if isinstance(x, dict) else None)

# --- Step 1: Analyze Performance by Difficulty Level ---
if 'difficulty' in quiz_data.columns:
    avg_score_by_difficulty = quiz_data.groupby('difficulty')['score'].mean().sort_values()

    plt.figure(figsize=(8, 5))
    avg_score_by_difficulty.plot(kind='bar', color='darkorange')
    plt.xlabel("Difficulty Level")
    plt.ylabel("Average Score")
    plt.title("Performance by Difficulty Level")
    plt.show()
else:
    print("Warning: Column 'difficulty' not found! Skipping difficulty analysis.")

# --- Step 2: Identify Weak Areas ---
# Identify topics with lowest average score
average_score_by_topic = quiz_data.groupby('quiz_title')['score'].mean().sort_values()
lowest_scoring_topics = average_score_by_topic.head(5)  # Get the bottom 5 topics

print("\nWeak Areas (Topics with lowest average scores):")
print(lowest_scoring_topics)

# Visualize the weakest topics
plt.figure(figsize=(12, 6))
lowest_scoring_topics.plot(kind='barh', color='red')
plt.xlabel("Average Score")
plt.ylabel("Topic")
plt.title("Weak Areas: Topics with Lowest Average Scores")
plt.show()

# --- Step 3: Trend Analysis (if possible) ---
# If 'submitted_at' exists, we can analyze performance over time.
if 'submitted_at' in quiz_data.columns:
    quiz_data['submitted_at'] = pd.to_datetime(quiz_data['submitted_at'])
    quiz_data['month'] = quiz_data['submitted_at'].dt.month

    # Calculate average score per month
    avg_score_by_month = quiz_data.groupby('month')['score'].mean()

    plt.figure(figsize=(8, 5))
    avg_score_by_month.plot(kind='line', marker='o', color='b')
    plt.xlabel("Month")
    plt.ylabel("Average Score")
    plt.title("Trend Analysis: Average Score by Month")
    plt.show()
else:
    print("Warning: Column 'submitted_at' not found! Skipping trend analysis.")

# --- Step 4: Personalized Recommendations ---
# Recommend topics with lowest average scores
recommended_topics = lowest_scoring_topics.index.tolist()

print("\nPersonalized Recommendations (Topics for Improvement):")
for topic in recommended_topics:
    print(f"- {topic}")

# --- Step 5: Bonus - Define Student Persona ---
# Group students based on performance in specific topics (for example, identify top and bottom 5 topics)
topic_performance = quiz_data.groupby(['user_id', 'quiz_title'])['score'].mean().unstack()

# Identify students with strong and weak areas
strong_areas = topic_performance.max(axis=1)  # Strongest topics for each student
weak_areas = topic_performance.min(axis=1)  # Weakest topics for each student

# Visualize the top and bottom performers in each topic
plt.figure(figsize=(12, 6))
strong_areas.plot(kind='barh', color='green', alpha=0.6, label="Strong Areas")
weak_areas.plot(kind='barh', color='red', alpha=0.6, label="Weak Areas")
plt.xlabel("Score")
plt.ylabel("Student ID")
plt.title("Student Persona: Strong and Weak Areas")
plt.legend()
plt.show()
