snowflake_table_names={
     # if dev_mode and not check_final_plots: 
        'sf_hist_dev'         : 'DEV.DS.MODEL_CATALOGUE_HIST_DEV',
        'sf_table_decile_dev' : 'DEV.DS.MODEL_CATALOGUE_DECILE_DEV',
        'sf_table_gain_dev'   : 'DEV.DS.MODEL_CATALOGUE_GAIN_DEV',
        'sf_table_auc_dev'    : 'DEV.DS.MODEL_CATALOGUE_AUC_DEV',
        'sf_table_shap_dev'   : 'DEV.DS.MODEL_CATALOGUE_SHAP_DEV',

    # debugging mode and check the final plot with actual data
    # elif dev_mode and check_final_plots:
        'sf_hist_dev_plot'         : 'DEV.DS.MODEL_CATALOGUE_HIST_DEV_ACTUAL_RESULTS',
        'sf_table_decile_dev_plot' : 'DEV.DS.MODEL_CATALOGUE_DECILE_DEV_ACTUAL_RESULTS',
        'sf_table_gain_dev_plot'   : 'DEV.DS.MODEL_CATALOGUE_GAIN_DEV_ACTUAL_RESULTS',
        'sf_table_auc_dev_plot'    : 'DEV.DS.MODEL_CATALOGUE_AUC_DEV_ACTUAL_RESULTS',
        'sf_table_shap_dev_plot'   : 'DEV.DS.MODEL_CATALOGUE_SHAP_DEV_ACTUAL_RESULTS',

    # prod mode
    # elif not dev_mode: 
        'sf_hist_prod'         : 'DEV.DS.MODEL_CATALOGUE_HIST',
        'sf_table_decile_prod' : 'DEV.DS.MODEL_CATALOGUE_DECILE',
        'sf_table_gain_prod'   : 'DEV.DS.MODEL_CATALOGUE_GAIN',
        'sf_table_auc_prod'    : 'DEV.DS.MODEL_CATALOGUE_AUC',
        'sf_table_shap_prod'   : 'DEV.DS.MODEL_CATALOGUE_SHAP'   
}