
import pandas as pd
import numpy as np
import pickle
import os
import shap


model_path = "../static/model/"
data_path = "../static/intermediate/"

def get_model(model_version, model_name, this_model_name):
    #target_name = "race_lgm_主催者コード_2_UMAREN_ARE"
    model_folder = model_path + model_version + '/' + model_name + '/'

    with open(model_folder + this_model_name + '.pickle', 'rb') as f:
        model = pickle.load(f)
    return model

def lightgbm_importance(model):
    importance = pd.DataFrame({"特徴": model.feature_name(), "重要度": model.feature_importance()}).sort_values(
        ["重要度", "特徴"], ascending=False)
    return importance

def get_shap(model, exp_data, i ):
    shap.initjs()
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(exp_data)
    force_plot = shap.force_plot(explainer.expected_value[i], shap_values[i][0, :], exp_data.iloc[0, :])
    decision_plot = shap.decision_plot(explainer.expected_value[i], shap_values[i][0, :], exp_data.iloc[0, :])
    return force_plot

def predict_v4_model(target_date, race_id, target):
    # target = ['１着', '２着', '３着']
    model_name = 'raceuma_lgm'
    intermediate_folder = "../static/"
    class_list = ['主催者コード']
    cls_val = '主催者コード'
    exp_data = pd.read_pickle(intermediate_folder + convert_date_to_str(target_date) + '_exp_data.pkl')
    exp_data = exp_data[exp_data["RACE_KEY"] == race_id]
    val = get_val_list(exp_data, cls_val)[0]
    # 対象の競馬場のデータを取得する
    filter_df = get_filter_df(exp_data, cls_val, val, class_list)
    # 予測を実施
    if not filter_df.empty:
        this_model_name = model_name + "_" + cls_val + '_' + val + '_' + target
        pred_df = predict_race_lgm(this_model_name, filter_df)


def predict_race_lgm(self, this_model_name, temp_df):
    temp_df = temp_df.replace(np.inf,np.nan).fillna(temp_df.replace(np.inf,np.nan).mean()).reset_index()
    exp_df = temp_df.drop(self.index_list, axis=1).to_numpy()
    if os.path.exists(self.model_folder + this_model_name + '.pickle'):
        with open(self.model_folder + this_model_name + '.pickle', 'rb') as f:
            model = pickle.load(f)
        y_pred = model.predict(exp_df)
        pred_df = pd.DataFrame(y_pred, columns=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        base_df = pd.DataFrame({"RACE_KEY": temp_df["RACE_KEY"], "NENGAPPI": temp_df["NENGAPPI"]})
        pred_df = pd.concat([base_df, pred_df], axis=1)
        pred_df = pred_df.set_index(["RACE_KEY", "NENGAPPI"])
        pred_df = pred_df.stack().reset_index().rename(columns={"level_2":"UMABAN", 0: "prob"})
        pred_df = pred_df[pred_df["UMABAN"] != 0]
        pred_df.loc[:, "pred"] = 0
        return pred_df
    else:
        return pd.DataFrame()

def convert_date_to_str(date):
    """ yyyy/MM/ddの文字列をyyyyMMddの文字型に変換する

    :param str date: date yyyy/MM/dd
    :return: str yyyyMMdd
    """
    return date.replace('/', '')

def get_val_list(df, cls_val):
    val_list = df[cls_val].drop_duplicates().astype(str)
    return val_list

def get_filter_df(df, cls_val, val, class_list):
    query_str = cls_val + " == " + val
    filter_df = df.query(query_str)
    # 分類対象のデータを削除
    filter_df.drop(class_list, axis=1, inplace=True)
    return filter_df