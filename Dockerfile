FROM tensorflow/tensorflow
RUN pip install wandb
COPY mnist_wandb_test.py /mnist_wandb_test.py
ENTRYPOINT ["python3", "/mnist_wandb_test.py"]
