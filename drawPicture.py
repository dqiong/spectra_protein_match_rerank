# encoding=utf-8
import matplotlib.pyplot as plt
from pylab import *                                 #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

def drawNoAssmble(y1,y2,y4,y5,y6,title):
    x = [1, 2, 3, 5, 8,10]
    #plt.plot(x, y, 'ro-')
    #plt.plot(x, y1, 'bo-')
    plt.xlim(0.5, 10.5)  # 限定横轴的范围
    if title=="ST":
        plt.ylim(-1, 300)  # 限定纵轴的范围
    if title=="Ecoli":
        plt.ylim(-1,250)
    plt.plot(x, y1, marker='o', ls="-.",mec='r', mfc='w',label=u'xgboost')
    plt.plot(x, y2, marker='*', ls="--",ms=7,mec='r', mfc='w',label=u'LR')
    plt.plot(x, y4, marker='>', ls="--", mec='r', mfc='w',label=u'SVM')

    plt.plot(x, y5, marker='x', mec='r', mfc='w',label=u'MS_Align+')
    plt.plot(x, y6, marker='D',mec='y', mfc='w',label=u'MS-Topdown')
    plt.legend()  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"FDR(%)") #X轴标签
    plt.ylabel("Number of Identified PSM") #Y轴标签
    st_title="ST(total:4460 PSM,target PSM:1725) pvalue rank"
    ecoli_title="Ecoli(total:1848 PSM,target PSM:925) pvalue rank"
    if title=="ST":
        plt.title(st_title) #标题
    if title=="Ecoli":
        plt.title(ecoli_title) #标题
    plt.grid(True,linestyle = "--")
    plt.show()
def drwPic(y1,y2,y3,y4,y5,y6,title):
    x = [1, 2, 3, 5, 8,10]
    #plt.plot(x, y, 'ro-')
    #plt.plot(x, y1, 'bo-')
    plt.xlim(0.5, 10.5)  # 限定横轴的范围
    if title=="ST":
        plt.ylim(-1, 300)  # 限定纵轴的范围
    if title=="Ecoli":
        plt.ylim(-1,250)
  #  plt.plot(x, y1, marker='o', ls="-.",mec='r', mfc='w',label=u'xgboost')
  #  plt.plot(x, y2, marker='*', ls="--",ms=7,mec='r', mfc='w',label=u'LR')
 #   plt.plot(x, y4, marker='>', ls="--", mec='r', mfc='w',label=u'SVM')
    plt.plot(x, y3, marker='s', ls=":",mec='r', mfc='w',label=u'ASSMBLE')
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
    st_xgb=[27,59,84,128,189,265]
    st_lr=[21,56,80,129,197,246]
    st_ass=[30,65,95,135,200,265]
    st_svm=[28,59,87,125,194,246]
    st_align=[28,62,86,124,193,246]
    st_topdown=[23,51,88,131,195,242]

    st_xgb_evalue=[27,59,84,128,189,265]
    st_lr_evalue=[21,56,80,129,197,246]
    st_svm_evalue=[28,59,87,125,194,246]

    st_xgb_peaks=[23,51,86,129,202,246]
    st_lr_peaks=[14,35,51,104,176,217]
    st_svm_peaks=[19,52,82,132,195,252]

    st_xgb_pvalue=[25,52,68,104,165,211]
    st_lr_pvalue=[20,53,71,105,181,243]
    st_svm_pvalue=[29,42,70,102,165,204]


    ecoli_xgb_evalue=[10,28,46,76,115,126]
    ecoli_lr_evalue=[12,40,59,74,108,144]
    ecoli_svm_evalue=[13,26,39,58,105,130]

    ecoli_xgb_peaks=[36,36,36,89,90,155]
    ecoli_lr_peaks=[74,127,160,160,209,209]
    ecoli_svm_peaks=[38,38,38,91,99,156]

    ecoli_xgb_pvalue=[8,13,29,53,78,110]
    ecoli_lr_pvalue=[10,23,33,75,124,166]
    ecoli_svm_pvalue=[14,25,33,75,131,166]

    ecoli_xgb=[10,28,46,76,115,126]
    ecoli_lr=[32,63,84,103,147,173]
    ecoli_ass=[40,44,59,95,115,161]
    ecoli_svm=[38,38,38,99,91,155]
    ecoli_align=[13,26,39,58,105,130]
    ecoli_topdown=[36,36,36,89,89,153]
    # drawNoAssmble(st_xgb_evalue,st_lr_evalue,st_svm_evalue,st_align,st_topdown,u"ST")
    #drawNoAssmble(st_xgb_peaks,st_lr_peaks,st_svm_peaks,st_align,st_topdown,u"ST")
    #drawNoAssmble(st_xgb_pvalue,st_lr_pvalue,st_svm_pvalue,st_align,st_topdown,u"ST")
    #drawNoAssmble(ecoli_xgb_peaks,ecoli_lr_peaks,ecoli_svm_peaks,ecoli_align,ecoli_topdown,u"Ecoli")
    # drawNoAssmble(ecoli_xgb_evalue,ecoli_lr_evalue,ecoli_svm_evalue,ecoli_align,ecoli_topdown,u"Ecoli")
    #drawNoAssmble(ecoli_xgb_pvalue,ecoli_lr_pvalue,ecoli_svm_pvalue,ecoli_align,ecoli_topdown,u"Ecoli")

    #drwPic(st_xgb,st_lr,st_ass,st_svm,st_align,st_topdown,"ST")
    drwPic(ecoli_xgb,ecoli_lr,ecoli_ass,ecoli_svm,ecoli_align,ecoli_topdown,"Ecoli")