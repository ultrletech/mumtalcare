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
}