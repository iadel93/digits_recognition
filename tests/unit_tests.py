from digits_recognition.server.server import predict_digit
from digits_recognition.types.server_types import Item

def test_predict_image():
    img = [0.0] * 784  # Example flat list representing a 28x28 image
    item = Item(image_data=img)
    response = predict_digit(item)
    assert "prediction" in response
    assert isinstance(response["prediction"], int)