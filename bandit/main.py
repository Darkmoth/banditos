import pandas as pd

def get_load_factor(cnt):
    inflection_point = 200
    adj_cnt = min(cnt,inflection_point)
    increment = 0.5 / inflection_point
    load_factor = adj_cnt * increment
    return 1 - load_factor

def reduce(df, col):
    df['age'] = df.index.max() - df.index
    g = df.sort_values('age', ascending=False).groupby(col)
    df['age_rank'] = g['age'].rank(method='min')
    df_newest = df[df.age_rank == 1]
    df_oldest = df[df.age_rank > 1]
    data_cnt = len(df_oldest.index)
    load_factor = get_load_factor(data_cnt)
    data_len = int(round(data_cnt * load_factor,0))
    print(data_cnt, load_factor, data_len)
    df_oldest = df_oldest.sort_values('age', ascending=False).tail(data_len)
    df_new = pd.concat([df_newest,df_oldest])
    df_new = df_new.sort_values('age', ascending=False).drop(['age','age_rank'], axis=1)
    return df_new

def get_quality(df_num):
    df_min = df_num.transform(lambda x: x - x.min()).transform(lambda x: x/x.max())
    df_quality = df_min.to_frame('Quality')
    return df_quality