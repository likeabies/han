$(document).ready(function() {
	$('input').keydown(function(e) {
		if (e.which == 13)
		{
			$('form').submit();
		}
	});
});

function login() {
	if (!$('#username').val())
	{
		alert("아이디를 입력해주세요.");
		return;
	}
	if (!$('#password').val()) {
		alert("비밀번호를 입력해주세요.");
		return;
	}

	$('#login_form').submit();
}