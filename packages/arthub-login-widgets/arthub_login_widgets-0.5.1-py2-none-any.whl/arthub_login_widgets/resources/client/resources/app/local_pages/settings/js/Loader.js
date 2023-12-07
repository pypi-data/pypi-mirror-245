(function(global)
{
    let head = document.getElementsByTagName('head')[0];
    async function loadScriptSync(src) 
    {
        return new Promise(function (resolve, reject) 
        {
            var s = document.createElement('script');
            s.src = src;
            s.type = "text/javascript";
            head.appendChild(s);
            s.onload = function() 
            {
                resolve();
            };
            s.onerror = function(error) 
            {
                reject(error);
            };
        });
    };

    async function loadAllScriptSync(baseUrl)
    {
        baseUrl = baseUrl ? baseUrl : '';
        await loadScriptSync(baseUrl + 'js/Settings.js');
        await loadScriptSync(baseUrl + 'js/Main.js');
        await loadScriptSync(baseUrl + 'js/Window.js');
        await loadScriptSync(baseUrl + 'js/Interface.js');

    };
    global.loadAllScriptSync = loadAllScriptSync;
}(this));