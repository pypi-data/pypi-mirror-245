import aiohttp
import base64
from azure.devops.v7_1.pipelines import PipelinesClient
from msrest.authentication import BasicAuthentication  
import datetime
import pandas as pd
import asyncio

class PipelineUtil:

    def __init__(self,organization_url:str,pat:str,project_name:str,pipeline_id:str) -> None:
        self.organization_url = organization_url
        self.pat = pat
        self.project_name = project_name
        self.pipeline_id = pipeline_id
        pass

    async def fetch_data(self,run_id:str,**kwargs):
        """
        semaphore int : A semaphore manages an internal counter which is decremented
        """
        semaphore = kwargs.get("semaphore",10)
        if semaphore == 0:
            semaphore = 10
        sem = asyncio.Semaphore(semaphore)
        
        async with sem:
            encoded_pat = base64.b64encode((":" + self.pat).encode()).decode()
            headers = {"Authorization":"Basic "+encoded_pat}
            async with aiohttp.ClientSession() as session:
                url = f"{self.organization_url}/{self.project_name}/_apis/build/builds/{run_id}/timeline?api-version=6.0"

                print(url)
                async with session.get(url,headers=headers) as resp:
                    data = await resp.json()
                    data["run_id"] = run_id                
                    return data

    async def get_pipeline_build_ids(self,state:str="",result:str="",**kwargs):
        """
            state str: build state such as completed
            result str: build run result such as succeeded, failed
            start_year int: start year
            start_month int: start month
            start_day int: start day
        """
        credentials = BasicAuthentication('', self.pat)  
        client = PipelinesClient(self.organization_url,credentials)
        all_runs = client.list_runs(self.project_name,self.pipeline_id)
        all_succeed_run_ids=[]
        start_year = kwargs.get("start_year",0)
        start_month = kwargs.get("start_month",0)
        start_day = kwargs.get("start_day",0)
        for run in all_runs:
            if state and result:
                if run.state == state and run.result == result:
                    if run.created_date.year >= start_year and run.created_date.month >= start_month and run.created_date.day >= start_day:
                        all_succeed_run_ids.append(run.id)
            else:
                if run.created_date.year >= start_year and run.created_date.month >= start_month and run.created_date.day >= start_day:
                        all_succeed_run_ids.append(run.id)
        return all_succeed_run_ids
    

    def parse_pipeline_data_to_excel(excel_name:str,all_data:list):
        pd.DataFrame(columns=["create_date","build_id","stage","time"]).to_excel(excel_name,index=False)
        dataframe=pd.read_excel(excel_name)
        for json_content in all_data:
            records = json_content["records"]
            time_format = "%Y-%m-%dT%H:%M:%S"
            for record in records:
                if record["type"] == "Stage":
                    if record["startTime"]  and record["finishTime"]:
                        start_time = record["startTime"][:19]
                        end_time = record["finishTime"][:19]
                        start_time = datetime.datetime.strptime(start_time,time_format)
                        end_time = datetime.datetime.strptime(end_time,time_format)
                        time = (end_time-start_time).total_seconds()/3600
                    else:
                        time=None
                    new_data = {f'create_date':json_content["records"][0]["startTime"][:19],'build_id': json_content["run_id"], 'stage': record["name"], 'time':time}
                    dataframe = dataframe._append(new_data, ignore_index=True)
                    dataframe.to_excel(excel_name,index=False)