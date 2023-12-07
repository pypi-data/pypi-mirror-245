const textLanguage = {
  us: {
    preference_tab_button: 'Preference',
    network_tab_button: 'Network',
    general_prompt_text: 'General',
    download_path_prompt_text: 'Cache Directory',
    minimize_to_tray_text: 'Minimize to tray',
    debug_in_console_text: 'Debug tool in console',
    change_download_path_button: 'Change',
    install_dependencies_button: 'Install required dependencies',
    open_download_path_button: 'Browse',
    select_entry_prompt_text: 'Select the entry domain for launch',
    proxy_host_prompt_text: 'Proxy Host',
    ok_button: 'OK',
    cancel_button: 'Cancel',
  },
  cn: {
    preference_tab_button: '偏好设置',
    network_tab_button: '网络设置',
    general_prompt_text: '通用',
    download_path_prompt_text: '缓存目录',
    minimize_to_tray_text: '点击关闭时最小化到系统托盘',
    debug_in_console_text: '控制台中的调试工具',
    change_download_path_button: '更改目录',
    install_dependencies_button: '安装必须依赖',
    open_download_path_button: '浏览目录',
    select_entry_prompt_text: '选择启动时的入口域名',
    proxy_host_prompt_text: '代理服务器地址',
    ok_button: '确定',
    cancel_button: '取消',
  },
}
function getText(key) {
  let lang = 'cn'
  if (window.ArtHubDesktop && window.ArtHubDesktop.language) {
    lang = window.ArtHubDesktop.language
  }
  return textLanguage[lang][key]
}
function translationElement(id) {
  const element = document.getElementById(id)
  if (element) {
    element.innerText = getText(id)
  }
}
function formatTranslation() {
  translationElement('preference_tab_button')
  translationElement('network_tab_button')
  translationElement('general_prompt_text')
  translationElement('download_path_prompt_text')
  translationElement('minimize_to_tray_text')
  translationElement('debug_in_console_text')
  translationElement('change_download_path_button')
  translationElement('install_dependencies_button')
  translationElement('open_download_path_button')
  translationElement('select_entry_prompt_text')
  translationElement('proxy_host_prompt_text')
  translationElement('ok_button')
  translationElement('cancel_button')
}
formatTranslation()

window.ArtHubDesktop.getNetworkConfigs(networkConfigs => {
  _Settings._networkConfigs = networkConfigs
  createHomeDomainRadios(_Settings._networkConfigs)
  window.ArtHubDesktop.getLocalSettings(settingsObj => {
    if (settingsObj !== undefined) {
      _Settings._settings = settingsObj
      window.updateViewFromSettings()
    }
  })
})
