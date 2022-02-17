<?php
//get the q parameter from URL
$q=$_GET["q"];

//find out which feed was selected
if($q=="Google") {
  $xml=("https://news.google.com/rss/search?q=corona%2019%20when%3A1h&hl=id&gl=ID&ceid=ID%3Aid");
} elseif($q=="ZDN") {
  $xml=("https://trends.google.com/trends/trendingsearches/daily/rss?geo=ID");
}

$xmlDoc = new DOMDocument();
$xmlDoc->load($xml);


//get and output "<item>" elements
$x=$xmlDoc->getElementsByTagName('item');
for ($i=0; $i<=15; $i++) {
  $item_title=$x->item($i)->getElementsByTagName('title')
  ->item(0)->childNodes->item(0)->nodeValue;
  $item_link=$x->item($i)->getElementsByTagName('link')
  ->item(0)->childNodes->item(0)->nodeValue;
  $item_date=$x->item($i)->getElementsByTagName('pubDate')
  ->item(0)->childNodes->item(0)->nodeValue;
  $item_from=$x->item($i)->getElementsByTagName('source')
  ->item(0)->childNodes->item(0)->nodeValue;
  date_default_timezone_set('Asia/Jakarta');  // Set timezone.

  $utc_ts = strtotime($item_date);  // UTC Unix timestamp.
  $item_date = date('d M H:i T', $utc_ts);
  $day = date('y-m-d', $utc_ts);
  $week = array("Minggu" , "Senin"  , "Selasa" , "Rabu" , "Kamis" , "Jumat" ,"Saptu") ;
  $weekday = $week[ date('w'  , strtotime($day)  ) ];
  $strTok =explode(' - ' , $item_title);
  $item_title=$strTok[0];


  echo ("<p class='pb-3 mb-10 big lh-125 border-bottom border-gray'>");
  echo ("<strong class='small d-block text-gray-dark'>".$item_from." ".$weekday." ".$item_date."</strong>");
  echo ("<a href='".$item_link."' target='_blank' >".$item_title."</a></p>");


}
?>
