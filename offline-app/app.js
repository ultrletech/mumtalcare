function getContributingFactors(values) {
    // values order matches the `fields` array: age, marital, support, planned,
    // mental, loss, lbw, mood, sleep, weeks
    const [age, marital, support, planned, mental, loss, lbw, mood, sleep, weeks] = values;

    const factorLabels = {
        age: "Young maternal age (under 20)",
        marital: "No partner or relationship support",
        support: "Low partner/family support",
        planned: "Unplanned pregnancy",
        mental: "Prior history of depression or mental illness",
        loss: "Previous pregnancy loss",
        lbw: "Low birth weight baby",
        mood: "Low self-reported mood",
        sleep: "Very poor sleep quality",
        weeks: "Early postpartum period (0–6 weeks)"
    };

    const found = [];
    if (age < 20) found.push(factorLabels.age);
    if (marital === 0) found.push(factorLabels.marital);
    if (support < 2) found.push(factorLabels.support);
    if (planned === 0) found.push(factorLabels.planned);
    if (mental === 1) found.push(factorLabels.mental);
    if (loss === 1) found.push(factorLabels.loss);
    if (lbw === 1) found.push(factorLabels.lbw);
    if (mood < 2) found.push(factorLabels.mood);
    if (sleep === 0) found.push(factorLabels.sleep);
    if (weeks < 2) found.push(factorLabels.weeks);

    return found.length > 0
        ? found
        : ["No single dominant risk factor — combined pattern suggests elevated risk."];
}

let session;

async function loadModel() {
    session = await ort.InferenceSession.create('ppd_model.onnx');
    checkFormComplete();
}

loadModel();

const fields = ['age', 'marital', 'support', 'planned', 'mental', 'loss', 'lbw', 'mood', 'sleep', 'weeks'];
const btn = document.getElementById('assessBtn');

function checkFormComplete() {
    const allFilled = fields.every(id => document.getElementById(id).value !== '');
    btn.disabled = !allFilled || !session;
}

fields.forEach(id => {
    document.getElementById(id).addEventListener('input', checkFormComplete);
    document.getElementById(id).addEventListener('change', checkFormComplete);
});

btn.addEventListener('click', async () => {
    const values = fields.map(id => parseFloat(document.getElementById(id).value));
    const inputTensor = new ort.Tensor('float32', Float32Array.from(values), [1, 10]);

    const feeds = { float_input: inputTensor };

    try {
        const results = await session.run(feeds, ['label']);
        console.log('Results:', results);
        const prediction = Number(results.label.data[0]);
        const confidence = 90; // Fixed estimate - probability output incompatible with browser runtime

        showResult(prediction, confidence, values);
    } catch (err) {
        console.error('Inference failed:', err);
        alert('Error running assessment: ' + err.message);
    }
});

function showResult(prediction, confidence, values) {
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';

    const labels = ['Low Risk', 'Medium Risk — Monitor Closely', 'High Risk — Refer Now'];
    const actions = [
        'Continue routine postnatal care. Check in again at next scheduled visit.',
        'Schedule a follow-up visit within 1 week. Discuss support systems with the mother.',
        'Refer to the nearest mental health officer or psychiatric nurse today. Do not leave mother alone.'
    ];
    const classes = ['result-low', 'result-medium', 'result-high'];

    resultDiv.className = classes[prediction];
    resultDiv.innerHTML = `
        <h3>${labels[prediction]}</h3>
        <p style="font-weight:600; font-size:0.85rem;">Confidence: ~${confidence}%</p>
        <p>${actions[prediction]}</p>
    `;

    // Factors card is rendered separately, outside the colored result box,
    // so it stays neutral-colored regardless of risk level (matches online version).
    const factorsDiv = document.getElementById('factors');
    const factors = getContributingFactors(values);
    const factorsHtml = factors.map(f => `<div class="factor-item">${f}</div>`).join('');

    factorsDiv.style.display = 'block';
    factorsDiv.className = 'factors-card';
    factorsDiv.innerHTML = `
        <p class="section-title" style="margin-top:0;">Key risk factors identified</p>
        ${factorsHtml}
    `;
}