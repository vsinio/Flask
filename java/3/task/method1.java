package task;

import java.util.Scanner;

public class Method1 {

    public void method() {
        int x = 0;
        while (x != 1) {
            System.out.println("Введите число: ");
            Scanner scan = new Scanner(System.in);
            String num = scan.nextLine();

            try {
                float number = Float.parseFloat(num);
                System.out.println(number);
                System.out.println("Все верно, идем дальше!");
                x = 1;

            } catch (Exception NumberFormat) {
                System.out.println("Exception NumberFormat: Строки вводить нельзя, попробуйте ещё раз!");
            }
        }
    }
}