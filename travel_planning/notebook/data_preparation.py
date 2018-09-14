import pandas as pd
import time
from duration_by_mapbox import MapboxDistance

mapbox_api_key = None
md = MapboxDistance(mapbox_api_key)
RATE_INTERVAL = 60
RATE_LIMIT = 60

def prepare_dataset(csv_path):
    df = pd.read_csv(csv_path)
    df = df.reset_index()
    df.columns = [c.strip() for c in df.columns]
   
    return df


def add_start_point(df, start_point_info):
    assert isinstance(start_point_info, dict)

    assert all([k in start_point_info.keys() for k in ["name", "lat", "long"]])
    df.loc[-1] = {**{"index":-1, "hours":8}, **start_point_info}
    return df


def generate_edge_dataset(df, edge_path, service):
    edge_df = pd.DataFrame([{"from": i, "to": df.index[r]} for i in df.index for r in range(len(df.index)) if i!=df.index[r]])
    edge_df["from_xy"] = edge_df.apply(lambda x: (df.iloc[x['from']].long, df.iloc[x['from']].lat), axis=1)
    edge_df["to_xy"] = edge_df.apply(lambda x: (df.iloc[x['to']].long, df.iloc[x['to']].lat), axis=1)
    edge_df["walking"], edge_df["driving"] = None, None
    edge_df['lat'] = edge_df["from_xy"].apply(lambda x: x[1])
    edge_df['long'] = edge_df["from_xy"].apply(lambda x: x[0])
    combi = list(zip(edge_df['from'].tolist(), edge_df['to'].tolist()))
    count_updates = 0
    start_time = time.time()
    for c in combi:
        print("combi: {}".format(c))
        result_dict = edge_df[(edge_df['walking'].isnull()) & (edge_df['from'].isin(c)) & (edge_df['to'].isin(c))][['from_xy', "to_xy"]].to_dict()
        if result_dict['from_xy'] and result_dict['to_xy']:
            res_index = list(result_dict['from_xy'].keys())
            coords = [result_dict['from_xy'][res_index[0]], result_dict['from_xy'][res_index[1]]]
            walking, driving = md.get_duration(*coords, service=service)
            for enum, rindex in enumerate(res_index):
                edge_df.at[rindex, "walking"] = walking[enum]
                edge_df.at[rindex, "driving"] = driving[enum]
            print("updated")
            count_updates+=2
        print(count_updates, RATE_LIMIT)
        if count_updates == RATE_LIMIT:
            sleep_seconds = abs(time.time()-(start_time+RATE_INTERVAL))
            print("have to wait {} seconds".format(sleep_seconds))
            time.sleep(sleep_seconds)
            count_updates = 0
            start_time = time.time()
    edge_df.to_csv(edge_path)
    return edge_df
