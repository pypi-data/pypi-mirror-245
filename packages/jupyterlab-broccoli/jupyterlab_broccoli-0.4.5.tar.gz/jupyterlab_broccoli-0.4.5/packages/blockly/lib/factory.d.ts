import { ABCWidgetFactory, DocumentRegistry, DocumentModel } from '@jupyterlab/docregistry';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { IEditorMimeTypeService } from '@jupyterlab/codeeditor';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { WidgetTracker } from '@jupyterlab/apputils';
import { CodeCell } from '@jupyterlab/cells';
import { TranslationBundle } from '@jupyterlab/translation';
import { BlocklyEditor } from './widget';
import { BlocklyRegistry } from './registry';
import { BlocklyManager } from './manager';
/**
 * A widget factory to create new instances of BlocklyEditor.
 */
export declare class BlocklyEditorFactory extends ABCWidgetFactory<BlocklyEditor, DocumentModel> {
    private _registry;
    private _rendermime;
    private _mimetypeService;
    private _manager;
    private _app;
    private _tracker;
    private _cell;
    private _trans;
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(app: JupyterFrontEnd, tracker: WidgetTracker<BlocklyEditor>, options: BlocklyEditorFactory.IOptions);
    get trans(): TranslationBundle;
    get registry(): BlocklyRegistry;
    get manager(): BlocklyManager;
    get cell(): CodeCell;
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    protected createNewWidget(context: DocumentRegistry.IContext<DocumentModel>): BlocklyEditor;
}
export declare namespace BlocklyEditorFactory {
    interface IOptions extends DocumentRegistry.IWidgetFactoryOptions {
        rendermime: IRenderMimeRegistry;
        mimetypeService: IEditorMimeTypeService;
    }
}
