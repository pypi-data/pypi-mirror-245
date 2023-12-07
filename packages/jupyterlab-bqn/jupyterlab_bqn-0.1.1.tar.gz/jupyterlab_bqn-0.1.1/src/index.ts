import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IEditorLanguageRegistry } from '@jupyterlab/codemirror';
import { bqn } from 'lang-bqn';

/**
 * Initialization data for the jupyterlab-bqn extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-bqn:plugin',
  description: 'A JupyterLab extension for the BQN language.',
  autoStart: true,
  requires: [IEditorLanguageRegistry],
  activate: (app: JupyterFrontEnd, language: IEditorLanguageRegistry) => {
    const bqnSupport = bqn();
    language.addLanguage({
      name: 'bqn',
      mime: 'text/bqn',
      support: bqnSupport,
      extensions: ['bqn']
    });
    console.log('JupyterLab extension jupyterlab-bqn is activated!');
  }
};

export default plugin;
