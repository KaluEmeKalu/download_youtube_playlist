import sys, os
import urllib2
from bs4 import BeautifulSoup as B



def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


class ExecuteDownload():
    """
    Takes a DownloadEngine object as a required parameter.
    """

    def __init__(self, download_engine):
        self.playlist_name, self.start_from, self.html_source = download_engine.prepare_download()

    def start_download(self):

        directory = self.playlist_name

        if not os.path.exists(directory):
            os.makedirs(directory)

        error_file = open(directory + '/' + self.playlist_name + "_errors.txt", 'a')
        success_file = open(directory + '/' + self.playlist_name + "_success.txt", 'a')
        total_report = open(directory + '/' + self.playlist_name + "_total_report.txt", 'a')

        soup = B(self.html_source, 'html.parser')

        if self.start_from:
            self.start_from = int(self.start_from) - 1
            trs = soup.tbody.find_all('tr')[self.start_from:]
        else:
            trs = soup.tbody.find_all('tr')

        for tr in trs:
            url = tr.a['href']
            text = tr.text.strip() + '.mp4'
            index = tr.th.text
            # text = text[:1] + ' - ' + text[1:]
            temp_filepath = self.playlist_name + '/' + text

            #check to see if file already exists
            if not os.path.exists(temp_filepath):

                try:
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                    print("\tAttempting to open " + text + '\n')
                    response = opener.open(url)
                    
                    file = open(temp_filepath, 'w')
                    file.write(response.read())
                    file.close()
                    message = "{} - Success {} \n".format(index, text)
                    success_file.write(message)
                    total_report.write(message)
                    print(message)
                except:
                    message = "{} - FAILED!!!!!!!!!!!!!!!!! {} \n".format(
                        index, text)
                    total_report.write(message)
                    error_file.write(message)
                    print(message)
            else:
                print("{} ALREADY EXISTS\n".format(temp_filepath) * 5)

        error_file.close()
        success_file.close()
        total_report.close()

class DownloadEngine():
    """
    Can take sys.argv as optional parameter.
    This expects sys.argv[1] to be the html_source_filepath
    sys.argv[2] to be the playlist_name
    and sys.argv[3] to be the start_from
    playlist_name and start_from are optional
    """
    def __init__(self, sys_argvs=None):
        if sys_argvs is not None:
            self.sys_argvs = sys_argvs

    def prepare_download(self):
        """
        Returns a  playlist_name, start_from (or none if none proivided) and an html_source
        """
        if not self.sys_argvs:
            self.sys_argvs = sys.argv

        #MUST EDIT WITH EXCEPTIONNS TO HANDLE IF ARGVS NOT PROVIDED
        html_source_filepath = self.sys_argvs[1]
        playlist_name = self.sys_argvs[2]
        try:
            start_from = self.sys_argvs[3]
        except:
            start_from = None

        if not playlist_name:
            # set playlist_name to filepath after
            # getting rid of folder names if present
            index = html_source_filepath.rfind('/')
            if index != -1:
                html_source_filepath = html_source_filepath[index + 1:]
            playlist_name = html_source_filepath

        file = open(html_source_filepath, 'r',)
        html_source = file.read()
        file.close()

        return playlist_name, start_from, html_source


engine = DownloadEngine(sys.argv)
download = ExecuteDownload(engine)
download.start_download()
