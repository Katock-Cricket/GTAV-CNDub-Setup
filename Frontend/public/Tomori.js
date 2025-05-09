mdui.mutation();

function selectDirectory() {
    window.pywebview.api.select_directory().then(function (directory) {
        document.getElementById('directory').value = directory;
    });
}

function install() {
  window.pywebview.api.install();
}

function openTool(toolFunction) {
    toolFunction().then(function (result) {
        // alert(result);
    }).catch(function (error) {
        alert('发生错误: ' + error,);
    });
}

function openGames() {
    openTool(window.pywebview.api.OpenGames);
}

// 用于获取进度的函数，返回一个0-100之间的整数
function getInstallProgress() {
    return window.pywebview.api.install_progress();
}
// 用于获取最新执行日志的函数，返回一个字符串
function getLog() {
    return window.pywebview.api.get_log();
}
