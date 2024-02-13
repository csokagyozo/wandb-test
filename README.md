# wandb-test
W&amp;B integration 101: the simplest starter kit possible  
1. register at wand.ai, get your api key: <api_key>

## then run the python file
2a. ``python3 mnist-wandb-test.py --project_name test-mnist-wandb-project --epochs 5 --learning_rate 0.001 --wandb_api_key <api_key>`` 

## or do it the docker way
2. docker pull csokagyozo/mnist_wandb_test:latest 
3. run ``docker run csokagyozo/mnist_wandb_test:latest --project_name test-mnist-wandb-project --epochs 5 --learning_rate 0.001 --wandb_api_key <api_key>``  

## finally
check you W&amp;B dashboard. enjoy!
