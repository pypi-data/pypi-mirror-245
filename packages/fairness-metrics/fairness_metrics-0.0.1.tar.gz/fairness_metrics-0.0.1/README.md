# fairness_metrics_package
## Description:
This package is used to determine the fairness of an AutoML classification or regression model. It can also be used to determine the fairness of self-made models. 
## Features
Within the package there are 10 fairness metrics under 3 categories:
| | | Metric/Function Name | Function |
| ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| <td rowspan="3">-</td> | All Metrics | run_all(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | All Classification Metrics | run_all_classification(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | All Regression Metrics | run_all_regression(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
| <td rowspan="2">Parity-based Metrics</td> | Statistical/Demographic Parity | stat_demo_parity(_dataset_, _predictedColumn_, _group_) |
|  | Disparte Impact | disparte_impact(_dataset_, _actualColumn_, _group_) |
| <td rowspan="6">Confusion Matrix-based Metrics</td> | Equal Opportunity | equal_opportunity(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | Equalized Odds | equalized_odds(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | Overall Accuracy Equality | overall_accuracy_equality(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | Conditional Use Accuracy Equality | conditional_use_accuracy_equality(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | Treatment Equality | treatment_equality(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | Equalizing Disincentives | equalizing_disincentives(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
| <td rowspan="2">Score-based Metrics</td> | Differences in Squared Error | differences_in_squared_error(_dataset_, _predictedColumn_, _actualColumn_, _group_) |
|  | Balance between Subgroups | balance_btwn_subgroups(_dataset_, _predictedColumn_, _actualColumn_, _group_) |

## Installation
