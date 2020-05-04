import pandas as pd
import pyodbc
from datetime import datetime as dt
from datetime import timedelta
import glob
import pickle

class GetData(object):
    """
    ClassMethodでデータを返してみる
    """

    @classmethod
    def get_target_file_list(cls, start_date, end_date, type):
        # type race, raceuma, bet, haraimodoshi
        stored_folder_path = "./static/data/"
        start_dt = dt.strptime(start_date, "%Y-%m-%d")
        end_dt = dt.strptime(end_date, "%Y-%m-%d")
        days_num = (end_dt - start_dt).days + 1

        yearmonth_list = []
        for i in range(days_num):
            yearmonth_list.append((start_dt + timedelta(days=i)).strftime("%Y%m"))
        all_file_list = glob.glob(stored_folder_path + type + "/*.pickle")
        yearmonth_list = sorted(list(set(yearmonth_list)))
        target_list = []
        for ym in yearmonth_list:
            l_in = [s for s in all_file_list if ym in s]
            if len(l_in) != 0:
                target_list.append(l_in[0])
        return sorted(list(target_list))

    @classmethod
    def get_race_data(cls, start_date, end_date):
        file_list = cls.get_target_file_list(start_date, end_date, 'race')
        race_df = pd.DataFrame()
        for file in file_list:
            temp_df = pd.read_pickle(file)
            race_df = race_df.append(temp_df)
        race_df = race_df.query(f"月日 >= '{start_date}' and 月日 <= '{end_date}'")
        return race_df

    @classmethod
    def get_raceuma_data(cls, start_date, end_date):
        file_list = cls.get_target_file_list(start_date, end_date, 'raceuma')
        raceuma_df = pd.DataFrame()
        for file in file_list:
            temp_df = pd.read_pickle(file)
            raceuma_df = raceuma_df.append(temp_df)
        raceuma_df.loc[:, "馬名"] = raceuma_df.apply(lambda x : str(x["馬番"]).zfill(2) + "_" + x["馬名"], axis=1)
        raceuma_df = raceuma_df.query(f"年月日 >= '{start_date}' and 年月日 <= '{end_date}'")
        return raceuma_df

    @classmethod
    def get_raceuma_prev_df(cls, term_start_date, term_end_date, ketto_toroku_bango_list):
        term_raceuma_df = cls.get_raceuma_data(term_start_date, term_end_date).query("データ区分 =='7'").drop("馬名", axis=1)
        print(term_raceuma_df.shape)
        raceuma_prev_df = term_raceuma_df[term_raceuma_df["血統登録番号"].isin(ketto_toroku_bango_list)]
        print(raceuma_prev_df.shape)
        return raceuma_prev_df

    @classmethod
    def get_bet_data(cls, start_date, end_date):
        file_list = cls.get_target_file_list(start_date, end_date, 'bet')
        bet_df = pd.DataFrame()
        for file in file_list:
            temp_df = pd.read_pickle(file)
            bet_df = bet_df.append(temp_df)
        bet_df.loc[:, "結果"] = bet_df["結果"] * bet_df["金額"] / 100
        bet_df.loc[:, "式別名"] = bet_df["式別"].apply(lambda x : cls.trans_baken_type(x))
        bet_df.loc[:, "合計"] = bet_df["結果"] - bet_df["金額"]
        race_df = cls.get_race_data(start_date, end_date)
        bet_df = pd.merge(bet_df, race_df[["競走コード", "場名"]], on="競走コード")
        bet_df = bet_df.query(f"日付 >= '{start_date}' and 日付 <= '{end_date}'")
        return bet_df

    @classmethod
    def get_haraimodoshi_table_base(cls, start_date, end_date):
        file_list = cls.get_target_file_list(start_date, end_date, 'haraimodoshi')
        haraimodoshi_df = pd.DataFrame()
        for file in file_list:
            temp_df = pd.read_pickle(file)
            haraimodoshi_df = haraimodoshi_df.append(temp_df)
        haraimodoshi_df = haraimodoshi_df.query(f"データ作成年月日 >= '{start_date}' and データ作成年月日 <= '{end_date}'")
        return haraimodoshi_df

    @classmethod
    def bk_get_race_data(cls, start_date, end_date):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\BaoZ\DB\Baoz.MDB;'
        )
        cnxn = pyodbc.connect(conn_str)
        select_sql = 'SELECT データ区分, 競走コード, 月日, 距離, トラック種別コード, 主催者コード, 競走番号, 場コード, 場名, グレードコード, 競走種別コード, 競走条件コード, 発走時刻, 頭数, 天候コード, 前３ハロン, 前４ハロン' \
                     ', 後３ハロン, 後４ハロン, トラックコード,  馬場状態コード, 前半タイム, 予想計算済み, 予想勝ち指数, ペース, 初出走頭数, 混合, 予想決着指数, 投票フラグ, 波乱度, 馬券発売フラグ, 予想計算状況フラグ, メインレース, タイム指数誤差, 登録頭数, 回次, 日次 FROM レースT WHERE 月日 >= #' + \
                     start_date + '# AND 月日 <= #' + end_date + '#'
        df_org = pd.read_sql(select_sql, cnxn)
        cnxn.close()
        df = df_org.astype({'トラック種別コード': object, '主催者コード': object, '場コード': object, '競走種別コード': object, '競走条件コード': object,
                            'トラックコード': object,
                            '天候コード': object, '馬場状態コード': object, '投票フラグ': object, '波乱度': object, '馬券発売フラグ': object,
                            '予想計算状況フラグ': object})
        return_df = df[df["主催者コード"] == 2].copy()
        return return_df

    @classmethod
    def bk_get_raceuma_data(cls, start_date, end_date):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\BaoZ\DB\Baoz.ex.MDB;'
        )
        cnxn = pyodbc.connect(conn_str)
        select_sql = 'SELECT * FROM 出走馬T WHERE 年月日 >= #' + \
            start_date + '# AND 年月日 <= #' + end_date + '#'
        df_org = pd.read_sql(select_sql, cnxn)
        cnxn.close()
        df = df_org.astype({'血統登録番号': object, '性別コード': object, '展開コード': object, '騎手コード': object, '騎手所属場コード': object,
                            '見習区分': object, '調教師コード': object, '調教師所属場コード': object, '異常区分コード': object, '前走トラック種別コード':object})
        return df

    @classmethod
    def bk_get_bet_table_base(cls, start_date, end_date):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\BaoZ\DB\MasterDB\BaoZ-Bet.MDB;'
        )
        cnxn = pyodbc.connect(conn_str)
        select_sql = 'SELECT * FROM 投票記録T WHERE 日付 >= #' + \
            start_date + '# AND 日付 <= #' + end_date + '#'
        df_org = pd.read_sql(select_sql, cnxn)
        df_org.loc[:, "結果"] = df_org["結果"] * df_org["金額"] / 100
        df_org.loc[:, "式別名"] = df_org["式別"].apply(lambda x : cls.trans_baken_type(x))
        df_org.loc[:, "合計"] = df_org["結果"] - df_org["金額"]
        race_df = cls.get_race_data(start_date, end_date)
        df_org = pd.merge(df_org, race_df[["競走コード", "場名"]], on="競走コード")
        cnxn.close()
        df = df_org.astype(
            {'式別': object, 'レース種別': object, 'PAT_ID': object, '投票方法': object})
        return df

    @classmethod
    def trans_baken_type(cls, type):
        if type == 1:
            return '単勝　'
        elif type == 2:
            return '複勝　'
        elif type == 3:
            return '枠連　'
        elif type == 4:
            return '枠単　'
        elif type == 5:
            return '馬連　'
        elif type == 6:
            return '馬単　'
        elif type == 7:
            return 'ワイド'
        elif type == 8:
            return '三連複'
        elif type == 9:
            return '三連単'
        elif type == 0:
            return '合計　'

    @classmethod
    def bk_get_haraimodoshi_table_base(cls, start_date, end_date):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\BaoZ\DB\MasterDB\BaoZ-RA.MDB;'
        )
        cnxn = pyodbc.connect(conn_str)
        select_sql = 'SELECT * FROM 払戻T WHERE データ作成年月日 >= #' + \
            start_date + '# AND データ作成年月日 <= #' + end_date + '#'
        df_org = pd.read_sql(select_sql, cnxn)
        cnxn.close()
        df = df_org.astype({'不成立フラグ': object, '特払フラグ': object, '返還フラグ': object, '返還馬番情報': object, '返還枠番情報': object, '返還同枠情報': object, '単勝馬番1': object, '単勝馬番2': object, '単勝馬番3': object, '複勝馬番1': object, '複勝馬番2': object, '複勝馬番3': object, '複勝馬番4': object, '複勝馬番5': object, '枠連連番1': object, '枠連連番2': object, '枠連連番3': object, '馬連連番1': object, '馬連連番2': object, '馬連連番3': object, 'ワイド連番1': object, 'ワイド連番2': object,
                            'ワイド連番3': object, 'ワイド連番4': object, 'ワイド連番5': object, 'ワイド連番6': object, 'ワイド連番7': object, '枠単連番1': object, '枠単連番2': object, '枠単連番3': object, '馬単連番1': object, '馬単連番2': object, '馬単連番3': object, '馬単連番4': object, '馬単連番5': object, '馬単連番6': object, '三連複連番1': object, '三連複連番2': object, '三連複連番3': object, '三連単連番1': object, '三連単連番2': object, '三連単連番3': object, '三連単連番4': object, '三連単連番5': object, '三連単連番6': object})
        return df

    @classmethod
    def get_haraimodoshi_dict(cls, start_date, end_date):
        haraimodoshi_df = cls.get_haraimodoshi_table_base(start_date, end_date)
        tansho_df = cls.get_tansho_df(haraimodoshi_df)
        fukusho_df = cls.get_fukusho_df(haraimodoshi_df)
        umaren_df = cls.get_umaren_df(haraimodoshi_df)
        wide_df = cls.get_wide_df(haraimodoshi_df)
        umatan_df = cls.get_umatan_df(haraimodoshi_df)
        sanrenpuku_df = cls.get_sanrenpuku_df(haraimodoshi_df)
        sanrentan_df = cls.get_sanrentan_df(haraimodoshi_df)
        dict_haraimodoshi = {"tansho_df": tansho_df, "fukusho_df": fukusho_df, "umaren_df": umaren_df,
                             "wide_df": wide_df, "umatan_df": umatan_df, "sanrenpuku_df": sanrenpuku_df,
                             "sanrentan_df": sanrentan_df}
        return dict_haraimodoshi

    @classmethod
    def get_tansho_df(cls, df):
        """ 単勝配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        tansho_df1 = df[["競走コード", "単勝馬番1", "単勝払戻金1"]]
        tansho_df2 = df[["競走コード", "単勝馬番2", "単勝払戻金2"]]
        tansho_df3 = df[["競走コード", "単勝馬番3", "単勝払戻金3"]]
        df_list = [tansho_df1, tansho_df2, tansho_df3]
        return_df = cls.arrange_return_df(df_list)
        return return_df

    @classmethod
    def get_fukusho_df(cls, df):
        """ 複勝配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        fukusho_df1 = df[["競走コード", "複勝馬番1", "複勝払戻金1"]]
        fukusho_df2 = df[["競走コード", "複勝馬番2", "複勝払戻金2"]]
        fukusho_df3 = df[["競走コード", "複勝馬番3", "複勝払戻金3"]]
        fukusho_df4 = df[["競走コード", "複勝馬番4", "複勝払戻金4"]]
        fukusho_df5 = df[["競走コード", "複勝馬番5", "複勝払戻金5"]]
        df_list = [fukusho_df1, fukusho_df2, fukusho_df3, fukusho_df4, fukusho_df5]
        return_df = cls.arrange_return_df(df_list)
        return return_df

    @classmethod
    def get_wide_df(cls, df):
        """ ワイド配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        wide_df1 = df[["競走コード", "ワイド連番1", "ワイド払戻金1"]]
        wide_df2 = df[["競走コード", "ワイド連番2", "ワイド払戻金2"]]
        wide_df3 = df[["競走コード", "ワイド連番3", "ワイド払戻金3"]]
        wide_df4 = df[["競走コード", "ワイド連番4", "ワイド払戻金4"]]
        wide_df5 = df[["競走コード", "ワイド連番5", "ワイド払戻金5"]]
        wide_df6 = df[["競走コード", "ワイド連番6", "ワイド払戻金6"]]
        wide_df7 = df[["競走コード", "ワイド連番7", "ワイド払戻金7"]]
        df_list = [wide_df1, wide_df2, wide_df3, wide_df4, wide_df5, wide_df6, wide_df7]
        return_df = cls.arrange_return_df(df_list)
        return_df.loc[:, "馬番"] = return_df["馬番"].map(cls.separate_umaban)
        return return_df

    @classmethod
    def get_umaren_df(cls, df):
        """ 馬連配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        umaren_df1 = df[["競走コード", "馬連連番1", "馬連払戻金1"]]
        umaren_df2 = df[["競走コード", "馬連連番2", "馬連払戻金2"]]
        umaren_df3 = df[["競走コード", "馬連連番3", "馬連払戻金3"]]
        df_list = [umaren_df1, umaren_df2, umaren_df3]
        return_df = cls.arrange_return_df(df_list)
        return_df.loc[:, "馬番"] = return_df["馬番"].map(cls.separate_umaban)
        return return_df

    @classmethod
    def get_umatan_df(cls, df):
        """ 馬単配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        umatan_df1 = df[["競走コード", "馬単連番1", "馬単払戻金1"]]
        umatan_df2 = df[["競走コード", "馬単連番2", "馬単払戻金2"]]
        umatan_df3 = df[["競走コード", "馬単連番3", "馬単払戻金3"]]
        umatan_df4 = df[["競走コード", "馬単連番4", "馬単払戻金4"]]
        umatan_df5 = df[["競走コード", "馬単連番5", "馬単払戻金5"]]
        umatan_df6 = df[["競走コード", "馬単連番6", "馬単払戻金6"]]
        df_list = [umatan_df1, umatan_df2, umatan_df3, umatan_df4, umatan_df5, umatan_df6]
        return_df = cls.arrange_return_df(df_list)
        return_df.loc[:, "馬番"] = return_df["馬番"].map(cls.separate_umaban)
        return return_df

    @classmethod
    def get_sanrenpuku_df(cls, df):
        """  三連複配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        sanrenpuku1 = df[["競走コード", "三連複連番1", "三連複払戻金1"]]
        sanrenpuku2 = df[["競走コード", "三連複連番2", "三連複払戻金2"]]
        sanrenpuku3 = df[["競走コード", "三連複連番3", "三連複払戻金3"]]
        df_list = [sanrenpuku1, sanrenpuku2, sanrenpuku3]
        return_df = cls.arrange_return_df(df_list)
        return_df.loc[:, "馬番"] = return_df["馬番"].map(cls.separate_umaban)
        return return_df

    @classmethod
    def get_sanrentan_df(cls, df):
        """ 三連単配当のデータフレームを作成する。同着対応のため横になっているデータを縦に結合する。

        :param dataframe df:
        :return: dataframe
        """
        sanrentan1 = df[["競走コード", "三連単連番1", "三連単払戻金1"]]
        sanrentan2 = df[["競走コード", "三連単連番2", "三連単払戻金2"]]
        sanrentan3 = df[["競走コード", "三連単連番3", "三連単払戻金3"]]
        sanrentan4 = df[["競走コード", "三連単連番4", "三連単払戻金4"]]
        sanrentan5 = df[["競走コード", "三連単連番5", "三連単払戻金5"]]
        sanrentan6 = df[["競走コード", "三連単連番6", "三連単払戻金6"]]
        df_list = [sanrentan1, sanrentan2, sanrentan3, sanrentan4, sanrentan5, sanrentan6]
        return_df = cls.arrange_return_df(df_list)
        return_df.loc[:, "馬番"] = return_df["馬番"].map(cls.separate_umaban)
        return return_df

    @classmethod
    def arrange_return_df(cls, df_list):
        """ 内部処理用、配当データの列を競走コード、馬番、払戻に統一する

        :param list df_list: dataframeのリスト
        :return: dataframe
        """
        for df in df_list:
            df.columns = ["競走コード", "馬番", "払戻"]
        return_df = pd.concat(df_list)
        temp_return_df = return_df[return_df["払戻"] != 0]
        return temp_return_df

    @classmethod
    def separate_umaban(cls, x):
        """ 内部処理用。馬番結果の文字をリスト(4,6),(12,1,3)とかに変換する.0,00といった値の場合は０のリストを返す

        :param str x: str
        :return: list
        """
        umaban = str(x)
        if len(umaban) <= 2:
            return [0, 0, 0]
        if len(umaban) % 2 != 0:
            umaban = '0' + umaban
        if len(umaban) == 6:
            list_umaban = [int(umaban[0:2]), int(umaban[2:4]), int(umaban[4:6])]
        else:
            list_umaban = [int(umaban[0:2]), int(umaban[2:4])]
        return list_umaban
