import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
try:
    quiz_data = pd.read_csv("student_quiz_performance.csv")
    print("✅ Data loaded successfully!")
except FileNotFoundError:
    print("❌ Error: student_quiz_performance.csv not found.")
    exit()

# Debugging: Check dataset structure
print("🔹 Data Preview:\n", quiz_data.head())

# Extract quiz topic from the 'quiz' column
try:
    quiz_data["quiz"] = quiz_data["quiz"].apply(eval)  # Convert string representation of dict to actual dict
    quiz_data["quiz_topic"] = quiz_data["quiz"].apply(lambda x: x.get("title", "Unknown") if isinstance(x, dict) else "Unknown")
    print("✅ Extracted 'quiz_topic' successfully!")
except Exception as e:
    print(f"❌ Error extracting quiz topic: {e}")
    exit()

# Ensure required columns exist
required_columns = ["quiz_topic", "score", "accuracy", "correct_answers", "incorrect_answers"]
missing_columns = [col for col in required_columns if col not in quiz_data.columns]

if missing_columns:
    print(f"❌ Missing columns in dataset: {missing_columns}")
    exit()

# 🛠 Convert 'score' and 'accuracy' to numeric (removing % signs)
for col in ["score", "accuracy"]:
    quiz_data[col] = quiz_data[col].astype(str).str.replace("%", "").str.strip()  # Remove %
    quiz_data[col] = pd.to_numeric(quiz_data[col], errors="coerce")  # Convert to float

# Compute average performance by topic
topic_performance = quiz_data.groupby("quiz_topic")[["score", "accuracy", "correct_answers", "incorrect_answers"]].mean().reset_index()

# Debugging: Check grouped data
print("🔹 Topic Performance:\n", topic_performance)

# Plot Average Score by Topic
plt.figure(figsize=(10, 6))
plt.barh(topic_performance["quiz_topic"], topic_performance["score"], color="skyblue")
plt.xlabel("Average Score")
plt.ylabel("Topic")
plt.title("Average Score by Topic")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

