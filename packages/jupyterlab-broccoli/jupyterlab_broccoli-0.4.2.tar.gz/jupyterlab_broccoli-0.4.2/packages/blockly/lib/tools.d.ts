/**
*/
import { JupyterFrontEnd } from '@jupyterlab/application';
import { WidgetTracker } from '@jupyterlab/apputils';
import { BlocklyEditor } from './widget';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';
export declare namespace JlbTools {
    function copyElement(e: HTMLElement): void;
    function isEnabled(shell: JupyterFrontEnd.IShell, tracker: WidgetTracker<BlocklyEditor>): boolean;
    function getCurrentWidget(shell: JupyterFrontEnd.IShell, tracker: WidgetTracker<BlocklyEditor>, args: ReadonlyPartialJSONObject): BlocklyEditor | null;
    function disp_obj(obj: object): void;
}
