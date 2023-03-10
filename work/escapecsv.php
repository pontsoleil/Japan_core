<?php
function escaped_entities($string) {
  return strtr(
      $string, 
      array(
        " " => "&nbsp;",
        "\n" => "<br/>",
        "<" => "&lt;",
        ">" => "&gt;",
        '"' => "&quot;",
        "'" => "&apos;",
        "&" => "&amp;",
      )
  );
}
chdir(__DIR__);
$contents = file_get_contents("data/csv/Example1_PINT.csv");
echo(escaped_entities($contents));
