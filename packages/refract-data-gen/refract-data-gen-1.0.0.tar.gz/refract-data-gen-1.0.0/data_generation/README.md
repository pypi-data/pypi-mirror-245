# Data Synthesizer - Refract Plugin

## Dependency packages installed in NAS, /packages/custom_plugin/data_generation
```commandline
pip install great-expectations==0.13.4 -t "/packages/custom_plugin/data_generation";
pip install pandas-profiling -t "/packages/custom_plugin/data_generation";
pip install jinja2==3.0.0 -t "/packages/custom_plugin/data_generation";
pip install matplotlib==3.4.0 -t "/packages/custom_plugin/data_generation";
pip install tensorflow==2.11.0 -t "/packages/custom_plugin/data_generation";
pip install tensorflow-probability==0.19.0 -t "/packages/custom_plugin/data_generation";
pip install easydict==1.10 -t "/packages/custom_plugin/data_generation";
pip install evidently==0.2.1 -t "/packages/custom_plugin/data_generation";
pip install pandas -t "/packages/custom_plugin/data_generation";
pip install numpy -t "/packages/custom_plugin/data_generation";
pip install scikit-learn -t "/packages/custom_plugin/data_generation";
pip install typeguard -t "/packages/custom_plugin/data_generation";
pip install pytest -t "/packages/custom_plugin/data_generation";
pip install path==16.4.0 -t "/packages/custom_plugin/data_generation";
pip install refractio[all] -t "/packages/custom_plugin/data_generation";
pip uninstall dataclasses -y;
pip install git+https://gitlab+deploy-token-14:myUpFE_XRxShG53Hs6tV@git.lti-aiq.in/mosaic-decisions-2-0/mosaic-connector-python.git@1.0.29.3 -t "/packages/custom_plugin/data_generation";
```

# Environment variables used:
```python
import os
os.getenv("data_source")
os.getenv("numeric_columns")
os.getenv("reference_data_path")
os.getenv("sample_size")
os.getenv("categorical_columns")
os.getenv("set_conditional")
os.getenv("learning_rate")
os.getenv("epoch")
os.getenv("conditional_columns")
os.getenv('output_path')
os.getenv('filter_condition')
os.getenv('default_container_size')
```
