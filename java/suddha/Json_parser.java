import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Json_parser {
    public static void main(String args[] ) throws Exception {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT */
        Scanner input = new Scanner(System.in);
        List<String> lines = new ArrayList<String>();
        String lineNew;
        int i = 0;

        while (input.hasNextLine()) {
            lineNew = input.nextLine();
            if (lineNew.isEmpty()) {
                break;
            }
            //System.out.println(lineNew);
            lines.add(lineNew);
        }

        // System.out.println("Content of List<String> lines:");
        //for (String string : lines) {
        //    System.out.println(string);
        // }

        // for (i=0;i<lines.size();i++) {
        //     System.out.println(lines.get(i));
        // }

        //System.out.println(lines.get(1));

        //String regex_code = ".*Satta*.*";

        // boolean matches = Pattern.matches(regex_code, "Suddha Satta Ray");

        // enrollment
        for (i=0;i<lines.size();i++){
            if (Pattern.matches(".*enrollment.*", lines.get(i))== true){
                String s = lines.get(i);
                // remove all spaces 
                s = s.replaceAll("\\s","");
                System.out.println(s);
                // remove all "enrolment" 
                s = s.replaceAll("enrollment","");
                System.out.println(s);
                s = s.replaceAll("[\]"\:\,"","");
            }
        }

    }
}