import sys
import math
import scipy.stats as stats
from bamt.networks.continuous_bn import ContinuousBN


class ResTimeModel:
    def __init__(self, dbwrapper):
        self.wrapper = dbwrapper

    @staticmethod
    def nearest_value(precalculation: dict, volume_for_work: dict, work_name: str) -> float:
        volumes_list = list(precalculation[work_name].keys())
        min_dist = sys.maxsize
        for volume in volumes_list:
            if abs(volume - volume_for_work) < min_dist:
                result = volume
                min_dist = abs(volume - volume_for_work)

        return result

    def get_resources_volumes(self, work_name, work_volume, resource_name=None) -> dict:
        precalc = self.wrapper.get_precalculation([work_name])
        if len(precalc) == 0:
            return {}
        worker_reqs = {}
        worker_reqs['worker_reqs'] = []
        res = resource_name
        if resource_name is None:
            vol_0 = list(precalc[work_name].keys())[0]
            res = list(precalc[work_name][vol_0]['10%'].keys())
        
        for r in res:
            volume_for_work = self.nearest_value(precalc, work_volume, work_name)
            min_res_value = precalc[work_name][volume_for_work]['10%'][r]
            max_res_value = precalc[work_name][volume_for_work]['90%'][r]
            volume = precalc[work_name][volume_for_work]['50%'][r]
            worker_reqs['worker_reqs'].append({'kind': r,
                                               'volume': volume,
                                               'min_count': min_res_value,
                                               'max_count': max_res_value})

        return worker_reqs

    def get_time(self, work_volume: dict, resources: dict, quantile) -> float:
        q = 0.5
        if quantile == '0.9':
            q = 0.1
        if quantile == '0.1':
            q = 0.9
        work_name = list(work_volume.keys())[0]
        print(work_name)
        bn_params = self.wrapper.get_models(work_name)
        model_work_name = ''
        model_res_names = []
        for k in bn_params['info']['types']:
            if '_prod' in k:
                model_work_name = k
            else:
                model_res_names.append(k)
        
        bn = ContinuousBN()
        bn.load(bn_params)
        roots = []
        for n in bn.nodes:
            if '_prod' not in str(n):
                roots.append(str(n))
        test_data = {}
        for res_bn_name in roots:
            for res_name in resources:
                if res_name in res_bn_name:
                    test_data[res_bn_name] = resources[res_name]
                    break
        mu, var = bn.get_dist(model_work_name, test_data)

        if var == 0:
            prod = mu
        elif math.isnan(mu):
            prod = 0
        else:
            prod = stats.norm.ppf(q=q, loc=mu, scale=var)
        if prod == 0:
            return 0
        if prod < 0:
            return math.ceil(work_volume[work_name] / mu)
        else:
            return math.ceil(work_volume[work_name] / prod)

    def estimate_time(self, work_unit, worker_list, mode='0.5'):
        if not worker_list:
            return 0
        work_name = work_unit['name']
        work_volume = work_unit['volume']
        res_dict = {}
        for req in worker_list:
            res_dict[req['name']] = req['_count']
        time = self.get_time(work_volume={work_name: work_volume}, resources=res_dict, quantile=mode)
        return time
