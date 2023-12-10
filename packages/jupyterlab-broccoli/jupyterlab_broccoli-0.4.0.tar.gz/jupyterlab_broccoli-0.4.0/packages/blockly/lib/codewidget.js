/**
  SourceCodeWidhet Class
*/
import { Widget } from '@lumino/widgets';
import { codeIcon } from '@jupyterlab/ui-components';
import HLjs from 'highlight.js';
import 'highlight.js/styles/github.css';
//import 'highlight.js/styles/googlecode.css';
//declare function require(string): any;
/**
 */
export class SourceCodeWidget extends Widget {
    //
    constructor(classname, title) {
        super();
        //
        this.addClass(classname);
        this.title.label = title;
        this.title.icon = codeIcon;
        this.default_style();
        this._source = '';
        this._language = '';
        HLjs.highlightAll();
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
        this.node.innerHTML = HLjs.highlight(code, { language: this._language }).value;
    }
    //
    getSource() {
        return this._source;
    }
}
//# sourceMappingURL=codewidget.js.map