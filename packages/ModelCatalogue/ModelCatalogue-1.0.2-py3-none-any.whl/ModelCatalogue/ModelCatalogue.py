import pandas as pd
import pyspark
import pyspark.sql.functions as F
import numpy as np
import logging
import random
from matplotlib import pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
import shap

from ds_luigi.helpers.util_helpers import load_dataframe_to_snowflake_table
from smmt.helpers import get_sampling_rate
from datasciencetools.db.db_collections import DBCollections

from .constants import snowflake_table_names

def get_snowflake_table_name(dev_mode, check_final_plots, project_name, snapshot_date, model_version=''):
    snow = DBCollections(support_pandas=True, environment=str(random.randint(0, 100000))).snowflake_poc

    # debugging mode
    if dev_mode and not check_final_plots:
        sf_hist = snowflake_table_names['sf_hist_dev']
        sf_table_decile = snowflake_table_names['sf_table_decile_dev']
        sf_table_gain = snowflake_table_names['sf_table_gain_dev']
        sf_table_auc = snowflake_table_names['sf_table_auc_dev']
        sf_table_shap = snowflake_table_names['sf_table_shap_dev']

    # debugging mode and check the final plot with actual data
    elif dev_mode and check_final_plots:
        sf_hist = snowflake_table_names['sf_hist_dev_plot']
        sf_table_decile = snowflake_table_names['sf_table_decile_dev_plot']
        sf_table_gain = snowflake_table_names['sf_table_gain_dev_plot']
        sf_table_auc = snowflake_table_names['sf_table_auc_dev_plot']
        sf_table_shap = snowflake_table_names['sf_table_shap_dev_plot']

        # remove if duplicates in snowflake table
        for table in [sf_hist, sf_table_decile, sf_table_gain, sf_table_auc, sf_table_shap]:
            snow.query(f'''DELETE FROM {table} 
                           WHERE project='{project_name}' and snapshot_date='{snapshot_date}'
                             and model_version='{model_version}'; ''')
    # prod mode
    elif not dev_mode:
        sf_hist = snowflake_table_names['sf_hist_prod']
        sf_table_decile = snowflake_table_names['sf_table_decile_prod']
        sf_table_gain = snowflake_table_names['sf_table_gain_prod']
        sf_table_auc = snowflake_table_names['sf_table_auc_prod']
        sf_table_shap = snowflake_table_names['sf_table_shap_prod']

        # check if there are duplicates in Prod table
        for table in [sf_hist, sf_table_decile, sf_table_gain, sf_table_auc, sf_table_shap]:
            duplicate_check = snow.query(f'''SELECT * 
                                             FROM {table} 
                                             WHERE project='{project_name}' and snapshot_date='{snapshot_date}' 
                                               and model_version='{model_version}'; ''')
            if not duplicate_check.empty:
                raise ValueError(
                    f"There are the same project name, model version, and snapshot date in Prod table. Please remove them from '{table}' and proceed")

    return sf_hist, sf_table_decile, sf_table_gain, sf_table_auc, sf_table_shap


class ModelCatalogue:
    ''' Generates 3 tables for decile curves, gain chart, and auc score. The tables will be loaded to snowflake tables.

         Attributes:
            project_name: Project name.
            snapshot_date: Target date.
            logger: Logging. If you don't use Logging function, it can be created with "from smmt.custom_logger import create_prod_logger" and "logger = create_prod_logger(logger_name='_your_logger_name')"
            bin_no: Number of quantiles.
            data_in_pyspark: Data type of input data. If Pandas dataframe, data_in_pyspark=False. Default is True.
            dev_mode: Enables to debug with small sample data to reduce the run time and output the results in snowflake DEV table. Default is True and it should be False for production pipeline. If dev_mode=False and there are duplicated project name and snapshot_date in snowflake table, then it will raise an error.
            check_final_plots: Enables to test the code with actual data in DEV mode. check_final_plots=True and dev_mode=True helps checking the final test with actual data before proceeding to Prod. If there are the same project name and snapshot_date, the old one will be overwritten.
            model_version: String column to define model version. Default is an empty string.
    '''

    def __init__(self, project_name: str, snapshot_date: str, logger: logging.Logger, bin_no=20, data_in_pyspark=True,
                 dev_mode=True, check_final_plots=False, model_version=''):
        self.project_name = project_name
        self.snapshot_date = snapshot_date
        self.bin_no = bin_no
        self.logger = logger
        self.data_in_pyspark = data_in_pyspark
        self.dev_mode = dev_mode
        self.check_final_plots = check_final_plots
        self.model_version = model_version

    def sample_data(self, df: pyspark.sql.DataFrame, target_variable_name: str) -> pd.DataFrame:
        ''' Checks if data is in pyspark dataframe.
            Samples data and returns it in pandas dataframe.

        Attributes:
            df: pyspark dataframe with input features and a target feature.
            target_variable_name: Column name for target variable in df.
        '''
        # Sample/prep data
        if self.dev_mode and not self.check_final_plots:
            sample_size = 1_000
        else:
            sample_size = 2_000_000

        if self.data_in_pyspark:
            frac = get_sampling_rate(df.count(), sample_size)

            if self.dev_mode and not self.check_final_plots:
                # for 1,000 data sampling, it will add 20 positive cases (F.col(target_variable_name)==1)
                df_0: pd.DataFrame = df.filter(F.col(target_variable_name) == 0).sample(fraction=frac,
                                                                                        seed=42).toPandas()
                df_1: pd.DataFrame = df.filter(F.col(target_variable_name) == 1).limit(20).toPandas()
                data: pd.DataFrame = pd.concat([df_0, df_1], ignore_index=True).reset_index(drop=True).copy()
            else:
                data: pd.DataFrame = df.sample(fraction=frac, seed=42).toPandas()
        else:
            if self.dev_mode and not self.check_final_plots:
                frac = get_sampling_rate(len(df), sample_size)
                # for 1,000 data sampling, it will add 20 positive cases (F.col(target_variable_name)==1)
                df_0: pd.DataFrame = df[df[target_variable_name] == 0].sample(frac=frac, random_state=42)
                df_1: pd.DataFrame = df[df[target_variable_name] == 1].sample(n=20, random_state=42)
                data: pd.DataFrame = pd.concat([df_0, df_1], ignore_index=True).reset_index(drop=True).copy()
            else:
                data: pd.DataFrame = df.copy()

        data.rename(columns={target_variable_name: "actual"}, errors="raise", inplace=True)
        data['actual'] = data['actual'].astype(int)
        data.columns = data.columns.str.lower()
        self.logger.info(f"Sampling data completed")

        return data

    def predict_probability(self, data: pd.DataFrame, model: Pipeline, sf_hist: str) -> pd.DataFrame:
        '''
         Attributes:
            data: Pandas dataframe with input features and a target variable.
            model: Model pipeline that is trained previsouly.
            sf_hist: Snowflake table name to upload propensity score histogram
        '''
        df_labels = pd.DataFrame()
        df_labels['probas'] = model.predict_proba(data)[:, 1]
        df_labels['actual'] = data['actual']
        df_labels['quant'] = pd.qcut(df_labels['probas'].rank(method='first'), self.bin_no, labels=False)
        df_labels['quant'] = df_labels['quant'] + 1
        self.logger.info(f"Predict proba completed")

        # Histogram of propensity scores
        hist_df = plt.hist(df_labels.probas, bins=100)
        hist_df_front = pd.DataFrame({'project': self.project_name,
                                      'snapshot_date': self.snapshot_date,
                                      'model_version': self.model_version,
                                      'proba_bins': hist_df[1][:-1],
                                      'cnt': [int(cnt) for cnt in hist_df[0]]})
        # Update SF table
        load_dataframe_to_snowflake_table(snowflake_table=sf_hist, df=hist_df_front)
        self.logger.info(f"Histogram table is loaded to {sf_hist}")

        return df_labels

    # Generate and upload decile chart to SF table
    def decile_chart(self, df_labels: pd.DataFrame, sf_table_decile: str) -> pd.DataFrame:
        decile = df_labels.groupby(['quant']).mean()
        decile = decile.round(15)
        decile['project'] = self.project_name
        decile['snapshot_date'] = self.snapshot_date
        decile['model_version'] = self.model_version
        decile = decile.reset_index()[['project', 'snapshot_date', 'quant', 'actual', 'probas', 'model_version']]

        # Update SF table
        load_dataframe_to_snowflake_table(snowflake_table=sf_table_decile, df=decile)
        self.logger.info(f"Decile table is loaded to {sf_table_decile}")

        return decile

    # Generate and upload gain chart to SF table
    def gain_chart(self, df_labels: pd.DataFrame, sf_table_gain: str) -> pd.DataFrame:
        gain = df_labels.groupby(['quant']).agg({'probas': ['mean', 'count']})
        gain.columns = gain.columns.droplevel()
        gain['sum'] = gain['mean'] * gain['count']
        gain = gain.append(pd.DataFrame({'sum': 0, 'count': 0}, index=[self.bin_no]))
        gain.sort_index(ascending=False, inplace=True)

        gain_final = (100.0 * gain.expanding().sum() / gain.sum()).reset_index(drop=True)
        gain_final.rename(columns={'count': 'population', 'sum': 'conversion'}, errors="raise", inplace=True)
        gain_final['project'] = self.project_name
        gain_final['snapshot_date'] = self.snapshot_date
        gain_final['model_version'] = self.model_version
        gain_final = gain_final.reset_index().rename(columns={'index': 'quant'}, errors="raise")[
            ['project', 'snapshot_date', 'quant', 'population', 'conversion', 'model_version']]

        # Update SF table
        load_dataframe_to_snowflake_table(snowflake_table=sf_table_gain, df=gain_final)
        self.logger.info(f"Gain table is loaded to {sf_table_gain}")

        return gain_final

    # Generate and upload auc score to SF table
    def auc_score(self, df_labels: pd.DataFrame, sf_table_auc: str) -> pd.DataFrame:
        auc_score = np.round(roc_auc_score(df_labels['actual'], df_labels['probas']), 15)
        auc_df = pd.DataFrame([[self.project_name, self.snapshot_date, auc_score, self.model_version]],
                              columns=['project', 'snapshot_date', 'auc_score', 'model_version'])

        # Update SF table
        load_dataframe_to_snowflake_table(snowflake_table=sf_table_auc, df=auc_df)
        self.logger.info(f"AUC table is loaded to {sf_table_auc}")

        return auc_df

    # Ganerate and upload feature importance with SHAP values to SF table
    def shap_value(self, data: pd.DataFrame, model: Pipeline, feature_processor_name: str, model_name: str,
                   sf_table_shap: str) -> pd.DataFrame:
        '''
         Attributes:
            data: Pandas dataframe with input features and a target variable.
            model: Model pipeline that is trained previsouly.
            feature_processor_name: Key name for feature processing in Pipeline (model).
            model_name: Key name for ML model in Pipeline (model).
        '''
        if self.dev_mode and not self.check_final_plots:
            data_shap = data
        else:
            data_shap = data.sample(n=50_000, random_state=42)
        data_shap = model[feature_processor_name].transform(data_shap)

        model_ml = model[model_name]
        explainer = shap.TreeExplainer(model_ml, data_shap)
        shap_values = explainer(data_shap, check_additivity=False)
        mean_abs_shap_by_feature = np.abs(shap_values.values).mean(axis=0)

        df_shap = pd.DataFrame()
        df_shap["feature"] = model[feature_processor_name].get_feature_names_out()
        df_shap["feature"] = df_shap["feature"].str.replace('_', ' ').str.title()
        df_shap["shap_value"] = mean_abs_shap_by_feature
        df_shap["project"] = self.project_name
        df_shap["snapshot_date"] = self.snapshot_date
        df_shap['model_version'] = self.model_version

        df_shap = df_shap[['project', 'snapshot_date', 'feature', 'shap_value', 'model_version']]

        # Update SF table
        load_dataframe_to_snowflake_table(snowflake_table=sf_table_shap, df=df_shap)
        self.logger.info(f"SHAP table is loaded to {sf_table_shap}")

        return df_shap