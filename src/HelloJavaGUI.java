import javax.swing.*;
import com.suddha.*;

public class HelloJavaGUI {

    public static void main( String[] args ) {
        JFrame frame = new JFrame( "Hello, Java!" );

        Car myCar = new Car("Mini Cooper", 2012);
        //System.out.println(myCar.PrintCar1());
        JLabel label1 = new JLabel(myCar.PrintCar1(), JLabel.CENTER );
        frame.add(label1);
        frame.setSize( 300, 300 );
        frame.setVisible( true );
    }
}
