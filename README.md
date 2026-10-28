# AI Cognitive Load Detector

A school project that uses Artificial Intelligence to estimate how much mental effort (cognitive load) a learning task takes.

Students complete a 10-question task on the website. The site records how long they took, how many answers were correct, and how many times they changed an answer. Students then rate the difficulty (1–5) and their mental effort (1–9). A Decision Tree model estimates their cognitive load as **Low**, **Moderate** or **High**, and every response is saved to a Google Sheet.

> Estimates are for improving learning materials only. They are not medical or psychological diagnoses.

## What's in this repository

| File / folder | What it is |
|---|---|
| `index.html` | The whole website (task + model demo). This is the only file the host needs. |
| `google-apps-script.gs` | Small script that saves each response into your Google Sheet |
| `model/1_create_sample_data.py` | Creates a sample dataset of 150 simulated students |
| `model/2_train_model.py` | Trains and tests the Decision Tree, makes charts |
| `model/cognitive_load_data.csv` | The sample dataset |
| `model/results.txt` | Accuracy and rules the model learned (73% on sample data) |
| `model/chart_*.png` | Charts for the presentation |
| `model/tree_model.json` | The trained model (the website uses the same rules) |

---

## Setup (about 15 minutes, no coding)

### Part 1 – Put the code on GitHub

1. Sign in at [github.com](https://github.com) and click **New** (green button) to create a repository.
2. Name it `cognitive-load-detector`, choose **Public**, and click **Create repository**.
3. On the next page click **uploading an existing file**.
4. Unzip the project folder on your computer. Drag **everything inside it** (`index.html`, `README.md`, `google-apps-script.gs` and the `model` folder) into the upload box.
5. Click **Commit changes**.

### Part 2 – Create the Google Sheet that collects responses

1. Go to [sheets.new](https://sheets.new) to create a new Google Sheet. Name it `Cognitive Load Responses`.
2. In the menu click **Extensions → Apps Script**.
3. Delete the code you see there. Open `google-apps-script.gs` from this project, copy all of it, and paste it in.
4. Click the **Save** icon.
5. Click **Deploy → New deployment**. Click the gear icon next to "Select type" and choose **Web app**.
6. Set **Execute as: Me** and **Who has access: Anyone**. Click **Deploy**.
7. Google asks for permission. Click **Authorize access**, pick your account, then **Advanced → Go to (project name) → Allow**. This warning appears because it is your own new script.
8. Copy the **Web app URL**. It ends with `/exec`.
9. Optional check: paste that URL in a new browser tab. You should see `"Cognitive Load Detector receiver is running."`

### Part 3 – Connect the website to the Sheet

1. In your GitHub repository, click `index.html`, then the **pencil icon** (Edit).
2. Near the top, find the **EASY EDIT** section:
   ```js
   SHEET_URL: ""
   ```
3. Paste your Web app URL between the quotes:
   ```js
   SHEET_URL: "https://script.google.com/macros/s/XXXXXXXX/exec"
   ```
4. Click **Commit changes**.

### Part 4 – Make the website live (free, GitHub Pages)

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Choose branch **main**, folder **/ (root)**, and click **Save**.
4. Wait 1–2 minutes and refresh. GitHub shows your link:
   `https://YOUR-USERNAME.github.io/cognitive-load-detector/`
5. Open it, do the task once yourself, and check that a new row appears in the **Responses** tab of your Sheet.

Share this link with classmates on WhatsApp. Every finished task adds one row to the Sheet automatically.

> **Other free hosts:** On [Netlify](https://app.netlify.com/drop) you can drag the project folder onto the page. On Vercel, import the GitHub repository. Do Part 3 before uploading.

---

## Retrain the model on real student data

Collect at least 30 responses, with at least 5 students in each of Low, Moderate and High.

1. In the Google Sheet, open the **Responses** tab, then **File → Download → Comma-separated values (.csv)**.
2. Rename the file to `cognitive_load_data.csv`.
3. Open [Google Colab](https://colab.research.google.com) and click **New notebook**. Click the folder icon on the left and upload the CSV and `model/2_train_model.py`.
4. In a code cell, run:
   ```
   !python 2_train_model.py
   ```
5. The new accuracy prints on screen. The new charts appear in the folder panel, ready to download.

The extra columns in the Sheet (`predicted_load`, `name`, `submitted_at`) are ignored by the model. Delete the `name` column before you share the data with anyone.

## Changing the code later

- **If you edit `google-apps-script.gs`:** in Apps Script choose **Deploy → Manage deployments → Edit (pencil) → Version: New version → Deploy**. Otherwise Google keeps running the old code. The URL stays the same.
- **If you retrain the model:** the website still uses the rules from the sample data. Ask your AI assistant to copy the new `tree_model.json` into the `TREE` line of `index.html`.

## Tools used

Python (pandas, scikit-learn, matplotlib), HTML/CSS/JavaScript, Google Sheets + Apps Script, GitHub Pages.

## References

1. Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science, 12*(2), 257–285.
2. Paas, F. G. W. C. (1992). Training strategies for attaining transfer of problem-solving skill in statistics: A cognitive-load approach. *Journal of Educational Psychology, 84*(4), 429–434.
3. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.
