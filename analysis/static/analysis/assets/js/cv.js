function writeSend() {
	if (!$('#title').val())
	{
		alert("제목을 입력해 주시기 바랍니다.");
		return;
	}

	if (!$('#content').val())
	{
		alert("내용을 입력해 주시기 바랍니다.");
		return;
	}

  	if (!$('#job').val())
  	{
    		alert("직무를 선택해 주시기 바랍니다.");
    		return;
	}

  	if (!$('#ability').val())
  	{
    		alert("직무역량을 선택해 주시기 바랍니다.");
    		return;
	}


	$('#write_form').submit();	
}