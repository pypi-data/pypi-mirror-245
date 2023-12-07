/* eslint-disable no-sync */
/* eslint-disable @typescript-eslint/explicit-member-accessibility */
const { ipcRenderer, remote } = require('electron')
const functionList = [
  // version
  'getVersion',
  'upgradeToNewVersion',
  'postponeUpgradePromptInSeconds',
  'resetVerisionWindowHeight',
  // local
  'openFileDialog',
  'checkAdminPermission',
  'fixAdminPermission',
  'openGPEdit',
  'listDrive',
  // transfer
  'onTransferCenterViewInitial',
  'pauseTransferTasksByType',
  'restartTransferTasksByType',
  'cancelTransferTasksByType',
  'cancelCompletedTransferTasks',
  'pauseTransferTaskById',
  'restartTransferTaskById',
  'cancelTransferTaskById',
  'openTransferTaskById',
  'findTransferTaskById',
  'showLocalFileInFolder',
  'openLocalFile',
  // ui
  'postEvent',
  'closeCurrentWindow',
  'cancelToolRunning',
  'showToolErrorLog',
  'openMainWindow',
  'setWindowStickyOnTop',
  'isWindowStickyOnTop',
  'getErrorWindowInfo',
  'getProgressWindowInfo',
  'JumptoManualConsultation',
  // settings
  'setLanguage',
  'getLocalSettings',
  'setLocalSettings',
  'getNetworkConfigs',
  'hideSettingsWindow',
  // messagebox
  'messageboxSelect',
  'networkAlert',
  // log
  'saveNetworkError',
  // cache
  'queryFileInCache',
  'clearCache',
  // monitor
  'findFileLocation',
  // plugin test
  'getToken',
  // directory sync related
  'isNodeRegisteredForSync',
  'triggerNodeSync',
  // tool
  'runTool',
  'installDependencies',
  // login
  'loginStatusChanged',
  // network
  'isServiceReachable',
  // main window
  'goBack',
  'goForward',
  'checkGoBackForwardState'
]

const rendererCallbackEventName = 'callback-to-renderer'
const rendererCallEventName = 'call-from-renderer'
let version = undefined
let macAddress = undefined
let devMode = undefined

function isDevMode() {
  if (devMode === undefined) {
    devMode = ipcRenderer.sendSync('is-dev-mode')
  }
  return devMode
}


function getVersion() {
  if (version === undefined) {
    version = ipcRenderer.sendSync('get-version')
  }
  return version
}

function getMacAddress() {
  if (macAddress === undefined) {
    macAddress = ipcRenderer.sendSync('get-mac-address')
  }
  return macAddress
}
class RendererHandler {
  // private curCallbackId = 0;
  // private callbackMap = new Map<number, Array<() => any>>();
  constructor() {
    window.ArtHubDesktop = {}
    this.curCallbackId = 0
    this.callbackMap = new Map()

    // register event to main process
    functionList.forEach(functionName => {
      window.ArtHubDesktop[functionName] = (...args) => {
        const inputArgList = []
        const callbackList = []
        args.forEach(arg => {
          const argType = typeof arg
          if (argType === 'undefined') {
            return
          }
          if (argType === 'function') {
            callbackList.push(arg)
          } else {
            inputArgList.push(arg)
          }
        })
        let callbackId = -1
        if (callbackList.length > 0) {
          callbackId = this.registerCallbacks(callbackList)
        }
        this.callMainProcess({
          funcName: functionName,
          args: inputArgList,
          callbackId: callbackId,
        })
        return callbackId
      }
    })

    // register event from renderer process
    window.ArtHubDesktop['registerEventCallback'] = (eventName, callback) => {
      ipcRenderer.on(eventName, (event, args) => {
        callback.apply(null, args)
      })
    }

    window.ArtHubDesktop['macAddress'] = getMacAddress()
    window.ArtHubDesktop['version'] = getVersion()
    window.ArtHubDesktop['environment'] = 'electron'
    window.ArtHubDesktop['isDevMode'] = isDevMode()

    // register callback event
    ipcRenderer.on(rendererCallbackEventName, (e, arg) => {
      this.trigerCallBack(arg.callbackId, arg.callbackType, arg.args)
    })
  }

  registerCallbacks(functionList) {
    if (functionList.length <= 0) {
      return -1
    }
    if (this.curCallbackId < Number.MAX_VALUE) {
      this.curCallbackId++
    } else {
      this.curCallbackId = 0
    }
    this.callbackMap.set(this.curCallbackId, functionList)
    return this.curCallbackId
  }

  trigerCallBack(callbackId, callbackType, args) {
    const callbacks = this.callbackMap.get(callbackId)
    if (callbacks) {
      if (callbacks.length <= callbackType) {
        return false
      }
      callbacks[callbackType].apply(null, args)
      if (callbackType === 0 || callbackType == 1) {
        this.callbackMap.delete(callbackId)
      }
      return true
    } else {
      return false
    }
  }

  callMainProcess(arg) {
    ipcRenderer.send(rendererCallEventName, arg)
  }
}

new RendererHandler()
