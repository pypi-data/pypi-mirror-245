import { ABCWidgetFactory } from '@jupyterlab/docregistry';
import { nullTranslator } from '@jupyterlab/translation';
import { BlocklyEditor, BlocklyPanel } from './widget';
import { BlocklyRegistry } from './registry';
import { BlocklyManager } from './manager';
/**
 * A widget factory to create new instances of BlocklyEditor.
 */
export class BlocklyEditorFactory extends ABCWidgetFactory {
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(app, tracker, options) {
        super(options);
        this._app = app;
        this._tracker = tracker;
        this._registry = new BlocklyRegistry();
        this._rendermime = options.rendermime;
        this._mimetypeService = options.mimetypeService;
        this._trans = (options.translator || nullTranslator).load('jupyterlab');
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
        const manager = new BlocklyManager(this._app, this._registry, context.sessionContext, this._mimetypeService);
        this._manager = manager;
        const content = new BlocklyPanel(this._tracker, context, manager, this._rendermime);
        this._cell = content.activeLayout.cell;
        const editor = new BlocklyEditor(this._app, { context, content, manager });
        content.activeEditor = editor;
        return editor;
    }
}
//# sourceMappingURL=factory.js.map