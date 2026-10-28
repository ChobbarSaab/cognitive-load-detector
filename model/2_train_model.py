"""
STEP 2 - TRAIN AND TEST THE AI MODEL (Decision Tree)
----------------------------------------------------
What this script does, in plain words:
  1. Reads the spreadsheet (cognitive_load_data.csv).
  2. Checks for missing values (Data Preparation).
  3. Picks the inputs the AI looks at (Feature Selection).
  4. Splits students into 70% for learning and 30% for testing.
  5. Trains a Decision Tree (Model Selection + Training).
  6. Tests it on students it has never seen (Evaluation).
  7. Saves charts and a results file you can paste into your slides.

To use your own Google Form data later: export it as CSV with the same
column names and save it as cognitive_load_data.csv, then run this again.
"""

import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

LABELS = ["Low", "Moderate", "High"]
COLORS = {"Low": "#2E9E6B", "Moderate": "#E0A12B", "High": "#D64545"}

# ---------- 1. Load data ----------
df = pd.read_csv("cognitive_load_data.csv")

# ---------- 2. Data preparation ----------
missing = int(df.isnull().sum().sum())
df = df.dropna()

# ---------- 3. Feature selection ----------
# The AI only sees task performance + how hard the task felt.
# We do NOT give it "mental_effort", because that is what the label is
# built from - giving it the answer would be cheating.
# We also skip "wrong_answers" because it is just 10 minus correct_answers.
FEATURES = ["time_minutes", "correct_answers", "errors_made", "difficulty_rating"]
X = df[FEATURES]
y = df["cognitive_load"]

# ---------- 4. Train / test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# ---------- 5. Train the Decision Tree ----------
# max_depth=3 keeps the tree small enough to explain on one slide.
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# ---------- 6. Test it ----------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=LABELS)
report = classification_report(y_test, y_pred, labels=LABELS, digits=2)

# Consistency check: give the model two almost identical students
a = pd.DataFrame([[8.0, 9, 1, 2]], columns=FEATURES)
b = pd.DataFrame([[8.3, 9, 1, 2]], columns=FEATURES)
consistent = model.predict(a)[0] == model.predict(b)[0]

# ---------- 7. Save results ----------
with open("results.txt", "w") as f:
    f.write("AI COGNITIVE LOAD DETECTOR - RESULTS (sample / simulated data)\n")
    f.write("=" * 62 + "\n\n")
    f.write(f"Students in dataset: {len(df)}\n")
    f.write(f"Missing values found: {missing}\n")
    f.write(f"Training students: {len(X_train)}   Testing students: {len(X_test)}\n")
    f.write(f"Inputs used: {', '.join(FEATURES)}\n\n")
    f.write(f"ACCURACY ON TEST DATA: {accuracy:.0%}  "
            f"({int((y_pred == y_test).sum())} of {len(y_test)} correct)\n\n")
    f.write("Confusion matrix (rows = actual, columns = predicted):\n")
    f.write(pd.DataFrame(cm, index=LABELS, columns=LABELS).to_string() + "\n\n")
    f.write("Per-category scores:\n" + report + "\n")
    f.write("Feature importance (how much the tree relies on each input):\n")
    for name, imp in sorted(zip(FEATURES, model.feature_importances_), key=lambda t: -t[1]):
        f.write(f"  {name:<18} {imp:.0%}\n")
    f.write(f"\nConsistency check (similar inputs -> same prediction): "
            f"{'PASSED' if consistent else 'FAILED'}\n\n")
    f.write("Decision rules the AI learned:\n")
    f.write(export_text(model, feature_names=FEATURES))
print(open("results.txt").read())

# Save the tree as JSON so the demo web page can use the exact same rules
t = model.tree_
tree_json = {
    "features": FEATURES,
    "classes": list(model.classes_),
    "left": t.children_left.tolist(),
    "right": t.children_right.tolist(),
    "feature": t.feature.tolist(),
    "threshold": t.threshold.tolist(),
    "value": [v[0].tolist() for v in t.value],
}
json.dump(tree_json, open("tree_model.json", "w"))

# ---------- Charts for the slides ----------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12})

# Chart 1: confusion matrix
fig, ax = plt.subplots(figsize=(6.5, 5.5))
ax.imshow(cm, cmap="Purples")
ax.set_xticks(range(3), LABELS)
ax.set_yticks(range(3), LABELS)
ax.set_xlabel("Predicted by AI")
ax.set_ylabel("Actual (from student's mental effort)")
for i in range(3):
    for j in range(3):
        ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=18,
                color="white" if cm[i, j] > cm.max() / 2 else "#222")
ax.set_title(f"Model Predictions vs Actual  (Accuracy {accuracy:.0%})", pad=12)
fig.tight_layout()
fig.savefig("chart_confusion_matrix.png", dpi=200)
plt.close(fig)

# Chart 2: feature importance
order = sorted(zip(FEATURES, model.feature_importances_), key=lambda t: t[1])
nice = {"time_minutes": "Completion time", "correct_answers": "Correct answers",
        "errors_made": "Errors made", "difficulty_rating": "Reported difficulty"}
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh([nice[n] for n, _ in order], [v * 100 for _, v in order], color="#6A3FB5")
for i, (_, v) in enumerate(order):
    ax.text(v * 100 + 1, i, f"{v:.0%}", va="center")
ax.set_xlabel("Importance (%)")
ax.set_xlim(0, 100)
ax.set_title("Which inputs the AI relies on most")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("chart_feature_importance.png", dpi=200)
plt.close(fig)

# Chart 3: data pattern - time vs correct answers, coloured by load
fig, ax = plt.subplots(figsize=(7, 5))
for lab in LABELS:
    part = df[df["cognitive_load"] == lab]
    ax.scatter(part["time_minutes"], part["correct_answers"], label=lab,
               color=COLORS[lab], alpha=0.75, s=45, edgecolor="white")
ax.set_xlabel("Completion time (minutes)")
ax.set_ylabel("Correct answers (out of 10)")
ax.set_title("Pattern: slower + fewer correct = higher load")
ax.legend(title="Cognitive load")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("chart_data_pattern.png", dpi=200)
plt.close(fig)

# Chart 4: average values per category
means = df.groupby("cognitive_load")[["time_minutes", "correct_answers",
                                      "errors_made", "difficulty_rating"]].mean().loc[LABELS]
fig, axes = plt.subplots(1, 4, figsize=(12, 3.8))
titles = ["Avg time (min)", "Avg correct (/10)", "Avg errors", "Avg difficulty (/5)"]
for ax, col, title in zip(axes, means.columns, titles):
    bars = ax.bar(LABELS, means[col], color=[COLORS[l] for l in LABELS])
    ax.bar_label(bars, fmt="%.1f")
    ax.set_ylim(0, means[col].max() * 1.25)
    ax.set_title(title, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_yticks([])
fig.suptitle("Average task results for each cognitive load level")
fig.tight_layout()
fig.savefig("chart_averages.png", dpi=200)
plt.close(fig)

# Chart 5: the decision tree itself
fig, ax = plt.subplots(figsize=(16, 7))
plot_tree(model, feature_names=[nice[f] for f in FEATURES],
          class_names=list(model.classes_), filled=True, rounded=True,
          impurity=False, fontsize=10, ax=ax)
ax.set_title("The Decision Tree the AI learned", fontsize=16)
fig.tight_layout()
fig.savefig("chart_decision_tree.png", dpi=200)
plt.close(fig)

print("Charts saved.")
