mdui.mutation();

function selectDirectory() {
    window.pywebview.api.select_directory().then(function (directory) {
        document.getElementById('directory').value = directory;
    });
}

function install() {
  window.pywebview.api.install();
}

function uninstall() {
  window.pywebview.api.uninstall();
}

function openTool(toolFunction) {
    toolFunction().then(function (result) {
        // alert(result);
    }).catch(function (error) {
        alert('发生错误: ' + error,);
    });
}

// 用于获取进度的函数，返回一个0-100之间的整数
function getInstallProgress() {
    return window.pywebview.api.install_progress();
}
// 用于获取最新执行日志的函数，返回一个字符串
function getLog() {
    return window.pywebview.api.get_log();
}

// 用于获取模组包含的RPF list，返回一个字符串数组
function updateModules(selectedModules) {
    window.pywebview.api.update_modules(selectedModules);
}
