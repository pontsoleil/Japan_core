package wuwei.japan_core.utils;

import java.util.AbstractMap;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class CustomComparator implements Comparator<String> {
    @Override
    public int compare(String o1, String o2) {
        List<Map.Entry<Integer, Integer>> entries1 = Arrays.stream(o1.split(" "))
            .map(pair -> pair.split("="))
            .filter(keyValue -> keyValue.length > 1 && !keyValue[1].equals("0"))
            .map(keyValue -> new AbstractMap.SimpleEntry<>(Integer.parseInt(keyValue[0]), Integer.parseInt(keyValue[1])))
            .sorted(Map.Entry.comparingByKey())
            .collect(Collectors.toList());

        List<Map.Entry<Integer, Integer>> entries2 = Arrays.stream(o2.split(" "))
            .map(pair -> pair.split("="))
            .filter(keyValue -> keyValue.length > 1 &&!keyValue[1].equals("0"))
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

