import webview
import os
import configparser
from installer import install_main, is_installed

current_dir = os.path.dirname(os.path.realpath(__file__))
Assets = os.path.join(current_dir, 'Assets')

class API:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('Assets/Config.ini')
        self.directory = self.config.get('Settings', 'directory', fallback='')

    def select_directory(self):
        directory = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if directory:
            self.directory = directory[0]
            self.config.set('Settings', 'directory', self.directory)
            with open('Assets/Config.ini', 'w') as configfile:
                self.config.write(configfile)
        return self.directory

    def install(self):
        install_main(self.directory)

    def uninstall(self):
        install_main(self.directory, uninstall=True)

    def isInstalled(self):
        return is_installed(self.directory)

    def OpenGames(self):
        program_path = os.path.join(self.directory, "GTA5.exe")
        if not os.path.exists(program_path):
            return "游戏目录无效，请检查目录是否正确。"
        os.startfile(program_path)

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