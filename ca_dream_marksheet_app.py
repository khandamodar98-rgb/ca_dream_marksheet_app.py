from flask import Flask, request, render_template_string
from markupsafe import escape
import json

app = Flask(__name__)

CREATOR = "Nishchay Sharma"
MOTIVATIONAL_MESSAGE = (
    "TU CA BAN NE KE KARIB TO AA GYA HAI, OR TU JARUR KAR LEGA. "
    "BEST WISHES FOR THE EXAM."
)

# Illustrative subject names for the commonly used six-paper scheme.
# Always verify subjects against the syllabus applicable to the student's attempt.
COURSES = {
    "CA Intermediate": {
        "Group I": [
            "Advanced Accounting",
            "Corporate and Other Laws",
            "Taxation",
        ],
        "Group II": [
            "Cost and Management Accounting",
            "Auditing and Ethics",
            "Financial Management and Strategic Management",
        ],
    },
    "CA Final": {
        "Group I": [
            "Financial Reporting",
            "Advanced Financial Management",
            "Advanced Auditing, Assurance and Professional Ethics",
        ],
        "Group II": [
            "Direct Tax Laws and International Taxation",
            "Indirect Tax Laws",
            "Integrated Business Solutions",
        ],
    },
}

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#102b4e">
<title>CA Dream Marksheet | Nishchay Sharma</title>
<style>
:root {
  --navy:#102b4e; --blue:#1b4f82; --gold:#d8b45c;
  --ink:#1e293b; --muted:#64748b; --bg:#edf2f8; --line:#d8e0eb;
  --white:#fff; --pale:#f5f8fc;
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
       font-family:Inter,Arial,Helvetica,sans-serif; }
header { color:white; padding:34px 16px 38px; text-align:center;
         background:linear-gradient(125deg,#0b1d35,#174d7e 72%,#9b7931); }
.brand { font-size:12px; letter-spacing:3px; color:#f0d995; font-weight:800; }
header h1 { font-size:clamp(27px,5vw,43px); margin:10px 0; }
header p { max-width:640px; margin:0 auto; line-height:1.6; color:#e5edf7; }
.wrap { width:min(1000px,94%); margin:26px auto 48px; }
.card { background:white; border:1px solid #e3e9f1; border-radius:16px;
        padding:clamp(17px,3vw,28px); margin-bottom:22px;
        box-shadow:0 10px 30px #102b4e0b; }
h2 { color:var(--navy); margin:0 0 8px; }
.sub { color:var(--muted); margin:0 0 22px; line-height:1.6; }
.grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }
label { display:block; font-size:14px; font-weight:750; margin-bottom:7px; }
input,select { width:100%; min-width:0; padding:12px 13px; border:1px solid #cbd5e1;
  border-radius:9px; background:white; color:var(--ink); font-size:15px; }
input:focus,select:focus { outline:2px solid #8cb9e6; border-color:var(--blue); }
.field { min-width:0; }
.group-heading { margin:25px 0 12px; display:flex; align-items:center; gap:10px;
  color:var(--navy); font-weight:800; }
.group-heading:after { content:""; height:1px; flex:1; background:var(--line); }
.subjects { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
.btn { border:0; border-radius:9px; padding:13px 16px; font-size:15px;
  font-weight:800; cursor:pointer; text-decoration:none; display:inline-flex;
  align-items:center; justify-content:center; gap:8px; }
.btn-primary { background:var(--navy); color:white; }
.btn-gold { background:var(--gold); color:#1b2738; }
.btn-light { background:#eaf0f7; color:var(--navy); }
.btn:hover { filter:brightness(1.04); }
.submit { width:100%; margin-top:22px; }
.hint { color:var(--muted); font-size:12px; line-height:1.6; margin-top:12px; }
.error { background:#fff1f2; border:1px solid #fecdd3; color:#9f1239;
  padding:12px; border-radius:9px; margin-bottom:16px; }
.result-top { display:flex; justify-content:space-between; align-items:start;
  gap:16px; flex-wrap:wrap; margin-bottom:18px; }
.pill { border:1px solid #d3b25d; background:#fff9e7; color:#795a12;
  padding:8px 11px; border-radius:999px; font-size:11px; font-weight:900;
  letter-spacing:.5px; }
.sheet { border:4px double var(--navy); padding:clamp(14px,3vw,28px);
  background:white; }
.sheet-head { text-align:center; border-bottom:2px solid var(--gold); padding-bottom:17px; }
.sheet-head .smallcap { font-size:11px; font-weight:900; letter-spacing:2px; color:var(--blue); }
.sheet-head h2 { font-size:clamp(21px,4vw,30px); margin:9px 0; }
.sheet-head p { margin:0; color:var(--muted); }
.target-banner { display:inline-block; margin-top:13px; padding:7px 11px;
  border:1px solid #b48b31; color:#795a12; font-weight:900; font-size:11px; }
.details { display:grid; grid-template-columns:repeat(2,minmax(0,1fr));
  gap:10px 18px; margin:18px 0; font-size:14px; overflow-wrap:anywhere; }
table { width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }
th,td { padding:11px 9px; border:1px solid #cbd5e1; text-align:left; }
th { background:#eaf0f7; color:var(--navy); }
td.num,th.num { text-align:center; white-space:nowrap; }
.group-row td { background:#f7f9fc; font-weight:850; color:var(--navy); }
.metrics { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin-top:17px; }
.metric { background:#f0f5fb; border-radius:10px; text-align:center; padding:14px 8px; }
.metric span { display:block; font-size:12px; color:var(--muted); }
.metric strong { display:block; color:var(--navy); font-size:clamp(19px,3vw,25px); margin-top:6px; }
.motivation { margin-top:20px; padding:22px 18px; text-align:center; color:white;
  border-radius:10px; background:linear-gradient(125deg,#102b4e,#1b4f82); line-height:1.8; }
.motivation small { color:#f1d58b; font-weight:850; letter-spacing:1.5px; }
.motivation blockquote { margin:10px 0 0; font-size:clamp(16px,2.5vw,21px); font-weight:800; }
.sign { text-align:right; color:var(--navy); font-weight:800; line-height:1.6; margin-top:18px; }
.disclaimer { text-align:center; color:#64748b; font-size:10px; line-height:1.6; margin-top:18px; }
.actions { display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; }
.actions .btn { flex:1 1 180px; }
footer { text-align:center; padding:20px; color:#64748b; font-size:12px; }
@media(max-width:620px) {
  .grid,.subjects,.details { grid-template-columns:1fr; }
  .metrics { grid-template-columns:1fr; }
  th,td { padding:8px 6px; font-size:11px; }
  .sheet { padding:10px; }
}
@media print {
  body { background:white; }
  header,.form-card,footer,.actions,.result-title { display:none!important; }
  .wrap { width:100%; margin:0; }
  .card { border:0; box-shadow:none; padding:0; margin:0; }
  .sheet { padding:10mm; border:4px double #102b4e; }
  .motivation { print-color-adjust:exact; -webkit-print-color-adjust:exact; }
  @page { size:A4; margin:10mm; }
}
</style>
</head>
<body>
<header>
  <div class="brand">YOUR GOAL. YOUR JOURNEY.</div>
  <h1>CA Dream Marksheet</h1>
  <p>Picture your target. Plan your preparation. Keep moving forward.</p>
</header>

<main class="wrap">
<section class="card form-card">
  <h2>Create your dream result</h2>
  <p class="sub">Choose your course and exam attempt, then enter the marks you are aiming for.</p>

  {% if error %}<div class="error" role="alert">{{ error }}</div>{% endif %}

  <form method="post" action="#result">
    <div class="grid">
      <div class="field">
        <label for="student">Student name</label>
        <input id="student" name="student" maxlength="80" required
               placeholder="Enter your name" value="{{ student }}">
      </div>
      <div class="field">
        <label for="course">Course</label>
        <select id="course" name="course" onchange="renderSubjects()" required>
          {% for c in courses %}
          <option value="{{ c }}" {% if c == course %}selected{% endif %}>{{ c }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="field">
        <label for="attempt">Examination attempt</label>
        <input id="attempt" name="attempt" maxlength="40"
               placeholder="e.g. May 2027 / September 2027"
               value="{{ attempt }}" required>
      </div>
      <div class="field">
        <label for="target">Personal target</label>
        <select id="target" name="target">
          <option value="Exemption-focused" {% if target == 'Exemption-focused' %}selected{% endif %}>Exemption-focused</option>
          <option value="Balanced score" {% if target == 'Balanced score' %}selected{% endif %}>Balanced score</option>
          <option value="My own target" {% if target == 'My own target' %}selected{% endif %}>My own target</option>
        </select>
      </div>
    </div>

    <div id="subjectInputs"></div>
    <p class="hint">Enter whole-number target marks from 0 to 100 per paper. Group totals and overall percentage update in the generated marksheet. Subject names are illustrative; confirm the syllabus applicable to your attempt.</p>
    <button class="btn btn-primary submit" type="submit">Generate My Dream Marksheet →</button>
  </form>
</section>

{% if generated %}
<section class="card" id="result">
  <div class="result-top result-title">
    <div><h2>Your target, in writing.</h2><p class="sub" style="margin:6px 0 0">Save it, print it, or share it as a reminder.</p></div>
    <span class="pill">UNOFFICIAL TARGET MARKSHEET</span>
  </div>

  <div class="sheet" id="printable">
    <div class="sheet-head">
      <div class="smallcap">CA DREAM MARKSHEET • PERSONAL GOAL PLANNER</div>
      <h2>CHARTERED ACCOUNTANCY</h2>
      <p>{{ course }} · Examination attempt: {{ attempt }}</p>
      <div class="target-banner">TARGET MARKS — NOT AN OFFICIAL RESULT</div>
    </div>

    <div class="details">
      <div><strong>Student name:</strong> {{ student }}</div>
      <div><strong>Goal style:</strong> {{ target }}</div>
      <div><strong>Prepared with:</strong> {{ creator }}</div>
      <div><strong>Result status:</strong> Self-entered target</div>
    </div>

    <table>
      <thead><tr><th>Paper</th><th>Subject</th><th class="num">Target</th><th class="num">Out of</th></tr></thead>
      <tbody>
      {% for group, items in groups.items() %}
        <tr class="group-row"><td colspan="4">{{ group }}</td></tr>
        {% for item in items %}
        <tr>
          <td>{{ item.number }}</td><td>{{ item.subject }}</td>
          <td class="num">{{ item.mark }}</td><td class="num">100</td>
        </tr>
        {% endfor %}
        <tr class="group-row"><td colspan="2">{{ group }} target total</td>
          <td class="num">{{ group_totals[group] }}</td>
          <td class="num">{{ items|length * 100 }}</td></tr>
      {% endfor %}
      </tbody>
    </table>

    <div class="metrics">
      <div class="metric"><span>Total target marks</span><strong>{{ total }}/{{ maximum }}</strong></div>
      <div class="metric"><span>Target percentage</span><strong>{{ percentage }}%</strong></div>
      <div class="metric"><span>Target per group</span><strong>{{ group_count }} groups</strong></div>
    </div>

    <div class="motivation">
      <small>A PERSONAL MESSAGE FROM {{ creator|upper }}</small>
      <blockquote>{{ message }}</blockquote>
    </div>
    <div class="sign">Best Wishes,<br>{{ creator }}</div>
    <div class="disclaimer">
      UNOFFICIAL MOTIVATIONAL TARGET ONLY. Not issued, verified, affiliated with or endorsed by ICAI.
      Marks are entered by the student and do not represent actual results or guarantee a qualification.
      Subject names may vary by syllabus and exam attempt. No student information is stored by this demo.
    </div>
  </div>

  <div class="actions">
    <button class="btn btn-primary" type="button" onclick="window.print()">Print / Save as PDF</button>
    <button class="btn btn-gold" type="button" onclick="shareWhatsApp()">Share on WhatsApp</button>
    <button class="btn btn-light" type="button" onclick="copySummary()">Copy result summary</button>
  </div>
  <p class="hint" id="shareStatus" aria-live="polite"></p>
</section>
{% endif %}
</main>

<footer>CA Dream Marksheet · A student motivation project by {{ creator }} · Not an official ICAI website</footer>

<script>
const subjectData = {{ courses_json|safe }};
const savedMarks = {{ marks_json|safe }};
const selectedCourse = {{ course_json|safe }};

function renderSubjects() {
  const course = document.getElementById("course").value;
  const container = document.getElementById("subjectInputs");
  container.replaceChildren();
  let index = 0;

  Object.entries(subjectData[course]).forEach(([group, subjects]) => {
    const heading = document.createElement("div");
    heading.className = "group-heading";
    heading.textContent = group;
    container.appendChild(heading);

    const grid = document.createElement("div");
    grid.className = "subjects";
    subjects.forEach(subject => {
      const field = document.createElement("div");
      field.className = "field";
      const label = document.createElement("label");
      label.htmlFor = "mark" + index;
      label.textContent = subject;
      const input = document.createElement("input");
      input.type = "number";
      input.id = "mark" + index;
      input.name = "mark" + index;
      input.min = "0"; input.max = "100"; input.step = "1";
      input.required = true;
      input.inputMode = "numeric";
      input.value = (course === selectedCourse && savedMarks[index] !== undefined)
        ? savedMarks[index] : 75;
      field.append(label, input);
      grid.appendChild(field);
      index++;
    });
    container.appendChild(grid);
  });
}
renderSubjects();

const shareText = {{ share_text_json|safe }};
function shareWhatsApp() {
  const url = "https://wa.me/?text=" + encodeURIComponent(shareText);
  window.open(url, "_blank", "noopener,noreferrer");
}
async function copySummary() {
  const status = document.getElementById("shareStatus");
  try {
    await navigator.clipboard.writeText(shareText);
    status.textContent = "Result summary copied. Paste it into your favourite app.";
  } catch (e) {
    status.textContent = shareText;
  }
}
</script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    course = request.form.get("course", "CA Final")
    if course not in COURSES:
        course = "CA Final"

    student = request.form.get("student", "").strip()[:80]
    attempt = request.form.get("attempt", "").strip()[:40]
    target = request.form.get("target", "Balanced score")
    if target not in {"Exemption-focused", "Balanced score", "My own target"}:
        target = "Balanced score"

    generated = request.method == "POST"
    error = None
    marks = []
    groups = {}
    group_totals = {}
    total = maximum = 0
    percentage = 0.0

    if generated:
        try:
            if not student or not attempt:
                raise ValueError("Please enter your name and examination attempt.")
            index = 0
            for group_name, subjects in COURSES[course].items():
                group_items = []
                group_sum = 0
                for subject in subjects:
                    raw = request.form.get(f"mark{index}", "")
                    # Reject decimals and non-numeric values.
                    mark = int(raw)
                    if not 0 <= mark <= 100:
                        raise ValueError("Each paper's target must be between 0 and 100.")
                    marks.append(mark)
                    group_items.append({
                        "number": index + 1,
                        "subject": subject,
                        "mark": mark,
                    })
                    group_sum += mark
                    index += 1
                groups[group_name] = group_items
                group_totals[group_name] = group_sum

            total = sum(marks)
            maximum = len(marks) * 100
            percentage = round(total / maximum * 100, 2)

        except (ValueError, TypeError):
            error = "Please enter your name, exam attempt, and whole-number marks from 0 to 100."
            generated = False
            marks = []

    if not marks:
        marks = [75] * sum(len(s) for s in COURSES[course].values())

    summary = (
        f"My CA Dream Marksheet target: {student or 'CA Aspirant'} | {course} | "
        f"{attempt or 'My exam attempt'} | Target: {total}/{maximum} ({percentage}%). "
        f"{MOTIVATIONAL_MESSAGE} — {CREATOR}. "
        "Unofficial target only; not an ICAI result."
    )

    return render_template_string(
        PAGE,
        courses=COURSES,
        course=course,
        student=student,
        attempt=attempt,
        target=target,
        generated=generated,
        error=error,
        groups=groups,
        group_totals=group_totals,
        marks=marks,
        total=total,
        maximum=maximum,
        percentage=percentage,
        group_count=len(COURSES[course]),
        creator=CREATOR,
        message=MOTIVATIONAL_MESSAGE,
        courses_json=json.dumps(COURSES),
        marks_json=json.dumps(marks),
        course_json=json.dumps(course),
        share_text_json=json.dumps(summary),
    )


if __name__ == "__main__":
    # For local development only. Use a production WSGI server when deployed.
    app.run(host="127.0.0.1", port=5000, debug=True)
