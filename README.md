# Replicate the results

## Preparing the Python installation

In order to install all necessary packages, please run the following commands within a new virtual environment:

```python
pip install -e lingreg/
pip install -r requirements.txt
```

## Downloading and preprocessing the data

We provide a makefile that runs all the necessary code.
You can run the following two commands to download all repositories and preprocess the data:

```console
make download
make preprocessing
```

## Replicate the analysis

To replicate the analysis with the full results table, please run the following command:

```console
make measure
```

## Plotting the distribution of sites per pattern

You can find a script that creates the plot for the distribution of sites per pattern in the folder "plots/".
