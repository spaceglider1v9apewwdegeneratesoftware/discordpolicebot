from requests import get as fetch #importing from requests get function to aquire data from database, fetch is appreviation for get
import discord #importing discord API
import csv #importing csv library to interpret csv files

class BotClient(discord.Client): #creating class to give the argument to the bot client (discord.Client)
    def download_database(self): #function start for downloading database
        try:
            print("DOWNLOADING DATABASE") #output for user to see when its downloading
            new_csv = fetch("https://www.police.govt.nz/stolenwanted/vehicles/csv/download?all=true&gzip=false&full=true", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'})
        except: #for above: fetches the police govt website for the stolen cars csv, user agent is mozilla so that the server will accept the request, this includes the Windows NT so that it thinks its an actual browser request
            print("Connection Error!") #if fetching the csv fails then print out error to user and exit (for connection error)
            exit()
        new_csv = str(new_csv.text) #i stringify the text, converting the request object into a string object
        
        if(new_csv): #if string object exists then output download success
          print("DOWNLOAD SUCCESS")

        with open('stolen.csv', 'w', encoding='utf-8') as file_descriptor: #open the csv file and encode into utf-8 to preserve all characters, set this filedescriptor varname
            file_descriptor.write(new_csv) #with the new file descriptor we just encoded into utf-8 we write it to the new csv file
            file_descriptor.close() #close after writing

    def fix_null_chars(self, string)->str: #fix_null_chars function created here to preserve and fix the characters for error prevention
        for line in string: 
            yield line.replace('\0', ' ') #replaces the whitespace with a 0 so that it doesnt give error for NULL character, yield used instead of return because it can be used inside a function

    def search(self, plate)->list: #plate is the search argument for the functions search, searches the plate and returns a list of plates
        csv_file = csv.reader(self.fix_null_chars(open('stolen.csv', "r", encoding='utf-8')), delimiter=",") #create csv reader on the csv file, fix characters with our function we made, open the csv file to and read it, use delimiter comma to specify the boundries for the data when the sequence is read
        found = 0 #create var called found to determine whether a plate has been found or not
        for row in csv_file: #iterate over csv file
            if(row[0] == plate.upper()): #comparing if row 0 [A in CSV] is uppercase and return the row
                return (row) #return row
                found = 1 #when found set found var to 1 [found]
            elif(row[0] == plate.lower()): #if row is lowercase we find it and return the row
                return (row)
                found = 1
        if(found == 0): #if we havent found anything
            return -1 #return -1 [error]
            
    def parse_data(self, data)->str: #parse data function to parse the data [plates] found, convert to string
        if (data != -1): #this just means if there is no error aka if there is a plate found
            plate_description = "" #description is 0 because there is no description yet, we havent found it - we find it below, then we add
            #checking if plate is actually here
            if(data[0]): #in array 0 index is the numberplate so if there is something there then we found a car
              title = "Plate of a stolen car has been found!" #output to user that a car has been found
            if(data[4]): #data array row 5 [colour]
              plate_description = str(data[4]) + " " #equal the string to the data values found
            if(data[5]): #data array row 6 [car company]
              plate_description += str(data[5]) + " " #then we ADD onto it
            if(data[6]): #data array row 7 [car make]
              plate_description += str(data[6]) + " "
            if(data[7]): #data array row 8 [car type]
              plate_description += str(data[7]) + " "
            if(data[9]): #data array row 10 [date reported stolen]
              plate_description += "LAST SEEN AT " + str(data[9]) + " "
            if(data[10]): #data array 11 [last seen location]
              plate_description += "IN THE " + str(data[10]) + " AREA"
            print(plate_description) #we stringify all data and print it out
            return(title, plate_description) #then we return the values 
            
    async def on_ready(self): #async def is how discord library is supposed to structured, standard of definition for this API
        print("Logged into: " + str(self.user)) #output the discord bot that it connected to

    async def on_message(self, message): #message argument, API convention structure for argument paramater
        if message.author == self.user: return #this is to prevent a loop of bot constanting outputting the plate number
        elif len(message.content) < 7: #number plates length less than 7 characters, wont search if its over 7 string (not a plate)
            search_result = self.search((message.content)) #search the content if under 7 characters
            search = self.parse_data((search_result)) #parse the data with the search as a search result, find title and description
            if(search == None): #if search found nothing
              embed = discord.Embed(title="Plate not found") #embed the discord message through embed API to make it in the block form it is
              await message.channel.send(embed=embed) #await discord API function to output text, embeds it automatically in argument
            elif(search != -1): #if search finds something
                await message.channel.send(embed=discord.Embed(title=search[0], description=search[1])) #send a discord embed message of title and description
        elif len(message.content) > 6: #if input has more than 6 characters (non-existant plate)
            embed = discord.Embed(title="Sorry but, a number plate can't have more than 6 characters")
            await message.channel.send(embed=embed)

if __name__ == "__main__": #initialize script
    clientz = BotClient() #use clientz because client can be a discord API keyword
    #clientz.download_database() #client downloads fresh copy of the csv file (can be commented out if not needed)
    my_secret = 'mej-Vkd_kggRHuZqkc76bm2GwpQMaw6y' #discord bot token
    clientz.run(my_secret) #run discord bot with token