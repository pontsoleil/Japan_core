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
$contents = file_get_contents("data/xml/Example1_PINT.xml");
echo(escaped_entities($contents));
