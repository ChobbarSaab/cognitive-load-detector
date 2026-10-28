"""
STEP 1 - CREATE A SAMPLE DATASET
--------------------------------
This script makes a practice dataset of 150 students who each did a
10-question learning quiz. It is SIMULATED data (made by the computer),
so you can build and test the model before collecting real responses.

Each row = one student. Columns:
  student_id         - anonymous ID (no names, for privacy)
  time_minutes       - how long the student took to finish the quiz
  correct_answers    - answers right (out of 10)
  wrong_answers      - answers wrong (out of 10)
  errors_made        - times they changed / corrected an answer while working
  difficulty_rating  - "How difficult was this task?" 1 = very easy ... 5 = very hard
  mental_effort      - "How much mental effort did you put in?" 1 = very low ... 9 = very high
                       (this 1-9 scale is the Paas mental effort scale, widely used
                        in cognitive load research)
  cognitive_load     - the category we want the AI to predict:
                       mental effort 1-3 = Low, 4-6 = Moderate, 7-9 = High
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)   # fixed seed = same data every time you run it
N = 150                           # number of students
QUESTIONS = 10

rows = []
for i in range(N):
    # a hidden "true load" for this student, from 0 (very easy) to 1 (very hard)
    load = rng.beta(2, 2)

    time_minutes = np.clip(rng.normal(6 + 13 * load, 1.5), 3, 25)
    correct = int(rng.binomial(QUESTIONS, 0.95 - 0.6 * load))
    errors = int(rng.poisson(0.5 + 6 * load))
    difficulty = int(np.clip(round(1 + 4 * load + rng.normal(0, 0.5)), 1, 5))
    effort = int(np.clip(round(1 + 8 * load + rng.normal(0, 0.6)), 1, 9))

    if effort <= 3:
        category = "Low"
    elif effort <= 6:
        category = "Moderate"
    else:
        category = "High"

    rows.append({
        "student_id": f"S{i + 1:03d}",
        "time_minutes": round(float(time_minutes), 1),
        "correct_answers": correct,
        "wrong_answers": QUESTIONS - correct,
        "errors_made": errors,
        "difficulty_rating": difficulty,
        "mental_effort": effort,
        "cognitive_load": category,
    })

df = pd.DataFrame(rows)
df.to_csv("cognitive_load_data.csv", index=False)

print("Saved cognitive_load_data.csv with", len(df), "students")
print(df["cognitive_load"].value_counts())
