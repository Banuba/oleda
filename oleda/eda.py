import numpy as np
import matplotlib.pyplot as pls 
import pandas as pd

from IPython.display import display, HTML
import seaborn as sns


from .eda_core import *
from .eda_core import __cramer_v_corr
from .eda_pairwise import pairwise_report
from .eda_anova import anova,two_way_anova

import warnings

warnings.filterwarnings("ignore")

#=====================#=====================#=====================
# dataset comparison  pairwise report
#=====================#=====================#=====================  

#def pairwise_report(df1,df2,target=None,ignore=[],nbrmax=20,full=True):
    # Compare two datasets:
    # df1      pandas dataframe     first dataset 
    # df2      pandas dataframe     second dataset
    # ignore  list                  features to ignore 
    # nbrmax  int                   max number of features (with max shap values) to print

#pairwise_report(df1,df2,target,ignore,nbrmax,full)

#for compatibility
print_report = pairwise_report      

#=====================#=====================#=====================
# single dataset  eda
#=====================#=====================#=====================  

#single dataset report
def report(df,target=None,ignore=[],nbrmax=20,full=True):
     return do_eda(df, target,ignore,nbrmax)  

    
#shap values
def  plot_shaps(df, target, ignore=[], nbrmax=20):
    #
    # plot shaps values
    # target should be binary or float
    # returns features list sorted by importance
    #    
    return plot_shap( df, target, ignore, nbrmax)

#=====================#=====================#=====================
# time series plots
#=====================#=====================#=====================
    
# plots n top feature values counts per day   
def plot_ntop_categorical_values_counts(df,feature,target,nbr_max=4,figsize=(20,4),linewidth=2.0,period="1d"):
    values=df[feature].value_counts()[:nbr_max].index.to_list()
    if  len(values)==0:
        return
    ax=df[df[feature]==values[0]][target].resample(period).count().plot(x_compat=True,figsize=figsize, grid=True,linewidth=linewidth)
    legend=[values[0]]
    for i in range(1,len(values)):
        df[df[feature]==values[i]][target].resample(period).count().plot(x_compat=True,figsize=figsize,ax=ax, grid=True, linewidth=2.0,title='{} per day'.format(feature))
        legend.append(values[i])

    if len(values) > 1:
        ax.lines[1].set_linestyle(":")
    ax.lines[0].set_linestyle("--")
    pls.legend(legend, bbox_to_anchor=(1.2, 0))
    pls.show()
    
    
def plot_ntop_categorical_values_sums(df,feature,target,nbr_max=4,figsize=(20,4),linewidth=2.0,period="1d"):
    values=df[feature].value_counts()[:nbr_max].index.to_list()
    if  len(values)==0:
        return
    ax=df[df[feature]==values[0]][target].resample(period).sum().plot(x_compat=True,figsize=figsize, grid=True,linewidth=2.0)
    legend=[values[0]]
    for i in range(1,len(values)):
        df[df[feature]==values[i]][target].resample(period).sum().plot(x_compat=True,figsize=figsize,ax=ax, grid=True, linewidth=linewidth,title='{} sum per {} per day'.format(target,feature))
        legend.append(values[i])

    if len(values) > 1:
        ax.lines[1].set_linestyle(":")
    ax.lines[0].set_linestyle("--")
    pls.legend(legend, bbox_to_anchor=(1.2, 0))
    pls.show()
    
def plot_ntop_categorical_values_means(df,feature,target,nbr_max=4,figsize=(20,4),linewidth=2.0,period="1d"):
    
    values=df[feature].value_counts()[:nbr_max].index.to_list()
    if  len(values)==0:
        return
    ax=df[df[feature]==values[0]][target].resample(period).mean().plot(x_compat=True,figsize=figsize, grid=True,linewidth=linewidth )
    legend=list()
    legend.append(values[0])
    for i in range(1,len(values)):
        df[df[feature]==values[i]][target].resample(period).mean().plot(x_compat=True,figsize=figsize,ax=ax, grid=True, linewidth=linewidth,title='{} % mean per {} per day'.format(target,feature))
        legend.append(values[i])

    if len(values) > 1:
        ax.lines[1].set_linestyle(":")
    ax.lines[0].set_linestyle("--")
    pls.legend(legend,bbox_to_anchor=(1.2, 0))
    pls.show()
    
    
#=====================#=====================#=====================#=====================
# continues
#=====================#=====================#=====================#=====================

def plot_cuts(df,feature,target,bins=None, figsize=(12,6)):
    
    if bins==None:
        bins=np.arange(df[feature].min(),df[feature].max(),(df[feature].max()-df[feature].min())/10.)
    
    fig, (ax1, ax2) = pls.subplots(ncols=2, figsize=figsize)
    pls.title('Histogram of {}'.format(feature)); 
    ax1.set_xlabel(feature); 
    ax1.set_ylabel('count');
    ax2.set_xlabel(feature); 
    ax2.set_ylabel(target);
    df.groupby(pd.cut(df[feature], bins=bins))[target].count().plot(kind='bar',ax=ax1)
    df.groupby(pd.cut(df[feature], bins=bins))[target].mean().plot(kind='bar',ax=ax2)
    pls.show()  
    
def plot_qcuts(df,feature,target,q=None, figsize=(8,4)):
    
    if q==None:
        q = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,0.9, 1]
    
    fig, (ax1, ax2) = pls.subplots(ncols=2, figsize=figsize)
    pls.title('Histogram of {}'.format(feature)); 
    ax1.set_xlabel(feature); 
    ax1.set_ylabel('count');
    ax2.set_xlabel(feature); 
    ax2.set_ylabel(target);
    df.groupby(pd.qcut(df[feature], q=q,duplicates='drop'))[target].count().plot(kind='bar',ax=ax1)
    df.groupby(pd.qcut(df[feature], q=q,duplicates='drop'))[target].mean().plot(kind='bar',ax=ax2)
    pls.show()    

                       
#=====================#=====================#=====================#=====================
# categorical 
#=====================#=====================#=====================#=====================

import seaborn as sns

def plot_stats(df,feature,target,max_nbr=20):
    end=max_nbr
    cat_count = df[feature].value_counts()
    cat_count = pd.DataFrame({feature: cat_count.index,'Count ': cat_count.values})
    cat_count.sort_values(by='Count ', ascending=False, inplace=True)

    cat_perc = df[[feature, target]].groupby([feature],as_index=False).mean()
    cat_perc=pd.merge(cat_perc,cat_count,on=feature)
    cat_perc.sort_values(by='Count ', ascending=False, inplace=True)
    
    hs=len(cat_count[:max_nbr])
    if(hs<=40):
        fig, (ax1, ax2) = pls.subplots(ncols=2, figsize=(12,6))
    else:
        fig, (ax1, ax2) = pls.subplots(nrows=2, figsize=(12,14))
        
    sns.set_color_codes("pastel")
    s = sns.barplot(ax=ax1, x = feature, y="Count ",order=cat_count[feature][:max_nbr],data=cat_count[:max_nbr])
    s.set_xticklabels(s.get_xticklabels(),rotation=90)   
    
    s = sns.barplot(ax=ax2, x = feature, y=target, order=cat_perc[feature][:max_nbr], data=cat_perc[:max_nbr])  
    s.set_xticklabels(s.get_xticklabels(),rotation=90)
        
    pls.ylabel('Percent ', fontsize=10)
    pls.tick_params(axis='both', which='major', labelsize=10)

    pls.show();

def plot_melt(df,feature,target1,target2,end=20):
    
    cat_count = df[feature].value_counts()
    cat_count = pd.DataFrame({feature: cat_count.index,'Count ': cat_count.values})
    cat_count.sort_values(by='Count ', ascending=False, inplace=True)

    cat_perc = df[[feature, target1]].groupby([feature],as_index=False).mean()
    cat_perc=pd.merge(cat_perc,cat_count,on=feature)

    cat_perc2 = df[[feature, target2]].groupby([feature],as_index=False).mean()
    cat_perc=pd.merge(cat_perc,cat_perc2,on=feature)   
    cat_perc.sort_values(by='Count ', ascending=False, inplace=True)
    cat_perc=cat_perc[:end]
    
    data_melted = pd.melt(cat_perc[[feature,target1,target2]], id_vars=feature,\
                           var_name="source", value_name="value_numbers")
    
    fig, (ax1, ax2) = pls.subplots(ncols=2, figsize=(12,6))
    sns.set_color_codes("pastel") 
    s = sns.barplot(ax=ax1, x = feature, y="Count ",order=cat_count[feature][:end],data=(cat_count[:end]))
    s.set_xticklabels(s.get_xticklabels(),rotation=90)
  
    s = sns.barplot(ax=ax2, x = feature, y="value_numbers",hue="source", order=data_melted[feature][:min(end,cat_count.shape[0])],data=(data_melted))
    s.set_xticklabels(s.get_xticklabels(),rotation=90)
    
    pls.tick_params(axis='both', which='major', labelsize=10)
    pls.legend(bbox_to_anchor=(2, 0))
    pls.show();
    
#==========================================#=====================#=====================
# nan
#==========================================#=====================#=====================

def plot_na(df):
    
    pls.style.use('seaborn-talk')

    fig = pls.figure(figsize=(18,6))
    miss = pd.DataFrame((df.isnull().sum())*100/df.shape[0]).reset_index()

    ax = sns.pointplot("index",0,data=miss)
    pls.xticks(rotation =90,fontsize =7)
    pls.title("Missed data")
    pls.ylabel(" %")
    pls.xlabel("Features")
    
def print_na(df,max_row=20):
    mdf=missing_values_table(df)
    if mdf.shape[0]:
        print(missing_values_table(df).head(max_row))
    else:
        print('No missed values in dataframe ')
    
#=====================#=====================#=====================#=====================
# correlations
#=====================#=====================#=====================#=====================
    
def corr(df,maxnbr=20,figsize=None):
    #
    # plots correlation heatmap for all numerical features
    #
    #numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    #l=df.select_dtypes(include=numerics).columns.to_list()
    corr=df.corr()
    cx=corr.abs().unstack().sort_values(ascending=False).reset_index().dropna() 
    f=list(cx[cx.level_0!=cx.level_1]['level_0'].drop_duplicates(keep='first')[:maxnbr].values)
    #show most correlated values
    if figsize==None:
        x=min(len(f),20)
        figsize=(x,x)
    fig, ax = pls.subplots(1,1,figsize=figsize)
    sns.heatmap( corr[corr.index.isin(f)][f], cmap = pls.cm.RdYlBu_r, vmin = -0.25, annot = True, vmax = 0.6)
    pls.title('Correlation Heatmap')
    pls.show() 
    return cx

#plots correlation heatmap for features from the list 
#show all features correlation without filtering
def corr_(df,features,figsize=(20,20)):
    if len(features)>=2:
        fig, ax = pls.subplots(1,1,figsize=figsize)            
        sns.heatmap(df[features].corr(), cmap = pls.cm.RdYlBu_r, vmin = -0.25, annot = True, vmax = 0.6)
        pls.title('Correlation Heatmap')
        pls.show()
        
#plots correlation heatmap between features from two lists        
def corr__(df,features_x,features_y,figsize=(20,20)):
    c=features_x.copy()
    c.extend(features_y)
    fig, ax = pls.subplots(1,1,figsize=figsize)
    sns.heatmap(df[c].corr()[features_y].T[features_x], cmap = pls.cm.RdYlBu_r, vmin = -0.25, annot = True, vmax = 0.6)
    pls.title('Correlation Heatmap')
    pls.show()    
    
    
#=====================#=====================#=====================#=====================
# cramers V
#=====================#=====================#=====================#=====================

import scipy.stats as ss
import itertools
import seaborn as sns

    #Theil’s U, conditional_entropy (no symetrical)
    #https://towardsdatascience.com/the-search-for-categorical-correlation-a1cf7f1888c9
    #https://github.com/shakedzy/dython/blob/master/dython/nominal.py

def plot_cramer_v_corr(df,max_features=20,figsize=(10,10)):
    # plot features correlation (Theil’s U, conditional_entropy) heatmap
    #max_features max features to display
    #features are selected automaticly - categorical or binary  
    #features with too many different values are ignored
    fig, ax = pls.subplots(1,1,figsize=figsize)
    __cramer_v_corr(df.loc[:,df.apply(pd.Series.nunique) < df.shape[0]/2],ax,max_features)
    pls.show()    
    
    
def cramer_v_corr(df,categoricals,figsize=(10,10)):
    
    # plot categorical or binary features specifyed in categoricals list 
    # correlation (Theil’s U, conditional_entropy)  heatmap   
    
    fig, ax = pls.subplots(1,1,figsize=figsize)

    correlation_matrix = pd.DataFrame(
        np.zeros((len(categoricals), len(categoricals))),
        index=categoricals,
        columns=categoricals
    )

    for col1, col2 in itertools.combinations(categoricals, 2):
        idx1, idx2 = categoricals.index(col1), categoricals.index(col2)
        correlation_matrix.iloc[idx1, idx2] = cramers_corrected_stat(pd.crosstab(df[col1], df[col2]))
        correlation_matrix.iloc[idx2, idx1] = correlation_matrix.iloc[idx1, idx2]

    ax = sns.heatmap(correlation_matrix, annot=True, ax=ax); 
    ax.set_title("Cramer V Correlation between Variables");
    pls.show() 

    
#=====================#=====================#=====================#=====================
# report
#=====================#=====================#=====================#=====================

def print_features(df,target=None,sorted_features=[]):
    
    #explore features selected by shap (sorted_features)
    features = sorted_features if len(sorted_features)>0 else list(set(df.columns.to_list()))

    _,tg_cardinality,_ = get_feature_info(df,target)
   

    top10=get_top_correlated(df)
    if target !=None and target not in top10 :
            top10.append(target)
    
    fanova=[]
            
    for feature in features:
                                                                   
        if feature==target:
            continue
                                                                   
        print('\n ')
        display(HTML("<hr>"))
        display(HTML("<h3 align=\"center\">{}</h3>".format(feature)))
        print('\n ') 
                                                                   
        feature_type,cardinality,missed = get_feature_info(df,feature)

        info = pd.DataFrame(
        index=['Type :' ,'Distinct count :', 'Missed %:'],
        columns=[' '])       
        info[' ']=[feature_type,cardinality,missed ]
        print(info.head())
        print('\n ') 
        
        #-----------------Categorical
        
        if feature_type=='Categorical' or feature_type=='Boolean':
                                                                   
            if cardinality > df.shape[0]/2.0 :
                print("Too many values to plot ")
            elif df[feature].isnull().values.all() :
                print("All values are null")
            elif cardinality<2:
                print("Zero variance")
                                                                   
            else:
                if target != None :
                    plot_stats(df,feature,target,30)
                elif cardinality<=40:
                    fig,ax =  pls.subplots(1, 1,figsize=(9, 5))
                    pls.hist(df[feature])
                    pls.xticks(rotation='vertical')
                    pls.show()
                else:
                    fig,ax =  pls.subplots(1, 1,figsize=(9, 5))
                    f=df[feature].value_counts()[:40].index
                    pls.hist(df[df[feature].isin(f)][feature])
                    pls.xticks(rotation='vertical')
                    pls.show()
                                                                   
                #count of records with feature=value per day
                if target != None and  isTime(df.index.dtype):
                    display(HTML("<h3 align=\"center\">Top {} count per day</h3>".format(feature)))
                    plot_ntop_categorical_values_counts(df,feature,target,4)
                
                    #mean of target for records with feature=value per day
                    display(HTML("<h3 align=\"center\">{} mean per day </h3>".format(target)))
                    plot_ntop_categorical_values_means(df,feature,target,4)
                 
                if target != None and tg_cardinality>2 and cardinality<40 :
                    if tg_cardinality>15:
                        sns.catplot(y=feature,x=target,data=df, orient="h", kind="box",height=7)
                    else:
                        sns.catplot(y=feature,x=target,data=df, orient="h", kind="box")
                    pls.show()
            
            #partitioning
            if len(top10)>1:
                depended =[]
                #to speed up - select 4 most popopular values
                top=df[feature].value_counts()[:4].index
                sub=df[df[feature].isin(top)]

                for t in top10:
                    try:
                        #check variance 
                        if anova(sub,feature,t,False):
                            depended.append(t)
                    except Exception:
                        a=0

                if len(depended)>0:
                    fanova.append(feature)  
                    if len(depended)>1:
                        sns.pairplot(sub,vars=depended,hue=feature,corner=True)
                        pls.show()

                  
        #---------------- Numeric    
        
        elif feature_type=='Numeric':
            #pairwise_feature_sum_per_day(df1,df2,feature)
            #pairwise_feature_mean_per_day(df1,df2,feature)
            if cardinality<=40:
                
                plot_stats(df,feature,target,40)
                
                if target !=None and tg_cardinality>2 and cardinality>2 :
                    fig,ax =  pls.subplots(1, 1,figsize=(8, 5))
                    pls.scatter(df[feature], df[target], marker='.', alpha=0.7, s=30, lw=0,  edgecolor='k')
                    ax.set_xlabel(feature)
                    ax.set_ylabel(target)
                    pls.show()
                    
                if target !=None and tg_cardinality>2:
                    #.sample(min(df.shape[0],100000))
                    if tg_cardinality>15:
                        sns.catplot(y=feature,x=target,data=df, orient="h", kind="box",height=7)
                    else:
                        sns.catplot(y=feature,x=target,data=df, orient="h", kind="box")
                    pls.show()
            else:
                #df[feature].hist() 
                
                #distribution
                fig,ax = pls.subplots(1, 2,figsize=(16, 5))
                sns.distplot(df[feature],kde=True,ax=ax[0]) 
                ax[0].axvline(df[feature].mean(),color = "k",linestyle="dashed",label="MEAN")
                ax[0].legend(loc="upper right")
                ax[0].set_title('Skewness = {:.4f}'.format(df[feature].skew()))
                sns.boxplot(df[feature],color='blue',orient='h',ax=ax[1])
                pls.show()
                
                if  target !=None :
                    
                    if tg_cardinality < 10:
                        fig,ax = pls.subplots(1, 2,figsize=(16, 5))
                        ax[0].scatter(df[feature], df[target], marker='.', alpha=0.7, s=30, lw=0,  edgecolor='k')
                        ax[0].set_xlabel(feature)
                        ax[0].set_ylabel(target)
                        sns.violinplot(x=target, y=feature, data=df, ax=ax[1], inner='quartile')
                        pls.show()  
                    else:
                        #continues - continues
                        plot_qcuts(df,feature,target)
                        q = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1]
                        df['cut']=pd.qcut(df[feature],q=q,duplicates='drop')
                        sns.catplot(x=target,y='cut',data=df, orient="h", kind="box") 
                        pls.show()
                        fig,ax = pls.subplots(1, 1,figsize=(8, 5))
                        pls.scatter(df[feature], df[target], marker='.', alpha=0.7, s=30, lw=0,  edgecolor='k')
                        ax.set_xlabel(feature)
                        ax.set_ylabel(target)
                        pls.show()
                        
                       
        else:
            
            print("Time column skip plotting ")
            
    #second order interactions:
    if False and len(fanova)>1 :
        
        header('2nd order Interactions',sz='h3')

        for ff1 in range(len(fanova)-1):
            f1=fanova[ff1]
            for ff2 in range(ff1+1,len(fanova)):
                f2=fanova[ff2]
                df[f1+f2]=df[f1]+df[f2]
                top=df[f1+f2].value_counts()[:10].index
                sub=df[df[f1+f2].isin(top)]
                depended=[] 
                for t in top10:
                       
                    try:
                        #print('\n\n',t)
                        res=two_way_anova(sub,f1,f2,t)
                        #print(res)
                        
                        if(res.iloc[2]['PR(>F)']<=0.05):
                            depended.append(t)

                    except Exception:
                        a=0
                if len(depended)>0:        
                    if len(depended)>1: 
                        sns.pairplot(sub,vars=depended,hue=f1+f2,corner=True)
                        pls.show()
                    for t in depended:
                        g = sns.catplot(x=t, y=f1, row=f2, kind="box", orient="h", height=1.5, aspect=4,data=sub)
                        pls.show()
            del df[f1+f2]
                        
                        
def do_eda(df,target,ignore=[],nbrmax=20,figsize=(20,4),linewidth=2):
    
    #detect time columns
    df = df.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object else col, axis=0)
    
    header('Missed values' )
    print_na(df)
                      
    #print shap values for each frame predicting targed
    feature_type,cardinality,missed = get_feature_info(df,target)
    
    if feature_type=='Numeric' :#and cardinality==2:
        header('Shap values')

        sorted_features=plot_shap(df,target,ignore=ignore,nbrmax=nbrmax)[:nbrmax]
    else:
        sorted_features=list(set(df.columns.tolist())-set(ignore))

    # if dataframe has timedate index - plot time series
    if target !=None and  isTime(df.index.dtype) :
        header('Time series' )
        ax=df[target].resample('1d').mean().plot( grid=True,x_compat=True,figsize=figsize,linewidth=linewidth,label=target)
        pls.title(' {} mean per day '.format(target))
        pls.legend()
        pls.show() 
    
    
    header('Features' )
    print_features(df,target,sorted_features)
     
    #for numeric variables only
    header('Pearson correlations' )     
    cx=corr(df,nbrmax) 

    #correlations of categorical variables
    header('Cramers V staticstics' )    
    #third parameter max features to display
    plot_cramer_v_corr(df,nbrmax) 

    #plot 10 most correlated features
    header('Top correlated features' )  
    f=list(cx[(cx[0]>0.099)&(cx.level_0!=cx.level_1)]['level_0'].drop_duplicates(keep='first')[:10].values)
    sns.pairplot(df[f])  
    
    return sorted_features

def get_top_correlated(df,th=0.099,maxcount=10):
    corr=df.corr()
    if corr.shape[0]>0:
        cx=corr.unstack().dropna().abs().sort_values(ascending=False).reset_index()
        return list(cx[(cx[0]>th)&(cx.level_0!=cx.level_1)]['level_0'].drop_duplicates(keep='first')[:maxcount].values)   
    else:
        return []

def interactions(ddf):
    df=ddf.copy()
    
    features =  list(set(df.columns.to_list()))
   
    candidates=[]
    numeric=[]
    
    for feature in features:                                                                                                                                                       
        feature_type,cardinality,missed = get_feature_info(df,feature)
        
        if feature_type=='Categorical' or feature_type=='Boolean' and\
            cardinality < df.shape[0]/2.0 and not df[feature].isnull().values.all()\
            and cardinality>=2:
            candidates.append(feature)
                                                                   
        elif feature_type=='Numeric':
            if cardinality> 1:
                numeric.append(feature)
                
            if cardinality < df.shape[0]/2.0 and cardinality>=2 and cardinality < 40:
                candidates.append(feature)
            else:
                q = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,0.9, 1]
                df['   '+feature]=pd.qcut(df[feature], q=q,duplicates='drop')
                df['   '+feature]=df['   '+feature].astype(str)
                candidates.append('   '+feature)
                
    for ff1 in range(len(candidates)-1):
        f1=candidates[ff1]

        for ff2 in range(ff1+1,len(candidates)):
            f2=candidates[ff2]

            df[f1+f2]=df[f1].astype(str)+df[f2].astype(str)
            top=df[f1+f2].value_counts()[:8].index
            sub=df[df[f1+f2].isin(top)]
            depended=[] 
            for t in numeric:
                if ('   '+t) in [f1, f2] or t in [f1,f2]:
                    continue

                try:
                    #print('\n\n',t)
                    res=two_way_anova(sub,f1,f2,t)
                    #print(res)

                    if(res.iloc[2]['PR(>F)']<=0.05):
                        #print(f1,f2,t)
                        depended.append(t)

                except Exception:
                    a=0
                    
            if len(depended)>0:        
                if len(depended)>1: 
                    sns.pairplot(sub,vars=depended,hue=f1+f2,corner=True)
                    pls.show()
                for t in depended:
                    print(f1+'*'+f2+'='+t)
                    g = sns.catplot(x=t, y=f1, row=f2, kind="box", orient="h", height=1.5, aspect=4,data=sub)
                    pls.show()