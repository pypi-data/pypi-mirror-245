# NiCo

Developed by Ankit Agrawal (c) Grün lab 2023


Find covariation patterns between interacted cell types from image-based single cell resolution of spatial data.

A package that performs cell type annotations on spatial transcriptomics data, find the niche interactions and covariation patterns between interacted cell types.

Under construction! Ready for use! Currently experimenting and planning!


## Install the NiCo package using the conda environment.  

```shell
conda create -n nicoUser python=3.11
conda activate nicoUser
pip install nico-sc-sp
pip install jupyterlab
```

# Required packages built upon
By default, these packages should install automatically.
But if any version conflict exists, the user can install the specific version independently using pip command.
```shell
scanpy==1.9.6
seaborn==0.12.2
scipy==1.11.3
matplotlib==3.7.3
numpy==1.26.1
gseapy==1.0.6
xlsxwriter==3.1.9
numba==0.58.1
pydot==1.4.2
KDEpy==1.1.8
leidenalg
```

# Import the functions from the Python prompt in the following way.  

```python
from nico import Annotations as sann
from nico import Interactions as sint
from nico import Covariations as scov
```

# Documentations

Please follow the NiCo documentation here.

http://htmlpreview.github.io/?https://github.com/ankitbioinfo/nicodoc/blob/main/docs/_build/html/index.html

# Tutorials
Please follow the NiCo tutorial here.

https://github.com/ankitbioinfo/nico_tutorial


# Check out more:
Thanks to the following two utils packages to develop NiCo.

SCTransformPy

https://github.com/atarashansky/SCTransformPy

pyliger

https://github.com/welch-lab/pyliger
