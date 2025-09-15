# test_local_model.py
from transformers import pipeline

def test_local_model_load():
    """
    Test that the local sentiment model loads and returns valid output.
    """
    model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    result = model("I am happy!")[0]
    
    # Assertions to make sure model output has expected keys
    assert "label" in result, "Model output missing 'label'"
    assert "score" in result, "Model output missing 'score'"
    assert isinstance(result["score"], float), "'score' should be a float"
    assert isinstance(result["label"], str), "'label' should be a string"

if __name__ == "__main__":
    test_local_model_load()
    print("✅ Local model test passed!")
