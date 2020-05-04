import pandas as pd
import numpy as np
import shap

import pickle

def calc_return_rate(bet_df):
    result = bet_df["結果"].sum()
    bet = bet_df["金額"].sum()
    if bet != 0:
        return result / bet * 100
    else:
        return 0

def calc_cut_sr(sr, cut_list):
    # print(cut_sr.index.values.categories.left.values) # seriesのラベルを取得する際に手間がかかる
    cut_sr = pd.cut(sr, cut_list, right=False).value_counts(sort=False)
    return cut_sr

def get_weekly_summary_bet_df(bet_df):
    weekly_summary_bet_df = bet_df[["日付", "式別", "式別名", "金額", "結果", "合計"]]
    weekly_summary_bet_df.loc[:, "年月"] = weekly_summary_bet_df["日付"].apply(lambda x: x.strftime("%Y%m%d"))
    weekly_summary_bet_df = weekly_summary_bet_df.groupby(["年月", "式別名"]).sum().groupby(level=1).cumsum()
    weekly_summary_bet_df.loc[:, "回収率"] = round(weekly_summary_bet_df["結果"] / weekly_summary_bet_df["金額"] * 100, 1)
    return weekly_summary_bet_df

def get_daily_summary_bet_df(bet_df):
    daily_summary_bet_df = bet_df[["日付", "式別", "式別名", "金額", "結果", "合計"]].groupby(["日付","式別", "式別名"]).sum().reset_index()
    return daily_summary_bet_df.sort_values(["日付", "式別"])

def get_summary_bet_df(bet_df):
    summary_bet_df = bet_df[["式別", "式別名", "金額", "結果", "合計"]].groupby(["式別", "式別名"]).sum().reset_index()
    summary_bet_df = summary_bet_df.append(pd.Series([10, "合計", summary_bet_df["金額"].sum(), summary_bet_df["結果"].sum(), summary_bet_df["合計"].sum()], index= summary_bet_df.columns) ,ignore_index=True)
    return summary_bet_df.sort_values("式別")

def get_place_bet_df(bet_df):
    temp_daily_bet_df = bet_df[["競走コード", "場名", "合計", "結果", "金額"]].groupby(["競走コード", "場名"]).sum().reset_index()
    temp_daily_bet_df.loc[:, "的中"] = temp_daily_bet_df.apply(lambda x: 1 if x["結果"] > 0 else 0, axis=1)
    temp_daily_bet_df.loc[:, "レース"] = 1
    place_bet_df = temp_daily_bet_df[["場名", "合計", "結果", "金額", "的中", "レース"]].groupby("場名").sum().reset_index()
    return place_bet_df

def get_daily_bet_df(bet_df):
    daily_bet_df = bet_df[["日付", "合計", "結果", "金額"]].groupby("日付").sum().reset_index()
    # daily_bet_df = daily_bet_df[daily_bet_df["金額"] != 0].copy()
    daily_bet_df.loc[:, "回収率"] = daily_bet_df["結果"] / daily_bet_df["金額"] * 100
    return daily_bet_df.sort_values("日付")


def get_race_summary_df(race_df, haraimodoshi_dict):
    base_race_df = race_df[["競走コード", "場名"]]
    base_race_df = pd.merge(base_race_df, haraimodoshi_dict["umaren_df"], on="競走コード")
    race_summary_df = base_race_df[["場名", "払戻"]].groupby("場名").median().reset_index()
    return race_summary_df


def get_summary_rank1_raceuma_sr(raceuma_df):
    rank1_raceuma_df = raceuma_df[raceuma_df["馬券評価順位"] == 1]
    summary_rank1_raceuma_df = rank1_raceuma_df["確定着順"].value_counts()
    return summary_rank1_raceuma_df

def get_daily_rank1_raceuma_df(raceuma_df):
    rank1_raceuma_df = raceuma_df[raceuma_df["馬券評価順位"] == 1]
    daily_rank1_raceuma_df = rank1_raceuma_df[["年月日", "単勝配当", "複勝配当"]].groupby("年月日").mean().reset_index()
    return daily_rank1_raceuma_df.sort_values("年月日")


def get_shap_sr(race_id, raceuma_df, umaban):
    # データ取得
    # race_id = 22005014410
    base_exp_data = pd.read_pickle("./static/intermediate/lb_v5_predict/raceuma_lgm/20200430_exp_data.pkl")
    filter_exp_data = base_exp_data[base_exp_data["RACE_KEY"] == race_id]
    exp_data = filter_exp_data.drop(["RACE_KEY", "NENGAPPI", "主催者コード"], axis=1).reset_index(drop=True)
    base_raceuma_df = raceuma_df[["競走コード", "馬番"]].sort_values("馬番").reset_index()
    exp_data = exp_data[exp_data["UMABAN"] == umaban]

    # target encoding
    target_flag = "WIN_FLAG"
    label_list = exp_data.select_dtypes(include=object).columns.tolist()

    for label in label_list:
        exp_data.loc[:, label] = _target_encoding(exp_data[label], target_flag + '_tr_' + label)

    # 不要列削除
    with open('./static/model/lb_v5/raceuma_lgm/raceuma_lgm_主催者コード_2_WIN_FLAG_feat_columns.pickle', 'rb') as f:
        imp_features = pickle.load(f)

    exp_data = exp_data.replace(np.inf, np.nan).fillna(exp_data.replace(np.inf, np.nan).mean()).reset_index(drop=True)
    exp_data = exp_data[imp_features]#.to_numpy()

    with open('./static/model/lb_v5/raceuma_lgm/raceuma_lgm_主催者コード_2_WIN_FLAG.pickle', 'rb') as f:
        model = pickle.load(f)
    shap.initjs()
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(exp_data)
    shap_df = pd.DataFrame(shap_values[1], columns=exp_data.columns)
    shap_df["expected_value"] = explainer.expected_value[1]
    exp_data["expected_value"] = "expected_value"
    shap_df = pd.concat([base_raceuma_df, shap_df], axis=1)
    shap_sr = shap_df[shap_df["馬番"] == umaban].drop(["index", "競走コード", "馬番"], axis=1).iloc[0]#.sort_values()
    pd.set_option('display.max_columns', 3000)
    pd.set_option('display.max_rows', 3000)
    print(len(shap_sr))
    print(exp_data.shape)
    print(exp_data)
    print(shap_sr)
    shap_df = pd.DataFrame({"col_name": exp_data.columns, "shap_value": shap_sr, "org_value": exp_data.iloc[0]})
    shap_df.loc[:, "name"] = shap_df.apply(lambda x: x["col_name"] + "_" + str(x["org_value"]), axis=1)
    print(shap_df)
    return shap_sr

def load_dict(dict_name, dict_folder):
    """ エンコードした辞書を呼び出す

    :param str dict_name: 辞書名
    :return: encodier
    """
    with open(dict_folder + dict_name + '.pkl', 'rb') as f:
        return pickle.load(f)

def _target_encoding(sr, dict_name):
    tr = load_dict(dict_name, "./static/dict/lb_v5/")
    sr_tr = tr.transform(sr)
    return sr_tr
