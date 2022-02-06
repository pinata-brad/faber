[![Pylint](https://github.com/pinata-brad/faber/actions/workflows/pylint.yml/badge.svg?branch=main&event=push)](https://github.com/pinata-brad/faber/actions/workflows/pylint.yml)

# faber

### what is faber? 
faber is a lightweight pipelining tool for machine learning and data projects

### why though?
so our pipelines look clean - like the below
```python
from faber import node
from data_science.nodes.quick_ml import *

ml_pipe = [
    node(
        prepare_ml,
        ['df_processed', 'ml_params'],
        ['df_master_train', 'df_master_test'],
    ),
    node(
        train_models,
        ['df_master_train', 'ml_params'],
        ['ml'],
    ),
    node(
        get_best_params,
        ['ml'],
        ['best_params']
    ),
]
```
and our data is connected externally and defined in a yaml file; meaning if a data location changes only one place is changed
. wildcards are also supported with {{}}
```yaml
df_raw:
    filepath: data/00_raw/df_raw.csv
    read_func: read_csv_pandas
    
df_processed:
    filepath: data/01_master/df_processed_{{run_number}}.csv
    read_func: read_csv_pandas
    write_func: write_csv_pandas
    
output_profile:
    filepath: data/02_insight/output_profile.csv
    read_func: read_csv_pandas
    write_func: write_csv_pandas
    
ml:
    filepath: data/models/ml_object.pickle
    read_func: read_pickle
    write_func: write_pickle
    
```

### install using
 
```shell script
git clone https://github.com/pinata-brad/faber.git
cd faber
python3 setup.py sdist bdist_wheel && pip install dist/faber-0.0.3.tar.gz 
```
