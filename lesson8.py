#!/opt/anaconda3/bin/python
from re import A
import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import seaborn as sns

style.use('ggplot')


def visualize_data():
    # 读取 CSV 时，指定第一列（Date）为索引，并解析为日期类型
    df = pd.read_csv("sp500_joined_closes.csv", index_col=0, parse_dates=True)  # 读取包含所有股票收盘价的 CSV 文件
    df_corr = df.corr()  # 计算相关性矩阵，所有股票两两之间的相关系数，范围 -1 到 1
    print(df_corr.head())  # 打印相关性矩阵的前 5 行，用于查看数据

    data = df_corr.values  # 将 DataFrame 转换为 numpy 数组（纯数字矩阵）
    fig = plt.figure()  # 创建图形对象（画布）
    ax = fig.add_subplot(1, 1, 1)  # 添加子图，(1,1,1) 表示 1x1 网格中的第 1 个位置

    # heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    heatmap = ax.pcolormesh(data, cmap=plt.cm.RdYlGn)  # 绘制热力图，使用红-黄-绿配色方案
    fig.colorbar(heatmap)  # 添加颜色条，显示颜色与数值的对应关系
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)  # 设置 x 轴刻度位置在单元格中心（+0.5）
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)  # 设置 y 轴刻度位置在单元格中心
    ax.invert_yaxis()  # 反转 y 轴，使第一个股票在顶部
    ax.xaxis.tick_top()  # 将 x 轴刻度移到图表顶部

    column_labels = df_corr.columns  # 获取列标签（股票代码）
    row_labels = df_corr.index  # 获取行标签（股票代码）

    ax.set_xticklabels(column_labels)  # 设置 x 轴标签为股票代码
    ax.set_yticklabels(row_labels)  # 设置 y 轴标签为股票代码
    plt.xticks(rotation=90)  # 旋转 x 轴标签 90 度，竖着显示避免重叠
    heatmap.set_clim(-1, 1)  # 设置颜色范围：-1（完全负相关）到 1（完全正相关）
    plt.tight_layout()  # 自动调整布局，避免元素重叠
    plt.show()  # 显示图表

def visualize_data2():
    """Seaborn 热力图 - 每隔 10 个显示一个标签"""
    df = pd.read_csv("sp500_joined_closes.csv", index_col=0, parse_dates=True)
    df_corr = df.corr()
    
    # 每隔 10 个股票显示一个标签，避免标签过于拥挤
    n = 10
    tick_labels = [label if i % n == 0 else '' for i, label in enumerate(df_corr.columns)]
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(df_corr, 
                cmap='RdYlGn',        # 颜色方案：红-黄-绿
                center=0,              # 颜色中心点设为 0
                vmin=-1,               # 最小值 -1（完全负相关）
                vmax=1,                # 最大值 1（完全正相关）
                square=True,           # 方形单元格
                linewidths=0,          # 不显示网格线
                cbar_kws={"shrink": 0.8},  # 调整颜色条大小
                xticklabels=tick_labels,   # 每隔 n 个显示一个标签
                yticklabels=tick_labels)   # 每隔 n 个显示一个标签
    
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.title('S&P 500 Stock Correlation Heatmap', fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()

visualize_data()