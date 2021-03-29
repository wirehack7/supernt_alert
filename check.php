<html>
<head>
<title>Is it running?</title>
</head>
<body>
<?php

function isPidRunning($pid) {
  $lines_out = array();
  exec('ps '.(int)$pid, $lines_out);
  if(count($lines_out) >= 2) {
    // Process is running
    return true;
  }
  return false;
}

# set path to the log file
$file = '/path/to/supernt_alert/alerting.log';

$str = fgets(fopen($file, 'r'));
$re = '/[0-9]{5,6}/';

if(preg_match($re, $str, $matches)){
        if(isPidRunning($matches[0])){
                echo "Script is running\n\n";
        }else{
                echo "Script is <b>not</b> running\n\n";
        }
}

echo "<pre>\n\n";

# replace with your telegram id, avoid to data leakage
echo str_replace('000000000', 'telegram_id', file_get_contents($file));
echo "\n</pre>\n\n";
?>
</body>
</html>
