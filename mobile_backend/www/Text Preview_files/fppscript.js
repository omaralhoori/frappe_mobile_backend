
			/*$(window).scroll(function () {
			  var s = $(window).scrollTop(),
					d = $(document).height(),
					c = $(window).height();
					scrollPercent = (s / (d-c)) * 100;
					var position = scrollPercent;

			   $("#progressbar").attr('value', position);
			}); */
			
				$(".q1").click(function(){
				$("#progress-num").text("0%");
				$("#progressbar").attr('value', "0");
				});
				$(".q2").click(function(){
				$("#progress-num").text("5%");
				$("#progressbar").attr('value', "5");
				});
				$(".q3").click(function(){
				$("#progress-num").text("10%");
				$("#progressbar").attr('value', "10");
				});
				$(".q4").click(function(){
				$("#progress-num").text("25%");
				$("#progressbar").attr('value', "25");
				});
				$(".q5").click(function(){
				$("#progress-num").text("35%");
				$("#progressbar").attr('value', "35");
				});
				$(".q6").click(function(){
				$("#progress-num").text("40%");
				$("#progressbar").attr('value', "40");
				});
				$(".q7").click(function(){
				$("#progress-num").text("50%");
				$("#progressbar").attr('value', "50");
				});
				$(".google").click(function(){
				$("#progress-num").text("60%");
				$("#progressbar").attr('value', "60");
				});
				$(".caloppa").click(function(){
				$("#progress-num").text("70%");
				$("#progressbar").attr('value', "70");
				});
				$(".coppa").click(function(){
				$("#progress-num").text("80%");
				$("#progressbar").attr('value', "80");
				});
				$(".fairinfo").click(function(){
				$("#progress-num").text("90%");
				$("#progressbar").attr('value', "90");
				});
				$(".canspam").click(function(){
				$("#progress-num").text("95%");
				$("#progressbar").attr('value', "95");
				});
				$(".final").click(function(){
				$("#progress-num").text("100%");
				$("#progressbar").attr('value', "100");
				});

				$(document).ready(function() {
				$('#tooltip1').tooltip();
				$('#tooltip2').tooltip();
				$('#tooltip3').tooltip();
				$('#tooltip-google').tooltip();
				$('#tooltip-caloppa').tooltip();
				$('#tooltip-coppa').tooltip();
				$('#tooltip-fair').tooltip();
				$('#tooltip-canspam').tooltip();
				$("[data-toggle=tooltip]").tooltip();
		
				});
		