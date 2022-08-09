$(document).ready(function() {
	$('#title').focus();

	$('.article-view').each(function() {
		var article_id = $(this);
		$.ajax({
			type: "GET",
			url: "/comm_view/"+$(this).data('id'),
			success: function(response) {
				article_id.html(response);
			},
		});	
	});
});

}

function replyClick(reply_id) {
	$('.reply-reply').each(function() {
		$(this).css('display','none');
	});

	$('.reply-reply[data-id='+reply_id+']').css('display','block');
}

var inProgress = false;
