import pandas as pd

meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL',
         'MAYO', 'JUNIO', 'JULIO', 'AGOSTO',
         'SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']

def gen_cols(n):
    dict = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    len_dict = len(dict)
    lista = []
    for i in range(n):
        if i<len_dict:
            lista.append(dict[i])
        else:
            x=i//len_dict-1
            y=i%len_dict
            lista.append(dict[x]+dict[y])

    return lista

def clear_info(x):
    x = x.strip()
    x = x.upper()
    return x


vacs = ['BCG',    'HvB',    'APO',    'Penta 3',    'Rotavirus 2',
    'Neumococo 2',    'Influenza 2',    'Neumococo 3',    'SPR 1',
    'Varicela 1',    'AntiAmarílica',    'hepatitis A',    'SPR 2',
    'Ref. DPT 1',    'Ref. DPT 2',    'Ref. APO 2']

rango_edad = ['RN','<1_ANIO','1_ANIO','2_ANIOS','3_ANIOS','4_ANIOS']
dict_vacs_df = {
    'BCG':['E','G','BC','BY','CU','DQ'],
    'HvB':['H','I','','','',''],
    'APO':['','L','AP','BK','CG','DC'],
    'Penta 3':['','O','AV','BN','CJ','DF'],
    'Rotavirus 2':['','W','','','',''],
    'Neumococo 2':['','Y','AL','BX','CT','DP'],
    'Influenza 2':['','AA','AI','','',''],
    'Neumococo 3':['','','AE','','',''],
    'SPR 1':['','','AF','BU','CQ','DM'],
    'Varicela 1':['','','AG','BG','CC','CY'],
    'AntiAmarílica':['','','AM','BH','CD','CZ'],
    'hepatitis A':['','','','','',''],
    'SPR 2':['','','AN','BV','CR','DN'],
    'Ref. DPT 1':['','','AO','','',''],
    'Ref. DPT 2':['','','','','','DR'],
    'Ref. APO 2':['','','','','','DS']
}

def create_df(df1, dicts,rango, vacunas, mes):
    
    lista_labs = df1['C'].unique()
    cols=['ANIO','DEPARTAMENTO', 'RANGO_EDAD', 'EFERMERDAD','MES',
                 'CANTIDAD']
    df = pd.DataFrame(0, index=lista_labs, columns=cols) 
    df.reset_index(inplace= True)
    df = df.rename(columns={'index': 'RENAES'})
    df['ANIO']= 2019
    df['MES'] = mes
    df['DEPARTAMENTO']= 'LORETO'
    df['RANGO_EDAD']= '-'
    df['ENFERMERDAD']= '-'
    list_df = []
    for vac in vacunas:
        ubic_col = dicts[vac]
        for i, celda in enumerate(ubic_col):
            if celda:
                print('---------------------' , celda)
                df3 = df.copy()
                df3['ENFERMERDAD'] = vac
                df3['RANGO_EDAD']= rango[i]
                df4 = df1[['C', celda]].copy()
                for index, row in df3.iterrows():
                    row1 = df4[df4['C']==row['RENAES']]
                    df3.loc[index,'CANTIDAD'] = row1[celda].to_list()[0]
                list_df.append(df3)

    result = pd.concat(list_df)
    return result       

""" def clear_string(x):
    x = x.replace('.', '')
    x = x.replace('I-3', '')
    x = x.replace('  ', ' ')
    x = x.replace('I-4', '')
    x = x.replace('"', '')
    x = x.replace('DENAUTA', 'NAUTA')
    x = x.replace('PUESTO DE SALUD', '')
    x = x.replace('CENTRO DE SALUD', '')
    x = x.replace('CENTRO DE ALUD', '')
    x = x.replace('PS', '')
    x = x.replace('CS', '')
    x = x.replace('I1', '')
    x = x.replace('I -1', '')
    x = x.replace('I - 1', '')
    x = x.replace('I-1', '')
    x = x.replace('I-2', '')
    x = x.replace('KM', '')
    x = x.replace('-', '')
    x = x.replace('  ', ' ')
    x = x.strip()
    x = x.upper()
    

    return x
 """
def get_personal():

    #cols = ['RENAES','DESCRIPCION ESTABLECIMIENTO','UBIGEO','DEPARTAMENTO','PROVINCIA','DISTRITO',
    #        'RED','MICRORRED','cargo','Grupo Final 2','PEA']

    cols1 = ['RENAES','DESCRIPCION ESTABLECIMIENTO','UBIGEO','DEPARTAMENTO','PROVINCIA','DISTRITO',
            'RED','MICRORRED']
    list_df =[]
    for mes in meses:
        try:
            print('---------------------' , mes)
            df = pd.read_excel('C:\\Users\\John\\Desktop\\personal2019\\'+mes+'.xlsx','DATA')
            df = df[cols1].copy()

            #df = df[df['DEPARTAMENTO']=='LORETO']
            #df['DESCRIPCION ESTABLECIMIENTO'] = df['DESCRIPCION ESTABLECIMIENTO'].apply(clear_string)
            dfx = df.drop_duplicates(subset=['RENAES']).copy()
            dfx['MES'] = mes
            df1 = df[['RENAES']].copy()
            df1['PERSONAL'] = 1
            df2 = (df1.groupby('RENAES').count().reset_index()).copy()
            df2 = pd.merge(dfx, df2, on=['RENAES'])
            list_df.append(df2)
        except FileNotFoundError:
            print('File does not exist')


    result = pd.concat(list_df)
    result = result.rename(columns={'DESCRIPCION ESTABLECIMIENTO': 'CENTRO DE SALUD'})
    result.to_csv('personal_resumen_2019.csv')
    #result.to_csv('personal_loreto.csv')
    
    return result

if __name__ == "__main__":
    df_vacs = pd.DataFrame(data=dict_vacs_df)
    """ df_redes = pd.read_csv('REDES.csv',delimiter=';')
    dir = df_redes.columns[0]
    df_redes[dir] = df_redes[dir].apply(clear_info) """

    xls = pd.ExcelFile('C:\\Users\\John\\Desktop\\cob2019.xlsx')
    mes = meses[0]
    df = pd.read_excel(xls, mes[0:3])

    df = df.iloc[17:481,:]
    df.columns = gen_cols(df.shape[1])

    df = df.fillna(0)
    df = df[df.C !=0]
    df['D'] = df['D'].apply(clear_info)

    df2 = create_df(df, dict_vacs_df,rango_edad, vacs, mes)
    df2 = df2.rename(columns={'Lab': 'CENTRO DE SALUD'})
    
    df2.to_csv('ENE_vacs2019.csv')
    

    #usar para generar tabla del personal
    #df_personal = get_personal() 

    #si ya existe tabla del personal:
    # df_personal = pd.read_csv('C:\\Users\\John\\Desktop\\MIT\\personal_resumen_2019.csv')   

    # df5 = pd.merge(df2,df_personal, on='RENAES', how='inner')

    # df5.to_csv('consolidado_cob_personal_2019_loreto.csv')

