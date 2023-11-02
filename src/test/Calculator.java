package test;

public class Calculator {

    public static void main(String[] args) {
        Calculator calculator = new Calculator();
        int sum = calculator.add(2, 3);
        System.out.println("Sum: " + sum);
    }

    public int add(int a, int b) {
        return a + b;
    }
}
