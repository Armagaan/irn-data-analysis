# Data Analysis of the Indian Railway Network
![Indian Train](train.png)

# Blog
We wrote a supporting blog for this project. Find it [here](https://glamorous-snowdrop-fc2.notion.site/Data-Analysis-of-the-Indian-Railway-Network-1c06d44fe4944bd19ca4ea9b10aede15?pvs=4).

# Environment
Don't run these commands as a script. Run them one by one in this order in the terminal.
```bash
conda create -n irn_delay python=3.10 --yes
conda activate irn_delay

pip install torch==1.11.0+cpu torchvision==0.12.0+cpu torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cpu

# required for installing torch geometric
conda install -c conda-forge cxx-compiler --yes

TORCH="1.11.0"; CUDA="cpu"
pip install torch-scatter -f https://pytorch-geometric.com/whl/torch-${TORCH}+${CUDA}.html

# The following command from pyg's documentation doesn't work.
# pip install torch-sparse -f https://pytorch-geometric.com/whl/torch-${TORCH}+${CUDA}.html

# Use this instead. Followed this: https://github.com/pytorch/pytorch/issues/74454
# This takes a while.
pip install torch-sparse==0.6.14

pip install torch-geometric
pip install torch-geometric-temporal

conda install ipykernel ipywidgets matplotlib seaborn networkx --yes
conda install -c anaconda beautifulsoup4 --yes
```

# Code
| Notebook/Script | Description |
|-----------------------|--------------------------|
| `src/irn_data_analysis.ipynb` | Data analysis of the IRN |
| `src/json_to_graph.ipynb` | Create a temporal graph dataset where the target is the number of delayed trains at a station. |
| `src/train_tgnn.ipynb` | Train a TGNN to predict the number of delayed trains at a station. |
| `src/json_to_graph_time.ipynb` | Create a temporal graph dataset where the target is the average delay at a station. |
| `src/train_tgnn_time.ipynb` | Train a TGNN to predict the average delay at a station. |
| `src/scrapper.ipynb` | Contains functions for scrapping train data (delay, info, connectivity). |
