segments_normal = [];
segments_delay = [];
//for(var i=0;i<Segments.length;i++)
    //Segments[i]=0;
SegTrainList_normal = [];
SegTrainList_delay = [];
function updateSegments_normal(seg, tr_id){
    var tmp;
    if (seg){
	for(i in seg){
	    //if(tr_id  == "18110" && seg[0]!=[]) alert(i + " : " + seg[i].seg_no + " : " + seg[i].seg_label);
	    if(seg[i].seg_label==0){
		if( SegTrainList_normal[seg[i].seg_no].indexOf(tr_id)==-1){
		    segments_normal[seg[i].seg_no]++;Ccolor_normal(seg[i].seg_no);
		    SegTrainList_normal[seg[i].seg_no].push(tr_id);
		}else alert(tr_id+"Train already present. "+SegTrainList_normal[seg[i].seg_no]);
	    }
	    
	    if(seg[i].seg_label==2){
		if((tmp=SegTrainList_normal[seg[i].seg_no].indexOf(tr_id))>-1){
		    SegTrainList_normal[seg[i].seg_no].splice(tmp, 1);
		    segments_normal[seg[i].seg_no]--;
		    Ccolor_normal(seg[i].seg_no);
		}else alert(tr_id +"Train is not Found. " + SegTrainList_normal[seg[i].seg_no]+" " + tmp);
	    }
	}
    }
}

function updateSegments_delay(seg, tr_id){
    var tmp;
    if (seg){
	for(i in seg){
	    //if(tr_id  == "18110" && seg[0]!=[]) alert(i + " : " + seg[i].seg_no + " : " + seg[i].seg_label);
	    if(seg[i].seg_label==0){
		if( SegTrainList_delay[seg[i].seg_no].indexOf(tr_id)==-1){
		    segments_delay[seg[i].seg_no]++;Ccolor_delay(seg[i].seg_no);
		    SegTrainList_delay[seg[i].seg_no].push(tr_id);
		}else alert(tr_id+"Train already present. "+SegTrainList_delay[seg[i].seg_no]);
	    }
	    
	    if(seg[i].seg_label==2){
		if((tmp=SegTrainList_delay[seg[i].seg_no].indexOf(tr_id))>-1){
		    SegTrainList_delay[seg[i].seg_no].splice(tmp, 1);
		    segments_delay[seg[i].seg_no]--;
		    Ccolor_delay(seg[i].seg_no);
		}else alert(tr_id +"Train is not Found. " + SegTrainList_delay[seg[i].seg_no]+" " + tmp);
	    }
	}
    }
}

function async_update_normal(seg, tr_id){
    var tmp;
    var i;
    if (seg){
		for(i in seg){
			//if(tr_id  == "18110" && seg[0]!=[]) alert(i + " : " + seg[i].seg_no + " : " + seg[i].seg_label);
			if(seg[i].seg_label!=2)
			{
				if( SegTrainList_normal[seg[i].seg_no].indexOf(tr_id)==-1)
				{
					segments_normal[seg[i].seg_no]++;Ccolor_normal(seg[i].seg_no);
					SegTrainList_normal[seg[i].seg_no].push(tr_id);
				}
			}
		}
	}
}

function async_update_delay(seg, tr_id){
    var tmp;
    var i;
    if (seg){
		for(i in seg){
			//if(tr_id  == "18110" && seg[0]!=[]) alert(i + " : " + seg[i].seg_no + " : " + seg[i].seg_label);
			if(seg[i].seg_label!=2){
				if( SegTrainList_delay[seg[i].seg_no].indexOf(tr_id)==-1){
				segments_delay[seg[i].seg_no]++;Ccolor_delay(seg[i].seg_no);
				SegTrainList_delay[seg[i].seg_no].push(tr_id);
				}
			}
		}
	}
}

var WeekDays = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
function Train(train, mode){
    this.reInitialize = function(){
	this.finished = 1;
	this.cur_stn = 0;
	this.startedAt=0;
	this.day=0;
    }

    this.Initialize = function(mode){
	this.mode = mode;
	this.id = train.tr_id;
	this.stn_list = train.stn_list;
	var l = this.stn_list.length;
	this.stn_list[l-1].sch_dep = this.stn_list[l-1].sch_arr;
	/*
	this.daysRun = [];
	for(i in WeekDays){
	    if(train.days.indexOf(WeekDays[i]) != 1)
		this.daysRun[i] = 1;
	    else this.daysRun[i] = 0;
	}
	*/	
	this.reInitialize();
    }
    this.Initialize(mode);

    this.start = function(c){
	
	//if(this.daysRun[Math.floor(c/1440)%7] == 1){
	    if(c%1440 > this.stn_list[0].sch_dep){
		this.day=0;
		this.startedAt = c;
		if(this.mode == 1)
			updateSegments_normal(this.stn_list[0].seg_list, this.id);
		else if(this.mode == 2)
			updateSegments_delay(this.stn_list[0].seg_list, this.id);
		this.cur_stn++;
		//if(this.id=="18110") alert("Starting again" + c/1440);
		//		this.	move(c);
	    }
	//}
	
    }
    
    this.move = function(c){
	if(this.cur_stn==0 && this.finished==1) {
	    this.start(c); return;
	}
	var s = this.cur_stn;
	t = this.day*1440 + this.stn_list[s].sch_dep - this.stn_list[0].sch_dep
	if(t < c-this.startedAt){
	    if (s==this.stn_list.length-1){
		this.finished = 1;
	    }
	    if(this.mode == 1)
			updateSegments_normal(this.stn_list[s].seg_list, this.id);
		else if(this.mode == 2)
			updateSegments_delay(this.stn_list[s].seg_list, this.id);
	    if(this.cur_stn<this.stn_list-1 && this.stn_list[this.cur_stn+1].sch_dep < this.stn_list[this.cur_stn].sch_dep){
		this.day++;
		if(this.id=="18110") alert("Day: "+ this.day);
	    }
	    this.cur_stn = (this.cur_stn+1)%this.stn_list.length;
	    //	    this.move(c);
	}
    }
    this.move_async = function(c){
		var s = 0;
		var g = 0;
		for(s = 0; s < this.stn_list.length; s++)
		{
			var t = this.stn_list[s].sch_dep - c;
			if(t>0)
			{
				if(s!=0)
				{
					if(this.mode == 1)
						async_update_normal(this.stn_list[s-1].seg_list, this.id);
					else if(this.mode == 2)
						async_update_delay(this.stn_list[s-1].seg_list, this.id);
					break;
				}
			}
		}
	}
};

var Segments, Trains_normal=[], Trains_delay = [];
$.getJSON("data/NewTrainStationWSegmentsWDays.min.json", function(json) {
	T = eval(json);
	for( i in T.trains){
	    Trains_normal[i] = new Train(T.trains[i].train, 1);
	}
    });
$.getJSON("data/NewTrainStationDetailWDelayWSegments.json", function(json) {
	T = eval(json);
	for( i in T){
	    Trains_delay[i] = new Train(T[i].train, 2)
	}
    });
$.getJSON("data/segments.js", function(json) {
	T = eval(json);
	Segments = T.segments;
	Initialize();
    });
var segNames = [];
$.getJSON("data/segmentName.js", function(json) {
	T = eval(json);
	segNames = T.segNames;
    });

function viewAsyncTraffic()
{
	Initialize();
	var i;
	for(i=0;i<Trains_normal.length;i++)
	{
		Trains_normal[i].move_async(clock);
	}
	for(i=0;i<Trains_normal.length;i++)
	{
		Trains_delay[i].move_async(clock);
	}		
	var s = 0; 
	for( i in segments_normal) s+= segments_normal[i];
    $("#SegTot_normal").html("Total running trains(MAP_NORMAL): " + s);
    
    s = 0; 
    for( i in segments_delay) s+= segments_delay[i];
    $("#SegTot_delay").html("Total running trains(MAP_DELAY) : " + s);
    
    busy3high_normal();
    busy3high_delay();
}
	
function Ccolor_normal(i){
    c = segments_normal[i];
    if (i in poly_seg_normal)   
	//poly_seg[i].setOptions({strokeColor: 'blue'});
	poly_seg_normal[i].setOptions({strokeWeight: (c/3) });
}
	
function Ccolor_delay(i){
    c = segments_delay[i];
    if (i in poly_seg_delay)   
	//poly_seg[i].setOptions({strokeColor: 'blue'});
	poly_seg_delay[i].setOptions({strokeWeight: (c/3) });
}

poly_seg_normal = [];
poly_seg_delay = [];
function Initialize() {
    stop = 1;
    var myOptions = {
	center: new google.maps.LatLng(22.5, 82),
	zoom: 5,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map_normal = new google.maps.Map(document.getElementById("map_normal"), myOptions);
    map_delay = new google.maps.Map(document.getElementById("map_delay"), myOptions);
    var c = [23,34,12];
    for(i=0;i<Segments.length;i++){
	segments_normal[i] = 0;
	SegTrainList_normal[i] = [];
	segments_delay[i] = 0;
	SegTrainList_delay[i] = [];
	var tmp = [];
	for(j in Segments[i].segment.seg_list)
	    tmp[j] = new google.maps.LatLng(
					    Segments[i].segment.seg_list[j].lat, 
					    Segments[i].segment.seg_list[j].lng
					    );
	//alert(tmp);
	var color = '#' + c[0].toString(16)+c[1].toString(16)+c[2].toString(16);
	c[i%3] = 100 + (c[i%3]*2) % 100;
	poly_seg_normal[i] = new google.maps.Polyline({
		path: tmp,  
		strokeColor: color,  
		strokeOpacity: 1.0,  
		strokeWeight: 2, 
		map: map_normal
	    });
    
    poly_seg_delay[i] = new google.maps.Polyline({
		path: tmp,  
		strokeColor: color,  
		strokeOpacity: 1.0,  
		strokeWeight: 2, 
		map: map_delay
	    });
    }
}
last = 0;clock=0;

/*
function Update(t,c){
    for(i=0;i<Trains_normal.length;i++){
		Trains_normal[i].move(clock);
	}
	for(i=0;i<Trains_delay.length;i++){
		Trains_delay[i].move(clock);
	}
    clock+=20;c+=20;
    //setTimeout("animate(0)",0);
    updateClock();
    setTimeout("Update("+t+","+c+")", 5)
}

function setStartPoint1(t){
    $("#time-line").html(Math.floor(t/60) + "::" + t%60);
    var c = clock%1440;
    if(t<c) {t+=1440;}
    for(i=0;i<Trains.length;i++)
	Trains[i].move(clock);
    clock+=20;c+=20;
    //setTimeout("animate(0)",0);
	updateClock();
}
function setStartPoint(t){
    $("#time-line").html(Math.floor(t/60) + "::" + t%60);
    var c = clock%1440;
    if(t<c) {t+=1440;}
    while(t<c){
	for(i=0;i<Trains.length/100;i++)
	    Trains[i].move(clock);
	clock+=20;c+=20;
    }
    updateClock();
}
*/

function showValue(value){
    $("#timeScale").html(value);
    t_incr = parseInt(value);
    //    alert(t_incr);
}

function showValueTime(value){
	$("#time-line").html(value);	
}

function setTime(){
	var str = $("#time-line").html();
	var t = str.split("::");
	clock = parseInt(t[0])*60 + parseInt(t[1]) - t_incr;
	updateClock();
}

function setOpacity(value) {
    var t = $("#overlay_normal");
    t.css("opacity", value);
    t = $("#overlay_delay");
    t.css("opacity", value);
    //    t.style.filter = 'alpha(opacity=' + value*10 + ')';
}

function reset(){
	Initialize();
    $("#SegTot_normal").html("Total running trains(MAP_NORMAL): 0");
    $("#SegTot_delay").html("Total running trains(MAP_DELAY) : 0");
    stop=1;
    document.getElementById("range").value = 6;
    showValue(6);
    clock=-t_incr;
    updateClock();
    var i;
    for(i=0;i<Segments.length;i++){
	segments_normal[i] = 0;
	segments_delay[i] = 0;
	SegTrainList_normal[i] = [];
	SegTrainList_delay[i] = [];
    }
    for(i=0;i<Trains_normal.length;i++){
        Trains_normal[i].reInitialize();
        //marker[i].setPosition(Trains[i].ptset[Trains[i].cur_stn]);
    }
    for(i=0;i<Trains_delay.length;i++){
        Trains_delay[i].reInitialize();
        //marker[i].setPosition(Trains[i].ptset[Trains[i].cur_stn]);
    }
}

function updateClock(){
    clock+=t_incr;
    var d = Math.floor(clock/1440);
    var h = Math.floor((clock%1440)/60);
    var m = clock%60;
    document.getElementById("time").innerHTML = "<b>Time</b>(day:hr::min)&nbsp " + d + " :: " + h + " :: " + m;
    var value;
    value = 0.3 + 0.3 * Math.cos(h*3.141/12);
    setOpacity(value);
}

var incr = 10;
var tick = 50;
var t_incr = 6;
var stop=1;
function animate(d) {
    if(stop==1) {return;}
    var i;
    for(i=0;i<Trains_normal.length;i++){
        Trains_normal[i].move(clock);
    }
    for(i=0;i<Trains_delay.length;i++){
        Trains_delay[i].move(clock);
    }
    updateClock();
    setTimeout("animate("+(d+incr)+")", tick);
    //setTimeout("showGraph()", tick*30);
    var s = 0; 
    for( i in segments_normal) s+= segments_normal[i];
    $("#SegTot_normal").html("Total running trains(MAP_NORMAL): " + s);
    s = 0; for( i in segments_delay) s+= segments_delay[i];
    $("#SegTot_delay").html("Total running trains(MAP_DELAY) : " + s);
}
//marker = [];
function start() {
    s = $("#anim").html();
    if(s=="Pause"){
	stop=1;
	//showGraph();
	$("#anim").html("Start");
    }
    else if(s=="Start"){
	$("#anim").html("Pause");
	stop=0;
	setTimeout("animate(0)",0);
    }
}

function showGraph(){
    $(function () 
      {
	  var d1 = [];
	  for (i in segments )
	      d1.push([i, segments[i]]);
	  $.plot($("#placeholder"), 
		 [{ data: d1, bars: { show: true }}]);
      });
}

function search(v){
    v = parseInt(v);
    if(v in segments){
	var s = Segments[v].segment;
	t = "<b>Name</b>: "+ s.seg_name + "<br/>";
	t+=segNames[v].list.join("->")+"<br/>";
	t+= "<b>Number of Trains</b>: " + segments[v];
	$("#segInfo").html(t);
    }
}

function search_seg(v){
	v = parseInt(v);
	if(v in segments){
		var s = Segments[v].segment;
		$("#segName").html("Segment Name: " + s.seg_name);
		$("#segInfo").html("Number of Running Trains: " + segments[v]);
	}
}

function sort_traffic(a,b){
	return b.traffic - a.traffic;
}
function segment_obj(sname, traffic, trn_list){
	this.sname = sname;
	this.traffic = traffic;
	this.trn_list = trn_list;
}

function busy3high_normal(){
	var busy1_name, busy2_name, busy3_name;
	var seg_traffic_array = new Array();
	
	/* Create an array of objects for various segments */
	for(var i in segments_normal){
		//alert(segments_normal[i]);
		var seg_obj = new segment_obj(Segments[i].segment.seg_name, segments_normal[i], SegTrainList_normal[i]);
		seg_traffic_array[i] = seg_obj;
	}
	
	
	/* Now sort them */
	seg_traffic_array.sort(sort_traffic);
	
	/* Display in HTML */
	$("#bus_seg_normal").children().remove(); 
	for(var i in seg_traffic_array){
		$("#bus_seg_normal").append('<li>'+'<b>'+seg_traffic_array[i].sname+'\t'+seg_traffic_array[i].traffic+'</b>'+'</li>');
		var s = '<li>';
		seg_traffic_array[i].trn_list.sort();
		for(var j in seg_traffic_array[i].trn_list)
		{
			s = s + seg_traffic_array[i].trn_list[j] + '\t';
			if((j % 10) == 9)
				s = s + "</li>" + "<li>";			
		}
		s = s + '</li>';
		$("#bus_seg_normal").append(s);
	}
	
	
}

function busy3high_delay(){
	var busy1_name, busy2_name, busy3_name;
	var busy1_info = 0, busy2_info = 0, busy3_info = 0;
	var seg_traffic_array = new Array();
	
	/* Create an array of objects for various segments */
	for(var i in segments_normal){
		//alert(segments_normal[i]);
		var seg_obj = new segment_obj(Segments[i].segment.seg_name, segments_delay[i], SegTrainList_delay[i]);
		seg_traffic_array[i] = seg_obj;
	}
	
	/* Now sort them */
	seg_traffic_array.sort(sort_traffic);
	
	/* Display in HTML */
	$("#bus_seg_delay").children().remove(); 
	for(var i in seg_traffic_array){
		$("#bus_seg_delay").append('<li>'+'<b>'+seg_traffic_array[i].sname+'\t'+seg_traffic_array[i].traffic+'</b>'+'</li>');
		var s = '<li>';
		seg_traffic_array[i].trn_list.sort();
		for(var j in seg_traffic_array[i].trn_list)
		{
			s = s + seg_traffic_array[i].trn_list[j] + '\t';
			if((j % 10) == 9)
				s = s + "</li>" + "<li>";			
		}
		s = s + '</li>';
		$("#bus_seg_delay").append(s);
	}
}
