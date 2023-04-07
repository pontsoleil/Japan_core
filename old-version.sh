cd /ebs/www/sambuichi.jp/public_html/core-japan

cp index.html old-version/index.`date +'%Y-%m-%d'`.html
cp js/convert.js old-version/convert.`date +'%Y-%m-%d'`.js
cp css/main.css old-version/main.`date +'%Y-%m-%d'`.css

cp server/data/base/core_japan.csv old-version/core_japan.`date +'%Y-%m-%d'`.csv
cp server/data/base/jp_pint_binding.csv old-version/jp_pint_binding.`date +'%Y-%m-%d'`.csv
cp server/data/base/sme_binding.csv old-version/sme_binding.`date +'%Y-%m-%d'`.csv

cp server/csv2invoice.php old-version/csv2invoice.`date +'%Y-%m-%d'`.php
cp server/invoice2csv.php old-version/invoice2csv.`date +'%Y-%m-%d'`.php
cp server/source2target.php old-version/source2target.`date +'%Y-%m-%d'`.php

cp server/lib/core-japan-0.0.2-shaded.jar old-version/core-japan-0.0.2-shaded.`date +'%Y-%m-%d'`.jar
cp server/lib/core-japan-0.0.2.jar old-version/core-japan-0.0.2.jar.`date +'%Y-%m-%d'`.jar


ls old-version/*.`date +'%Y-%m-%d'`.*


cp ../core-dev/index.html .
cp ../core-dev/js/convert.js js
cp ../core-dev/css/main.css css

cp ../core-dev/server/data/base/core_japan.csv server/data/base
cp ../core-dev/server/data/base/jp_pint_binding.csv server/data/base
cp ../core-dev/server/data/base/sme_binding.csv server/data/base

cp ../core-dev/server/csv2invoice.php server
cp ../core-dev/server/invoice2csv.php server
cp ../core-dev/server/source2target.php server

cp ../core-dev/server/lib/core-japan-0.0.2-shaded.jar server/lib
cp ../core-dev/server/lib/core-japan-0.0.2.jar server/lib


cp ../core-japan/server/data/schema/data/standard/ReusableAggregateBusinessInformationEntity_SME.xsd old-version/inReusableAggregateBusinessInformationEntity_SMEdex.`date +'%Y-%m-%d'`.xsd
sudo cp server/data/schema/data/standard/ReusableAggregateBusinessInformationEntity_SME.xsd ../core-japan/server/data/schema/data/standard/


cd /ebs/www/sambuichi.jp/public_html/core-japan

cp server/data/base/core_japan.csv old-version/core_japan.`date +'%Y-%m-%d'`.csv
cp server/data/base/jp_pint_binding.csv old-version/jp_pint_binding.`date +'%Y-%m-%d'`.csv
cp server/data/base/sme_binding.csv old-version/sme_binding.`date +'%Y-%m-%d'`.csv

cp ~/tmp/base/core_japan.csv server/data/base
cp ~/tmp/base/jp_pint_binding.csv server/data/base
cp ~/tmp/base/sme_binding.csv server/data/base

cd /ebs/www/sambuichi.jp/public_html/core-japan

cp server/lib/core-japan-0.0.2-shaded.jar old-version/core-japan-0.0.2-shaded.`date +'%Y-%m-%d'`.jar
cp server/lib/core-japan-0.0.2.jar old-version/core-japan-0.0.2.`date +'%Y-%m-%d'`.jar

cp ~/tmp/core-japan-0.0.2-shaded.jar server/lib
cp ~/tmp/core-japan-0.0.2.jar server/lib

cd /ebs/www/sambuichi.jp/public_html/core-dev

cp ~/tmp/core-japan-0.0.2-shaded.jar server/lib
cp ~/tmp/core-japan-0.0.2.jar server/lib
