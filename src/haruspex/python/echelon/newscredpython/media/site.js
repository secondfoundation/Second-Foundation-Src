function slide() {
  var $active = $('div#slideshow img.active');

    if ($active.length == 0) {
    $active = $('div#slideshow img:last');
  }

  $active.fadeOut(500, function() {
      var $next =  $active.next().length ? $active.next() : $('div#slideshow img:first');
    $next.fadeIn(500).addClass("active");
  }).removeClass("active");
}

$(function() {
    setInterval("slide()", 5000);
});

showVideoPopUp = function(embed_code)
{
   dimensions = getVideoDimensions(embed_code)
   newWindow= window.open ("", "","status=1,width="+dimensions[0]+",height="+dimensions[1]+",resizable=1");
   var doc = newWindow.document;
   doc.open("text/html", "replace");
   doc.write(embed_code);
   doc.close();
}

getVideoDimensions = function(embed_code)
{
  width  = embed_code.match(/width="[\d]+"/gi).toString().match(/[\d]+/)[0]
  height = embed_code.match(/height="[\d]+"/gi).toString().match(/[\d]+/)[0]
  
  return new Array(parseInt(width,10) + 10, parseInt(height,10) + 10);
}

$(document).ready(function()
{
  $('img.video_thumbnail').click(function()
  {
    embed_code = $(this).siblings('span.video_embed_code').text();
    showVideoPopUp(embed_code);
    return;
  });
  
  $('a.video_title').click(function()
  {
    embed_code = $(this).parent().siblings('span.video_embed_code').text();
    showVideoPopUp(embed_code);
    return;
  });
});