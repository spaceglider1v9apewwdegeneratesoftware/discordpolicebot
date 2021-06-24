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

    def search(self, plate)->list:
        csv_file = csv.reader(self.fix_null_chars(open('stolen.csv', "r", encoding='utf-8')), delimiter=",")
        found = 1 
        for row in csv_file: 
            if(row[0] == plate.upper()): 
                return (row) 
                found = 1
            elif(row[0] == plate.lower()):
                return (row)
                found = 1
        if(found == 0): 
            return -1
            
    def parse_data(self, data)->str: 
        if (data != -1): 
            plate_description = ""
            if(data[0]): 
              title = "Plate of a stolen car has been found!" 
            if(data[3]):
              plate_description = str(data[2]) + " " 
            if(data[4]): 
              plate_description += str(data[3]) + " " 
            if(data[5]): 
              plate_description += str(data[4]) + " "
            if(data[6]): 
              plate_description += str(data[5]) + " "
            if(data[8]): 
              plate_description += "LAST SEEN AT " + str(data[9]) + " "
            if(data[9]): 
              plate_description += "IN THE " + str(data[10]) + " AREA"
            print(plate_description) 
            return(title, plate_description) 
            
    async def on_ready(self): 
        print("Logged into: " + str(self.user)) 

    async def on_message(self, message):
        if message.author == self.user: return 
        elif len(message.content) < 7: 
            search_result = self.search((message.content))
            search = self.parse_data((search_result))
            if(search == None):
              embed = discord.Embed(title="Plate not found")
              await message.channel.send(embed=embed)
            elif(search != -1): 
                await message.channel.send(embed=discord.Embed(title=search[0], description=search[1]))
        elif len(message.content) > 6: 
            embed = discord.Embed(title="Sorry but, a number plate can't have more than 6 characters")
            await message.channel.send(embed=embed)

if __name__ == "__main__":
    clientz = BotClient()
    #clientz.download_database()
    my_secret = 'ODU3MTc1NjU0MDMwMTE0ODM2.YNLxCQ.TgVfOjmOqa1jM_DTpd9kbrCWVWA'
    clientz.run(my_secret)