const state = {
  stepIndex: 0,
  answers: {
    age_group: null,
    main_symptom: null,
    severity: null,
    red_flags: [],
    fever_temp: "none_or_unknown",
    duration: null,
    risk_factors: ["none"],
  }
};

// 7 steps total (fever_temp step is shown always but can be forced to none)
const steps = [
  {
    key: "age_group",
    title: "Age group",
    help: "Choose the age group. (Used for more conservative guidance in young children and older adults.)",
    type: "single",
    options: [
      { value: "under_2", label: "Under 2 years" },
      { value: "2_to_12", label: "2–12 years" },
      { value: "13_to_64", label: "13–64 years" },
      { value: "65_plus", label: "65+ years" },
    ],
  },
  {
    key: "main_symptom",
    title: "Main symptom",
    help: "Pick the main symptom that best matches what is happening now.",
    type: "single",
    options: [
      { value: "chest_pain", label: "Chest pain" },
      { value: "breathing_trouble", label: "Breathing trouble" },
      { value: "abdominal_pain", label: "Abdominal pain" },
      { value: "fever", label: "Fever" },
      { value: "headache", label: "Headache" },
      { value: "vomiting_diarrhea", label: "Vomiting / diarrhea" },
      { value: "sore_throat_cough", label: "Sore throat / cough" },
      { value: "rash", label: "Rash" },
    ],
  },
  {
    key: "severity",
    title: "Severity right now",
    help: "How severe does it feel right now?",
    type: "single",
    options: [
      { value: "mild", label: "Mild (annoying but manageable)" },
      { value: "moderate", label: "Moderate (noticeable impact on daily activities)" },
      { value: "severe", label: "Severe (hard to function or very concerning)" },
    ],
  },
  {
    key: "red_flags",
    title: "Red flags (select any that apply)",
    help: "These may indicate a higher risk situation. If any apply, the guidance becomes more urgent.",
    type: "multi",
    options: [
      { value: "fainting_or_unresponsive", label: "Fainting or unresponsive" },
      { value: "severe_shortness_of_breath", label: "Severe shortness of breath" },
      { value: "blue_lips_face", label: "Blue lips/face" },
      { value: "new_confusion", label: "New confusion" },
      { value: "signs_of_stroke", label: "Possible stroke signs (face/arm/speech)" },
      { value: "uncontrolled_bleeding", label: "Uncontrolled bleeding" },
      { value: "seizure", label: "Seizure" },
      { value: "severe_allergic_reaction", label: "Severe allergic reaction (swelling + breathing trouble)" },
    ],
  },
  {
    key: "fever_temp",
    title: "Fever temperature (if you have a reading)",
    help: "If fever is not your main symptom, you can keep this as 'Unknown/none'.",
    type: "single",
    options: [
      { value: "none_or_unknown", label: "Unknown / none" },
      { value: "below_38", label: "Below 38°C" },
      { value: "38_to_39_4", label: "38°C to 39.4°C" },
      { value: "39_5_or_more", label: "39.5°C or more" },
    ],
  },
  {
    key: "duration",
    title: "Duration",
    help: "How long has this been going on?",
    type: "single",
    options: [
      { value: "less_24h", label: "Less than 24 hours" },
      { value: "1_to_3_days", label: "1–3 days" },
      { value: "more_3_days", label: "More than 3 days" },
    ],
  },
  {
    key: "risk_factors",
    title: "High-risk conditions (select any that apply)",
    help: "These can make it safer to seek care earlier.",
    type: "multi_with_none",
    options: [
      { value: "none", label: "None of these" },
      { value: "pregnant", label: "Pregnant" },
      { value: "immunocompromised", label: "Immunocompromised" },
      { value: "serious_heart_lung_disease", label: "Serious heart/lung disease" },
      { value: "diabetes_kidney_disease", label: "Diabetes/kidney disease" },
      { value: "infant_under_3_months", label: "Infant under 3 months" },
    ],
  },
];

const stepLabel = document.getElementById("stepLabel");
const barFill = document.getElementById("barFill");
const questionArea = document.getElementById("questionArea");
const backBtn = document.getElementById("backBtn");
const nextBtn = document.getElementById("nextBtn");

const resultCard = document.getElementById("resultCard");
const categoryPill = document.getElementById("categoryPill");
const reasonsList = document.getElementById("reasonsList");
const timestampText = document.getElementById("timestampText");

const restartBtn = document.getElementById("restartBtn");
const showHistoryBtn = document.getElementById("showHistoryBtn");
const historyArea = document.getElementById("historyArea");
const historyList = document.getElementById("historyList");

function percentComplete() {
  return Math.round(((state.stepIndex) / (steps.length - 1)) * 100);
}

function isStepAnswered(step) {
  const v = state.answers[step.key];
  if (step.type === "single") return v !== null && v !== undefined;
  if (step.type === "multi") return Array.isArray(v) && v.length >= 0; // multi can be empty
  if (step.type === "multi_with_none") return Array.isArray(v) && v.length > 0;
  return false;
}

function currentStep() {
  return steps[state.stepIndex];
}

function setNextEnabled() {
  const step = currentStep();

  // special: red_flags can be empty and still proceed
  if (step.key === "red_flags") {
    nextBtn.disabled = false;
    return;
  }

  // special: fever_temp can always proceed
  if (step.key === "fever_temp") {
    nextBtn.disabled = false;
    return;
  }

  nextBtn.disabled = !isStepAnswered(step);
}

function render() {
  const step = currentStep();
  stepLabel.textContent = `Step ${state.stepIndex + 1}/${steps.length}`;
  barFill.style.width = `${percentComplete()}%`;

  backBtn.disabled = state.stepIndex === 0;
  nextBtn.textContent = state.stepIndex === steps.length - 1 ? "Get result" : "Next";

  const html = `
    <h2 class="q-title">${step.title}</h2>
    <p class="q-help">${step.help}</p>
    <div class="options">
      ${step.options.map(opt => renderOption(step, opt)).join("")}
    </div>
  `;
  questionArea.innerHTML = html;

  attachHandlers(step);
  setNextEnabled();
}

function renderOption(step, opt) {
  const key = step.key;
  const value = opt.value;

  if (step.type === "single") {
    const checked = state.answers[key] === value ? "checked" : "";
    return `
      <label class="option">
        <input type="radio" name="${key}" value="${value}" ${checked} />
        <div>${opt.label}</div>
      </label>
    `;
  }

  // multi / multi_with_none
  const arr = state.answers[key] || [];
  const checked = arr.includes(value) ? "checked" : "";
  return `
    <label class="option">
      <input type="checkbox" name="${key}" value="${value}" ${checked} />
      <div>${opt.label}</div>
    </label>
  `;
}

function attachHandlers(step) {
  const inputs = questionArea.querySelectorAll("input");

  inputs.forEach(inp => {
    inp.addEventListener("change", () => {
      if (step.type === "single") {
        state.answers[step.key] = inp.value;
      } else if (step.type === "multi") {
        const v = inp.value;
        const set = new Set(state.answers[step.key] || []);
        if (inp.checked) set.add(v);
        else set.delete(v);
        state.answers[step.key] = Array.from(set);
      } else if (step.type === "multi_with_none") {
        const v = inp.value;
        const set = new Set(state.answers[step.key] || ["none"]);

        if (v === "none") {
          // selecting none clears others
          if (inp.checked) {
            state.answers[step.key] = ["none"];
            // uncheck all others visually
            inputs.forEach(i => {
              if (i.value !== "none") i.checked = false;
            });
          } else {
            // don't allow empty -> keep none checked
            inp.checked = true;
            state.answers[step.key] = ["none"];
          }
        } else {
          // selecting any other clears none
          set.delete("none");
          if (inp.checked) set.add(v);
          else set.delete(v);

          const arr = Array.from(set);
          state.answers[step.key] = arr.length ? arr : ["none"];

          // keep 'none' checkbox in sync
          inputs.forEach(i => {
            if (i.value === "none") i.checked = state.answers[step.key].includes("none");
          });
        }
      }

      // If main symptom isn't fever, force fever_temp to unknown (but still allow user to set if they want)
      if (step.key === "main_symptom" && inp.value !== "fever") {
        state.answers.fever_temp = "none_or_unknown";
      }

      setNextEnabled();
    });
  });
}

backBtn.addEventListener("click", () => {
  if (state.stepIndex > 0) {
    state.stepIndex -= 1;
    render();
  }
});

nextBtn.addEventListener("click", async () => {
  if (state.stepIndex < steps.length - 1) {
    state.stepIndex += 1;
    render();
    return;
  }

  // Submit
  await submit();
});

restartBtn.addEventListener("click", () => {
  state.stepIndex = 0;
  state.answers = {
    age_group: null,
    main_symptom: null,
    severity: null,
    red_flags: [],
    fever_temp: "none_or_unknown",
    duration: null,
    risk_factors: ["none"],
  };

  historyArea.classList.add("hidden");
  resultCard.classList.add("hidden");
  render();
});

showHistoryBtn.addEventListener("click", async () => {
  if (!historyArea.classList.contains("hidden")) {
    historyArea.classList.add("hidden");
    return;
  }
  const res = await fetch("/triage/history");
  const data = await res.json();
  historyList.innerHTML = (data.items || []).slice(0, 10).map(item => {
    const when = item.timestamp ? new Date(item.timestamp).toLocaleString() : "—";
    const reasons = (item.reasons || []).slice(0, 2).join("; ");
    return `<li><b>${item.category}</b> <span class="small">(${when})</span><br/><span class="small">${reasons}</span></li>`;
  }).join("");
  historyArea.classList.remove("hidden");
});

function setPill(category) {
  categoryPill.textContent = category;
  // simple color cues via inline style
  if (category.startsWith("Emergency")) categoryPill.style.borderColor = "rgba(255,77,77,0.7)";
  else if (category.startsWith("Urgent")) categoryPill.style.borderColor = "rgba(255,176,32,0.7)";
  else if (category.startsWith("See")) categoryPill.style.borderColor = "rgba(76,141,255,0.7)";
  else categoryPill.style.borderColor = "rgba(57,217,138,0.7)";
}

async function submit() {
  // Basic client validation for required single answers
  const requiredKeys = ["age_group", "main_symptom", "severity", "duration"];
  for (const k of requiredKeys) {
    if (!state.answers[k]) {
      alert("Please answer all required questions.");
      return;
    }
  }

  // If main symptom isn't fever, keep fever_temp to none_or_unknown
  if (state.answers.main_symptom !== "fever") {
    state.answers.fever_temp = "none_or_unknown";
  }

  // Build payload
  const payload = {
    age_group: state.answers.age_group,
    main_symptom: state.answers.main_symptom,
    severity: state.answers.severity,
    red_flags: state.answers.red_flags || [],
    fever_temp: state.answers.fever_temp || "none_or_unknown",
    duration: state.answers.duration,
    risk_factors: state.answers.risk_factors || ["none"],
  };

  const res = await fetch("/triage", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const txt = await res.text();
    alert("Server error: " + txt);
    return;
  }

  const data = await res.json();

  setPill(data.category);
  timestampText.textContent = data.timestamp ? new Date(data.timestamp).toLocaleString() : "";

  reasonsList.innerHTML = "";
  (data.reasons || []).forEach(r => {
    const li = document.createElement("li");
    li.textContent = r;
    reasonsList.appendChild(li);
  });

  resultCard.classList.remove("hidden");
  resultCard.scrollIntoView({ behavior: "smooth" });
}

render();
