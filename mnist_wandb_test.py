import argparse
import tensorflow as tf
from tensorflow import keras
import wandb
from wandb.keras import WandbMetricsLogger

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, default=0.001, help='the alpha parameter for Adam optimizer')
    parser.add_argument('--epochs', type=int, default=15, help='the number of epochs in training')
    parser.add_argument('--project_name', default='test-mnist-wandb-project', help='the project name used for wandb logging')
    parser.add_argument('--architecture', default='simple_sequential')
    parser.add_argument('--dataset', default='MNIST')
    parser.add_argument('--wandb_api_key', required=True)
    args = parser.parse_args()
    return args.epochs, args.learning_rate, args.project_name, args.wandb_api_key


def create_model(alpha=0.001):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(784,)))
    model.add(tf.keras.layers.Dense(1000, activation='relu'))
    model.add(tf.keras.layers.Dense(500, activation='relu'))
    model.add(tf.keras.layers.Dense(200, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='linear'))
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(alpha), metrics=['accuracy'])
    return model


epochs, alpha, project_name, api_key = get_arguments()
(X, y), (X_test, y_test) = tf.keras.datasets.mnist.load_data(path='mnist.npz')
X = X.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)

model = create_model(alpha=alpha)
model_untrained = keras.models.clone_model(model)
wandb.login(key=api_key)
config = {
        "learning_rate": alpha,
        "architecture": "simple_sequential",
        "dataset": "MNIST",
        "epochs": epochs
    }

run = wandb.init(project=project_name, config=config)

model.fit(X, y, epochs=epochs, callbacks = [WandbMetricsLogger(log_freq=1)])
model_untrained.save('model_untrained.h5')
model.save('model_trained.h5')
(loss_train, accuracy_train) = model.evaluate(X, y)
(loss_test, accuracy_test) = model.evaluate(X_test, y_test)

artifact = wandb.Artifact(name = 'mnist_test_run', type = 'model', metadata = {'accuracy': accuracy_test})
artifact.add_file('model_untrained.h5')
artifact.add_file('model_trained.h5')
run.log_artifact(artifact)
run.finish()

