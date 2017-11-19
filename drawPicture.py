# encoding=utf-8
import matplotlib.pyplot as plt
from pylab import *                                 #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

def drwPic(y1,y2,y3,y4,y5,y6,title):
    x = [1, 2, 3, 5, 8,10]
    #plt.plot(x, y, 'ro-')
    #plt.plot(x, y1, 'bo-')
    plt.xlim(0.5, 10.5)  # 限定横轴的范围
    if title=="ST":
        plt.ylim(-1, 500)  # 限定纵轴的范围
    if title=="Ecoli":
        plt.ylim(-1,350)
    plt.plot(x, y1, marker='o', ls="-.",mec='r', mfc='w',label=u'xgboost')
    plt.plot(x, y2, marker='*', ls="--",ms=7,mec='r', mfc='w',label=u'LR')
    plt.plot(x, y3, marker='s', ls=":",mec='r', mfc='w',label=u'NB')
    plt.plot(x, y4, marker='>', ls="--", mec='r', mfc='w',label=u'SVM')
    plt.plot(x, y5, marker='x', mec='r', mfc='w',label=u'MS_Align+')
    plt.plot(x, y6, marker='D',mec='y', mfc='w',label=u'MS-Topdown')
    plt.legend()  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"FDR(%)") #X轴标签
    plt.ylabel("Number of Identified PSM") #Y轴标签
    st_title="ST(total:4460 PSM,target PSM:1725)"
    ecoli_title="Ecoli(total:1848 PSM,target PSM:925)"
    if title=="ST":
        plt.title(st_title) #标题
    if title=="Ecoli":
        plt.title(ecoli_title) #标题
    plt.grid(True,linestyle = "--")
    plt.show()
if __name__ == "__main__":
    st_xgb=[208,230,260,341,395,423]
    st_lr=[32,64,95,159,259,323]
    st_nb=[28,61,95,153,250,299]
    st_svm=[49,98,146,220,323,397]
    st_align=[46,61,97,153,259,310]
    st_topdown=[60,103,126,187,288,347]

    ecoli_xgb=[84,155,179,214,290,310]
    ecoli_lr=[37,50,72,155,203,238]
    ecoli_nb=[20,29,48,77,140,155]
    ecoli_svm=[16,33,40,86,150,164]
    ecoli_align=[15,24,38,66,118,140]
    ecoli_topdown=[30,44,53,91,180,180]
    drwPic(st_xgb,st_lr,st_nb,st_svm,st_align,st_topdown,"ST")
    drwPic(ecoli_xgb,ecoli_lr,ecoli_nb,ecoli_svm,ecoli_align,ecoli_topdown,"Ecoli")