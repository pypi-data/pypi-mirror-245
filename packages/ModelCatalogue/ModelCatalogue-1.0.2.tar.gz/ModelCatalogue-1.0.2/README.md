# ModelCatalogue

Generates 5 tables to monitor the propensity model performance. <br>
Five tables are for:
1. Propensity Score Distribution
2. Decile Curves
3. Gain Charts
4. AUC Score
5. SHAP Analysis

### How to install
* python3 -m pip install -i https://test.pypi.org/simple/ ModelCatalogue==1.0.2

### How to use
```
# import package
from ModelCatalogue.ModelCatalogue import ModelCatalogue

# Parameters are described in ModelCatalogue.py
MC = ModelCatalogue(model=model, 
                    feature_processor_name ='fp', 
                    model_name = 'clf',
                    df=df_combined, 
                    target_name="max_cancel_request",
                    project_name=self.project_name, 
                    snapshot_date=self.snapshot_date.isoformat(),
                    logger=self.project_configs.logger,
                    dev_mode=True,
                    check_final_plots=False,
                    #data_in_pyspark=True,
                    #model_version=''
                    )

```

### Example:
* example.txt

### For Production Pipeline
* A parameter "dev_mode" should be False
