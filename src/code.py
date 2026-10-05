import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# L0任务1
def task1():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False 
    Data = {'发电': 7062.04, '自用': 6500, '弃电': 428.37, '下网': 200}
    utilization_rate = (Data['自用'] / Data['发电']) * 100

    plt.bar(list(Data.keys()), list(Data.values()), color='skyblue')
    plt.title('能量分布')
    plt.xlabel('种类')
    plt.ylabel('能量(MWh)')
    plt.savefig('results/能量分布条形图.png')
    plt.show()
    return Data, utilization_rate

# L0任务2
def generate_and_save_data2():
    rng = np.random.default_rng(seed=42)
    before_RTO = rng.normal(loc=10835, scale=75, size=100)
    after_RTO = rng.normal(loc=10298, scale=50, size=100)

    RTO_Data = pd.DataFrame({'before': before_RTO, 'after': after_RTO})
    RTO_Data.to_csv('data/RTO_Data.csv', index=False, encoding='utf-8-sig')
    Data = pd.read_csv('data/RTO_Data.csv').melt(var_name='阶段', value_name='数值')
    return Data

def calculate_and_plot_stats2(Data):
    result = Data.groupby('阶段')['数值'].quantile([0.25, 0.5, 0.75]).unstack()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    from pandas.api.types import CategoricalDtype
    order = ['before', 'after']
    Data['阶段'] = Data['阶段'].astype(CategoricalDtype(order, ordered=True))
    Data.boxplot(column='数值', by='阶段', ax=axes[0])
    axes[0].set_title('')
    plt.suptitle('')
    axes[0].set_ylabel('数值')
    axes[0].set_xticks([1, 2])
    axes[0].set_xticklabels(['RTO之前', 'RTO之后'])

    data_before = Data[Data['阶段'] == 'before']['数值']
    data_after = Data[Data['阶段'] == 'after']['数值']
    plot_data = [data_before, data_after]
    axes[1].boxplot(plot_data)
    axes[1].set_xticks([1, 2])
    axes[1].set_xticklabels(['RTO之前', 'RTO之后'])
    axes[1].set_ylabel('数值')
    plt.xlabel('阶段')
    fig.suptitle('RTO前后对照图', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/RTO前后对照图.png')
    plt.show()
    return result

# L0任务3
def ramp_load(start, end, dt, rate=4.38):
    t_data = []
    t_load, t= start, 0
    if rate > 0:
        while t_load < end:
            t_data.append([t, t_load])
            t = t + dt
            t_load = t_load + rate * dt
            if t_load > end:
                t_load = end
                t_data.append([t, t_load])
                break
        return np.array(t_data)
    elif rate < 0:
        while t_load > end:
            t_data.append([t, t_load])
            t = t + dt
            t_load = t_load + rate * dt
            if t_load < end:
                t_load = end
                t_data.append([t, t_load])
                break
        return np.array(t_data)

def generate_and_save_data3():
    data_inc = ramp_load(30, 70, 1)
    load_increase = pd.DataFrame({'时间': data_inc[:,0], '负荷': data_inc[:,1]})
    data_dec = ramp_load(90, 10, 1, -4.38)
    load_decrease = pd.DataFrame({'时间': data_dec[:,0], '负荷': data_dec[:,1]})
    data_inc_persec = ramp_load(30, 70, 1, 0.073)
    load_increase_persec = pd.DataFrame({'时间': data_inc_persec[:,0], '负荷': data_inc_persec[:,1]})
    data_dec_persec = ramp_load(90, 10, 1, -0.073)
    load_decrease_persec = pd.DataFrame({'时间': data_dec_persec[:,0], '负荷': data_dec_persec[:,1]})
    return load_increase, load_decrease, load_increase_persec, load_decrease_persec

def calculate_and_plot_stats3(load_increase, load_decrease, load_increase_persec, load_decrease_persec):
    fig, ax = plt.subplots()
    fig.suptitle('负荷变化曲线图', fontsize=16)
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 100)
    ax.set_xlabel("时间(min)")
    ax.set_ylabel("负荷(%)")
    labels = ['负荷增加', '负荷减少', '负荷增加(每秒)', '负荷减少(每秒)']
    linestyles = ['-', '-', '--', '--']
    colors = ['#ff0000','#0000ff', '#ff8080', "#8080ff"]
    for (i, k) in enumerate([load_increase, load_decrease, load_increase_persec, load_decrease_persec]):
        ax.plot(k['时间'], k['负荷'], color = colors[i], linestyle = linestyles[i], label=labels[i])
    ax.legend(loc='best')
    plt.savefig('results/负荷变化曲线图.png')
    plt.show()

if __name__ == '__main__':
    print('Q1、论文摘要说风光实际消纳率 96.8%、下网电量占比小于 4.2%，但你只有一天的数据：\
          发电 7062.04 MWh、弃电 428.37 MWh。你能用 Python 算利用率，并解释为什么和 96.8% 不一样吗？')
    Data, utilization_rate = task1()
    print(utilization_rate)

    print('Q2、论文说 RTO 投用后吨氨电耗中位数降约 536.75 kWh/t。你能用 Python 模拟两组数据，\
          算出中位数、四分位区间，并判断这个降幅是否稳定吗？')
    Data = generate_and_save_data2()
    result2 = calculate_and_plot_stats2(Data)
    print(result2)

    print('Q3、论文说合成氨负荷调节速率实测 4.38%/min，负荷范围 10%~110%。如果从 30% 升到 70%，\
          需要多久？如果从 90% 降到 10%，又需要多久？')
    inc, dec, inc_s, dec_s = generate_and_save_data3()
    calculate_and_plot_stats3(inc, dec, inc_s, dec_s)
    print('负荷变化时间见results文件夹内问题三折线图')