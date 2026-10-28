/**
 * GOOGLE SHEET RECEIVER for the AI Cognitive Load Detector website.
 *
 * Paste this whole file into Extensions > Apps Script of your Google Sheet,
 * then deploy it as a Web app (see README.md, Part 2).
 * Every time a student finishes the task, one row is added to the
 * "Responses" tab.
 */

const SHEET_NAME = "Responses";
const HEADERS = [
  "student_id", "time_minutes", "correct_answers", "wrong_answers",
  "errors_made", "difficulty_rating", "mental_effort", "cognitive_load",
  "predicted_load", "name", "submitted_at"
];
const LEVELS = ["Low", "Moderate", "High"];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000); // one student at a time, so IDs never clash
  try {
    const d = JSON.parse(e.postData.contents);

    // Basic checks so random or broken data can't get in
    const num = (v, lo, hi) => typeof v === "number" && isFinite(v) && v >= lo && v <= hi;
    const ok =
      num(d.time_minutes, 0, 180) &&
      num(d.correct_answers, 0, 10) && Number.isInteger(d.correct_answers) &&
      num(d.errors_made, 0, 500) && Number.isInteger(d.errors_made) &&
      num(d.difficulty_rating, 1, 5) && Number.isInteger(d.difficulty_rating) &&
      num(d.mental_effort, 1, 9) && Number.isInteger(d.mental_effort);
    if (!ok) return reply({ ok: false, error: "invalid data" });

    const sheet = getSheet();
    const id = "S" + String(sheet.getLastRow()).padStart(3, "0"); // row 2 -> S001
    const load = d.mental_effort <= 3 ? "Low" : d.mental_effort <= 6 ? "Moderate" : "High";
    const predicted = LEVELS.indexOf(d.predicted_load) >= 0 ? d.predicted_load : "";
    // a leading = + - @ would make Sheets treat the name as a formula
    const name = String(d.name || "").slice(0, 60).replace(/^[=+\-@]+/, "");

    sheet.appendRow([
      id, d.time_minutes, d.correct_answers, 10 - d.correct_answers,
      d.errors_made, d.difficulty_rating, d.mental_effort, load,
      predicted, name, new Date()
    ]);
    return reply({ ok: true, student_id: id });
  } catch (err) {
    return reply({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// Opening the web app link in a browser shows this, so you can check it is live
function doGet() {
  return reply({ ok: true, message: "Cognitive Load Detector receiver is running." });
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
