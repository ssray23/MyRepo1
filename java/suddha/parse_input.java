import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

import sun.security.util.Length;

public class Solution {
    public static void main(String args[] ) throws Exception {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT */
        BufferedReader br;
        br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        //System.out.println(line);
        //System.out.println(line.length());
        char[] charArray = new char[line.length()];
        char[] charArray2 = new char[line.length()];
        char[] charArray3 = new char[line.length()];
        String output_string = "";
        int j = 0;
        int k = 0;


        for (int i=0;i<line.length();i++){
           //System.out.println(line.charAt(i)); 
           charArray[i] = line.charAt(i);
           if ((line.charAt(i) != '{') && (line.charAt(i) != '}') && (line.charAt(i) != '[') && (line.charAt(i) != ']') && (line.charAt(i) != '(') && (line.charAt(i) != ')')){charArray2[j]=line.charAt(i);j++;}
           if ((line.charAt(i) == '{') && (line.charAt(i) == '}') && (line.charAt(i) == '[') && (line.charAt(i) == ']') && (line.charAt(i) == '(') && (line.charAt(i) == ')')){charArray3[k]=line.charAt(i);k++;}
        }

        // System.out.println(charArray); //  ok
        // System.out.println(charArray2); // ok
        // System.out.println(charArray3); // ok
        // System.out.println(charArray2.toString()); // prints garbage?

        int count_curly_open=0, count_curly_close=0, count_square_open=0, count_square_close=0, count_curve_close=0, count_curve_open=0;

         for (int i=0;i<line.length();i++){
           //System.out.println(line.charAt(i)); 
           if (charArray[i] == '[') {
               count_square_open = ++count_square_open;
           }
           if (charArray[i] == ']') {
               count_square_close = ++count_square_close;
           }
           if (charArray[i] == '(') {
               count_curve_open = ++count_curve_open;
           }
           if (charArray[i] == ')') {
               count_curve_close = ++count_curve_close;
           }
           if (charArray[i] == '{') {
               count_curly_open = ++count_curly_open;
           }
           if (charArray[i] == '}') {
               count_curly_close = ++count_curly_close;
           }
        }

        //System.out.println("count_curly_open = " + Integer.toString(count_curly_open));
        //System.out.println("count_curly_close = " + Integer.toString(count_curly_close));

        if ((count_curly_open == count_curly_close) && (count_square_open == count_square_close) && (count_curve_open == count_curve_close)){ 
            output_string = "Y";
        }
        else {output_string = "N";}

        output_string = output_string + " " ;
        System.out.print(output_string);
        System.out.println(charArray3);

    } // main



} // solution