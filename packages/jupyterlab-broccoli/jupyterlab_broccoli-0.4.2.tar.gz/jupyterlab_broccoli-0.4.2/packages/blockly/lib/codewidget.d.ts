/**
  SourceCodeWidhet Class
*/
import { Widget } from '@lumino/widgets';
import 'highlight.js/styles/github.css';
/**
 */
export declare class SourceCodeWidget extends Widget {
    private _source;
    private _language;
    constructor(classname: string, title: string);
    default_style(): void;
    setLanguage(lang: string): void;
    getLanguage(): string;
    setSource(code: string): void;
    getSource(): string;
}
