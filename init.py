#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from flask import  Flask, request ,jsonify
from unidecode import unidecode

# incorporo datos con geo
#df=pd.read_csv('leonardoTotal_1.csv')
df=pd.read_csv('dataFrameGeoTopics_v3.csv')


# conf pedidos de archivos estaticos
app = Flask('Visualizacion',static_url_path='/static')


# para eliminacion de columnas que no aportan nada
def cleanColumns(df,columns):
    for c in columns:
        df.drop(c,axis=1,inplace=True);
    return df


def df_to_geojson(df, properties, lat, lng):
    """
    Turn a dataframe containing point data into a geojson formatted python dictionary

    df : the dataframe to convert to geojson
    properties : a list of columns in the dataframe to turn into geojson feature properties
    lat : the name of the column in the dataframe that contains latitude data
    lng : the name of the column in the dataframe that contains longitude data
    """

    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    # x is the equivalent of the row, df.iterrows converts the dataframe in to a pd.series object
    # the x is a counter and has no influence
    for x, row in df.iterrows():

        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [float(row[lat]),float(row[lng])]

        # be aware that the dataframe is a pd.series
        #print('rowitem converts to ndarray(numpy) :\n ', row)
        # convert the array to a pandas.serie
        geo_props = pd.Series(row)

        # for each column, get the value and add it as a new feature property
        # prop determines the list from the properties
        for prop in properties:

            #loop over the items to convert to string elements

            #convert to string
            if type(geo_props[prop]) == float:
                #print('ok')
                geo_props[prop] = str(int(geo_props[prop]))

            # now create a json format, here we have to make the dict properties
            feature['properties'][prop] = geo_props[prop]

        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    return geojson


#columns=['Observación','Respuestas del cuestionario','# contacto','Fecha cambio de estado','Calle','Altura','Esquina proxima','Rubro','Prestación','Motivo','Organizacion responsable','Usuario','Estado flujo','Historial de cambios','CGPC']        
#df=cleanColumns(df,columns)


# borro las filas que no tienen coordenadas
df.drop(df[df['x']==df['y']].index,inplace=True)

# paso los barrios a uppercase
df['Barrio']=df['Barrio'].apply(lambda x: unidecode(x.upper()))

# preparacion de los datos para ser consultados despues
df['year']=pd.to_datetime(df['Fecha creación']).dt.strftime('%Y')

# preparacion consultas x mes
df['month']=pd.to_datetime(df['Fecha creación']).dt.strftime('%m')


df=df[['# contacto','Barrio','year','month','x','y','topic_max']]


# consulta para totales por year x barrios
@app.route('/topicPolar/<p_year>/<p_barrio>')
def getTopicYearBarrio(p_year,p_barrio):
    dict_values=[0,0,0,0,0]
    
    if(p_barrio!='-1'):
        df_topic_month=df[(df['year']==p_year)&(df['Barrio']==p_barrio)].groupby('topic_max').count() 
    else:
        df_topic_month=df[(df['year']==p_year)].groupby('topic_max').count()  
   
    for index, row in df_topic_month.iterrows():
        dict_values[index - 1]=str(row['x'])
        
    print(dict_values)    

    print('get-Topic-Year-Barrio :'+p_year +' : '+p_barrio+' count: '+str(len(df_topic_month)))
    return jsonify(dict_values)


# consulta para totales por year x barrios
@app.route('/tot/<p_year>/<p_barrio>')
def getTotYearBarrio(p_year,p_barrio):
    dict_values=[]
    
    if(p_barrio!='-1'):
        df_per_month=df[(df['year']==p_year)&(df['Barrio']==p_barrio)].groupby('month').count() 
    else:
        df_per_month=df[(df['year']==p_year)].groupby('month').count()  
   
    for index, row in df_per_month.iterrows():
        dict_values.append(str(row['x']))

    print(dict_values)    

    print('getTotYearBarrio :'+p_year +' : '+p_barrio+' count: '+str(len(df_per_month)))
    return jsonify(dict_values)

@app.route('/geo/<p_year>/<p_barrio>/<p_topic>')
def getPointsGeoYBTopic(p_year,p_barrio,p_topic):
    properties=['# contacto']
    #cambiar consulta aca
    
    if((p_year!='-1')&(p_barrio!='-1')):
        if(p_year!='-1'):
            df_to_geo=df[(df['year']==p_year)&(df['Barrio']==p_barrio)&(df['topic_max']==int(p_topic))] 
        else:
            df_to_geo=df[(df['Barrio']==p_barrio)&(df['topic_max']==int(p_topic))] 
    else:
         df_to_geo=df[df['topic_max']==int(p_topic)] 

    json_point=df_to_geojson(df_to_geo, properties, 'x', 'y')
    print('getPointsGeoYBTopic :'+p_year +' : '+p_barrio+' : '+str(p_topic)+' count: '+str(len(json_point)))
    return jsonify(json_point)


@app.route('/geo/<p_year>/<p_barrio>')
def getPointsGeoYearBarrio(p_year,p_barrio):
    
    properties=['# contacto','topic_max']
    if(p_year!='-1'):
        df_to_geo=df[(df['year']==p_year)&(df['Barrio']==p_barrio)] 
    else:
        df_to_geo=df[(df['Barrio']==p_barrio)] 
    #for index,row in df_to_geo.iteritems():
    #    print(row['year']+' '+row['Barrio']+' '+str(row['x'])+' '+str(row['y'])) 
    
    json_point=df_to_geojson(df_to_geo, properties, 'x', 'y')
    print('getPointsGeoYearBarrio :'+p_year +' : '+p_barrio+' count: '+str(len(df_to_geo)))
    return jsonify(json_point)

@app.route('/geo/<p_year>')
def getPointsGeoYear(p_year):
    
    properties=['# contacto','topic_max']
    df_to_geo=df[df['year']==p_year]
    json_point=df_to_geojson(df_to_geo, properties, 'x', 'y')
    
    print('getPointsGeoYear: '+p_year+' count '+str(len(df_to_geo)))
    return jsonify(json_point)
    


@app.route("/")
def loadInitVisualizacion():
    file = open('index.html', 'r') 
    return file.read()

#host='0.0.0.0',
app.run(host='0.0.0.0',port=8080)



