let Settings = function () {
  this._settings = {
    defaultDownloadPath: '',
    clickToRunTool: true,
    minimizedToTray: false,
    openSystemNotify: true,
    debugInConsole: false,
    onlineConfigUrl: '',
    currentNetworkConfigKey: '',
  }
  this._networkConfigs = {}
}

Settings.prototype.SaveSettings = function () {
  this._settings.onlineConfigUrl = document.getElementById(
    'update_service_path_input'
  ).value
  window.ArtHubDesktop.setLocalSettings(this._settings)
}
