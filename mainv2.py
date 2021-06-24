from requests import get as fetch
import discord 
import csv 

class BotClient(discord.Client):
    def download_database(self):
        try:
            print("DOWNLOADING DATABASE")
            new_csv = fetch("https://www.police.govt.nz/stolenwanted/vehicles/csv/download?all=true&gzip=false&full=true", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'})
        except: 
            print("Connection Error!") 
            exit()
        new_csv = str(new_csv.text) 
        
        if(new_csv):
          print("DOWNLOAD SUCCESS")

        with open('stolen.csv', 'w', encoding='utf-8') as file_descriptor: 
            file_descriptor.write(new_csv) 
            file_descriptor.close() 

    def fix_null_chars(self, string)->str: 
        for line in string: 
            yield line.replace('\0', ' ') 

if __name__ == "__main__":
    clientz = BotClient()
    clientz.download_database()