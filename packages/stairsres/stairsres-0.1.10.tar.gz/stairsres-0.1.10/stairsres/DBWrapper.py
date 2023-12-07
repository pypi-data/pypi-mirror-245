import os
from idbadapter.schedule_loader import Schedules, GRANULARY, TYPEDLVL2, PROCESSED
from idbadapter import MschmAdapter
import pandas as pd
from datetime import datetime, timedelta


class DBWrapper:
    def __init__(self, mschm_adapter, adapter, unit='', level=GRANULARY):
        self.mschm_adapter = mschm_adapter
        self.adapter = adapter
        self.level = level
        self.unit = unit

    def get_works(self):
        works = self.adapter.get_works_names(work_type=self.level)
        return works

    def get_resources(self):
        res = self.adapter.get_resources_names(res_type="granulary")
        return res

    def get_act_names(self):
        df = self.adapter.get_all_works_name()
        return df

    def get_res_names(self):
        df = self.adapter.get_all_resources_name()
        return df

    def get_models(self, name_of_works: str):
        return self.mschm_adapter.get_model(name_of_works)

    def save_model(self, model: dict):
        self.mschm_adapter.save_model_to_db(model=model)

    def get_precalculation(self, name_of_works: list[str]):
        return self.mschm_adapter.get_precalculation(name_of_works=name_of_works)

    def save_precalculation(self, precalc: dict):
        self.mschm_adapter.save_precalculation_to_db(data=precalc)

    def delete_model(self, work_name):
        self.mschm_adapter.delete_model(work_name=work_name)

    def get_data(self, works_names, res_names):
        frames = []
        for p in self.adapter.from_names(
                works=works_names,    # список работ
                resources=res_names,  # список ресурсов
                ceil_limit=-1,        # ограничение по количеству строк на один запрос (-1 - выдать все)
                objects_limit=-1,     # ограничение на кол-во одновременно выдаваемых объектов (-1 - выдать все)
                crossing=False,       # переключение логики выбора объектов по работам и ресурсам (True - И, False - ИЛИ)
                key=self.level
        ):
            frames.append(p)

        data = pd.concat(frames)
        # data = data.loc[data['measurement_unit'].isin(self.unit+['-'])]
        data = data.loc[data[self.level["column"]].isin(works_names + res_names)]

        # This part is tightly dependent on schedule_loader
        data.loc[data[self.level["column"]] == '-', self.level["column"]] = data.loc[
            data[self.level["column"]] == '-', 'name']

        data = data[[self.level["column"]] + list(data.columns[8:])]

        # final_df = pd.DataFrame()
        # for _, df in data.groupby("object_name"):
        #     df = df[[self.level["column"]] + list(df.columns[8:])]
        del data['start_date']
        del data['finish_date']
        data = data.groupby(self.level["column"]).sum()
        data = data.reset_index()
        data = data.transpose()
        data.columns = data.iloc[0]
        data.drop(index=data.index[0], axis=0, inplace=True)
        data = data.rename_axis(None, axis=1)
        data = data.drop(data.index[0])
        # data.reset_index(drop=True, inplace=True)

        # base = datetime.today()
        # date_list = [
        #     (base + timedelta(days=x)).strftime("%d.%m.%Y")
        #     for x in range(final_df.shape[0])
        # ]
        # final_df.index = date_list
        # final_df.fillna(0, inplace=True)

        return data
