import webview
import os
import configparser
from installer import install_main, get_install_progress, get_output

current_dir = os.path.dirname(os.path.realpath(__file__))
Assets = os.path.join(current_dir, 'Assets')


class API:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.directory = self.config.get('Settings', 'directory', fallback='')

    def select_directory(self):
        directory = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if directory:
            self.directory = directory[0]
            with open('Assets/Config.ini', 'w') as configfile:
                self.config.write(configfile)
        return self.directory

    def install(self):
        install_main(self.directory)

    def install_progress(self):
        return get_install_progress()

    def get_log(self):
        return get_output()


if __name__ == '__main__':
    api = API()

    webview.create_window(
        'GTAV中配MOD安装器丨Powered by Cyber蝈蝈总 和 鼠子Tomoriゞ ',
        'Assets/UI/index.html',
        js_api=api,
        width=900,
        height=650
    )
    webview.start()
