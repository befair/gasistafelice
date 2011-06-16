/* Copyright 2009 Aaron Porter aaron@mongus.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


(function($) {

        function lerp(a, b, t) {
                // from http://www.cubic.org/docs/bezier.htm
                return {
                        x: Math.round(a.x + (b.x - a.x) * t),
                        y: Math.round(a.y + (b.y - a.y) * t)};
        }

        function bezierPoint(a, b, c, d, t) {
                var ab = lerp(a, b, t);
                var bc = lerp(b, c, t);
                var cd = lerp(c, d, t);
                var abbc = lerp(ab, bc, t);
                var bccd = lerp(bc, cd, t);
                return lerp(abbc, bccd, t);
        }

        // line drawing functions
        $.wireable = {
                bezier : function(x1, y1, x2, y2, options) {
                        var ctx = this.getContext('2d');

                        var width = Math.abs(x2 - x1);
                        var height = Math.abs(y2 - y1);

                        var v = Math.min(Math.max(width, height) / 2, 75);

                        ctx.beginPath();
                        ctx.moveTo(x1, y1);

                        var h1 = typeof options.sourceAngle == 'number' ? {
                                x : x1 + v * Math.cos(options.sourceAngle * Math.PI / 180),
                                y : y1 - v * Math.sin(options.sourceAngle * Math.PI / 180)
                        } : {
                                x : x1,
                                y : y1
                        };

                        var h2 = typeof options.sinkAngle == 'number' ? {
                                x : x2 + v * Math.cos(options.sinkAngle * Math.PI / 180),
                                y : y2 - v * Math.sin(options.sinkAngle * Math.PI / 180)
                        } : {
                                x : x2,
                                y : y2
                        };

                        ctx.bezierCurveTo(h1.x, h1.y, h2.x, h2.y, x2, y2);

                        ctx.lineCap = 'round';

                        ctx.lineWidth = options.width + options.borderWidth * 2;
                        ctx.strokeStyle = options.borderColor;
                        ctx.stroke();

                        ctx.lineWidth = options.width;
                        ctx.strokeStyle = options.color;
                        ctx.stroke();

                        if (options.calculateCuts) {
                                var length = Math.sqrt(width*width + height*height);

                                var p1, p2;

                                if (length < 90) {
                                        p1 = p2 = bezierPoint({x:x1, y:y1}, h1, h2, {x:x2, y:y2}, .5);
                                }
                                else {
                                        for (var i = .05; i < .5; i+=.025) {
                                                p1 = bezierPoint({x:x1, y:y1}, h1, h2, {x:x2, y:y2}, i);
                                                var w = p1.x-x1;
                                                var h = p1.y-y1;
                                                if (Math.sqrt(w*w + h*h) >= 25)
                                                        break;
                                        }
                                        for (var i = .95; i > .5; i-=.025) {
                                                p2 = bezierPoint({x:x1, y:y1}, h1, h2, {x:x2, y:y2}, i);
                                                var w = p2.x-x2;
                                                var h = p2.y-y2;
                                                if (Math.sqrt(w*w + h*h) >= 25)
                                                        break;
                                        }
                                }

                                this.info = $.extend(this.info || {}, {sourceCut:p1, sinkCut:p2});
                        }
                },

                line : function(x1, y1, x2, y2, options) {
                        var ctx = this.getContext('2d');

                        ctx.beginPath();
                        ctx.moveTo(x1, y1);
                        ctx.lineTo(x2, y2);

                        ctx.lineCap = 'round';

                        ctx.lineWidth = options.width + options.borderWidth * 2;
                        ctx.strokeStyle = options.borderColor;
                        ctx.stroke();

                        ctx.lineWidth = options.width;
                        ctx.strokeStyle = options.color;
                        ctx.stroke();

                        if (options.calculateCuts) {
                                var width = x2 - x1;
                                var height = y2 - y1;
                                var length = Math.sqrt(width*width + height*height);

                                var cx1, cy1, cx2, cy2;

                                if (length < 75) {
                                        cx1 = cx2 = Math.round((x1 + x2) / 2);
                                        cy1 = cy2 = Math.round((y1 + y2) / 2);
                                }
                                else {
                                        cx1 = x1 + Math.round(Math.cos(Math.acos(width/length))*25);
                                        cy1 = y1 + Math.round(Math.sin(Math.asin(height/length))*25);
                                        cx2 = x2 - Math.round(Math.cos(Math.acos(width/length))*25);
                                        cy2 = y2 - Math.round(Math.sin(Math.asin(height/length))*25);
                                }

                                this.info = $.extend(this.info || {}, {sourceCut:{x:cx1, y:cy1}, sinkCut:{x:cx2, y:cy2}});
                        }
                },

                wired : {}
        };

        // default values
        $.wireable.defaults = {
                width : 5,
                color : '#4cf',
                borderWidth : 1.5,
                borderColor : '#08f',
                target : '.terminal',           // selector for endpoints
                wiringCursor : 'pointer',
                drawFunction : $.wireable.bezier,
                sourceAngle : null,             // in degrees
                sinkAngle : null,               // in degrees
                wiredClass : 'wired',
                cutClass : 'wire-cut',
                container: 'body'

        };

        var cuts = [];
        var drawingWire = false;

        var drawInfo = {};

        $.fn.wireable = function(opts) {

                var options = $.extend({}, $.wireable.defaults);

                switch (typeof opts) {
                        case 'object':
                                $.extend(options, opts);
                                break;
                        case 'string':
                                options.target = opts;
                                break;
                }

                options.container = $(options.container || 'body');

                function drawWire() {
                        hideCuts();

                        var source = drawInfo.source;
                        var sink = drawInfo.sink;

                        var startPoint = source || sink;

                        var opts = $.metadata ? $.extend( {}, options, startPoint.metadata(), startPoint.metadata().source) : options;

                        var x = startPoint.offsetX + startPoint.offsetWidth / 2, y = startPoint.offsetY
                                        + startPoint.offsetHeight / 2;

                        var parent = startPoint.offsetParent;

                        while (parent != null) {
                                x += parent.offsetX;
                                y += parent.offsetY;
                                parent = parent.offsetParent;
                        }

                        var endPoint = $('<div></div>');
                        opts.container.append(endPoint);

                        drawingWire = true;;

                        startPoint.bind('drag', function(event, ui) {
                                // this handler is called before the element is moved
                                // so we need to wait a little before drawing
                                setTimeout(function() {
                                        if (drawingWire)
                                                draw(source || endPoint, sink || endPoint, opts);
                                }, 0);
                        }).bind('dragstop',function(event, ui) {
                                startPoint.unbind('drag').unbind('dragstop');
                                drawingWire = false;
                                var id = getId(source || endPoint) + ':'
                                + getId(sink || endPoint);
                                var canvas = $.wireable.wired[id];
                                $(canvas).remove();
                                endPoint.remove();
                        });

                        return endPoint;
                }

                function drawFromSource() {
                        drawInfo = {
                                source : $(this)
                        };
                        return drawWire().get(0);
                }

                function drawFromSink() {
                        drawInfo = {
                                sink : $(this)
                        };
                        return drawWire().get(0);
                }

                function createWire(event, ui) {
                        var source = drawInfo.source || $(this);
                        var sink = drawInfo.sink || $(this);

                        wire(source, sink, options);
                }

                var sourceSelector = options.target;
                var sinkSelector = this.selector;

                function makeDroppable(e, s) {
                        e.droppable( {
                                accept : s,
                                hoverClass : 'ui-state-hover',
                                activeClass : 'ui-state-active'
                        }).bind('drop', createWire);
                }

                this.not('.wireable-source').draggable( {
                        helper : drawFromSource,
                        cursor : options.wiringCursor,
                        cursorAt : {
                                top : 0,
                                left : 0
                        }
                }).each(function() {
                        var it = $(this);
                        makeDroppable(it, sourceSelector);
                        it.addClass('wireable-source');
                });

                $(options.target).not('.wireable-sink').draggable( {
                        helper : drawFromSink,
                        cursor : options.wiringCursor,
                        cursorAt : {
                                top : 0,
                                left : 0
                        }
                }).each(function() {
                        var it = $(this);
                        makeDroppable(it, sinkSelector);
                        it.addClass('wireable-sink');
                });

                return this;
        };

        function eventAllowed(eventName, source, sink) {
                var wiringEvent = $.Event(eventName);
                wiringEvent.source = source;
                wiringEvent.sink = sink;

                source.trigger(wiringEvent);
                if (!wiringEvent.isDefaultPrevented()) {
                        sink.trigger(wiringEvent);

                        if (!wiringEvent.isDefaultPrevented())
                                return true;
                }

                return false;
        }

        function wire(source, sink, options) {
                source = $(source);
                sink = $(sink);

                var id = getId(source) + ':' + getId(sink);

                if ($.wireable.wired[id]) {
                        // wire already exists
                        return false;
                }

                // make sure the source and the sink accept the wire
                if (!eventAllowed('wiring', source, sink))
                        return false;

                var opts = $.metadata ? $.extend({}, $.wireable.defaults, sink.metadata(),
                                source.metadata(),
                                sink.metadata().sink || {},
                                source.metadata().source || {},
                                options
                        ) : $.extend({}, $.wireable.defaults, options);

                opts.calculateCuts = true;

                // wire it up!
                var wire = draw(source, sink, opts);

                wire.info = $.extend(wire.info || {}, {source:source.get(0),sink:sink.get(0)});

                var dragHandler = function(event) {
                        if (event.target != this)
                                return;

                        hideCuts();

                        // this handler is called before the element is moved
                        // so we need to wait a little before drawing
                        setTimeout(function() {
                                draw(source, sink, opts);
                        }, 0);
                }

                var terminals = [source, sink];
                for (i in terminals) {
                        var terminal = terminals[i];

                        // when a parent of the terminal is dragged we need to redraw
                        terminal.parents().bind('drag dragstop', dragHandler);

                        terminal.bind('unwired', function(event) {
                                if (event.source.get(0) != source.get(0) || event.sink.get(0) != sink.get(0))
                                        return;

                                $(this).parents().unbind('drag dragstop', dragHandler);
                        });

                        var wires = terminal.get(0).wires;

                        if (!wires) {
                                terminal.get(0).wires = wires = [];
                                terminal.mouseenter(function(){showCuts.call(this, opts);});
                                terminal.mouseleave(function(){scheduleHideCuts.call(this, opts);});
                        }

                        wires[wires.length] = wire;

                        // let the source and sink know the wire has been created
                        var wiredEvent = $.Event('wired');
                        wiredEvent.source = source;
                        wiredEvent.sink = sink;

                        terminal.addClass(opts.wiredClass);

                        terminal.trigger(wiredEvent);
                }

                return true;
        }

        $.wire = wire;

        function unwire(source, sink, opts) {
                source = $(source);
                sink = $(sink);

                var sourceEl = source.get(0);
                var sinkEl = sink.get(0);

                var wires = sourceEl.wires;

                if (!wires) // can't unwire if it isn't wired
                        return false;

                opts = $.metadata ? $.extend({}, $.wireable.defaults, sink.metadata(),
                                source.metadata(),
                                sink.metadata().sink || {},
                                source.metadata().source || {},
                                opts
                        ) : $.extend({}, $.wireable.defaults, opts);

                for (i in wires) {
                        var wire = wires[i];

                        if (wire.info.source == sourceEl && wire.info.sink == sinkEl) {
                                // found the one we're looking for
                                if (!eventAllowed('unwiring', source, sink))
                                        return false;

                                // remove wire from source and sink
                                wires.splice(i, 1);
                                if (wires.length == 0)
                                        source.removeClass(opts.wiredClass);

                                wires = sinkEl.wires;
                                for (i in wires) {
                                        if (wires[i] == wire) {
                                                wires.splice(i, 1);
                                                if (wires.length == 0)
                                                        sink.removeClass(opts.wiredClass);
                                                break;
                                        }
                                }

                                // remove wire from the DOM (canvas)
                                $(wire).remove();

                                // remove wire from global list of wires
                                var id = getId(source) + ':' + getId(sink);
                                $.wireable.wired[id] = null;

                                // let the source and sink know the wire has been removed
                                var wiredEvent = $.Event('unwired');
                                wiredEvent.source = source;
                                wiredEvent.sink = sink;

                                source.trigger(wiredEvent);
                                sink.trigger(wiredEvent);

                                return true;
                        }
                }

                return false;
        }

        $.unwire = unwire;

        function cutHandler() {
                unwire(this.wire.info.source, this.wire.info.sink);
                hideCuts();
        }

        function hideCuts() {
                while (cuts.length) {
                        var cut = cuts[0];
                        cuts.splice(0, 1);
                        clearCutTimeout.call(cut);
                        $(cut).remove();
                }

                cuts = [];
        }

        function showCuts(opts) {
                if (drawingWire)
                        return;

                var terminal = this;

                hideCuts();

                for (i in terminal.wires) {
                        var wire = terminal.wires[i];

                        var isSource = terminal == wire.info.source;

                        var cutPoint = wire.info[isSource ? 'sourceCut' : 'sinkCut'];

                        var cut = $('<div></div>');
                        opts.container.append(cut);
                        cut.css({position:'absolute',visibility:'hidden',zIndex:'65535',cursor:'pointer',color:'#f00'});
                        cut.addClass(opts.cutClass);
                        cut.get(0).wire = wire;
                        cuts[cuts.length] = cut.get(0);

                        if (cut.width() == 0) {
                                var width = 16;
                                var height = 16;

                                cut.css({height:height+'px',width:width+'px'});

                                var canvas = document.createElement('canvas');
                                canvas.width = width;
                                canvas.height = height;
                                canvas.style.width = width + 'px';
                                canvas.style.height = height + 'px';

                                cut.append(canvas);

                                if (typeof G_vmlCanvasManager != 'undefined')
                                        canvas = G_vmlCanvasManager.initElement(canvas);

                                var ctx = canvas.getContext('2d');

                                ctx.beginPath();
                                ctx.moveTo(2, 2);
                                ctx.lineTo(14, 14);
                                ctx.moveTo(14, 2);
                                ctx.lineTo(2, 14);
                                ctx.lineCap = 'square';

                                ctx.lineWidth = 4;
                                ctx.strokeStyle = '#000';
                                ctx.stroke();

                                ctx.lineWidth = 2;
                                ctx.strokeStyle = '#f00';
                                ctx.stroke();
                        }

                        cut.css({
                                left:(wire.offsetLeft+cutPoint.x-cut.width()/2)+'px',
                                top:(wire.offsetTop+cutPoint.y-cut.height()/2)+'px',
                                visibility:'visible'
                        }).click(cutHandler);

                }
        }

        function clearCutTimeout() {
                if (this.timerId) {
                        clearTimeout(this.timerId);
                        this.timerId = null;
                }
        }

        function setCutTimer() {
                var cut = this;

                cut.timerId = setTimeout(function(){
                        clearCutTimeout.call(cut);
                        $(cut).remove();
                }, 1000);
        }

        function scheduleHideCut(cut) {
                $(cut).mouseenter(clearCutTimeout).mouseleave(setCutTimer);

                setCutTimer.call(cut);
        }

        function scheduleHideCuts() {
                for (i in cuts) {
                        scheduleHideCut(cuts[i]);
                }
        }

        function getId(t) {
                var id = t.attr('id');

                if (!id) {
                        if (!getId.counter)
                                getId.counter = 1;

                        id = 'wireable-auto-id-' + (getId.counter++);

                        t.attr('id', id);
                }

                return id;
        }

        var canvasBorder = 50;

        function draw(t1, t2, opts) {
                var id = getId(t1) + ':' + getId(t2);

                var canvas = $.wireable.wired[id];

                var p1 = t1.offset();
                var x1 = p1.left + Math.round(t1.width() / 2);
                var y1 = p1.top + Math.round(t1.height() / 2);

                var p2 = t2.offset();
                var x2 = p2.left + Math.round(t2.width() / 2);
                var y2 = p2.top + Math.round(t2.height() / 2);

                var adjustX = Math.min(x1, x2);
                var adjustY = Math.min(y1, y2);

                var left = Math.min(x1, x2) - canvasBorder;
                var top = Math.min(y1, y2) - canvasBorder;
                var width = Math.abs(x2 - x1) + canvasBorder * 2;
                var height = Math.abs(y2 - y1) + canvasBorder * 2;

                var containerOffset = opts.container.offset();
                left -= containerOffset.left;
                top -= containerOffset.top;
                left += opts.container.scrollLeft();
                top += opts.container.scrollTop();

                var ctx;

                if (!canvas) {
                        canvas = document.createElement('canvas');
                        canvas.id = id;
                        canvas.width = width;
                        canvas.height = height;
                        canvas.style.left = left + 'px';
                        canvas.style.top = top + 'px';
                        canvas.style.width = width + 'px';
                        canvas.style.height = height + 'px';
                        canvas.style.position = 'absolute';

                        opts.container.append(canvas);

                        if (typeof G_vmlCanvasManager != 'undefined')
                                canvas = G_vmlCanvasManager.initElement(canvas);

                        $.wireable.wired[id] = canvas;
                } else {
                        ctx = canvas.getContext('2d');
                        ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
                        $(canvas).css( {
                                left : left + 'px',
                                top : top + 'px',
                                width : width + 'px',
                                height : height + 'px'
                        }).attr( {
                                width : width,
                                height : height
                        });
                }

                x1 += canvasBorder - adjustX;
                y1 += canvasBorder - adjustY;
                x2 += canvasBorder - adjustX;
                y2 += canvasBorder - adjustY;

                opts.drawFunction.call(canvas, x1, y1, x2, y2, opts);

                return canvas;
        }

})(jQuery);