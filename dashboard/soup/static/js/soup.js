$.ajaxSetup({async:false});

$(document).ready(function() {

    cellwidth = (((document.width - ($('.soup-zone .soup-network').length * 3)) / $('.soup-zone .soup-table2').length) | 0) - 1;

    $('.soup-zone .soup-block2').css('width',cellwidth+"px");

    sum = 0; 
    $('.soup-zone .soup-network').each(function(i,o) { 
        sum += $(o).width() + 2; 
    }); 
    $('.soup-zone').width(sum);

//    counter = 0;
//    $('.soup-zone .soup-network').last().find('td').each(function(i) { 
//        if (counter <= 10) {
//console.log("lolz");
//console.log(this);
//	    $(this).tooltip({placement:"bottom"}); 
//        } else {
//            $(this).tooltip({placement:"left"}); 
//        }
//        counter++;
//    });
//
//    counter = 0;
//    $('.soup-zone .soup-network').find('td').each(function(i) { 
//        if (counter <= 10) {
//console.log("wat");
//console.log(this);
//	    $(this).tooltip({placement:"bottom"}); 
//        } else {
//            $(this).tooltip({placement:"right"}); 
//        }
//        counter++;
//    });
	$('.soup-zone .soup-network').last().find('.soup-table2').each(function(i,t) {
		counter = 0;
		$(t).find('td').each(function(k,d) {
				if (counter <= 10) {
					$(d).tooltip({placement:"bottom"});
				} else {
					$(d).tooltip({placement:"left"});
				}
				counter++;
		});
	});
	$('.soup-table2').each(function(i,t) {
	    counter = 0
		$(t).find('td').each(function(k,d) {
				if (counter <= 10) {
					$(this).tooltip({placement:"bottom"});
				} else {
					$(this).tooltip({placement:"right"});
				}
				counter++;
		});
	});

    refresh();
});

function setcell(obj) {
    tdclass = "soup-host-none";
    // Host is ARPable
    if (obj.arp == 1) { tdclass = "soup-host-arp"; }
    // Host is Pingable
    if (obj.ping == 1) { tdclass = "soup-host-ping"; }
    // Host is not registered but is either ARPable or Pingable
    if (obj.reg == 0 && (obj.arp == 1||obj.ping == 1)) { tdclass = "soup-host-unknown"; }
    // Host is in a reserved range but not registered
    if (obj.warn == 1 && (obj.arp == 1||obj.ping == 1)) { tdclass = "soup-host-warning"; }
    // Host is registered but is neither ARPable or Pingable
    if (obj.reg ==  1 && obj.arp == 0 && obj.ping == 0) { tdclass = "soup-host-dead"; }

    box = $(document.getElementById(obj.address))
    if (!box.hasClass(tdclass)) {
        box.attr('class','soup-block2');
        box.addClass(tdclass)
    }

    arptext = "No";
    if (obj.arp == 1) { arptext = "Yes"; }
    pingtext = "No";
    if (obj.ping == 1) { pingtext = "Yes"; }
    regtext = "No";
    if (obj.reg == 1) { regtext = "Yes"; }

    titletext = "Address: "+obj.address+"\nSubnet: "+obj.subnet+"\nIP Range: "+obj.range+"\nARP: "+arptext+"\nPing: "+pingtext+"\nRegistered: "+regtext

    box.attr('title',titletext);
    box.tooltip('fixTitle');

    if (tdclass != "soup-host-none") {
	box.unbind("click");
        box.click(function() {
            $.get("/starrs/"+obj.address, function(returl) {
                window.open(returl, '_blank');
            });
        });
    }
}

//function refresh() {
//    $('.soup-block2').each(function() {
//        ip = $(this).attr('id');
//        $.get("/status/"+ip, function(statobject) {
//            setcell(statobject);
//        });
//    });
//}

function refresh() {
    $.getJSON("/status2", function(data) {
        $.each(data, function(k, v) {
            setcell(v);
        });
    });
    $('.soup-loading').toggle();
}
