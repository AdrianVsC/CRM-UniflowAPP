import pandas as pd
from data.load_data import load_data_analisis

# Llamada de las tablas a usar
customer_df,condominum_df = load_data_analisis()

# Convertir la columna 'createdAt' a formato de fecha
customer_df['createdAt'] = pd.to_datetime(customer_df['createdAt'])
# Establecer 'createdAt' como el índice
customer_df.set_index('createdAt', inplace=True)
# Formato para mostrar las fechas como DD/MM/YY
customer_df.index = customer_df.index.strftime('%d/%m/%y')
customer_df.sort_values('createdAt', inplace=True)

#funciones totales sin filtros por mes

# Total clientes en estado propuesta
def total_customer_proposed(customer_df):
    #Realización de cálculos
    Total_Clientes_Propuesta = customer_df[customer_df['prospect_status'] == 'Proposed'].shape[0]
    return Total_Clientes_Propuesta

# Total clientes en estado negociacion
def total_customer_negociation(customer_df):
    #Realización de cálculos
    Total_Clientes_Negociacion = customer_df[customer_df['prospect_status'] == 'Negociation'].shape[0]
    return  Total_Clientes_Negociacion

# Total clientes en estado contactado
def total_customer_contated(customer_df):
    #Realización de cálculos
    Total_Clientes_Contactado = customer_df[customer_df['prospect_status'] == 'Contacted'].shape[0]
    return  Total_Clientes_Contactado

# Total Clientes en estado Cerrado
def total_customer_closed(customer_df):
    #Realización de cálculos
    Total_Clientes_Cerrados = customer_df[customer_df['prospect_status'] == 'Closed'].shape[0]
    return Total_Clientes_Cerrados

# Total facturacion por cliente 
def total_customer_facturation (customer_df,condominium_df):
    #Realizacion del calculo
    join = pd.merge(customer_df,condominium_df,on='id_customer',how='inner')
    total_propiedades = join.groupby('id_customer')['propieties'].sum().reset_index(name='total_propiedades')
    total_propiedades['total_propiedades'] = total_propiedades['total_propiedades'].apply(lambda x: f"${x:,.2f}")
    return total_propiedades

# Total de condominios por cada cliente
def total_customer_condominum (customer_df,condominium_df):
    #realizacion del calculo
    join = pd.merge(customer_df,condominium_df,on='id_customer', how='inner')
    total_condominios = join.groupby('id_customer')['propieties'].count().reset_index(name='total_condominios')
    return total_condominios

# Total clientes activos
def total_customer_active(customer_df):
    Total_Clientes_Activos = customer_df[customer_df['isEnable']==True].shape[0]
    return Total_Clientes_Activos

# Total clientes inactivos 
def total_customer_inactive(customer_df):
    Total_Clientes_Inactivos = customer_df[customer_df['isEnable']==False].shape[0]
    return Total_Clientes_Inactivos

# Total clientes en prospectos en total sin importar los meses
def total_prospect(customer_df):
    total_prospectos = customer_df[customer_df['client_status'] != 'Closed'].shape[0]
    return total_prospectos

# Totales filtrados por mes
# Todos estos filtros se ejecutan en base a la fecha de createdAt, en caso de actualizacion de estado, sigue tomando la fecha de creacion, no toma en cuenta la fecha de actualizacion


#Funcion para filtrar por mes en la visualizacion, tomada por numeros del 1 al 12 
def monthly_filter(customer_df, mes):
    # Extraemos el mes del índice (que es la columna 'createdAt')
    df_filtrado = customer_df[customer_df.index.to_series().apply(lambda x: pd.to_datetime(x).month) == mes]
    return df_filtrado

# Total clientes totales prospectos en todos los estados, prospecto, contactado, negociacion y cerrado en el mes
def total_customer_prospect_month(customer_df, mes):
    df_filtrado = monthly_filter(customer_df,mes)
    #prospectos para el mes
    total_clientes_propuesta_mes = df_filtrado.shape[0]
    
    return total_clientes_propuesta_mes

# Total clientes cerrados por mes 
def total_customer_closed_month(customer_df, mes):
    df_filtrado = monthly_filter(customer_df,mes)
    total_cliente_cerrado_mes = df_filtrado[df_filtrado['prospect_status']== 'Closed'].shape[0]
    return total_cliente_cerrado_mes

# Total clientes en estado contactado por mes
def total_customer_contacted_month (customer_df, mes):
    df_filtrado = monthly_filter(customer_df,mes)
    total_cliente_contactado_mes = df_filtrado[df_filtrado['prospect_status'] == 'Contacted'].shape[0]
    return total_cliente_contactado_mes

# Total clientes en estado negociacion por mes 
def total_customer_negociation_month (customer_df,mes):
    df_filtrado = monthly_filter(customer_df,mes)
    total_cliente_negociacion_mes = df_filtrado[df_filtrado['prospect_status']== 'Negociation'].shape[0]
    return total_cliente_negociacion_mes

# Total clientes en estado propuesta por mes
def total_customer_proposed_month(customer_df,mes):
    df_filtrado = monthly_filter(customer_df,mes)
    Total_Clientes_Propuesta_mes = df_filtrado[df_filtrado['prospect_status'] == 'Proposed'].shape[0]
    return Total_Clientes_Propuesta_mes

# Total clientes activos por mes
def total_customer_active_month(customer_df,mes):
    df_filtrado = monthly_filter(customer_df,mes)
    Total_Clientes_Activos_mes = df_filtrado[df_filtrado['isEnable']==True].shape[0]
    return Total_Clientes_Activos_mes

# Total de clientes inactivos por mes
def total_customer_inactive_month(customer_df,mes):
    df_filtrado = monthly_filter(customer_df,mes)
    Total_Clientes_Inactivos_mes = df_filtrado[df_filtrado['isEnable']==False].shape[0]
    return Total_Clientes_Inactivos_mes

# Porcentaje de meta mensual
def monthly_target_porcent (customer_df,mes):
    total = total_customer_prospect_month(customer_df,mes)
    meta_mensual_porcentaje = total * 0.75
    porcentaje = meta_mensual_porcentaje/total_customer_prospect_month(customer_df,mes) * 100
    return porcentaje

# Meta Mensual
def monthly_target(customer_df,mes):
    total = total_customer_prospect_month(customer_df,mes)
    meta_mensual = total * 0.75
    return meta_mensual

# Porcentaje de cumplimiento al momento 
def compliance_rate(customer_df,mes):
    total_prospectos = total_customer_prospect_month(customer_df,mes)
    meta = total_prospectos * 0.75
    if meta > 0:
        cumplimiento = (total_customer_closed_month(customer_df,mes)/meta) *100
    else:
        cumplimiento = 0 #Evitar division por 0

    return cumplimiento

