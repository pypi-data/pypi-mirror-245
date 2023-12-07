//tab page
var currentpageindex = 0
var pagebuttons = document.getElementById('page_button_container').children
var pages = document.getElementById('page_container').children

var changepagestate = function (pageindex) {
  if (currentpageindex == pageindex) return
  for (var i = 0; i < pagebuttons.length; i++) {
    pagebuttons[i].className = 'pagebutton'
    pages[i].style.display = 'none'
  }
  pagebuttons[pageindex].className = 'pagebuttonchecked'
  pages[pageindex].style.display = 'flex'
  currentpageindex = pageindex
}
changepagestate(0)

var onPageButtonClick = function (index) {
  changepagestate(index)
}

//radio button.
function eventDelegate(parentSelector, targetSelector, events, foo) {
  // 触发执行的函数
  function triFunction(e) {
    // 兼容性处理
    var event = e || window.event

    // 获取到目标阶段指向的元素
    var target = event.target || event.srcElement

    // 获取到代理事件的函数
    var currentTarget = event.currentTarget

    // 处理 matches 的兼容性
    if (!Element.prototype.matches) {
      Element.prototype.matches =
        Element.prototype.matchesSelector ||
        Element.prototype.mozMatchesSelector ||
        Element.prototype.msMatchesSelector ||
        Element.prototype.oMatchesSelector ||
        Element.prototype.webkitMatchesSelector ||
        function (s) {
          var matches = (this.document || this.ownerDocument).querySelectorAll(
              s
            ),
            i = matches.length
          while (--i >= 0 && matches.item(i) !== this) {}
          return i > -1
        }
    }

    // 遍历外层并且匹配
    while (target !== currentTarget) {
      // 判断是否匹配到我们所需要的元素上
      if (target.matches(targetSelector)) {
        var sTarget = target
        // 执行绑定的函数，注意 this
        foo.call(sTarget, Array.prototype.slice.call(arguments))
      }

      target = target.parentNode
    }
  }

  // 如果有多个事件的话需要全部一一绑定事件
  events.split('.').forEach(function (evt) {
    // 多个父层元素的话也需要一一绑定
    Array.prototype.slice
      .call(document.querySelectorAll(parentSelector))
      .forEach(function ($p) {
        $p.addEventListener(evt, triFunction)
      })
  })
}
var hasClass = (function () {
  var div = document.createElement('div')
  if ('classList' in div && typeof div.classList.contains === 'function') {
    return function (elem, className) {
      return elem.classList.contains(className)
    }
  } else {
    return function (elem, className) {
      var classes = elem.className.split(/\s+/)
      for (var i = 0; i < classes.length; i++) {
        if (classes[i] === className) {
          return true
        }
      }
      return false
    }
  }
})()

eventDelegate('.domainblock', 'input', 'click', function (e) {
  if (this.type == 'radio') {
    //console.log(e[0])
    e[0].stopImmediatePropagation()
    e[0].stopPropagation()
    if (this.getAttribute('aria-hidden') == 'true') {
      // this.parentNode.className = 'ah-radio__input';
      // this.setAttribute('aria-hidden','false')
    } else {
      var elements = document.getElementsByClassName('ah-radio__domain')
      for (var i = 0; i < elements.length; i++) {
        elements[i].parentNode.className = 'ah-radio__input'
        elements[i].setAttribute('aria-hidden', 'false')
      }

      this.parentNode.className = 'ah-radio__input is-checked'
      this.setAttribute('aria-hidden', 'true')
      const domainKey = String(this.getAttribute('tabkey'))
      _Settings._settings.currentNetworkConfigKey = domainKey
      console.log(`On url domain checked, key: ${domainKey}`)
    }
  }
})

// eventDelegate('.dbclickblock', 'input', 'click', function (e) {
//   if (this.type === 'radio') {
//     e[0].stopImmediatePropagation()
//     e[0].stopPropagation()
//     if (this.getAttribute('aria-hidden') == 'true') {
//       // this.parentNode.className = 'ah-radio__input';
//       // this.setAttribute('aria-hidden','false')
//     } else {
//       const elements = document.getElementsByClassName('ah-radio__dbclick')
//       for (var i = 0; i < elements.length; i++) {
//         elements[i].parentNode.className = 'ah-radio__input'
//         elements[i].setAttribute('aria-hidden', 'false')
//       }

//       this.parentNode.className = 'ah-radio__input is-checked'
//       this.setAttribute('aria-hidden', 'true')
//       var Type = Number(this.getAttribute('tabindex'))
//       if (Type == 0) {
//         _Settings._settings.clickToRunTool = false
//       } else if (Type == 1) {
//         _Settings._settings.clickToRunTool = true
//       }
//     }
//   }
// })

function setDomain(key) {
  const elements = document.getElementsByClassName('ah-radio__domain')
  for (let i = 0; i < elements.length; i++) {
    const domainKey = String(elements[i].getAttribute('tabkey'))
    if (key === domainKey) {
      elements[i].parentNode.className = 'ah-radio__input is-checked'
      elements[i].setAttribute('aria-hidden', 'true')
    } else {
      elements[i].parentNode.className = 'ah-radio__input'
      elements[i].setAttribute('aria-hidden', 'false')
    }
  }
}
window.setDomain = setDomain

// function setDbclick(turnon) {
//   const elements = document.getElementsByClassName('ah-radio__dbclick')
//   const _index_ = turnon ? 1 : 0
//   for (let i = 0; i < elements.length; i++) {
//     if (i === _index_) {
//       elements[i].parentNode.className = 'ah-radio__input is-checked'
//       elements[i].setAttribute('aria-hidden', 'true')
//     } else {
//       elements[i].parentNode.className = 'ah-radio__input'
//       elements[i].setAttribute('aria-hidden', 'false')
//     }
//   }
// }

const onSaveButtonClick = function () {
  _Settings.SaveSettings()
  window.ArtHubDesktop.hideSettingsWindow()
}
const onCancelButtonClick = function () {
  window.ArtHubDesktop.hideSettingsWindow()
}

const triggerChoiceButton = function (id, ischoice) {
  var button = document.getElementById(id)
  button.className = ischoice ? 'choicebuttonchecked' : 'choicebutton'
}

const onMinimizedToTray = function () {
  if (_Settings._settings.minimizedToTray) {
    triggerChoiceButton('minimized_to_tray_button', false)
    _Settings._settings.minimizedToTray = false
  } else {
    triggerChoiceButton('minimized_to_tray_button', true)
    _Settings._settings.minimizedToTray = true
  }
}

const onOpenSystemNotify = function () {
  if (_Settings._settings.openSystemNotify) {
    triggerChoiceButton('open_system_notify_button', false)
    _Settings._settings.openSystemNotify = false
  } else {
    triggerChoiceButton('open_system_notify_button', true)
    _Settings._settings.openSystemNotify = true
  }
}

const onDebugInConsole = function () {
  if (_Settings._settings.debugInConsole) {
    triggerChoiceButton('debug_in_console_button', false)
    _Settings._settings.debugInConsole = false
  } else {
    triggerChoiceButton('debug_in_console_button', true)
    _Settings._settings.debugInConsole = true
  }
}

const onOpenDownloadPathButtonClick = function () {
  window.ArtHubDesktop.openLocalFile(_Settings._settings.defaultDownloadPath)
}

const onChangeDownloadPathButtonClick = function () {
  window.ArtHubDesktop.openFileDialog(
    _Settings._settings.defaultDownloadPath,
    'Please select cache directory',
    2,
    function (pathlist) {
      if (pathlist.length >= 0) {
        path = pathlist[0]['path']
        i = path.indexOf(':\\')
        if (i !== -1) {
          path = path.substring(0, i) + ':\\_thm'
        }
        _Settings._settings.defaultDownloadPath = path
        updateViewFromSettings()
      }
    },
    function () {}
  )
}

const onInstallDependenciesButtonClick = function () {
  window.ArtHubDesktop.installDependencies()
}

const createHomeDomainRadios = function (domainInfos) {
  let first_index = true
  const domainblock = document.getElementById('domainblock')
  while (domainblock.hasChildNodes()) {
    domainblock.removeChild(domainblock.firstChild)
  }
  for (const key in domainInfos) {
    const domain = domainInfos[key]
    const childDom = document.createElement('label')
    childDom.setAttribute('role', 'radio')
    childDom.setAttribute('tabkey', `${key}`)
    childDom.className = first_index ? 'ah-radio is-checked' : 'ah-radio'

    childDom.innerHTML = `
        <span class=${
          first_index ? 'ah-radio__input is-checked' : 'ah-radio__input'
        }><span class="ah-radio__inner"></span>
            <input
              type="radio"
              aria-hidden=${first_index ? 'true' : 'false'}
              tabkey="${key}"
              class="ah-radio__domain"
              value="1"
            />
        </span>
        <span class="ah-radio__label">${domain}</span>`
    domainblock.appendChild(childDom)
    first_index = false
  }
}
window.createHomeDomainRadios = createHomeDomainRadios

const updateViewFromSettings = function () {
  triggerChoiceButton(
    'minimized_to_tray_button',
    _Settings._settings.minimizedToTray
  )
  // triggerChoiceButton(
  //   'open_system_notify_button',
  //   _Settings._settings.openSystemNotify
  // )
  triggerChoiceButton(
    'debug_in_console_button',
    _Settings._settings.debugInConsole
  )

  document.getElementById('update_service_path_input').value =
    _Settings._settings.onlineConfigUrl

  document.getElementById('download_path').value =
    _Settings._settings.defaultDownloadPath

  setDomain(_Settings._settings.currentNetworkConfigKey)
  // setDbclick(_Settings._settings.clickToRunTool)
}

window.updateViewFromSettings = updateViewFromSettings
