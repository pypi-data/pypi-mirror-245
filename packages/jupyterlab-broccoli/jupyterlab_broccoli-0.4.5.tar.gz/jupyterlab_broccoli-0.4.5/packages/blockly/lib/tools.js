/**
*/
export var JlbTools;
(function (JlbTools) {
    //
    function copyElement(e) {
        const sel = window.getSelection();
        if (sel == null)
            return;
        // Save the current selection.
        const savedRanges = [];
        for (let i = 0; i < sel.rangeCount; ++i) {
            savedRanges[i] = sel.getRangeAt(i).cloneRange();
        }
        //
        const range = document.createRange();
        range.selectNodeContents(e);
        sel.removeAllRanges();
        sel.addRange(range);
        document.execCommand('copy');
        // Restore the saved selection.
        sel.removeAllRanges();
        savedRanges.forEach(r => sel.addRange(r));
    }
    JlbTools.copyElement = copyElement;
    // for Tracker
    function isEnabled(shell, tracker) {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    JlbTools.isEnabled = isEnabled;
    // for Tracker
    function getCurrentWidget(shell, tracker, args) {
        const widget = tracker.currentWidget;
        if (args !== null) {
            const activate = args['activate'] !== false;
            if (activate && widget)
                shell.activateById(widget.id);
        }
        return tracker.currentWidget;
    }
    JlbTools.getCurrentWidget = getCurrentWidget;
    // for Debug
    function disp_obj(obj) {
        const getMethods = (obj) => {
            const getOwnMethods = (obj) => Object.entries(Object.getOwnPropertyDescriptors(obj))
                .filter(([name, { value }]) => typeof value === 'function' && name !== 'constructor')
                .map(([name]) => name);
            const _getMethods = (o, methods) => o === Object.prototype ? methods : _getMethods(Object.getPrototypeOf(o), methods.concat(getOwnMethods(o)));
            return _getMethods(obj, []);
        };
        console.log("+++++++++++++++++++++++++++++++++++");
        for (const key in obj) {
            console.log(String(key) + " -> " + obj[key]);
        }
        console.log("===================================");
        console.log(getMethods(obj));
        console.log("-----------------------------------");
    }
    JlbTools.disp_obj = disp_obj;
})(JlbTools || (JlbTools = {}));
//# sourceMappingURL=tools.js.map