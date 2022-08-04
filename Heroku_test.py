
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')



markdown_text = '''
The gender wage gap (or gender pay gap) is generally defined by [Wikipedia](https://en.wikipedia.org/wiki/Gender_pay_gap) as the mean difference in annual wages paid to men and women who are actively working. Historically, men have earned significantly higher than women on average; these differences in pay between genders have been linked to various socioeconomic, legal, and economic factors. According to [US Census Data](https://www.census.gov/library/stories/2022/03/what-is-the-gender-wage-gap-in-your-state.html), most states in the U.S. have a measureable wage gap of $4,500 or higher.  

The [2019 General Social Survey](https://gss.norc.org/) (GSS) is a survey that has run for about 5 decades, the goal of which is to capture data on trends and opinions, attitudes, and behaviors of 'contemporary American society.' By sampling the U.S. population consistently over time, it is considered one of the best sources to assess trends in the population and is a widely cited source for research in the Social Sciences.
'''



gss_display = gss_clean.groupby('sex').agg({'income':'mean',
                                        'job_prestige':'mean',
                                          'socioeconomic_index':'mean',
                                           'education':'mean'}).reset_index()
gss_display = gss_display.rename({'sex':'Sex',
                                   'income':'Annual Income',
                                   'job_prestige':'Occupational Prestige',
                                   'socioeconomic_index':'Socioeconomic Index',
                                   'education':'Years of Education'}, axis=1)
gss_display = round(gss_display, 2)


gss_bar = gss_clean.groupby(['sex','male_breadwinner']).size().reset_index()
gss_bar = gss_bar.rename({0:'count',
                         'sex':'Sex',
                         'male_breadwinner':'Man is the Breadwinner'}, axis=1)


fig_bar = px.bar(gss_bar, x='Sex', y='count', color='Man is the Breadwinner', 
            # facet_col='Sex', facet_col_wrap=2,
             text='Man is the Breadwinner',
             hover_data = ['count'], barmode = 'group',
            labels={'Man is the Breadwinner':'Should the man be<br>the breadwinner?'},
             width=1000, height=600)
fig_bar.update(layout=dict(title=dict(x=0.5)))
fig_bar.update_layout(showlegend=False)


gss_scatter = gss_clean[~gss_clean.job_prestige.isnull()]
gss_scatter = gss_clean[~gss_clean.income.isnull()]

fig_scatter = px.scatter(gss_scatter, x='job_prestige', y='income', color = 'sex',
                 opacity = .5, 
                 #color=['black']*gss_scatter.shape[0],
                 color_discrete_map = {'black':'black'},
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Annual Income'},
                 hover_data=['education',  'socioeconomic_index'])
fig_scatter.update(layout=dict(title=dict(x=0.5)))
fig_scatter.update_layout(showlegend=True)


gss_dist1  = gss_clean[~gss_clean.income.isnull()]
gss_dist1  = gss_clean[~gss_clean.sex.isnull()]
gss_dist2  = gss_clean[~gss_clean.job_prestige.isnull()]
gss_dist2  = gss_clean[~gss_clean.sex.isnull()]

fig_vio = px.box(gss_dist1, y='income', x = 'sex', color = 'sex',
                   labels={'income':'Annual Income', 'sex':''})
fig_vio.update(layout=dict(title=dict(x=0.5)))
fig_vio.update_layout(showlegend=False)


fig_vio2 = px.box(gss_dist1, y='job_prestige', x = 'sex', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige', 'sex':''})
fig_vio2.update(layout=dict(title=dict(x=0.5)))
fig_vio2.update_layout(showlegend=False)


gss_facet = gss_clean[['income','sex','job_prestige']]
gss_facet['job_prestige_cut'] = pd.cut(gss_facet.job_prestige, bins = 6)
gss_facet = gss_facet.sort_values(by = 'job_prestige_cut', axis=0, ascending=True)
gss_facet = gss_facet.dropna()
gss_facet.job_prestige_cut.value_counts()


fig_facet = px.violin(gss_facet, x='sex', y='income', color='sex', 
             facet_col='job_prestige_cut', facet_col_wrap=2,
             #hover_data = ['votes', 'Biden thermometer', 'Trump thermometer'],
            labels={'income':'Income', 'sex':'', 'job_prestige_cut': 'Job Prestige Range'},
                      color_discrete_map = {'male':'blue', 'female':'red'},
             width=1000, height=600)
fig_facet.update(layout=dict(title=dict(x=0.5)))
fig_facet.update_layout(showlegend=False)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.H1("Exploring the 2019 General Social Survey (GSS)"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H3("Mean income, occupational prestige, socioeconomic index, and years education for men/women."),
        
        dcc.Graph(figure=table),
                
        html.H3("# of Agreement Responses to the question: 'Should men be the breadwinner?' by Sex"),
        
        dcc.Graph(figure=fig_bar),
        
        html.H3("Occupational Prestige and Annual Income by Sex"),
        
        dcc.Graph(figure=fig_scatter),
        
        html.Div([
            
            html.H3("Annual Income by Sex"),
            
            dcc.Graph(figure=fig_vio)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H3("Occupational Prestige by Sex"),
            
            dcc.Graph(figure=fig_vio2)
            
        ], style = {'width':'48%', 'float':'right'}),
        html.H3("Annual Income by Sex, Faceted by Occupational Prestige Level"),
        
        dcc.Graph(figure=fig_facet)
 ]
)


if __name__ == '__main__':
    app.run_server(mode='external', debug=True)