import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="InsightFlow Data Explorer", 
    page_icon="📊", 
    )

st.title(":blue[📊 InsightFlow Data Explorer]")

st.header("Visualize Your Data with Confidence" , divider="rainbow")
st.subheader(" :grey[Empowering you with actionable insights and intuitive data visualization.]")

file = st.file_uploader("Upload a CSV file", type=['csv', 'xlsx'])


if(file!=None):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info("File Loaded Successfully!" , icon="🚨")



    st.header( ':violet[Data Insights : ]' , divider="rainbow")
    tab1, tab2, tab3, tab4 = st.tabs(['Data Summary', 'Top & Bottom rows', 'Data Types', 'Columns'])


    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
        st.subheader('Data Summary')
        st.dataframe(data.describe())

    with tab2:
        toprows = st.slider('Top Rows', 1, data.shape[0] , 5 , key = 'toprows')
        st.dataframe(data.head(toprows))

        bottomrows = st.slider('Bottom Rows', 1, data.shape[0] , 5 , key = 'bottomrows')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':blue[Types of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':blue[Column names in Dataset ]')
        st.dataframe(list(data.columns))


    st.header(':violet[Data Visualization : ]' , divider="rainbow")
    with st.expander('Value Count'):
        col1, col2 = st.columns(2)


        with col1:
            column = st.selectbox('Select Column name', options = list(data.columns))

        with col2:
            toprows = st.number_input('Top Rows', min_value=1, step=1)

        count = st.button('Value Count')
        if(count == True):
            result = data[column].value_counts().head(toprows).reset_index()
            st.dataframe(result)

            st.subheader(':blue[Visualization]', divider = 'rainbow')
            fig = px.bar(data_frame = result, x = column, y = 'count')
            st.plotly_chart(fig)
            fig = px.line(data_frame = result, x = column, y = 'count')
            st.plotly_chart(fig)
            fig = px.pie(data_frame = result, names = column, values = 'count')
            st.plotly_chart(fig)


    st.header(':violet[ Groupby - Simplify your Data Analysis ]' , divider="rainbow")
    st.write('Groupby is a powerful tool for data analysis. It allows you to split your data into separate groups to perform computations for better insights.')

    with st.expander('Group By your columns'):
        col1, col2, col3 = st.columns(3)

        with col1:
            groupby_cols = st.multiselect('Select Column to groupby', options = list(data.columns))

        with col2:
            operation_col = st.selectbox('Select Column name for operation ', options = list(data.columns))

        with col3:
            operation = st.selectbox('Select Operation', options = ['sum', 'mean', 'count', 'min', 'max'])



        if(groupby_cols):

            result = data.groupby(groupby_cols).agg(
            newcol = (operation_col, operation)
            ).reset_index()
            st.dataframe(result)

            st.subheader(':blue[Visualization]', divider = 'rainbow')
            graph = st.selectbox('Select Graph', options = ['Bar', 'Line', 'Pie', 'Scatter', 'sunburst'])
            if(graph == 'Line'):
                x_axis = st.selectbox('Select X-axis', options = list(result.columns))
                y_axis = st.selectbox('Select Y-axis', options = list(result.columns))
                color = st.selectbox('Select Color', options = [None] + list(result.columns))  
                fig = px.line(data_frame = result, x = x_axis, y = y_axis, color = color)
                st.plotly_chart(fig)
            elif(graph == 'Bar'):
                x_axis = st.selectbox('Select X-axis', options = list(result.columns))
                y_axis = st.selectbox('Select Y-axis', options = list(result.columns))
                color = st.selectbox('Select Color', options = [None] + list(result.columns))
                facet_col = st.selectbox('Column Information', options = [None] + list(result.columns))    
                fig = px.bar(data_frame = result, x = x_axis, y = y_axis, color = color, facet_col = facet_col)
                st.plotly_chart(fig)
            elif(graph == 'Scatter'): 
                x_axis = st.selectbox('Select X-axis', options = list(result.columns))
                y_axis = st.selectbox('Select Y-axis', options = list(result.columns))
                color = st.selectbox('Select Color', options = [None] + list(result.columns))
                size = st.selectbox('Column Information', options = [None] + list(result.columns))    
                fig = px.scatter(data_frame = result, x = x_axis, y = y_axis, color = color, size = size)
                st.plotly_chart(fig)
            elif(graph == 'Pie'):
                names = st.selectbox('Choose Numerical Values', options = list(result.columns))
                values = st.selectbox('Choose Labels', options = list(result.columns))
                fig = px.pie(data_frame = result, names = names, values = values)
                st.plotly_chart(fig)
            elif(graph == 'sunburst'):
                path = st.multiselect('Choose Path', options = list(result.columns))
                fig = px.sunburst(data_frame = result, path = path, values = 'newcol')
                st.plotly_chart(fig)


st.markdown("---")
st.markdown("### Made with ❤️ by Sourav Upadhyay")
st.markdown("##### Powered by Streamlit 🚀")


