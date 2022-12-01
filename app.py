import streamlit as st
import pandas as pd
import plotly.express as px


@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=True).encode('utf-8')

def download_button(df_read, title_button, filename, key):
    csv = convert_df(df_read)
    return st.download_button(title_button, csv, filename, "text/csv", key=key)


st.set_page_config(page_title='Excel Plotter',
                    layout="wide")
st.title('Excel Plotter 📊')
st.subheader('Feed me with your Excel file')

uploaded_file = st.file_uploader("Choose a XLSX file", type='xlsx')

if uploaded_file:
    st.markdown('---')

    df_read = pd.read_excel(uploaded_file, engine='openpyxl')

    df = df_read.dropna(subset=["Fatal Risk"])
    st.dataframe(df)

    if "Jawaban CCFV" in df:
        column_jawaban_ccfv = "Jawaban CCFV"
    else:
        column_jawaban_ccfv = "Jawaban CCC"
    
    total_fatal_risk=len(df)
    total_catatan_no=df["Catatan No"].count()

    left_column, middle, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Fatal Risk:")
        st.subheader(total_fatal_risk)
    with right_column:
        st.subheader("Total Catatan No:")
        st.subheader(total_catatan_no)
   

    groupby_column = st.selectbox(
        "What would you like to analyze ?",
        ('Fatal Risk', 'Critical Control', 'Lokasi', 'Division', 'Department', 'Worker', 'Section'),
        key=1
    )

    output_columns = ['No. ID', 'Catatan No']
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].count()
    df_grouped.rename(columns = {'No. ID':'Count of Fatal Risk', 'Catatan No': 'Jawaban No'}, inplace = True)
    df_grouped = df_grouped.sort_values(by='Count of Fatal Risk', ascending=False)
    df_grouped = df_grouped.reset_index(drop=True)
    df_grouped.index += 1
    download_button(df_grouped, "Download Table", "Fatal Risk.csv", "download-table-1")
    st.table(df_grouped)



    groupby_column_fig = st.selectbox(
        "What would you like to analyze ?",
        ('Fatal Risk', 'Critical Control', 'Lokasi', 'Division', 'Department', 'Worker', 'Section'),
        key=2
    )

    df_grouped_fig = df.groupby(by=[groupby_column_fig], as_index=False)[output_columns].count()
    df_grouped_fig.rename(columns = {'No. ID':'Count of Fatal Risk', 'Catatan No': 'Jawaban No'}, inplace = True)
    df_ordered_fig = df_grouped_fig.sort_values(by='Count of Fatal Risk', ascending=False)

    fig = px.bar(
        df_ordered_fig,
        x=groupby_column_fig,
        y='Count of Fatal Risk',
        color='Jawaban No',
        color_continuous_scale=['green', 'yellow', 'red'],
        template='plotly_white',
        title=f'<b>Count of Fatal Risk & Jawaban No by {groupby_column_fig}'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("CCFV Ad-Hoc Submitted")

    df_ccfv_submitted = df.drop_duplicates(subset=["No. ID"])

    df_done = df_ccfv_submitted.copy()
    df_done.drop(df_done[df_done['Status Pekerjaan'] == "CC Checking"].index, inplace = True)
    
    df_check = df_ccfv_submitted.copy()
    df_check.drop(df_check[df_check['Status Pekerjaan'] != "CC Checking"].index, inplace = True)


    left_ccfv_done, right_cc_check = st.columns(2)
    with left_ccfv_done:
        total_ccfv_done=len(df_done)
        st.subheader("Total CCFV Done & CC Done:")
        st.subheader(total_ccfv_done)
    with right_cc_check:
        total_cc_checking=len(df_check)
        st.subheader("Total CC Checking:")
        st.subheader(total_cc_checking)

    groupby_column_fig_submit = st.selectbox(
        "What would you like to analyze ?",
        ('Department','Fatal Risk', 'Critical Control', 'Lokasi', 'Division', 'Worker', 'Section'),
        key=3
    )

    df_done_grouped = df_done.groupby(by=groupby_column_fig_submit, as_index=False)[output_columns].count()
    df_done_grouped.rename(columns = {'No. ID':'Count of Fatal Risk', 'Catatan No': 'Jawaban No'}, inplace = True)

    df_check_grouped = df_check.groupby(by=groupby_column_fig_submit, as_index=False)[output_columns].count()
    df_check_grouped.rename(columns = {'No. ID':'Count of Fatal Risk', 'Catatan No': 'Jawaban No'}, inplace = True)

    fig_done = px.bar(
        df_done_grouped,
        x=groupby_column_fig_submit,
        y='Count of Fatal Risk',
        color='Jawaban No',
        color_continuous_scale=['green', 'yellow', 'red'],
        template='plotly_white',
        title=f'<b>CCFV Done & CC Done by {groupby_column_fig_submit}'
    )

    fig_check = px.bar(
        df_check_grouped,
        x=groupby_column_fig_submit,
        y='Count of Fatal Risk',
        color='Jawaban No',
        color_continuous_scale=['green', 'yellow', 'red'],
        template='plotly_white',
        title=f'<b>CC Checking by {groupby_column_fig_submit}'
    )

    left_fig, right_fig = st.columns(2)
    with left_fig:
        st.plotly_chart(fig_done, use_container_width=True)

        
        
    with right_fig:
        # if(df_check.empty):
            # st.subheader("Tidak Ada CC Checking")
        # else:
        st.plotly_chart(fig_check, use_container_width=True)

    
    st.header("Keterangan Catatan No")

    column_output = st.multiselect(
        "Select the column output:",
        options=["Tanggal", "Pekerjaan", "Detail Pekerjaan", "Lokasi", "Status Pekerjaan", "Fatal Risk", "Critical Control", "Pertanyaan", column_jawaban_ccfv, "Catatan No", "Catatan Solve", "Worker ID", "Worker", "Division", "Department", "Section", "List of Workers ID", "List of Workers"],
        default=["Fatal Risk", "Catatan No"]
    )
    
    df_catatan_no=df.dropna(subset=['Catatan No'])
    df_catatan_no = df_catatan_no.reset_index(drop=True)
    df_catatan_no.index += 1

    download_button(df_catatan_no[column_output], "Download Table", "Catatan No.csv", "download-table-2")
    st.dataframe(df_catatan_no[column_output])

    st.header("Jumlah " + column_jawaban_ccfv)


    df_jawaban_CCFV=df.dropna(subset=[column_jawaban_ccfv])
    df_jawaban_CCFV.drop(df_jawaban_CCFV[df_jawaban_CCFV[column_jawaban_ccfv] == "Yes" ].index, inplace = True)
    total_jawaban_CCFV=len(df_jawaban_CCFV)

    left_column_bot, right_column_bot = st.columns(2)

    with left_column_bot:
        st.dataframe(df_jawaban_CCFV[column_jawaban_ccfv].value_counts())
    with right_column_bot:
        st.subheader("Total " + column_jawaban_ccfv + " :")
        st.subheader(f"{total_jawaban_CCFV}")

    
    
