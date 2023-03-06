java -p "C:\Users\nobuy\GitHub\Japan_core\bin" -m wuwei.japan_core/wuwei.japan_core.cius.Invoice2csv SME-COMMON data/csv/Example1_SME.xml data/csv/Example1_SME.csv

java -p "C:\Users\nobuy\GitHub\Japan_core\bin" -m wuwei.japan_core/wuwei.japan_core.cius.Csv2invoice JP-PINT data/csv/Example1_PINT.csv data/csv/Example1_PINT.xml

java -classpath target/core-japan-0.0.1.jar wuwei.japan_core.cius.Invoice2csv SME-COMMON data/xml/Example1_SME.xml data/csv/Example1_SME.csv