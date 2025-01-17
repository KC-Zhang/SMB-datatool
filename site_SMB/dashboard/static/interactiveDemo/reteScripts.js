import * as Vue from './node_modules/vue/dist/vue.min.js'
import * as Rete from './node_modules/rete/build/rete.min.js'
import * as VueRenderPlugin from './node_modules/rete-vue-render-plugin/build/vue-render-plugin.min.js'
import * as ConnectionPlugin from './node_modules/rete-comment-plugin/build/comment-plugin.min.js'
import * as ContextMenuPlugin from './node_modules/rete-context-menu-plugin/build/context-menu-plugin.min.js'
import * as AreaPlugin from './node_modules/rete-area-plugin/build/area-plugin.min.js'
import * as CommentPlugin from './node_modules/rete-comment-plugin/build/comment-plugin.min.js'
import * as HistoryPlugin from './node_modules/rete-history-plugin/build/history-plugin.min.js'
import * as ConnectionMasteryPlugin from './node_modules/rete-connection-mastery-plugin/build/connection-mastery-plugin.min.js'
import Lodash from './node_modules/lodash-es/min.js'

// {#<script src={% static './interactiveDemo/node_modules/vue/dist/vue.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete/build/rete.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-vue-render-plugin/build/vue-render-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-connection-plugin/build/connection-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-context-menu-plugin/build/context-menu-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-area-plugin/build/area-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-comment-plugin/build/comment-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-history-plugin/build/history-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/rete-connection-mastery-plugin/build/connection-mastery-plugin.min.js' %}></script>#}
// {#<script src={% static './interactiveDemo/node_modules/lodash-es/min.js' %}></script>#}

var numSocket = new Rete.Socket('Number value');
var VueNumControl = {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData'],
  template: '<input type="number" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>',
  data() {
    return {
      value: 0,
    }
  },
  methods: {
    change(e){
      this.value = +e.target.value;
      this.update();
    },
    update() {
      if (this.ikey)
        this.putData(this.ikey, this.value)
      this.emitter.trigger('process');
    }
  },
  mounted() {
    this.value = this.getData(this.ikey);
  }
}

class NumControl extends Rete.Control {

  constructor(emitter, key, readonly) {
    super(key);
    this.component = VueNumControl;
    this.props = { emitter, ikey: key, readonly };
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}

class NumComponent extends Rete.Component {

    constructor(){
        super("Number");
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Number", numSocket);

        return node.addControl(new NumControl(this.editor, 'num')).addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}

class AddComponent extends Rete.Component {
    constructor(){
        super("Add");
    }

    builder(node) {
        var inp1 = new Rete.Input('num',"Number", numSocket);
        var inp2 = new Rete.Input('num2', "Number2", numSocket);
        var out = new Rete.Output('num', "Number", numSocket);

        inp1.addControl(new NumControl(this.editor, 'num'))
        inp2.addControl(new NumControl(this.editor, 'num2'))

        return node
            .addInput(inp1)
            .addInput(inp2)
            .addControl(new NumControl(this.editor, 'preview', true))
            .addOutput(out);
    }

    worker(node, inputs, outputs) {
        var n1 = inputs['num'].length?inputs['num'][0]:node.data.num1;
        var n2 = inputs['num2'].length?inputs['num2'][0]:node.data.num2;
        var sum = n1 + n2;

        this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
        outputs['num'] = sum;
    }
}

class MyCanvasArea{
    constructor() {
        this.editor;
        this.engine;
        this.components;
        this.htmlContainerDiv;
    }
}
(async () => {
    myCanvasArea = new MyCanvasArea();
    myCanvasArea.htmlContainerDiv = document.querySelector('#interactiveDemoCanvas');
    myCanvasArea.components = [new NumComponent(), new AddComponent()];
    myCanvasArea.editor = new Rete.NodeEditor('demo@0.1.0', myCanvasArea.htmlContainerDiv);
    myCanvasArea.editor.use(ConnectionPlugin.default);
    myCanvasArea.editor.use(VueRenderPlugin.default);
    myCanvasArea.editor.use(ContextMenuPlugin.default);
    myCanvasArea.editor.use(AreaPlugin);
    myCanvasArea.editor.use(CommentPlugin.default);
    myCanvasArea.editor.use(HistoryPlugin);
    myCanvasArea.editor.use(ConnectionMasteryPlugin.default);

    myCanvasArea.engine = new Rete.Engine('demo@0.1.0');

    myCanvasArea.components.map(c => {
        myCanvasArea.editor.register(c);
        myCanvasArea.engine.register(c);
    });

    var n1 = await myCanvasArea.components[0].createNode({num: 2});
    var n2 = await myCanvasArea.components[0].createNode({num: 0});
    var add = await myCanvasArea.components[1].createNode();

    n1.position = [80, 0];
    n2.position = [80, 400];
    add.position = [500, 240];


    myCanvasArea.editor.addNode(n1);
    myCanvasArea.editor.addNode(n2);
    myCanvasArea.editor.addNode(add);

    myCanvasArea.editor.connect(n1.outputs.get('num'), add.inputs.get('num'));
    myCanvasArea.editor.connect(n2.outputs.get('num'), add.inputs.get('num2'));

    myCanvasArea.editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
      console.log('process');
        await myCanvasArea.engine.abort();
        await myCanvasArea.engine.process(myCanvasArea.editor.toJSON());
    });

    myCanvasArea.editor.view.resize();
    AreaPlugin.zoomAt(myCanvasArea.editor);
    myCanvasArea.editor.trigger('process');
})();

async function addNodeBlock(event) {

    var n1 = await myCanvasArea.components[0].createNode({num: 2});

    n1.position = [event.clientX-$(myCanvasArea.htmlContainerDiv).position().left, event.clientY-$(myCanvasArea.htmlContainerDiv).position().top];

    myCanvasArea.editor.addNode(n1);

    myCanvasArea.editor.connect(n1.outputs.get('num'));
    myCanvasArea.editor.trigger('process');
}
