import pandas as pd
import os
import matplotlib
import seaborn as sns
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import telebot
import logging
import zipfile
from io import BytesIO
import openai
import random
from typing import List,Optional,Dict,Union

from Modules.Count_Token import token,num_tokens_from_list,find_and_store_pairs,find_max_index_below_threshold,subtract_value_from_list

from Classes.UserSession_API import UserSessionData
from Classes.DbConnect import DbConnect
from Classes.helper import Helper

db_connector = DbConnect()
connection = db_connector.connect()
UserSessions = UserSessionData()

base_directory = "temp"
# Enable logging
log_file = "bot.log"
dateformat = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s  - %(message)s",
    level=logging.INFO,
    filename=log_file,
    datefmt=dateformat,
)

logger = logging.getLogger(__name__)

TOKEN = os.environ("TOKEN")
bot = telebot.TeleBot(TOKEN)
helper = Helper(bot, logger, UserSessions)

openai.api_key = os.environ("openaitoken")

class Him():

    def __init__(self):
        super().__init__()

    @staticmethod
    def token(main_data) -> List :

        token = num_tokens_from_list(main_data)

        key_points = find_and_store_pairs(token,13000)

        key_points_keys = list(key_points.keys())

        key_points_keys = [0] + [key + 1 for key in key_points_keys]

        chunk_wishes = []
        for index, key in enumerate(key_points_keys):
            if index == len(key_points_keys) - 1:
                globals()[f'liste{key}'] = main_data[key:]
                chunk_wishes.append(f'liste{key}')
            else:
                next_key = key_points_keys[index + 1]
                globals()[f'liste{key}'] = main_data[key:next_key]
                chunk_wishes.append(f'liste{key}')

                print(f"key: {key}\nnext_key:{next_key}")
        
        random_selected = random.choice(chunk_wishes)

        selected_list = globals()[random_selected]

        return selected_list

    @staticmethod
    def get_completion2(prompt, model) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.75,
            #top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#", ";"],
            max_tokens=2000

        )
        return response.choices[0].message["content"]

    @staticmethod
    def create_zip_tosend():
        current_directory = os.getcwd()

        file_to_delete = os.path.join(current_directory, "him_general_images.zip")
        # Check if the file exists before attempting to delete
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
            print(f"File '{file_to_delete}' has been deleted.")

        relative_path = os.path.join(current_directory, "graphs")
        image1_path = os.path.join(relative_path, "toplam_plot1.png")
        image2_path = os.path.join(relative_path, "toplam_plot2.png")
        image3_path = os.path.join(relative_path, "toplam_plot3.png")

        os.makedirs(relative_path, exist_ok=True)

        # Assuming you have image files in the temp_dir
        image_files = [image1_path, image2_path, image3_path]

        # Create a ZIP archive and add the image files to it
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_file in image_files:
                zipf.write(image_file, os.path.basename(image_file))    

        # zip_buffer.seek(0)
        with open("him_general_images.zip", "wb") as f:
            f.write(zip_buffer.getbuffer())

        return os.path.join(current_directory, "him_general_images.zip")

    @staticmethod
    def delete_files_in_directory():

        project_path = os.getcwd()
        directory_path = os.path.join(project_path, "graphs")
        # Check if the directory exists
        try:
            if os.path.exists(directory_path):
                # List all files in the directory
                files = os.listdir(directory_path)
                # Loop through the files and delete each one
                for file in files:
                    file_path = os.path.join(directory_path, file)
                    print(file_path)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"Deleted: {file}")
                        else:
                            print(f"Skipped: {file} (not a file)")
                    except Exception as e:
                        print(f"Error deleting {file}: {str(e)}")
                print("All files have been deleted.")
            else:
                print(f"The directory '{directory_path}' does not exist.")
        except Exception as e:
            print(f"An error occurred while deleting files: {str(e)}")
            helper.inform_admins(
                f"❌ Got Error ❌\nwhile deleting files in {directory_path}\n\n{str(e)}"
            )

    def complaint_query_1(self,ILCE_ADI: str , MAHALLE_ADI: str, startDate:str, endDate:str) -> List:
        query1 = """
                select unit_name,count(*) as toplam from complaint3
                where district = :1 and NEIGHBOURHOOD = :2 AND APPLICATION_DATE > :3 AND APPLICATION_DATE < :4
                group by unit_name
                order by toplam desc
                """

        params = []

        params.append(ILCE_ADI)
        params.append(MAHALLE_ADI)
        params.append(startDate)
        params.append(endDate)

        cursor = connection.cursor()
        cursor.execute(query1, params)
        result1 = cursor.fetchall()

        cursor.close()

        result1 = [(item[0], *item[1:]) for item in result1]

        return result1
    
    def complaint_plot_1(self,df, ilce:str = '')  -> Optional[None]:
        # Set the color palette (e.g., 'viridis')
        sns.set_palette("viridis")

        # Create a bar plot
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=df, x="toplam", y="unit_name")
        plt.title(f"{ilce} - En Sık Şikayet İletilen 10 Birim")
        plt.xlabel("Şikayet Sayısı")
        plt.ylabel("Konu")

        # Add data labels to the bars
        for p in ax.patches:
            width = p.get_width()
            plt.text(
                width,
                p.get_y() + p.get_height() / 2,
                f"{int(width)}",
                ha="left",
                va="center",
                fontsize=10,
                color="black",
            )

        # Customize the grid lines (remove if not needed)
        sns.despine(left=True, bottom=True)

        # Invert the y-axis to show the highest value at the top
        # plt.gca().invert_yaxis()

        # Return the plot as a matplotlib figure
        directory = "graphs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(os.path.join(directory, "toplam_plot1.png"), dpi=300, bbox_inches="tight")
        #plt.show()
        try:
            plt.close()
        except:
            None
        return 1

    def complaint_query_2(self,ILCE_ADI: str, MAHALLE_ADI: str) -> List:
        query1 = """
                    SELECT
                        c.UNIT_NAME,
                        c.answer_duration_category,
                        COUNT(*) AS SAYI,
                        round((COUNT(*) / t.total_count) * 100,1) AS PERCENTAGE
                    FROM (
                        SELECT
                            UNIT_NAME,
                            answer_duration_days,
                            CASE
                                WHEN TO_NUMBER(NVL(REPLACE(answer_duration_days, ',', '.'), '0'), '999.9') < 7 THEN '7 Günden Az'
                                WHEN TO_NUMBER(NVL(REPLACE(answer_duration_days, ',', '.'), '0'), '999.9') BETWEEN 7 AND 14 THEN '7-14 Arası'
                                WHEN TO_NUMBER(NVL(REPLACE(answer_duration_days, ',', '.'), '0'), '999.9') > 14 THEN '14 Günden Fazla'
                            END AS answer_duration_category
                        FROM
                            complaint3
                        WHERE
                            DISTRICT = :1
                            AND NEIGHBOURHOOD = :2
                    ) c
                    JOIN (
                        SELECT UNIT_NAME, COUNT(*) AS total_count
                        FROM complaint3
                        WHERE DISTRICT = :1 AND NEIGHBOURHOOD = :2
                        GROUP BY UNIT_NAME
                    ) t
                    ON c.UNIT_NAME = t.UNIT_NAME
                    GROUP BY c.UNIT_NAME, c.answer_duration_category, t.total_count
                    ORDER BY SAYI DESC

                """

        params = []

        params.append(ILCE_ADI)
        params.append(MAHALLE_ADI)

        cursor = connection.cursor()
        cursor.execute(query1, params)
        result1 = cursor.fetchall()

        cursor.close()

        result1 = [(item[0], *item[1:]) for item in result1]

        return result1

    def complaint_plot_2(self,data, ilce:str = '')  -> Optional[None]:
        filtered_data = data[
            data["UNIT_NAME"].isin(data["UNIT_NAME"].unique()[:9])
        ].reset_index()

        grouped_units = (
            filtered_data.groupby(["UNIT_NAME", "ANSWER_DURATION_DAYS"])["SAYI"]
            .sum()
            .reset_index()
        )

        unit_total_counts = grouped_units.groupby("UNIT_NAME")["SAYI"].sum().reset_index()

        unit_total_counts = unit_total_counts.sort_values(by="SAYI", ascending=False)

        sorted_unit_names = unit_total_counts["UNIT_NAME"].tolist()
        grouped_units["UNIT_NAME"] = pd.Categorical(
            grouped_units["UNIT_NAME"], categories=sorted_unit_names, ordered=True
        )

        grouped_units = grouped_units.sort_values(
            by=["UNIT_NAME", "SAYI"], ascending=[True, False]
        )

        column_order = data["ANSWER_DURATION_DAYS"].unique()

        table = pd.pivot_table(
            grouped_units, index=["UNIT_NAME"], columns=["ANSWER_DURATION_DAYS"]
        ).fillna(0)

        # table = table.dropna(axis=1).astype(int)

        grouped_df = (
            data.groupby(["UNIT_NAME", "ANSWER_DURATION_DAYS"])
            .sum()
            .reset_index()
            .fillna(0)
        )

        pivot_table = grouped_df.pivot(
            index="UNIT_NAME", columns="ANSWER_DURATION_DAYS", values="SAYI"
        ).fillna(0)

        font_color = "#525252"
        colors = ["#A7E5A5", "#FF6B6B", "#FFD166", "#6A0572", "#AB83A1", "#F5D6C6"]

        fig, axes = plt.subplots(3, 3, figsize=(10, 10), facecolor="#e8f4f0")
        fig.delaxes(ax=axes[2, 2])

        table = table.reindex(table.sum().sort_values(ascending=False).index, axis=1)
        table = table.head(8)


        for i, (idx, row) in enumerate(table.iterrows()):
            ax = axes[i // 3, i % 3]
            row = row[row.gt(row.sum() * 0.01)]
            wedges, texts, autotexts = ax.pie(
                row,
                labels=row.values,
                startangle=30,
                wedgeprops=dict(width=0.5),  # For donuts
                colors=colors,
                textprops={"color": font_color},
                pctdistance=0.75,
                autopct="%1.0f%%",  # Display percentages on the pie chart
            )
            ax.set_title(idx, fontsize=8, color=font_color)

            legend = plt.legend(
                [x[1] for x in row.index],
                bbox_to_anchor=(1.3, 0.87),  # Legend position
                loc="upper left",
                ncol=1,
                fancybox=True,
            )
            for text in legend.get_texts():
                plt.setp(text, color=font_color)  # Legend font color

            # Add percentage labels inside the pie chart slices
            for autotext in autotexts:
                autotext.set(size=7, color=font_color)

        fig.subplots_adjust(wspace=0.2)  # Space between charts

        title = fig.suptitle(f"{ilce} - TALEP ÇÖZÜM SÜRELERİ", y=0.95, fontsize=20, color=font_color)
        # To prevent the title from being cropped
        plt.subplots_adjust(top=0.85, bottom=0.15)
        directory = "graphs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(
            os.path.join(directory, "toplam_plot2.png"), dpi=300, bbox_inches="tight"
        )

        # plt.show()
        try:
            plt.close()
        except:
            None
        return 1

    def complaint_query_3(self,ILCE_ADI: str, MAHALLE_ADI: str) -> pd.DataFrame:
        query1 = """
                    select 
                        c.UNIT_NAME,
                        c.RESULT,
                        c.SAYI,
                        q.SUM_SAYI
                    from 
                    (
                        select UNIT_NAME, RESULT, COUNT(*) AS SAYI 
                        from complaint3 
                        WHERE DISTRICT = :1 AND NEIGHBOURHOOD = :2
                        GROUP BY UNIT_NAME, RESULT
                    ) c
                    JOIN
                    (
                        select UNIT_NAME, SUM(SAYI) as SUM_SAYI
                        from
                        (
                            select UNIT_NAME, RESULT, COUNT(*) AS SAYI 
                            from complaint3 
                            WHERE DISTRICT = :1 AND NEIGHBOURHOOD = :2
                            GROUP BY UNIT_NAME, RESULT
                        ) subquery
                        GROUP BY UNIT_NAME
                    ) q
                    ON c.UNIT_NAME = q.UNIT_NAME

                """

        params = []

        params.append(ILCE_ADI)
        params.append(MAHALLE_ADI)

        cursor = connection.cursor()
        cursor.execute(query1, params)
        result1 = cursor.fetchall()

        cursor.close()

        result1 = [(item[0], *item[1:]) for item in result1]

        df1 = pd.DataFrame(result1, columns=["UNIT_NAME", "RESULT", "SAYI", "SUM_SAYI"])

        df1 = df1.sort_values("SUM_SAYI", ascending=False)

        return df1

    def complaint_plot_3(self,data, ilce:str )  -> Optional[None]:
        # list of units
        unit_names = data["UNIT_NAME"].unique().tolist()
        # for each unit, get the count of complaints for each RESULT value and store in a list with the unit name as the key
        unit_counts = {
            unit: data[data["UNIT_NAME"] == unit]["SAYI"].tolist() for unit in unit_names
        }
        # sum the counts for each unit and store in a list with the unit name as the key
        unit_counts = {unit: sum(counts) for unit, counts in unit_counts.items()}
        # get top 8 units with the highest count of complaints
        unit_counts = dict(
            sorted(unit_counts.items(), key=lambda item: item[1], reverse=True)[:8]
        )
        # for each unit, create dataframes with the count of complaints for each RESULT names and values with the unit name as the key
        dataFrames = {
            unit: data[data["UNIT_NAME"] == unit]
            .groupby("RESULT")["SAYI"]
            .sum()
            .reset_index()
            for unit in unit_names
        }
        # order the dataframes by the count of complaints for each RESULT value
        dataFrames = {
            unit: df.sort_values("SAYI", ascending=False) for unit, df in dataFrames.items()
        }
        # get only top 8 dataframes
        dataFrames = {unit: df.head(7) for unit, df in dataFrames.items()}
        # get all unique RESULT values from all dataframes
        RESULT_names = data["RESULT"].unique().tolist()
        # order by name alphabetically
        RESULT_names.sort()

        # create a dataframe with the count of complaints for each RESULT value for each unit add 0 if the unit does not have a count for a RESULT value
        dataFrames = {
            unit: df.set_index("RESULT").reindex(RESULT_names, fill_value=0).reset_index()
            for unit, df in dataFrames.items()
        }
        print(dataFrames)
        # order the dataframes RESULT values by the RESULT name ascending
        for unit, df in dataFrames.items():
            df["RESULT"] = pd.Categorical(df["RESULT"], RESULT_names, ordered=True)
        print(dataFrames)
        # get UNIT_NAME frames where top 8 unit_counts are in
        dataFrames = {unit: df for unit, df in dataFrames.items() if unit in unit_counts}
        
        # get top 8 of dict
        dataFrames = dict( sorted(dataFrames.items(), key=lambda item: unit_counts[item[0]], reverse=True)[:8] )
        

        font_color = "#525252"
        colors = [
            "#A7E5A5",
            "#FF6B6B",
            "#FFD166",
            "#6A0572",
            "#AB83A1",
            "#F5D6C6",
            "#FFC0CB",
            "#FF1493",
            "#FF00FF",
            "#C71585",
            "#DB7093",
            "#FFB6C1",
            "#FFA07A",
            "#FF7F50",
            "#FF6347",
            "#FF4500",
            "#FF8C00",
            "#FFA500",
        ]

        fig, axes = plt.subplots(3, 3, figsize=(10, 10), facecolor="#e8f4f0")
        for ax in axes.flat:
            ax.axis("off")

        explodeValues = (
            0.05,
            0.1,
            0.125,
            0.15,
            0.175,
            0.2,
            0.225,
            0.25,
            0.275,
            0.3,
            0.325,
            0.35,
        )

        

        # use dataFrames to create pie charts for each unit get total count of results for each unit
        for ax, col in zip(axes.flat, dataFrames.keys()):
            explodeValues = [0.05] * len(dataFrames[col])
            leg = ax.pie(
                dataFrames[col]["SAYI"],
                labels=dataFrames[col].index,
                explode=explodeValues[:len(dataFrames[col])],
                startangle=180,
                wedgeprops=dict(width=0.5),
                colors=colors,
                pctdistance=0.75,
                textprops={"color": font_color},
            )
            ax.set_title(col, fontsize=8, color=font_color)
            ax.set(aspect="equal")
            # replace labels with count of complaints for each RESULT value, if the count is 0, do not display the label
            for i, (idx, row) in enumerate(dataFrames[col].iterrows()):
                if row["SAYI"] > 0:
                    # calculate the percentage of the count of complaints for each RESULT value
                    percentage = row["SAYI"] / sum(dataFrames[col]["SAYI"]) * 100
                    # add the percentage to the label
                    leg[1][i].set_text(f'{row["SAYI"]} ({percentage:.0f}%)')
                else:
                    leg[1][i].set_text("")

        # last row is legend, add global legend to last row
        axes[0, 0].legend(
            leg[0],
            dataFrames[col]["RESULT"],
            bbox_to_anchor=(3.1, -1.5),
            loc="upper center",
            ncol=1,
            fancybox=True,
        )

        # add percentage labels inside the pie chart slices
        for ax in axes.flat:
            for autotext in ax.texts:
                autotext.set(size=7, color=font_color)
        fig.suptitle(f"{ilce} - SONUÇLANAN TALEPLER (ORAN)", y=0.95, fontsize=20, color=font_color)
        directory = "graphs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(
            os.path.join(directory, "toplam_plot3.png"), dpi=300, bbox_inches="tight"
        )
        plt.show()
        try:
            plt.close()
        except:
            None
        return 1

    def plot_complaints(self,ILCE_ADI: str , MAHALLE_ADI: str):
        
        Him.delete_files_in_directory()

        try:
            image1 = self.complaint_plot_1(pd.DataFrame(self.complaint_query_1(ILCE_ADI,MAHALLE_ADI)[:10], columns=["unit_name", "toplam"]),ILCE_ADI)
        except Exception as e:
            logger.error(
                f"{self.plot_complaints.__name__} PLOT 1 ERROR: %s", str(e),)
            helper.inform_admins(  f"{self.plot_complaints.__name__} ❌ PLOT 1 ERROR: ❌\n  {str(e)}")

        try:
            image2 = self.complaint_plot_2(pd.DataFrame(self.complaint_query_2(ILCE_ADI,MAHALLE_ADI), columns=["UNIT_NAME", "ANSWER_DURATION_DAYS", "SAYI", "PERCENTAGE"]),ILCE_ADI)
        except Exception as e:
            logger.error(
                f"{self.plot_complaints.__name__} PLOT 1 ERROR: %s", str(e),)
            helper.inform_admins(  f"{self.plot_complaints.__name__} ❌ PLOT 1 ERROR: ❌\n  {str(e)}")

        try:

            df1 = pd.DataFrame(self.complaint_query_3(ILCE_ADI,MAHALLE_ADI), columns=["UNIT_NAME", "RESULT", "SAYI", "SUM_SAYI"])
            df1 = df1.sort_values("SUM_SAYI", ascending=False)

            image3 = self.complaint_plot_3((df1),ILCE_ADI)

        except Exception as e:
            logger.error(
                f"{self.plot_complaints.__name__} PLOT 1 ERROR: %s", str(e),)
            helper.inform_admins(  f"{self.plot_complaints.__name__} ❌ PLOT 1 ERROR: ❌\n  {str(e)}")

    def MainIssues(self,district:str, neighborhood:str, StartDate:str, EndDate:str) -> List[Dict[str, any]]:

        query1 = """
                    SELECT maın_topıc,
                        COUNT(*) AS toplam_sayı,
                        ROUND(COUNT(CASE WHEN result = 'BİLGİLENDİRİLDİ' THEN 1 END) / COUNT(*) * 100, 1) AS BILGILENDIRILDI,
                        ROUND(COUNT(CASE WHEN result = 'TALEP YERİNE GETİRİLDİ' THEN 1 END) / COUNT(*) * 100, 1) AS TALEP_YERINE_GETIRILDI,
                        ROUND(COUNT(CASE WHEN result = 'SORUMLULUK ALANI DIŞINDA' THEN 1 END) / COUNT(*) * 100, 1) AS SORUMLULUK_ALANI_DISINDA,
                        ROUND(COUNT(CASE WHEN result = 'UYGUN GÖRÜLMEDİ' THEN 1 END) / COUNT(*) * 100, 1) AS UYGUN_GORULMEDI,
                        ROUND(COUNT(CASE WHEN result = 'ÇALIŞMA DEVAM EDİYOR' THEN 1 END) / COUNT(*) * 100, 1) AS CALISMA_DEVAM_EDIYOR,
                        ROUND(COUNT(CASE WHEN result = 'İLGİLİ BİRİME AKTARILDI' THEN 1 END) / COUNT(*) * 100, 1) AS ILGILI_BIRIME_AKTARILDI,
                        ROUND(COUNT(CASE WHEN result = 'BEKLEMEDE' THEN 1 END) / COUNT(*) * 100, 1) AS BEKLEMEDE
                    FROM COMPLAINT3
                    WHERE dıstrıct = :1 AND neıghbourhood = :2 AND APPLICATION_DATE > :3 AND APPLICATION_DATE < :4 
                    GROUP BY maın_topıc
                    ORDER BY toplam_sayı desc
                    """
        params = []

        params.append(district)
        params.append(neighborhood)
        params.append(StartDate)
        params.append(EndDate)

        cursor = connection.cursor()

        cursor.execute(query1, params)
        result1 = cursor.fetchall()

        cursor.close()

        result1 = [(item[0], *item[1:]) for item in result1]
        df1 = pd.DataFrame(result1, columns=['Ana Konu', 'Sayı','BILGILENDIRILDI','TALEP_YERINE_GETIRILDI','SORUMLULUK_ALANI_DISINDA','UYGUN_GORULMEDI','CALISMA_DEVAM_EDIYOR','ILGILI_BIRIME_AKTARILDI','BEKLEMEDE'])  # Use result1 instead of res
        df1['Ana Konu'] = df1['Ana Konu'].str.strip("\n")

        df_as_dict = df1.to_dict()

        records_as_dict = df1.to_dict(orient='records')

        # top10Subjects = df1['Ana Konu'].head(10)
        return records_as_dict

    def SubIssues(self,district:str, neighborhood:str, StartDate:str, EndDate:str,main_topic:str) -> List[Dict[str, any]]:
        
        main_topic = main_topic+"\n"

        query1 = """
        SELECT TOPIC_DETAILED,
        COUNT(*) AS toplam_sayı,
        ROUND(COUNT(CASE WHEN result = 'BİLGİLENDİRİLDİ' THEN 1 END) / COUNT(*) * 100, 1) AS BILGILENDIRILDI,
        ROUND(COUNT(CASE WHEN result = 'TALEP YERİNE GETİRİLDİ' THEN 1 END) / COUNT(*) * 100, 1) AS TALEP_YERINE_GETIRILDI,
        ROUND(COUNT(CASE WHEN result = 'SORUMLULUK ALANI DIŞINDA' THEN 1 END) / COUNT(*) * 100, 1) AS SORUMLULUK_ALANI_DISINDA,
        ROUND(COUNT(CASE WHEN result = 'UYGUN GÖRÜLMEDİ' THEN 1 END) / COUNT(*) * 100, 1) AS UYGUN_GORULMEDI,
        ROUND(COUNT(CASE WHEN result = 'ÇALIŞMA DEVAM EDİYOR' THEN 1 END) / COUNT(*) * 100, 1) AS CALISMA_DEVAM_EDIYOR,
        ROUND(COUNT(CASE WHEN result = 'İLGİLİ BİRİME AKTARILDI' THEN 1 END) / COUNT(*) * 100, 1) AS ILGILI_BIRIME_AKTARILDI,
        ROUND(COUNT(CASE WHEN result = 'BEKLEMEDE' THEN 1 END) / COUNT(*) * 100, 1) AS BEKLEMEDE
        FROM COMPLAINT3
        WHERE dıstrıct = :1 AND neıghbourhood = :2 AND APPLICATION_DATE > :3 AND APPLICATION_DATE < :4  AND maın_topıc=:5
        GROUP BY TOPIC_DETAILED
        ORDER BY toplam_sayı desc

    """
        params = []

        params.append(district)
        params.append(neighborhood)
        params.append(StartDate)
        params.append(EndDate)
        params.append(main_topic)
        
        cursor = connection.cursor()
        cursor.execute(query1, params)
        result1 = cursor.fetchall()
        cursor.close()
        
        result1 = [(item[0].rstrip('\n'), *item[1:]) for item in result1]
        
        df1 = pd.DataFrame(result1, columns=['Ana Konu', 'Sayı','BILGILENDIRILDI','TALEP_YERINE_GETIRILDI','SORUMLULUK_ALANI_DISINDA','UYGUN_GORULMEDI','CALISMA_DEVAM_EDIYOR','ILGILI_BIRIME_AKTARILDI','BEKLEMEDE'])  # Use result1 instead of res
        
        df_as_dict = df1.to_dict()

        records_as_dict = df1.to_dict(orient='records')

        # top10Subjects = df1['Ana Konu'].head(10)
        return records_as_dict
    
    def Gpt_Maintopic_Data(self,district:str, neighborhood:str, StartDate:str, EndDate:str,main_topic:str) -> List:

        main_topic = main_topic+"\n"

        query1 = """
            select ISTEK_OZETI FROM WISH4
                where ISTEK_OZETI is not null and (basvuru_no,basvuru_yili) IN 
                (
                SELECT basvuru_no,EXTRACT(YEAR FROM application_date) AS application_date
                FROM COMPLAINT3
                WHERE DISTRICT = :1 AND NEIGHBOURHOOD = :2 AND APPLICATION_DATE > :3 AND APPLICATION_DATE < :4 AND  MAIN_TOPIC = :5 )
                """

        params = []

        params.append(district)
        params.append(neighborhood)
        params.append(StartDate)
        params.append(EndDate)
        params.append(main_topic)

        cursor = connection.cursor()
        cursor.execute(query1, params)
        result1 = cursor.fetchall()
        cursor.close()

        result1 = [(item[0].rstrip('\n'), *item[1:]) for item in result1]

        df1 = pd.DataFrame(result1, columns=['ISTEK_OZETI'])  # Use result1 instead of res

        main_data_for_gpt = df1["ISTEK_OZETI"].tolist()

        return main_data_for_gpt

    def Gpt_Subtopic_Data(self,district:str, neighborhood:str, StartDate:str, EndDate:str,topic_detailed:str) -> List:

        query1 = """
                select ISTEK_OZETI FROM WISH4
                where ISTEK_OZETI is not null and (basvuru_no,basvuru_yili) IN 
                (
                SELECT basvuru_no,EXTRACT(YEAR FROM application_date) AS application_date
                FROM COMPLAINT3
                WHERE DISTRICT = :1 AND NEIGHBOURHOOD = :2 AND APPLICATION_DATE > :3 and  APPLICATION_DATE < :4   and  TOPIC_DETAILED = :5 )

                    """

        params = []

        params.append(district)
        params.append(neighborhood)
        params.append(StartDate)
        params.append(EndDate)
        params.append(topic_detailed)

        cursor = connection.cursor()
        cursor.execute(query1, params)

        result1 = cursor.fetchall()
        print(result1)
        cursor.close()

        result1 = [(item[0].rstrip('\n'), *item[1:]) for item in result1]

        df1 = pd.DataFrame(result1, columns=['ISTEK'])  # Use result1 instead of res

        main_data_for_gpt = df1["ISTEK"].tolist()

        return main_data_for_gpt

    def gpt_main(self,wishes_for_gpt) -> Union[str, int]:

        try:
            # Check if the user has provided both location and date

            row2 = wishes_for_gpt
            print(row2)
            
            template21 = f"""
                                    You are an data analist and personal assistant for mayor of İzmir. Mayor can read only in Turkish language. You will be provided with list demilited by triple quotes. The list contains some wishes or complaints from citizen.                  

                                    I want you to consider wishes and complaint to answer them globally as a report as like below;
                                    Do not forget report titles cannot contain more than 5 items. 

                                    1 - <b>Ana Konular</b>
                                        -
                                        -
                                        -
                                        -
                                        -
                                    2 - <b>Kök Nedenler</b>
                                        -
                                        -
                                        -
                                        -
                                        -

                                    3 - <b>Duygu Analizi</b>
                                    Analyze the sentiments expressed by citizens in the provided sample data, and categorize them based on the various feelings they convey. Kindly provide the top five most frequently encountered distinct emotions with percentage, along with some brief (more than one) illustrative examples from the dataset. Do not categorized emotions as "Request" and "Complaint." Additionally, please keep in mind that the Mayor can only comprehend the Turkish language.
                                    I want answer will be as like below;

                                        - <b>Korku</b> - % 60 - Köpekler saldırıyor, kanal kapağı açık, ...
                                        - <b>Öfke</b> - % 20 - Yardım henüz gelmedi, otobüs gelmiyor iş yerine geç kaldım  ....
                                        -
                                        -
                                        -                 


                                                \"\"\"{row2}\"\"\
                                            """
            print(template21)
            if len(wishes_for_gpt) > 0:


                print("GPT IS WORKING")
                gpt_main_response = Him.get_completion2(
                    template21, model="gpt-3.5-turbo-16k"
                )

                print("GPT DONE")

                # if len(gpt_main_response) > 4096: split the message into multiple messages
                if len(gpt_main_response) > 4096:
                    split_index = gpt_main_response.rfind("\n\n", 0, 4096)
                    
                    return split_index
                else:
                    print(gpt_main_response)
                    
                    return gpt_main_response
                
                
            else:
                
                helper.inform_admins(
                    f" NO DATA in gpt_topic_analiz"
                )
                

        except Exception as e:
                logging.error(f"Error in gpt_main : {e}")
                helper.inform_admins(
                    f" ❌ Got Error ❌\nin gpt_main:\n\n{str(e)}"
                )










