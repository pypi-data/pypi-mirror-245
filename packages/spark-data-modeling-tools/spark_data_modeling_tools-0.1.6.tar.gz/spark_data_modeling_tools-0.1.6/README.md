# spark_data_modeling_tools

[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)

spark_data_modeling_tools is a Python library that implements styles in the Dataframe

## Installation

The code is packaged for PyPI, so that the installation consists in running:

```sh
pip install spark-data-modeling-tools --user --upgrade
```

## Usage
```sh
from spark_data_modeling_tools import dm_generated_table_refused
```

```sh

UPLOAD PATH_BUI


%%writefile tablitas.txt
t_pmol_finc_gl_ac_mthly_balances
t_pbtq_spectrum_gm_oper_ctpty


nro_sda = "39984"
project_name = "Golden Data"
sprint_name = "SP1"
nro_q = "Q4"
scrum_master =  "jonathan quiza"
collaborator_dm = "Erika Salazar"
comment_resolution = "[JQP]: Se solicita el reuso de la fuente para el proyecto Golden Data, para agregar reglas expertas"
comment_history = "[JQP]: No se requiere historia"
add_dashboard_ingesta_procesamiento = "Si"


dm_generated_table_refused(path_bui=None,
                               path_tables=None,
                               nro_sda=None,
                               project_name=None,
                               sprint_name=None,
                               nro_q=None,
                               scrum_master=None,
                               collaborator_dm=None,
                               comment_resolution=None,
                               comment_history=None,
                               add_dashboard_ingesta_procesamiento=None)
                               
                               
                               
                              
```



```



## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).

## New features v1.0

## BugFix

- choco install visualcpp-build-tools

## Reference

- Jonathan Quiza [github](https://github.com/jonaqp).
- Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
