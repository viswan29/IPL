import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import time

class CricketScoreExtractor():
    def __init__(self):
        self.base_url="https://stats.espncricinfo.com"
        
    def BS(self,year):
        if year in (2020,2007):
            self.match_url="/ci/engine/records/team/match_results.html?id="+str(year)+"%"+str(year+1).replace('0','F',1)+";trophy=117;type=season"
        elif year==2010:
            self.match_url="/ci/engine/records/team/match_results.html?id="+str(year-1)+"%"+str(year).replace('0','F',1)+";trophy=117;type=season"
        else:
            self.match_url="/ci/engine/records/team/match_results.html?id="+str(year)+";trophy=117;type=season"
            
        html=urllib.request.urlopen(self.base_url+self.match_url).read()
        self.bs=BeautifulSoup(html,'lxml')
        return self.bs
        
    def ExtractMatchResults(self,year):
        for i in year:
            self.table_data_list=[]
            self.BS(i)
            headers_soup=self.bs.findAll("tr",{'class':'head'})
            try:
                headers_tag=headers_soup[0].findAll("th")
            except IndexError:
                continue
            list_headers=[]
            for header in headers_tag:
                list_headers.append(header.text)
            table_body=self.bs.findAll("tbody")[0]
            rows=table_body.findAll("tr")
            for row in rows:
                row_data=[]
                col=row.findAll("td")
                row_data=[c.text.strip() for c in col]
                self.table_data_list.append(row_data)
            a=pd.DataFrame(self.table_data_list)
            a.columns=list_headers
            a.to_csv('MatchResults_'+str(i)+'.csv',index=False)
        
if __name__ == '__main__':
    obj = CricketScoreExtractor()
    lst=[2019,2020]
    sttime=time.time()
    obj.ExtractMatchResults(lst)
    entime=time.time()
    print(f"Time Taken: {(entime-sttime)/60} mins")