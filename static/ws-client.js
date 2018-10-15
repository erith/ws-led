$(function() {

        var WEBSOCKET_ROUTE = "/ws";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
            }
        else if(window.location.protocol == "https:"){
            //Dataplicity
            var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE);
            }

        ws.onopen = function(evt) {
            $("#ws-status").html("Connected!!");
            };

        ws.onmessage = function(evt) {
            };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            };

	 $('#picker')
	 .farbtastic(function(c) {
		$("#color").val(c);
		var data = {'cmd':'led', 'data':c};
		ws.send(JSON.stringify(data));
	 })


	 /*

      $('#picker').farbtastic(function(e){
        var c   = hexToRgb(e)
        , h   = rgbToHsl(c.r,c.g,c.b)
        , r   = hslToRgb(h.h,h.s,h.l)
        ;

        $('#color').css({backgroundColor:e}).val(e);

		var str = JSON.stringify(r);
		alert(str);

        var url = "http://192.168.178.55/?red="+r.r+"&green="+r.g+"&blue="+r.b;
        $.get( url, function( data ) {});
      });
	  */

});