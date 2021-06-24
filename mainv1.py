from requests import get as fetch
import discord
import csv

class BotClient(discord.Client):
    def download_database(self):
        try:
            print("DOWNLOADING DATABASE")
            fetch("https://www.police.govt.nz/stolenwanted/vehicles/csv/download?all=true&gzip=false&full=true", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'})
        except:
            print("Connection Error!") 
        
if __name__ == "__main__":
    clientz = BotClient()
    clientz.download_database()