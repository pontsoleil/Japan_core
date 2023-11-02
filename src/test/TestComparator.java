package test;

import java.util.*;
// import java.util.Map.Entry;
import java.util.stream.Collectors;

public class TestComparator {

    static TreeMap<String, TreeMap<Integer, String>> rowMapList = new TreeMap<>(new CustomComparator());

    public static void main(String[] args) {
        // テストデータの追加と出力
        rowMapList.put("1=1 365=0 454=0 533=0", new TreeMap<>());
        rowMapList.put("1=1 365=1 454=0 533=0", new TreeMap<>());
        rowMapList.put("1=1 365=1 454=0 533=1", new TreeMap<>());
        rowMapList.put("1=1 365=1 454=0 533=2", new TreeMap<>());
        rowMapList.put("1=1 365=1 454=1 533=0", new TreeMap<>());

        for (Map.Entry<String, TreeMap<Integer, String>> entry : rowMapList.entrySet()) {
            System.out.println(entry.getKey());
        }
    }
}

class CustomComparator implements Comparator<String> {
    @Override
    public int compare(String o1, String o2) {
        List<Map.Entry<Integer, Integer>> entries1 = Arrays.stream(o1.split(" "))
            .map(pair -> pair.split("="))
            .filter(keyValue -> !keyValue[1].equals("0"))
            .map(keyValue -> new AbstractMap.SimpleEntry<>(Integer.parseInt(keyValue[0]), Integer.parseInt(keyValue[1])))
            .sorted(Map.Entry.comparingByKey())
            .collect(Collectors.toList());

        List<Map.Entry<Integer, Integer>> entries2 = Arrays.stream(o2.split(" "))
            .map(pair -> pair.split("="))
            .filter(keyValue -> !keyValue[1].equals("0"))
            .map(keyValue -> new AbstractMap.SimpleEntry<>(Integer.parseInt(keyValue[0]), Integer.parseInt(keyValue[1])))
            .sorted(Map.Entry.comparingByKey())
            .collect(Collectors.toList());

        for (int i = 0; i < Math.min(entries1.size(), entries2.size()); i++) {
            int keyComparison = entries1.get(i).getKey().compareTo(entries2.get(i).getKey());
            if (keyComparison != 0) {
                return keyComparison;
            }

            int valueComparison = entries1.get(i).getValue().compareTo(entries2.get(i).getValue());
            if (valueComparison != 0) {
                return valueComparison;
            }
        }

        return Integer.compare(entries1.size(), entries2.size());
    }
}
