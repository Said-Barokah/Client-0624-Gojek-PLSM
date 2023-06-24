import pandas as pd, plspm.config as c
from plspm.plspm import Plspm
from plspm.scheme import Scheme
from plspm.mode import Mode
from plspm.bootstrap import Bootstrap
import streamlit as st
import time

def app():
    st.title("Web Analisis Tingkat Kepuasan Pelanggan")
    data_master = st.file_uploader("upload datas_masteret berformat xlsx", type=['xlsx'])
    if data_master is not None:
        
        data_master = pd.read_excel(data_master)
        # hide_table_row_index = """
        #     <style>
        #     thead tr th:first-child {display:none}
        #     tbody th {display:none}
        #     </style>
        #     """
        #050979
        # Inject CSS with Markdown
        # st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.write(data_master)

            # st.success('Outer Model Sudah di Inisialisai')
        iterasi= st.number_input("Berapa banyak iterasi untuk tahap bootstrapping", min_value=1, value=500)
        if st.button("Jalankan PLSPM"):
            with st.spinner('Tunggu inisialisasi Inner Model'):
                time.sleep(3) 
            structure = c.Structure()
            structure.add_path(["Content"], ["Satisfaction"])
            structure.add_path(["Accuracy"], ["Satisfaction"])
            structure.add_path(["Format"], ["Satisfaction"])
            structure.add_path(["ease"], ["Satisfaction"])
            structure.add_path(["Timeliness"], ["Satisfaction"])
            # st.success('Inner Model Sudah di Inisialisai')
            with st.spinner('Tunggu inisialisasi Outer Model'):
                time.sleep(3)
                config = c.Config(structure.path(), scaled=False)
                config.add_lv_with_columns_named("Content", Mode.A, data_master, "Content.")
                config.add_lv_with_columns_named("Accuracy", Mode.A, data_master, "Accuracy.")
                config.add_lv_with_columns_named("Format", Mode.A, data_master, "Format.")
                config.add_lv_with_columns_named("ease", Mode.A, data_master, "Ease.")
                config.add_lv_with_columns_named("Timeliness", Mode.A, data_master, "Timeliness.")
                config.add_lv_with_columns_named("Satisfaction", Mode.A, data_master, "Satisfaction.") 
            plspm_calc = Plspm(data_master, config, Scheme.CENTROID)
            st.header('Tahap 1 Measurement Model Assessment')
            st.subheader('Unidimensionality')
            st.info('indikator dinyatakan mewakili dengan baik variabel yang diukurnya dengan melihat nilai cronbach alpha > 0.7')

            data=pd.DataFrame(plspm_calc.unidimensionality())
            st.line_chart(data[["cronbach_alpha","dillon_goldstein_rho","eig_1st","eig_2nd"]])
            st.write(data)

            st.subheader('Pengujian keeratan hubungan dan reliability indikator')
            st.info('Setiap indikator dinyatakan memiliki hubungan dan reliability yang bagus untuk mengukur variabelnya masing-masing melalui nilai outer loading atau loading factor > 0.7 dan communality test > 0.5')
            data=pd.DataFrame(plspm_calc.outer_model())
            st.line_chart(data)
            st.write(data)


            st.subheader('Pengujian cross-loadings')
            st.info('indikator dari setiap variabel mengukur dengan baik variabelnya. Cross loading merupakan pengujian dari Diskriminant Validity')
            data=pd.DataFrame(plspm_calc.crossloadings())
            st.line_chart(data)
            st.write(data)


            st.header('Tahap 2 Structural Model Assessment')
            st.subheader('Persamaan regresi tiap variabel endogen')
            data=pd.DataFrame(plspm_calc.inner_model())
            st.line_chart(data[["estimate", "std error", "t", "p>|t|"]])
            st.write(data)


            st.subheader('Koefisien determinasi R2 dan Redundancy')
            st.info('Redundancy, nilai mean_redundancy yang semakin besar menunjukkan kemampuan variabel independent semakin mampu mengukur variasi variabel endogen nya')
            data=pd.DataFrame(plspm_calc.inner_summary())
            st.line_chart(data[["r_squared",  "r_squared_adj",  "block_communality" ,"mean_redundancy" ,"ave"]])
            st.write(data)



            st.subheader('the Goodness-of-Fit (GoF)')
            st.info('Semakin besar nilai GoF menunjukkan semakin bagusnya kinerja dan kualitas secara umum dari model pengukuran baik inner maupun outer model')
            st.write('GoF = ',plspm_calc.goodness_of_fit())
            data=pd.DataFrame(plspm_calc.effects())
            st.line_chart(data[["direct",  "indirect",  "total"]])
            st.write(data)
            data = pd.DataFrame(plspm_calc.path_coefficients())
            st.write(data)


            st.header('Tahap 3 Bootstrapping')

            plspm_calc = Plspm(data_master, config, bootstrap=True, bootstrap_iterations=iterasi)
            
            st.subheader('Direct effects for paths')
            data = pd.DataFrame(plspm_calc.bootstrap().paths())
            st.line_chart(data)
            st.write(data)

            st.subheader('Total effects for paths')
            data = pd.DataFrame(plspm_calc.bootstrap().total_effects())
            st.line_chart(data)
            st.write(data)

            st.subheader('Koefisien Determinasi (R-squared)')
            data = pd.DataFrame(plspm_calc.bootstrap().total_effects())
            st.line_chart(data)
            st.write(data)


            st.subheader('Bobot model')
            data = pd.DataFrame(plspm_calc.bootstrap().weights())
            st.line_chart(data)
            st.write(data)

















