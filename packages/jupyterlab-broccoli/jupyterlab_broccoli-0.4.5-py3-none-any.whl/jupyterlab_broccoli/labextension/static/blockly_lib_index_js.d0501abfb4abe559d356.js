(self["webpackChunkjupyterlab_broccoli_extension"] = self["webpackChunkjupyterlab_broccoli_extension"] || []).push([["blockly_lib_index_js"],{

/***/ "../blockly/lib/codewidget.js":
/*!************************************!*\
  !*** ../blockly/lib/codewidget.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SourceCodeWidget: () => (/* binding */ SourceCodeWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var highlight_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! highlight.js */ "../../node_modules/highlight.js/es/index.js");
/* harmony import */ var highlight_js_styles_github_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! highlight.js/styles/github.css */ "../../node_modules/highlight.js/styles/github.css");
/**
  SourceCodeWidhet Class
*/




//import 'highlight.js/styles/googlecode.css';
//declare function require(string): any;
/**
 */
class SourceCodeWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    //
    constructor(classname, title) {
        super();
        //
        this.addClass(classname);
        this.title.label = title;
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.codeIcon;
        this.default_style();
        this._source = '';
        this._language = '';
        highlight_js__WEBPACK_IMPORTED_MODULE_2__["default"].highlightAll();
    }
    //
    default_style() {
        this.node.style.height = '100%';
        this.node.style.overflowX = 'scroll';
        this.node.style.overflowY = 'scroll';
        //this.node.style.overflowWrap = 'normal';
        //this.node.style.wordBreak = 'break-all';
        this.node.style.paddingTop = '40px';
        this.node.style.paddingRight = '40px';
        this.node.style.paddingLeft = '60px';
        this.node.style.paddingBottom = '100px';
        this.node.style.border = '0px';
        this.node.style.whiteSpace = 'pre';
        this.node.style.fontSize = 'var(--jp-code-font-size)';
        this.node.style.fontFamily = 'var(--jp-code-font-family)';
        this.node.style.fontWeight = 'bold';
        //console.log(this.node.style.cssText);
    }
    //
    setLanguage(lang) {
        if (lang === null || lang === undefined)
            lang = 'javascript';
        this._language = lang;
    }
    //
    getLanguage() {
        return this._language;
    }
    //
    setSource(code) {
        this._source = code;
        this.node.innerHTML = highlight_js__WEBPACK_IMPORTED_MODULE_2__["default"].highlight(code, { language: this._language }).value;
    }
    //
    getSource() {
        return this._source;
    }
}


/***/ }),

/***/ "../blockly/lib/dialog.js":
/*!********************************!*\
  !*** ../blockly/lib/dialog.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   closeDialog: () => (/* binding */ closeDialog)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

function _closeDialog(widget) {
    const path = widget.context.path;
    const n = path.lastIndexOf('/');
    const fileName = path.substring(n + 1);
    const trans = widget.trans;
    const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog({
        title: trans.__('Save your work'),
        body: trans.__('Save changes in "%1" before closing?', fileName),
        buttons: [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: trans.__('Cancel') }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: trans.__('Discard') }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Save') })
        ]
    });
    return dialog;
}
async function closeDialog(widget) {
    const dialog = _closeDialog(widget);
    const result = await dialog.launch();
    dialog.dispose();
    if (result.button.label === widget.trans.__('Cancel') || result.button.label === 'Cancel') {
        return Promise.resolve(false);
    }
    // on Save, save the file
    if (result.button.label === widget.trans.__('Save') || result.button.label === 'Save') {
        await widget.save(true);
    }
    return Promise.resolve(true);
}


/***/ }),

/***/ "../blockly/lib/factory.js":
/*!*********************************!*\
  !*** ../blockly/lib/factory.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyEditorFactory: () => (/* binding */ BlocklyEditorFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "../blockly/lib/widget.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./registry */ "../blockly/lib/registry.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./manager */ "../blockly/lib/manager.js");





/**
 * A widget factory to create new instances of BlocklyEditor.
 */
class BlocklyEditorFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.ABCWidgetFactory {
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(app, tracker, options) {
        super(options);
        this._app = app;
        this._tracker = tracker;
        this._registry = new _registry__WEBPACK_IMPORTED_MODULE_2__.BlocklyRegistry();
        this._rendermime = options.rendermime;
        this._mimetypeService = options.mimetypeService;
        this._trans = (options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator).load('jupyterlab');
        this._cell = null;
    }
    //
    get trans() {
        return this._trans;
    }
    get registry() {
        return this._registry;
    }
    get manager() {
        return this._manager;
    }
    get cell() {
        return this._cell;
    }
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    createNewWidget(context) {
        // Set a map to the model. The widgets manager expects a Notebook model
        // but the only notebook property it uses is the metadata.
        context.model['metadata'] = new Map();
        const manager = new _manager__WEBPACK_IMPORTED_MODULE_3__.BlocklyManager(this._app, this._registry, context.sessionContext, this._mimetypeService);
        this._manager = manager;
        const content = new _widget__WEBPACK_IMPORTED_MODULE_4__.BlocklyPanel(this._tracker, context, manager, this._rendermime);
        this._cell = content.activeLayout.cell;
        const editor = new _widget__WEBPACK_IMPORTED_MODULE_4__.BlocklyEditor(this._app, { context, content, manager });
        content.activeEditor = editor;
        return editor;
    }
}


/***/ }),

/***/ "../blockly/lib/index.js":
/*!*******************************!*\
  !*** ../blockly/lib/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyEditor: () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_7__.BlocklyEditor),
/* harmony export */   BlocklyEditorFactory: () => (/* reexport safe */ _factory__WEBPACK_IMPORTED_MODULE_1__.BlocklyEditorFactory),
/* harmony export */   BlocklyLayout: () => (/* reexport safe */ _layout__WEBPACK_IMPORTED_MODULE_2__.BlocklyLayout),
/* harmony export */   BlocklyManager: () => (/* reexport safe */ _manager__WEBPACK_IMPORTED_MODULE_3__.BlocklyManager),
/* harmony export */   BlocklyPanel: () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_7__.BlocklyPanel),
/* harmony export */   BlocklyRegistry: () => (/* reexport safe */ _registry__WEBPACK_IMPORTED_MODULE_4__.BlocklyRegistry),
/* harmony export */   IBlocklyRegistry: () => (/* reexport safe */ _token__WEBPACK_IMPORTED_MODULE_5__.IBlocklyRegistry),
/* harmony export */   JlbTools: () => (/* reexport safe */ _tools__WEBPACK_IMPORTED_MODULE_9__.JlbTools),
/* harmony export */   SourceCodeWidget: () => (/* reexport safe */ _codewidget__WEBPACK_IMPORTED_MODULE_8__.SourceCodeWidget),
/* harmony export */   THEME: () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_6__.THEME),
/* harmony export */   TOOLBOX: () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_6__.TOOLBOX),
/* harmony export */   closeDialog: () => (/* reexport safe */ _dialog__WEBPACK_IMPORTED_MODULE_0__.closeDialog)
/* harmony export */ });
/* harmony import */ var _dialog__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./dialog */ "../blockly/lib/dialog.js");
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./factory */ "../blockly/lib/factory.js");
/* harmony import */ var _layout__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./layout */ "../blockly/lib/layout.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./manager */ "../blockly/lib/manager.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./registry */ "../blockly/lib/registry.js");
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./token */ "../blockly/lib/token.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./utils */ "../blockly/lib/utils.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widget */ "../blockly/lib/widget.js");
/* harmony import */ var _codewidget__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./codewidget */ "../blockly/lib/codewidget.js");
/* harmony import */ var _tools__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tools */ "../blockly/lib/tools.js");












/***/ }),

/***/ "../blockly/lib/layout.js":
/*!********************************!*\
  !*** ../blockly/lib/layout.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyLayout: () => (/* binding */ BlocklyLayout)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./utils */ "../blockly/lib/utils.js");
/* harmony import */ var _codewidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./codewidget */ "../blockly/lib/codewidget.js");



//import { BoxLayout } from '@lumino/widgets';


//import { IIterator, ArrayIterator } from '@lumino/algorithm';
//import { InputArea } from '@jupyterlab/cells';
//import { SimplifiedOutputArea, OutputAreaModel } from '@jupyterlab/outputarea';
//import { CodeMirrorEditor } from './editor';
//import { CodeEditor } from '@jupyterlab/codeeditor'





/**
 * A blockly layout to host the Blockly editor.
 */
class BlocklyLayout extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.SplitLayout {
    /**
     * Construct a `BlocklyLayout`.
     *
     */
    constructor(manager, sessionContext, rendermime) {
        super({ renderer: _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.SplitPanel.defaultRenderer, orientation: 'horizontal' });
        this._finishedLoading = false;
        this._manager = manager;
        this._sessionContext = sessionContext;
        // Creating the container for the Blockly editor
        // and the output area to render the execution replies.
        this._host = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget();
        this._dock = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.DockPanel();
        const factoryService = new _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__.CodeMirrorEditorFactory({});
        // Creating a CodeCell widget to render the code and
        // outputs from the execution reply.
        this._cell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell({
            model: new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCellModel(),
            contentFactory: new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.Cell.ContentFactory({
                editorFactory: factoryService.newInlineEditor
                //editorFactory: factoryService.newInlineEditor.bind(factoryService)
            }),
            rendermime
        });
        // Trust the outputs and set the mimeType for the code
        this._cell.addClass('jp-blockly-codeCell');
        this._cell.title.label = '# Code View';
        this._cell.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.codeIcon;
        this._cell.readOnly = true;
        this._cell.model.trusted = true;
        this._cell.model.mimeType = this._manager.mimeType;
        this._cell.node.style.overflow = 'scroll';
        //
        this._cell.outputArea.title.label = '# Output View';
        this._cell.outputArea.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.circleIcon;
        this._cell.outputArea.node.style.overflow = 'scroll';
        //this._cell.outputArea.node.style.marginTop = '40px';
        this._cell.outputArea.node.style.paddingTop = '40px';
        this._cell.outputArea.node.style.paddingRight = '20px';
        this._cell.outputArea.node.style.paddingBottom = '100px';
        this._cell.outputArea.node.style.border = '0px';
        this._code = new _codewidget__WEBPACK_IMPORTED_MODULE_7__.SourceCodeWidget('jp-blockly-sourceCode', '# Code View');
        /*
            // InputArea of code
            this._inpt = new InputArea({
              model: new CodeCellModel({}),
              contentFactory: new Cell.ContentFactory({
                //editorFactory: factoryService.newDocumentEditor
                editorFactory: factoryService.newDocumentEditor.bind(factoryService)
                //editorFactory: factoryService.newInlineEditor.bind(factoryService)
              })
            });
        
            this._output = new SimplifiedOutputArea({
              model: new OutputAreaModel({ trusted: true }),
              rendermime
            });
        */
        this._manager.changed.connect(this._onManagerChanged, this);
    }
    /*
     * The code cell.
     */
    get cell() {
        return this._cell;
    }
    /*
     */
    get code() {
        return this._code;
    }
    /*
     * The current workspace.
     */
    get workspace() {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        return blockly__WEBPACK_IMPORTED_MODULE_6__.serialization.workspaces.save(this._workspace);
    }
    /*
     * Set a new workspace.
     */
    set workspace(workspace) {
        const data = workspace === null ? { variables: [] } : workspace;
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        blockly__WEBPACK_IMPORTED_MODULE_6__.serialization.workspaces.load(data, this._workspace);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this._manager.changed.disconnect(this._resizeWorkspace, this);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
        this._workspace.dispose();
        super.dispose();
    }
    /**
     * Init the blockly layout
     */
    init() {
        super.init();
        this.insertWidget(0, this._host);
    }
    /**
     * Create an iterator over the widgets in the layout.
     */
    /*
      iter(): IIterator<Widget> {
        return new ArrayIterator([]);
      }
    */
    /**
     * Remove a widget from the layout.
     *
     * @param widget - The `widget` to remove.
     */
    removeWidget(widget) {
        return;
    }
    /**
     * Return the extra coded (if it exists), composed of the individual
     * data from each block in the workspace, which are defined in the
     * toplevel_init property. (e.g. : imports needed for the block)
     *
     * Add extra code example:
     * Blockly.Blocks['block_name'].toplevel_init = `import numpy`
     */
    getBlocksToplevelInit() {
        // Initalize string which will return the extra code provided
        // by the blocks, in the toplevel_init property.
        let finalToplevelInit = '';
        // Get all the blocks in the workspace in order.
        const ordered = true;
        const used_blocks = this._workspace.getAllBlocks(ordered);
        // For each block in the workspace, check if theres is a toplevel_init,
        // if there is, add it to the final string.
        for (const block in used_blocks) {
            const current_block = used_blocks[block].type;
            if (blockly__WEBPACK_IMPORTED_MODULE_6__.Blocks[current_block].toplevel_init) {
                // console.log(Blockly.Blocks[current_block].toplevel_init);
                // Attach it to the final string
                const string = blockly__WEBPACK_IMPORTED_MODULE_6__.Blocks[current_block].toplevel_init;
                finalToplevelInit = finalToplevelInit + string;
            }
        }
        // console.log(finalToplevelInit);
        return finalToplevelInit;
    }
    /*
     * Generates and runs the code from the current workspace.
     */
    run() {
        var _a;
        // Get extra code from the blocks in the workspace.
        const extra_init = this.getBlocksToplevelInit();
        // Serializing our workspace into the chosen language generator.
        const code = extra_init + this._manager.generator.workspaceToCode(this._workspace);
        //const code = "import ipywidgets as widgets\nwidgets.IntSlider()";
        this._cell.model.sharedModel.setSource(code);
        this._code.setLanguage((_a = this._manager.kernelspec) === null || _a === void 0 ? void 0 : _a.language);
        this._code.setSource(code);
        // Execute the code using the kernel, by using a static method from the
        // same class to make an execution request.
        if (this._sessionContext.hasNoKernel) {
            // Check whether there is a kernel
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Select a valid kernel', `There is not a valid kernel selected, select one from the dropdown menu in the toolbar.
        If there isn't a valid kernel please install 'xeus-python' from Pypi.org or using mamba.
        `);
        }
        else {
            // focus outputArea
            this._dock.activateWidget(this._cell.outputArea);
            //
            _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell.execute(this._cell, this._sessionContext)
                .then(() => this._resizeWorkspace())
                .catch(e => {
                console.error(e);
                window.alert('Warning: Perhaps, canceled future for execute_request message before replies were done.');
            });
        }
    }
    interrupt() {
        if (!this._sessionContext.hasNoKernel) {
            const kernel = this._sessionContext.session.kernel;
            kernel.interrupt();
        }
    }
    clearOutputArea() {
        // focus outputArea
        this._dock.activateWidget(this._cell.outputArea);
        this._cell.outputArea.model.clear();
    }
    setupWidgetView() {
        if (!this._host.isVisible) {
            this.removeWidgetAt(0);
            this.insertWidget(0, this._host);
        }
        if (this._cell.outputArea != null && !this._cell.outputArea.isVisible) {
            this._dock.addWidget(this._cell.outputArea);
            //this._dock.addWidget(this._cell);
            this._dock.addWidget(this._code);
            this.removeWidgetAt(1);
            this.insertWidget(1, this._dock);
        }
    }
    /**
     * Handle `update-request` messages sent to the widget.
     */
    onUpdateRequest(msg) {
        super.onUpdateRequest(msg);
        this._resizeWorkspace();
    }
    /**
     * Handle `resize-request` messages sent to the widget.
     */
    onResize(msg) {
        super.onResize(msg);
        this._resizeWorkspace();
    }
    /**
     * Handle `fit-request` messages sent to the widget.
     */
    onFitRequest(msg) {
        super.onFitRequest(msg);
        this._resizeWorkspace();
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        //inject Blockly with appropiate JupyterLab theme.
        this._workspace = blockly__WEBPACK_IMPORTED_MODULE_6__.inject(this._host.node, {
            toolbox: this._manager.toolbox,
            theme: _utils__WEBPACK_IMPORTED_MODULE_8__.THEME
        });
        this._workspace.addChangeListener((event) => {
            var _a;
            // Get extra code from the blocks in the workspace.
            const extra_init = this.getBlocksToplevelInit();
            // Serializing our workspace into the chosen language generator.
            const code = extra_init + this._manager.generator.workspaceToCode(this._workspace);
            this._cell.model.sharedModel.setSource(code);
            this._code.setLanguage((_a = this._manager.kernelspec) === null || _a === void 0 ? void 0 : _a.language);
            this._code.setSource(code);
            //
            if (event.type == blockly__WEBPACK_IMPORTED_MODULE_6__.Events.FINISHED_LOADING) {
                this._finishedLoading = true;
            }
            else if (this._finishedLoading && (event.type == blockly__WEBPACK_IMPORTED_MODULE_6__.Events.BLOCK_CHANGE ||
                event.type == blockly__WEBPACK_IMPORTED_MODULE_6__.Events.BLOCK_CREATE ||
                event.type == blockly__WEBPACK_IMPORTED_MODULE_6__.Events.BLOCK_MOVE ||
                event.type == blockly__WEBPACK_IMPORTED_MODULE_6__.Events.BLOCK_DELETE)) {
                // dirty workspace
                this._manager.dirty(true);
            }
        });
    }
    _resizeWorkspace() {
        //Resize logic.
        blockly__WEBPACK_IMPORTED_MODULE_6__.svgResize(this._workspace);
    }
    _onManagerChanged(sender, change) {
        var _a;
        if (change === 'kernel') {
            // Get extra code from the blocks in the workspace.
            const extra_init = this.getBlocksToplevelInit();
            // Serializing our workspace into the chosen language generator.
            const code = extra_init + this._manager.generator.workspaceToCode(this._workspace);
            this._cell.model.sharedModel.setSource(code);
            this._cell.model.mimeType = this._manager.mimeType;
            //
            this._code.setLanguage((_a = this._manager.kernelspec) === null || _a === void 0 ? void 0 : _a.language);
            this._code.setSource(code);
        }
        else if (change === 'toolbox') {
            this._workspace.updateToolbox(this._manager.toolbox);
        }
    }
}


/***/ }),

/***/ "../blockly/lib/manager.js":
/*!*********************************!*\
  !*** ../blockly/lib/manager.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyManager: () => (/* binding */ BlocklyManager)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

/**
 * BlocklyManager the manager for each document
 * to select the toolbox and the generator that the
 * user wants to use on a specific document.
 */
class BlocklyManager {
    /**
     * Constructor of BlocklyManager.
     */
    constructor(app, registry, sessionContext, mimetypeService) {
        this._app = app;
        this._registry = registry;
        this._sessionContext = sessionContext;
        this._mimetypeService = mimetypeService;
        this._toolbox = 'default';
        this._generator = this._registry.generators.get('python');
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._sessionContext.kernelChanged.connect(this._onKernelChanged, this);
        this._language = this._registry.language;
        __webpack_require__("../blockly/lib/msg lazy recursive ^\\.\\/.*\\.js$")(`./${this._language}.js`)
            .then(() => {
            this._changed.emit('toolbox');
        })
            .catch(() => {
            if (this._language !== 'En') {
                __webpack_require__.e(/*! import() */ "blockly_lib_msg_En_js").then(__webpack_require__.bind(__webpack_require__, /*! ./msg/En.js */ "../blockly/lib/msg/En.js"))
                    .then(() => { this._changed.emit('toolbox'); })
                    .catch(() => { });
            }
        });
        this._shell = this._app.shell;
        this._shell.currentChanged.connect((_, change) => {
            this._changed.emit('focus');
        });
        this._shell.activeChanged.connect((_, change) => {
            this._changed.emit('focus');
        });
    }
    get shell() {
        return this._shell;
    }
    /**
     * Returns the selected toolbox.
     */
    get toolbox() {
        return this._registry.toolboxes.get(this._toolbox);
    }
    /**
     * Returns the mimeType for the selected kernel.
     *
     * Note: We need the mimeType for the syntax highlighting
     * when rendering the code.
     */
    get mimeType() {
        if (this._selectedKernel) {
            return this._mimetypeService.getMimeTypeByLanguage({
                name: this._selectedKernel.language
            });
        }
        else {
            return 'text/plain';
        }
    }
    /**
     * Returns the name of the selected kernel.
     */
    get kernel() {
        var _a;
        return ((_a = this._selectedKernel) === null || _a === void 0 ? void 0 : _a.name) || 'No kernel';
    }
    /**
     *
     */
    get kernelspec() {
        return this._selectedKernel;
    }
    /**
     * Returns the selected generator.
     */
    get generator() {
        return this._generator;
    }
    /**
     * Signal triggered when the manager changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Send a 'block' signal to BlocklyEditor
     */
    dirty(dirty) {
        if (dirty) {
            this._changed.emit('dirty');
        }
    }
    /**
     * Dispose.
     */
    dispose() {
        this._sessionContext.kernelChanged.disconnect(this._onKernelChanged, this);
    }
    /**
     * Get the selected toolbox's name.
     *
     * @returns The name of the toolbox.
     */
    getToolbox() {
        return this._toolbox;
    }
    /**
     * Set the selected toolbox.
     *
     * @argument name The name of the toolbox.
     */
    setToolbox(name) {
        if (this._toolbox !== name) {
            const toolbox = this._registry.toolboxes.get(name);
            this._toolbox = toolbox ? name : 'default';
            this._changed.emit('toolbox');
        }
    }
    /**
     * List the available toolboxes.
     *
     * @returns the list of available toolboxes for Blockly
     */
    listToolboxes() {
        const list = [];
        this._registry.toolboxes.forEach((toolbox, name) => {
            list.push({ label: name, value: name });
        });
        return list;
    }
    /**
     * Set the selected kernel.
     *
     * @argument name The name of the kernel.
     */
    selectKernel(name) {
        this._sessionContext.changeKernel({ name });
    }
    /**
     * List the available kernels.
     *
     * @returns the list of available kernels for Blockly
     */
    listKernels() {
        const specs = this._sessionContext.specsManager.specs.kernelspecs;
        const list = [];
        Object.keys(specs).forEach(key => {
            const language = specs[key].language;
            if (this._registry.generators.has(language)) {
                list.push({ label: specs[key].display_name, value: specs[key].name });
            }
        });
        return list;
    }
    _onKernelChanged(sender, args) {
        const specs = this._sessionContext.specsManager.specs.kernelspecs;
        if (args.newValue && specs[args.newValue.name] !== undefined) {
            this._selectedKernel = specs[args.newValue.name];
            const language = specs[args.newValue.name].language;
            this._generator = this._registry.generators.get(language);
            this._changed.emit('kernel');
        }
    }
}


/***/ }),

/***/ "../blockly/lib/registry.js":
/*!**********************************!*\
  !*** ../blockly/lib/registry.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyRegistry: () => (/* binding */ BlocklyRegistry)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! blockly/python */ "../../node_modules/blockly/python.js");
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(blockly_python__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! blockly/javascript */ "../../node_modules/blockly/javascript.js");
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(blockly_javascript__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var blockly_lua__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! blockly/lua */ "../../node_modules/blockly/lua.js");
/* harmony import */ var blockly_lua__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(blockly_lua__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var blockly_dart__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! blockly/dart */ "../../node_modules/blockly/dart.js");
/* harmony import */ var blockly_dart__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(blockly_dart__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var blockly_php__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! blockly/php */ "../../node_modules/blockly/php.js");
/* harmony import */ var blockly_php__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(blockly_php__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var blockly_msg_en__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! blockly/msg/en */ "../../node_modules/blockly/msg/en.js");
/* harmony import */ var blockly_msg_en__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(blockly_msg_en__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./utils */ "../blockly/lib/utils.js");








/**
 * BlocklyRegistry is the class that JupyterLab-Blockly exposes
 * to other plugins. This registry allows other plugins to register
 * new Toolboxes, Blocks and Generators that users can use in the
 * Blockly editor.
 */
class BlocklyRegistry {
    /**
     * Constructor of BlocklyRegistry.
     */
    constructor() {
        this._language = "En";
        this._lock = false;
        this._toolboxes = new Map();
        this._toolboxes.set('default', _utils__WEBPACK_IMPORTED_MODULE_7__.TOOLBOX);
        //
        this._generators = new Map();
        this._generators.set('python', blockly_python__WEBPACK_IMPORTED_MODULE_1__.pythonGenerator);
        this._generators.set('javascript', blockly_javascript__WEBPACK_IMPORTED_MODULE_2__.javascriptGenerator);
        this._generators.set('lua', blockly_lua__WEBPACK_IMPORTED_MODULE_3__.luaGenerator);
        this._generators.set('dart', blockly_dart__WEBPACK_IMPORTED_MODULE_4__.dartGenerator);
        this._generators.set('php', blockly_php__WEBPACK_IMPORTED_MODULE_5__.phpGenerator);
    }
    /**
     * Returns a map with all the toolboxes.
     */
    get toolboxes() {
        return this._toolboxes;
    }
    /**
     * Returns a map with all the generators.
     */
    get generators() {
        return this._generators;
    }
    /**
     * Returns language (2 charactors).
     */
    get language() {
        return this._language;
    }
    get lock() {
        return this._lock;
    }
    set lock(use) {
        this._lock = use;
    }
    /**
     * Register a toolbox for the editor.
     *
     * @argument name The name of the toolbox.
     *
     * @argument toolbox The toolbox to register.
     */
    registerToolbox(name, toolbox) {
        this._toolboxes.set(name, toolbox);
    }
    /**
     * Register block definitions.
     *
     * @argument blocks A list of block definitions to register.
     */
    registerBlocks(blocks) {
        blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray(blocks);
    }
    /**
     * Register a language generator.
     *
     * @argument language The language output by the generator.
     *
     * @argument generator The generator to register.
     *
     * #### Notes
     * If a generator already exists for the given language it is overwritten.
     */
    registerGenerator(language, generator) {
        this._generators.set(language, generator);
    }
    /**
     * Register blocks codes.
     *
     * @argument language The name of the programming language. python, lua, javascript, ...
     *
     * @argument funcs Imported functions.
     */
    registerCodes(language, funcs) {
        let generator = this._generators.get(language);
        Object.assign(generator, funcs);
    }
    setlanguage(language) {
        this._language = language;
        Private.importLanguageModule(language);
    }
}
var Private;
(function (Private) {
    // Dynamically importing the language modules needed for each respective
    // user, in order to change the Blockly language in accordance to the
    // JL one.
    async function importLanguageModule(language) {
        let module;
        switch (language) {
            case 'En':
                module = Promise.resolve(/*! import() */).then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/en */ "../../node_modules/blockly/msg/en.js", 23));
                break;
            case 'Es':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_es_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/es */ "../../node_modules/blockly/msg/es.js", 23));
                break;
            case 'Fr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_fr_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/fr */ "../../node_modules/blockly/msg/fr.js", 23));
                break;
            case 'Sa' || 0:
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ar_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ar */ "../../node_modules/blockly/msg/ar.js", 23));
                break;
            case 'Cz':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_cs_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/cs */ "../../node_modules/blockly/msg/cs.js", 23));
                break;
            case 'Dk':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_da_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/da */ "../../node_modules/blockly/msg/da.js", 23));
                break;
            case 'De':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_de_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/de */ "../../node_modules/blockly/msg/de.js", 23));
                break;
            case 'Gr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_el_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/el */ "../../node_modules/blockly/msg/el.js", 23));
                break;
            case 'Ee':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_et_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/et */ "../../node_modules/blockly/msg/et.js", 23));
                break;
            case 'Fi':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_fi_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/fi */ "../../node_modules/blockly/msg/fi.js", 23));
                break;
            case 'Il':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_he_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/he */ "../../node_modules/blockly/msg/he.js", 23));
                break;
            case 'Hu':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_hu_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/hu */ "../../node_modules/blockly/msg/hu.js", 23));
                break;
            case 'Am':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_hy_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/hy */ "../../node_modules/blockly/msg/hy.js", 23));
                break;
            case 'Id':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_id_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/id */ "../../node_modules/blockly/msg/id.js", 23));
                break;
            case 'It':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_it_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/it */ "../../node_modules/blockly/msg/it.js", 23));
                break;
            case 'Jp':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ja_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ja */ "../../node_modules/blockly/msg/ja.js", 23));
                break;
            case 'Kr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ko_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ko */ "../../node_modules/blockly/msg/ko.js", 23));
                break;
            case 'Lt':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_lt_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/lt */ "../../node_modules/blockly/msg/lt.js", 23));
                break;
            case 'Nl':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_nl_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/nl */ "../../node_modules/blockly/msg/nl.js", 23));
                break;
            case 'Pl':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_pl_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/pl */ "../../node_modules/blockly/msg/pl.js", 23));
                break;
            case 'Br':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_pt_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/pt */ "../../node_modules/blockly/msg/pt.js", 23));
                break;
            case 'Ro':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ro_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ro */ "../../node_modules/blockly/msg/ro.js", 23));
                break;
            case 'Ru':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ru_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ru */ "../../node_modules/blockly/msg/ru.js", 23));
                break;
            case 'Lk':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_si_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/si */ "../../node_modules/blockly/msg/si.js", 23));
                break;
            case 'Tr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_tr_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/tr */ "../../node_modules/blockly/msg/tr.js", 23));
                break;
            case 'Ua':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_uk_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/uk */ "../../node_modules/blockly/msg/uk.js", 23));
                break;
            case 'Vn':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_vi_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/vi */ "../../node_modules/blockly/msg/vi.js", 23));
                break;
            case 'Tw':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_zh-hant_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/zh-hant */ "../../node_modules/blockly/msg/zh-hant.js", 23));
                break;
            case 'Cn':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_zh-hans_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/zh-hans */ "../../node_modules/blockly/msg/zh-hans.js", 23));
                break;
            default:
                // Complete with all the cases taken from: (last updates June 2022)
                // List of languages in blockly: https://github.com/google/blockly/tree/master/msg/js
                // List of languages in Lab: https://github.com/jupyterlab/language-packs/tree/master/language-packs
                console.warn('Language not found. Loading english');
                module = Promise.resolve((blockly_msg_en__WEBPACK_IMPORTED_MODULE_6___default()));
                break;
        }
        // Setting the current language in Blockly.
        module.then(lang => {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            blockly__WEBPACK_IMPORTED_MODULE_0__.setLocale(lang);
        });
    }
    Private.importLanguageModule = importLanguageModule;
})(Private || (Private = {}));


/***/ }),

/***/ "../blockly/lib/token.js":
/*!*******************************!*\
  !*** ../blockly/lib/token.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IBlocklyRegistry: () => (/* binding */ IBlocklyRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The registry token.
 */
const IBlocklyRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab-broccoli/registry');


/***/ }),

/***/ "../blockly/lib/toolbar/generator.js":
/*!*******************************************!*\
  !*** ../blockly/lib/toolbar/generator.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectGenerator: () => (/* binding */ SelectGenerator)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "../blockly/lib/toolbar/utils.js");



class SelectGenerator extends _utils__WEBPACK_IMPORTED_MODULE_2__.BlocklyButton {
    constructor(props) {
        super(props);
        this.handleChange = (event) => {
            this._manager.selectKernel(event.target.value);
            this.update();
        };
        this._manager = props.manager;
        this._manager.changed.connect(this.update, this);
    }
    dispose() {
        super.dispose();
        this._manager.changed.disconnect(this.update, this);
    }
    render() {
        const kernels = this._manager.listKernels();
        if (this._manager.kernel === 'No kernel') {
            kernels.push({ label: 'No kernel', value: 'No kernel' });
        }
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.HTMLSelect, { onChange: this.handleChange, value: this._manager.kernel, options: kernels }));
    }
}


/***/ }),

/***/ "../blockly/lib/toolbar/toolbox.js":
/*!*****************************************!*\
  !*** ../blockly/lib/toolbar/toolbox.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectToolbox: () => (/* binding */ SelectToolbox)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "../blockly/lib/toolbar/utils.js");



class SelectToolbox extends _utils__WEBPACK_IMPORTED_MODULE_2__.BlocklyButton {
    constructor(props) {
        super(props);
        this.handleChange = (event) => {
            this._manager.setToolbox(event.target.value);
            this.update();
        };
        this._manager = props.manager;
        this._manager.changed.connect(this.update, this);
    }
    dispose() {
        super.dispose();
        this._manager.changed.disconnect(this.update, this);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.HTMLSelect, { onChange: this.handleChange, value: this._manager.getToolbox(), options: this._manager.listToolboxes() }));
    }
}


/***/ }),

/***/ "../blockly/lib/toolbar/utils.js":
/*!***************************************!*\
  !*** ../blockly/lib/toolbar/utils.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyButton: () => (/* binding */ BlocklyButton),
/* harmony export */   Spacer: () => (/* binding */ Spacer)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);


class BlocklyButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton {
    constructor(props) {
        super(props);
        this.addClass('jp-blockly-button');
    }
}
class Spacer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor() {
        super();
        this.addClass('jp-Toolbar-spacer');
    }
}


/***/ }),

/***/ "../blockly/lib/tools.js":
/*!*******************************!*\
  !*** ../blockly/lib/tools.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JlbTools: () => (/* binding */ JlbTools)
/* harmony export */ });
/**
*/
var JlbTools;
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


/***/ }),

/***/ "../blockly/lib/utils.js":
/*!*******************************!*\
  !*** ../blockly/lib/utils.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   THEME: () => (/* binding */ THEME),
/* harmony export */   TOOLBOX: () => (/* binding */ TOOLBOX)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);

// Creating a toolbox containing all the main (default) blocks.
const TOOLBOX = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'category',
            name: '%{BKY_TOOLBOX_LOGIC}',
            colour: '210',
            contents: [
                {
                    kind: 'block',
                    type: 'controls_if'
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_compare'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_operation"></block>',
                    type: 'logic_operation'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_negate"></block>',
                    type: 'logic_negate'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_boolean"></block>',
                    type: 'logic_boolean'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_null"></block>',
                    type: 'logic_null'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_ternary"></block>',
                    type: 'logic_ternary'
                }
            ]
        },
        {
            kind: 'category',
            name: '%{BKY_TOOLBOX_LOOPS}',
            colour: '120',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_repeat_ext">\n          <value name="TIMES">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_repeat_ext'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_whileUntil"></block>',
                    type: 'controls_whileUntil'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_for">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n          <value name="BY">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_for'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_forEach"></block>',
                    type: 'controls_forEach'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_flow_statements"></block>',
                    type: 'controls_flow_statements'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_MATH}',
            colour: '230',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number"></block>',
                    type: 'math_number'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_arithmetic">\n          <value name="A">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="B">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_arithmetic'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_single">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">9</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_single'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_trig">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">45</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_trig'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constant"></block>',
                    type: 'math_constant'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number_property">\n          <value name="NUMBER_TO_CHECK">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_number_property'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_change">\n          <value name="DELTA">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_change'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_round">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">3.1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_round'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_on_list"></block>',
                    type: 'math_on_list'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_modulo">\n          <value name="DIVIDEND">\n            <shadow type="math_number">\n              <field name="NUM">64</field>\n            </shadow>\n          </value>\n          <value name="DIVISOR">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_modulo'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constrain">\n          <value name="VALUE">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="LOW">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="HIGH">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_constrain'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_int">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_random_int'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_float"></block>',
                    type: 'math_random_float'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_TEXT}',
            colour: '160',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text"></block>',
                    type: 'text'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_join"></block>',
                    type: 'text_join'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_append">\n          <value name="TEXT">\n            <shadow type="text"></shadow>\n          </value>\n        </block>',
                    type: 'text_append'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_length">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_isEmpty">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT"></field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n          <value name="FIND">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_charAt">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_charAt'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_getSubstring">\n          <value name="STRING">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_getSubstring'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_changeCase">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_changeCase'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_trim">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_trim'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_print">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_print'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_prompt_ext">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_prompt_ext'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_LISTS}',
            colour: '260',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with">\n          <mutation items="0"></mutation>\n        </block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with"></block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_repeat">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_repeat'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_length"></block>',
                    type: 'lists_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_isEmpty"></block>',
                    type: 'lists_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getIndex">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_setIndex">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_setIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getSublist">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getSublist'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_split">\n          <value name="DELIM">\n            <shadow type="text">\n              <field name="TEXT">,</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_split'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_sort"></block>',
                    type: 'lists_sort'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_COLOR}',
            colour: '20',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_picker"></block>',
                    type: 'colour_picker'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_random"></block>',
                    type: 'colour_random'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_rgb">\n          <value name="RED">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n          <value name="GREEN">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="BLUE">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_rgb'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_blend">\n          <value name="COLOUR1">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#ff0000</field>\n            </shadow>\n          </value>\n          <value name="COLOUR2">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#3333ff</field>\n            </shadow>\n          </value>\n          <value name="RATIO">\n            <shadow type="math_number">\n              <field name="NUM">0.5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_blend'
                }
            ]
        },
        {
            kind: 'SEP'
        },
        {
            kind: 'CATEGORY',
            colour: '330',
            custom: 'VARIABLE',
            name: '%{BKY_TOOLBOX_VARIABLES}'
        },
        {
            kind: 'CATEGORY',
            colour: '290',
            custom: 'PROCEDURE',
            name: '%{BKY_TOOLBOX_FUNCTIONS}'
        }
    ]
};
// Defining a Blockly Theme in accordance with the current JupyterLab Theme.
const jupyterlab_theme = blockly__WEBPACK_IMPORTED_MODULE_0__.Theme.defineTheme('jupyterlab', {
    name: 'JupyterLab Blockly',
    base: blockly__WEBPACK_IMPORTED_MODULE_0__.Themes.Classic,
    componentStyles: {
        workspaceBackgroundColour: 'var(--jp-layout-color0)',
        toolboxBackgroundColour: 'var(--jp-layout-color2)',
        toolboxForegroundColour: 'var(--jp-ui-font-color0)',
        flyoutBackgroundColour: 'var(--jp-border-color2)',
        flyoutForegroundColour: 'var(--jp-layout-color3)',
        flyoutOpacity: 1,
        scrollbarColour: 'var(--jp-border-color0)',
        insertionMarkerOpacity: 0.3,
        scrollbarOpacity: 0.4,
        cursorColour: 'var(--jp-scrollbar-background-color)'
    },
    fontStyle: {
        // letters are corrupted in spacing with var()
        family: '--jp-ui-font-family'
    }
});
const THEME = jupyterlab_theme;


/***/ }),

/***/ "../blockly/lib/widget.js":
/*!********************************!*\
  !*** ../blockly/lib/widget.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BlocklyEditor: () => (/* binding */ BlocklyEditor),
/* harmony export */   BlocklyPanel: () => (/* binding */ BlocklyPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _dialog__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./dialog */ "../blockly/lib/dialog.js");
/* harmony import */ var _layout__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./layout */ "../blockly/lib/layout.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./toolbar */ "../blockly/lib/toolbar/utils.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./toolbar */ "../blockly/lib/toolbar/toolbox.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./toolbar */ "../blockly/lib/toolbar/generator.js");
/* harmony import */ var _tools__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tools */ "../blockly/lib/tools.js");










const DIRTY_CLASS = 'jp-mod-dirty';
/**
 * DocumentWidget: widget that represents the view or editor for a file type.
 */
class BlocklyEditor extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.DocumentWidget {
    constructor(app, options) {
        super(options);
        this._dirty = false;
        this._context = options.context;
        this._manager = options.manager;
        // Loading the ITranslator
        this._trans = (this._context.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
        // this.content is BlocklyPanel
        this._blayout = this.content.layout;
        // Create and add a button to the toolbar to execute
        // the code.
        const button_save = new _toolbar__WEBPACK_IMPORTED_MODULE_6__.BlocklyButton({
            label: '',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.saveIcon,
            className: 'jp-blockly-saveFile',
            onClick: () => this.save(true),
            tooltip: 'Save File'
        });
        const button_run = new _toolbar__WEBPACK_IMPORTED_MODULE_6__.BlocklyButton({
            label: '',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.runIcon,
            className: 'jp-blockly-runButton',
            onClick: () => this._blayout.run(),
            tooltip: 'Run Code'
        });
        const button_stop = new _toolbar__WEBPACK_IMPORTED_MODULE_6__.BlocklyButton({
            label: '',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.stopIcon,
            className: 'jp-blockly-stopButton',
            onClick: () => this._blayout.interrupt(),
            tooltip: 'Stop Code'
        });
        const button_clear = new _toolbar__WEBPACK_IMPORTED_MODULE_6__.BlocklyButton({
            label: '',
            //icon: circleEmptyIcon,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.clearIcon,
            className: 'jp-blockly-clearButton',
            onClick: () => this._blayout.clearOutputArea(),
            tooltip: 'Copy Output View'
        });
        const button_copyOutput = new _toolbar__WEBPACK_IMPORTED_MODULE_6__.BlocklyButton({
            label: '',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.copyIcon,
            className: 'jp-blockly-copyOutputButton',
            onClick: () => {
                const outputAreaAreas = this._blayout.cell.outputArea.node.getElementsByClassName('jp-OutputArea-output');
                if (outputAreaAreas.length > 0) {
                    let element = outputAreaAreas[0];
                    for (let i = 1; i < outputAreaAreas.length; i++) {
                        element.appendChild(outputAreaAreas[i]);
                    }
                    _tools__WEBPACK_IMPORTED_MODULE_7__.JlbTools.copyElement(element);
                }
            },
            tooltip: 'Copy Output View'
        });
        const button_copyCode = new _toolbar__WEBPACK_IMPORTED_MODULE_6__.BlocklyButton({
            label: '',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.duplicateIcon,
            className: 'jp-blockly-copyCodeButton',
            onClick: () => {
                _tools__WEBPACK_IMPORTED_MODULE_7__.JlbTools.copyElement(this._blayout.code.node);
            },
            tooltip: 'Copy Code View'
        });
        this.toolbar.addItem('save', button_save);
        this.toolbar.addItem('run', button_run);
        this.toolbar.addItem('stop', button_stop);
        this.toolbar.addItem('spacer1', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.Spacer());
        this.toolbar.addItem('spacer2', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.Spacer());
        this.toolbar.addItem('spacer3', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.Spacer());
        this.toolbar.addItem('spacer5', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.Spacer());
        this.toolbar.addItem('clear', button_clear);
        this.toolbar.addItem('copyOutput', button_copyOutput);
        this.toolbar.addItem('copyCode', button_copyCode);
        this.toolbar.addItem('spacer7', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.Spacer());
        this.toolbar.addItem('spacer8', new _toolbar__WEBPACK_IMPORTED_MODULE_6__.Spacer());
        this.toolbar.addItem('toolbox', new _toolbar__WEBPACK_IMPORTED_MODULE_8__.SelectToolbox({
            label: 'Toolbox',
            tooltip: 'Select tollbox',
            manager: options.manager
        }));
        this.toolbar.addItem('generator', new _toolbar__WEBPACK_IMPORTED_MODULE_9__.SelectGenerator({
            label: 'Kernel',
            tooltip: 'Select kernel',
            manager: options.manager
        }));
        //
        this._manager.changed.connect(this._onBlockChanged, this);
    } /* End of constructor */
    // for dialog.ts
    get trans() {
        return this._trans;
    }
    //
    get blayout() {
        return this._blayout;
    }
    //
    get cell() {
        var _a;
        return (_a = this._blayout) === null || _a === void 0 ? void 0 : _a.cell;
    }
    /**
     * Sets the dirty boolean while also toggling the DIRTY_CLASS
     */
    dirty(dirty) {
        this._dirty = dirty;
        //
        if (this._dirty && !this.title.className.includes(DIRTY_CLASS)) {
            this.title.className += ' ' + DIRTY_CLASS;
        }
        else if (!this._dirty) {
            this.title.className = this.title.className.replace(DIRTY_CLASS, '');
        }
        this.title.className = this.title.className.replace('  ', ' ');
    }
    // 
    async save(exiting = false) {
        exiting ? await this._context.save() : this._context.save();
        this.dirty(false);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    async dispose() {
        if (!this.isDisposed && this._dirty) {
            const isclose = await (0,_dialog__WEBPACK_IMPORTED_MODULE_10__.closeDialog)(this);
            if (!isclose)
                return;
        }
        this.content.dispose();
        super.dispose();
    }
    //
    _onBlockChanged(sender, change) {
        if (change === 'dirty') {
            this.dirty(true);
        }
        else if (change === 'focus') {
            this._blayout.setupWidgetView();
        }
    }
}
/**
 * Widget that contains the main view of the DocumentWidget.
 */
class BlocklyPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.SplitPanel {
    /**
     * Construct a `BlocklyPanel`.
     *
     * @param context - The documents context.
     */
    constructor(tracker, context, manager, rendermime) {
        super({
            layout: new _layout__WEBPACK_IMPORTED_MODULE_11__.BlocklyLayout(manager, context.sessionContext, rendermime)
        });
        this.addClass('jp-BlocklyPanel');
        this._context = context;
        this._rendermime = rendermime;
        this._manager = manager;
        this._tracker = tracker;
        this._editor = null;
        // Load the content of the file when the context is ready
        this._context.ready.then(() => this._load());
        // Connect to the save signal
        this._context.saveState.connect(this._onSave, this);
    }
    /*
     * The code cell.
     */
    get cell() {
        return this.layout.cell;
    }
    /*
     * The rendermime instance used in the code cell.
     */
    get rendermime() {
        return this._rendermime;
    }
    get context() {
        return this._context;
    }
    get content() {
        return this._content;
    }
    get manager() {
        return this._manager;
    }
    get activeLayout() {
        return this.layout;
    }
    set activeEditor(editor) {
        this._editor = editor;
    }
    get activeEditor() {
        return this._editor;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal.clearData(this);
        super.dispose();
    }
    _load() {
        // Loading the content of the document into the workspace
        let kernelname = '';
        this._content = this._context.model.toJSON();
        if (this._content != null) {
            if (('metadata' in this._content) &&
                ('kernelspec' in this._content['metadata']) &&
                ('name' in this._content['metadata']['kernelspec'])) {
                kernelname = this._content['metadata']['kernelspec']['name'];
            }
        }
        if (kernelname === '') {
            if (this._editor.id === this._tracker.currentWidget.id) {
                const sessionContextDialogs = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.SessionContextDialogs({ translator: this._context.translator });
                sessionContextDialogs.selectKernel(this._context.sessionContext);
            }
        }
        else {
            this._manager.selectKernel(kernelname);
        }
        this.layout.workspace = this._content;
        // Set Block View, Output View and Code View to DockPanel
        this.layout.setupWidgetView();
    }
    _onSave(sender, state) {
        if (state === 'started') {
            const workspace = this.layout.workspace;
            //
            if (this._manager['kernelspec'] != undefined) {
                workspace['metadata'] = {
                    'kernelspec': {
                        'display_name': this._manager.kernelspec.display_name,
                        'language': this._manager.kernelspec.language,
                        'name': this._manager.kernelspec.name
                    }
                };
            }
            this._context.model.fromJSON(workspace);
        }
    }
}


/***/ }),

/***/ "../blockly/lib/msg lazy recursive ^\\.\\/.*\\.js$":
/*!**************************************************************!*\
  !*** ../blockly/lib/msg/ lazy ^\.\/.*\.js$ namespace object ***!
  \**************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var map = {
	"./En.js": [
		"../blockly/lib/msg/En.js",
		"blockly_lib_msg_En_js"
	],
	"./Jp.js": [
		"../blockly/lib/msg/Jp.js",
		"blockly_lib_msg_Jp_js"
	]
};
function webpackAsyncContext(req) {
	if(!__webpack_require__.o(map, req)) {
		return Promise.resolve().then(() => {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		});
	}

	var ids = map[req], id = ids[0];
	return __webpack_require__.e(ids[1]).then(() => {
		return __webpack_require__(id);
	});
}
webpackAsyncContext.keys = () => (Object.keys(map));
webpackAsyncContext.id = "../blockly/lib/msg lazy recursive ^\\.\\/.*\\.js$";
module.exports = webpackAsyncContext;

/***/ })

}]);
//# sourceMappingURL=blockly_lib_index_js.d0501abfb4abe559d356.js.map