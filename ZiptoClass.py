
from multiprocessing.resource_sharer import stop
from operator import index
import streamlit as st
import pandas as pd
from itertools import chain


st.image('zizzl health logo 22.png')
st.title("Zip to Class Tool")

choice = st.radio('Choose one: ', ['Individual', 'Census'])
#st.subheader("Upload Census Here:")


def convert_df(df):
    return df.to_csv(index=False)


classed_file_df = pd.read_csv('National classing matrix.csv')
zip_to_fips_df= pd.read_csv('CSA zip.csv')
zip_to_fips_df_dropdown = pd.read_csv('CSA zip.csv', dtype=object)


if (choice == 'Individual') :
    Zip = st.multiselect('Input Zip Code: ', zip_to_fips_df_dropdown['Zip Code'])
    #st.write(Zip)
    def convert_df(df):
        return df.to_csv(index=False)


    if (Zip is not None):
        join = pd.merge(classed_file_df[['FIPS','Class']], zip_to_fips_df, on = 'FIPS', how = 'inner')

        #st.write(join)
        for i in range(len(Zip)):
            #st.write(i)
            check = join['Class'][join['Zip Code'] == int(Zip[i])].reset_index()
            #st.write(check)

            st.write(Zip[i],': This Zip Code belongs to class: ',check['Class'][0].upper())

elif (choice == 'Census'):
    census = st.file_uploader('Upload Census: ')
    if census is not None:
        censusdf = pd.read_csv(census, encoding_errors='replace')

        join = pd.merge(classed_file_df[['FIPS','Class']], zip_to_fips_df, on = 'FIPS', how = 'inner')

    

        list = join[['Class','Zip Code', 'rating_area_id']].set_index('Zip Code').to_dict()
        list = list['Class']
        
        censusdf['Class'] = censusdf['Zip Code'].map(list)
        
        #st.write(censusdf)

        check = False

        

        classes = censusdf['Class'].unique()

        
        for i in classes:
            st.write('Class ', str(i))
            format = censusdf[ censusdf['Class'] == i]
            st.write(format[['First Name','Last Name', 'DOB', 'Zip Code', 'Relationship', 'Notes']])
            csv = convert_df(format[['First Name','Last Name', 'DOB', 'Zip Code', 'Relationship', 'Notes']]) 

            st.download_button(
                label = 'Download above data as CSV',
                data = csv,
                file_name = 'Class '+ str(i) +'.csv',
                mime='text/csv'
            )  