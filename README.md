# ft_linear_regression

The goal of the project is to implement a simple linear regression with a single feature.

``` python3 predict.py ```  or  ``` python3 predict.py mileage``` used to predict the price of a car for a given mileage.

```python3 train.py [-h] [--animation] [--thetas] [--graph] [--warmStart] [--iterations ITERATIONS] [--learningRate LEARNINGRATE] ```  used to train model - it will read dataset file
and perform a linear regression on the data.


Optional arguments are:
```
  -h, --help            show this help message and exit
  --animation, -a       Animation of linear function evolving.
  --thetas, -t          Animation for thetas evolving.
  --graph, -g           If set, draws a graph of linear function.
  --warmStart, -w       Training with thetas from the file (if exists).
  --iterations ITERATIONS, -i ITERATIONS
                        Set the number of iterations (default is 1000)
  --learningRate LEARNINGRATE, -l LEARNINGRATE
                        To set a number of iterations (default is 500)
```

Graphs are interactive on Unix and static on Linux.

Full subject: https://cdn.intra.42.fr/pdf/pdf/13331/en.subject.pdf

