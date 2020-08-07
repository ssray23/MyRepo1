package com.suddha;

import java.util.Scanner;

public class AddNumbers{

    public static void main(final String[] args) {

        int num1, num2, sum;

        final Scanner sc = new Scanner(System.in);

        System.out.println("Enter First Number: ");
        num1 = sc.nextInt();

        System.out.println("Enter Second Number: ");
        num2 = sc.nextInt();

        System.out.println("Enter a Noun : ");
        final String myNoun = sc.next();

        System.out.println("Enter a Verb : ");
        final String myVerb = sc.next();

        sc.close();
        
        sum = num1 + num2;
        System.out.println("Sum of your entered numbers: "+sum);

        System.out.println("Sentence using your noun and verb: " + myNoun + " " + myVerb + ".");
    }
}