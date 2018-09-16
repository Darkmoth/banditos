import pandas as pd
import math

def get_simple_ucb(row, centercalc):
    div1 = 2 * math.log(row['total']) / row['count']
    ucb = math.sqrt(div1)
    return ucb + row[centercalc]

def get_tuned_ucb(row, centercalc, spreadcalc):
    cnt = max(row['count'],1)
    row_total = max(row['total'],1)
    div1 = 2 * math.log(row_total) / cnt
    min1 = min(0.25, row[spreadcalc] + div1)
    div2 = math.log(row_total) / cnt
    ucb = math.sqrt(div2 * min1)
    return ucb + row[centercalc]

def mad_function(df):
    const_med = df.median()
    df_med = abs(df - const_med)
    v_mad = df_med.median()
    return v_mad

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
    # scale the min and max values
    df_min = df_num.transform(lambda x: x - x.min()).transform(lambda x: x/x.max())
    # where df_min is null and passed value is not NAN set quality = 0.5
    null_calc = df_min.isnull()
    score_exists = df_num.notnull()
    m = null_calc & score_exists
    df_quality = df_min.mask(m, 0.5).to_frame('Quality')
    return df_quality