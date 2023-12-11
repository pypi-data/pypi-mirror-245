from .utils_model import ParallelWorkerPool
from .utils_model import ONNXModelWorker, convert_model_to_onnx

def get_embeddings(sentences, model_name="bert-base-uncased", output_dir="./models"):
    model_path = convert_model_to_onnx(model_name, output_dir)
    pool = ParallelWorkerPool(num_workers=2, worker_class=ONNXModelWorker, model_path=str(model_path), model_name=model_name)
    pool.start()

    embeddings = []
    for sentence in sentences:
        embedding = pool.get_embedding(sentence)
        embeddings.append(embedding)

    pool.stop()
    return embeddings

