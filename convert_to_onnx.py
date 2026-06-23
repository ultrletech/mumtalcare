import joblib
import numpy as np
from skl2onnx import convert_sklearn, update_registered_converter
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx.common.shape_calculator import calculate_linear_classifier_output_shapes
from onnxmltools.convert.xgboost.operator_converters.XGBoost import convert_xgboost
from xgboost import XGBClassifier

# Register XGBoost converter with skl2onnx
update_registered_converter(
    XGBClassifier, 'XGBoostXGBClassifier',
    calculate_linear_classifier_output_shapes, convert_xgboost,
    options={'nocl': [True, False], 'zipmap': [True, False, 'columns']}
)

# Load your trained model
model = joblib.load('ppd_model.pkl')

# Fix: XGBoost stored pandas column names internally, which breaks ONNX conversion.
# Strip them so it uses generic feature names instead.
model.get_booster().feature_names = None

# Define the input shape: 10 features, as floats
initial_type = [('float_input', FloatTensorType([None, 10]))]

onnx_model = convert_sklearn(
    model,
    initial_types=initial_type,
    target_opset={'': 12, 'ai.onnx.ml': 3},
    options={'zipmap': False}
)

# Inspect outputs before saving
for output in onnx_model.graph.output:
    print("Output name:", output.name)

# Save the ONNX model
with open("ppd_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("Model successfully converted to ppd_model.onnx")

# Quick verification - test that it loads and runs
import onnxruntime as rt

sess = rt.InferenceSession("ppd_model.onnx", providers=["CPUExecutionProvider"])
test_input = np.array([[25, 0, 0, 0, 1, 1, 0, 1, 0, 0]], dtype=np.float32)
result = sess.run(None, {"float_input": test_input})
print("Test prediction:", result[0])
print("Test probabilities:", result[1])