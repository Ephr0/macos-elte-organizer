import xattr
import plistlib #binary property list
import os
import shutil
import configparser
import logging



#SETTINGS -> PRIVACY AND SECURITY -> FULL DISK ACCESS -> enable for TERMINAL and VISUAL STUDIO CODE
def append_list(dir_path):
    elte_list = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            values = plistlib.loads(xattr.getxattr(file_path, 'com.apple.metadata:kMDItemWhereFroms'))
            #print(value1)
            result = (link_returner(file_path, values))  
            if result is not None:
                elte_list.append(result)
        except:
            pass
            #print(f"This {file_name} does not work\n")
    return elte_list
def link_checker(value):
    return 'https://canvas.elte.hu' in value or 'https://ikelte.sharepoint.com/sites' in value or 'https://tms.inf.elte.hu' in value 

def link_returner(file_path, value):
    if ('https://tms.inf.elte.hu' in value[0]):
        return [file_path, value[0]]
    elif ('https://canvas.elte.hu' in value[1] or 'https://ikelte.sharepoint.com/sites' in value[1]):
        return [file_path, value[1]]
    return None
        

# Creates the Folders for the Subjects
def create_folder(desired_path, config, logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)
    misc = os.path.join(desired_path, 'Miscellaneous')
    if not os.path.exists(misc):
        os.mkdir(misc)
        logger.info(f"'{misc}' was created")
    for key in config:
        folder = os.path.join(desired_path, key)
        if not os.path.exists(folder):
            os.mkdir(folder)
            logger.info(f"'{folder}' was created")
            
            
def move_copy_error(file_path, destination, M_C, logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)
    action = "copying" if M_C.lower() == 'copy' else 'moving'
    #print(f'move function {logger}')
    try:
        if M_C.lower() == 'copy':
            shutil.copy(file_path, destination)
            logger.info(f"'{file_path}' was copied to '{destination}'")
        elif M_C.lower() == 'move':
            shutil.move(file_path, destination)
            logger.info(f"'{file_path}' was moved to '{destination}'")
            #print('moved -------')
        else:
            logger.error("ERROR: fix Move or Copy section in 'config.ini'")
    except:
        logger.error(f"Error occurred while {action} '{file_path}' to '{destination}'")
        #print('error but shuold be logged')

            
def move_files(desired_path, list, config, logger):
    #print(logger)
    file_links = config.items('LINKS')
    for file_path, link in list:
        matched = False
        for key, values in file_links:
            for value in [url.strip() for url in values.split("|") if url.strip()]:
                if value in link:
                    #print(f"Moving {links} to {desired_path} because it matched with {values}\n")
                    destination = os.path.join(desired_path, key)
                    matched = True
                    move_copy_error(file_path, destination, config["SETTINGS"]["Move or Copy"], logger)
        if not matched:
            destination = os.path.join(desired_path, 'Miscellaneous')
            move_copy_error(file_path, destination, config["SETTINGS"]["Move or Copy"], logger)
            


def organizer_main():
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = lambda option : option
    config.read("config.ini")
    dir_path = config["DIRECTORIES"]["Downloads"]
    desired_path = config["DIRECTORIES"]["Destination"]
 
    elte_list = append_list(dir_path)
    create_folder(desired_path, config["LINKS"])
    move_files(desired_path, elte_list, config, logger)

if __name__ == "__main__":
    logging.basicConfig(filename='organizer.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger('organizer.py')
    organizer_main()




# combined_list = teams_elte_list + canvas_elte_list

# for links in combined_list:
#     for key, value in courses.items():
#         if links[1].find(key) > -1:
#             try:
#                 shutil.move(links[0], desired_path + '/' + value)
#             except:
#                 os.remove(links[0])
#                 pass
#         else:
#             try:
#                 shutil.move(links[0], desired_path + '/Miscellaneous')
#             except:
#                 pass


        



# courses = {
#     "https://canvas.elte.hu/courses/38584" : "Computer Systems Le.",
#     "https://canvas.elte.hu/courses/36812" : "Basic Math",
#     "https://canvas.elte.hu/courses/36748" : "Programming",
#     "https://canvas.elte.hu/courses/40758" : "Functional Programming Le.",
#     "https://canvas.elte.hu/courses/40454" : "Imperative Programming",
#     "https://canvas.elte.hu/courses/37410" : "Computer Systems Pr.",
#     "https://canvas.elte.hu/courses/36848" : "Learning Methodology",
#     "https://canvas.elte.hu/courses/40326" : "Business Fundamentals Le.",
#     "https://canvas.elte.hu/courses/40012" : "Business Fundamentals Pr.",
#     'https://ikelte.sharepoint.com/sites/ComSys20232' : 'Computer Systems Le.',
#     'https://ikelte.sharepoint.com/sites/BasicMathematicsGroup4' : 'Basic Math',
#     'https://ikelte.sharepoint.com/sites/Programminglectureandpractice-2023-24I' : 'Programming',
#     'https://ikelte.sharepoint.com/sites/23241FPGr410.15-11.452.107' : 'Functional Programming Pr.',
#     'https://ikelte.sharepoint.com/sites/FUNCPROGLECT90/' : 'Functional Programming Le.',
#     'https://ikelte.sharepoint.com/sites/FUNcPROGCONSULTATIONS' : 'Functional Programming Pr.',
#     'https://ikelte.sharepoint.com/sites/Imperativeprogramming23241-Group4-Wednesday16-19' : 'Imperative Programming',
#     'https://ikelte.sharepoint.com/sites/CS-4-Fall-20232024' : 'Computer Systems Pr.',
#     'https://ikelte.sharepoint.com/sites/IP-18fTMKG-Bsc.4.LearningMethodology' : 'Learning Methodology',
# }
