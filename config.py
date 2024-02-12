import sys
import configparser
import shutil

def case_sensitive_optionxform(option):
    return option

def configurator(download, destination, move_or_copy):
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = case_sensitive_optionxform
    config.read("config.ini")
    
    if not config.has_section("DIRECTORIES"):
        config.add_section("DIRECTORIES")
    if not config.has_section("SETTINGS"):
        config.add_section("SETTINGS")

    if destination != "skip":
        config["DIRECTORIES"]["Destination"] = destination
    if download != "skip":    
        config["DIRECTORIES"]["Downloads"] = download
    if move_or_copy != "skip":
        config["SETTINGS"]["Move or Copy"] = move_or_copy
    
    while True:
        line = input().split("|")
        if line == ["done"]:
            break
        if len(line) != 2:
            print("ERROR: input should have subject and link\nFunctional Programming | https://canvas.elte.hu/courses/40758 ")
            break
        subject, link = line[0].strip(), line[1].strip()
        if "canvas.elte.hu" or "ikelte.sharepoint.com" or "tms.inf.elte.hu" in link:
            section = "LINKS"
        else:
            section = "MISCELLANEOUS"
        
        if not config.has_section(section):
            config.add_section(section)
            
        current_value = config.get(section, subject, fallback="")
        
        updated_value = current_value + link + " | "
        
        config.set(section, subject, updated_value)
            
    with open('current_config.ini', 'w') as configfile:
        config.write(configfile)

def config_main():
    print("Give the folder directory where you get your downloads from (or skip if you already have the correct directory)")
    print("Go to Chrome -> 3 dots on top right -> Downloads -> Press on the 3 dots on the top right of the webpage you opened -> Open Downloads folder -> Get directory:")
    download = input()
    print("Give a destination folder for storing your subject files (Open terminal at the folder you want for storing your files and write pwd, copy paste the directory onto here) or skip:")
    destination = input()
    print("Do you want the program to move the files from the given Download directory to the Destination folder and delete the files from the given original Download Directory? (yes/no)")
    yn = input()

    move_or_copy = "move" #shutil.move()
    if yn == "no":
        move_or_copy = "copy" #shutil.copy()
    elif yn == "skip":
        move_or_copy = "skip"
    
    print("Give subject and link separated by '|' followed by a new line. When finished write 'done'. Example:\nFunctional Programming | https://canvas.elte.hu/courses/40758\nImperative Programming | https://canvas.elte.hu/courses/40454\ndone")
    configurator(download, destination, move_or_copy)
        

if __name__ == "__main__":
    config_main()
    
